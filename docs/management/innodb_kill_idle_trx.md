# Kill Idle Transactions

This feature limits the age of idle transactions, for all transactional storage
engines. If a transaction is idle for more seconds than the threshold
specified, it will be killed. This prevents users from blocking InnoDB purge
by mistake.

In *Percona Server for MySQL* Percona Server for MySQL 5.7.17-11 this feature has been re-implemented by
setting a connection socket read timeout value instead of periodically scanning
the internal InnoDB transaction list.

## Version Specific Information

* Percona Server for MySQL 5.7.10-1: Feature ported from *Percona Server for MySQL* 5.6.

* Percona Server for MySQL 5.7.17-11: Feature re-implemented using socket timeouts.

## System Variables

### `innodb_kill_idle_transaction`

| Option      | Description                        |
|-------------|------------------------------------|
| Config file | `YES`|
| Scope       | `GLOBAL`|
| Dynamic     | `YES`|
| Data type   | `INTEGER`|
| Default     | 0 (disabled)                       |
| Units       | Seconds                            |

Starting with Percona Server for MySQL 5.7.17-11 this variable is an alias of kill_idle_transaction. To enable this feature, set this variable to the desired seconds wait until the transaction is killed. 

**NOTE:** This variable has been deprecated and it will be removed in a future major release.

### `kill_idle_transaction`

| Option      | Description                        |
|-------------|------------------------------------|
| Config file | `YES`|
| Scope       | `GLOBAL`|
| Dynamic     | `YES`|
| Data type   | `INTEGER`|
| Default     | 0 (disabled)                       |
| Units       | Seconds                            |

The variable has been implemented in Percona Server for MySQL 5.7.17-11. If non-zero, any idle transaction will be killed after being idle for this many seconds.
