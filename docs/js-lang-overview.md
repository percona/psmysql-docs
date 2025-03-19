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

The target SQL data type defines how the system converts values. The system typically converts a JS value to one of the basic types, such as string, integer, or double, depending on the SQL data type. After the conversion, the system stores the result in the SQL parameter or return value. This step can fail if the value is too large or has an incorrect format, which will cause an error. During the process, JS strings automatically convert from `utf8mb4` to the character set of the SQL parameter.

JS `null` and `undefined` values always convert to SQL `NULL` values for the target SQL type.

| Target SQL data type | Rules for converting JS value | Example |
|----------------------|----------------------------|---------|
| Integer Numbers (BOOLEAN, TINYINT, SHORTINT, MEDIUMINT, INT, BIGINT) | JS Integers/Numbers: integers stored as-is, BIGINTs attempted as integers, others as strings. | 42 → 42 <br>  3.14 → "3.14" <br> true → "true"|
| DECIMAL | Converted to strings | 123.45 → "123.45" |
| FLOAT, DOUBLE | Stored as doubles for Numbers, converted to strings for other values | 3.14 → 3.14, "3.14" → "3.14" |
| BIT | Converted to SQL BIT type | 1 → BIT(1) |
| BigInt | For BigInt values: stored as integers. For other values: converted to Number then stored. Invalid Number conversions cause errors | 9007n → 9007, "123" → 123 |
| TIME, DATE, TIMESTAMP, DATETIME | Converted to strings | Date() → "2024-01-30" |
| CHAR, VARCHAR, TINYTEXT, TEXT, MEDIUMTEXT, ENUM | Converted to strings with charset conversion if needed | "hello" → "hello" |
| BINARY, VARBINARY, TINYBLOB, BLOB, MEDIUMBLOB, LONGBLOB | ArrayBuffer/ArrayBufferView: stored directly. Other values: converted to strings | buffer → binary data |
| SET | Numbers: stored as integers or doubles. BigInt: stored as integers. Others: converted to strings with charset conversion if needed | 1 → 1, "value" → "value" |
| GEOMETRY | ArrayBuffer/ArrayBufferView: stored as binary if valid GEOMETRY. Other values: error | valid buffer → GEOMETRY |
| JSON | Converted to JSON string using JSON.stringify() | {key: "value"} → "{"key":"value"}" |