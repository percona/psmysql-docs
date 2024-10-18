# Kill idle transactions

The Idle Transaction Timeout feature helps manage database performance by automatically ending transactions that have been inactive for too long. This feature works with all types of database storage that support transactions.

When you set a time limit, any transaction that stays inactive longer than this limit is automatically stopped. This action prevents forgotten or stuck transactions from slowing down your database by blocking important cleanup processes.

## Determine the idle transaction threshold

When setting up a database, you need to decide how long to let inactive transactions sit before ending them. This decision affects the database's performance.

| Items to consider                  | Description                                                                                          |
|---------------------------------|------------------------------------------------------------------------------------------------------|
| How your database Is used       | Look at how long transactions usually take and how often they happen. If most transactions finish quickly, you should end idle ones sooner. |
| How ,any things happen at once  | Count how many transactions your system handles simultaneously. If it's a lot, you might need to end idle transactions faster to free up space for new ones. |
| How it affects speed            | Watch how idle transactions change your database's speed. If they slow things down a lot, ending them sooner can help keep everything running smoothly. |
| What your business needs        | Think about what's important for your work. Some important transactions might need more time, so you shouldn't end them too quickly. |

## InnoDB purge

The InnoDB purge process in MySQL removes outdated row versions (undo logs) from the system. When a transaction modifies data, InnoDB keeps old row versions for rollback and to support transactions running with multi-version concurrency control (MVCC). Once these versions are no longer needed, the purge process deletes them to free up space and improve performance.

Blocking the InnoDB purge can lead to issues such as increased disk space usage and potential performance degradation. This feature helps prevent issues such by:

* Limiting idle transactions: It kills any idle transaction after a specified threshold, ensuring transactions don’t remain idle for too long.

* Preventing mistakes: Users can’t accidentally block the InnoDB purge by leaving transactions idle.

* Improving performance: Keeping the purge process running smoothly helps maintain optimal database performance.

## System variables

### `kill_idle_transaction`

| Option         | Description        |
| -------------- | ------------------ |
| Config file    | Yes                |
| Scope:         | Global             |
| Dynamic:       | Yes                |
| Data type      | Integer            |
| Default value  | 0 (disabled)       |
| Unit           | Seconds            |

If set to a non-zero value, the server kills any idle transaction after it stays idle for this number of seconds.
