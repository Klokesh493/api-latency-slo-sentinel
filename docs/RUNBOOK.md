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
