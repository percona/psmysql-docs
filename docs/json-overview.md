# JSON in Percona Server for MySQL

JSON stands for JavaScript Object Notation. It is a lightweight data-interchange format that is easy for humans to read and write. It is also easy for machines to parse and generate. Percona Server for MySQL supports JSON data type, allowing you to store JSON documents in your database. 

The JSON data type in Percona Server for MySQL is a handy way to store and work with flexible, semi-structured data right in your database. Think of it as a way to save JSON objects directly into your tables, so you don’t have to convert them into a rigid format.

When you use the JSON data type, the database stores your data in a special binary format that’s optimized for speed and space which is faster and more efficient than just saving JSON as plain text.

The JSON data type is great when your data doesn’t fit into a fixed structure or if it’s likely to change over time. The following are examples of when you would use the JSON data type:

* Storing user preferences or settings.
	
* Capturing logs or other dynamic data.
	
* Handling complex objects without adding a ton of columns to your table.

JSON has the following features:

<style>
  table {
    width: 100%;
    border-collapse: collapse;
  }
  th, td {
    border: 1px solid #ccc;
    padding: 8px;
    text-align: left;
  }
  th:first-child, td:first-child {
    width: auto;
    white-space: nowrap;
  }
</style>

| Feature              | Details                                                                                                               |
|----------------------|-----------------------------------------------------------------------------------------------------------------------|
| Validation Built-In  | Percona Server checks your JSON data when you insert or update it to make sure it’s valid. If something’s wrong, you’ll know right away. |
| Powerful Querying    | You can dig into specific parts of your JSON data using built-in functions like the following: <br>  - `JSON_EXTRACT()` to pull out specific keys or values. <br> - `JSON_CONTAINS()` to check if a key or value exists. <br> - `JSON_SET()` to update parts of your JSON object without replacing the whole thing. |
| Indexing for Speed   | If you often query a particular key inside your JSON, you can create a generated column based on that key and index it, making queries much faster. |

## Use JSON in your database

The following is an example using JSON in your database.

```JSON
CREATE TABLE user_data (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    settings JSON
);

INSERT INTO user_data (name, settings)
VALUES ('John', '{"theme": "dark", "notifications": {"email": true, "sms": false}}');

SELECT JSON_EXTRACT(settings, '$.theme') AS theme
FROM user_data
WHERE name = 'John';
```

* The settings column stores JSON data.

* You can use `JSON_EXTRACT()` to get the value of a specific key, like theme.

JSON in Percona Server for MySQL gives you have the flexibility of NoSQL with the reliability and querying power of a relational database. 

## Create a table with JSON Data Type

Create a table that includes a column with the JSON data type.

```{.bash data-prompt="mysql>"}
mysql> CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    info JSON
);
```

The columns are the following:

* `id` is an auto-incremented primary key.

* `name` is a column for storing the user's name.

* `info` is a column for storing JSON data.

## Insert JSON Data

Insert the JSON data into the table using the `INSERT` statement. The `name` column stores the user's name. The `info` column stores JSON data using the `JSON_OBJECT` function. This function creates a JSON object with key-value pairs.

```{.bash data-prompt="mysql>"}
mysql> INSERT INTO users (name, info) VALUES (
    'John Doe',
    JSON_OBJECT('age', 30, 'city', 'New York', 'email', 'john.doe@example.com')
);
```

## Query JSON Data

You can query JSON data using the `SELECT` statement. The `name` column retrieves the user's name. The `info->>'$.age'` expression retrieves the value of the `age` key from the JSON object stored in the `info` column.

```{.bash data-prompt="mysql>"}
mysql> SELECT name, info->>'$.age' AS age FROM users;
```

## Update JSON Data

You can update JSON data using the `UPDATE` statement. The `JSON_SET` function updates the value of the `age` key in the JSON object stored in the `info` column. The `WHERE` clause specifies that only the row with the name 'John Doe' should be updated.

```{.bash data-prompt="mysql>"}
mysql> UPDATE users
SET info = JSON_SET(info, '$.age', 31)
WHERE name = 'John Doe';
```

## Delete JSON Data

You can delete JSON data using the `DELETE` statement. This statement removes rows from the `users` table where the `city` key in the JSON object stored in the `info` column has the value 'New York'.

```{.bash data-prompt="mysql>"}
mysql> DELETE FROM users WHERE info->>'$.city' = 'New York';
```

## Add New Key-Value Pairs to JSON Data

You can add new key-value pairs to existing JSON data using the `JSON_SET` function. The `JSON_SET` function adds a new key `phone` with the value '123-456-7890' to the JSON object stored in the `info` column.

```{.bash data-prompt="mysql>"}
mysql> UPDATE users
SET info = JSON_SET(info, '$.phone', '123-456-7890')
WHERE name = 'John Doe';
```

## Remove Key-Value Pairs from JSON Data

You can remove key-value pairs from existing JSON data using the `JSON_REMOVE` function. This function removes the `email` key from the JSON object stored in the `info` column.

```{.bash data-prompt="mysql>"}
mysql> UPDATE users
SET info = JSON_REMOVE(info, '$.email')
WHERE name = 'John Doe';
```

## Use JSON Functions

Percona Server for MySQL provides several functions to work with JSON data.

### `JSON_EXTRACT`

You can extract data from a JSON document using the `JSON_EXTRACT` function. This function extracts the value of the `city` key from the JSON object stored in the `info` column.

```{.bash data-prompt="mysql>"}
mysql> SELECT JSON_EXTRACT(info, '$.city') AS city FROM users WHERE name = 'John Doe';
```

### `JSON_ARRAY`

You can create a JSON array using the `JSON_ARRAY` function. This function creates a JSON array with the values 'apple', 'banana', and 'cherry'.

```{.bash data-prompt="mysql>"}
mysql> INSERT INTO users (name, info) VALUES (
    'Jane Smith',
    JSON_ARRAY('apple', 'banana', 'cherry')
);
```

### `JSON_CONTAINS`

You can check if a JSON document contains a specific value using the `JSON_CONTAINS` function. This function checks if the `info` column contains the value 'New York' for the `city` key.

```{.bash data-prompt="mysql>"}
mysql> SELECT name FROM users WHERE JSON_CONTAINS(info, '"New York"', '$.city');
```
