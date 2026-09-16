# OpenTelemetry component overview

Percona Server for MySQL 9.7 includes native OpenTelemetry (OTel) support. OTel is a vendor-neutral standard for observability data. Database administrators can stream metrics, traces, and logs directly to OTel-compatible platforms. This support removes the need for external scraping agents.

## OpenTelemetry support and Percona telemetry

Before you configure your environment, distinguish between two features in Percona Server:

| Feature | Purpose |
|---|---|
| OpenTelemetry (`component_telemetry`) | Sends performance metrics, traces, and logs to a collector you configure. This component uses OpenTelemetry Protocol (OTLP). Compatible collectors include Grafana Tempo, Grafana Mimir, Datadog, and OpenTelemetry Collector. |
| [Percona telemetry (`component_percona_telemetry`)](telemetry.md) | Collects anonymous deployment and usage statistics. Percona uses this data to prioritize bug fixes and feature development. Participation is optional. |

## Feature benefits

The `component_telemetry` component includes an OTLP exporter inside the database engine. This exporter uses a push model. Other tools, such as [`mysqld_exporter`](https://github.com/prometheus/mysqld_exporter), use a pull model.

| Model | Who starts the transfer | Example |
| --- | --- | --- |
| Push | The server sends OTLP data to a collector | `component_telemetry` |
| Pull | A scraper requests metrics from an HTTP endpoint | Prometheus and `mysqld_exporter` |

A push exporter can reduce extra database connections. A pull exporter often runs as a sidecar process. That sidecar opens its own connections to collect `SHOW STATUS` and similar data.

For the OpenTelemetry definitions, see [Push metric exporter](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#push-metric-exporter) and [Pull metric exporter](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#pull-metric-exporter). For the Prometheus pull design, see [Why do you pull rather than push?](https://prometheus.io/docs/introduction/faq/#why-do-you-pull-rather-than-push).

`component_telemetry` covers the following areas:

* Metrics: Counters and gauges track query execution (`Com_*` counters), thread activity, memory usage, and storage engine statistics. These metrics follow the OpenTelemetry data model. For the model, see the [OpenTelemetry observability primer](https://opentelemetry.io/docs/concepts/observability-primer/) and the [OpenTelemetry metrics data model](https://opentelemetry.io/docs/specs/otel/metrics/data-model/). For the metrics that Percona Server for MySQL exports, see [OpenTelemetry data reference](opentelemetry-data-reference.md).

* Traces: Spans follow the query execution lifecycle. A trace groups related spans together. Traces help database administrators find bottlenecks across microservices and database operations.

* Logs: Error log, slow query log, and general query log records stream as OTLP log records. Centralized log aggregation engines can collect these records.

Native OpenTelemetry support unifies observability across the application stack and the database stack. Teams do not need custom sidecar agents. TLS and token-based authentication secure telemetry data in transit.

The `mysql` command-line client can export traces with the `telemetry_client` plugin. That plugin is separate from `component_telemetry`. See [OpenTelemetry client plugin](opentelemetry-client.md).

## Limitations and known constraints

The OpenTelemetry component (`component_telemetry`) in Percona Server for MySQL 9.7 operates under specific network, protocol, and infrastructure requirements:

| Requirement | Description |
|---|---|
| gRPC Transport Unsupported | Native `grpc` protocol transport is not supported by any of the OTLP exporters. All telemetry streams (metrics, traces, and logs) strictly require HTTP transport. |
| Protocol Encoding Restrictions | Payload serialization is limited to `http/protobuf` (the default binary Protocol Buffers) and `http/json`. |
| HTTP/HTTPS Endpoint Requirements | All endpoint destination variables (`telemetry.otel_exporter_otlp_*_endpoint`) must be explicitly defined with `http://` or `https://` schemes targeting an OTLP/HTTP-compatible receiver port (typically port `4318`). |
| External Receiver Required for Logging and Telemetry | The database server does not retain, format, or render exported OTLP log records, traces, or metrics locally. An external receiver or telemetry collector (such as an OpenTelemetry Collector gateway, Percona Monitoring and Management, Grafana, or Datadog) must be actively running to ingest and process the outgoing HTTP payloads. |
| Push-Only Exporter | The component functions strictly as an active push exporter. The component does not expose a pull-based endpoint for [Prometheus-style metric scraping](https://prometheus.io/docs/instrumenting/exporters/) or incoming OTLP queries on the database instance. |

## Related reading

- [Quickstart: test OpenTelemetry locally](quickstart-opentelemetry.md)

- [Install and manage the OpenTelemetry component](opentelemetry-lifecycle.md)

- [Configure OpenTelemetry](configure-opentelemetry.md)

- [OpenTelemetry client plugin](opentelemetry-client.md)

- [OpenTelemetry variable reference](opentelemetry-variables.md)

- [OpenTelemetry data reference](opentelemetry-data-reference.md)

- [Troubleshoot OpenTelemetry](troubleshoot-opentelemetry.md)

- [OpenTelemetry observability primer](https://opentelemetry.io/docs/concepts/observability-primer/)

- [OpenTelemetry metrics data model](https://opentelemetry.io/docs/specs/otel/metrics/data-model/)

- [OpenTelemetry push metric exporter](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#push-metric-exporter)

- [OpenTelemetry pull metric exporter](https://opentelemetry.io/docs/specs/otel/metrics/sdk/#pull-metric-exporter)

- [Prometheus: Why do you pull rather than push?](https://prometheus.io/docs/introduction/faq/#why-do-you-pull-rather-than-push)
