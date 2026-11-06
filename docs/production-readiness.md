# Production readiness and baseline configuration

Prepare each production host after you install Percona Server for MySQL.

This page is a Day-1 **tuning baseline**. The page covers host checks, `my.cnf` sizing, restart safety, and Percona feature activation.

Complete security, recovery, availability, and operating-system hardening in the related guides:

* [First five minutes after installation](first-five-minutes.md)

* [Sanity check: First five minutes](sanity-check.md)

* [Post-installation](post-installation.md)

* [Backup and restore overview](backup-restore-overview.md)

Use these values as a baseline. Test each value with a representative workload. Change one value at a time.

!!! important

    Test this configuration in a test environment before production use.

    Memory, storage latency, concurrency, durability, and replication affect the correct values.

    Stop when a check fails. Fix the issue before you change memory, connections, or restart MySQL.

## Key terms

| Term | Meaning |
|---|---|
| Direct input/output (I/O) | The server writes data files without the operating system page cache. MySQL often uses the `O_DIRECT` flush method for this path. |
| Buffer pool hit rate | The share of InnoDB page reads that MySQL serves from memory. A low hit rate can show that the buffer pool is too small for the working set. |
| Binary logs | Server files that record data changes. Replication and point-in-time recovery use these files. |
| Non-Uniform Memory Access (NUMA) | A memory layout on multi-socket hosts. Nearby memory is faster than remote memory. MySQL can spread allocations across NUMA nodes. |
| Point-in-time recovery | A restore method that applies a full backup, then applies binary log events up to a selected time. |
| Drop-in file | An extra option file that MySQL loads from a configuration directory. Use one controlled drop-in file for production baseline values. |

## Find and edit the active configuration file

Complete these steps before you change production values.

### List every option file that MySQL can load

1. List the default option-file search order:

    ```shell
    mysqld --help --verbose 2>/dev/null | grep -A1 'Default options'
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Default options are read from the following files in the given order:
        /etc/my.cnf /etc/mysql/my.cnf ~/.my.cnf
        ```

        **Pass:** The command prints at least one readable path.

        **Stop:** The command prints no paths, or every listed path is missing and you cannot locate the package configuration.

2. Show which option files a server process would read, including directories:

    ```shell
    mysqld --verbose --help 2>/dev/null | awk '/^Default options/,/^$/'
    ls -la /etc/my.cnf /etc/mysql/my.cnf /etc/mysql/conf.d /etc/mysql/mysql.conf.d /etc/my.cnf.d 2>/dev/null
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Default options are read from the following files in the given order:
        /etc/my.cnf /etc/mysql/my.cnf ~/.my.cnf

        -rw-r--r-- 1 root root  120 Apr  1 10:00 /etc/my.cnf
        /etc/mysql/mysql.conf.d:
        -rw-r--r-- 1 root root 3122 Apr  1 10:00 mysqld.cnf
        ```

        **Pass:** You can list every file under the included directories for your package.

        **Stop:** You cannot identify which directories MySQL includes. Do not edit random files.

### How duplicate values win

MySQL reads option files in search order. Later values override earlier values for the same option and group.

Rules:

* Values in a later file override values in an earlier file.

* Within one file, a later line for the same option overrides an earlier line.

* Command-line options override option-file values.

* Files in an included directory load in alphabetical order. A `zz-production.cnf` file loads after `mysqld.cnf` and overrides matching options.

Confirm the effective value after restart with `SHOW VARIABLES`. The effective value is the final winner.

### Common package locations

* Debian and Ubuntu often use `/etc/mysql/my.cnf` and files under `/etc/mysql/conf.d/` or `/etc/mysql/mysql.conf.d/`.

* Red Hat Enterprise Linux and Oracle Linux often use `/etc/my.cnf` and files under `/etc/my.cnf.d/`.

Prefer a dedicated drop-in file for production changes:

* `/etc/mysql/mysql.conf.d/zz-production.cnf`

* `/etc/my.cnf.d/zz-production.cnf`

### Create the production drop-in file safely

Use these steps when the drop-in file does not exist.

