# Replay evidence

Captured stdout is compared with a checked-in baseline.

## Demo 1

Result: **PASS**

````text
{'p95': 1100.0, 'p99': 1100.0, 'status': 'breach'}
````

## Demo 2

Result: **PASS**

````text
# HELP api_latency_p95_seconds Evaluated p95 latency in seconds.
# TYPE api_latency_p95_seconds gauge
api_latency_p95_seconds 1.1
# HELP api_latency_p99_seconds Evaluated p99 latency in seconds.
# TYPE api_latency_p99_seconds gauge
api_latency_p99_seconds 1.1
# HELP api_latency_slo_breach Whether the evaluated latency breached a threshold.
# TYPE api_latency_slo_breach gauge
api_latency_slo_breach 1
````
