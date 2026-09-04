# Troubleshoot OpenTelemetry

Use the tasks in this guide to diagnose OpenTelemetry metrics, traces, and logs.

Run the initial checks before you change the configuration. Save the original values before you apply a temporary change.

## Run the initial checks

Confirm that the telemetry component is installed:

```sql
SELECT component_urn
FROM mysql.component
WHERE component_urn = 'file://component_telemetry';
```

The query must return one row with `file://component_telemetry`.

Check the component state and signal support:

```sql
SHOW GLOBAL STATUS
WHERE Variable_name IN (
  'telemetry.run_level',
  'telemetry.live_sessions',
  'Telemetry_metrics_supported',
  'Telemetry_traces_supported',
  'Telemetry_logs_supported'
);
```

The expected results are:

| Status variable               | Expected value | Meaning                                                |
| ----------------------------- | -------------- | ------------------------------------------------------ |
| `telemetry.run_level`         | `READY`        | Component initialization completed                     |
| `telemetry.live_sessions`     | `0` or greater | Sessions that telemetry currently instruments          |
| `Telemetry_metrics_supported` | `ON`           | The server binary supports metrics                     |
| `Telemetry_traces_supported`  | `ON`           | The server binary supports traces                      |
| `Telemetry_logs_supported`    | `ON`           | The server binary supports logs                        |

Check the signal states, endpoints, and protocols:

```sql
SHOW GLOBAL VARIABLES
WHERE Variable_name IN (
  'telemetry.metrics_enabled',
  'telemetry.trace_enabled',
  'telemetry.log_enabled',
  'telemetry.otel_exporter_otlp_metrics_endpoint',
  'telemetry.otel_exporter_otlp_metrics_protocol',
  'telemetry.otel_exporter_otlp_traces_endpoint',
  'telemetry.otel_exporter_otlp_traces_protocol',
  'telemetry.otel_exporter_otlp_logs_endpoint',
  'telemetry.otel_exporter_otlp_logs_protocol'
);
```

Each required signal must be `ON`. Each endpoint must match an active collector receiver.

The server exporters support `http/protobuf` and `http/json`. The endpoints normally use port `4318` and these paths:

| Signal  | Path          |
| ------- | ------------- |
| Metrics | `/v1/metrics` |
| Traces  | `/v1/traces`  |
| Logs    | `/v1/logs`    |

## Enable diagnostic messages

Increase the OpenTelemetry diagnostic level while you reproduce a problem:

```sql
SET GLOBAL telemetry.otel_log_level = 'DEBUG';

SHOW GLOBAL VARIABLES LIKE 'telemetry.otel_log_level';
```

The result must show `DEBUG`.

Search the server error log for relevant messages:

```bash
rg -i 'component_telemetry|opentelemetry|telemetry|otlp|export|http|tls|certificate' <ERROR_LOG>
```

On a system that writes the error log to the system journal, use this command:

```bash
journalctl -u <MYSQL_SERVICE> -b | rg -i 'opentelemetry|telemetry|otlp|export|http|tls|certificate'
```

Message text can differ by server build and OpenTelemetry library version. Look for these message patterns:

| Pattern                                                      | Likely cause                                          |
| ------------------------------------------------------------ | ----------------------------------------------------- |
| `component_telemetry` with `load`, `initialize`, or `failed` | Component file, dependency, or initialization failure |
| `export failed`, `send failed`, or `timeout`                 | Collector, network, or backend failure                |
| `connection refused` or `could not resolve host`             | Listener, port, or Domain Name System failure         |
| `certificate verify failed` or `TLS handshake`               | Certificate trust, name, or protocol failure          |
| HTTP `401` or `403`                                          | Missing or invalid authentication                     |
| HTTP `404` or `405`                                          | Incorrect endpoint path or receiver                   |
| HTTP `415`                                                   | Unsupported media type or protocol mismatch           |
| HTTP `429`                                                   | Collector or backend rate limit                       |
| HTTP `503`                                                   | Collector or backend unavailable                      |

