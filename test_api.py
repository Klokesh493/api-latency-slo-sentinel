import http.client
import json
import threading
import unittest

from api import MAX_BODY, EvaluationServer
from latency_sentinel import evaluate


class ApiTest(unittest.TestCase):
    def setUp(self):
        self.server = EvaluationServer(("127.0.0.1", 0))
        self.worker = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.worker.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.worker.join()

    def request(self, method, path, body=None):
        client = http.client.HTTPConnection(*self.server.server_address, timeout=3)
        try:
            client.request(method, path, body, {"Content-Type": "application/json"})
            response = client.getresponse()
            body = response.read()
            if path == "/metrics":
                return response.status, response.getheader("Content-Type"), body.decode()
            return response.status, json.loads(body)
        finally:
            client.close()

    def test_health(self):
        self.assertEqual(self.request("GET", "/healthz"), (200, {"status": "ok"}))

    def test_api_and_cli_share_evaluation(self):
        for samples in ([120, 140, 160], [120, 300, 1100]):
            with self.subTest(samples=samples):
                status, result = self.request("POST", "/evaluate", json.dumps({"latency_ms": samples}))
                self.assertEqual(status, 200)
                self.assertEqual(result, evaluate(samples))

    def test_rejects_invalid_samples(self):
        for body in ('{}', '{"latency_ms":[-1]}', '{"latency_ms":[NaN]}',
                     '{"latency_ms":[true]}', '{"latency_ms":[]}'):
            with self.subTest(body=body):
                self.assertEqual(self.request("POST", "/evaluate", body)[0], 400)

    def test_rejects_large_bodies(self):
        self.assertEqual(self.request("POST", "/evaluate", " " * (MAX_BODY + 1))[0], 413)

    def test_scrape_tracks_outcomes_and_preserves_last_accepted_batch(self):
        status, content_type, initial = self.request("GET", "/metrics")
        self.assertEqual(status, 200)
        self.assertEqual(content_type, "text/plain; version=0.0.4; charset=utf-8")
        self.assertIn("api_latency_last_evaluation_timestamp_seconds 0\n", initial)
        self.assertNotIn("api_latency_p95_seconds", initial)
        self.request("POST", "/evaluate", '{"latency_ms":[90,110,125]}')
        self.request("POST", "/evaluate", '{"latency_ms":[1100]}')
        _, _, before_rejection = self.request("GET", "/metrics")
        self.request("POST", "/evaluate", '{"latency_ms":[-1]}')
        _, _, after_rejection = self.request("GET", "/metrics")
        self.assertEqual(
            after_rejection,
            before_rejection.replace('outcome="rejected"} 0', 'outcome="rejected"} 1'),
        )
        self.assertIn('api_latency_evaluations_total{outcome="ok"} 1', after_rejection)
        self.assertIn('api_latency_evaluations_total{outcome="breach"} 1', after_rejection)
        self.assertIn("api_latency_slo_breach 1\n", after_rejection)
        self.assertIn("api_latency_p99_seconds 1.1\n", after_rejection)
        self.assertTrue(after_rejection.endswith("\n"))