1. Choose the drop-in directory for your operating system. Confirm that the directory exists:

    ```shell
    ls -ld /etc/mysql/mysql.conf.d
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        drwxr-xr-x 2 root root 4096 Apr  1 10:00 /etc/mysql/mysql.conf.d
        ```

        On Red Hat-based systems, check `/etc/my.cnf.d` instead.

        **Pass:** The directory exists and belongs to `root`.

        **Stop:** The directory is missing. Install the server package, or create only the directory that your package already includes through its main `my.cnf`.

2. Create the drop-in file only if the file is absent:

    ```shell
    DROPIN=/etc/mysql/mysql.conf.d/zz-production.cnf
    test -e "$DROPIN" && echo "STOP: file exists: $DROPIN" && exit 1
    sudo tee "$DROPIN" >/dev/null <<'EOF'
    [mysqld]
    # Add production baseline settings in later steps.
    EOF
    sudo chmod 644 "$DROPIN"
    sudo chown root:root "$DROPIN"
    ls -l "$DROPIN"
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        -rw-r--r-- 1 root root 62 Aug  3 10:00 /etc/mysql/mysql.conf.d/zz-production.cnf
        ```

        **Pass:** The command creates a new `root`-owned file with mode `644`.

        **Stop:** The script prints `STOP: file exists`. Do not overwrite an existing file. Save a backup first, then edit that file.

3. Save a timestamped backup after the file exists and before every edit:

    ```shell
    DROPIN=/etc/mysql/mysql.conf.d/zz-production.cnf
    sudo cp "$DROPIN" "$DROPIN.bak.$(date +%Y%m%d%H%M%S)"
    ls -l "$DROPIN".bak.*
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        -rw-r--r-- 1 root root 62 Aug  3 10:01 /etc/mysql/mysql.conf.d/zz-production.cnf.bak.20260803100100
        ```

        **Pass:** A new `.bak.<timestamp>` file appears beside the drop-in file.

        **Stop:** The copy fails. Fix permissions or free space before you edit.

4. Edit the drop-in file as the `root` operating system user. Place production settings under the `[mysqld]` section.

5. Validate the configuration before you restart:

    ```shell
    sudo mysqld --validate-config
    echo "exit_status=$?"
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        exit_status=0
        ```

        **Pass:** No error text. Exit status is `0`.

        **Stop:** Any error text, or a non-zero exit status. Fix the option file before restart.

!!! tip

    Keep one production drop-in file under version control. Avoid mixed edits across many option files when one controlled file can hold the baseline.

## Day-1 host checks

Run these checks on the database host before you tune MySQL.

For each check:

* **Pass** means continue.

* **Stop** means fix the issue before memory or connection changes.

### Storage and free space

Check free space for the data directory and related mounts:

```shell
df -hT /
df -hT /var/lib/mysql
```

??? example "Expected output"

    ```{.text .no-copy}
    Filesystem     Type  Size  Used Avail Use% Mounted on
    /dev/sda1      ext4  200G   40G  160G  20% /
    /dev/sdb1      xfs   500G  120G  380G  24% /var/lib/mysql
    ```

    **Pass:** Each MySQL mount has enough free space for data growth, binary logs, and temporary files. Many teams stop when use reaches 80% or higher.

    **Stop:** Any MySQL mount is near capacity, read-only, missing, or reports an unexpected file system type for your plan.

Confirm MySQL paths:

```sql
SHOW VARIABLES WHERE Variable_name IN (
    'datadir',
    'innodb_log_group_home_dir',
    'tmpdir',
    'log_bin_basename',
    'slow_query_log_file',
    'log_error'
);
```

??? example "Expected output"

    ```{.text .no-copy}
    +---------------------------+----------------------------------+
    | Variable_name             | Value                            |
    +---------------------------+----------------------------------+
    | datadir                   | /var/lib/mysql/                  |
    | innodb_log_group_home_dir | ./                               |
    | log_bin_basename          | /var/lib/mysql/binlog            |
    | log_error                 | /var/log/mysql/error.log         |
    | slow_query_log_file       | /var/lib/mysql/host-slow.log     |
    | tmpdir                    | /tmp                             |
    +---------------------------+----------------------------------+
    ```

    Paths depend on the install method and configuration.

    **Pass:** Each path exists on a mount with free space, and you know which mount holds data, logs, and temporary files.

    **Stop:** A required path is missing, points to a full mount, or places temporary files on an unsuitable filesystem.

### Direct I/O and flush method

Confirm the active flush method:

```sql
SHOW VARIABLES LIKE 'innodb_flush_method';
```

