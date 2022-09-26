# Encrypting Doublewrite Buffers

A summary of Doublewrite buffer and Doublewrite buffer encryption changes:

|_Percona Server for MySQL_ Versions| Doublewrite Buffer and Doublewrite Buffer Encryption Implementation|
|---|---|
|Percona Server from Percona-Server-8.0.23-14|_MySQL_ 8.0.23 implemented its own version of [parallel doublewrite encryption](https://dev.mysql.com/doc/refman/8.0/en/innodb-data-encryption.html#innodb-doublewrite-file-encryption). Pages that belong to encrypted tablespaces are also written into the doublewrite buffer in an encrypted form. Percona’s implementation was reverted and [innodb\_parallel\_dblwr\_encrypt](#innodb-parallel-dblwr-encrypt) is deprecated.|
|Percona Server from Percona-Server-8.0.20-11 to Percona-Server-8.0.22-13 inclusive|_MySQL_ 8.0.20 implemented its own [parallel doublewrite buffer](https://dev.mysql.com/doc/refman/8.0/en/innodb-doublewrite-buffer.html), which is stored in external files (#ib\_16384\_xxx.dblwr) and not stored in the system tablespace. Percona’s implementation was reverted. As a result, [innodb\_parallel\_doublewrite\_path](../performance/xtradb_performance_improvements_for_io-bound_highly-concurrent_workloads.html#innodb-parallel-doublewrite-path) was deprecated. <br> However, _MySQL_ did not implement parallel doublewrite buffer encryption at this time, so Percona reimplemented parallel doublewrite buffer encryption on top of the _MySQL_ parallel doublewrite buffer implementation. Percona preserved the meaning and functionality of the [innodb\_parallel\_dblwr\_encrypt](#innodb-parallel-dblwr-encrypt) variable. |
|Percona-Server-8.0.12-1.alpha to Percona-Server-8.0.19-10 inclusive|_Percona Server for MySQL_ had its own implementation of the parallel doublewrite buffer which was enabled by setting the [innodb\_parallel\_doublewrite\_path](../performance/xtradb_performance_improvements_for_io-bound_highly-concurrent_workloads.html#innodb-parallel-doublewrite-path) variable. <br> Enabling the [innodb\_parallel\_dblwr\_encrypt](#innodb-parallel-dblwr-encrypt) controlled whether the parallel doublewrite pages were encrypted or not. In case the parallel doublewrite buffer was disabled ([innodb\_parallel\_doublewrite\_path](../performance/xtradb_performance_improvements_for_io-bound_highly-concurrent_workloads.html#innodb-parallel-doublewrite-path) was set to empty string),the doublewrite buffer pages were located in the system tablespace (ibdata1). The system tablespace itself could be encrypted by setting [innodb\_sys\_tablespace\_encrypt](encrypting-system-tablespace.html#innodb-sys-tablespace-encrypt), which also encrypted the doublewrite buffer pages.|


For *Percona Server for MySQL* versions below *Percona Server for MySQL* version 8.0.23-14, *Percona* encrypts the `doublewrite buffer` using innodb_parallel_dblwr_encrypt.

### `innodb_parallel_dblwr_encrypt`

| Option       | Description                     |
|--------------|---------------------------------|
| Command-line | --innodb-parallel-dblwr-encrypt |
| Scope        | Global                          |
| Dynamic      | Yes                             |
| Data type    | Boolean                         |
| Default      | OFF                             |

The variable was announced as deprecated in Percona Server for MySQL 8.0.23-14.

This variable controls whether the parallel doublewrite buffer pages were encrypted or not. The encryption used the key of the tablespace to which the page belongs.

Starting from *Percona Server for MySQL* 8.0.23-14 the value of this variable is ignored. Pages from the encrypted tablespaces are always written to the doublewrite buffer as encrypted, and pages from unencrypted tablespaces are always written unencrypted.

The `innodb_parallel_dblwr_encrypt` is accepted but has no effect. An explicit attempt to change the value generates the following warning in the error log file:

```text
**Setting Percona-specific INNODB_PARALLEL_DBLWR_ENCRYPT is deprecated and has no effect.**
```
