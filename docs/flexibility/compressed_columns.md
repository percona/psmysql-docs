# Compressed columns with dictionaries

The `per-column compression` feature is a data type modifier, independent from
user-level SQL and *InnoDB* data compression, that causes the data stored in the
column to be compressed on writing to storage and decompressed on reading. For
all other purposes, the data type is identical to the one without the modifier,
i.e. no new data types are created. Compression is done by using the `zlib`
library.

Additionally, it is possible to pre-define a set of strings for each compressed
column to achieve a better compression ratio on relatively small individual
data items.

This feature provides:


* a better compression ratio for text data which consists of a large number of
predefined words (e.g. JSON or XML) using compression methods with static
dictionaries


* a way to select columns in the table to compress (in contrast to the *InnoDB*
row compression method). This feature is based on a patch provided by Weixiang Zhai.

## Specifications

The feature is limited to InnoDB/XtraDB storage engine and to columns of the
following data types:


* `BLOB` (including `TINYBLOB`, `MEDIUMBLOB`, `LONGBLOG`)


* `TEXT` (including `TINYTEXT`, `MEDUUMTEXT`, `LONGTEXT`)


* `VARCHAR` (including `NATIONAL VARCHAR`)


* `VARBINARY`


* `JSON`

A compressed column is declared by using the syntax that extends the existing
`COLUMN_FORMAT` modifier: `COLUMN_FORMAT COMPRESSED`. If this modifier is
applied to an unsupported column type or storage engine, an error is returned.

The compression can be specified:


* when creating a table:
`CREATE TABLE ... (..., foo BLOB COLUMN_FORMAT COMPRESSED, ...);`


* when altering a table and modifying a column to the compressed format:
`ALTER TABLE ... MODIFY [COLUMN] ... COLUMN_FORMAT COMPRESSED`, or
`ALTER TABLE ... CHANGE [COLUMN] ... COLUMN_FORMAT COMPRESSED`.

Unlike Oracle MySQL, compression is applicable to generated stored columns. Use
this syntax extension as follows:

```sql
mysql> CREATE TABLE t1(
       id INT,
       a BLOB,
       b JSON COLUMN_FORMAT COMPRESSED,
       g BLOB GENERATED ALWAYS AS (a) STORED COLUMN_FORMAT COMPRESSED WITH COMPRESSION_DICTIONARY numbers
     ) ENGINE=InnoDB;
```

To decompress a column, specify a value other than `COMPRESSED` to
`COLUMN_FORMAT`: `FIXED`, `DYNAMIC`, or `DEFAULT`. If there is a column
compression/decompression request in an `ALTER TABLE`, it is forced to the
`COPY` algorithm.

Two new variables: innodb_compressed_columns_zip_level and
innodb_compressed_columns_threshold have been implemented.

## Compression dictionary support

To achieve a better compression ratio on relatively small individual data items,
it is possible to predefine a compression dictionary, which is a set of strings
for each compressed column.

Compression dictionaries can be represented as a list of words in the form of a
string (a comma or any other character can be used as a delimiter although not
required). In other words, `a, bb, ccc`, `a bb ccc`, and `abbccc` will have
the same effect. However, the latter is more compact. The Quote symbol
quoting is handled by regular SQL quoting. The maximum supported dictionary length is 32506 bytes (`zlib` limitation).

The compression dictionary is stored in a new system *InnoDB* table.  As this
table is of the data dictionary kind, concurrent reads are allowed, but writes
are serialized, and reads are blocked by writes. Table read through old read
views are not supported, similar to *InnoDB* internal DDL transactions.

### Interaction with innodb_force_recovery variable

Compression dictionary operations are treated like DDL operations with the
exception when innodb_force_value is set to `3`: with values
less than `3`, compression dictionary operations are allowed, and with
values >= `3`, they are forbidden.

!!! note

    Prior to Percona Server for MySQL 8.0.15-6 using Compression dictionary operations with innodb_force_recovery variable set to value > 0 would result in an error.

### Example

In order to use the compression dictionary, you need to create it. This
can be done by running:

```sql
mysql> SET @dictionary_data = 'one' 'two' 'three' 'four';
```

The output should look like this:

```text
Query OK, 0 rows affected (0.00 sec)
```

```sql
mysql> CREATE COMPRESSION_DICTIONARY numbers (@dictionary_data);
```

The output should look like this:

```text
Query OK, 0 rows affected (0.00 sec)
```

To create a table that has both compression and compressed dictionary support
you should run:

```sql
mysql> CREATE TABLE t1(
        id INT,
        a BLOB COLUMN_FORMAT COMPRESSED,
        b BLOB COLUMN_FORMAT COMPRESSED WITH COMPRESSION_DICTIONARY numbers
      ) ENGINE=InnoDB;
```

The following example shows how to insert a sample of JSON data into the table:

```json
SET @json_value =
'[\n'
' {\n'
' "one" = 0,\n'
' "two" = 0,\n'
' "three" = 0,\n'
' "four" = 0\n'
' },\n'
' {\n'
' "one" = 0,\n'
' "two" = 0,\n'
' "three" = 0,\n'
' "four" = 0\n'
' },\n'
' {\n'
' "one" = 0,\n'
' "two" = 0,\n'
' "three" = 0,\n'
' "four" = 0\n'
' },\n'
' {\n'
' "one" = 0,\n'
' "two" = 0,\n'
' "three" = 0,\n'
' "four" = 0\n'
' }\n'
']\n'
;
```

```
mysql> INSERT INTO t1 VALUES(0, @json_value, @json_value);
Query OK, 1 row affected (0.01 sec)
```

## INFORMATION_SCHEMA Tables

This feature implements two new `INFORMATION_SCHEMA` tables.

