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

```{.bash data-prompt="mysql>"}
mysql> INSTALL PLUGIN clone SONAME 'mysql_clone.so';
```

Review the INFORMATION_SCHEMA.PLUGINS table or run the `SHOW PLUGINS` command to verify the installation. The following is an example of querying the PLUGINS table.

```{.bash data-prompt="mysql>"}
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS FROM INFORMATION_SCHEMA.PLUGINS WHERE PLUGIN_NAME='clone';
```

The result lists the Clone plugin and the status.

## Clone data

The SQL statement used to clone data depends on if the operation is local or remote. The following code is an example of cloning data from a remote server:

```{.bash data-prompt="mysql>"}
mysql> CLONE INSTANCE FROM `root@remote.server:13336` IDENTIFIED BY `user`;
```

Replace the user name, host name, and port number with the settings from the donor server.