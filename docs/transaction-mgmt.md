# Transaction management

A database transaction is a unit of work performed within a database management system (DBMS) that must be executed atomically and consistently. A transaction represents a series of operations (such as queries, inserts, updates, or deletes) that are treated as a single, indivisible unit. Transactions ensure data integrity by guaranteeing that all of the transaction's operations are completed successfully and permanently saved to the database (committed) or none of them are applied (rolled back).

Percona Server for MySQL provides features for managing transactions to ensure the consistency and reliability of data.Transactions in Percona Server for MySQL are typically managed using the following commands and techniques:

- START TRANSACTION: This command begins a new transaction. Once started, all subsequent SQL statements will be part of the transaction until it is either committed or rolled back.

- COMMIT: The COMMIT command is used to save the changes made during the transaction to the database permanently. Once committed, the changes become visible to other transactions.

- ROLLBACK: The ROLLBACK command is used to undo the changes made during the transaction and restore the database to its state before the transaction begins. It cancels any modifications made within the transaction.

- SAVEPOINT: SAVEPOINTs are markers within a transaction that allow you to set points to which you can later roll back. They provide a way to partially undo changes within a transaction without rolling back the entire transaction.

Transactions in Percona Server for MySQL are ACID-compliant, meaning they adhere to the principles of Atomicity, Consistency, Isolation, and Durability:

| Type        | Description                                                                                                                                                                         |
|-------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Atomicity   | Transactions are atomic, meaning that all the operations within a transaction are treated as a single unit of work. Either all operations are completed successfully, or none of them are applied.                                             |
| Consistency | Transactions ensure that the database remains in a consistent state before and after the transaction. Constraints, triggers, and other rules are enforced to maintain data integrity.                                                             |
| Isolation   | Transactions are isolated from each other, meaning that the changes made within one transaction are not visible to other transactions until the transaction is committed.                                                                             |
| Durability  | Once a transaction is committed, the changes made to the database are permanent and cannot be lost, even in the event of system failure.                                                                                                       |

Percona Server for MySQL supports different transaction isolation levels, such as READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, and SERIALIZABLE, which control how transactions interact with each other and with the data in the database.

## Database management

- [Database](database.md)
- [Modify Tables](modify-tables.md)
- [Isolation Levels](isolation-levels.md)
- [Views](views.md)