### `INFORMATION_SCHEMA.COMPRESSION_DICTIONARY`

|Column Name|Description|
|--- |--- |
|‘BIGINT(21)_UNSIGNED dict_version’|‘dictionary version’|
|‘VARCHAR(64) dict_name’|‘dictionary name’|
|‘BLOB dict_data’|‘compression dictionary string’|

This table provides a view of the internal compression dictionary. The
`SUPER` privilege is required to query it.

### `INFORMATION_SCHEMA.COMPRESSION_DICTIONARY_TABLES`

| Column Name                        | Description                                                                   |
|------------------------------------|-------------------------------------------------------------------------------|
| ‘BIGINT(21)_UNSIGNED table_schema’ | ‘table schema’                                                                |
| ‘BIGINT(21)_UNSIGNED table_name’   | ‘table ID from INFORMATION_SCHEMA.INNODB_SYS_TABLES’                          |
| ‘BIGINT(21)_UNSIGNED column_name’  | ‘column position (starts from 0 as in INFORMATION_SCHEMA.INNODB_SYS_COLUMNS)’ |
| ‘BIGINT(21)_UNSIGNED dict_name’    | ‘dictionary ID’                                                               |


This table provides a view over the internal table that stores the mapping
between the compression dictionaries and the columns using them. The `SUPER`
privilege is require to query it.

## Limitations

Compressed columns cannot be used in indices (neither on their own nor as parts
of composite keys).

!!! note

    `CREATE TABLE t2 AS SELECT \* FROM t1` will create a new table with a compressed column, whereas `CREATE TABLE t2 AS SELECT CONCAT(a,'') AS a FROM t1` will not create compressed columns.

    At the same time, after executing the `CREATE TABLE t2 LIKE t1` statement, `t2.a` will have the `COMPRESSED` attribute.

`ALTER TABLE ... DISCARD/IMPORT TABLESPACE` is not supported for tables with
compressed columns. To export and import tablespaces with compressed columns,
you uncompress them first with: `ALTER TABLE ... MODIFY ...
COLUMN_FORMAT DEFAULT`.

## mysqldump command line parameters

By default, with no additional options, `mysqldump` will generate a *MySQL*
compatible SQL output.

All `/\*!50633 COLUMN_FORMAT COMPRESSED \*/` and `/\*!50633 COLUMN_FORMAT
COMPRESSED WITH COMPRESSION_DICTIONARY <dictionary> \*/` won’t be in the dump.

When a new option enable-compressed-columns is specified, all
`/\*!50633 COLUMN_FORMAT COMPRESSED \*/` will be left intact and all `/\*!50633
COLUMN_FORMAT COMPRESSED WITH COMPRESSION_DICTIONARY <dictionary> \*/` will be
transformed into `/\*!50633 COLUMN_FORMAT COMPRESSED \*/`. In this mode, the
dump will contain the necessary SQL statements to create compressed columns,
but without dictionaries.

When a new enable-compressed-columns-with-dictionaries option is
specified, dump will contain all compressed column attributes and compression
dictionary.

Moreover, the following dictionary creation fragments will be added before
`CREATE TABLE` statements which are going to use these dictionaries for the
first time.

```text
/*!50633 DROP COMPRESSION_DICTIONARY IF EXISTS <dictionary>; */
/*!50633 CREATE COMPRESSION_DICTIONARY <dictionary>(...); */
```

Two new options add-drop-compression-dictionary and
skip-add-drop-compression-dictionary will control if `/\*!50633 DROP
COMPRESSION_DICTIONARY IF EXISTS <dictionary> \*/` part from previous paragraph
will be skipped or not. By default, add-drop-compression-dictionary
the mode will be used.

When both enable-compressed-columns-with-dictionaries and
`--tab=<dir>` (separate file for each table) options are specified, necessary
compression dictionaries will be created in each output file using the
following fragment (regardless of the values of
add-drop-compression-dictionary and
skip-add-drop-compression-dictionary options).

```text
/*!50633 CREATE COMPRESSION_DICTIONARY IF NOT EXISTS <dictionary>(...); */
```

## Version Specific Information

* Percona Server for MySQL 8.0.13-3: The feature was ported from *Percona Server for MySQL* 5.7.

## System Variables

### `innodb_compressed_columns_zip_level`

| Option       | Description |
|--------------|-------------|
| Command-line | Yes         |
| Config file  | Yes         |
| Scope        | Global      |
| Dynamic      | Yes         |
| Data type    | Numeric     |
| Default      | 6           |
| Range        | 0-9         |

This variable is used to specify the compression level used for compressed
columns. Specifying `0` will use no compression, `1` the fastest, and `9`
the best compression. The default value is `6`.

### `innodb_compressed_columns_threshold`

| Option       | Description                               |
|--------------|-------------------------------------------|
| Command-line | Yes                                       |
| Config file  | Yes                                       |
| Scope        | Global                                    |
| Dynamic      | Yes                                       |
| Data type    | Numeric                                   |
| Default      | 96                                        |
| Range        | 1 - 2^64-1 (or 2^32-1 for 32-bit release) |

By default, a value being inserted will be compressed if its length exceeds
innodb_compressed_columns_threshold bytes. Otherwise, it will be
stored in the raw (uncompressed) form.

Please also note that because of the nature of some data, the compressed
representation can be longer than the original value. In this case, it does not
make sense to store such values in compressed form as *Percona Server for MySQL* would
have to waste both memory space and CPU resources for unnecessary
decompression. Therefore, even if the length of such non-compressible values
exceeds innodb_compressed_columns_threshold, they will be stored in
an uncompressed form (however, an attempt to compress them will still be made).

This parameter can be tuned to skip unnecessary attempts of data
compression for values that are known in advance by the user to have a bad
compression ratio of their first N bytes.
