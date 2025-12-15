# MySQL Clone plugin

The MySQL Clone plugin lets you clone data from either a local server or from a remote server. The plugin creates a physical snapshot of the data stored in InnoDB, which includes schemas, tables, tablespaces, and data dictionary metadata. The cloned data is a functional data directory and can be used for provisioning a server .

The following table lists the cloning operation types:

| Cloning operation type | Description |
|---|---|
| Local | Clones the data from the server where the operation is initiated to either a directory on the same server or a server node. |
| Remote | Clones the data from the donor to the joiner over the network. |

When replicating a large number of transactions, the Clone plugin may be a more efficient solution. 

## Install the Clone plugin

The Clone plugin must be installed on both the donor and the joiner servers at either server startup or at runtime. To install the plugin at runtime, run the following command:

```sql
INSTALL PLUGIN clone SONAME 'mysql_clone.so';
```

Review the INFORMATION_SCHEMA.PLUGINS table or run the `SHOW PLUGINS` command to verify the installation. The following is an example of querying the PLUGINS table.

```sql
SELECT PLUGIN_NAME, PLUGIN_STATUS FROM INFORMATION_SCHEMA.PLUGINS WHERE PLUGIN_NAME='clone';
```

The result lists the Clone plugin and the status.

## Clone data

The SQL statement used to clone data depends on if the operation is local or remote. The following code is an example of cloning data from a remote server:

```sql
CLONE INSTANCE FROM `root@remote.server:13336` IDENTIFIED BY `user`;
```

Replace the user name, host name, and port number with the settings from the donor server.

## Limitations

The MySQL 8.4 clone plugin enforces several functional and scope limitations that define which instances administrators clone and which data or metadata a clone operation includes.

## Version and instance limits

* The clone plugin only supports cloning within the same MySQL server series, so administrators clone between patch releases such as 8.4.1 and 8.4.13, but not between different major series such as 8.0 and 8.4.

* Each clone operation targets only one MySQL instance, and a single operation never clones multiple instances at once.

## Network and protocol restrictions

* The clone plugin uses the classic MySQL protocol, so the X Protocol port defined by `mysqlx_port` does not serve as the donor port in remote cloning operations with `CLONE INSTANCE` .

* The donor MySQL server instance does not accept clone connections that pass through MySQL Router, so administrators connect directly to the donor.

## Configuration and logs excluded

* The clone plugin preserves the configuration of the recipient server instance, so a clone operation does not copy the donor server configuration or persisted system variable settings.

* The plugin does not copy binary logs, so the recipient does not receive the donor’s binary log files as part of the clone .

## Storage engine behavior

* The clone plugin copies only data stored in the InnoDB storage engine and excludes data that other storage engines store.

* The plugin creates `MyISAM` and `CSV` tables on the recipient as empty tables, even when those tables reside in special schemas such as the `sys` schema .

## Local cloning and tablespaces

* During local cloning, the clone plugin does not support general tablespaces that use an absolute path, because cloning those tablespaces would create a conflicting file that uses the same absolute path on the destination host.
