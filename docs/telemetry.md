# Telemetry on Percona Server for MySQL

Percona telemetry fills in the gaps in our understanding of how you use Percona Server for MySQL to improve our products. Participation in the anonymous program is optional. You can opt-out if you prefer to not share this information.

## What information is collected

At this time, telemetry is added only to the Percona packages and Docker images. Percona Server for MySQL collects only information about the installation environment. Future releases may add additional metrics.

Be assured that access to this raw data is rigorously controlled. Percona does not collect personal data. All data is anonymous and cannot be traced to a specific user. To learn more about our privacy practices, read our [Percona Privacy statement].

An example of the data collected is the following:

```JSON
[{"id" : "c416c3ee-48cd-471c-9733-37c2886f8231",
"product_family" : "PRODUCT_FAMILY_PS",
"instanceId" : "6aef422e-56a7-4530-af9d-94cc02198343",
"createTime" : "2023-10-16T10:46:23Z",
"metrics":
[{"key" : "deployment","value" : "PACKAGE"},
{"key" : "pillar_version","value" : "8.0.35-27"},
{"key" : "OS","value" : "Oracle Linux Server 8.8"},
{"key" : "hardware_arch","value" : "x86_64 x86_64"}]}]
```

## Disable telemetry

Telemetry is enabled by default. If you decide not to send usage data to Percona, you can set the `PERCONA_TELEMETRY_DISABLE=1` environment variable for either the root user or in the operating system prior to the installation process.

=== "Debian-derived distribution"

    Add the environment variable before the install process.

    ```{.bash data-prompt="$"}
    $ sudo PERCONA_TELEMETRY_DISABLE=1 apt install percona-server-server
    ```

=== "Red Hat-derived distribution"

    Add the environment variable before the install process.

    ```{.bash data-prompt="$"}
    $ sudo PERCONA_TELEMETRY_DISABLE=1 yum install percona-server-server
    ```

=== "DOCKER"

    Add the environment variable when running a command in a new container.

    ```{.bash data-prompt="$"}
    $ docker run -d -e MYSQL_ROOT_PASSWORD=test1234# -e PERCONA_TELEMETRY_DISABLE=1 -e --name=percona-server percona/percona-server:8.0.35-27
    ```

[Percona Privacy statement]: https://www.percona.com/privacy-policy#h.e34c40q8sb1a