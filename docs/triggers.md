# Triggers



## Using triggers

A trigger is a database object that automatically performs a specified action in response to certain events on a table or view. It allows users to enforce business rules, maintain data integrity, and automate tasks within the database.

### Advantages of Using Triggers

| Benefits      | Description                                                                                                                                                                 |
|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Data Integrity | Triggers can enforce data integrity constraints by automatically validating or modifying data before it is inserted, updated, or deleted in a table.                      |
| Audit Trails  | Triggers can be used to create audit trails by recording changes made to the database, including who made the changes and when they occurred.                               |
| Simplified    | Triggers simplify application logic by moving complex business rules and validation checks into the database, reducing the amount of code needed in the application layer. |
| Automated     | Triggers automate repetitive tasks, such as updating denormalized data or sending notifications, by executing predefined actions in response to specified events.       |

### Disadvantages of Using Triggers

| Disadvantages     | Description                                                                                                                                                                            |
|-------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Complexity        | Triggers can add complexity to the database schema and make it harder to understand and maintain, especially when dealing with multiple triggers and complex logic.                |
| Performance       | Triggers may impact database performance, particularly if they involve complex operations or are triggered frequently, leading to increased overhead and slower response times. |
| Debugging         | Triggers can be difficult to debug and troubleshoot, as they are executed automatically in response to events and may not provide detailed error messages or logging information. |
| Dependency        | Triggers create dependencies between database objects, making it challenging to modify or refactor the database schema without considering the impact on existing triggers.     |


### Create a before_insert trigger

```{.bash data-prompt="mysql>"}
mysql> CREATE TRIGGER before_insert_customer
    -> BEFORE INSERT ON customers
    -> FOR EACH ROW
    -> BEGIN
    ->     SET NEW.created_at = NOW();
    -> END;
```

### Create an after_update trigger

```{.bash data-prompt="mysql>"}
mysql> CREATE TRIGGER after_update_inventory
    -> AFTER UPDATE ON inventory
    -> FOR EACH ROW
    -> BEGIN
    ->     INSERT INTO inventory_changes (product_id, old_quantity, new_quantity, change_date)
    ->     VALUES (OLD.product_id, OLD.quantity, NEW.quantity, NOW());
    -> END;
```

### Drop a before_insert trigger

```{.bash data-prompt="mysql>"}
mysql> DROP TRIGGER IF EXISTS before_insert_customer;
```

### Drop an after_update trigger

```{.bash data-prompt="mysql>"}
mysql> DROP TRIGGER IF EXISTS after_update_inventory;
```

## Advanced SQL features

* [Data Types Basic](data-types-basic.md)
* [Functions](functions.md)
* [SQL Conventions](sql-conventions.md)
* [SQL Errors](sql-errors.md)
* [SQL Syntax](sql-syntax.md)
* [Stored Procedures](stored-procedures.md)
* [Stored Procedure Error Handling](stored-procedure-error-handling.md)
* [Stored Procedure Variables](stored-procedure-variables.md)
* [Troubleshooting SQL](troubleshooting-sql.md)