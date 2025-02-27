# Use the Clone plugin

The Clone plugin in the server enables you to create a physical copy of a server instance. This feature simplifies server provisioning and replication setup. Using the Clone plugin, you can quickly copy data from one server instance (donor) to another (recipient).

## Common scenarios

The following are common scenarios for using the Clone plugin:

| **Scenario**                                     | **Description**                                                      |
|--------------------------------------------------|----------------------------------------------------------------------|
| Set up new replicas quickly                      | Without manual data copying                                          |
| Bootstrap new Group Replication members          | Efficiently add new members to the group                             |
| Create physical backups                          | With minimal performance impact                                      |
| Build test environments                          | Mirror production data for accurate testing                          |
| Provision new MySQL server instances             | Quickly set up new servers with existing data                        |
| Perform local cloning                            | Clone data within the same server for testing or backup purposes     |
| Clone encrypted and compressed data              | Support for cloning encrypted and page-compressed data               |

The Clone Plugin significantly reduces the time needed to create full server instance copies compared to traditional backup and restore methods.

## Local clone on the same server

To clone data to a different directory on the same server:

```{.bash data-prompt="mysql>"}
mysql> CLONE LOCAL DATA DIRECTORY = '/path/to/destination/directory';
```

This command creates a full copy of all databases in the source directory.

## Remote cloning to copy data between servers

On the source server, create a user with the necessary privileges:

```{.bash data-prompt="mysql>"}
mysql> CLONECREATE USER clone_user@'%' IDENTIFIED BY 'password';
mysql> GRANT CLONE_ADMIN ON *.* TO clone_user@'%';
```

On the target server, run the clone command:

```{.bash data-prompt="mysql>"}
mysql> CLONE INSTANCE FROM 'clone_user'@'donor_host':3306 
IDENTIFIED BY 'password';
```

The destination server will shut down, replace its data, and restart automatically.

## Monitor clone operations

Check the status of ongoing and completed clone operations:

```{.bash data-prompt="mysql>"}
mysql> SELECT * FROM performance_schema.clone_status;
mysql> SELECT * FROM performance_schema.clone_progress;
```

Additional details are recorded in the server error log.

For more information about the Clone plugin, see:

* [Clone plugin overview](clone-plugin-overview.md)

* [Load the Clone plugin](load-clone-plugin.md)

* [Clone plugin limitations](clone-plugin-limitations.md)