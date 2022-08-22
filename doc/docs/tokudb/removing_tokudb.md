# Removing TokuDB storage engine

In case you want remove the TokuDB storage engine from *Percona Server for MySQL* without causing any errors, the following is the recommended procedure:

## Change the tables from TokuDB to InnoDB

If you still need the data in the TokuDB tables you must alter the tables to another supported storage engine, i.e., InnoDB:

```sql
mysql> ALTER TABLE City ENGINE=InnoDB;
```

!!! note

    Removing the TokuDB storage engine before you have changed your tables to another supported storage engine closes access to that data. You must re-install the TokuDB storage engine to regain access.

## Removing the plugins

One option is to remove the TokuDB storage engine with all installed plugins by running the `ps-admin` script:

```shell
ps-admin --disable-tokudb -uroot -pPassw0rd
```

The script output should look like this:

```text
Checking if Percona server is running with jemalloc enabled...
>> Percona server is running with jemalloc enabled.

Checking transparent huge pages status on the system...
>> Transparent huge pages are currently disabled on the system.

Checking if thp-setting=never option is already set in config file...
>> Option thp-setting=never is set in the config file.

Checking TokuDB plugin status...
>> TokuDB plugin is installed.

Removing thp-setting=never option from /etc/mysql/my.cnf
>> Successfully removed thp-setting=never option from /etc/mysql/my.cnf

Uninstalling TokuDB plugin...
>> Successfully uninstalled TokuDB plugin.
```

!!! note

    The ps-admin removal may not restore the Transparent Huge Pages (THP) to the original operating system default state. You may have the following result:

```shell
$ cat /sys/kernel/mm/transparent_hugepage/enabled
```

The output could be the following:

```text
always madvise [never]
```

On many operating systems, the default state is `[always]`. To enable transparent huge pages, run the following:

```shell
echo always > /sys/kernel/mm/transparent_hugepage/enabled
```

Another option is to manually remove the TokuDB storage engine with all installed plugins:

```sql
UNINSTALL PLUGIN tokudb;
UNINSTALL PLUGIN tokudb_file_map;
UNINSTALL PLUGIN tokudb_fractal_tree_info;
UNINSTALL PLUGIN tokudb_fractal_tree_block_map;
UNINSTALL PLUGIN tokudb_trx;
UNINSTALL PLUGIN tokudb_locks;
UNINSTALL PLUGIN tokudb_lock_waits;
UNINSTALL PLUGIN tokudb_background_job_status;
```

After the engine and the plugins have been uninstalled you can remove the TokuDB package by using the apt/yum commands:

```shell
[root@centos ~]# yum remove Percona-Server-tokudb-57.x86_64
```

or

```shell
root@wheezy:~# apt remove percona-server-tokudb-5.7
```

!!! note

    Make sure you’ve removed all the TokuDB specific variables from your configuration file (`my.cnf`) before you restart the server, otherwise server could show errors or warnings and will not start.
