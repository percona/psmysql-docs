# TokuDB file management

!!! important

    Starting with [Percona Server for MySQL 8.0.28-19](release-notes/Percona-Server-8.0.28-19.md), the TokuDB storage engine is no longer supported. We have removed the storage engine from the installation packages and disabled the storage engine in our binary builds.

    Starting with [Percona Server for MySQL 8.0.26-16](release-notes/Percona-Server-8.0.26-16.md), the binary builds and packages include but disable the TokuDB storage engine plugins. The tokudb_enabled option and the tokudb_backup_enabled option control the state of the plugins and have a default setting of FALSE. The result of attempting to load the plugins are the plugins fail to initialize and print a deprecation message.

    We recommend [Migrating the data to the MyRocks storage engine](https://docs.percona.com/percona-server/latest/tokudb/removing_tokudb.html#migrate-myrocks). To enable the plugins to migrate to another storage engine, set the tokudb_enabled and tokudb_backup_enabled options to TRUE in your my.cnf file and restart your server instance. Then, you can load the plugins.

    The TokuDB storage engine was declared as deprecated in [Percona Server for MySQL 8.0](release-notes/Percona-Server-8.0.13-3.md). For more information, see the Percona blog post: [Heads-Up: TokuDB Support Changes and Future Removal from Percona Server for MySQL 8.0](https://www.percona.com/blog/2021/05/21/tokudb-support-changes-and-future-removal-from-percona-server-for-mysql-8-0/).
    

As mentioned in the TokuDB files and file types *Percona FT* is particular when validating its data set. If a file goes missing or can’t be accessed, or seems to contain some nonsensical data, it will assert, abort or fail to start. It does this not to annoy you, but to try to protect you from doing any further damage to your data.

This document contains examples of common file maintenance operations and
instructions on how to safely execute these operations.

The `tokudb_dir_per_db` option addressed two shortcomings the [renaming of data files](tokudb-file-management.md#improved-table-renaming-functionality) on table/index rename, and the ability
to [group data files together](tokudb-file-management.md#improved-directory-layout-functionality)
within a directory that represents a single database. This feature is enabled
by default.

The [tokudb_dir_cmd](tokudb-file-management.md#tokudbdircmd) variable can be used to edit the contents of the TokuDB/PerconaFT directory map.

## Moving TokuDB data files to a location outside of the default MySQL datadir

*TokuDB* uses the location specified by the [tokudb_data_dir](tokudb-variables.md#tokudbdatadir)
variable for all of its data files. If the tokudb_data_dir variable
is not explicitly set, *TokuDB* will use the location specified by the servers
datadir for these files.

The *TokuDB* data files are protected from concurrent process access by the
`__tokudb_lock_dont_delete_me_data` file that is located in the same
directory as the *TokuDB* data files.

*TokuDB* data files may be moved to other locations with symlinks left behind
in their place. If those symlinks refer to files on other physical data
volumes, the [tokudb_fs_reserve_percent](tokudb-variables.md#tokudbfsreservepercent) monitor will not traverse
the symlink and monitor the real location for adequate space in the file
system.

To safely move your TokuDB data files:

1. Shut the server down cleanly.

2. Change the `tokudb_data_dir` in your `my.cnf` configuration file to the location where you wish to store your *TokuDB* data files.

3. Create your new target directory.

4. Move your `\*.tokudb` files and your `__tokudb_lock_dont_delete_me_data` from the current location to the new location.

5. Restart your server.

## Moving TokuDB temporary files to a location outside of the default MySQL datadir

*TokuDB* will use the location specified by the [tokudb_tmp_dir](tokudb-variables.md#tokudbtmpdir)
variable for all of its temporary files. If tokudb_tmp_dir variable
is not explicitly set, *TokuDB* will use the location specified by the
tokudb_data_dir variable. If the tokudb_data_dir
variable is also not explicitly set, *TokuDB* will use the location specified
by the servers datadir for these files.

*TokuDB* temporary files are protected from concurrent process access by the
`__tokudb_lock_dont_delete_me_temp` file that is located in the same
directory as the *TokuDB* temporary files.

If you locate your *TokuDB* temporary files on a physical volume that is
different from where your *TokuDB* data files or recovery log files are
located, the tokudb_fs_reserve_percent monitor will not monitor their location for adequate space in the file system.

To safely move your *TokuDB* temporary files:

1. Shut the server down cleanly. A clean shutdown will ensure that there are no
temporary files that need to be relocated.

2. Change the tokudb_tmp_dir variable in your `my.cnf`
configuration file to the location where you wish to store your new *TokuDB* temporary files.

3. Create your new target directory.

4. Move your `__tokudb_lock_dont_delete_me_temp` file from the current
location to the new location.

5. Restart your server.

## Moving TokuDB recovery log files to a location outside of the default MySQL datadir

TokuDB will use the location specified by the tokudb_log_dir
variable for all of its recovery log files. If the tokudb_log_dir
variable is not explicitly set, TokuDB will use the location specified by the
servers source/glossary.rst\`datadir\` for these files.

The *TokuDB* recovery log files are protected from concurrent process access by
the `__tokudb_lock_dont_delete_me_logs` file that is located in the same
directory as the *TokuDB* recovery log files.

TokuDB recovery log files may be moved to another location with symlinks left
behind in place of the tokudb_log_dir. If that symlink refers to a directory on another physical data volume, the
tokudb_fs_reserve_percent monitor will not traverse the symlink and
monitor the real location for adequate space in the file system.

To safely move your *TokuDB* recovery log files:

1. Shut the server down cleanly.

2. Change the tokudb_log_dir in your `my.cnf` configuration
file to the location where you wish to store your TokuDB recovery log files.

3. Create your new target directory.

4. Move your `log\*.tokulog\*` files and your
`__tokudb_lock_dont_delete_me_logs` file from the current location to the
new location.

5. Restart your server.

## Improved table renaming functionality

When you rename a *TokuDB* table via SQL, the data files on disk keep their
original names and only the mapping in the *Percona FT* directory file is
changed to map the new dictionary name to the original internal file names.
This makes it difficult to quickly match database/table/index names to their
actual files on disk, requiring you to use the
refTOKUDB_FILE_MAP table to cross reference.

The [tokudb_dir_per_db](tokudb-variables.md#tokudbdirperdb) variable is implemented to address this issue.

When [tokudb_dir_per_db](tokudb-variables.md#tokudbdirperdb)is enabled (`ON` by default), this is no
longer the case. When you rename a table, the mapping in the *Percona FT*
directory file will be updated and the files will be renamed on disk to reflect
the new table name.

## Improved directory layout functionality

Many users have had issues with managing the huge volume of individual files
that *TokuDB* and *Percona FT* use. The [tokudb_dir_per_db](tokudb-variables.md#tokudbdirperdb) variable
addresses this issue.

When [tokudb_dir_per_db](tokudb-variables.md#tokudbdirperdb) variable is enabled (`ON` by default),
all new tables and indices will be placed within their corresponding database
directory within the `tokudb_data_dir` or server datadir.

If you have tokudb_data_dir variable set to something other than
the server datadir, *TokuDB* will create a directory matching the name
of the database, but upon dropping of the database, this directory will remain
behind.

Existing table files will not be automatically relocated to their corresponding
database directory.

You can easily move a tables data files into the new scheme and proper database
directory with a few steps:

```sql
mysql> SET GLOBAL tokudb_dir_per_db=true;
mysql> RENAME TABLE <table> TO <tmp_table>;
mysql> RENAME TABLE <tmp_table> TO <table>;
```

!!! note

    Two renames are needed because *MySQL* doesn’t allow you to rename a table to itself. The first rename, renames the table to the temporary name and moves the table files into the owning database directory. The second rename sets the table name back to the original name. Tables can also be renamed/moved across databases and will be placed correctly into the corresponding database directory.

!!! warning

    You must be careful with renaming tables in case you have used any tricks to create symlinks of the database directories on different storage volumes, the move is not a simple directory move on the same volume but a physical copy across volumes. This can take quite some time and prevent access to the table being moved during the copy.

### System Variables

### `tokudb_dir_cmd`

| Option       | Description |
|--------------|-------------|
| Command-line | Yes         |
| Config file  | Yes         |
| Scope        | Global      |
| Dynamic      | Yes         |
| Data type    | String      |

This variable is used to send commands to edit *TokuDB* directory files.

!!! warning

    Use this variable only if you know what you are doing otherwise it **WILL** lead to data loss.

### Status Variables

### `tokudb_dir_cmd_last_error`

| Option    | Description |
|-----------|-------------|
| Scope     | Global      |
| Data type | Numeric     |

This variable contains the error number of the last executed command by using
the tokudb_dir_cmd variable.

### `tokudb_dir_cmd_last_error_string`

| Option    | Description |
|-----------|-------------|
| Scope     | Global      |
| Data type | Numeric     |


This variable contains the error string of the last executed command by using
the tokudb_dir_cmd variable.