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

OpenTelemetry configuration variables have global scope. The `telemetry.trace_enabled`, `telemetry.log_enabled`, `telemetry.query_text_enabled`, and `telemetry.otel_log_level` variables are dynamic.

All other telemetry variables are startup-only, including exporter endpoints, protocols, certificate settings, batch settings, metrics settings, and resource attributes. For the change method of each variable, see [OpenTelemetry variable reference](opentelemetry-variables.md).

Configure startup-only variables with `SET PERSIST_ONLY`. Then, restart the server.

You need the `SYSTEM_VARIABLES_ADMIN` privilege to change global system variables.

You also need `PERSIST_RO_VARIABLES_ADMIN` to persist startup-only variables.

## Configure metrics

Metrics telemetry periodically exports measurements from the server meters to an OTLP-compatible endpoint.

### Set the metrics endpoint and enable metrics

Persist the endpoint and enable metrics at the next server start:

```sql
SET PERSIST_ONLY telemetry.otel_exporter_otlp_metrics_endpoint =
  'http://otel-collector.example.com:4318/v1/metrics';

SET PERSIST_ONLY telemetry.metrics_enabled = ON;
```

Restart the server to apply the settings.

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

### Configure meters

The `performance_schema.setup_meters` table controls each meter. You can change the `FREQUENCY` and `ENABLED` columns at runtime.

The following statement disables the MyISAM meter:

```sql
UPDATE performance_schema.setup_meters
SET ENABLED = 'NO'
WHERE NAME = 'mysql.myisam';
```

The following statement assigns a 60-second frequency to the `mysql.inno` meter:

```sql
UPDATE performance_schema.setup_meters
SET FREQUENCY = 60
WHERE NAME = 'mysql.inno';
```

Use the `performance-schema-meter` option to configure a meter at server startup. You can specify the option more than once.

```ini
[mysqld]
performance-schema-meter='mysql.inno=frequency:60,enabled:ON'
performance-schema-meter='mysql.myisam=frequency:60,enabled:OFF'
```

The command-line form is `--performance-schema-meter='<METER_NAME>=frequency:<SECONDS>,enabled:ON|OFF'`.

The `performance_schema_max_meter_classes` variable sets the maximum number of meter instruments. This variable is startup-only.

### Configure metric reader frequencies

The component assigns each meter to a metric reader. The meter's `FREQUENCY` value determines the assignment.

| Reader | Meter selection | Collection interval |
| ------ | --------------- | ------------------- |
| `telemetry.metrics_reader_frequency_1` | `FREQUENCY` is less than or equal to reader one | Reader one value |
| `telemetry.metrics_reader_frequency_2` | `FREQUENCY` is greater than reader one and less than or equal to reader two | Reader two value |
| `telemetry.metrics_reader_frequency_3` | `FREQUENCY` is greater than reader two | Reader three value |

Reader one is required. Readers two and three are optional. A value of `0` disables an optional reader.

For example, configure the readers with intervals of 10, 60, and 300 seconds:

```sql
SET PERSIST_ONLY telemetry.metrics_reader_frequency_1 = 10;
SET PERSIST_ONLY telemetry.metrics_reader_frequency_2 = 60;
SET PERSIST_ONLY telemetry.metrics_reader_frequency_3 = 300;
```

The configuration assigns meters as follows:

| Meter `FREQUENCY` | Assigned reader | Collection interval |
| ----------------: | --------------- | ------------------: |
| 10 seconds | Reader one | 10 seconds |
| 30 seconds | Reader two | 60 seconds |
| 120 seconds | Reader three | 300 seconds |

The reader interval controls the collection schedule. A meter can have a smaller `FREQUENCY` value than its reader interval.

All metric reader variables are startup-only. Persist changes and restart the server.

Set the metrics export timeout and compression separately:

```sql
SET PERSIST_ONLY telemetry.otel_exporter_otlp_metrics_timeout = 10000;
SET PERSIST_ONLY telemetry.otel_exporter_otlp_metrics_compression = 'gzip';
```

The timeout uses milliseconds. Compression accepts `none` or `gzip`.

## Configure traces

Trace telemetry records client sessions and statement executions as spans.

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

| Variable                                             |  Default | Purpose                                       |
| ---------------------------------------------------- | -------: | --------------------------------------------- |
| `telemetry.otel_bsp_schedule_delay`                  |  5000 ms | Delay between consecutive trace exports       |
| `telemetry.otel_bsp_max_queue_size`                  |     2048 | Maximum number of spans in the export queue   |
| `telemetry.otel_bsp_max_export_batch_size`           |      512 | Maximum number of spans in one export batch   |
| `telemetry.otel_exporter_otlp_traces_timeout`        | 10000 ms | Maximum time to wait for a trace batch export |
| `telemetry.otel_exporter_otlp_traces_compression`    |   `none` | Export compression: `none` or `gzip`          |

These variables are startup-only. Persist changes and restart the server:

