# Introduction to Databases and SQL

## Introduction to databases

A database in the server is a structured collection of data. It helps store, organize, and manage various types of information like customer details, product inventories, financial records, and more. Using a database allows you to store data in an organized manner, making it easy to retrieve, update, and manipulate as needed.

### Advantages

Using a database in servers has several benefits. The table below lists these advantages:

| Advantages         | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| **Efficient Storage**     | Databases store data in an organized way, making it easy to manage large volumes of information.|
| **Quick Retrieval**       | You can quickly find and retrieve specific data using SQL queries.    |
| **Data Integrity**        | Databases ensure data accuracy and consistency through constraints and relationships.|
| **Scalability**           | Databases can handle growing amounts of data and users efficiently.   |
| **Security**              | Databases provide robust security features to protect sensitive data. |

### Disadvantages

While databases offer many advantages, there are also some drawbacks to consider. The table below outlines these disadvantages:

| Disadvantages       | Description                                                                       |
|---------------------|-----------------------------------------------------------------------------------|
| **Complex Setup**         | Setting up and configuring a database can be complex and time-consuming.       |
| **Maintenance**           | Databases require regular maintenance and updates to function optimally.        |
| **Resource Intensive**    | Databases can consume significant server resources, impacting performance.     |
| **Backup and Recovery**   | Proper backup and recovery processes are necessary to prevent data loss.       |
| **Cost**                  | Licensing and operational costs for databases can be high, especially for large-scale deployments. |

## Permissions required

To create a database on a server, a user must have the `CREATE` privilege. This privilege allows the user to create new databases and tables within those databases.

## Using SQL Commands with a database

### Create a database

You use the `CREATE DATABASE` command to create a new database in the server. This command tells the server to create a new database with the specified name. For example, to create a database named `my_database`, you execute the following command:

```{.bash data-prompt="mysql>"}
mysql> CREATE DATABASE my_database;
```

This command creates a new, empty database called `my_database`. You can then start adding tables and data to this database.

### Select a database

After creating a database, you need to select it to start working with it. Use the `USE` command to specify which database you want to use for your SQL statements. For example, to select the `my_database` database, you execute the following command:

```{.bash data-prompt="mysql>"}
mysql> USE my_database;
```

This command tells the server to use `my_database` for all subsequent SQL commands. Now, any SQL operations you perform will apply to `my_database`.

## Database management

* [Modify Tables](modify-tables.md)
* [Isolation Levels](isolation-levels.md)
* [Transaction Management](transaction-mgmt.md)
* [Views](views.md)