??? example "Expected output"

    ```{.text .no-copy}
    +---------------------+----------+
    | Variable_name       | Value    |
    +---------------------+----------+
    | innodb_flush_method | O_DIRECT |
    +---------------------+----------+
    ```

    **Pass:** The value is `O_DIRECT` on a supported Linux data filesystem.

    **Stop and review:** The value is `fsync` and you expected direct I/O. Confirm filesystem support before you force `O_DIRECT`.

Test direct I/O on the same filesystem as the data directory, outside the live data directory:

```shell
DATADIR=$(mysql -Nse "SELECT @@datadir")
FS_ROOT=$(df --output=target "$DATADIR" | tail -n 1)
TESTDIR="$FS_ROOT/mysql-dio-check"
sudo mkdir -p "$TESTDIR"
sudo chown root:root "$TESTDIR"
sudo chmod 700 "$TESTDIR"
sudo dd if=/dev/zero of="$TESTDIR/dio-test" bs=4096 count=1 oflag=direct
echo "dd_exit_status=$?"
sudo rm -f "$TESTDIR/dio-test"
sudo rmdir "$TESTDIR"
```

??? example "Expected output"

    ```{.text .no-copy}
    1+0 records in
    1+0 records out
    4096 bytes (4.1 kB, 4.0 KiB) copied, 0.000123 s, 33.3 MB/s
    dd_exit_status=0
    ```

    **Pass:** `dd` writes one 4096-byte record. Exit status is `0`. The cleanup commands remove the test file and directory.

    **Stop:** `dd` prints `Invalid argument`, another I/O error, or a non-zero exit status. Do not force `innodb_flush_method=O_DIRECT` on that filesystem.

    The test directory sits on the same mount as `datadir`, but outside `/var/lib/mysql` contents. Replace `FS_ROOT` only when `df` shows a different mount point.

### Memory and swap

Check physical memory and swap:

```shell
free -h
swapon --show
```

??? example "Expected output"

    ```{.text .no-copy}
                  total        used        free      shared  buff/cache   available
    Mem:           15Gi       2.1Gi       8.0Gi       100Mi       5.0Gi        12Gi
    Swap:         2.0Gi          0B       2.0Gi

    NAME      TYPE      SIZE USED PRIO
    /swapfile file      2.0G   0B   -2
    ```

    **Pass:** Available memory covers the planned buffer pool plus operating-system headroom. Swap used stays near zero under normal load.

    **Stop:** Available memory cannot support the planned buffer pool. Sustained swap use already appears for MySQL. Resolve memory pressure before you raise `innodb_buffer_pool_size`.

### Logs

Confirm that error and slow query logging are active:

```sql
SHOW VARIABLES WHERE Variable_name IN (
    'log_error',
    'slow_query_log',
    'slow_query_log_file',
    'long_query_time',
    'log_output'
);
```

??? example "Expected output"

    ```{.text .no-copy}
    +---------------------+------------------------------+
    | Variable_name       | Value                        |
    +---------------------+------------------------------+
    | log_error           | /var/log/mysql/error.log     |
    | log_output          | FILE                         |
    | long_query_time     | 1.000000                     |
    | slow_query_log      | ON                           |
    | slow_query_log_file | /var/lib/mysql/host-slow.log |
    +---------------------+------------------------------+
    ```

    **Pass:** `log_error` points to a writable file. For this baseline, `slow_query_log` is `ON` and `log_output` includes `FILE`.

    **Stop:** `log_error` is empty or unwritable. Slow logging remains off when you planned to enable it. Fix logging before you continue.

Check recent error log lines:

```shell
sudo tail -n 50 /var/log/mysql/error.log
```

??? example "Expected output"

    ```{.text .no-copy}
    ...
    [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections.
    ```

    The path can differ. Use the `log_error` value from MySQL.

    **Pass:** The log shows a ready-for-connections message. No unresolved `[ERROR]` lines block startup.

    **Stop:** The log shows startup failures, permission errors, or repeated severe errors. Resolve those errors before configuration changes.

## Day-1 checklist

### Storage

* Place data files, redo logs, binary logs, and temporary files on storage with predictable latency.

* Confirm that the Linux file system supports direct I/O.

* Monitor free space for each data directory and log directory.

* Store backups outside the database host.

* Test a restore from the backup.

