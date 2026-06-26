# Data at Rest Encryption

Data security is a concern for institutions and organizations. `Transparent
Data Encryption (TDE)` or `Data at Rest Encryption` encrypts
data files. Data at rest is any data that is not accessed or changed frequently, stored on different
types of storage devices. Encryption ensures that if an unauthorized user
accesses the data files from the file system, the user cannot read the contents.

If the user uses master key encryption, the MySQL keyring plugin stores the
InnoDB master key, used for the master key encryption implemented by *MySQL*.
The master key is also used to encrypt redo logs, and undo logs, along with the
tablespaces.

--8<--- "encryption-architecture-overview.md"

--8<--- "get-help-snip.md"

## Percona XtraBackup support

--8<--- "xtrabackup-encryption-support.md"
