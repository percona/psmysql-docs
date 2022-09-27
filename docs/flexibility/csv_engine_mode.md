# CSV engine mode for standard-compliant quote and comma parsing

[MySQL CSV Storage Engine](https://dev.mysql.com/doc/refman/5.7/en/csv-storage-engine.html) is non-standard with respect to embedded `"` and `,` character parsing. Fixing this issue unconditionally would break MySQL CSV format compatibility for any pre-existing user tables and for data exchange with other MySQL instances, but it would improve compatibility with other CSV producing/consuming tools.

To keep both MySQL and other tool compatibility, a new dynamic, global/session server variable csv_mode has been implemented. This variable allows an empty value (the default), and `IETF_QUOTES`.

If `IETF_QUOTES` is set, then embedded commas are accepted in quoted fields as-is, and a quote character is quoted by doubling it. In legacy mode embedded commas terminate the field, and quotes are quoted with a backslash.

## Example

Table:

```sql
> CREATE TABLE albums (
`artist` text NOT NULL,
`album` text NOT NULL
) ENGINE=CSV DEFAULT CHARSET=utf8
;
```

Following example shows the difference in parsing for default and `IETF_QUOTES` csv_quotes.

```sql
> INSERT INTO albums VALUES ("Great Artist", "Old Album"),
("Great Artist", "Old Album \"Limited Edition\"");
```

If the variable csv_mode is set to empty value (default) parsed data will look like:

```sql
"Great Artist","Old Album"
"Great Artist","\"Limited Edition\",Old Album"
```

If the variable csv_mode is set to `IETF_QUOTES` parsed data will look like as described in [CSV rules](http://en.wikipedia.org/wiki/Comma-separated_values#Basic_rules_and_examples):

```text
"Great Artist","Old Album"
"Great Artist","""Limited Edition"",Old Album"
```

Parsing the CSV file which has the proper quotes (shown in the previous example) can show different results:

With csv_mode set to empty value, parsed data will look like:

```sql
> SELECT * FROM albums;
```
The output could be similar to the following:

```text
+--------------+--------------------+
| artist       | album              |
+--------------+--------------------+
| Great Artist | Old Album          |
| Great Artist | ""Limited Edition" |
+--------------+--------------------+
2 rows in set (0.02 sec)
```

With csv_mode set to `IETF_QUOTES` parsed data will look like:

```
mysql> SET csv_mode = 'IETF_QUOTES';
```
The output could be similar to the following:

```text
Query OK, 0 rows affected (0.00 sec)
```

```sql
> SELECT * FROM albums;
```
The output could be similar to the following:

```text
+--------------+-----------------------------+
| artist       | album                       |
+--------------+-----------------------------+
| Great Artist | Old Album                   |
| Great Artist | "Limited Edition",Old Album |
+--------------+-----------------------------+
```

## Version Specific Information

* Percona Server for MySQL 5.7.10-1: Feature ported from *Percona Server for MySQL* 5.6

## System Variables

### <a id="csv-mode" /> csv_mode

| Option       | Description                     |
|--------------|---------------------------------|
| Command-line | Yes                             |
| Config file  | Yes                             |
| Scope        | Global, Session                 |
| Dynamic      | Yes                             |
| Data type    | SET                             |
| Default      | `(empty string)`                |
| Range        | `(empty string)`, `IETF_QUOTES` |

Setting this variable is to `IETF_QUOTES` will enable the standard-compliant quote parsing: commas are accepted in quoted fields as-is, and quoting of `"` is changed from `\\"` to `""`. If the variable is set to empty value (the default), then the old parsing behavior is kept.

## Related Reading

* [MySQL bug #71091](https://bugs.mysql.com/bug.php?id=71091)
