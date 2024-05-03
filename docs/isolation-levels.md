# Isolation levels

In databases, isolation levels define how transactions interact with each other and the data they access. They determine the level of concurrency and consistency in a multi-user database environment.

In MySQL, there are four isolation levels available, each offering different trade-offs between concurrency and consistency:

Each isolation level offers a different balance between concurrency and consistency, and the choice depends on the application's specific requirements. By selecting the appropriate isolation level, developers can ensure their MySQL database applications' desired data integrity and performance level.


## Read Uncommitted

In the Read Uncommitted isolation level, transactions can read data that has been modified by other transactions but not yet committed. This level allows for the highest concurrency but can lead to dirty reads.

```{.bash data-prompt="mysql>"}
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;

-- Perform a SELECT query to read uncommitted data
SELECT * FROM table_name;
```

## Read Committed

In Read Committed isolation level, transactions can only read data that has been committed by other transactions. This level prevents dirty reads but allows for non-repeatable reads and phantom reads.

```{.bash data-prompt="mysql>"}
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- Perform a SELECT query to read committed data
SELECT * FROM table_name;
```

## Repeatable Read

In Repeatable Read isolation level, transactions can only read data that has been committed by other transactions at the start of the transaction. This level prevents dirty reads and non-repeatable reads but allows for phantom reads.

```{.bash data-prompt="mysql>"}
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;

-- Perform a SELECT query to read data consistently within the transaction
SELECT * FROM table_name;
```

## Serializable

In Serializable isolation level, transactions are executed serially, preventing any concurrent access to the data. This level provides the highest level of isolation but can lead to reduced concurrency and potential deadlock situations.

```{.bash data-prompt="mysql>"}
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Perform a SELECT query within a serializable transaction
SELECT * FROM table_name;
```

These examples demonstrate how to set and use different isolation levels in SQL transactions, each providing consistency and concurrency control.

## Database management

* [Database](database.md)
* [Modify Tables](modify-tables.md)
* [Transaction Management](transaction-mgmt.md)
* [Views](views.md)
