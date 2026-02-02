# Kill idle transaction

Database servers face a constant challenge: managing resources efficiently while maintaining system stability. The kill idle transactions timeout option is a strategic tool to address this challenge. The server automatically stops any transaction that remains inactive for longer than this limit. This action prevents forgotten or stuck transactions from slowing down your database by blocking critical cleanup processes.

The option has the following benefits:

* Automatically terminates long-running, inactive database connections

* Prevents resource hogging by abandoned or forgotten transactions

* Frees up database connection pools

* Reduces unnecessary memory consumption

* Protects against potential connection leaks

* Prevents unnecessary server load from dormant sessions

You must also consider the following:

* May interrupt legitimate long-running queries

* Requires careful configuration to avoid disrupting critical processes

* Can cause unexpected application behavior if timeout is too aggressive

* Might create additional overhead in monitoring and logging

* Requires precise tuning for different application requirements

We recommend that starting with a conservative timeout setting and reviewing the logs frequently to track terminated transactions.

This feature works with all types of database storage that support transactions.

## Best practices

Consider these recommended practices when configuring the idle transaction timeout:

* Starting with a higher timeout value: Begin by setting the `kill_idle_transaction` to a larger value, such as 600 seconds (10 minutes). This initial higher value provides a buffer and reduces the risk of prematurely terminating legitimate, long-running transactions while you observe your application's behavior under normal load.

* Monitoring logs for premature terminations: After implementing the idle transaction timeout, actively monitor the MySQL error logs for messages indicating that transactions are being killed. If you observe "Killed idle transaction" messages frequently for transactions that should still be active, it suggests that your timeout value is too aggressive and needs adjustment.

* Testing in a staging environment: Before applying any changes to the `kill_idle_transaction` setting in your production environment, thoroughly test the configuration in a staging or development environment that closely mirrors your production setup. This testing allows you to identify and resolve any unintended consequences, such as premature transaction terminations, without impacting your live application and data.

## Determine the idle transaction threshold

When setting up a database, you must decide how long to let inactive transactions sit before ending them. This decision affects the database's performance.

| Items to consider                  | Description                                                                                          |
|---------------------------------|------------------------------------------------------------------------------------------------------|
| How your database is used       | Look at how long transactions usually take and how often they happen. If most transactions finish quickly, you should end idle ones sooner. |
| How many things happen at once  | Count how many transactions your system handles simultaneously. You may need to end idle transactions faster to free up space for new ones. |
| How it affects speed            | Monitor how idle transactions change your database's speed. If they noticeably slow down the database, ending these transaction can help keep everything running smoothly. |
| What your business needs        | What's important for your work. Some transactions may need more time. |

## InnoDB purge

The InnoDB purge process removes outdated row versions (undo logs) from the system. When a transaction modifies data, InnoDB keeps old row versions for rollback and to support transactions running with multi-version concurrency control (MVCC). Once these versions are no longer needed, the purge process deletes them to free up space and improve performance.

Blocking the InnoDB purge can lead to increased disk space usage and potential performance degradation. This feature helps prevent issues such as:

| Benefit                | Description                                                                                      |
|------------------------|--------------------------------------------------------------------------------------------------|
| Limiting idle transactions | Kills any idle transaction after a specified threshold, ensuring transactions don’t remain idle for too long. |
| Preventing mistakes        | Users can’t accidentally block the InnoDB purge by leaving transactions idle.                |
| Improving performance      | Keeping the purge process running smoothly helps maintain optimal database performance.      |

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

#### Examples

The `SET GLOBAL kill_idle_transaction = 300;` command configures the server to automatically end any idle transaction that has lasted for 300 seconds (5 minutes). This command immediately takes effect for the current and new server sessions. An idle transaction holds resources, potentially preventing other operations from proceeding. This setting helps to release these resources if a transaction is unintentionally left open.

```sql
SET GLOBAL kill_idle_transaction = 300;
```

The [mysqld] section in the my.cnf configuration file allows you to set server-wide options that persist across server restarts. Adding the line kill_idle_transaction = 300 under [mysqld] makes the idle transaction timeout of 300 seconds the default setting for the server. This setting ensures that the server automatically terminates idle transactions after 5 minutes every time it starts. 

You must restart the server for changes in the my.cnf file to take effect. This configuration prevents long-held idle transactions from consuming resources over extended periods.

```ini
[mysqld]
kill_idle_transaction = 300
```

## Monitor terminated transactions

If the `kill_idle_transaction` setting is active and idle transactions have been terminated, this command will output any lines from the error log that contain the "Killed idle transaction" message. Each matching line typically includes a timestamp and details about the terminated transaction, such as its ID and the duration it was idle. 

If the kill_idle_transaction setting is active and idle transactions have been terminated, this command will output any lines from the error log that contain the “Killed idle transaction” message. Each matching line typically includes a timestamp and details about the terminated transaction, such as its ID and the duration it was idle.

The command produces no output if the server has not terminated any idle transactions since the last log rotation or server start. Regularly checking this log helps you verify that the idle transaction option is working as expected and provides insights into transaction management within your server.


```shell
$ grep "Killed idle transaction" /var/log/mysql/error.log
```