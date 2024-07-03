# Modify a table

The `ALTER TABLE` command acts like a toolkit that allows you to change the structure of existing tables. You can add new sections (columns), remove old ones, or change how information is stored [(data types)](data-types-basic.md). This command helps you adapt your database to new needs or improve efficiency.

## Things to Watch Out For

* Data loss: Be careful when modifying tables! Deleting a section (column) or changing its format might erase existing data in that section.

* Slowdowns: Altering large tables or making complex changes can slow down the database, especially during busy times. It might take longer for things to work while the changes are applied.

* Locks: MySQL might temporarily lock the tables you're working on when making changes. This operation means other users can't access or modify that data until the changes are complete, which can cause delays for others.

## Modify table example

After a table has been created, you may need to modify its structure or properties. Percona Server for MySQL provides the `ALTER TABLE` command for making such modifications. You can add, modify, or drop columns, change data types, add constraints, and more using this command.

The following is an example using an `ALTER TABLE` command:

```{.bash data-prompt="mysql>"}
mysql> ALTER TABLE users
ADD COLUMN age INT,
MODIFY COLUMN email VARCHAR(255),
DROP COLUMN username;
```

## Database management

* [Database](database.md)
* [Tables](table.md)
* [Create table](create-table.md)
* [Isolation Levels](isolation-levels.md)
* [Transaction Management](transaction-mgmt.md)
* [Views](views.md)
