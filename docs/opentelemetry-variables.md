# OpenTelemetry variable reference

Percona Server for MySQL 9.7 provides OpenTelemetry system and status variables. Use these variables for exporter configuration, security, and tuning. For configuration procedures, see [Configure OpenTelemetry](configure-opentelemetry.md).

The exporter uses OpenTelemetry Protocol (OTLP).

All variables have global scope.

Use the change method in each table:

| Change method | Result |
| --- | --- |
| Dynamic | Use `SET GLOBAL` for a runtime change. Use `SET PERSIST` to retain the change after a restart. |
| Startup | Use `SET PERSIST_ONLY` or configure the variable under `[mysqld]`. Restart the server to apply the change. |

## Enablement variables

Use the following variables to turn each telemetry signal on or off:

| Variable | Default | Change method | Description |
|---|---|---|---|
| `telemetry.trace_enabled` | `OFF` | Dynamic | Turns trace export on or off. |
| `telemetry.metrics_enabled` | `OFF` | Startup | Turns metrics export on or off. |
| `telemetry.log_enabled` | `OFF` | Dynamic | Turns log export on or off. |
| `telemetry.query_text_enabled` | `ON` | Dynamic | Includes raw SQL statement text in trace spans. Set to `OFF` to remove query text from trace payloads. |

## Global variables

| Variable | Default | Change method | Description |
|---|---|---|---|
| `telemetry.otel_log_level` | `ERROR` | Dynamic | Sets the log level for the telemetry component's internal diagnostic output. The variable accepts `SILENT`, `ERROR`, `WARNING`, `INFO`, and `DEBUG`. |
| `telemetry.otel_resource_attributes` | *(empty)* | Startup | Attaches resource metadata to all exported signals. Use comma-separated `key=value` pairs. |
| `telemetry.resource_provider` | *(none)* | Startup | Names a component that supplies OpenTelemetry resource data. The data depends on the provider implementation. |
| `telemetry.secret_provider` | *(none)* | Startup | Names a component that decodes secrets for exporter HTTP headers. The secret format depends on the provider implementation. |

## Endpoint and protocol variables

Each signal type (traces, metrics, logs) has a separate set of endpoint and protocol variables. Replace `<signal>` with `traces`, `metrics`, or `logs`.

| Variable | Default | Change method | Description |
|---|---|---|---|
| `telemetry.otel_exporter_otlp_<signal>_endpoint` | *(empty)* | Startup | Sets the OTLP/HTTP collector URL for this signal. |
| `telemetry.otel_exporter_otlp_<signal>_protocol` | `http/protobuf` | Startup | Sets the payload encoding to `http/protobuf` or `http/json`. |
| `telemetry.otel_exporter_otlp_<signal>_compression` | `none` | Startup | Sets the payload compression to `none` or `gzip`. |
| `telemetry.otel_exporter_otlp_<signal>_timeout` | `10000` ms | Startup | Sets the timeout for an export request. |
| `telemetry.otel_exporter_otlp_<signal>_headers` | *(empty)* | Startup | Adds HTTP headers to export requests. Header values can include authentication tokens. |
| `telemetry.otel_exporter_otlp_<signal>_secret_headers` | *(none)* | Startup | Names a secret that contains HTTP headers. Requires the component named by `telemetry.secret_provider`. |
| `telemetry.otel_exporter_otlp_<signal>_network_namespace` | *(none)* | Startup | Sets the Linux network namespace for export requests. This variable applies only on Linux. The `mysqld` binary must have the `CAP_SYS_ADMIN` capability. |

## Transport Layer Security and mutual TLS variables

Use Transport Layer Security (TLS) or mutual TLS (mTLS) to secure exporter connections. Each variable exists per signal type. Replace `<signal>` with `traces`, `metrics`, or `logs`.

