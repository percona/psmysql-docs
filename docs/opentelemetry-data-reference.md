# OpenTelemetry data reference

Percona Server for MySQL exposes metrics, traces, and logs through OpenTelemetry.

The available data can vary by server version and installed components.

Use the Performance Schema tables to view the data available on your server.

## Signal summary

| Signal  | Data                                         | Creation condition                                       | Export condition                                       |
| ------- | -------------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------ |
| Metrics | Measurements from enabled meters             | The server collects a measurement at the meter frequency | Global metric collection and the meter must be enabled |
| Traces  | Control, session, and statement spans        | The server creates a span for the related event          | Trace collection must be enabled                       |
| Logs    | Error, slow query, and general query records | The related logger receives a record at an enabled level | Log collection must be enabled                         |

The OpenTelemetry Protocol (OTLP) exporter sends each enabled signal to its configured endpoint.

The exporter uses the configured security, compression, timeout, queue, and batch settings.

## Metrics

A meter groups related metrics. Each meter has an independent collection frequency and enabled state.

### View available meters

Query the `performance_schema.setup_meters` table:

```sql
SELECT NAME, FREQUENCY, ENABLED, DESCRIPTION
FROM performance_schema.setup_meters
ORDER BY NAME;
```

The table contains these fields:

| Field         | Description                             |
| ------------- | --------------------------------------- |
| `NAME`        | Meter name                              |
| `FREQUENCY`   | Collection interval in seconds          |
| `ENABLED`     | Meter state. The value is `YES` or `NO` |
| `DESCRIPTION` | Meter description                       |

Percona Server for MySQL can provide these server meters:

| Meter                    | Data category                                |
| ------------------------ | -------------------------------------------- |
| `mysql.inno`             | InnoDB activity and status                   |
| `mysql.inno.buffer_pool` | InnoDB buffer pool activity and state        |
| `mysql.inno.data`        | InnoDB data input and output                 |
| `mysql.mle`              | Multilingual Engine activity, when available |
| `mysql.myisam`           | MyISAM activity and state                    |
| `mysql.perf_schema`      | Performance Schema telemetry status          |
| `mysql.stats`            | General server status                        |
| `mysql.stats.com`        | Statement command counts                     |
| `mysql.stats.connection` | Connection activity and errors               |
| `mysql.stats.handler`    | Storage engine handler activity              |
| `mysql.stats.ssl`        | Secure Sockets Layer (SSL) connection status |
| `mysql.x`                | X Plugin activity and state                  |
| `mysql.x.stmt`           | X Plugin statement activity                  |

The exact list is authoritative for the running server. Components can add meters.

OTLP stores the meter name as the instrumentation scope name. OTLP stores the metric name separately.

For example, `mysql.stats` is the scope name for the `bytes_received` metric.

### View available metrics

Query the `performance_schema.setup_metrics` table for the complete metric catalog:

```sql
SELECT NAME, METER, METRIC_TYPE, NUM_TYPE, UNIT, DESCRIPTION
FROM performance_schema.setup_metrics
ORDER BY METER, NAME;
```

The table contains these fields:

| Field         | Description                                                        |
| ------------- | ------------------------------------------------------------------ |
| `NAME`        | Metric name                                                        |
| `METER`       | Meter that owns the metric                                         |
| `METRIC_TYPE` | OpenTelemetry metric type                                          |
| `NUM_TYPE`    | Numeric data type. The value is `INTEGER` or `DOUBLE`              |
| `UNIT`        | Measurement unit. An empty value means that the metric has no unit |
| `DESCRIPTION` | Metric description                                                 |

The server uses these metric types:

| Metric type           | Meaning                                       |
| --------------------- | --------------------------------------------- |
| `ASYNC COUNTER`       | A cumulative value that normally increases    |
| `ASYNC GAUGE COUNTER` | A current value that can increase or decrease |

The following table contains representative metrics.

Query `performance_schema.setup_metrics` for the complete list, units, and exact descriptions.

