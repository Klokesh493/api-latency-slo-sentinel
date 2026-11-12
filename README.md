# API Latency SLO Sentinel

Evaluates API latency samples against p95 and p99 SLO thresholds.

Focus: Consumer-scale SRE observability.

Built as a small, runnable Python project with clear input, output, sample data, and tests.

## Run

```bash
python3 latency_sentinel.py sample_latency.csv
```

## Verify

```bash
python3 -m unittest discover . -v
```

## Local verification

Run `make verify` with Make and Python 3 installed. The target runs the documented sample through the project CLI. It also runs the existing Python unit tests.

## Prometheus metrics

Run `python3 latency_sentinel.py sample_latency.csv --prometheus` for Prometheus text exposition. The output includes p95 and p99 latency in seconds and a breach gauge (1 for breach, 0 for healthy). To collect a scheduled snapshot with a node_exporter textfile collector, redirect the command to a temporary file in the configured collector directory, then rename it to `api_latency.prom` after the command succeeds. The CLI evaluates one CSV snapshot per run.
