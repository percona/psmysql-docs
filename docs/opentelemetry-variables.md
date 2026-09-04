# OpenTelemetry system variable reference

This page lists all `telemetry.*` system variables in Percona Server for MySQL 9.7. Use this page as a reference for TLS configuration and tuning. For basic setup steps, see [Configure OpenTelemetry](configure-opentelemetry.md).

All variables in this list have global scope. All variables are dynamic. Set a variable with `SET GLOBAL`, or add the variable to your `my.cnf` file under `[mysqld]` to persist the setting across restarts.

## Enablement variables

Use the following variables to turn each telemetry signal on or off:

| Variable | Default | Description |
|---|---|---|
| `telemetry.trace_enabled` | `ON` | Turns trace export on or off. |
| `telemetry.metrics_enabled` | `ON` | Turns metrics export on or off. |
| `telemetry.log_enabled` | `ON` | Turns log export on or off. |
| `telemetry.query_text_enabled` | `ON` | Includes raw SQL statement text in trace spans. Set to `OFF` to remove query text from trace payloads. |

## Global variables

| Variable | Default | Description |
|---|---|---|
| `telemetry.otel_log_level` | `info` | Sets the log level for the telemetry component's internal diagnostic output. |
| `telemetry.otel_resource_attributes` | *(empty)* | Attaches resource-level metadata to all exported signals, such as environment name or service name. Use comma-separated `key=value` pairs. |

## Endpoint and protocol variables

Each signal type (traces, metrics, logs) has a separate set of endpoint and protocol variables. Replace `<signal>` with `traces`, `metrics`, or `logs`.

| Variable | Default | Description |
|---|---|---|
| `telemetry.otel_exporter_otlp_<signal>_endpoint` | `http://localhost:4318/v1/<signal>` | Sets the OTLP/HTTP collector URL for this signal. |
| `telemetry.otel_exporter_otlp_<signal>_protocol` | `http/protobuf` | Sets the payload encoding: `http/protobuf` or `http/json`. |
| `telemetry.otel_exporter_otlp_<signal>_compression` | `none` | Sets the payload compression scheme: `none` or `gzip`. |
| `telemetry.otel_exporter_otlp_<signal>_timeout` | `10000` ms | Sets the timeout for an export request. |
| `telemetry.otel_exporter_otlp_<signal>_headers` | *(empty)* | Adds custom HTTP headers to export requests, for example authentication tokens. |

## TLS and mTLS variables

Use the following variables to secure the connection between the server and your OTLP collector. Each variable exists per signal type. Replace `<signal>` with `traces`, `metrics`, or `logs`.

| Variable | Default | Description |
|---|---|---|
| `telemetry.otel_exporter_otlp_<signal>_certificates` | *(empty)* | Sets the path to the CA certificate file used to verify the collector. |
| `telemetry.otel_exporter_otlp_<signal>_client_certificates` | *(empty)* | Sets the path to the client certificate file for mutual TLS (mTLS). |
| `telemetry.otel_exporter_otlp_<signal>_client_key` | *(empty)* | Sets the path to the client private key file for mTLS. |
| `telemetry.otel_exporter_otlp_<signal>_min_tls` | `default` | Sets the minimum TLS protocol version accepted. |
| `telemetry.otel_exporter_otlp_<signal>_max_tls` | `default` | Sets the maximum TLS protocol version accepted. |
| `telemetry.otel_exporter_otlp_<signal>_cipher` | *(TLS default list)* | Sets the allowed cipher list for TLS 1.2 and earlier. |
| `telemetry.otel_exporter_otlp_<signal>_cipher_suite` | *(TLS default list)* | Sets the allowed cipher suite list for TLS 1.3. |

!!! note

    A collector endpoint that uses plain HTTP does not require these TLS variables. Configure TLS variables only when the collector endpoint uses HTTPS.

## Batch processor tuning variables

Each signal type uses a separate batch processor. Trace spans use the Batch Span Processor (BSP). Log records use the Batch Log Record Processor (BLRP). Metrics use reader frequency variables instead of a batch processor.

### Trace tuning: BSP variables

| Variable | Default | Description |
|---|---|---|
| `telemetry.otel_bsp_schedule_delay` | `5000` ms | Sets the delay between consecutive batch span exports. |
| `telemetry.otel_bsp_max_queue_size` | `2048` | Sets the maximum number of spans held in the export queue. |
| `telemetry.otel_bsp_max_export_batch_size` | `512` | Sets the maximum number of spans sent per export request. |

### Log tuning: BLRP variables

| Variable | Default | Description |
|---|---|---|
| `telemetry.otel_blrp_schedule_delay` | `5000` ms | Sets the delay between consecutive batch log exports. |
| `telemetry.otel_blrp_max_queue_size` | `2048` | Sets the maximum number of log records held in the export queue. |
| `telemetry.otel_blrp_max_export_batch_size` | `512` | Sets the maximum number of log records sent per export request. |

### Metrics tuning: reader frequency variables

| Variable | Default | Description |
|---|---|---|
| `telemetry.metrics_reader_frequency_1` | `10` seconds | Sets the export interval for the first metric reader. |
| `telemetry.metrics_reader_frequency_2` | `60` seconds | Sets the export interval for the second metric reader. |
| `telemetry.metrics_reader_frequency_3` | `0` seconds | Sets the export interval for the third metric reader. A value of `0` turns this reader off. |