| Meter                    | Metric                   | Type                  | Unit | Description                                              |
| ------------------------ | ------------------------ | --------------------- | ---- | -------------------------------------------------------- |
| `mysql.stats`            | `bytes_received`         | `ASYNC COUNTER`       | `By` | Bytes received from clients                              |
| `mysql.stats`            | `threads_connected`      | `ASYNC GAUGE COUNTER` | None | Open client connections                                  |
| `mysql.stats.connection` | `errors_max_connections` | `ASYNC COUNTER`       | None | Connections rejected due to the maximum connection limit |
| `mysql.stats.handler`    | `read_key`               | `ASYNC COUNTER`       | None | Requests to read a row by key                            |
| `mysql.stats`            | `slow_queries`           | `ASYNC COUNTER`       | None | Queries that exceeded `long_query_time`                  |
| `mysql.stats.connection` | `total`                  | `ASYNC COUNTER`       | None | Total connections created                                |
| `mysql.stats.handler`    | `read_key`               | `ASYNC COUNTER`       | None | Requests to read a row by key                            |
| `mysql.inno.data`        | `reads`                  | `ASYNC COUNTER`       | None | Read operations started by InnoDB                        |
| `mysql.x`                | `ssl_finished_accepts`   | `ASYNC COUNTER`       | None | Successful SSL connections to X Plugin                   |
| `mysql.perf_schema`      | `metric_lost`            | `ASYNC COUNTER`       | None | Metric instruments that could not be loaded              |

OpenTelemetry uses `By` as the unit for bytes. `None` means that the metric declares no unit.

### Metric creation and export

The server processes a metric as follows:

1. The meter reaches its configured collection interval.

2. The server reads each metric in the enabled meter.

3. The metric reader places the measurement in the export pipeline.

4. The OTLP exporter sends the measurement to the configured metrics endpoint.

The server does not collect a meter when its `ENABLED` value is `NO`. Global metric collection must also be enabled.

## Traces

The server creates `control`, `session`, and `stmt` spans. The `telemetry.trace_enabled` variable controls trace collection.

### Control span

The `control` span records a telemetry lifecycle or configuration event.

| Attribute         | Description                                           |
| ----------------- | ----------------------------------------------------- |
| `trace_enabled`   | Trace collection state                                |
| `metrics_enabled` | Metric collection state                               |
| `logs_enabled`    | Log collection state                                  |
| `details`         | Additional information about the configuration change |

The telemetry component creates this span when the telemetry configuration changes.

Trace collection must be active for the span to reach the trace pipeline.

### Session span

The `session` span represents a client session.

| Attribute                             | Description                                  |
| ------------------------------------- | -------------------------------------------- |
| `mysql.processlist_id`                | Session identifier shown in the process list |
| `mysql.thread_id`                     | Internal server thread identifier            |
| `mysql.user`                          | Authenticated account name                   |
| `mysql.host`                          | Client host                                  |
| `mysql.group`                         | Session group, when available                |
| `mysql.session_attr.<ATTRIBUTE_NAME>` | Client connection attribute and value        |

The span covers the period from the initial connection through the session close.

The server emits the completed span when the session ends.

### Statement span

The `stmt` span represents a server statement event. The server completes the span when statement execution ends.

#### Statement identity attributes

| Attribute              | Description                                               |
| ---------------------- | --------------------------------------------------------- |
| `mysql.event_name`     | Performance Schema statement event name                   |
| `mysql.lock_time`      | Time spent waiting for table locks                        |
| `mysql.sql_text`       | SQL statement text, when query text collection is enabled |
| `mysql.digest_text`    | Normalized statement digest text                          |
| `mysql.current_schema` | Default schema for the statement                          |
| `mysql.object_type`    | Object type                                               |
| `mysql.object_schema`  | Object schema                                             |
| `mysql.object_name`    | Object name                                               |

#### Statement result attributes

| Attribute             | Description                       |
| --------------------- | --------------------------------- |
| `mysql.sql_errno`     | MySQL error number                |
| `mysql.sqlstate`      | SQLSTATE value                    |
| `mysql.message_text`  | Error or diagnostic message       |
| `mysql.error_count`   | Number of errors                  |
| `mysql.warning_count` | Number of warnings                |
| `mysql.rows_affected` | Number of affected rows           |
| `mysql.rows_sent`     | Number of rows sent to the client |
| `mysql.rows_examined` | Number of rows examined           |

#### Statement performance attributes

| Attribute                       | Description                                                 |
| ------------------------------- | ----------------------------------------------------------- |
| `mysql.created_tmp_disk_tables` | Internal temporary tables created on disk                   |
| `mysql.created_tmp_tables`      | Internal temporary tables created in memory or on disk      |
| `mysql.select_full_join`        | Joins that performed a full table scan due to a missing key |
| `mysql.select_full_range_join`  | Joins that used a range search on a reference table         |
| `mysql.select_range`            | Joins that used ranges on the first table                   |
| `mysql.select_range_check`      | Joins that checked key usage after each row                 |
| `mysql.select_scan`             | Joins that performed a full scan of the first table         |
| `mysql.sort_merge_passes`       | Merge passes performed by the sort algorithm                |
| `mysql.sort_range`              | Sort operations that used ranges                            |
| `mysql.sort_rows`               | Rows sorted                                                 |
| `mysql.sort_scan`               | Sort operations that scanned a table                        |
| `mysql.no_index_used`           | Indicates that the statement used no index                  |
| `mysql.no_good_index_used`      | Indicates that the optimizer found no suitable index        |
| `mysql.max_controlled_memory`   | Maximum controlled memory used by the statement             |
| `mysql.max_total_memory`        | Maximum total memory used by the statement                  |
| `mysql.cpu_time`                | CPU time used by the statement                              |

### Trace export

Completed spans enter the batch span processor queue.

The processor forms batches according to the configured schedule and maximum batch size.

The OTLP exporter sends each batch to the configured traces endpoint.

A full queue can reject new spans. Export failures can prevent the backend from receiving spans.

Monitor the collector and server error log for failures.

## Logs

The server provides separate OpenTelemetry loggers for the error log, slow query log, and general query log.

### View available loggers

Query the `performance_schema.setup_loggers` table:

```sql
SELECT NAME, LEVEL, DESCRIPTION
FROM performance_schema.setup_loggers
ORDER BY NAME;
```

| Logger                   | Record level   | Description                                          |
| ------------------------ | -------------- | ---------------------------------------------------- |
| `logger/sql/error_log`   | Event-specific | Server error log records retain their event severity |
| `logger/sql/slow_log`    | `WARN`         | Slow query records                                   |
| `logger/sql/general_log` | `INFO`         | General query records                                |

The `LEVEL` field accepts these values. Each level accepts records at the same or a greater severity.

| Level   | Records accepted                                 |
| ------- | ------------------------------------------------ |
| `none`  | No records                                       |
| `error` | Error records                                    |
| `warn`  | Error and warning records                        |
| `info`  | Error, warning, and informational records        |
| `debug` | Error, warning, informational, and debug records |

The OpenTelemetry slow query and general query loggers operate independently from these variables:

- `slow_query_log`

- `general_log`

- `log_output`

- `log_slow_replica_statements`

Changing a file or table log setting does not change the matching OpenTelemetry logger.

### Log creation and export

The server processes a log record as follows:

1. The server produces an error, slow query, or general query event.

2. The matching logger compares the event severity with its configured level.

3. The batch log record processor places the accepted record in its queue.

4. The processor forms a batch according to the configured schedule and maximum batch size.

5. The OTLP exporter sends the batch to the configured logs endpoint.

Global log collection must be enabled. A logger with the `none` level does not create exportable records.

## Resource attributes

Resource attributes identify the server that produced telemetry. Set custom attributes with `telemetry.otel_resource_attributes`.

Use the OpenTelemetry resource attribute format:

```text
service.name=payments-mysql,deployment.environment.name=production,service.instance.id=mysql-01
```

Recommended attributes include:

| Attribute                     | Purpose                                                   |
| ----------------------------- | --------------------------------------------------------- |
| `service.name`                | Stable service name for the MySQL deployment              |
| `service.instance.id`         | Unique identifier for one server instance                 |
| `deployment.environment.name` | Deployment environment, such as `production` or `staging` |

Use the same attribute names across metrics, traces, and logs.

Consistent attributes support correlation in the observability backend.

The OpenTelemetry software development kit and resource providers can add other attributes.

Inspect received telemetry to confirm the complete resource for your deployment.

## Sensitive data

Telemetry can contain confidential or regulated data. Review these fields before you enable export:

| Signal              | Potentially sensitive data                                                                    |
| ------------------- | --------------------------------------------------------------------------------------------- |
| Statement traces    | SQL text, normalized digest text, schema names, object names, errors, and diagnostic messages |
| Session traces      | User names, client hosts, connection attributes, and session identifiers                      |
| General query logs  | SQL text and connection activity                                                              |
| Slow query logs     | SQL text and query performance details                                                        |
| Error logs          | Account names, host names, object names, paths, and diagnostic data                           |
| Resource attributes | Service names, instance identifiers, environment names, and custom values                     |

Set `telemetry.query_text_enabled` to `OFF` to omit `mysql.sql_text` from statement spans.

This setting does not remove SQL text from general query or slow query log records.

Apply these controls before production use:

- Export only the required signals.

- Disable unused loggers and meters.

- Choose the least detailed logger level that meets operational needs.

- Restrict access to the collector and observability backend.

- Use Transport Layer Security (TLS) for network export.

- Configure retention and redaction in the telemetry pipeline.

- Do not place secrets in custom resource attributes.

## Related reading

- [Install and manage the OpenTelemetry component](opentelemetry-lifecycle.md)

- [Configure OpenTelemetry](configure-opentelemetry.md)


