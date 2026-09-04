# Quickstart: test OpenTelemetry locally[¶](#quickstart-test-opentelemetry-locally "Permanent link")

Use this quickstart to test OpenTelemetry (OTel) on a single Docker host. This quickstart uses a local collector with a debug exporter. The debug exporter prints received data to the terminal.

This quickstart is a test procedure. For production installation and configuration, see [Install and manage the OpenTelemetry component](opentelemetry-lifecycle.md) and [Configure OpenTelemetry](configure-opentelemetry.md).

## Prerequisites[¶](#prerequisites "Permanent link")

- Docker
- A running Percona Server for MySQL 9.7 container named `psmysql`, started per [Quickstart - Run and create database (containers)](quickstart-docker.html)
- The MySQL root user, or an account with the `INSERT` privilege on the `mysql.component` system table
- The ability to restart the `psmysql` container

## Step 1: Start a local collector on the same Docker network[¶](#step-1-start-a-local-collector "Permanent link")

The collector and `psmysql` must be able to reach each other by container name — they will not be able to reach each other over `localhost`, since each runs in its own network namespace.

Create a dedicated Docker network and attach `psmysql` to it:

```
docker network create otel-quickstart
docker network connect otel-quickstart psmysql
```

Create a file named `otel-collector-config.yaml` with the following content:

```
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

Start the collector on the same network, giving it a name so `psmysql` can resolve it:

```
docker run -d --name otel-collector \
  --network otel-quickstart \
  -p 4318:4318 \
  -v $(pwd)/otel-collector-config.yaml:/etc/otelcol/config.yaml \
  otel/opentelemetry-collector:latest
```

## Step 2: Install the component[¶](#step-2-install-the-component "Permanent link")

Connect to Percona Server for MySQL in the container:

```
docker exec -it psmysql mysql -uroot -p
```

Run the following statement:

```
INSTALL COMPONENT 'file://component_telemetry';
```

## Step 3: Enable one signal[¶](#step-3-enable-one-signal "Permanent link")

This quickstart enables metrics only. `telemetry.metrics_enabled` and `telemetry.otel_exporter_otlp_metrics_endpoint` are non-dynamic variables, so they must be set in a configuration file and applied with a container restart.

!!! warning "Verify this path"
    The command below assumes the Percona Server Docker image reads config overrides from `/etc/my.cnf.d/`. Confirm this against [Docker environment variables](docker-config.html) before publishing this step — if the image uses a different config directory, adjust the path accordingly.

Write a config override into the running container, referencing the collector by its container name rather than `localhost`:

```
docker exec -i psmysql sh -c 'cat > /etc/my.cnf.d/otel-quickstart.cnf' <<'EOF'
[mysqld]
telemetry.metrics_enabled=ON
telemetry.otel_exporter_otlp_metrics_endpoint=http://otel-collector:4318/v1/metrics
EOF
```

Restart the container to apply the change:

```
docker restart psmysql
```

## Step 4: Generate sample activity[¶](#step-4-generate-sample-activity "Permanent link")

Connect and run a sample query to generate metric data:

```
docker exec -it psmysql mysql -uroot -p -e "SELECT 1;"
```

Wait 10 seconds. The default export interval for metrics is 10 seconds.

## Step 5: Confirm that the collector receives data[¶](#step-5-confirm-that-the-collector-receives-data "Permanent link")

Check the collector's logs:

```
docker logs otel-collector
```

Confirm the output contains metric names with the `mysql` prefix.

!!! note "What this quickstart validates"
    This procedure confirms that the OTLP/HTTP metrics pipeline is wired up correctly between Percona Server for MySQL and a collector, using an unauthenticated, unencrypted connection between containers on the same Docker network.

    It does **not** confirm:

    - That the metric values match what you expect for your workload — see the [OpenTelemetry data reference](opentelemetry-data-reference.html) for what each metric measures
    - That TLS works with your certificates, or that authentication (headers or secret-based) works with your credentials — both of which any real deployment needs

    For a production setup with TLS and authentication, see [Configure OpenTelemetry](configure-opentelemetry.md).

## Step 6: Remove the test configuration[¶](#step-6-remove-the-test-configuration "Permanent link")

!!! note
    Completing this quickstart confirms connectivity only. Before enabling OpenTelemetry in production, see [Configure OpenTelemetry](configure-opentelemetry.md) to set up TLS and authentication.

Remove the config override and restart the container:

```
docker exec psmysql rm /etc/my.cnf.d/otel-quickstart.cnf
docker restart psmysql
```

Uninstall the component — this does not require a restart:

```
docker exec -it psmysql mysql -uroot -p -e "UNINSTALL COMPONENT 'file://component_telemetry';"
```

Remove the collector and the network:

```
docker rm -f otel-collector
docker network rm otel-quickstart
```
