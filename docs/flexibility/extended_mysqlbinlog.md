# Extended mysqlbinlog

!!! note
    
    In Percona Server 8.0.18, the `--compress` option was marked as deprecated and may be removed in a future version of Percona Server for MySQL.

Percona Server for MySQL has implemented compression support for mysqlbinlog. This is similar to support that both `mysql` and
`mysqldump` programs include (the `-C`, `--compress` options “Use
compression in server/client protocol”). Using the compressed protocol helps
reduce the bandwidth use and speed up transfers.

Percona Server for MySQL has also implemented support for `SSL`.
mysqlbinlog now accepts the `SSL` connection options as all the
other client programs. This feature can be useful with
`--read-from-remote-server` option. 

## Version Specific Information

    * 8.0.12-1: The feature was ported from Percona Server for MySQL 5.7
