
Percona Server for MySQL 8.0 comes with the TokuDB and MyRocks storage engine and can be installed as a plugin. For information on installing and configuring MyRocks, refer to the [Percona MyRocks Installation Guide](install-myrocks.md).

For information on installing and configuring TokuDB, refer to the [TokuDB Installation Guide](tokudb-installation.md).

From [Percona Server for MySQL 8.0.28-19](release-notes/Percona-Server-8.0.28-19.md), the TokuDB storage engine is no longer supported. We have removed the storage engine from the installation packages and disabled the storage engine in our binary builds.

From [Percona Server for MySQL 8.0.26-16](release-notes/Percona-Server-8.0.26-16.md), the binary builds and packages include but disable the TokuDB storage engine plugins. The tokudb_enabled option and the tokudb_backup_enabled option control the state of the plugins and have a default setting of FALSE. The result of attempting to load the plugins are the plugins fail to initialize and print a deprecation message.

We recommend [Migrating the data to the MyRocks storage engine](https://docs.percona.com/percona-server/latest/tokudb/removing_tokudb.html#migrate-myrocks). To enable the plugins to migrate to another storage engine, set the tokudb_enabled and tokudb_backup_enabled options to TRUE in your my.cnf file and restart your server instance. Then, you can load the plugins.

The TokuDB storage engine was declared as deprecated in [Percona Server for MySQL 8.0](release-notes/Percona-Server-8.0.13-3.md). For more information, see the Percona blog post: [Heads-Up: TokuDB Support Changes and Future Removal from Percona Server for MySQL 8.0](https://www.percona.com/blog/2021/05/21/tokudb-support-changes-and-future-removal-from-percona-server-for-mysql-8-0/).
