# Local verification

Command: `make verify`

Result: **PASS**

````text
python3 -B -m unittest discover -v
python3 latency_sentinel.py sample_latency.csv
{'p95': 1100.0, 'p99': 1100.0, 'status': 'breach'}
python3 latency_sentinel.py sample_latency.csv --prometheus
# HELP api_latency_p95_seconds Evaluated p95 latency in seconds.
# TYPE api_latency_p95_seconds gauge
api_latency_p95_seconds 1.1
# HELP api_latency_p99_seconds Evaluated p99 latency in seconds.
# TYPE api_latency_p99_seconds gauge
api_latency_p99_seconds 1.1
# HELP api_latency_slo_breach Whether the evaluated latency breached a threshold.
# TYPE api_latency_slo_breach gauge
api_latency_slo_breach 1
test_api_and_cli_share_evaluation (test_api.ApiTest) ... 127.0.0.1 - - [12/Nov/2026 11:42:19] "POST /evaluate HTTP/1.1" 200 -
127.0.0.1 - - [12/Nov/2026 11:42:19] "POST /evaluate HTTP/1.1" 200 -
ok
test_health (test_api.ApiTest) ... 127.0.0.1 - - [12/Nov/2026 11:42:19] "GET /healthz HTTP/1.1" 200 -
ok
test_rejects_invalid_samples (test_api.ApiTest) ... 127.0.0.1 - - [12/Nov/2026 11:42:19] "POST /evaluate HTTP/1.1" 400 -
127.0.0.1 - - [12/Nov/2026 11:42:19] "POST /evaluate HTTP/1.1" 400 -
127.0.0.1 - - [12/Nov/2026 11:42:19] "POST /evaluate HTTP/1.1" 400 -
127.0.0.1 - - [12/Nov/2026 11:42:19] "POST /evaluate HTTP/1.1" 400 -
127.0.0.1 - - [12/Nov/2026 11:42:19] "POST /evaluate HTTP/1.1" 400 -
ok
test_rejects_large_bodies (test_api.ApiTest) ... 127.0.0.1 - - [12/Nov/2026 11:42:19] "POST /evaluate HTTP/1.1" 413 -
ok
test_marks_latency_breach (test_latency_sentinel.LatencySentinelTest) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.511s

OK
````
