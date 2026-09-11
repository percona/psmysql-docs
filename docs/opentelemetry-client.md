# OpenTelemetry client plugin

The `mysql` command-line client can export OpenTelemetry (OTel) traces. The client uses the `telemetry_client` plugin. The plugin is separate from the server `component_telemetry` component. The plugin is also separate from [Percona telemetry](telemetry.md).

The client plugin exports traces only. The plugin does not export metrics or logs.

## How the client plugin works

The client process creates spans for work that the `mysql` client performs. The plugin then pushes those spans to an OpenTelemetry Protocol (OTLP) HTTP endpoint.

The server component and the client plugin use separate exporters. Each process sends data to the collector that you configure for that process.

MySQL connectors use a different tracing design. Connector spans go through the application OpenTelemetry Software Development Kit (SDK). The `telemetry_client` plugin does not use that path.

## Enable the plugin

The plugin is `OFF` by default.

To enable the plugin for one session, start the client with `--telemetry_client`:

```bash
mysql --telemetry_client -u root -p
```

The client loads `telemetry_client.so` from the plugin directory. If the plugin is not in the default directory, set `--plugin_dir` to the directory that contains `telemetry_client.so`:

```bash
mysql --telemetry_client --plugin_dir=<PLUGIN_DIR> -u root -p
```

Replace `<PLUGIN_DIR>` with the plugin directory for your packages. Common paths are `/usr/lib/mysql/plugin` and `/usr/lib64/mysql/plugin`.

To enable the plugin for every `mysql` client start, add the option under `[mysql]`:

```ini
[mysql]
telemetry-client=ON
```

With `telemetry-client=ON` in the option file, you do not pass `--telemetry_client` on the command line.

To print the client telemetry option help, run the following command:

```bash
mysql --telemetry_client --otel-help
```

A successful load prints the option table and this message:

```text
Telemetry plugin <telemetry_client> is loaded.
```

If that message is absent, the client did not load the plugin. Confirm that `telemetry_client.so` exists in the plugin directory. Then retry with `--plugin_dir`.

## Configure the plugin

The client reads telemetry settings from the `[telemetry_client]` group in the option file.

Command-line flags override the option file for the same setting.

The following example sends traces to a collector on the standard OTLP/HTTP port `4318`:

```ini
[mysql]
telemetry-client=ON

[telemetry_client]
trace=ON
otel-exporter-otlp-traces-endpoint=http://otel-collector.example.com:4318/v1/traces
otel-exporter-otlp-traces-protocol=http/protobuf
otel-resource-attributes=service.name=mysql-client,service.namespace=lab
otel-log-level=ERROR
otel-exporter-otlp-traces-compression=none
otel-exporter-otlp-traces-headers=authorization=Bearer <TOKEN>
```

The following command sets the same endpoint for one client session:

```bash
mysql --telemetry_client \
  --otel_exporter_otlp_traces_endpoint=http://otel-collector.example.com:4318/v1/traces \
  --otel_exporter_otlp_traces_protocol=http/protobuf \
  -u root -p
```

Replace `otel-collector.example.com` with the hostname of your collector.

The plugin supports the following encodings:

| Value           | Description                                  |
| --------------- | -------------------------------------------- |
| `http/protobuf` | Binary Protocol Buffers encoding. The default |
| `http/json`     | JSON encoding                                |

The plugin does not support OTLP over gRPC.

Use `http://` for an unencrypted collector. A TLS collector connection requires `https://` in the endpoint URL. The default endpoint is `http://localhost:4318/v1/traces`.

