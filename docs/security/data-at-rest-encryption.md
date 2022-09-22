# Data at Rest Encryption

Data security is a concern for institutions and organizations. `Transparent
Data Encryption (TDE)` or `Data at Rest Encryption` encrypts
data files. Data at rest is
any data that is not accessed or changed frequently, stored on different
types of storage devices. Encryption ensures that if an unauthorized user
accesses the data files from the file system, the user cannot read the contents.

If the user uses master key encryption, the MySQL keyring plugin stores the
InnoDB master key, used for the master key encryption implemented by *MySQL*.
The master key is also used to encrypt redo logs, and undo logs, along with the
tablespaces.

The InnoDB tablespace encryption has the following components:


* The database instance has a master key for tablespaces and a master key
for binary log encryption.


* Each tablespace has a tablespace key. The key is used to encrypt the
Tablespace data pages. Encrypted tablespace keys are written on
the tablespace header. In the master key implementation, the tablespace key
cannot be changed unless you rebuild the table.

Two separate keys allow the master key to be rotated in minimal operation.
When the master key is rotated, each tablespace key is decrypted and
re-encrypted with the new master key. The key rotation only reads and writes to the first page of each tablespace file (.ibd).

An InnoDB tablespace file is comprised of multiple logical and physical pages.
Page 0 is the tablespace header page and keeps the metadata for the tablespace.
The encryption information is stored on page 0 and the tablespace key is
encrypted.

A buffer pool page is not encrypted. An encrypted page is decrypted at the I/O
layer and added to the buffer pool and used to access the data. The page is
encrypted by the I/O layer before the page is flushed to disk.

!!! note

    *Percona XtraBackup* version 8 supports the backup of encrypted general tablespaces. Features that are not Generally Available (GA) in *Percona Server for MySQL* are not supported in *Percona XtraBackup*.
