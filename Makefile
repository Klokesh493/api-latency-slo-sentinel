PYTHON ?= python3

.PHONY: verify
verify:
	$(PYTHON) -B -m unittest discover -v
	$(PYTHON) latency_sentinel.py sample_latency.csv
	$(PYTHON) latency_sentinel.py sample_latency.csv --prometheus

.PHONY: replay
replay:
	$(PYTHON) tools/replay_examples.py --report reports/replay.md
.PHONY: lint security check
lint:
	$(PYTHON) -m ruff check --config ruff.toml --no-cache .

security:
	$(PYTHON) -m bandit -q -ll -ii -r . -x ./.venv,./.git

check: verify lint security replay

PROMTOOL ?= promtool

.PHONY: verify-monitoring
verify-monitoring:
	$(PROMTOOL) check config deploy/prometheus/prometheus.yml
	$(PROMTOOL) test rules deploy/prometheus/alerts.test.yml
	metrics="$$($(PYTHON) latency_sentinel.py sample_latency.csv --prometheus)" && \
		printf '%s\n' "$$metrics" | $(PROMTOOL) check metrics
