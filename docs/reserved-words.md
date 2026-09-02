# Reserved keywords

Percona Server for MySQL defines additional reserved keywords that are not included in the MySQL reserved keyword list. When you use Percona Server for MySQL, consider these keywords reserved in addition to the [MySQL reserved keywords :octicons-link-external-16:](https://dev.mysql.com/doc/refman/9.7/en/keywords.html).

Reserved keywords have a special meaning in SQL syntax and cannot be used as unquoted identifiers. To use a reserved keyword as an identifier, enclose it in backticks (`).

The following table lists the reserved keywords specific to Percona Server for MySQL and the version in which each keyword became reserved:

| Reserved keyword         | Version added |
| ------------------------ | ------------- |
| `CLIENT_STATISTICS`      |               |
| `COMPRESSION_DICTIONARY` |               |
| `EFFECTIVE`              |               |
| `INDEX_STATISTICS`       |               |
| `PERCONA_SEQUENCE_TABLE` |               |
| `TABLE_STATISTICS`       |               |
| `THREAD_STATISTICS`      |               |
| `USER_STATISTICS`        |               |
