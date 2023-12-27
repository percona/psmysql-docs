# Docker troubleshooting


To view the container's logs, use the following command:

```shell
docker logs ps --follow
```
??? example "Expected output"

    ```{.text .no-copy}
    Initializing database
    2022-09-07T15:20:03.158128Z 0 [System] [MY-013169] [Server] /usr/sbin/mysqld (mysqld {{release}}) initializing of server in progress as process 15
    2022-09-07T15:20:03.167764Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
    2022-09-07T15:20:03.530600Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
    2022-09-07T15:20:04.367600Z 0 [Warning] [MY-013829] [Server] Missing data directory for ICU regular expressions: /usr/lib64/mysql/private/.
    ...
    2022-09-07T15:20:13.706090Z 0 [System] [MY-011323] [Server] X Plugin ready for connections. Bind-address: '::' port: 33060, socket: /var/lib/mysql/mysqlx.sock
    2022-09-07T15:20:13.706136Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '{{release}}'  socket: '/var/lib/mysql/mysql.sock'  port: 3306  Percona Server (GPL), Release 21, Revision c59f87d2854.
    ```
You can access the server when you see the `ready for connections` information in the log.
 
If you must troubleshoot the Percona Server for MySQL instance, find the error log in `/var/log/` or `/var/log/mysql/`. The file name may be error.log or mysqld.log. You can view the error log with the following command:

```shell
[mysql@ps] $ more /var/log/mysql/error.log
```

??? example "Expected output"

    ```{.text .no-copy}
    ...
    2017-08-29T04:20:22.190474Z 0 [Warning] 'NO_ZERO_DATE', 'NO_ZERO_IN_DATE' and 'ERROR_FOR_DIVISION_BY_ZERO' sql modes should be used with strict mode. They will be merged with strict mode in a future release.
    2017-08-29T04:20:22.190520Z 0 [Warning] 'NO_AUTO_CREATE_USER' sql mode was not set.
    ...
    ```
