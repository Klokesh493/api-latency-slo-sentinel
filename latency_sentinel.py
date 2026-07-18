import csv
import sys


def percentile(values, pct):
    ordered = sorted(float(value) for value in values)
    index = round((len(ordered) - 1) * pct)
    return ordered[index]


def evaluate(values, p95_limit=300, p99_limit=750):
    p95 = percentile(values, 0.95)
    p99 = percentile(values, 0.99)
    status = "breach" if p95 > p95_limit or p99 > p99_limit else "ok"
    return {"p95": p95, "p99": p99, "status": status}


def main(path):
    with open(path, newline="", encoding="utf-8") as handle:
        values = [row["latency_ms"] for row in csv.DictReader(handle)]
    result = evaluate(values)
    print(result)


if __name__ == "__main__":
    main(sys.argv[1])
