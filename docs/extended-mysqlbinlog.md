# Extended mysqlbinlog

<!--- Check whether the note is actual--->

!!! note
    
    The `--compress` option was marked as deprecated and may be removed in a future version of Percona Server for MySQL.

Percona Server for MySQL has implemented compression support for mysqlbinlog. This is similar to support that both `mysql` and
`mysqldump` programs include (the `-C`, `--compress` options “Use
compression in server/client protocol”). Using the compressed protocol helps
reduce the bandwidth use and speed up transfers.

Percona Server for MySQL has also implemented support for `SSL`.
mysqlbinlog now accepts the `SSL` connection options as all the
other client programs. This feature can be useful with
`--read-from-remote-server` option. 