The collector must also enable TLS on the OTLP HTTP receiver. See [Configure OpenTelemetry](configure-opentelemetry.md#secure-exporter-connections).

## Client telemetry options

The following table lists the client telemetry options. The table uses the command-line form. Option-file names use hyphens.

| Option | Default | Description |
| ------ | ------- | ----------- |
| `--telemetry_client` | `OFF` | Loads the client telemetry plugin. Use `telemetry-client` under `[mysql]`. |
| `--otel-trace` | `ON` | Collects client traces after the plugin loads. Use `trace` under `[telemetry_client]`. |
| `--otel-help` | `OFF` | Prints help for client telemetry options. Use `help` under `[telemetry_client]`. |
| `--otel_log_level` | `ERROR` | Sets the diagnostic level for client telemetry messages. Valid values are `SILENT`, `ERROR`, `WARNING`, `INFO`, and `DEBUG`. |
| `--otel_resource_attributes` | *(empty)* | Adds resource attributes as comma-separated `key=value` pairs. |
| `--otel_exporter_otlp_traces_endpoint` | `http://localhost:4318/v1/traces` | Sets the OTLP/HTTP URL for trace export. |
| `--otel_exporter_otlp_traces_protocol` | `http/protobuf` | Sets the OTLP encoding to `http/protobuf` or `http/json`. |
| `--otel_exporter_otlp_traces_headers` | *(empty)* | Adds HTTP headers as comma-separated `key=value` pairs. |
| `--otel_exporter_otlp_traces_compression` | `none` | Sets export compression to `none` or `gzip`. |
| `--otel_exporter_otlp_traces_timeout` | `10000` | Sets the export timeout in milliseconds. |
| `--otel_bsp_schedule_delay` | `5000` | Sets the delay between consecutive span exports, in milliseconds. |
| `--otel_bsp_max_queue_size` | `2048` | Sets the maximum number of spans in the export queue. |
| `--otel_bsp_max_export_batch_size` | `512` | Sets the maximum number of spans in one export batch. |

These certificate options exist in the client but have no effect:

- `--otel_exporter_otlp_traces_certificates`

- `--otel_exporter_otlp_traces_client_certificates`

- `--otel_exporter_otlp_traces_client_key`

These certificate options do not enable Transport Layer Security (TLS) for the client plugin.

Keep authentication tokens out of the shell history. Store HTTP headers in the client option file.

The `mysql` client reads option files at start. Common client option files are `/etc/my.cnf` and `~/.my.cnf`. Add the headers in the `[telemetry_client]` group. See the example in [Configure the plugin](#configure-the-plugin).

Limit read access to the file owner:

```bash
chmod 600 ~/.my.cnf
```

## Use the plugin with the server component

Client export and server export are independent.

To collect server-side spans for the same session, install `component_telemetry`. Then configure the server exporter. See [Install and manage the OpenTelemetry component](opentelemetry-lifecycle.md) and [Configure OpenTelemetry](configure-opentelemetry.md).

A collector can receive both streams. Configure each exporter with an OTLP/HTTP traces receiver. The traces path is `/v1/traces` on port `4318`.

The client plugin does not replace server metrics, traces, or logs.

## Limits

The client plugin has the following limits:

* Trace export is the only supported signal.

* OTLP over HTTP is the only supported transport.

* `http/protobuf` and `http/json` are the only supported encodings.

* Certificate and client-key options have no effect.

* An external collector must receive the exported spans.

## Related reading

- [OpenTelemetry component overview](opentelemetry-overview.md)

- [Quickstart: test OpenTelemetry locally](quickstart-opentelemetry.md)

- [Install and manage the OpenTelemetry component](opentelemetry-lifecycle.md)

- [Configure OpenTelemetry](configure-opentelemetry.md)

- [OpenTelemetry variable reference](opentelemetry-variables.md)

- [OpenTelemetry data reference](opentelemetry-data-reference.md)

- [Troubleshoot OpenTelemetry](troubleshoot-opentelemetry.md)

- [OpenTelemetry Protocol specification](https://opentelemetry.io/docs/specs/otlp/)

- [OpenTelemetry Collector TLS configuration](https://github.com/open-telemetry/opentelemetry-collector/blob/main/config/configtls/README.md)

