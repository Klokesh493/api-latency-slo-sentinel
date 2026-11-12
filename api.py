"""HTTP interface for the latency SLO evaluator."""
import argparse
import json
import math
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Lock

from latency_sentinel import evaluate, prometheus_metrics

MAX_BODY = 65536
MAX_SAMPLES = 5000


class EvaluationServer(ThreadingHTTPServer):
    def __init__(self, address):
        super().__init__(address, Handler)
        self.metrics_lock = Lock()
        self.last_evaluation = None
        self.outcomes = {"ok": 0, "breach": 0, "rejected": 0}

    def record(self, outcome, result=None):
        with self.metrics_lock:
            self.outcomes[outcome] += 1
            if result is not None:
                self.last_evaluation = (time.time(), result)

    def metrics(self):
        with self.metrics_lock:
            lines = [
                "# HELP api_latency_evaluations_total Submitted evaluations by outcome.",
                "# TYPE api_latency_evaluations_total counter",
                *(f'api_latency_evaluations_total{{outcome="{key}"}} {count}'
                  for key, count in self.outcomes.items()),
                "# HELP api_latency_last_evaluation_timestamp_seconds Time of last accepted batch.",
                "# TYPE api_latency_last_evaluation_timestamp_seconds gauge",
            ]
            timestamp, result = self.last_evaluation or (0, None)
            lines.append(f"api_latency_last_evaluation_timestamp_seconds {timestamp}")
            if result is not None:
                lines.append(prometheus_metrics(result))
        return ("\n".join(lines) + "\n").encode()


class Handler(BaseHTTPRequestHandler):
    def reply_bytes(self, status, content_type, data):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def reply(self, status, payload):
        self.reply_bytes(status, "application/json", json.dumps(payload, allow_nan=False).encode())

    def reject(self, status, message):
        self.server.record("rejected")
        self.reply(status, {"error": message})

    def do_GET(self):
        if self.path == "/healthz":
            self.reply(200, {"status": "ok"})
        elif self.path == "/metrics":
            self.reply_bytes(200, "text/plain; version=0.0.4; charset=utf-8", self.server.metrics())
        else:
            self.reply(404, {"error": "route not found"})

    def do_POST(self):
        if self.path != "/evaluate":
            self.reply(404, {"error": "route not found"})
            return
        if self.headers.get_content_type() != "application/json":
            self.reject(415, "expected application/json")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length > MAX_BODY:
            self.reject(413, "request body too large")
            return
        if length <= 0:
            self.reject(400, "expected a request body")
            return
        try:
            payload = json.loads(self.rfile.read(length))
            samples = payload["latency_ms"]
            if not isinstance(samples, list) or not 1 <= len(samples) <= MAX_SAMPLES:
                raise ValueError
            if any(type(value) not in (int, float) or not math.isfinite(value)
                   or value < 0 for value in samples):
                raise ValueError
        except TimeoutError:
            self.reject(408, "request timed out")
            return
        except (KeyError, TypeError, ValueError, OverflowError):
            self.reject(400, "latency_ms must contain 1 to 5000 finite nonnegative numbers")
            return
        result = evaluate(samples)
        self.server.record(result["status"], result)
        self.reply(200, result)

    def setup(self):
        self.request.settimeout(5)
        super().setup()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    with EvaluationServer((args.host, args.port)) as server:
        server.serve_forever()