| Variable | Default | Change method | Description |
|---|---|---|---|
| `telemetry.otel_exporter_otlp_<signal>_certificates` | *(empty)* | Startup | Sets the path to the certificate authority (CA) file used to verify the collector. |
| `telemetry.otel_exporter_otlp_<signal>_client_certificates` | *(empty)* | Startup | Sets the path to the client certificate file for mutual TLS (mTLS). |
| `telemetry.otel_exporter_otlp_<signal>_client_key` | *(empty)* | Startup | Sets the path to the client private key file for mTLS. |
| `telemetry.otel_exporter_otlp_<signal>_min_tls` | `default` | Startup | Sets the minimum TLS protocol version accepted. |
| `telemetry.otel_exporter_otlp_<signal>_max_tls` | `default` | Startup | Sets the maximum TLS protocol version accepted. |
| `telemetry.otel_exporter_otlp_<signal>_cipher` | *(TLS default list)* | Startup | Sets the allowed cipher list for TLS 1.2 and earlier. |
| `telemetry.otel_exporter_otlp_<signal>_cipher_suite` | *(TLS default list)* | Startup | Sets the allowed cipher suite list for TLS 1.3. |

!!! note

    A collector endpoint that uses plain HTTP does not require these TLS variables. Configure TLS variables only when the collector endpoint uses `https://`. Repeat the TLS settings for each signal that uses HTTPS.

## Batch processor tuning variables

Each signal type uses a separate batch processor. Trace spans use the Batch Span Processor (BSP). Log records use the Batch Log Record Processor (BLRP). Metrics use reader frequency variables instead of a batch processor.

### Trace tuning: BSP variables

| Variable | Default | Change method | Description |
|---|---|---|---|
| `telemetry.otel_bsp_schedule_delay` | `5000` ms | Startup | Sets the delay between consecutive batch span exports. |
| `telemetry.otel_bsp_max_queue_size` | `2048` | Startup | Sets the maximum number of spans held in the export queue. |
| `telemetry.otel_bsp_max_export_batch_size` | `512` | Startup | Sets the maximum number of spans sent per export request. |

### Log tuning: BLRP variables

| Variable | Default | Change method | Description |
|---|---|---|---|
| `telemetry.otel_blrp_schedule_delay` | `5000` ms | Startup | Sets the delay between consecutive batch log exports. |
| `telemetry.otel_blrp_max_queue_size` | `2048` | Startup | Sets the maximum number of log records held in the export queue. |
| `telemetry.otel_blrp_max_export_batch_size` | `512` | Startup | Sets the maximum number of log records sent per export request. |

### Metrics tuning: reader frequency variables

| Variable | Default | Change method | Description |
|---|---|---|---|
| `telemetry.metrics_reader_frequency_1` | `10` seconds | Startup | Collects meters with a `FREQUENCY` value less than or equal to 10 seconds. Reader one is required. |
| `telemetry.metrics_reader_frequency_2` | `10` seconds | Startup | Collects meters above the reader one threshold and at or below the reader two threshold. A value of `0` disables this reader. |
| `telemetry.metrics_reader_frequency_3` | `10` seconds | Startup | Collects meters above the reader two threshold. A value of `0` disables this reader. |

The configured value sets both the meter threshold and the collection interval. See [Configure metric reader frequencies](configure-opentelemetry.md#configure-metric-reader-frequencies) for an example.

## Status variables

Status variables report the state of the telemetry component. You cannot set status variables.

| Variable | Type | Description |
| --- | --- | --- |
| `telemetry.live_sessions` | Integer | Reports the number of server sessions that telemetry currently instruments. |
| `telemetry.run_level` | Enumeration | Reports the current component initialization state. The value is `READY` when initialization completes. |
| `Telemetry_logs_supported` | Boolean | Reports whether the server binary supports OpenTelemetry logs. |
| `Telemetry_metrics_supported` | Boolean | Reports whether the server binary supports OpenTelemetry metrics. |
| `Telemetry_traces_supported` | Boolean | Reports whether the server binary supports OpenTelemetry traces. |

## Related reading

- [OpenTelemetry component overview](opentelemetry-overview.md)

- [Quickstart: test OpenTelemetry locally](quickstart-opentelemetry.md)

- [Install and manage the OpenTelemetry component](opentelemetry-lifecycle.md)

- [Configure OpenTelemetry](configure-opentelemetry.md)

- [OpenTelemetry client plugin](opentelemetry-client.md)

- [OpenTelemetry data reference](opentelemetry-data-reference.md)

- [Troubleshoot OpenTelemetry](troubleshoot-opentelemetry.md)

