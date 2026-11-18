> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Modify a table

The `ALTER TABLE` command acts like a toolkit that allows you to change the structure of existing tables. You can add new sections (columns), remove old ones, or change how information is stored [(data types)](https://docs.percona.com/percona-server/9.7/data-types-basic.html). This command helps you adapt your database to new needs or improve efficiency.

## Things to Watch Out For

- Data loss: Be careful when modifying tables! Deleting a section (column) or changing its format might erase existing data in that section.
- Slowdowns: Altering large tables or making complex changes can slow down the database, especially during busy times. It might take longer for things to work while the changes are applied.
- Locks: MySQL might temporarily lock the tables you’re working on when making changes. This operation means other users can’t access or modify that data until the changes are complete, which can cause delays for others.

## Modify table example

After a table has been created, you may need to modify its structure or properties. Percona Server for MySQL provides the `ALTER TABLE` command for making such modifications. You can add, modify, or drop columns, change data types, add constraints, and more using this command.

The following is an example using an `ALTER TABLE` command:

```
ALTER TABLE users
ADD COLUMN age INT,
MODIFY COLUMN city VARCHAR(100),
DROP COLUMN username;
```

## Database management

- [Database](https://docs.percona.com/percona-server/9.7/database.html)
- [Tables](https://docs.percona.com/percona-server/9.7/table.html)
- [Create table](https://docs.percona.com/percona-server/9.7/create-table.html)
- [Isolation Levels](https://docs.percona.com/percona-server/9.7/isolation-levels.html)
- [Transaction Management](https://docs.percona.com/percona-server/9.7/transaction-mgmt.html)
- [Views](https://docs.percona.com/percona-server/9.7/views.html)