```sql
SET PERSIST_ONLY telemetry.otel_bsp_schedule_delay = 5000;
SET PERSIST_ONLY telemetry.otel_bsp_max_queue_size = 2048;
SET PERSIST_ONLY telemetry.otel_bsp_max_export_batch_size = 512;
SET PERSIST_ONLY telemetry.otel_exporter_otlp_traces_timeout = 10000;
SET PERSIST_ONLY telemetry.otel_exporter_otlp_traces_compression = 'gzip';
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

Log telemetry exports instrumented server log records in OTLP format.

Percona Server for MySQL provides logger instruments for the following logs:

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

The `LEVEL` column stores lowercase values: `none`, `error`, `warn`, `info`, and `debug`. Each level accepts records at the same or a greater severity.

For example, set all configured loggers to `warn`:

```sql
UPDATE performance_schema.setup_loggers
SET LEVEL = 'warn';
```

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

The examples use `http://` to show each OTLP path.

A TLS connection to the collector requires an `https://` endpoint. An `http://` endpoint does not use TLS.

Traces, metrics, and logs use separate exporters. Certificate, key, and TLS settings apply to one signal only. Repeat the TLS settings for each signal that uses HTTPS, even when all three signals use the same collector.

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

Configure TLS on the collector OTLP HTTP receiver. The following example enables TLS on port `4318`:

```yaml
receivers:
  otlp:
    protocols:
      http:
        endpoint: 0.0.0.0:4318
        tls:
          cert_file: /etc/otelcol/server.crt
          key_file: /etc/otelcol/server.key
```

For collector TLS options, see [OpenTelemetry Collector TLS configuration](https://github.com/open-telemetry/opentelemetry-collector/blob/main/config/configtls/README.md).

Keep authentication tokens out of commands, shell history, and broadly readable configuration.

Use the corresponding `*_secret_headers` variable when a secret provider is available. The value identifies a secret that contains the HTTP headers.

Configure the provider and secret name as startup-only variables:

```sql
SET PERSIST_ONLY telemetry.secret_provider = '<SECRET_PROVIDER>';
SET PERSIST_ONLY telemetry.otel_exporter_otlp_traces_secret_headers =
  '<SECRET_NAME>';
```

The secret format depends on the provider implementation. Install the provider component before you restart the server.

Use `telemetry.resource_provider` to add resource data from a provider component:

```sql
SET PERSIST_ONLY telemetry.resource_provider = '<RESOURCE_PROVIDER>';
```

The provider name and resource data depend on the provider implementation.

On Linux, each signal can use a network namespace. Set the corresponding `*_network_namespace` variable:

```sql
SET PERSIST_ONLY telemetry.otel_exporter_otlp_traces_network_namespace =
  '<NETWORK_NAMESPACE>';
```

Replace `traces` with `metrics` or `logs` for another signal. Restart the server after you change a provider, secret header, or network namespace.

Network namespace export requires the `CAP_SYS_ADMIN` capability on the `mysqld` binary. Grant the capability, then confirm it:

```bash
sudo setcap cap_sys_admin+ep <MYSQLD_PATH>
getcap <MYSQLD_PATH>
```

Replace `<MYSQLD_PATH>` with the path to the `mysqld` binary. Repeat `setcap` after you replace the binary, including after a package upgrade.

## Verify the configuration

After restarting the server, inspect the active settings:

```sql
SHOW GLOBAL VARIABLES LIKE 'telemetry.%enabled';
SHOW GLOBAL VARIABLES LIKE 'telemetry.otel_exporter_otlp_%_endpoint';
SHOW GLOBAL VARIABLES LIKE 'telemetry.otel_exporter_otlp_%_protocol';
SHOW GLOBAL STATUS LIKE 'telemetry.live_sessions';
```

Confirm that the collector receives data at each configured endpoint:

- `/v1/metrics`

- `/v1/traces`

- `/v1/logs`

Check the collector logs when the collector does not receive an enabled signal.

Configure `telemetry.otel_log_level` to control diagnostics in the Percona Server for MySQL error log.

The variable accepts `SILENT`, `ERROR`, `WARNING`, `INFO`, and `DEBUG`:

```sql
SET GLOBAL telemetry.otel_log_level = 'INFO';
```

`telemetry.otel_log_level` is dynamic. Use `DEBUG` only for troubleshooting. The `DEBUG` level can produce substantial output.

## Related reading

- [OpenTelemetry component overview](opentelemetry-overview.md)

- [Quickstart: test OpenTelemetry locally](quickstart-opentelemetry.md)

- [Install and manage the OpenTelemetry component](opentelemetry-lifecycle.md)

- [OpenTelemetry client plugin](opentelemetry-client.md)

- [OpenTelemetry variable reference](opentelemetry-variables.md)

- [OpenTelemetry data reference](opentelemetry-data-reference.md)

- [Troubleshoot OpenTelemetry](troubleshoot-opentelemetry.md)

- [OpenTelemetry Protocol specification](https://opentelemetry.io/docs/specs/otlp/)

- [OpenTelemetry Collector documentation](https://opentelemetry.io/docs/collector/)

- [OpenTelemetry Collector TLS configuration](https://github.com/open-telemetry/opentelemetry-collector/blob/main/config/configtls/README.md)

