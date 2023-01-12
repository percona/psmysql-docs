# TokuDB installation

!!! important

    Starting with [Percona Server for MySQL 8.0.28-19](../release-notes/Percona-Server-8.0.28-19.md), the TokuDB storage engine is no longer supported. We have removed the storage engine from the installation packages and disabled the storage engine in our binary builds.

    Starting with [Percona Server for MySQL 8.0.26-16](../release-notes/Percona-Server-8.0.26-16.md), the binary builds and packages include but disable the TokuDB storage engine plugins. The tokudb_enabled option and the tokudb_backup_enabled option control the state of the plugins and have a default setting of FALSE. The result of attempting to load the plugins are the plugins fail to initialize and print a deprecation message.

    We recommend [Migrating the data to the MyRocks storage engine](https://docs.percona.com/percona-server/latest/tokudb/removing_tokudb.html#migrate-myrocks). To enable the plugins to migrate to another storage engine, set the tokudb_enabled and tokudb_backup_enabled options to TRUE in your my.cnf file and restart your server instance. Then, you can load the plugins.

    The TokuDB storage engine was declared as deprecated in [Percona Server for MySQL 8.0](../release-notes/Percona-Server-8.0.13-3.md). For more information, see the Percona blog post: [Heads-Up: TokuDB Support Changes and Future Removal from Percona Server for MySQL 8.0](https://www.percona.com/blog/2021/05/21/tokudb-support-changes-and-future-removal-from-percona-server-for-mysql-8-0/).

*Percona Server for MySQL* is compatible with the separately available *TokuDB* storage
engine package. The *TokuDB* engine must be separately downloaded and then
enabled as a plug-in component. This package can be installed alongside with
standard *Percona Server for MySQL* 8.0 releases and does not require any specially
adapted version of *Percona Server for MySQL*.

The *TokuDB* storage engine is a scalable, ACID and MVCC compliant storage
engine that provides indexing-based query improvements, offers online schema
modifications, and reduces replica lag for both hard disk drives and flash
memory. This storage engine is specifically designed for high performance on
write-intensive workloads which is achieved with Fractal Tree indexing. To learn
more about Fractal Tree indexing, you can visit the following [Wikipedia page](https://en.wikipedia.org/wiki/Fractal_tree_index).

!!! warning

    Only the [Percona supplied](https://www.percona.com/downloads/Percona-Server-8.0/LATEST/) *TokuDB* engine should be used with *Percona Server for MySQL* 8.0. A *TokuDB* engine downloaded from other sources is not compatible. *TokuDB* file formats are not the same across *MySQL* variants. Migrating from one variant to any other variant requires a logical data dump and reload.

## Prerequisites

### `libjemalloc` library

*TokuDB* storage engine requires `libjemalloc` library 3.3.0 or
greater. If the version in the distribution repository is lower than
that you can use one from Percona Software Repositories or download it.

If the `libjemalloc` wasn’t installed and enabled before it will be
automatically installed when installing the *TokuDB* storage engine
package by using the **apt`** or **yum** package
manager, but *Percona Server for MySQL* instance should be restarted for
`libjemalloc` to be loaded. This way `libjemalloc` will be loaded
with `LD_PRELOAD`. You can also enable `libjemalloc` by specifying
malloc-lib variable in the `[mysqld_safe]` section of
the `my.cnf` file:

```text
[mysqld_safe]
malloc-lib= /path/to/jemalloc
```

### Transparent huge pages

*TokuDB* won’t be able to start if the transparent huge pages are
enabled. [Transparent huge pages](https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/html/Performance_Tuning_Guide/s-memory-transhuge.html)
is a feature available in the newer kernel versions. You can check if
the Transparent huge pages are enabled with: `cat /sys/kernel/mm/transparent_hugepage/enabled`

If transparent huge pages are enabled and you try to start the TokuDB
engine you’ll get the following message in you `error.log`:

```text
Transparent huge pages are enabled, according to /sys/kernel/mm/redhat_transparent_hugepage/enabled
Transparent huge pages are enabled, according to /sys/kernel/mm/transparent_hugepage/enabled
```

You can [disable](https://access.redhat.com/solutions/46111)
transparent huge pages permanently by passing
`transparent_hugepage=never` to the kernel in your bootloader


!!! note

    For this change to take an effect you must reboot your server.

You can disable the transparent huge pages by running the following
command as root.
    
!!! note

    This setting lasts only until the server is rebooted.

```shell
echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo never > /sys/kernel/mm/transparent_hugepage/defrag
```

## Installation

The *TokuDB* storage engine for *Percona Server for MySQL* is currently
available in our apt and yum repositories.

You can install the *Percona Server for MySQL* with the *TokuDB* engine by using the respective package manager:

For **yum**, use the following command:

```shell
    $ yum install percona-server-tokudb.x86_64
```

For **apt**, use the following command:

```shell
    $ apt install percona-server-tokudb
```

## Enabling the TokuDB Storage Engine

Once the *TokuDB* server package is installed, the following output is shown:

*Percona Server for MySQL* has implemented **ps-admin** to make the enabling the
*TokuDB* storage engine easier. This script will automatically disable
Transparent huge pages, if they’re enabled, and install and enable the
*TokuDB* storage engine with all the required plugins. You need to run
this script as root or with **sudo**. The script should only
be used for local installations and should not be used to install
TokuDB to a remote server. After you run the script
with required parameters:

*Percona Server for MySQL* has implemented `ps_tokudb_admin` script to make the enabling the *TokuDB* storage engine easier. This script will automatically disable Transparent huge pages, if they’re enabled, and install and enable the *TokuDB* storage engine with all the required plugins. You need to run this script as root or with **sudo**. The script should only be used for local installations and should not be used to install TokuDB to a remote server. After you run the script with required parameters:

```shell
$ ps-admin --enable-tokudb -uroot -pPassw0rd
```

Following output will be displayed:

```text
Checking if Percona server is running with jemalloc enabled...
>> Percona server is running with jemalloc enabled.

Checking transparent huge pages status on the system...
>> Transparent huge pages are currently disabled on the system.

Checking if thp-setting=never option is already set in config file...
>> Option thp-setting=never is not set in the config file.
>> (needed only if THP is not disabled permanently on the system)

Checking TokuDB plugin status...
>> TokuDB plugin is not installed.

Adding thp-setting=never option into /etc/mysql/my.cnf
>> Successfuly added thp-setting=never option into /etc/mysql/my.cnf

Installing TokuDB engine...
>> Successfuly installed TokuDB plugin.
```

If the script returns no errors, *TokuDB* storage engine should be successfully enabled on your server. You can check it out by running `SHOW ENGINES;`

## Enabling the TokuDB Storage Engine Manually

If you don’t want to use **ps-admin** you’ll need to manually install
the storage engine ad required plugins.

```sql
INSTALL PLUGIN tokudb SONAME 'ha_tokudb.so';
INSTALL PLUGIN tokudb_file_map SONAME 'ha_tokudb.so';
INSTALL PLUGIN tokudb_fractal_tree_info SONAME 'ha_tokudb.so';
INSTALL PLUGIN tokudb_fractal_tree_block_map SONAME 'ha_tokudb.so';
INSTALL PLUGIN tokudb_trx SONAME 'ha_tokudb.so';
INSTALL PLUGIN tokudb_locks SONAME 'ha_tokudb.so';
INSTALL PLUGIN tokudb_lock_waits SONAME 'ha_tokudb.so';
INSTALL PLUGIN tokudb_background_job_status SONAME 'ha_tokudb.so';
```

After the engine has been installed it should be present in the
engines list. To check if the engine has been correctly installed and
active: `SHOW ENGINES;`

To check if all the *TokuDB* plugins have been installed correctly you should run: `SHOW PLUGINS;`

## TokuDB Version

*TokuDB* storage engine version can be checked with: `SELECT @@tokudb_version;`

## Upgrade

Before upgrading to *Percona Server for MySQL* 8.0, make sure that your system is ready by
running **mysqlcheck**: `mysqlcheck -u root -p --all-databases
--check-upgrade`

!!! warning

    With partitioned tables that use the *TokuDB* or *MyRocks* storage engine, the upgrade only works with native partitioning.

