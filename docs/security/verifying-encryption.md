# Verifying the Encryption for Tables, Tablespaces, and Schemas

If a general tablespace contains tables, check the table information to see if
the table is encrypted. When the general tablespace contains no tables, you
may verify if the tablespace is encrypted or not.

For single tablespaces, verify the ENCRYPTION option using
INFORMATION_SCHEMA.TABLES and the CREATE OPTIONS settings.

```sql
mysql> SELECT TABLE_SCHEMA, TABLE_NAME, CREATE_OPTIONS FROM
       INFORMATION_SCHEMA.TABLES WHERE CREATE_OPTIONS LIKE '%ENCRYPTION%';
```

The output could be the following:

```text
+----------------------+-------------------+------------------------------+
| TABLE_SCHEMA         | TABLE_NAME        | CREATE_OPTIONS               |
+----------------------+-------------------+------------------------------+
|sample                | t1                | ENCRYPTION="Y"               |
+----------------------+-------------------+------------------------------+
```

A `flag` field in the `INFORMATION_SCHEMA.INNODB_TABLESPACES` has bit number
13 set if the tablespace is encrypted. This bit can be checked with the `flag &
8192` expression in the following way:

```
SELECT space, name, flag, (flag & 8192) != 0 AS encrypted FROM
INFORMATION_SCHEMA.INNODB_TABLESPACES WHERE name in ('foo', 'test/t2', 'bar',
'noencrypt');
```

The encrypted table metadata is contained in the
INFORMATION_SCHEMA.INNODB_TABLESPACES_ENCRYPTION table. You must have the
`Process` privilege to view the table information.

!!! note

    **This table is in tech preview and may change in future releases.**

```sql
   mysql> DESCRIBE INNODB_TABLESPACES_ENCRYPTION;
```

The output could be:

```text
+-----------------------------+--------------------+-----+----+--------+------+
| Field                       | Type               | Null| Key| Default| Extra|
+-----------------------------+--------------------+-----+----+--------+------+
| SPACE                       | int(11) unsigned   | NO  |    |        |      |
| NAME                        | varchar(655)       | YES |    |        |      |
| ENCRYPTION_SCHEME           | int(11) unsigned   | NO  |    |        |      |
| KEYSERVER_REQUESTS          | int(11) unsigned   | NO  |    |        |      |
| MIN_KEY_VERSION             | int(11) unsigned   | NO  |    |        |      |
| CURRENT_KEY_VERSION         | int(11) unsigned   | NO  |    |        |      |
| KEY_ROTATION_PAGE_NUMBER    | bigint(21) unsigned| YES |    |        |      |
| KEY_ROTATION_MAX_PAGE_NUMBER| bigint(21) unsigned| YES |    |        |      |
| CURRENT_KEY_ID              | int(11) unsigned   | NO  |    |        |      |
| ROTATING_OR_FLUSHING        | int(1) unsigned    | NO  |    |        |      |
+-----------------------------+--------------------+-----+----+--------+------+
```

To identify encryption-enabled schemas, query the
INFORMATION_SCHEMA.SCHEMATA table:

```sql
mysql> SELECT SCHEMA_NAME, DEFAULT_ENCRYPTION FROM
INFORMATION_SCHEMA.SCHEMATA WHERE DEFAULT_ENCRYPTION='YES';
```

The output could be:

```text
+------------------------------+---------------------------------+
| SCHEMA_NAME                  | DEFAULT_ENCRYPTION              |
+------------------------------+---------------------------------+
| samples                      | YES                             |
+------------------------------+---------------------------------+
```

!!! note 

    The `SHOW CREATE SCHEMA` statement returns the `DEFAULT ENCRYPTION` clause.
