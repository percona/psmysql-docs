# JSON in MySQL

JSON stands for JavaScript Object Notation. It is a lightweight data-interchange format that is easy for humans to read and write. It is also easy for machines to parse and generate. MySQL supports JSON data type, allowing you to store JSON documents in your database. 

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

MySQL provides several functions to work with JSON data.

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