### Memory

* Set `innodb_buffer_pool_size` to 60–70% of physical random-access memory (RAM) on a dedicated database host.

* Use a lower percentage when MySQL shares the host with other services.

* Reserve memory for the operating system, Performance Schema, connections, temporary tables, sorts, replication, and backup tools.

* Test the highest expected connection count.

* Monitor swap use, resident memory, buffer pool hit rate, and temporary table use.

Connection buffers use memory only when a connection needs each buffer. Actual use depends on workload concurrency.

Check the buffer pool hit rate:

```sql
SHOW GLOBAL STATUS WHERE Variable_name IN (
    'Innodb_buffer_pool_read_requests',
    'Innodb_buffer_pool_reads'
);
```

??? example "Expected output"

    ```{.text .no-copy}
    +-----------------------------------+-------------+
    | Variable_name                     | Value       |
    +-----------------------------------+-------------+
    | Innodb_buffer_pool_read_requests  | 125000000   |
    | Innodb_buffer_pool_reads          | 250000      |
    +-----------------------------------+-------------+
    ```

Calculate the hit rate:

`1 - (Innodb_buffer_pool_reads / Innodb_buffer_pool_read_requests)`

A result near `1` means MySQL serves most reads from memory.

**Pass:** After representative load, the hit rate stays high enough for your service goals.

**Stop and review:** The hit rate stays low after load. Confirm that the working set exceeds the buffer pool before you raise memory further.

### Connections

* Add all application connection pool limits.

* Add connections for administration and metrics collection.

* Add a small margin for failures.

* Use the result for `max_connections`.

* Set limits on application connection pools.

* Queue or reject excess application work before MySQL reaches capacity.

* Reserve access for database administrators.

* Create an alert for high connection use.

Use the default one-thread-per-connection model for most workloads. Consider the Percona thread pool after tests show a high-concurrency requirement. The thread pool usually offers little benefit below 20,000 connections.

Check active, peak, and maximum connection values:

```sql
SHOW GLOBAL STATUS WHERE Variable_name IN ('Threads_connected', 'Max_used_connections');
SHOW VARIABLES LIKE 'max_connections';
```

??? example "Expected output"

    ```{.text .no-copy}
    +----------------------+-------+
    | Variable_name        | Value |
    +----------------------+-------+
    | Max_used_connections | 84    |
    | Threads_connected    | 32    |
    +----------------------+-------+

    +-----------------+-------+
    | Variable_name   | Value |
    +-----------------+-------+
    | max_connections | 200   |
    +-----------------+-------+
    ```

    The connection values depend on the workload. `Max_used_connections` must remain below `max_connections`.

    **Pass:** `Max_used_connections` stays below `max_connections` with headroom for peaks.

    **Stop:** `Max_used_connections` equals `max_connections`, or applications already hit connection errors. Raise capacity only after you confirm application pool limits.

### Logs and observability

* Collect, retain, and monitor the error log.

* Enable the slow query log with a cautious threshold.

* Adjust the threshold and sample rate after you measure log volume.

* Use `log_output=FILE` when Percona Monitoring and Management (PMM) Query Analytics reads the slow query log.

* Define retention and rotation for error, slow, binary, and audit logs.

* Create alerts for availability, disk space, replication lag, connection pressure, and resource saturation.

Logs can use substantial I/O capacity and disk space.

## Calculate memory and connection settings

### Buffer pool size

Use this formula on a dedicated MySQL host:

`innodb_buffer_pool_size ≈ total_RAM × 0.60 to 0.70`

Example for a 16 GiB host:

* `16 × 0.70 ≈ 11.2`

* Use `innodb_buffer_pool_size = 11G`

Leave memory for the following consumers:

* Operating system caches and kernel work

* Performance Schema

* Per-connection buffers

* Temporary tables and sort buffers

* Replication and backup tools

Use a lower percentage when other services share the host.

### Connection limit

Use this formula:

`max_connections = application_pool_total + admin_connections + monitoring_connections + margin`

Example:

* Three application pools use 50 connections each: `150`

* Administration needs `10`

* Monitoring needs `10`

* Margin is `30`

* Result: `max_connections = 200`

Keep each application pool below its own limit. Do not rely on MySQL alone to absorb unbounded connection growth.

## Recommended production `my.cnf` baseline

Configure a dedicated MySQL host as follows:

* Run a Linux operating system.

* Allocate 16 GiB of RAM.

* Use a solid-state drive (SSD) or Non-Volatile Memory Express (NVMe) storage device.

In this example, replace each value marked `CHANGE` before deployment.

```ini
[mysqld]

# Memory
# CHANGE: Use 60-70% of RAM on a dedicated database host.
# 11G is about 70% of the RAM on a 16 GiB host.
innodb_buffer_pool_size = 11G

# Connections
# CHANGE: Add application pool limits, metrics collection, and an administrative margin.
max_connections = 200

# Storage and durability
# MySQL 8.4 selects O_DIRECT on supported Linux systems.
# Set this value only after you validate the file system and storage.
# innodb_flush_method = O_DIRECT
innodb_flush_log_at_trx_commit = 1
sync_binlog = 1

# Logs
log_output = FILE
slow_query_log = ON
long_query_time = 1
log_slow_verbosity = standard

# Keep binary logs for point-in-time recovery and replication.
# CHANGE: Choose a retention period from the backup and recovery policy.
binlog_expire_logs_seconds = 604800
```

??? example "Expected result"

    The configuration file contains one `[mysqld]` section with the selected production values.

The durability values protect committed transactions during an operating system or host failure.

Lower values for `innodb_flush_log_at_trx_commit` or `sync_binlog` can increase throughput. This change can also create a documented data loss period.

### Apply the baseline

