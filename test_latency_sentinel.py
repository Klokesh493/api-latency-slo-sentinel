import unittest

from latency_sentinel import evaluate


class LatencySentinelTest(unittest.TestCase):
    def test_marks_latency_breach(self):
        result = evaluate([120, 180, 240, 990, 1100], p95_limit=300, p99_limit=750)
        self.assertEqual(result["status"], "breach")


if __name__ == "__main__":
    unittest.main()
