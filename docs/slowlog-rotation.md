# Slow query log rotation and expiration

!!! important

    --8<--- "tech.preview.md:5:5"

This feature was implemented in *Percona Server for MySQL* 8.0.27-18.

Percona has implemented two new variables, `max_slowlog_size` and `max_slowlog_files` to provide users with ability to control the slow query log disk usage. These variables have the same behavior as the [max_binlog_size variable](https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#sysvar_max_binlog_size) and the [max_binlog_files variable](https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#sysvar_max_binlog_size) used for controlling the binary log.

## System variables

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

The `max_slowlog_size` variable controls when the server rotates the slow query log file based on size.

The value is set to `0` by default, which means the server does not automatically rotate the slow query log file.

The block size is `4096` bytes. If you set a value that is not a multiple of `4096`, the server rounds it down to the nearest multiple of `4096`. For example, setting `max_slowlog_size` to any value less than `4096` will effectively set the value to `0`.

If you set a limit for this size and enable this feature, the server will rename the slow query log file to `slow_query_log_file.000001` once it reaches the specified size.

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

This variable limits the total amount of slow query log files and is used with `max_slowlog_size`.

The server creates and adds slow query logs until it reaches the range’s upper value. When the upper value is reached, the server creates a new slow query log file with a higher sequence number and deletes the log file with the lowest sequence number, maintaining the total amount defined in the range.
