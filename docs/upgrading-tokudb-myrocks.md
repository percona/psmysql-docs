# Upgrade from systems that use the MyRocks or TokuDB storage engine and partitioned tables

Due to the limitation imposed by *MySQL*, the storage engine provides support for partitioning. *MySQL* 8.0 only provides support for
partitioned table for the *InnoDB* storage engine.

If you use partitioned tables with the *MyRocks* or *TokuDB* storage engine, the
upgrade may fail if you do not enable the native partitioning provided by the storage engine.

*TokuDB* is deprecated. For more information, see [TokuDB Introduction](tokudb-intro.md).

Before you attempt the upgrade, check whether you have any tables that are not using the native partitioning.

```{.bash data-prompt="$"}
$ mysqlcheck -u root --all-databases --check-upgrade
```

If tables are found, **mysqlcheck** issues a warning:

Enable either the rocksdb_enable_native_partition variable or
the tokudb_enable_native_partition variable depending on the storage
engine and restart the server.

Your next step is to alter the tables that are not using the native partitioning with the
`UPGRADE PARTITIONING` clause:

```text
ALTER TABLE <table-name> UPGRADE PARTITIONING
```

Complete these steps for each table that **mysqlcheck** list. Otherwise, the upgrade to 8.0 fails and your error log contains messages like the following:

```text
2018-12-17T18:34:14.152660Z 2 [ERROR] [MY-013140] [Server] The 'partitioning' feature is not available; you need to remove '--skip-partition' or use MySQL built with '-DWITH_PARTITION_STORAGE_ENGINE=1'
2018-12-17T18:34:14.152679Z 2 [ERROR] [MY-013140] [Server] Can't find file: './comp_test/t1_RocksDB_lz4.frm' (errno: 0 - Success)
2018-12-17T18:34:14.152691Z 2 [ERROR] [MY-013137] [Server] Can't find file: './comp_test/t1_RocksDB_lz4.frm' (OS errno: 0 - Success)
```

## Perform a distribution upgrade in-place on a system with installed Percona packages

The following is the recommended process for performing a distribution upgrade on a system with the Percona packages installed:

1. Record the installed Percona packages.

2. Back up the data and configurations.

3. Uninstall the Percona packages without removing the configuration file or data.

4. Perform the upgrade by following the distribution upgrade instructions

5. Reboot the system.

6. Install the Percona packages intended for the upgraded version of the distribution.