Restore the normal diagnostic level after testing:

```sql
SET GLOBAL telemetry.otel_log_level = 'ERROR';
```

The `DEBUG` level can produce substantial error-log output.

## Confirm that the collector receives data

Add the collector `debug` exporter to a temporary test configuration. The detailed output can contain SQL text and user data.

```yaml
receivers:
  otlp:
    protocols:
      http:
        endpoint: 0.0.0.0:4318

exporters:
  debug:
    verbosity: detailed

service:
  pipelines:
    metrics:
      receivers: [otlp]
      exporters: [debug]
    traces:
      receivers: [otlp]
      exporters: [debug]
    logs:
      receivers: [otlp]
      exporters: [debug]
```

Restart or reload the collector according to your deployment method.

The collector output must contain exporter entries for the received signals.

Detailed output also shows resources and payload fields.

| Signal  | Expected debug output                                            |
| ------- | ---------------------------------------------------------------- |
| Metrics | A metrics exporter entry with resource metrics and metric points |
| Traces  | A traces exporter entry with resource spans and spans            |
| Logs    | A logs exporter entry with resource logs and log records         |

The exact entry names and format can differ between collector versions.

Confirm that the collector distribution contains the required components:

```bash
otelcol components
```

The output must list the `otlp` receiver and `debug` exporter. The executable name can differ by distribution.

Remove the `debug` exporter after testing. Detailed payloads can expose sensitive data and increase log volume.

## Fix a component installation failure

The `INSTALL COMPONENT` statement fails, or the component is absent from `mysql.component`.

### Verify the installation

Run the installation statement and record the complete error:

```sql
INSTALL COMPONENT 'file://component_telemetry';
```

Check the component directory:

```sql
SHOW GLOBAL VARIABLES LIKE 'plugin_dir';
```

The directory must contain the telemetry component library for the operating system.

The server process must be able to read the file.

### Resolve the failure

1. Confirm that the installed Percona Server package includes the telemetry component.

2. Confirm that the component file matches the server version and platform.

3. Install any missing library dependencies from the same supported package source.

4. Confirm that the server account has the privileges required to install components.

5. Run `INSTALL COMPONENT` again.

6. Confirm that `mysql.component` contains `file://component_telemetry`.

Search the server error log for the component name.

File-not-found, unresolved-symbol, dependency, and initialization messages identify the cause.

Do not copy a component library from a different server version.

## Fix a client plugin load failure

The `mysql` client does not print `Telemetry plugin <telemetry_client> is loaded.`

Run the client with help enabled:

```bash
mysql --telemetry_client --otel-help -u root -p
```

If the load message is absent, locate `telemetry_client.so` and pass that directory:

```bash
mysql --telemetry_client --plugin_dir=<PLUGIN_DIR> --otel-help -u root -p
```

Replace `<PLUGIN_DIR>` with the directory that contains `telemetry_client.so`.

## Restore missing telemetry variables

The server returns no rows for this statement:

```sql
SHOW GLOBAL VARIABLES LIKE 'telemetry.%';
```

The telemetry component registers these variables during installation.

### Verify the component state

```sql
SELECT component_urn
FROM mysql.component
WHERE component_urn = 'file://component_telemetry';

SHOW GLOBAL STATUS LIKE 'telemetry.run_level';

SHOW GLOBAL VARIABLES
WHERE Variable_name IN (
  'telemetry.resource_provider',
  'telemetry.secret_provider'
);
```

The first query must return the component row. The run level must become `READY`.

The provider variables contain component names when providers are configured.

### Resolve the failure

- Install the component when the component row is absent.

- Check the server error log when the run level is `FAILED`.

- Check the configured resource or secret provider when initialization stops at `DETECT_RESOURCE` or `DECODE_SECRET`.

- Confirm that any configured provider component is installed and available.

- Restart the server after you correct a startup-only provider setting.

