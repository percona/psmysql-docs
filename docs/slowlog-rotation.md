<!-- still tech preview in Innovation release? -->

# Slow query log rotation and expiration

!!! important

    --8<--- "tech.preview.md:5:5"

Percona has implemented two new variables, `max_slowlog_size` and `max_slowlog_files` to provide users with ability to control the slow query log disk usage. These variables have the same behavior as the [max_binlog_size variable] and the [max_binlog_files variable] used for controlling the binary log.


## `max_slowlog_size`

|    Option    |  Description   |
|--------------|----------------|
| Command-line |      Yes       |
| Config file  |      Yes       |
|    Scope     |     Global     |
|   Dynamic    |      Yes       |
|  Data type   |    numeric     |
|   Default    | 0 (unlimited)  |
|    Range     | 0 - 1073741824 |

The server rotates the slow query log when the log’s size reaches this value. The default value is `0`. If you limit the size and this feature is enabled, the server renames the slow query log file to slow_query_log_file.000001.

## `max_slowlog_files`

|    Option    |  Description  |
|--------------|---------------|
| Command-line |      Yes      |
| Config file  |      Yes      |
|    Scope     |    Global     |
|   Dynamic    |      Yes      |
|  Data type   |    numeric    |
|   Default    | 0 (unlimited) |
|    Range     |  0 - 102400   |

This variable limits the total amount of slow query log files and is used with max_slowlog_size.

The server creates and adds slow query logs until reaching the range’s upper value. When the upper value is reached, the server creates a new slow query log file with a higher sequence number and deletes the log file with the lowest sequence number maintaining the total amount defined in the range.

[max_binlog_size variable]: https://dev.mysql.com/doc/refman/{{vers}}/en/replication-options-binary-log.html#sysvar_max_binlog_size

[max_binlog_files variable]: https://dev.mysql.com/doc/refman/{{vers}}/en/replication-options-binary-log