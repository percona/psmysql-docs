# Expanded Program Option Modifiers

MySQL has the concept of [options modifiers](http://dev.mysql.com/doc/refman/5.7/en/option-modifiers.html) which is a simple way to modify either the way that MySQL interprets an option or the way the option behaves. Option modifiers are used by simply pre-pending the name of the modifier and a dash “-” before the actual configuration option name. For example specifying –maximum-query_cache_size=4M on the mysqld command line or specifying maximum-query_cache_size=4M in the `my.cnf` will prevent any client from setting the query_cache_size value larger than 4MB.

Currently MySQL supports five existing option modifiers:

    text
    * disable [disable-<option_name>] disables or ignores option_name.


    * enable [enable-<option_name>] enables option_name.


    * loose [loose-<option_name>] - mysqld will not exit with an error if it does not recognize option_name, but instead it will issue only a warning.


    * maximum [maximum-<option_name>=<value>] indicates that a client can not set the value of option_name greater than the limit specified. If the client does attempt to set the value of option_name greater than the limit, the option_name will simply be set to the defined limit. This option modifier does not work for non-numeric system variables.


    * skip [skip-<option_name>] skips or ignores option_name.

In order to offer more control over option visibility, access and range limits, the following new option modifiers have been added by *Percona Server for MySQL*:

    text
    * minimum [minimum-<option_name>=<value>] indicates that clients can not set the value of option_name to less than the limit specified. If the client does attempt to set the value of option_name lesser than the limit, the option_name will simply be set to the defined limit. This option modifier does not work for non-numeric system variables.


    * hidden [hidden-<option_name>=<TRUE/FALSE>] indicates that clients can not see or modify the value of option_name.


    * readonly [readonly-<option_name>=<TRUE/FALSE>] indicates that clients can see the value of option_name but can not modify the value.

## Combining the options

Some of the option modifiers may be used together in the same option specification, example:

```text
--skip-loose-<option_name>
--loose-readonly-<option_name>=<T/F>
--readonly-<option_name>=<T/F>
--hidden-<option_name>=<T/F>
```

## Version Specific Information

> 
> * Percona Server for MySQL 5.7.10-1: Feature ported from *Percona Server for MySQL* 5.6

## Examples

Adding the following option to the `my.cnf` will set the minimum limit on query_cache_size

```text
minimum-query_cache_size = 4M
```

Trying to set up bigger value will work correctly, but if we try to set it up with smaller than the limit, defined minimum limit will be used and warning (1292) will be issued:

Initial query_cache_size size:

```sql
mysql> show variables like 'query_cache_size';
```

The output should be similar to the following:

```text
+------------------+---------+
| Variable_name    | Value   |
+------------------+---------+
| query_cache_size | 8388608 |
+------------------+---------+
1 row in set (0.00 sec)
```

Setting up bigger value:

```sql
mysql> set global query_cache_size=16777216;
```

The output should be similar to the following:

```text

Query OK, 0 rows affected (0.00 sec)
```
```sql
mysql> show variables like 'query_cache_size';
```

The output should be similar to the following:

```text
+------------------+----------+
| Variable_name    | Value    |
+------------------+----------+
| query_cache_size | 16777216 |
+------------------+----------+
1 row in set (0.00 sec)
```

Setting up smaller value:

```sql
mysql> set global query_cache_size=1048576;
```

The output should be similar to the following:

```text
Query OK, 0 rows affected, 1 warning (0.00 sec)
```

```sql
mysql> show warnings;
```

The output should be similar to the following:

```text
+---------+------+-------------------------------------------------------+
| Level   | Code | Message                                               |
+---------+------+-------------------------------------------------------+
| Warning | 1292 | Truncated incorrect query_cache_size value: '1048576' |
+---------+------+-------------------------------------------------------+
1 row in set (0.00 sec)

```sql
mysql> show variables like 'query_cache_size';
```

The output should be similar to the following:

```text
+------------------+---------+
| Variable_name    | Value   |
+------------------+---------+
| query_cache_size | 4194304 |
+------------------+---------+
1 row in set (0.00 sec)
```

Adding following option to `my.cnf` will make query_cache_size hidden.

```text
hidden-query_cache_size=1
```

```sql
mysql> show variables like 'query_cache%';
```

The output should be similar to the following:

```text
+------------------------------+---------+
| Variable_name                | Value   |
+------------------------------+---------+
| query_cache_limit            | 1048576 |
| query_cache_min_res_unit     | 4096    |
| query_cache_strip_comments   | OFF     |
| query_cache_type             | ON      |
| query_cache_wlock_invalidate | OFF     |
+------------------------------+---------+
5 rows in set (0.00 sec)
```

Adding following option to `my.cnf` will make query_cache_size read-only

```text
readonly-query_cache_size=1
```

Trying to change the variable value will result in error:

```sql
mysql> show variables like 'query_cache%';
```

The output should be similar to the following:

```text
+------------------------------+---------+
| Variable_name                | Value   |
+------------------------------+---------+
| query_cache_limit            | 1048576 |
| query_cache_min_res_unit     | 4096    |
| query_cache_size             | 8388608 |
| query_cache_strip_comments   | OFF     |
| query_cache_type             | ON      |
| query_cache_wlock_invalidate | OFF     |
+------------------------------+---------+
6 rows in set (0.00 sec)
```

```sql
mysql> set global query_cache_size=16777216;
```

The output should be similar to the following:

```text
ERROR 1238 (HY000): Variable 'query_cache_size' is a read only variable
```
