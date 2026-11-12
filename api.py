"""HTTP interface for the latency SLO evaluator."""
import argparse
import json
import math
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from latency_sentinel import evaluate

MAX_BODY = 65536
MAX_SAMPLES = 5000


class Handler(BaseHTTPRequestHandler):
    def reply(self, status, payload):
        data = json.dumps(payload, allow_nan=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/healthz":
            self.reply(200, {"status": "ok"})
        else:
            self.reply(404, {"error": "route not found"})

    def do_POST(self):
        if self.path != "/evaluate":
            self.reply(404, {"error": "route not found"})
            return
        if self.headers.get_content_type() != "application/json":
            self.reply(415, {"error": "expected application/json"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length > MAX_BODY:
            self.reply(413, {"error": "request body too large"})
            return
        if length <= 0:
            self.reply(400, {"error": "expected a request body"})
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
            self.reply(408, {"error": "request timed out"})
            return
        except (KeyError, TypeError, ValueError, OverflowError):
            self.reply(400, {"error": "latency_ms must contain 1 to 5000 finite nonnegative numbers"})
            return
        self.reply(200, evaluate(samples))

    def setup(self):
        self.request.settimeout(5)
        super().setup()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    with ThreadingHTTPServer((args.host, args.port), Handler) as server:
        server.serve_forever()
