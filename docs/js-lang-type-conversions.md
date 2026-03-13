# js_lang type conversions

--8<--- "tech.preview.md:5:5"

SQL and JS use different data types, so the js_lang component converts values when passing SQL parameters to JS and back. This document describes how these conversions work.

## Convert SQL data types to JS

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

When the data converts to a JS string, it automatically changes from the SQL parameter's character set to `utf8mb4`, which JS uses.

## Convert JS data types to SQL

The system uses the target SQL data type to determine how to convert each value. It typically converts a JS value into a basic type—such as a string, integer, or double—based on the specified SQL type. Once converted, the system stores the result in the corresponding SQL parameter or return value.

If a value exceeds allowed limits or uses an unsupported format, the conversion fails and triggers an error. During this process, the system automatically converts JS strings from the utf8mb4 encoding to the character set defined by the SQL parameter.

The system always maps JS null and undefined values to SQL NULL, regardless of the target SQL type.

### JS to SQL type conversion rules

<!-- Clarify what the versions here refer to.-->


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

- [js_lang stored procedure and function overview](js-lang-overview.md)
- [js_lang stored function or procedure](js-lang-procedures.md)
- [Troubleshoot js_lang procedures and functions](js-lang-troubleshoot.md)
