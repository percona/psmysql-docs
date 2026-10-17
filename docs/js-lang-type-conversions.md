# js_lang type conversions

--8<--- "tech.preview.md:5:5"

SQL and JS use different data types, so the js_lang component converts values when passing SQL parameters to JS and back. This document describes how these conversions work.

## Convert SQL data types to JS

SQL `NULL` values are converted to JS `null` values.

| SQL type | JS return type | Notes |
|-----------|----------------|--------|
| BOOLEAN, TINYINT, SMALLINT, MEDIUMINT, INT | Number | |
| BIGINT | Number or BigInt | Number for values in [-(2^53-1), 2^53-1]. The magnitude limit is 9007199254740991. BigInt outside that range. `9007199254740991` is a Number. `-9007199254740992` and `9007199254740992` are BigInt. |
| DECIMAL | String | |
| FLOAT, DOUBLE | Number | |
| BIT(k) | Number or BigInt | Number for k ≤ 53, BigInt for k > 53 |
| TIME, DATE, TIMESTAMP, DATETIME | String | |
| YEAR | Number | |
| CHAR, VARCHAR, TINYTEXT, TEXT, MEDIUMTEXT, LONGTEXT | String | Fails if length exceeds 2^29 - 24 |
| BINARY, VARBINARY, TINYBLOB, BLOB, MEDIUMBLOB, LONGBLOB | DataView | |
| ENUM, SET | String | |
| GEOMETRY and spatial types | DataView | |
| JSON | Object, Array, or number | An object arrives as Object. An array arrives as Array. A scalar such as `1` arrives as number. |

When the data converts to a JS string, it automatically changes from the SQL parameter's character set to `utf8mb4`, which JS uses.

## Convert JS data types to SQL

The system uses the target SQL data type to determine how to convert each value. It typically converts a JS value into a basic type—such as a string, integer, or double—based on the specified SQL type. Once converted, the system stores the result in the corresponding SQL parameter or return value.

In strict SQL mode, an integer value past the target type's limit returns `ERROR 1264`. `FLOAT` can store a rounded value when it can represent the number.

The system converts JS strings from the utf8mb4 encoding to the character set defined by the SQL parameter.

JS `null` and `undefined` become SQL `NULL` for all 25 parameter types tested. Function return values were tested for `INT` and `VARCHAR`. Both become SQL `NULL`.

### JS to SQL type conversion rules

These rules were tested on Percona Server for MySQL 9.7.2.

| Target SQL Data Type | Conversion Rules | Explanation | Example |
|--------------------------|----------------------|------------------|-------------|
| `BOOLEAN`, `TINYINT`, `SMALLINT`, `MEDIUMINT`, `INT`, `BIGINT` | - Numbers: stored as integers<br>- Booleans: `true` → `1`, `false` → `0`<br>- BigInts: stored as integers when possible<br>- Other types: converted to strings first | These types round non-integer Numbers to the nearest integer. Halves round away from zero. `true` and `false` are stored as the integers `1` and `0`. The strings `"3.14"` and `"3.5"` are stored as `3` and `4`. | `42` → `42`<br>`3.14` → `3`<br>`3.5` → `4`<br>`2.5` → `3`<br>`-3.5` → `-4`<br>`0.5` → `1`<br>`-0.5` → `-1`<br>`123.45` → `123`<br>`true` → `1`<br>`false` → `0`<br>`"3.14"` → `3`<br>`"3.5"` → `4`<br>`'abc'` → `ERROR 1366`<br>`NaN` → `ERROR 1366 Incorrect integer value: 'NaN'`<br>`9007199254740991n` into `INT` → `ERROR 1264`<br>`9007199254740991n` into `BIGINT` is stored exactly |
| `DECIMAL` | - All values converted to strings<br>- Booleans: converted to `0`/`1` | The stored value is a `DECIMAL` at the column's scale. For `DECIMAL(10,2)`, `true` is stored as `1.00`. `JSON_TYPE` returns `DECIMAL`. | `123.45` → `123.45`<br>`3.14` → `3.14`<br>`true` → `1.00`<br>`false` → `0.00`<br>`"3.14"` is stored<br>`"3.5"` is stored |
| `FLOAT`, `DOUBLE` | - Numbers: stored as doubles<br>- Booleans: `true` → `1`, `false` → `0`<br>- Others: converted to strings | `3.14` stays `3.14`. `NaN` fails with `ERROR 1264` (out of range). `FLOAT` stores `12345678901.23` as `12345678848` and returns `ERROR 1264` for `1e39`. `DOUBLE` stores both values. | `3.14` → `3.14`<br>`true` → `1`<br>`false` → `0`<br>`'abc'` → `ERROR 1366`<br>`NaN` → `ERROR 1264`<br>`9007199254740991n` into `DOUBLE` keeps all digits<br>`9007199254740991n` into `FLOAT` → `9.0072e15` |
| `BIT` | Converted to SQL BIT type | Only binary-compatible values allowed | `1` → `BIT(1)` |
| `TIME` | A time string is stored as given. A datetime string keeps only the time. A Number is read as `hhmmss`. A date-only string returns `ERROR 1292`. | `3.14` is stored as `00:00:03`. | `"12:34:56"` → `12:34:56`<br>`"2024-01-30 12:34:56"` → `12:34:56`<br>`123456` → `12:34:56`<br>`2024` → `00:20:24`<br>`1` → `00:00:01`<br>`"2024-01-30"` → `ERROR 1292` |
| `DATE` | A date string is stored as given. A datetime string keeps only the date. Every Number returns `ERROR 1292`. | | `"2024-01-30"` → `2024-01-30`<br>`"2024-01-30 12:34:56"` → `2024-01-30`<br>`"12:34:56"` → `ERROR 1292`<br>`123456` → `ERROR 1292` |
| `TIMESTAMP`, `DATETIME` | A datetime string is stored as given. A date-only string is stored with time `00:00:00`. A time-only string or a Number returns `ERROR 1292`. | `TIMESTAMP` and `DATETIME` matched for these values. | `"2024-01-30 12:34:56"` is stored as given<br>`"2024-01-30"` → `2024-01-30 00:00:00`<br>`"12:34:56"` → `ERROR 1292` |
| `CHAR`, `VARCHAR`, `TEXT`, etc. | All values converted to strings<br>Charset conversion from `utf8mb4` if needed | Supports text types with encoding fallback. For `VARCHAR`, `true` is stored as the text `true`, not `1`. A string containing a character the target charset lacks fails with `ERROR 1366`. | `"hello"` → `"hello"`<br>`true` → `true`<br>`'abc'` is stored<br>`U+4E2D` into a `latin1` column → `ERROR 1366` |
| `BINARY`, `VARBINARY`, `BLOB`, etc. | - `ArrayBuffer`/`View`: stored directly<br>- Others: converted to strings | Binary data must be explicitly wrapped; others fallback to string | `buffer` → binary |
| `SET` | - Numbers: stored as integers/doubles<br>- BigInts: stored as integers<br>- Others: converted to strings with charset conversion if needed | Tries native storage before falling back to strings | `1` → `1`<br>`"value"` → `"value"` |
| `GEOMETRY` | - Valid `ArrayBuffer`/`View`: stored as binary<br>- Others: cause an error | Only ArrayBuffer-based values are accepted. A JS string causes an error. | valid buffer → `GEOMETRY` |
| `JSON` | Converted using `JSON.stringify()` | Converts objects or arrays to serialized strings | `{key: "value"}` → `"{"key":"value"}"` |