1. Save a copy of the active configuration. See [Find and edit the active configuration file](#find-and-edit-the-active-configuration-file).

2. Replace the memory, connection, and retention values.

3. Validate the configuration:

    ```shell
    sudo mysqld --validate-config
    echo "exit_status=$?"
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        exit_status=0
        ```

        **Pass:** No error text. Exit status is `0`.

        **Stop:** Any error text, or a non-zero exit status. Do not restart.

4. Restart MySQL during a maintenance period:

    ```shell
    sudo systemctl restart mysql
    ```

    Some installs use the `mysqld` unit name. Use the unit that your package provides.

5. Check the service state and error log:

    ```shell
    sudo systemctl status mysql --no-pager
    sudo tail -n 100 /var/log/mysql/error.log
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Active: active (running)
        ...
        [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections.
        ```

        **Pass:** The unit is `active (running)`. The error log shows ready for connections.

        **Stop:** The unit is `failed` or `inactive`, or the error log shows startup errors. Follow [Roll back after a failed restart](#roll-back-after-a-failed-restart).

6. Confirm the active values:

    ```sql
    SHOW VARIABLES WHERE Variable_name IN (
        'binlog_expire_logs_seconds',
        'innodb_buffer_pool_size',
        'innodb_flush_log_at_trx_commit',
        'innodb_flush_method',
        'log_output',
        'log_slow_verbosity',
        'long_query_time',
        'max_connections',
        'slow_query_log',
        'sync_binlog'
    );
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        +------------------------------------+-------------+
        | Variable_name                      | Value       |
        +------------------------------------+-------------+
        | binlog_expire_logs_seconds         | 604800      |
        | innodb_buffer_pool_size            | 11811160064 |
        | innodb_flush_log_at_trx_commit     | 1           |
        | innodb_flush_method                | O_DIRECT    |
        | log_output                         | FILE        |
        | log_slow_verbosity                 | standard    |
        | long_query_time                    | 1.000000    |
        | max_connections                    | 200         |
        | slow_query_log                     | ON          |
        | sync_binlog                        | 1           |
        +------------------------------------+-------------+
        ```

        MySQL can return `fsync` for `innodb_flush_method`. The value depends on direct I/O support.

        **Pass:** Each value matches the drop-in file that you intended to load.

        **Stop:** A value still comes from an older option file. Recheck file order and duplicate settings.

### Roll back after a failed restart

If MySQL fails to start after a configuration change, restore the previous file and restart.

1. Check the service state and the last error lines:

    ```shell
    sudo systemctl status mysql --no-pager
    sudo journalctl -u mysql -n 50 --no-pager
    sudo tail -n 100 /var/log/mysql/error.log
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Active: failed
        ...
        [ERROR] [MY-000067] [Server] unknown variable 'example_bad_setting=1'.
        ```

2. Restore the backup that you created before the edit:

    ```shell
    sudo cp /etc/mysql/mysql.conf.d/zz-production.cnf.bak.TIMESTAMP \
      /etc/mysql/mysql.conf.d/zz-production.cnf
    ```

    Replace `TIMESTAMP` with the backup suffix from your copy step. Use the path that matches your operating system.

3. Validate the restored configuration:

    ```shell
    sudo mysqld --validate-config
    ```

    ??? example "Expected output"

        A valid configuration produces no output. The command returns exit status zero.

4. Start MySQL:

    ```shell
    sudo systemctl start mysql
    ```

5. Confirm that the service is active and that clients can connect:

    ```shell
    sudo systemctl is-active mysql
    mysql -u root -p -e "SELECT 1;"
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        active
        +---+
        | 1 |
        +---+
        | 1 |
        +---+
        ```

6. Fix the rejected setting offline. Validate again. Apply the change in a new maintenance window.

### MySQL 8.4 defaults

Review each MySQL 8.0 override before you use the override with MySQL 8.4.

MySQL 8.4 has the following defaults:

* `innodb_adaptive_hash_index=OFF`.

* `innodb_change_buffering=none`.

* `innodb_flush_method=O_DIRECT` on supported Linux systems. MySQL uses `fsync` as the fallback.

* `innodb_io_capacity=10000`. This value targets SSD and NVMe storage. Hard disk drives may require a lower value.

* `innodb_log_buffer_size=64M`.

* `innodb_numa_interleave=ON`.

* `temptable_max_ram` uses 3% of total memory. The minimum value is 1 GiB. The maximum value is 4 GiB.

Read [Defaults and tuning guidance for MySQL 8.4](8.4-defaults-and-tuning.md) for more details.

## Percona feature quick-activation matrix

Each command requires the related package or component library. Run Structured Query Language (SQL) commands with the required administrative privileges.

Some features also require tables or policy definitions. Follow the linked procedure before activation.

| Feature | Activation | Production requirement |
|---|---|---|
| Thread pool | Add `thread_handling=pool-of-threads` under `[mysqld]`. Restart MySQL. | Use the feature only after high-concurrency tests show a benefit. Read [Thread pool](threadpool.md). |
| Audit Log Filter | Run `SET GLOBAL audit_log_filter.disable = false;` after component installation and filter assignment. | Complete the [Audit Log Filter installation](install-audit-log-filter.md) and [Audit Log Filter quickstart](audit-log-filter-quickstart.md). Define production filters and retention. |
| Data Masking | Create `mysql.masking_dictionaries`. Run `INSTALL COMPONENT 'file://component_masking_functions';`. | Use views and privileges to restrict access to unmasked data. Read [Install the data masking component](install-data-masking-component.md). |
| Extended Slow Log | Add `slow_query_log=ON` and `log_slow_verbosity=standard` under `[mysqld]`. | Start with `long_query_time=1`. Measure log volume. Use `log_slow_rate_limit` when you need a sample. Read [Slow query log](slow-extended.md). |

Verify each feature:

```sql
SHOW VARIABLES LIKE 'thread_handling';
SHOW GLOBAL STATUS LIKE 'audit_log_filter_events_written';
SELECT * FROM mysql.component
WHERE component_urn = 'file://component_masking_functions';
SHOW VARIABLES WHERE Variable_name IN (
    'slow_query_log',
    'log_slow_verbosity',
    'long_query_time'
);
```

??? example "Expected output"

    ```{.text .no-copy}
    +-----------------+-----------------+
    | Variable_name   | Value           |
    +-----------------+-----------------+
    | thread_handling | pool-of-threads |
    +-----------------+-----------------+

    +---------------------------------+-------+
    | Variable_name                   | Value |
    +---------------------------------+-------+
    | audit_log_filter_events_written | 42    |
    +---------------------------------+-------+

    +--------------+--------------------+------------------------------------+
    | component_id | component_group_id | component_urn                      |
    +--------------+--------------------+------------------------------------+
    | 2            | 2                  | file://component_masking_functions |
    +--------------+--------------------+------------------------------------+

    +--------------------+----------+
    | Variable_name      | Value    |
    +--------------------+----------+
    | log_slow_verbosity | standard |
    | long_query_time    | 1.000000 |
    | slow_query_log     | ON       |
    +--------------------+----------+
    ```

    Event counts and component identifiers depend on the server.
