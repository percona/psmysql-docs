# Percona MyRocks Installation Guide

Percona MyRocks is distributed as a separate package that can be enabled as a
plugin for *Percona Server for MySQL* 8.0 and later versions.

!!! note

    File formats across different MyRocks variants may not be compatible. *Percona Server for MySQL* supports only *Percona MyRocks*.  Migrating from one variant to another requires a logical data dump and reload.

* [Installing Percona MyRocks](#installing-percona-myrocks)

* [Removing Percona MyRocks](#removing-percona-myrocks)

## Installing Percona MyRocks

It is recommended to install Percona software from official repositories:

1. Configure Percona repositories as described in [Percona Software Repositories Documentation](https://www.percona.com/doc/percona-repo-config/index.html).

2. Install Percona MyRocks using the corresponding package manager:

    * For Debian or Ubuntu:

    ```shell
    $ sudo apt install percona-server-rocksdb
    ```

    !!! note

        Review the [Installing and configuring Percona Server for MySQL with ZenFS support](zenfs.md#zenfs) document for the [Installation](zenfs.md#zenfs-installation) and the [Configuration](zenfs.md#zenfs-configure) information.

    * For RHEL or CentOS:

    ```shell
    $ sudo yum install percona-server-rocksdb
    ```

After installation, you should see the following output:

```text
* This release of |Percona Server| is distributed with RocksDB storage engine.
* Run the following script to enable the RocksDB storage engine in Percona Server:
```

```shell
$ ps-admin --enable-rocksdb -u <mysql_admin_user> -p[mysql_admin_pass] [-S <socket>] [-h <host> -P <port>]
```

### Enable MyRocks with ps-admin

Run the `ps-admin` script as system root user or with **sudo**
and provide the MySQL root user credentials
to properly enable the RocksDB (MyRocks) storage engine:

```shell
$ sudo ps-admin --enable-rocksdb -u root -pPassw0rd
```

You should see the following output:

```text
Checking if RocksDB plugin is available for installation ...
INFO: ha_rocksdb.so library for RocksDB found at /usr/lib64/mysql/plugin/ha_rocksdb.so.

Checking RocksDB engine plugin status...
INFO: RocksDB engine plugin is not installed.

Installing RocksDB engine...
INFO: Successfully installed RocksDB engine plugin.
```

!!! note

    When you use the `ps-admin` script to enable Percona MyRocks, it performs the following:

    * Disables Transparent huge pages
    
    * Installs and enables the RocksDB plugin

If the script returns no errors,
Percona MyRocks should be successfully enabled on the server.
You can verify it as follows:

```sql
mysql> SHOW ENGINES;
```

The example of the output:

```text
+---------+---------+----------------------------------------------------------------------------+--------------+------+------------+
| Engine  | Support | Comment                                                                    | Transactions | XA   | Savepoints |
+---------+---------+----------------------------------------------------------------------------+--------------+------+------------+
| ROCKSDB | YES     | RocksDB storage engine                                                     | YES          | YES  | YES        |
...
| InnoDB  | DEFAULT | Percona-XtraDB, Supports transactions, row-level locking, and foreign keys | YES          | YES  | YES        |
+---------+---------+----------------------------------------------------------------------------+--------------+------+------------+
10 rows in set (0.00 sec)
```

Note that the RocksDB engine is not set to be default,
new tables will still be created using the InnoDB (XtraDB) storage engine.
To make RocksDB storage engine default,
set `default-storage-engine=rocksdb` in the `[mysqld]` section
of `my.cnf` and restart *Percona Server for MySQL*.

Alternatively, you can add `ENGINE=RocksDB`
after the `CREATE TABLE` statement
for every table that you create.

### Installing MyRocks Plugins

You can install MyRocks manually with a series of [INSTALL PLUGIN](https://dev.mysql.com/doc/refman/8.0/en/install-plugin.html) statements. You must have the `INSERT` privilege for the `mysql.plugin` system table.

The following statements install MyRocks:

```sql
INSTALL PLUGIN ROCKSDB SONAME 'ha_rocksdb.so';
INSTALL PLUGIN ROCKSDB_CFSTATS SONAME 'ha_rocksdb.so';
INSTALL PLUGIN ROCKSDB_DBSTATS SONAME 'ha_rocksdb.so';
INSTALL PLUGIN ROCKSDB_PERF_CONTEXT SONAME 'ha_rocksdb.so';
INSTALL PLUGIN ROCKSDB_PERF_CONTEXT_GLOBAL SONAME 'ha_rocksdb.so';
INSTALL PLUGIN ROCKSDB_CF_OPTIONS SONAME 'ha_rocksdb.so';
INSTALL PLUGIN ROCKSDB_GLOBAL_INFO SONAME 'ha_rocksdb.so';
INSTALL PLUGIN ROCKSDB_COMPACTION_HISTORY SONAME 'ha_rocksdb.so';
INSTALL PLUGIN ROCKSDB_COMPACTION_STATS SONAME 'ha_rocksdb.so';
INSTALL PLUGIN ROCKSDB_ACTIVE_COMPACTION_STATS SONAME 'ha_rocksdb.so';
INSTALL PLUGIN ROCKSDB_DDL SONAME 'ha_rocksdb.so';
INSTALL PLUGIN ROCKSDB_INDEX_FILE_MAP SONAME 'ha_rocksdb.so';
INSTALL PLUGIN ROCKSDB_LOCKS SONAME 'ha_rocksdb.so';
INSTALL PLUGIN ROCKSDB_TRX SONAME 'ha_rocksdb.so';
INSTALL PLUGIN ROCKSDB_DEADLOCK SONAME 'ha_rocksdb.so';
```

## Removing Percona MyRocks

It will not be possible to access tables created using the RocksDB engine
with another storage engine after you remove Percona MyRocks.
If you need this data, alter the tables to another storage engine.
For example, to alter the `City` table to InnoDB, run the following:

```sql
mysql> ALTER TABLE City ENGINE=InnoDB;
```

To disable and uninstall the RocksDB engine plugins,
use the `ps-admin` script as follows:

```shell
$ sudo ps-admin --disable-rocksdb -u root -pPassw0rd
```

You should see the following output:

```text
Checking RocksDB engine plugin status...
INFO: RocksDB engine plugin is installed.

Uninstalling RocksDB engine plugin...
INFO: Successfully uninstalled RocksDB engine plugin.
```

After the engine plugins have been uninstalled,
remove the Percona MyRocks package:

* For Debian or Ubuntu:

    ```shell
    $ sudo apt remove percona-server-rocksdb-8.0
    ```

* For RHEL or CentOS:

    ```shell
    $ sudo yum remove percona-server-rocksdb-80.x86_64
    ```

Finally, remove all the [MyRocks Server Variables](variables.md#myrocks-server-variables)
from the configuration file (`my.cnf`)
and restart *Percona Server for MySQL*.

### Uninstall MyRocks Plugins

You can [uninstall the plugins](https://dev.mysql.com/doc/refman/8.0/en/uninstall-plugin.html) for MyRocks. You must have the `DELETE` privilege for the `mysql.plugin` system table.

The following statements remove the MyRocks plugins:

```sql
UNINSTALL PLUGIN ROCKSDB;
UNINSTALL PLUGIN ROCKSDB_CFSTATS;
UNINSTALL PLUGIN ROCKSDB_DBSTATS;
UNINSTALL PLUGIN ROCKSDB_PERF_CONTEXT;
UNINSTALL PLUGIN ROCKSDB_PERF_CONTEXT_GLOBAL;
UNINSTALL PLUGIN ROCKSDB_CF_OPTIONS;
UNINSTALL PLUGIN ROCKSDB_GLOBAL_INFO;
UNINSTALL PLUGIN ROCKSDB_COMPACTION_HISTORY;
UNINSTALL PLUGIN ROCKSDB_COMPACTION_STATS;
UNINSTALL PLUGIN ROCKSDB_ACTIVE_COMPACTION_STATS;
UNINSTALL PLUGIN ROCKSDB_DDL;
UNINSTALL PLUGIN ROCKSDB_INDEX_FILE_MAP;
UNINSTALL PLUGIN ROCKSDB_LOCKS;
UNINSTALL PLUGIN ROCKSDB_TRX;
UNINSTALL PLUGIN ROCKSDB_DEADLOCK;
```
