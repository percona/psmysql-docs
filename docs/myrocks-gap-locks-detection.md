# MyRocks Gap locks detection

The [Gap locks :octicons-link-external-16:](https://dev.mysql.com/doc/refman/{{vers}}/en/innodb-locking.html#innodb-gap-locks) detection is based on a Facebook *MySQL* patch.

If a transactional storage engine does not support gap locks (for example
MyRocks) and a gap lock is being attempted while the transaction isolation
level is either `REPEATABLE READ` or `SERIALIZABLE`, the following SQL
error will be returned to the client and no actual gap lock will be taken
on the effected rows.

??? example "Error message"


    ```{.text .no-copy}
    ERROR HY000: Using Gap Lock without full unique key in multi-table or multi-statement transactions is not allowed. You need to either rewrite queries to use all unique key columns in WHERE equal conditions, or rewrite to single-table, single-statement transaction.
    ```

## Other reading

* [Isolation levels](isolation-levels.md)

* [MyRocks limitations](myrocks-limitations.md#unsupported-innodb-features-in-myrocks)

* [Differences between Percona MyRocks and Facebook MyRocks](myrocks-differences.md)

* [MyRocks supported features](myrocks-added-features.md#locking-reads-with-skip-locked-and-nowait)

* [Percona MyRocks introduction](myrocks-index.md)
