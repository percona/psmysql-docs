---
title: JS stored procedure and function overview
description: Integrating stored procedures and functions in JS within a MySQL-compatible
  database provides a versatile and practical approach to managing complex data processing
  tasks.
slug: js-lang-overview
since: '8.4'
until: null
stability: tech-preview
technical_preview: true
tags:
- percona-server
- tech-preview
author: Percona Documentation Team
last_modified: '2025-12-18'
draft: false
---


# JS stored procedure and function overview

--8<--- "experimental.md"

Integrating stored procedures and functions in JS within a MySQL-compatible database provides a versatile and practical approach to managing complex data processing tasks. This method significantly enhances performance, allowing developers to execute intricate operations more efficiently. For those proficient in JS, this approach streamlines the development process, reducing the load on client applications and optimizing overall system performance. By employing stored procedures and functions, developers achieve faster data processing and facilitate more manageable maintenance and scalability, making it an ideal solution for those skilled in JS.

| Benefit                            | Description                                                                                   |
|------------------------------------|-----------------------------------------------------------------------------------------------|
| Familiarity                        | Developers who are already proficient in JS can leverage their existing skills.               |
| Efficiency                         | JS allows for more efficient execution of complex data processing tasks.                      |
| Performance                        | Stored procedures and functions in JS can enhance database performance by reducing client load.|
| Reusability                        | Encapsulated logic in stored procedures and functions can be reused across multiple applications.|
| Scalability                        | Facilitates easier maintenance and scalability of database operations.                        |
| Simplified Development Process     | Streamlines the development process, making it more manageable for those skilled in JS.       |
| Integration with Client Applications| Seamless integration with client applications, reducing the need for additional processing.   |
| Optimization                       | Optimizes overall system performance through efficient data processing.                       |


## Limitations

The JS procedure parameters cannot be [JS reserved words](https://developer.mozilla.org/en-US/docs/Web/JS/Reference/Lexical_grammar#reserved_words) and must be [legal JS identifiers](https://www.capscode.in/blog/valid-identifier-in-js).

Our implementation offers the same level of JS support as the V8 engine inside the context of a database engine. You can check out the details at [v8.dev/docs](https://v8.dev/docs) and [tc39.es/ecma262](https://v8.dev/docs). Developers have access to standard operators, data types, objects (such as Math), and functions defined in the ECMAScript standard. However, objects and modules specific to Node.NS or DOM, which are only available in browsers, are not accessible. 

In a typical database environment, direct access to external files (like reading or writing files on the server's file system) is restricted. Our implementation adheres to a trusted external routine language policy, ensuring routines cannot perform operations beyond what is normally possible for database users. Consequently, file or network I/O operations are not supported within our routines.

Our system supports asynchronous JS code, but it does not work well for database routines. Since everything runs on the same thread and there is nothing to wait for asynchronously, using asynchronous code is unnecessary and not recommended.

We always run JS code in strict mode, and developers cannot disable or change this setting.

## Convert SQL data types to JS

SQL and JS use different data types, so our implementation converts values when passing SQL parameters to JS and back. The following rules explain how these conversions work:

SQL `NULL` values are converted to JS `null` values.

| SQL type | JS return type | Notes |
|-----------|----------------|--------|
| BOOLEAN, TINYINT, SHORTINT, MEDIUMINT, INT | Number | |
| BIGINT | Number or BigInt | Number for values [-2^53-1, 2^53-1], BigInt otherwise |
| DECIMAL | String | |
| FLOAT, DOUBLE | Number | |
| BIT(k) | Number or BigInt | Number for k ≤ 53, BigInt for k > 53 |
| TIME, DATE, TIMESTAMP, DATETIME | String | |
| YEAR | Number | |
| CHAR, VARCHAR, TINYTEXT, TEXT, MEDIUMTEXT, LONGTEXT | String | Fails if length exceeds 2^29 - 24 |
| BINARY, VARBINARY, TINYBLOB, BLOB, MEDIUMBLOB, LONGBLOB | DataView | |
| ENUM, SET | String | |
| GEOMETRY and spatial types | DataView | |
| JSON | Object | |

When the data converts to a JS string, it automatically changes from the SQL parameter’s character set to `utf8mb4`, which JS uses.

## Convert JS data types to SQL

The system uses the target SQL data type to determine how to convert each value. It typically converts a JS value into a basic type—such as a string, integer, or double—based on the specified SQL type. Once converted, the system stores the result in the corresponding SQL parameter or return value.

If a value exceeds allowed limits or uses an unsupported format, the conversion fails and triggers an error. During this process, the system automatically converts JS strings from the utf8mb4 encoding to the character set defined by the SQL parameter.

The system always maps JS null and undefined values to SQL NULL, regardless of the target SQL type.

### JS to SQL type conversion rules

| Target SQL Data Type | Conversion Rules | Explanation | Example |
|--------------------------|----------------------|------------------|-------------|
| `BOOLEAN`, `TINYINT`, `SHORTINT`, `MEDIUMINT`, `INT`, `BIGINT` | (Version 8.4.5) - Numbers: stored as integers<br>- Booleans: `true` → `1`, `false` → `0`<br>- BigInts: stored as integers when possible<br>- Other types: converted to strings first<br>(Version 8.4.4) - JS Integers/Numbers: integers stored as-is, BigInts attempted as integers, others as strings.) | Preserves native numeric forms where possible; other values default to string representation | `42` → `42`<br>`3.14` → `"3.14"`<br>`true` → `"1"` |
| `DECIMAL` | - All values converted to strings<br>- Booleans: converted to `0`/`1`, then stored as doubles | Supports precision formatting; special handling ensures Booleans fit numeric context | `123.45` → `"123.45"`<br>`true` → `1.0` |
| `FLOAT`, `DOUBLE` | - Numbers: stored as doubles<br>- (Version 8.4.5) - Booleans: converted to `0`/`1`, then stored as doubles<br>- Others: converted to strings | Treats numeric and Boolean inputs consistently using floating-point representation | `3.14` → `3.14`<br>`true` → `1.0`<br>`"3.14"` → `"3.14"` |
| `BIT` | Converted to SQL BIT type | Only binary-compatible values allowed | `1` → `BIT(1)` |
| `TIME`, `DATE`, `TIMESTAMP`, `DATETIME` | All values converted to strings | Usually expects ISO date formats or equivalents | `Date()` → `"2024-01-30"` |
| `CHAR`, `VARCHAR`, `TEXT`, etc. | All values converted to strings<br>Charset conversion from `utf8mb4` if needed | Supports text types with encoding fallback | `"hello"` → `"hello"` |
| `BINARY`, `VARBINARY`, `BLOB`, etc. | - `ArrayBuffer`/`View`: stored directly<br>- Others: converted to strings | Binary data must be explicitly wrapped; others fallback to string | `buffer` → binary |
| `SET` | - Numbers: stored as integers/doubles<br>- BigInts: stored as integers<br>- Others: converted to strings with charset conversion if needed | Tries native storage before falling back to strings | `1` → `1`<br>`"value"` → `"value"` |
| `GEOMETRY` | - Valid `ArrayBuffer`/`View`: stored as binary<br>- Others: cause an error | Enforces format rules to maintain spatial integrity | valid buffer → `GEOMETRY` |
| `JSON` | Converted using `JSON.stringify()` | Converts objects or arrays to serialized strings | `{key: "value"}` → `"{"key":"value"}"` |