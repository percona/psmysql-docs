# Slow Query Log Rotation and Expiration

**NOTE**: This feature is currently considered BETA quality.

Percona has implemented two new variables, max_slowlog_size and max_slowlog_files to provide users with ability to control the slow query log disk usage. These variables have the same behavior as upstream variable [max_binlog_size](https://dev.mysql.com/doc/refman/5.7/en/replication-options-binary-log.html#sysvar_max_binlog_size) and max_binlog_files variable used for controlling the binary log.

**WARNING**: For this feature to work variable slow_query_log_file needs to be set up manually and without the `.log` sufix. The slow query log files will be named using slow_query_log_file as a stem, to which a dot and a sequence number will be appended.

## Version Specific Information

> 
> * Percona Server for MySQL 5.7.10-1:
> Feature ported from *Percona Server for MySQL* 5.6

## System Variables

### `max_slowlog_size`

| Option       | Description       |
|--------------|-------------------|
| Command-line | Yes               |
| Config file  | Yes               |
| Scope        | Global            |
| Dynamic      | Yes               |
| Data type    | numeric           |
| Default      | 0 (unlimited)     |
| Range        | 4096 - 1073741824 |

Slow query log will be rotated automatically when its size exceeds this value. The default is `0`, don’t limit the size. When this feature is enabled slow query log file will be renamed to slow_query_log_file.000001.

### `max_slowlog_files`

| Option       | Description   |
|--------------|---------------|
| Command-line | Yes           |
| Config file  | Yes           |
| Scope        | Global        |
| Dynamic      | Yes           |
| Data type    | numeric       |
| Default      | 0 (unlimited) |
| Range        | 0 - 102400    |

Maximum number of slow query log files. Used with max_slowlog_size this can be used to limit the total amount of slow query log files. When this number is reached server will create a new slow query log file with increased sequence number. Log file with the lowest sequence number will be deleted.
