# TokuDB changes in Percona Server for MySQL by version

## Removed

[Percona Server for MySQL 8.0.28-19](release-notes/Percona-Server-8.0.28-19.md) removes the TokuDB storage engine and this storage engine is no longer supported. 

We have removed the storage engine from the installation packages and disabled the storage engine in our binary builds.

## Disabled 

[Percona Server for MySQL 8.0.26-16](release-notes/Percona-Server-8.0.26-16.md) includes the  TokuDB storage engine plugins in the binary builds and packages but disables them.

The `tokudb_enabled` option and the `tokudb_backup_enabled` option control the state of the plugins and have a default setting of `FALSE`. The plugins fail to initialize and print a deprecation message if you attempt to load them.

We recommend [migrating the data to the MyRocks storage engine](removing-tokudb.md#migrate-to-myrocks)

Set the `tokudb_enabled` and `tokudb_backup_enabled` options to `TRUE` in your `my.cnf` configuration file. 

This action enables the plugins needed for migration. 

```{.text .no-copy}
[tokudb]

# Enable TokuDB
tokudb_enabled=TRUE
# Enable TokuDB backup
tokudb_backup_enabled=TRUE
```

After saving these changes, restart your server instance to apply the new settings. This restart is crucial since it initializes the plugins and prepares your system for migration to MyRocks.

## Deprecated 

The TokuDB storage engine was declared deprecated in [Percona Server for MySQL 8.0](release-notes/Percona-Server-8.0.13-3.md). For more information, see the Percona blog post: [Heads-Up: TokuDB Support Changes and Future Removal from Percona Server for MySQL 8.0](https://www.percona.com/blog/2021/05/21/tokudb-support-changes-and-future-removal-from-percona-server-for-mysql-8-0/).