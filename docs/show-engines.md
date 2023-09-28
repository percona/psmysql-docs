# Show storage engines

This feature changes the comment field displayed when the `SHOW STORAGE ENGINES` command is executed and *XtraDB* is the storage engine.

## Version specific information

* 8.0.12-1: The feature was ported from *Percona Server for MySQL* 5.7.

Before the Change:

```{.bash data-prompt="mysql>"}
mysql> show storage engines;
```

??? example "Expected output"

    ```{.text .no-copy}
    +------------+---------+----------------------------------------------------------------+--------------+------+------------+
    | Engine     | Support | Comment                                                        | Transactions | XA   | Savepoints |
    +------------+---------+----------------------------------------------------------------+--------------+------+------------+
    | InnoDB     | YES     | Supports transactions, row-level locking, and foreign keys     | YES          | YES  | YES        |
    ...
    +------------+---------+----------------------------------------------------------------+--------------+------+------------+
    ```

After the Change:

```{.bash data-prompt="mysql>"}
mysql> show storage engines;
```

??? example "Expected output"

    ```{.text .no-copy}
    +------------+---------+----------------------------------------------------------------------------+--------------+------+------------+
    | Engine     | Support | Comment                                                                    | Transactions |   XA | Savepoints |
    +------------+---------+----------------------------------------------------------------------------+--------------+------+------------+
    | InnoDB     | YES     | Percona-XtraDB, Supports transactions, row-level locking, and foreign keys |          YES | YES  | YES        |
    ...
    +------------+---------+----------------------------------------------------------------------------+--------------+------+------------+
    ```