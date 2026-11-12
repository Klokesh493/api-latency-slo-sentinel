# Verification

`make verify` passed the HTTP and CLI checks.

```text
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
```

Docker, Kubernetes, and GitHub Actions require separate execution checks.
