PYTHON ?= python3

.PHONY: verify
verify:
	$(PYTHON) -B -m unittest discover -v
	$(PYTHON) latency_sentinel.py sample_latency.csv
	$(PYTHON) latency_sentinel.py sample_latency.csv --prometheus

.PHONY: replay
replay:
	$(PYTHON) tools/replay_examples.py --report reports/replay.md
