# Quickstart: test OpenTelemetry locally

Use the following procedure to test OpenTelemetry (OTel) on a single Docker host. Docker Compose starts Percona Server for MySQL and a local collector on one network. The collector uses a debug exporter. The debug exporter prints received data to the terminal.

The quickstart procedure is a connectivity test. For production installation and configuration, see [Install and manage the OpenTelemetry component](opentelemetry-lifecycle.md) and [Configure OpenTelemetry](configure-opentelemetry.md).

## Prerequisites

- Docker Engine and Docker Compose
- Stable internet access
- The ability to create files in a working directory



## Step 1: Create the Compose project

Create a directory named `otel-quickstart` and open that directory:

```bash
mkdir otel-quickstart
cd otel-quickstart
```

Create a file named `docker-compose.yml` with the following content:

```yaml
services:
  psmysql:
    image: percona/percona-server:{{tag}}
    environment:
      MYSQL_ROOT_PASSWORD: secret
    volumes:
      - psmysql-data:/var/lib/mysql
    depends_on:
      - otel-collector
    restart: unless-stopped

  otel-collector:
    image: otel/opentelemetry-collector:latest
    volumes:
      - ./otel-collector-config.yaml:/etc/otelcol/config.yaml:ro
    restart: unless-stopped

volumes:
  psmysql-data:
```

To run the ARM64 image of Percona Server for MySQL, use the `{{arm_tag}}` tag instead of `{{tag}}` in the `image` line.

The Compose project network lets `psmysql` resolve the collector as `otel-collector`. The containers do not use `localhost` to reach each other.

The file does not publish port `3306` or port `4318` on the host. The test uses `docker compose exec` and `docker compose logs`.

Create a file named `otel-collector-config.yaml` with the following content:

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
```



## Step 2: Start the stack

Start both services:

```bash
docker compose up -d
```

Wait until Percona Server for MySQL is ready. Check the server logs:

```bash
docker compose logs psmysql
```

Continue when the log contains `ready for connections`.

## Step 3: Install the component

Connect to Percona Server for MySQL in the `psmysql` service. The example password is `secret`.

```bash
docker compose exec psmysql mysql -uroot -psecret
```

Run the following statement:

```sql
INSTALL COMPONENT 'file://component_telemetry';
```

The `INSTALL COMPONENT` statement stores the component in the `mysql.component` table. The next server start loads the component from that table.

Exit the client.

## Step 4: Enable one signal

The procedure enables metrics only. `telemetry.metrics_enabled` and `telemetry.otel_exporter_otlp_metrics_endpoint` are startup-only variables. Add those settings in a configuration file. Then restart the `psmysql` service.

!!! warning "Verify this path"

```
The copy command places the file in `/etc/my.cnf.d/`. Confirm the configuration directory for your image in [Docker environment variables](docker-config.md). If the image uses a different directory, adjust the path.
```

Create a file named `otel-quickstart.cnf` with the following content:

```ini
[mysqld]
telemetry.metrics_enabled=ON
telemetry.otel_exporter_otlp_metrics_endpoint=http://otel-collector:4318/v1/metrics
```

Copy the file into the `psmysql` service. Then restart that service:

```bash
docker compose cp otel-quickstart.cnf psmysql:/etc/my.cnf.d/otel-quickstart.cnf
docker compose restart psmysql
```

Wait for `ready for connections` in the `psmysql` logs before you continue.

Do not add these telemetry settings before you install the component. The server treats the names as unknown variables when `component_telemetry` is not installed.

## Step 5: Generate sample activity

Connect and run a sample query to generate metric data:

```bash
docker compose exec psmysql mysql -uroot -psecret -e "SELECT 1;"
```

Wait 10 seconds. The default export interval for metrics is 10 seconds.

## Step 6: Confirm that the collector receives data

Check the collector logs:

```bash
docker compose logs otel-collector
```

Confirm that the output contains metric names with the `mysql` prefix.

!!! note "What this procedure validates"

```
The procedure confirms that the OTLP/HTTP metrics pipeline works between Percona Server for MySQL and a collector. The connection is unauthenticated and unencrypted on the Compose project network.

The procedure does not confirm the following items:

- Metric values for your workload

- TLS with your certificates

- Header or secret authentication with your credentials

See the [OpenTelemetry data reference](opentelemetry-data-reference.md) for the meaning of each metric.

For a production configuration with TLS and authentication, see [Configure OpenTelemetry](configure-opentelemetry.md).
```



## Step 7: Remove the test stack

!!! note

```
Completing the procedure confirms connectivity only. Before you enable OpenTelemetry in production, see [Configure OpenTelemetry](configure-opentelemetry.md) to configure TLS and authentication.
```

Uninstall the component. This statement does not require a restart:

```bash
docker compose exec psmysql mysql -uroot -psecret -e "UNINSTALL COMPONENT 'file://component_telemetry';"
```

Stop the services and remove the containers, the project network, and the named volume:

```bash
docker compose down -v
```

Remove the project directory if you no longer need the files:

```bash
cd ..
rm -rf otel-quickstart
```



## Related reading

- [OpenTelemetry component overview](opentelemetry-overview.md)
- [Install and manage the OpenTelemetry component](opentelemetry-lifecycle.md)
- [Configure OpenTelemetry](configure-opentelemetry.md)
- [OpenTelemetry client plugin](opentelemetry-client.md)
- [OpenTelemetry variable reference](opentelemetry-variables.md)
- [OpenTelemetry data reference](opentelemetry-data-reference.md)
- [Troubleshoot OpenTelemetry](troubleshoot-opentelemetry.md)
- [Use Docker Compose and named volumes](docker-compose.md)

