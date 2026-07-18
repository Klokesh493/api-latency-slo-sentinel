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
