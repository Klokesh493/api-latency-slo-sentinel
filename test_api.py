import http.client
import json
import threading
import unittest
from http.server import ThreadingHTTPServer

from api import Handler, MAX_BODY
from latency_sentinel import evaluate


class ApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.worker = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.worker.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.worker.join()

    def request(self, method, path, body=None):
        client = http.client.HTTPConnection(*self.server.server_address, timeout=3)
        try:
            client.request(method, path, body, {"Content-Type": "application/json"})
            response = client.getresponse()
            return response.status, json.loads(response.read())
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
