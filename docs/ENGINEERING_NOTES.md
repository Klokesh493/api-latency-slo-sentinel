# Skills and verification

## What this repository demonstrates

Percentile monitoring, bounded HTTP input, Prometheus instrumentation, and alert recovery.

## Reproduce the result

Run `make verify` and `make verify-monitoring`. The checks exercise HTTP submission, rejected input, metrics, and freshness-aware alert rules. Reproduce the primary fixture with `python3 latency_sentinel.py sample_latency.csv`.

Run `make verify` locally. Ruff and Bandit medium/high checks passed for the checked Python code.

## Scope

A live scrape was demonstrated on loopback. Docker and Kubernetes assets require runtime validation.

[latency_sentinel.py](../latency_sentinel.py) · [examples/Demo 1.stdout.txt](../examples/Demo%201.stdout.txt) · [Architecture](../docs/ARCHITECTURE.md) · [Case study](../docs/CASE_STUDY.md) · [Runbook](../docs/RUNBOOK.md) · [CI template](../docs/github-actions/ci.yml)
