# Troubleshooting

| Symptom | Check |
| --- | --- |
| HTTP 400 | Send JSON with a nonempty `latency_ms` array of finite, nonnegative numbers. |
| HTTP 413 | Keep the serialized request at or below 64 KiB. |
| HTTP 415 | Set the request content type to `application/json`. |
| Pod cannot load the image | Build the image and load it into the kind cluster before applying the manifest. |
| No metrics in Prometheus | The CLI emits text to standard output. Check that the configured node_exporter textfile collector reads the generated `.prom` file. |
