# Api Latency Slo Sentinel runbook

## What the project does

During a rollout, engineers need a repeatable way to tell whether slow API responses cross service targets. The Sentinel evaluates tail latency from a batch of samples and returns a verdict that can be reviewed before continuing.

See the [architecture and data flow](ARCHITECTURE.md) and [project case study](CASE_STUDY.md).

## Run from a clean checkout

Use Python 3 and Make. Install the pinned developer tools in a local environment.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

Run a bundled scenario from the repository root.

```sh
python3 latency_sentinel.py sample_latency.csv
```

## Expected result

- Demo 1. `{'p95': 1100.0, 'p99': 1100.0, 'status': 'breach'}` [Baseline](../examples/Demo%201.stdout.txt)
- Demo 2. `9 lines of output. Open the baseline for the full result.` [Baseline](../examples/Demo%202.stdout.txt)

Run `make replay` to compare results with the baselines and regenerate the [replay report](../reports/replay.md).
The [rules page](RULES.md) links to the code behind the decision.

## Verify a change

Run `make check PYTHON=python` inside the virtual environment. This runs the application checks, Ruff lint, and the Bandit static gate.
The [development guide](DEVELOPMENT.md) explains the tools and the [local report](../reports/devsecops.md) records what passed.

## If a check fails

Run the first failing command on its own. For a replay mismatch, inspect the diff and compare the input, rule, and expected output before updating the baseline.
For a lint or Bandit finding, review the reported source line and rerun the relevant target.

## Golden note

Check that latency input is in milliseconds. The Prometheus export converts it to seconds. Use the HTTP health check to distinguish service availability from a breach verdict.

## Operating limits

Use the [case study](CASE_STUDY.md) to check assumptions before applying a result to a live environment.

## Reproduce an alert locally

1. Start `python3 api.py` and, in another terminal, start
   `prometheus --config.file=deploy/prometheus/prometheus.yml`.
2. Submit the breach batch from the [README](../README.md). Confirm that
   `/metrics` shows `api_latency_slo_breach 1` and a nonzero
   `api_latency_last_evaluation_timestamp_seconds`.
3. Open the local Prometheus Alerts page at `http://localhost:9090/alerts`.
   Allow up to 45 seconds for target discovery, scrape, and rule evaluation.
4. Submit `{"latency_ms":[90,110,125]}` using the same command. Verify that
   the breach gauge returns to zero and the breach alert clears.

| Alert or symptom | First response |
| --- | --- |
| `LatencySentinelFreshBreach` | Confirm p95/p99 and sample size in the originating batch. Compare the collection window to the rollout timeline before acting. |
| `LatencySentinelNoFreshBatch` | Check the sample producer and the last accepted timestamp. Inspect the rejection counter and validate the request payload. |
| `LatencySentinelScrapeDown` | Check `/healthz`, then confirm that Prometheus can reach `/metrics` at its configured target. |
| `/metrics` returns counters with no latency gauges | Submit a valid batch and scrape again. A restart clears the last evaluation. |

Run `make verify-monitoring` to replay alert conditions without waiting
through the five-minute freshness window.
