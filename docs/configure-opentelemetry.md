# Configure OpenTelemetry

Percona Server for MySQL 9.7 exports metrics, traces, and logs to an OpenTelemetry-compatible backend. The server uses OpenTelemetry Protocol (OTLP) over HTTP.

Install and verify the OpenTelemetry component before configuration. See [Install and manage the OpenTelemetry component](opentelemetry-lifecycle.md).

!!! note

    The OpenTelemetry component supports OTLP over HTTP. The component rejects OTLP over gRPC.

    The examples use the standard OTLP/HTTP port, `4318`.

    Replace the example address with the address of your collector or compatible backend.

## Before you begin

Confirm that the OpenTelemetry component is installed:

```sql
SELECT component_urn
FROM mysql.component
WHERE component_urn = 'file://component_telemetry';
```

Confirm that the server supports each signal you plan to export:

```sql
SHOW GLOBAL STATUS LIKE 'Telemetry%_supported';
```

The relevant status variables are:

| Status variable               | Purpose                                                     |
| ----------------------------- | ----------------------------------------------------------- |
| `Telemetry_metrics_supported` | Indicates whether the server supports OpenTelemetry metrics |
| `Telemetry_traces_supported`  | Indicates whether the server supports OpenTelemetry traces  |
| `Telemetry_logs_supported`    | Indicates whether the server supports OpenTelemetry logs    |

OpenTelemetry configuration variables have global scope. Some variables are dynamic. Exporter endpoints, protocols, and processor settings are startup-only.

Configure startup-only variables with `SET PERSIST_ONLY`. Then, restart the server.

You need the `SYSTEM_VARIABLES_ADMIN` privilege to change global system variables.

You also need `PERSIST_RO_VARIABLES_ADMIN` to persist startup-only variables.

## Configure metrics

Metrics telemetry periodically exports measurements from MySQL server meters to an OTLP-compatible endpoint.

### Set the metrics endpoint and enable metrics

Persist the endpoint and enable metrics at the next server start:

```sql
SET PERSIST_ONLY telemetry.otel_exporter_otlp_metrics_endpoint =
  'http://otel-collector.example.com:4318/v1/metrics';

SET PERSIST_ONLY telemetry.metrics_enabled = ON;
```

Restart Percona Server for MySQL to apply the settings.

!!! note

    `telemetry.metrics_enabled` and the metrics exporter variables are startup-only. `SET GLOBAL` rejects changes to these variables.

### Select the metrics protocol

The metrics exporter supports the following OTLP/HTTP encodings:

| Value           | Description                                                  |
| --------------- | ------------------------------------------------------------ |
| `http/protobuf` | Binary Protocol Buffers encoding. This value is the default. |
| `http/json`     | JSON encoding for decoded payload inspection                 |

To select an encoding, persist the setting and restart the server:

```sql
SET PERSIST_ONLY telemetry.otel_exporter_otlp_metrics_protocol =
  'http/protobuf';
```

### Configure metric collection and export timing

The following variables control meter reads and export timeouts:

| Variable                                       | Purpose                                                          |
| ---------------------------------------------- | ---------------------------------------------------------------- |
| `telemetry.metrics_reader_frequency_1`         | First meter-reading interval, in seconds                         |
| `telemetry.metrics_reader_frequency_2`         | Optional second meter-reading interval, in seconds               |
| `telemetry.metrics_reader_frequency_3`         | Optional third meter-reading interval, in seconds                |
| `telemetry.otel_exporter_otlp_metrics_timeout` | Maximum time to wait for a metrics batch export, in milliseconds |

These variables are startup-only. Persist any changes and restart the server:

```sql
SET PERSIST_ONLY telemetry.metrics_reader_frequency_1 = 10;
SET PERSIST_ONLY telemetry.metrics_reader_frequency_2 = 60;
SET PERSIST_ONLY telemetry.metrics_reader_frequency_3 = 0;
SET PERSIST_ONLY telemetry.otel_exporter_otlp_metrics_timeout = 10000;
```

## Configure traces

Trace telemetry records MySQL sessions and statement executions as spans.

A supported client or connector can propagate trace context for distributed traces.

