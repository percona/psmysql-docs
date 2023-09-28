# Migrate and removing the TokuDB storage engine

!!! important

    Starting with [Percona Server for MySQL 8.0.28-19](release-notes/Percona-Server-8.0.28-19.md), the TokuDB storage engine is no longer supported. We have removed the storage engine from the installation packages and disabled the storage engine in our binary builds.

    Starting with [Percona Server for MySQL 8.0.26-16](release-notes/Percona-Server-8.0.26-16.md), the binary builds and packages include but disable the TokuDB storage engine plugins. The tokudb_enabled option and the tokudb_backup_enabled option control the state of the plugins and have a default setting of FALSE. The result of attempting to load the plugins are the plugins fail to initialize and print a deprecation message.

    We recommend [Migrating the data to the MyRocks storage engine](https://docs.percona.com/percona-server/latest/tokudb/removing_tokudb.html#migrate-myrocks). To enable the plugins to migrate to another storage engine, set the tokudb_enabled and tokudb_backup_enabled options to TRUE in your my.cnf file and restart your server instance. Then, you can load the plugins.

    The TokuDB storage engine was declared as deprecated in [Percona Server for MySQL 8.0](release-notes/Percona-Server-8.0.13-3.md). For more information, see the Percona blog post: [Heads-Up: TokuDB Support Changes and Future Removal from Percona Server for MySQL 8.0](https://www.percona.com/blog/2021/05/21/tokudb-support-changes-and-future-removal-from-percona-server-for-mysql-8-0/).

## Migrating the data to MyRocks Storage Engine

To migrate data use the [mysqldump](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html) client utility or the tools in the [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) to dump and restore the database.

We recommended migrating to the MyRocks storage engine. Follow these steps to migrate the data:

1. Use mysqldump to backup the TokuDB database into a single file.

2. Create a MyRocks instance with MyRocks tables with no data.

3. Replace the references to TokuDB with MyRocks.

4. Enable the following variable: rocksdb_bulk_load. This variable also enables rocksdb_commit_in_the_middle.

5. Import the data into the MyRocks database.

Follow the Removing the plugins steps.

## Migrating from TokuDB to InnoDB

In case you want remove the TokuDB storage engine from *Percona Server for MySQL* without
causing any errors following is the recommended procedure:

## Change the tables from TokuDB to InnoDB

If you still need the data in the TokuDB tables you must alter the tables
to other supported storage engine i.e., *InnoDB*: `ALTER TABLE City
ENGINE=InnoDB;`

!!! note

    Do not remove the TokuDB storage engine before you’ve changed your tables to the other supported storage engine. Otherwise, you will not be able to access that data without reinstalling the TokuDB storage engine.

## Removing the plugins

To remove the *TokuDB* storage engine with all installed plugins you can use the
**ps-admin** script:

```shell
$ ps-admin --disable-tokudb -uroot -pPassw0rd
```

Script output should look like this:

Another option is to manually remove the *TokuDB* storage engine with all installed plugins:

```sql
msql> UNINSTALL PLUGIN tokudb;
msql> UNINSTALL PLUGIN tokudb_file_map;
msql> UNINSTALL PLUGIN tokudb_fractal_tree_info;
msql> UNINSTALL PLUGIN tokudb_fractal_tree_block_map;
msql> UNINSTALL PLUGIN tokudb_trx;
msql> UNINSTALL PLUGIN tokudb_locks;
msql> UNINSTALL PLUGIN tokudb_lock_waits;
msql> UNINSTALL PLUGIN tokudb_background_job_status;
```

After the engine and the plugins have been uninstalled you can remove the TokuDB package by using the apt/yum commands:

```shell
[root@centos ~]# yum remove Percona-Server-tokudb-80.x86_64
```

or `apt remove percona-server-tokudb-8.0`

!!! note

    Make sure you’ve removed all the TokuDB specific variables from your configuration file (`my.cnf`) before you restart the server, otherwise server could show errors or warnings and won’t be able to start.
