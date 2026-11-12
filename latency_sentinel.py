import argparse
import csv


def percentile(values, pct):
    ordered = sorted(float(value) for value in values)
    index = round((len(ordered) - 1) * pct)
    return ordered[index]


def evaluate(values, p95_limit=300, p99_limit=750):
    p95 = percentile(values, 0.95)
    p99 = percentile(values, 0.99)
    status = "breach" if p95 > p95_limit or p99 > p99_limit else "ok"
    return {"p95": p95, "p99": p99, "status": status}


def prometheus_metrics(result):
    return "\n".join([
        "# HELP api_latency_p95_seconds Evaluated p95 latency in seconds.",
        "# TYPE api_latency_p95_seconds gauge",
        f"api_latency_p95_seconds {result['p95'] / 1000}",
        "# HELP api_latency_p99_seconds Evaluated p99 latency in seconds.",
        "# TYPE api_latency_p99_seconds gauge",
        f"api_latency_p99_seconds {result['p99'] / 1000}",
        "# HELP api_latency_slo_breach Whether the evaluated latency breached a threshold.",
        "# TYPE api_latency_slo_breach gauge",
        f"api_latency_slo_breach {int(result['status'] == 'breach')}",
    ])


def main(path, prometheus=False):
    with open(path, newline="", encoding="utf-8") as handle:
        values = [row["latency_ms"] for row in csv.DictReader(handle)]
    result = evaluate(values)
    print(prometheus_metrics(result) if prometheus else result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check API latency SLOs.")
    parser.add_argument("path")
    parser.add_argument("--prometheus", action="store_true", help="emit Prometheus metrics")
    args = parser.parse_args()
    try:
        main(args.path, args.prometheus)
    except (OSError, ValueError, KeyError, IndexError) as error:
        parser.error(str(error))
