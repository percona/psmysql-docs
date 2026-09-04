# OpenTelemetry component overview

Percona Server for MySQL 9.7 includes native OpenTelemetry (OTel) support. OTel is a vendor-neutral standard for observability data. Database administrators can stream metrics, traces, and logs directly to OTel-compatible platforms. This support removes the need for external scraping agents.

## OpenTelemetry support and Percona telemetry

Before you configure your environment, distinguish between two features in Percona Server:

| Feature | Purpose |
|---|---|
| OpenTelemetry (`component_telemetry`) | Sends performance metrics, traces, and logs to a collector you configure. This component uses the OpenTelemetry protocol (OTLP). Collectors include Grafana Tempo, Grafana Mimir, Datadog, and OTel Collector. |
| [Percona telemetry (`component_percona_telemetry`)](telemetry.md) | Collects anonymous deployment and usage statistics. Percona uses this data to prioritize bug fixes and feature development. Participation is optional. |

## Feature benefits

The `component_telemetry` component includes an OTLP exporter inside the database engine. This exporter uses a push model. Tools such as `mysqld_exporter` use a pull model instead. The push model reduces CPU and connection overhead.

`component_telemetry` covers the following areas:

* Metrics: Counters and gauges track query execution (`com_*` commands), thread activity, memory usage, and storage engine statistics. These metrics use standard OTel semantic conventions.

* Traces: Spans follow the query execution lifecycle. A trace groups related spans together. Traces help database administrators find bottlenecks across microservices and database operations.

* Logs: MySQL error and system log events stream as OTLP log records. Centralized log aggregation engines can collect these records.

Native OpenTelemetry support unifies observability across the application stack and the database stack. Teams do not need custom sidecar agents. TLS and token-based authentication secure telemetry data in transit.

## Limitations and known constraints

The OpenTelemetry component (`component_telemetry`) in Percona Server for MySQL 9.7 operates under specific network, protocol, and infrastructure requirements:

| Requirement | Description |
|---|---|
| gRPC Transport Unsupported | Native `grpc` protocol transport is not supported by any of the OTLP exporters. All telemetry streams (metrics, traces, and logs) strictly require HTTP transport. |
| Protocol Encoding Restrictions | Payload serialization is limited to `http/protobuf` (the default binary Protocol Buffers) and `http/json`. |
| HTTP/HTTPS Endpoint Requirements | All endpoint destination variables (`telemetry.otel_exporter_otlp_*_endpoint`) must be explicitly defined with `http://` or `https://` schemes targeting an OTLP/HTTP-compatible receiver port (typically port `4318`). |
| External Receiver Required for Logging and Telemetry | The database server does not retain, format, or render exported OTLP log records, traces, or metrics locally. An external receiver or telemetry collector (such as an OpenTelemetry Collector gateway, Percona Monitoring and Management, Grafana, or Datadog) must be actively running to ingest and process the outgoing HTTP payloads. |
| Push-Only Exporter | The component functions strictly as an active push exporter. It does not expose a pull-based endpoint for Prometheus-style metric scraping or incoming OTLP queries directly on the database instance. |