These `TIME`, `DATE`, `TIMESTAMP`, and `DATETIME` results are from strict SQL mode. `true`, `"a"`, `"c"`, `"abc"`, and a `Date` object return `ERROR 1292` for all four types. `Date()` returns a string such as `Sat Oct 10 2026 13:53:24 GMT+0000 (UTC)`.

In strict SQL mode, a value past an integer type's limit returns `ERROR 1264`. `TINYINT` is signed, from -128 to 127, so `255` returns `ERROR 1264`. `BOOLEAN` matches `TINYINT`.

| JS value | BOOLEAN and TINYINT | SMALLINT | MEDIUMINT | INT | BIGINT |
|---|---|---|---|---|---|
| 999, -999, 128, -129, 255 | `ERROR 1264` | stored | stored | stored | stored |
| 32768 | `ERROR 1264` | `ERROR 1264` | stored | stored | stored |
| 8388608 | `ERROR 1264` | `ERROR 1264` | `ERROR 1264` | stored | stored |
| 2147483648 | `ERROR 1264` | `ERROR 1264` | `ERROR 1264` | `ERROR 1264` | stored |
| BigInt 2^63-1 | `ERROR 1264` | `ERROR 1264` | `ERROR 1264` | `ERROR 1264` | stored |
| BigInt 2^63 | `ERROR 1264` | `ERROR 1264` | `ERROR 1264` | `ERROR 1264` | `ERROR 1264` |

`DECIMAL(10,2)` returns `ERROR 1264` for `1e39` and `12345678901.23`.

If a value has more decimal places than the column's scale, it is rounded to the nearest value. Halves round away from zero. In a `DECIMAL(10,2)` column, `3.145` is stored as `3.15` and `-3.145` is stored as `-3.15`. MySQL raises a note with code 1265, `Data truncated`. The statement does not return an error. The message says truncated, but the value is rounded. This behavior is the same in strict and non-strict SQL mode. `2.675` is stored as `2.68`. `1.005` is stored as `1.01`.

When the routine is created with an empty `sql_mode`, an out-of-range `TINYINT`, `INT`, or `DECIMAL` value is clamped. An out-of-range `ENUM` value is stored as the empty string. An out-of-range `YEAR` value is stored as `0` or as the leading digits. Each of these results includes a warning. The routine uses the `sql_mode` from creation time. The session `sql_mode` at call time does not change it.

`BOOLEAN`, `TINYINT`, `SMALLINT`, `MEDIUMINT`, `INT`, and `BIGINT` round non-integer Numbers to the nearest integer. Halves round away from zero.

## Further reading

- [js_lang stored procedure and function overview](js-lang-overview.md)
- [js_lang stored function or procedure](js-lang-procedures.md)
- [Troubleshoot js_lang procedures and functions](js-lang-troubleshoot.md)
