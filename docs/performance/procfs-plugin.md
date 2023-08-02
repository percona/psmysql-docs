# The ProcFS plugin

{% include '..//snippets/tech-preview/_tech-preview-feature.md'%}

Implemented in [Percona Server for MySQL 8.0.25-15](../release-notes/Percona-Server-8.0.25-15.md#id1), the ProcFS plugin provides access to the Linux performance counters by running SQL queries against a Percona Server for MySQL 8.0.

You may be unable to capture operating system metrics in certain environments, such as Cloud installations or MySQL-as-a-Service installations. These metrics are essential for complete system performance monitoring.

The plugin does the following:

* Reads selected files from the `/proc` file system and the `/sys` file system.

* Populates the file names and their content as rows in the INFORMATION_SCHEMA.PROCFS view.

The system variable [procfs_files_spec](#procfs_files_spec) provides access to the `/proc` and the `/sys` files and directories. This variable cannot be changed at run time, preventing a compromised account from giving itself greater access to those file systems.

## Install the PLUGIN manually

We recommend installing the plugin as part of the package. If needed, you can install this plugin manually. Copy the `procfs.so` file to the mysql plugin installation directory and execute the following command:

```sql
INSTALL PLUGIN procfs SONAME 'procfs.so';
```

## Access privileges required

Only users with the `ACCESS_PROCFS` dynamic privilege can access the `INFORMATION_SCHEMA.PROCFS` view. During the plugin startup, this dynamic privilege is registered with the server.

After the plugin installation, grant a user access to the INFORMATION_SCHEMA.PROCFS view by executing the following command:

```sql
GRANT ACCESS_PROCFS ON *.* TO 'user'@'host';
```

!!! important

    An SELinux policy or an AppArmor profile may prevent access to file locations needed by the ProcFS plugin, such as the '/proc/sys/fs/file-nr' directory or any sub-directories or files under '/proc/irq/'. Either edit the policy or profile to ensure that the plugin has the necessary access. If the policy and profile do not allow access, the plugin may may have unexpected behavior.

    For more information, see [Working with SELinux](../security/selinux.md#selinux) and [Working with AppArmor](../security/apparmor.md#enable-apparmor).

## Using the ProcFS plugin

Authorized users can obtain information from individual files by specifying the exact file name within a WHERE clause. Files that are not included are ignored and considered not to exist.

All files that match the [procfs_files_spec](#procfsfilesspec) are opened, read, stored in memory, and, finally, returned to the client. It is critical to add a WHERE clause to return only specific files to limit the impact of the plugin on the server’s performance. A failure to use a WHERE clause can lead to lengthy query response times, high load, and high memory usage on the server. The WHERE clause can contain either an equality operator, the LIKE operator, or the IN operator. The LIKE operator limits file globbing. You can write file access patterns in the [glob(7) style](https://man7.org/linux/man-pages/man7/glob.7.html), such as `/sys/block/sd[a-z]/stat;/proc/version\*`

The following example returns the `proc/version`:

```sql
SELECT * FROM INFORMATION_SCHEMA.PROCFS WHERE FILE = '/proc/version';
```

## Tables

### PROCFS

The schema definition of the INFORMATION_SCHEMA.PROCFS view is:

```sql
CREATE TEMPORARY TABLE `PROCFS` (
`FILE` varchar(1024) NOT NULL DEFAULT '',
`CONTENTS` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

Status variables provide the basic metrics:

| Name                     | Description                                    |
| ------------------------ | ---------------------------------------------- | 
| procfs_access_violations | The number of attempted queries by users without the ACCESS_PROCFS privilege.|
| procfs_queries           | The number of queries made against the procfs view. |
| procfs_files_read        | The number of files read to provide content    |
| procfs_bytes_read        | The number of bytes read to provide content    |

## Variable

### procfs_files_spec

| Option         | Description        |
| -------------- | ------------------ |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Read, Write, or Read-Only:     | Read-Only            |

The variable has been implemented in Percona Server for MySQL 8.0.25-14. 
The default value for `procfs_files_spec` is: /proc/cpuinfo;/proc/irq//;/proc/loadavg/proc/net/dev;/proc/net/sockstat;/proc/net/sockstat_rhe4;/proc/net/tcpstat;/proc/self/net/netstat;/proc/self/stat;/proc/self/io;/proc/self/numa_maps/proc/softirqs;/proc/spl/kstat/zfs/arcstats;/proc/stat;/proc/sys/fs/file-nr;/proc/version;/proc/vmstat

Enables access to the `/proc` and `/sys` directories and files. This variable is global, read only, and is set by using either the mysqld command line or by editing `my.cnf`.

## Limitations

The following limitations are:

* Only first 60k of /proc/ /sys/ files are returned

* The file name size is limited to 1k

* The plugin cannot read files if path does not start from /proc or /sys

* Complex WHERE conditions may force the plugin to read all configured files.

## Uninstall plugin

The following statement removes the procfs plugin.

```sql
UNINSTALL PLUGIN procfs;
```
