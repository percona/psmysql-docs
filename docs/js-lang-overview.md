# js_lang stored procedure and function overview

--8<--- "tech.preview.md:5:5"

You can use stored procedures and functions written in JS with a MySQL-compatible database. This feature helps you manage complex data processing tasks. This method improves performance. This method lets developers run complex operations faster. If you know JS, you can use your existing skills. Using stored procedures and functions reduces the work done by client applications. Using stored procedures and functions also improves overall system performance. Using stored procedures and functions helps developers process data faster. Using stored procedures and functions also makes maintenance and scaling easier. This approach is a good solution for developers who know JS.

| Benefit                            | Description                                                                                   |
|------------------------------------|-----------------------------------------------------------------------------------------------|
| Familiarity                        | Developers who already know JS can use their existing skills.                                 |
| Efficiency                         | JS can run complex data processing tasks more efficiently.                                    |
| Performance                        | Stored procedures and functions in JS improve database performance. They reduce the work done by client applications.|
| Reusability                        | You can write code once in stored procedures and functions. Then you can use that code in multiple applications.|
| Scalability                        | Using stored procedures and functions makes database operations easier to maintain and scale.  |
| Simplified Development Process     | This feature makes development easier for developers who know JS.                              |
| Integration with Client Applications| Stored procedures and functions work well with client applications. You need less additional processing.|
| Optimization                       | This feature improves overall system performance through efficient data processing.            |


## Limitations

The JS procedure parameters cannot be [JS reserved words :octicons-link-external-16:](https://developer.mozilla.org/en-US/docs/Web/JS/Reference/Lexical_grammar#reserved_words) and must be [legal JS identifiers :octicons-link-external-16:](https://www.capscode.in/blog/valid-identifier-in-js).

Our implementation offers the same level of JS support as the V8 engine inside the context of a database engine. You can check out the details at [v8.dev/docs :octicons-link-external-16:](https://v8.dev/docs) and [tc39.es/ecma262 :octicons-link-external-16:](https://v8.dev/docs). Developers have access to standard operators, data types, objects (such as Math), and functions defined in the ECMAScript standard. However, objects and modules specific to Node.NS or DOM, which are only available in browsers, are not accessible. 

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

## Further reading

- [Install js_lang component](install-js-lang.md)
- [Uninstall the js_lang component](uninstall-js-lang.md)
- [js_lang stored function or procedure](js-lang-procedures.md)
- [js_lang privileges](js-lang-privileges.md)
- [Troubleshoot js_lang procedures and functions](js-lang-troubleshoot.md)
