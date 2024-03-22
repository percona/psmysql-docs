# Migrate and remove the TokuDB storage engine

Starting with Percona Server for MySQL 8.0.28-19 (2022-05-12), the TokuDB storage engine is no longer supported. For more information, see the [TokuDB Introduction](tokudb-intro.md) and [TokuDB version changes](tokudb-version-changes.md). 

## Migrate to MyRocks

To migrate data use the [mysqldump](https://dev.mysql.com/doc/refman/8.0/en/mysqldump.html) client utility or the tools in the [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) to dump and restore the database.

We recommended migrating to the MyRocks storage engine. Follow these steps to migrate the data:

1. Use mysqldump to backup the TokuDB database into a single file.

2. Create a MyRocks instance with MyRocks tables with no data.

3. Replace the references to TokuDB with MyRocks.

4. Enable the following variable: `rocksdb_bulk_load`. This variable also enables `rocksdb_commit_in_the_middle`.

5. Import the data into the MyRocks database.

6. Go to [Remove the plugins](#remove-the-plugins)

## Migrate to InnoDB

Remove the TokuDB storage engine from Percona Server for MySQL without causing any errors. 

If you need the data in the TokuDB tables, you must alter the tables to another supported storage engine. Do not remove the TokuDB storage engine before you’ve changed your tables to a supported storage engine. 


```{.bash data-prompt="mysql>"}
mysql> ALTER TABLE table-name ENGINE=InnoDB;
```

If you remove the TokuDB storage engine and then find you are missing data, you must reinstall the TokuDB storage engine to access the data. 


## Remove the plugins

To remove the TokuDB storage engine with all installed plugins you can use the
**ps-admin** script:

```{.bash data-prompt="$"}
$ ps-admin --disable-tokudb -uroot -pPassw0rd
```

Another option is to remove the TokuDB storage engine with all installed plugins manually:

```{.bash data-prompt="mysql>"}
mysql> UNINSTALL PLUGIN tokudb;
mysql> UNINSTALL PLUGIN tokudb_file_map;
mysql> UNINSTALL PLUGIN tokudb_fractal_tree_info;
mysql> UNINSTALL PLUGIN tokudb_fractal_tree_block_map;
mysql> UNINSTALL PLUGIN tokudb_trx;
mysql> UNINSTALL PLUGIN tokudb_locks;
mysql> UNINSTALL PLUGIN tokudb_lock_waits;
mysql> UNINSTALL PLUGIN tokudb_background_job_status;
```

After the engine and the plugins are uninstalled, you can remove the TokuDB package by using the apt/yum commands:

```{.bash data-prompt="$"}
$ sudo yum remove Percona-Server-tokudb-80.x86_64
```
or

```{.bash data-prompt="$"}
sudo apt remove percona-server-tokudb-8.0
```

Ensure you’ve removed all TokuDB-specific variables from your configuration file before restarting the server. If variables are in your configuration file, the server won't start and the logs will contain errors or warnings.
