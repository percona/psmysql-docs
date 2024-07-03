# Introduction to database tables

A database table is a collection of data organized into rows and columns. Each table consists of records (rows) and fields (columns). Tables help organize and manage data efficiently.

### Advantages

| Advantages  | Description  |
|-------------|--------------|
| **Organized Data** | Tables allow you to organize data into rows and columns, making it easy to understand and manage. |
| **Efficient Queries** | You can use SQL queries to quickly search, filter, and retrieve data from tables. |
| **Data Integrity** | Tables support constraints like primary keys and foreign keys, ensuring data integrity and consistency. |
| **Scalability** | You can add or modify tables as your data grows, making it easy to scale your database. |
| **Relational Management** | Tables allow you to create relationships between different sets of data, making it easier to manage complex datasets. |

### Disadvantages

| Disadvantages  | Description  |
|----------------|--------------|
| **Complexity** | Designing and maintaining tables, especially with relationships, can become complex and time-consuming. |
| **Performance Issues** | Large tables with many rows can lead to performance issues, requiring optimization and indexing. |
| **Storage Overhead** | Tables with many columns or large data types can consume significant storage space. |
| **Maintenance** | Regular maintenance tasks, such as backups and indexing, are necessary to ensure optimal performance and data integrity. |
| **Learning Curve** | Beginners may find it challenging to learn SQL and understand how to design and manage tables effectively. |

## Permissions required

To create a table in a database, you need appropriate permissions granted to your database user account. These permissions are typically managed by the database administrator (DBA) or system administrator. Database permissions control what actions a user can perform on a database. In the context of creating a table, the user needs specific permissions related to database management.

| Permission   | Description |
|--------------|-------------|
| CREATE TABLE | The most fundamental permission required to create a table is the CREATE TABLE permission. This permission allows the user to create new tables within the database. |
| CREATE       | In addition to CREATE TABLE, the user might also need the more general CREATE permission. This permission grants the ability to create other database objects besides tables, such as indexes, views, or stored procedures. |
| ALTER        | Depending on the database configuration, the user might also need the ALTER permission. This permission allows the user to modify the structure of existing tables, such as adding or removing columns. |


## Create a table

To create a table, use the `CREATE TABLE` command. Follow it with the table name and define the columns and their data types. For example, to create a table named `customers` with columns for `id`, `name`, and `email`, use this command:

```mysql
CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);
```

## Database management

* [Database](database.md)
* [Create table](create-table.md)
* [Isolation Levels](isolation-levels.md)
* [Transaction Management](transaction-mgmt.md)
* [Views](views.md)