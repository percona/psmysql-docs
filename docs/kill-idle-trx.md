# Kill idle transactions

This feature limits the age of idle transactions, for all transactional storage
engines. If a transaction is idle for more seconds than the threshold
specified, it will be killed. This prevents users from blocking *InnoDB* purge
by mistake.

## System variables

### `kill_idle_transaction`

| Option         | Description        |
| -------------- | ------------------ |
| Config file    | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type      | Integer            |
| Default value  | 0 (disabled)       |
| Units          | Seconds            |

If non-zero, any idle transaction will be killed after being idle for this many seconds.
