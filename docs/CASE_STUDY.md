# Case study

A rollout reviewer needs to know whether a batch of API latency samples
exceeds a service target. Averages can hide slow requests. This project
evaluates p95 and p99 and returns a clear verdict.

The project started as a CSV tool. The HTTP interface supports callers that
already hold samples as JSON and shares the same evaluator so that the result
does not depend on the transport. The synthetic sample yields p95 and p99 of
1100 ms, above both default thresholds. A healthy synthetic batch exercises
the opposite decision. HTTP tests cover both decisions, malformed input,
oversized input, and the health endpoint.

The batch verdict does not describe how long a breach lasted or what caused
it. A production alert would need a measured request distribution, an
evaluation window, and an agreed paging policy.
