# Encrypt File-Per-Table Tablespace

A file-per-table tablespace stores the
table data and the indexes for a single InnoDB table. In this tablespace
configuration, each table is stored in a `.ibd` file.

The architecture for data at rest encryption for file-per-table tablespace
has two tiers:

* Master key

* Tablespace keys

The keyring plugin must be installed and enabled. The
file_per_table tablespace inherits the schema default encryption setting unless you explicitly define encryption in `CREATE TABLE` or `ALTER TABLE`.

```text
mysql> CREATE TABLE ... ENCRYPTION='Y';
```

```text
mysql> ALTER TABLE ... ENCRYPTION='Y';
```

Using `ALTER TABLE` without the `ENCRYPTION` option does not change the encryption state. An encrypted table remains encrypted or an unencrypted table remains unencrypted.
