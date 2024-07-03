# Common data types

Choosing the correct data type for each column ensures data accuracy, efficiency, and reliability within the database. The following describes the purpose of a data type in Percona Server for MySQL:

* Purpose:

   * Data types define the kind of data that can be stored in a column of a table.

   * They enforce constraints on the values that can be inserted into the column, ensuring data integrity.

   * Data types determine how the data is stored in memory and on disk, optimizing storage space and performance.

   * They provide a way to specify the format and range of acceptable values for numeric, string, date, and other types of data.

   * Data types facilitate efficient sorting, indexing, and searching of data within the database.

* Importance:

   * Choosing the appropriate data type for each column is crucial for efficient database design and performance.

   * Data types help prevent data corruption and inconsistency by enforcing strict rules for data storage and manipulation.

   * They enable database administrators and developers to define the structure of the database accurately and ensure compatibility with application requirements.

   * Understanding data types allows for effective data modeling and schema design, leading to well-organized and scalable databases.


The following is a description of common data types:

## Integer Types 

Integers are whole numbers without any fractional part. Percona Server for MySQL offers different sizes of integer types to accommodate various ranges of values.

| Data Type name | Description |
| --- | --- |
| `TINYINT` | A very small integer that can hold values from -128 to 127 (signed) or 0 to 255 (unsigned). |
| `SMALLINT` | A small integer that can hold values from -32768 to 32767 (signed) or 0 to 65535 (unsigned). |
| `MEDIUMINT` | A medium-sized integer that can hold values from -8388608 to 8388607 (signed) or 0 to 16777215 (unsigned). |
| `INT` or `INTEGER` | A standard-sized integer that can hold values from -2147483648 to 2147483647 (signed) or 0 to 4294967295 (unsigned). |
| `BIGINT` | A large integer that can hold values from -9223372036854775808 to 9223372036854775807 (signed) or 0 to 18446744073709551615 (unsigned). |

## Floating-Point Types

Floating-point types are used to represent numbers with a fractional part.

| Data Type name | Description |
| --- | --- |
| `FLOAT` | A single-precision floating-point number that can hold up to 7 decimal digits of precision. |
| `DOUBLE` or `REAL` | A double-precision floating-point number that can hold up to 15 decimal digits of precision. |

## Fixed-Point Types

Fixed-point types are used to represent exact numeric values.

* `DECIMAL` or `NUMERIC`: A fixed-point number with user-defined precision and scale.

## String Types

String types are used to store text data.

| Data Type name | Description |
| --- | --- |
| `CHAR` | A fixed-length string that can hold up to 255 characters. |
| `VARCHAR` | A variable-length string that can hold up to 65535 characters. |
| `TEXT` | A string with a maximum length of 65535 characters. |
| `BLOB` | A binary large object that can hold up to 65535 bytes. |

## Date and Time Types

Date and time types are used to store date and time information.

| Data Type name | Description |
| --- | --- |
| `DATE` | A date value in the format YYYY-MM-DD. |
| `TIME` | A time value in the format HH:MM:SS. |
| `DATETIME` | A combination of date and time values in the format YYYY-MM-DD HH:MM:SS. |
| `TIMESTAMP` | A timestamp value representing the number of seconds since the Unix epoch (January 1, 1970). |

## Advanced SQL features

* [Functions](functions.md)
* [SQL Conventions](sql-conventions.md)
* [SQL Errors](sql-errors.md)
* [SQL Syntax](sql-syntax.md)
* [Stored Procedures](stored-procedures.md)
* [Stored Procedure Error Handling](stored-procedure-error-handling.md)
* [Stored Procedure Variables](stored-procedure-variables.md)
* [Triggers](triggers.md)
* [Troubleshooting SQL](troubleshooting-sql.md)
