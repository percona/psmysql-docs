# Create a table

Creating a table is essential to organizing and storing your data effectively when working with a database. Here's a step-by-step guide on how to create a table in such a database:

## Permissions Required

To create a table in a database, you need appropriate permissions. Typically, you'll need the `CREATE TABLE` privilege, which allows you to create new tables within a database. This privilege is usually granted to database users by database administrators or through predefined user roles. If you do not have the necessary permissions, you'll need to contact your database administrator to grant them.

## Define the table structure

Now, define the structure of your table by specifying its columns along with their data types and any additional properties. Each column represents a different attribute of your data.

Here's the syntax for creating a table:

```text
CREATE TABLE table_name (
    column1_name data_type constraints,
    column2_name data_type constraints,
    ...
);
```

Replace `table_name` with the desired name for your table. For each column, provide a name, data type, and constraints such as `NOT NULL`, `PRIMARY KEY`, `AUTO_INCREMENT`.

## Create the table

Execute the `CREATE TABLE` command to create the table in the database. For example, to create a table named `employees` with columns for `id`, `name`, and `salary`, you would run the following SQL command:

```{.bash data-prompt="mysql>"}
CREATE TABLE employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    salary DECIMAL(10, 2)
);
```

This command creates a table named `employees` with three columns: `id`, `name`, and `salary`. The `id` column is an integer type and serves as the primary key with auto-increment functionality. The `name` column is a variable-length string, and the `salary` column is a decimal number with a precision of 10 digits and a scale of 2.

## Verify Table Creation

After executing the `CREATE TABLE` command, verify that the table has been successfully created. You can use various SQL commands such as `SHOW TABLES` or `DESCRIBE table_name` to check the existence and structure of the newly created table.

```{.bash data-prompt="mysql>"}
mysql> SHOW TABLES;
mysql> DESCRIBE employees;
```

## Database management

* [Database](database.md)
* [Tables](table.md)
* [Isolation Levels](isolation-levels.md)
* [Transaction Management](transaction-mgmt.md)
* [Views](views.md)