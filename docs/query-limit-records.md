<!--- still tech preview?--->

# Limit the estimation of records in a Query

!!! important

    --8<--- "tech.preview.md:5:5"

This page describes an alternative when running queries against a large number
of table partitions. When a query runs, InnoDB estimates the records in each
partition. This process can result in more pages read and more disk I/O, if the
buffer pool must fetch the pages from disk. This process increases the query
time if there are a large number of partitions.

The addition of two variables makes it possible to override [records_in_range](https://dev.mysql.com/doc/internals/en/records-in-range.html) which
effectively bypasses the process.

!!! warning

    The use of these variables may result in improper index selection by the optimizer.

## `innodb_records_in_range`

| Option         | Description        |
| -------------- | ------------------ |
| Command-line:  | `--innodb-records-in-range` |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type:     | Numeric            |
| Default        | 0                  |

!!! important

    --8<--- "tech.preview.md:5:5"

The variable provides a method to limit the number of records estimated for a
query.

```{.bash data-prompt="mysql>"}
mysql> SET @@GLOBAL.innodb_records_in_range=100;
100
```

### `innodb_force_index_records_in_range`

| Option         | Description        |
| -------------- | ------------------ |
| Command-line:  | `--innodb-force-index-records-in-range` |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type:     | Numeric            |
| Default        | 0                  |

!!! important

    --8<--- "tech.preview.md:5:5"

This variable provides a method to override the records_in_range result when a
FORCE INDEX is used in a query.

```{.bash data-prompt="mysql>"}
mysql> SET @@GLOBAL.innodb_force_index_records_in_range=100;
100
```

## Using the favor_range_scan optimizer switch

!!! important

    --8<--- "tech.preview.md:5:5"

In specific scenarios, the optimizer chooses to scan a table instead of using a range scan. The conditions are the following:

* Table with an extremely large number of rows

* Compound primary keys made of two or more columns

* WHERE clause contains multiple range conditions

The [optimizer_switch](https://dev.mysql.com/doc/refman/8.1/en/switchable-optimizations.html) controls the optimizer behavior. The favor_range_scan switch arbitrarily lowers the cost of a range scan by a factor of 10.

The available values are:

* ON

* OFF (Default)

* DEFAULT

```{.bash data-prompt="mysql>"}
mysql> SET optimizer_switch='favor_range_scan=on';
```
