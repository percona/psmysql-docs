# PS-Admin script

You can use the ps-admin script allows Enabling the TokuDB Storage Engine and Percona TokuBackup. If the TokuDB storage engine enables the transparent huge pages, the script adds the thp-setting=never option to my.cnf to disable transparent huge pages on runtime.

An example of enabling the TokuDB plugin follows:

```sql
$ sudo ps-admin --enable-tokudb -u root -pPassw0rd
```

The following example enables the TokuBackup.

```sql
$ sudo ps-admin --enable-tokubackup
```

You are able to Enable MyRocks with ps-admin and disable and uninstall the MyRocks storage engine.

An example of the enabling and disabling the MyRocksDB plugin follows:

```sql
$ sudo ps-admin --enable-rocksdb -u root -pPassw0rd
```

```sql
$ sudo ps-admin --disable-rocksdb -u root -pPassw0rd
```

The ps-admin script can also enable or disable the following:


* Audit Log plugin


* PAM Authentication Plugin


* Query Reponse Time plugin


* MYSQLX plugin

An example of enabling the PAM Authentication plugin follows:

```sql
$ sudo ps-admin --enable-pam -u root -pPassw0rd
```