An `Unknown system variable` error also indicates that the variable is not registered. Confirm the spelling and component state.

## Resolve unavailable signal support

A `Telemetry_*_supported` status variable reports `OFF`.

### Verify all signals

```sql
SHOW GLOBAL STATUS LIKE 'Telemetry%_supported';
```

An `ON` value confirms that the server binary provides the related instrumentation service.

An `OFF` value indicates unavailable support.

### Resolve the failure

1. Confirm the exact Percona Server version and package:

   ```sql
   SELECT VERSION();
   ```

2. Confirm that the installed package supports the required signal.

3. Replace an incompatible server build with a supported Percona Server build.

4. Restart the server and check the status variables again.

Installing `component_telemetry` cannot add instrumentation support that is absent from the server binary.

## Restore data flow to the collector

The component is `READY`, but the collector receives no metrics, traces, or logs.

### Verify the server configuration

Run the initial checks. Confirm these conditions:

- The required signal is enabled.

- The endpoint contains the correct scheme, host, port, and signal path.

- The protocol matches the collector receiver.

- The server host can resolve and reach the collector host.

- A firewall, proxy, or network policy does not block the connection.

- The per-signal network namespace matches the required Linux network namespace.

The `mysqld` binary has the `CAP_SYS_ADMIN` capability when a network namespace is set.

Inspect the configured network namespaces:

```sql
SHOW GLOBAL VARIABLES
LIKE 'telemetry.otel_exporter_otlp_%_network_namespace';
```

If a namespace value is set, confirm that `mysqld` has `CAP_SYS_ADMIN`:

```bash
getcap <MYSQLD_PATH>
```

