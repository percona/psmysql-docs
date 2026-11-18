> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Extended SET VAR optimizer hint

Percona Server for MySQL extends the `SET_VAR` introduced in MySQL 9.7 effectively replacing the `SET STATEMENT ... FOR` statement. `SET_VAR` is an optimizer hint that can be applied to session variables.

Percona Server for MySQL 9.7 extends the `SET_VAR` hint to support the following:

- The `OPTIMIZE TABLE` statement
- MyISAM session variables
- Plugin or Storage Engine variables
- InnoDB Session variables
- The `ALTER TABLE` statement
- `CALL stored_proc()` statement
- The `ANALYZE TABLE` statement
- The `CHECK TABLE` statement
- The `LOAD INDEX` statement (used for MyISAM)
- The `CREATE TABLE` statement

Percona Server for MySQL also supports setting the following variables by using `SET_VAR`:
