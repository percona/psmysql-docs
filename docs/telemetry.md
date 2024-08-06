# Telemetry and data collection

Percona has the following types of telemetry:

* [Installation-time telemetry](#installation-time-telemetry)

* [Continuous telemetry](#continuous-telemetry)

By understanding these types of telemetry systems and their respective features, you can effectively implement and manage them to gather valuable insights and improve your systems and software.

You control whether to share this information. The program is optional. You can disable either or both telemetry systems if you don't want to share anonymous data.

Percona protects your privacy. They don't gather personal information. All collected data is anonymous, preventing the identification of individual users or servers. Our [Percona Privacy policy](https://www.percona.com/privacy-policy) provides more details on data handling.

Percona includes the telemetry systems only in software packages, compressed archives (tarballs), and Docker images.

## Why telemetry matters

Telemetry in Percona Server for MySQL has the following qualities:

| Advantages                  | Description                                                                                                                                                         |
|-----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| See How People Use Your Software | Telemetry collects anonymous data on how users interact with our software. This tells developers which features are popular, which ones are confusing, and if anything is causing crashes. |
| Identify Issues Early       | Telemetry can catch bugs or performance problems before they become widespread. |

Benefits for Users in the Long Run:

| Advantages                | Description                                                                                                         |
|---------------------------|---------------------------------------------------------------------------------------------------------------------|
| Faster Bug Fixes          | With telemetry data, developers can pinpoint issues affecting specific users and prioritize fixing them quickly.  |
| Better Features           | Telemetry helps developers understand user needs and preferences. This allows them to focus on features that will be genuinely useful and improve your overall experience. |
| A More Stable Experience  | By identifying and resolving issues early, telemetry helps create a more stable and reliable software experience for everyone. |

## Installation-time telemetry

This telemetry is executed only once during software installation or Docker container startup. It collects information at the moment of installation and does not run afterward.

This telemetry collects the relevant data during the installation, such as system configuration, hardware specifications, software version, and environment details. After the installation is completed, this telemetry process does not run again or collect additional data.

This telemetry helps us to gain insights into the initial setup to tailor future updates or support.

### Installation-time telemetry file example

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

### Disable installation telemetry

This telemetry feature is enabled by default.

You can disable this telemetry if you decide not to send installation data to Percona. Set the `PERCONA_TELEMETRY_DISABLE=1` environment variable for either the root user or the operating system before installing.

These actions do not affect the continuous telemetry system.

=== "Debian-derived distribution"

    Add the environment variable before the installation process.

    ```{.bash data-prompt="$"}
    $ sudo PERCONA_TELEMETRY_DISABLE=1 apt install percona-server-server
    ```

=== "Red Hat-derived distribution"

    Add the environment variable before the installation process.
    
    ```{.bash data-prompt="$"}
    $ sudo PERCONA_TELEMETRY_DISABLE=1 yum install percona-server-server
    ```

=== "DOCKER"

    Add the environment variable when running a command in a new container.
    
    ```{.bash data-prompt="$"}
    $ docker run -d -e MYSQL_ROOT_PASSWORD=test1234# -e PERCONA_TELEMETRY_DISABLE=1 --name=percona-server percona/percona-server:8.1
    ```

## Continuous telemetry

This telemetry system involves setting up a telemetry agent and a database (DB) component. It continuously collects and sends information daily.
 
 The telemetry agent runs at scheduled daily intervals to collect data. The agent gathers data (for example, usage statistics) and sends this information to the Percona platform.

Percona includes the telemetry systems only in software packages, compressed archives (tarballs), and Docker images. The continuous telemetry system requires a telemetry agent and a specific folder to write data when installed from compressed archives (tarballs). If these elements are available, telemetry collects and sends the data.

## Elements of the continuous telemetry system

Percona collects information using these elements:

| Function                          | Description |
|-------------------------------|-------------|
| [Percona Telemetry DB component](#overview-of-the-db-component) | This component collects metrics directly from the database and stores them in a metrics file. |
| [Metrics File](#locations-of-metrics-files-and-telemetry-history) | This standalone file on the database host's file system stores the collected metrics. |
| [Telemetry Agent](#percona-telemetry-agent) | This independent process runs on your database host's operating system and performs the following tasks:<br> - Collects OS-level metrics.<br>- Reads the metrics file and adds the OS-level metrics.<br>- Sends the complete set of metrics to the Percona Platform.<br> - Collects the list of installed Percona packages using the local package manager. |

Telemetry uses the Percona Platform with these components:


| Functions             | Description                                                                                  |
|-------------------|----------------------------------------------------------------------------------------------|
| Telemetry Service | This service offers an API endpoint for sending telemetry data. It handles incoming requests and saves the data into telemetry storage. |
| Telemetry Storage | This component stores all telemetry data for the long term.                                  |

## Overview of the DB component

The Percona Server for MySQL includes a DB component by default during installation. This component extends the database's functionality in one of these ways, depending on the specific database:

* Modifying the source code directly

* Adding modular components

* Adding self-contained extensions

The DB component has the following qualities:

* Collects metrics from the database daily

* Writes these metrics to a new JSON file on the local file system, named with a timestamp and the .json extension

* Stores only the most recent week's data by deleting older Metrics files before creating a new one.

The DB component does NOT collect the following:

* Database names

* User names or credentials

* Data entered by users

## Locations of metrics files and telemetry history

Percona stores the Metrics file in one of the following directories on the local file system. The location depends on the product.

* Telemetry root path - `/usr/local/percona/telemetry`

* PSMDB (mongod) root path -   `${telemetry root path}/psmdb/`

* PSMDB (mongos) root path - `${telemetry root path}/psmdbs/`

* PS root path -   `${telemetry root path}/ps/`

* PXC root path - `${telemetry root path}/pxc/`

* PG root path - `${telemetry root path}/pg/`

Percona archives the telemetry history in `${telemetry root path}/history/`.

### Metrics file format

The Metrics file uses the Javascript Object Notation (JSON) format. Percona reserves the right to extend the current set of JSON structure attributes in the future.  

The following is an example of the Metrics file content:

```JSON
{
  "db_instance_id": "e83c568c-e140-11ee-8320-7e207666b18a",
  "pillar_version": "8.0.35-27",
  "active_plugins": [
    "binlog",
    "mysql_native_password",
    "sha256_password",
    "caching_sha2_password",
    "sha2_cache_cleaner",
    "daemon_keyring_proxy_plugin",
    "PERFORMANCE_SCHEMA",
    "CSV",
    "MEMORY",
    "InnoDB",
    "INNODB_TRX",
    "INNODB_CMP",
    "INNODB_CMP_RESET",
    "INNODB_CMPMEM",
    "INNODB_CMPMEM_RESET",
    "INNODB_CMP_PER_INDEX",
    "INNODB_CMP_PER_INDEX_RESET",
    "INNODB_BUFFER_PAGE",
    "INNODB_BUFFER_PAGE_LRU",
    "INNODB_BUFFER_POOL_STATS",
    "INNODB_TEMP_TABLE_INFO",
    "INNODB_METRICS",
    "INNODB_FT_DEFAULT_STOPWORD",
    "INNODB_FT_DELETED",
    "INNODB_FT_BEING_DELETED",
    "INNODB_FT_CONFIG",
    "INNODB_FT_INDEX_CACHE",
    "INNODB_FT_INDEX_TABLE",
    "INNODB_TABLES",
    "INNODB_TABLESTATS",
    "INNODB_INDEXES",
    "INNODB_TABLESPACES",
    "INNODB_COLUMNS",
    "INNODB_VIRTUAL",
    "INNODB_CACHED_INDEXES",
    "INNODB_SESSION_TEMP_TABLESPACES",
    "MyISAM",
    "MRG_MYISAM",
    "TempTable",
    "ARCHIVE",
    "BLACKHOLE",
    "ngram",
    "mysqlx_cache_cleaner",
    "mysqlx",
    "ROCKSDB",
    "rpl_semi_sync_source",
    "ROCKSDB_CFSTATS",
    "ROCKSDB_DBSTATS",
    "ROCKSDB_PERF_CONTEXT",
    "ROCKSDB_PERF_CONTEXT_GLOBAL",
    "ROCKSDB_CF_OPTIONS",
    "ROCKSDB_GLOBAL_INFO",
    "ROCKSDB_COMPACTION_HISTORY",
    "ROCKSDB_COMPACTION_STATS",
    "ROCKSDB_ACTIVE_COMPACTION_STATS",
    "ROCKSDB_DDL",
    "ROCKSDB_INDEX_FILE_MAP",
    "ROCKSDB_LOCKS",
    "ROCKSDB_TRX",
    "ROCKSDB_DEADLOCK"
  ],
  "active_components": [
    "file://component_percona_telemetry"
  ],
  "uptime": "6185",
  "databases_count": "7",
  "databases_size": "33149",
  "se_engines_in_use": [
    "InnoDB",
    "ROCKSDB"
  ],
  "replication_info": {
    "is_semisync_source": "1",
    "is_replica": "1"
  }
}
```

## Percona telemetry agent 

This program, called `percona-telemetry-agent`, constantly runs in the background on your server's operating system. It manages JSON files, which store the collected data in a specific location (`${telemetry root path}`). This agent can create, read, write, and delete these files.

The agent's log file, containing information about its activity, is located at `/var/log/percona/telemetry-agent.log`.

In the first 24 hours, no information is collected or sent. After that period, the agent tries to send the collected information to Percona's servers (Percona Platform) daily. If this operation fails, the agent retries up to five times. After the data is successfully sent, the agent saves a copy of the sent data in a separate "history" folder, and then, deletes the original file created by the database.

The agent won't send any data if the target directory doesn't contain specific files related to Percona software.

### Telemetry agent payload example

The following is an example of a telemetry agent payload:

```json
{
  "reports": [
    {
      "id": "B5BDC47B-B717-4EF5-AEDF-41A17C9C18BB",
      "createTime": "2023-09-01T10:56:49Z",
      "instanceId": "B5BDC47B-B717-4EF5-AEDF-41A17C9C18BA",
      "productFamily": "PRODUCT_FAMILY_PS",
      "metrics": [
        {
          "key": "OS",
          "value": "Ubuntu"
        },
        {
          "key": "pillar_version",
          "value": "8.0.33-25"
        }
      ]
    }
  ]
}
```

The agent sends information about the database and metrics.

| Key | Description |
|---|---|
| "id" | A randomly generated Universally Unique Identifier (UUID) version 4 of the request|
| "createTime" | UNIX timestamp |
| "instanceId" | The DB Host ID. The value can be taken from the `instanceId`, the `/usr/local/percona/telemetry_uuid` or generated as a UUID version 4 if the file is absent. |
| "productFamily" | The value from the file path |
| "metrics" | An array of key:value pairs collected from the Metrics file.

The following operating system-level metrics are sent with each check:

| Key | Description |
|---|---|
| "OS" | The name of the operating system |
| "hardware_arch" | CPU architecture used on the DB host |
| "deployment" | How the application was deployed. <br> The possible values could be "PACKAGE" or "DOCKER". |
| "installed_packages" | A list of the installed Percona packages. |

The information includes the following:

* Package name

* Package version - the same format as Red Hat Enterprise Linux or Debian

* Package repository - if possible

The package names must fit the following pattern:

* `percona-*`

* `Percona-*`

* `proxysql*`

* `pmm`

* `etcd*`

* `haproxy`

* `patroni`

* `pg*`

* `postgis`

* `wal2json`


## Disable continuous telemetry

Percona software enables the continuous telemetry system by default. Disable the Telemetry agent and uninstall the DB component to turn off this telemetry completely.

These actions do not affect Installation-time telemetry.

### Disable the telemetry agent

You can either disable the telemetry agent for a session or permanently.

=== "Disable temporarily"

    Turn off telemetry temporarily until the next server restart:

    ```{.bash data-prompt=$}
    $ systemctl stop percona-telemetry-agent
    ```

=== "Disable permanently"

    Turn off telemetry permanently:

    ```{.bash data-prompt=$}
    $ systemctl disable percona-telemetry-agent
    ```

#### Telemetry agent dependencies and removal considerations

Installing a Linux package also installs mandatory dependencies. The Telemetry agent is a mandatory dependency for Percona Server for MySQL packages. Removing the agent will delete the database.

On YUM-based systems, the system removes the Telemetry agent package when you remove the last dependency package.

On APT-based systems, you must use the `--autoremove` option to remove all dependencies, as the system doesn't automatically remove the Telemetry agent when you remove the database package.

The `--autoremove` option only removes unnecessary dependencies. It doesn't remove dependencies required by other packages or guarantee the removal of all package-associated dependencies.

### Disable DB component

The DB component continues to generate daily telemetry files and store them for a week, even after you stop the telemetry agent service. These files persist for seven days.

Uninstall the component on the server without restarting the database server:

```{.bash data-prompt="mysql"}
mysql> UNINSTALL COMPONENT "file://component_percona_telemetry";
```

Restarting the database server after uninstalling the component can reactivate the telemetry component. This action happens because the server reloads settings during restart, including any instructions for telemetry.

To prevent this reactivation, edit the my.cnf configuration file. Add this line:

```{text}
[mysqld]

percona_telemetry_disable=1
```

Restart the server after editing the configuration file. This setting ensures that the telemetry remains disabled even after a server restart.

[Percona Privacy statement]: https://www.percona.com/privacy-policy#h.e34c40q8sb1a
[disable telemetry]: #disable-telemetry