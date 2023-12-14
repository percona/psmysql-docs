# Kill idle transactions

This feature limits the age of idle transactions for all transactional storage
engines. Kills any idle transaction when the specified limit is reached. This limit prevents users from blocking the InnoDB purge by mistake.

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