### Set the traces endpoint and enable traces

Persist the exporter endpoint and trace setting:

```sql
SET PERSIST_ONLY telemetry.otel_exporter_otlp_traces_endpoint =
  'http://otel-collector.example.com:4318/v1/traces';

SET PERSIST_ONLY telemetry.trace_enabled = ON;
```

Restart Percona Server for MySQL to apply the endpoint.

`telemetry.trace_enabled` is dynamic. After the restart, enable or disable trace collection at runtime:

```sql
SET GLOBAL telemetry.trace_enabled = OFF;
SET GLOBAL telemetry.trace_enabled = ON;
```

Use `SET PERSIST` instead when the runtime change must survive a restart.

### Control SQL query text

Statement spans include the original SQL text by default. SQL text may contain sensitive values, such as passwords or personal information.

To omit SQL text from exported spans:

```sql
SET PERSIST telemetry.query_text_enabled = OFF;
```

`telemetry.query_text_enabled` is dynamic, so the change takes effect immediately and survives subsequent restarts.

!!! warning

    Other trace attributes may contain sensitive information after you disable query text.

    Review the exported attributes before you enable traces in production. Also review the collector retention and access policies.

### Select the traces protocol

The traces exporter supports `http/protobuf` and `http/json`. Persist a protocol change and restart the server:

```sql
SET PERSIST_ONLY telemetry.otel_exporter_otlp_traces_protocol =
  'http/protobuf';
```

### Configure trace batching

The component uses a Batch Span Processor (BSP) to buffer and export spans.

| Variable                                      |  Default | Purpose                                       |
| --------------------------------------------- | -------: | --------------------------------------------- |
| `telemetry.otel_bsp_schedule_delay`           |  5000 ms | Delay between consecutive trace exports       |
| `telemetry.otel_bsp_max_queue_size`           |     2048 | Maximum number of spans in the export queue   |
| `telemetry.otel_bsp_max_export_batch_size`    |      512 | Maximum number of spans in one export batch   |
| `telemetry.otel_exporter_otlp_traces_timeout` | 10000 ms | Maximum time to wait for a trace batch export |

These variables are startup-only. Persist changes and restart the server:

```sql
SET PERSIST_ONLY telemetry.otel_bsp_schedule_delay = 5000;
SET PERSIST_ONLY telemetry.otel_bsp_max_queue_size = 2048;
SET PERSIST_ONLY telemetry.otel_bsp_max_export_batch_size = 512;
SET PERSIST_ONLY telemetry.otel_exporter_otlp_traces_timeout = 10000;
```

### Understand the emitted spans

The component emits the following span types:

| Span type      | Description                                                 | Example attributes                                                                                                          |
| -------------- | ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Control span   | Reports changes to telemetry signal collection              | `trace_enabled`, `metrics_enabled`, `logs_enabled`                                                                          |
| Session span   | Records a client session when the session ends              | `mysql.processlist_id`, `mysql.thread_id`, `mysql.user`, `mysql.host`, `mysql.group`, `mysql.session_attr.<ATTRIBUTE_NAME>` |
| Statement span | Records a statement or protocol command when execution ends | `mysql.event_name`, `mysql.lock_time`, `mysql.sql_text`, `mysql.digest_text`, `mysql.current_schema`                        |

Statement spans can also include error details, affected-row counts, and resource-use measurements.

`mysql.sql_text` is included only when `telemetry.query_text_enabled` is `ON`.

## Configure logs

Log telemetry exports instrumented MySQL log records in OTLP format.

MySQL provides logger instruments for the following logs:

- Server error log

- Slow query log

- General query log

### Set the logs endpoint and enable logs

Persist the exporter endpoint and log setting:

```sql
SET PERSIST_ONLY telemetry.otel_exporter_otlp_logs_endpoint =
  'http://otel-collector.example.com:4318/v1/logs';

SET PERSIST_ONLY telemetry.log_enabled = ON;
```

Restart Percona Server for MySQL to apply the endpoint.

`telemetry.log_enabled` is dynamic. After the restart, enable or disable log export at runtime:

```sql
SET GLOBAL telemetry.log_enabled = OFF;
SET GLOBAL telemetry.log_enabled = ON;
```

