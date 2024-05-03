# Views

A view is a virtual table generated from a SQL query. It allows users to simplify complex queries, hide sensitive data, and provide a customized view of the database without altering the underlying schema.

## Advantages of Using Views

| Benefits        | Description                                                                                                                                                                        |
|-----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Simplification  | Views simplify complex queries by encapsulating them into a single, reusable object. They provide a convenient way to abstract and hide the complexity of underlying tables.       |
| Security        | Views can enhance security by restricting access to sensitive data. Users can be granted access to views containing only the necessary columns, without direct access to the tables. |
| Customization   | Views enable users to create customized perspectives of the data, presenting only the relevant information needed for specific tasks or reports.                                    |
| Performance     | Views can improve query performance by pre-computing and caching results, reducing the need to repeatedly execute complex queries.                                                  |

## Disadvantages of Using Views

| Disadvantages   | Description                                                                                                                                                          |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Complexity      | Views can introduce complexity to the database schema and query execution plan, making it harder to optimize and troubleshoot performance issues.                     |
| Overhead        | Views may incur overhead in terms of storage and processing resources, particularly for materialized views or views involving joins and aggregation functions.         |
| Maintenance     | Views require maintenance to keep them synchronized with the underlying tables. Changes to the base tables may impact the results returned by the view.               |
| Limited Use     | Views have limitations in terms of updateability and support for certain SQL operations, such as ordering or grouping by columns not present in the underlying tables. |

## Create view

```{.bash data-prompt="mysql>"}
mysql> CREATE VIEW customer_orders AS
    SELECT customers.name, orders.order_id, orders.total_amount
    FROM customers
    JOIN orders ON customers.customer_id = orders.customer_id;
```

```{.bash data-prompt="mysql>"}
mysql> CREATE VIEW recent_orders AS
   SELECT *
    FROM orders
    WHERE order_date >= CURDATE() - INTERVAL 30 DAY;
```

## Drop view

```{.bash data-prompt="mysql>"}
mysql> DROP VIEW IF EXISTS customer_orders;
```

```{.bash data-prompt="mysql>"}
mysql> DROP VIEW IF EXISTS recent_orders;
```


## Database management

* [Database](database.md)
* [Modify Tables](modify-tables.md)
* [Isolation Levels](isolation-levels.md)
* [Transaction Management](transaction-mgmt.md)