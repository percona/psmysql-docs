# Suppress Warning Messages

This feature is intended to provide a general mechanism (using `log_warnings_silence`) to disable certain warning messages to the log file. Currently, it is only implemented for disabling message #1592 warnings. This feature does not influence warnings delivered to a client. Please note that warning code needs to be a string:

```sql
mysql> SET GLOBAL log_warnings_suppress = '1592';
```
The output could be similar to the following:

```text
Query OK, 0 rows affected (0.00 sec)
```

## Version Specific Information

> 
> * Percona Server for MySQL 5.7.10-1: Variable [log_warnings_suppress](https://docs.percona.com/percona-server/8.0/flexibility/log_warnings_suppress.html#log-warnings-suppress) ported from *Percona Server for MySQL* 5.6.


> * Percona Server for MySQL 5.7.11-4: Feature has been removed from *Percona Server for MySQL* 5.7 because MySQL 5.7.11 has implemented a new system variable, [log_statements_unsafe_for_binlog](https://dev.mysql.com/doc/refman/5.7/en/replication-options-binary-log.html#sysvar_log_statements_unsafe_for_binlog), which implements the same effect.

## System Variables

### `innodb_ft_ignore_stopwords`

| Option       | Description                                                                                             |
|--------------|---------------------------------------------------------------------------------------------------------|
| Command-line | Yes                                                                                                     |
| Config file  | Yes                                                                                                     |
| Scope        | Global                                                                                                  |
| Dynamic      | Yes                                                                                                     |
| Data type    | SET                                                                                                     |
| Default      |`(empty string)`                                 |
| Range        | `(empty string)`, `1592` |

It is intended to provide a more general mechanism for disabling warnings than existed previously with variable suppress_log_warning_1592.
When set to the empty string, no warnings are disabled. When set to `1592`, warning #1592 messages (unsafe statement for binary logging) are suppressed.
In the future, the ability to optionally disable additional warnings may also be added.

## Related Reading

> 
> * [MySQL bug 42851](http://bugs.mysql.com/bug.php?id=42851)


> * [MySQL InnoDB replication](http://dev.mysql.com/doc/refman/5.7/en/innodb-and-mysql-replication.html)


> * [InnoDB Startup Options and System Variables](http://dev.mysql.com/doc/refman/5.7/en/innodb-parameters.html)


> * [InnoDB Error Handling](http://dev.mysql.com/doc/refman/5.7/en/innodb-error-handling.html)