Use `SET PERSIST` instead when the runtime change must survive a restart.

### Configure logger levels

Inspect the available logger instruments and their current levels:

```sql
SELECT NAME, LEVEL, DESCRIPTION
FROM performance_schema.setup_loggers;
```

Logger levels control which records qualify for export.

For example, set all configured loggers to the `WARN` level:

```sql
UPDATE performance_schema.setup_loggers
SET LEVEL = 'WARN';
```

Available levels are `NONE`, `ERROR`, `WARN`, `INFO`, and `DEBUG`.

### Select the logs protocol

The logs exporter supports `http/protobuf` and `http/json`. Persist a protocol change and restart the server:

```sql
SET PERSIST_ONLY telemetry.otel_exporter_otlp_logs_protocol =
  'http/protobuf';
```

### Configure log batching

The component uses a Batch Log Record Processor (BLRP) to buffer and export log records.

| Variable                                        |  Default | Purpose                                           |
| ----------------------------------------------- | -------: | ------------------------------------------------- |
| `telemetry.otel_blrp_schedule_delay`            |  5000 ms | Delay between consecutive log exports             |
| `telemetry.otel_blrp_max_queue_size`            |     2048 | Maximum number of log records in the export queue |
| `telemetry.otel_blrp_max_export_batch_size`     |      512 | Maximum number of log records in one export batch |
| `telemetry.otel_exporter_otlp_logs_timeout`     | 10000 ms | Maximum time to wait for a log batch export       |
| `telemetry.otel_exporter_otlp_logs_compression` |   `none` | Export compression: `none` or `gzip`              |

These variables are startup-only. Persist changes and restart the server:

```sql
SET PERSIST_ONLY telemetry.otel_blrp_schedule_delay = 5000;
SET PERSIST_ONLY telemetry.otel_blrp_max_queue_size = 2048;
SET PERSIST_ONLY telemetry.otel_blrp_max_export_batch_size = 512;
SET PERSIST_ONLY telemetry.otel_exporter_otlp_logs_timeout = 10000;
SET PERSIST_ONLY telemetry.otel_exporter_otlp_logs_compression = 'gzip';
```

## Secure exporter connections

The examples use `http://` to show each OTLP path. Use `https://` when telemetry crosses an untrusted network.

The component provides security settings for each signal. The settings include the following items:

- Trusted certificates

- Client certificates

- Client keys

- Headers

- Transport Layer Security (TLS) versions

- Cipher configuration

Use the variable prefix for the required signal:

- `telemetry.otel_exporter_otlp_metrics_*`

- `telemetry.otel_exporter_otlp_traces_*`

- `telemetry.otel_exporter_otlp_logs_*`

Keep authentication tokens out of commands, shell history, and broadly readable configuration.

Use the corresponding `*_secret_headers` variable when a configured secret provider is available.

## Verify the configuration

After restarting the server, inspect the active settings:

```sql
SHOW GLOBAL VARIABLES LIKE 'telemetry.%enabled';
SHOW GLOBAL VARIABLES LIKE 'telemetry.otel_exporter_otlp_%_endpoint';
SHOW GLOBAL VARIABLES LIKE 'telemetry.otel_exporter_otlp_%_protocol';
```

Confirm that the collector receives data at each configured endpoint:

- `/v1/metrics`

- `/v1/traces`

- `/v1/logs`

Check the collector logs when the collector does not receive an enabled signal.

Configure `telemetry.otel_log_level` to control diagnostics in the MySQL server error log.

The variable accepts `SILENT`, `ERROR`, `WARNING`, `INFO`, and `DEBUG`:

```sql
SET GLOBAL telemetry.otel_log_level = 'INFO';
```

`telemetry.otel_log_level` is dynamic. Use `DEBUG` only for troubleshooting. The `DEBUG` level can produce substantial output.

## Related reading

- [Install and manage the OpenTelemetry component](opentelemetry-lifecycle.md)

- [OpenTelemetry protocol specification](https://opentelemetry.io/docs/specs/otlp/)

- [OpenTelemetry Collector documentation](https://opentelemetry.io/docs/collector/)