The output must include `cap_sys_admin`. If the capability is missing, see [Configure OpenTelemetry](configure-opentelemetry.md#secure-exporter-connections).

Test the HTTP listener from the server host:

```bash
curl --verbose --connect-timeout 5 \
  http://<COLLECTOR_HOST>:4318/v1/traces
```

An HTTP response confirms network access to a listener.

A `404` or `405` response can occur. The test does not send an OTLP payload.

A connection refusal, name-resolution failure, or timeout indicates a network or listener problem.

If an exporter uses a network namespace, run the test from that namespace.

### Verify the collector configuration

Confirm these conditions in the collector configuration:

- The `otlp` receiver defines the HTTP protocol.

- The HTTP receiver listens on the address and port used by the server.

- Each required signal has a service pipeline.

- Each pipeline includes the `otlp` receiver.

- Each pipeline includes an exporter.

Use the `debug` exporter to confirm reception before you test the backend exporter.

Check the collector logs for receiver startup, binding, decoding, processing, and export errors.

## Restore a missing signal

Only one or two signals reach the collector.

### Compare each signal

```sql
SHOW GLOBAL VARIABLES
WHERE Variable_name IN (
  'telemetry.metrics_enabled',
  'telemetry.trace_enabled',
  'telemetry.log_enabled'
);

SELECT NAME, FREQUENCY, ENABLED
FROM performance_schema.setup_meters
ORDER BY NAME;

SELECT NAME, LEVEL
FROM performance_schema.setup_loggers
ORDER BY NAME;
```

For metrics, the global setting and required meters must be enabled. A meter produces data at its configured frequency.

For traces, `telemetry.trace_enabled` must be `ON`.

Statement spans complete when statements end. Session spans complete when sessions end.

For logs, `telemetry.log_enabled` must be `ON`. The required logger level must accept the event.

### Check signal-specific collector pipelines

Confirm that the collector defines a pipeline for every required signal.

A receiver definition does not activate a receiver by itself.

Use the detailed `debug` exporter. Generate a small amount of test activity and check each pipeline separately.

The backend can also discard one signal.

If the debug exporter receives all signals, inspect the backend exporter and backend ingestion rules.

## Correct a rejected variable change

The server rejects a `SET` statement.

### Identify the cause

Record the complete SQL error. Common errors include:

| Error pattern               | Cause                                                           |
| --------------------------- | --------------------------------------------------------------- |
| `Unknown system variable`   | Component absent, incorrect name, or unsupported server version |
| `read only variable`        | The variable is startup-only                                    |
| `Access denied`             | The account lacks a required administrative privilege           |
| `can't be set to the value` | The value has an invalid type, range, or enumeration value      |

Check the account privileges:

```sql
SHOW GRANTS;
```

Runtime changes to global variables normally require `SYSTEM_VARIABLES_ADMIN` or the deprecated `SUPER` privilege.

Persisting a startup-only variable also requires `PERSIST_RO_VARIABLES_ADMIN`.

### Apply the correct change method

Use `SET GLOBAL` for a dynamic, temporary change:

```sql
SET GLOBAL telemetry.trace_enabled = ON;
```

Use `SET PERSIST` for a dynamic change that must survive a restart:

```sql
SET PERSIST telemetry.query_text_enabled = OFF;
```

Use `SET PERSIST_ONLY` for a startup-only variable:

```sql
SET PERSIST_ONLY telemetry.otel_exporter_otlp_traces_endpoint =
  'http://otel-collector.example.com:4318/v1/traces';
```

Restart the server after a `SET PERSIST_ONLY` change.

## Apply startup-only changes

The server accepts a persisted change, but the active value does not change.

### Compare active and persisted values

```sql
SHOW GLOBAL VARIABLES LIKE 'telemetry.otel_exporter_otlp_traces_endpoint';

SELECT VARIABLE_NAME, VARIABLE_VALUE
FROM performance_schema.persisted_variables
WHERE VARIABLE_NAME = 'telemetry.otel_exporter_otlp_traces_endpoint';
```

Different values indicate a pending startup-only change.

### Activate the change

1. Confirm the persisted value.

2. Restart Percona Server for MySQL.

3. Check `telemetry.run_level` for `READY`.

4. Check the active variable again.

5. Review the server error log for startup validation or connection errors.

Exporter endpoints, protocols, certificate settings, batch settings, metrics settings, and resource attributes are startup-only.

These variables are dynamic:

- `telemetry.trace_enabled`

- `telemetry.log_enabled`

- `telemetry.query_text_enabled`

- `telemetry.otel_log_level`

## Resolve certificate and authentication failures

The error log reports a Transport Layer Security (TLS) failure, or the collector returns HTTP `401` or `403`.

Confirm that each TLS endpoint uses `https://`. An `http://` endpoint does not use TLS.

Traces, metrics, and logs each have separate certificate variables. Check the signal that fails.

Confirm that the collector OTLP HTTP receiver enables TLS. See [OpenTelemetry Collector TLS configuration](https://github.com/open-telemetry/opentelemetry-collector/blob/main/config/configtls/README.md).

### Verify certificates

Check the configured certificate values for the affected signal:

```sql
SHOW GLOBAL VARIABLES LIKE 'telemetry.otel_exporter_otlp_traces_certificates';
SHOW GLOBAL VARIABLES LIKE 'telemetry.otel_exporter_otlp_traces_client_certificates';
SHOW GLOBAL VARIABLES LIKE 'telemetry.otel_exporter_otlp_traces_client_key';
```

Replace `traces` with `metrics` or `logs` for another signal.

Confirm that the server process can read each configured file. Confirm that each file uses Privacy-Enhanced Mail (PEM) format.

Inspect a certificate without displaying a private key:

```bash
openssl x509 -in <CERTIFICATE_FILE> -noout -subject -issuer -dates -ext subjectAltName
```

The certificate must be valid. The Subject Alternative Name must match the endpoint host.

For mutual TLS, the client certificate and private key must form a pair. The collector must trust the client certificate issuer.

### Verify authentication

Inspect the secret provider and secret name for each affected signal:

```sql
SHOW GLOBAL VARIABLES
WHERE Variable_name IN (
  'telemetry.secret_provider',
  'telemetry.otel_exporter_otlp_traces_secret_headers'
);
```

Replace `traces` with `metrics` or `logs` for another signal.

Confirm that the required authorization header exists in the named secret.

Do not copy secret header values into logs, command output, or support requests.

Check these conditions:

- The header name matches the collector or gateway requirement.

- The token or credential has not expired.

- The credential permits ingestion for the required signal.

- A proxy does not remove the authorization header.

- The component named by `telemetry.secret_provider` is installed and available.

Persist corrected certificate or header settings. Restart the server to activate them.

## Correct the protocol or endpoint

The collector returns an HTTP error, cannot decode the request, or reports no matching receiver.

### Verify the protocol

```sql
SHOW GLOBAL VARIABLES LIKE 'telemetry.otel_exporter_otlp_%_protocol';
```

The server supports these protocol values:

- `http/protobuf`

- `http/json`

Do not configure the server exporter for gRPC. Configure the collector OTLP HTTP receiver instead.

The collector must accept the selected encoding. Many collector deployments accept OTLP Protocol Buffers on port `4318`.

### Verify the endpoint

```sql
SHOW GLOBAL VARIABLES LIKE 'telemetry.otel_exporter_otlp_%_endpoint';
```

Check the scheme, host, port, proxy path, and signal path.

Use these HTTP responses to guide the investigation:

| Response | Check                                        |
| -------- | -------------------------------------------- |
| `400`    | Invalid or incomplete OTLP payload           |
| `404`    | Incorrect signal path or reverse-proxy route |
| `405`    | Incorrect HTTP method or route               |
| `415`    | Protocol or `Content-Type` mismatch          |
| `431`    | Export headers are too large                 |

Persist corrected protocol or endpoint values. Restart the server and check the active values.

## Reduce queue pressure and dropped data

The error log reports a full queue, failed enqueue, timeout, or dropped telemetry.

### Check server queue settings

```sql
SHOW GLOBAL VARIABLES
WHERE Variable_name IN (
  'telemetry.otel_bsp_max_queue_size',
  'telemetry.otel_bsp_max_export_batch_size',
  'telemetry.otel_bsp_schedule_delay',
  'telemetry.otel_blrp_max_queue_size',
  'telemetry.otel_blrp_max_export_batch_size',
  'telemetry.otel_blrp_schedule_delay'
);
```

The batch span processor uses the `bsp` settings. The batch log record processor uses the `blrp` settings.

Check Performance Schema instrument registration failures:

```sql
SHOW GLOBAL STATUS
WHERE Variable_name IN (
  'Performance_schema_logger_lost',
  'Performance_schema_meter_lost',
  'Performance_schema_metric_lost'
);
```

A nonzero value means that the related instrument could not be created. These values do not count exporter queue drops. For each definition, see [Server status variable definitions](opentelemetry-data-reference.md#server-status-variable-definitions).

### Check collector internal metrics

The collector exposes internal metrics on `http://127.0.0.1:8888/metrics` by default.

```bash
curl --silent --show-error http://127.0.0.1:8888/metrics | \
  rg 'otelcol_(receiver|exporter)_(accepted|refused|queue|enqueue_failed|send_failed|sent)'
```

Check these metric groups:

| Metric group                        | Interpretation                                   |
| ----------------------------------- | ------------------------------------------------ |
| `otelcol_receiver_accepted_*`       | Data entered the collector pipeline              |
| `otelcol_receiver_refused_*`        | The receiver rejected data                       |
| `otelcol_exporter_queue_size`       | Current exporter queue use                       |
| `otelcol_exporter_queue_capacity`   | Exporter queue capacity                          |
| `otelcol_exporter_enqueue_failed_*` | Data could not enter an exporter queue           |
| `otelcol_exporter_send_failed_*`    | The destination rejected or did not receive data |
| `otelcol_exporter_sent_*`           | The destination accepted data                    |

Prometheus can add a `_total` suffix to counter names. Metric names can also differ between collector versions.

### Reduce pressure

1. Restore collector or backend availability.

2. Reduce telemetry volume or disable unused signals.

3. Increase meter frequencies for metrics that need less frequent collection.

4. Raise queue capacity only after you confirm available memory.

5. Adjust batch sizes to match collector and backend limits.

6. Configure the collector sending queue and retry behavior.

7. Scale the collector when sustained input exceeds its processing capacity.

Larger queues can reduce short data gaps, but they also use more memory.

Larger batches can exceed proxy or backend request limits.

## Remove unexpected query text

Statement spans or logs contain SQL text that should not be exported.

### Disable trace query text

```sql
SET PERSIST telemetry.query_text_enabled = OFF;

SHOW GLOBAL VARIABLES LIKE 'telemetry.query_text_enabled';
```

The result must show `OFF`. New statement spans omit the `mysql.sql_text` attribute.

Previously exported spans remain in the backend until their retention period ends.

The setting does not remove query text from OpenTelemetry general query or slow query logs.

### Control query text in logs

Inspect the logger levels:

```sql
SELECT NAME, LEVEL
FROM performance_schema.setup_loggers
WHERE NAME IN ('logger/sql/general_log', 'logger/sql/slow_log');
```

Set an unused logger to `none`:

```sql
UPDATE performance_schema.setup_loggers
SET LEVEL = 'none'
WHERE NAME = 'logger/sql/general_log';
```

Use a collector processor or backend rule when query text must be redacted instead of excluded.

Use the detailed `debug` exporter only in a protected test environment. The exporter prints complete payload fields.

## Reduce OpenTelemetry resource use

CPU use, memory use, network traffic, or server error-log volume increases after telemetry is enabled.

### Measure the effect

Record a workload baseline before you enable telemetry. Compare the same workload after you enable each signal separately.

On Linux, monitor the server process:

```bash
pidstat -p "$(pidof mysqld)" 1
```

Monitor collector CPU use, memory use, queue size, and export latency. The collector exposes process and pipeline metrics.

Check telemetry settings that affect volume:

```sql
SELECT NAME, FREQUENCY, ENABLED
FROM performance_schema.setup_meters
ORDER BY FREQUENCY, NAME;

SELECT NAME, LEVEL
FROM performance_schema.setup_loggers
ORDER BY NAME;

SHOW GLOBAL VARIABLES
WHERE Variable_name IN (
  'telemetry.trace_enabled',
  'telemetry.log_enabled',
  'telemetry.query_text_enabled',
  'telemetry.otel_log_level'
);
```

### Reduce overhead

- Disable signals that have no operational requirement.

- Disable unused meters and loggers.

- Increase the collection interval for lower-priority meters.

- Use less verbose logger levels.

- Set `telemetry.otel_log_level` to `ERROR` after troubleshooting.

- Disable query text when SQL text is not required.

- Reduce high-volume trace or log collection at the source.

- Use collector filtering, sampling, or aggregation when appropriate.

- Scale the collector before you increase server-side queue sizes.

Change one setting at a time. Repeat the same workload test after each change.

## Related reading

- [OpenTelemetry component overview](opentelemetry-overview.md)

- [Quickstart: test OpenTelemetry locally](quickstart-opentelemetry.md)

- [Install and manage the OpenTelemetry component](opentelemetry-lifecycle.md)

- [Configure OpenTelemetry](configure-opentelemetry.md)

- [OpenTelemetry client plugin](opentelemetry-client.md)

- [OpenTelemetry variable reference](opentelemetry-variables.md)

- [OpenTelemetry data reference](opentelemetry-data-reference.md)

- [OpenTelemetry Collector troubleshooting](https://opentelemetry.io/docs/collector/troubleshooting/)

- [OpenTelemetry Collector internal telemetry](https://opentelemetry.io/docs/collector/internal-telemetry/)

- [OpenTelemetry Collector TLS configuration](https://github.com/open-telemetry/opentelemetry-collector/blob/main/config/configtls/README.md)

