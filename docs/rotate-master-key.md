# Rotate the master encryption key

Rotate the master encryption key periodically and if the key has been compromised.

Rotating the master encryption key changes that key and tablespace keys are re-encrypted and updated in the tablespace headers. The rotation only succeeds if all operations are successful. If the rotation is interrupted, the operation is rolled forward when the server restarts.

The rotation operation does not affect tablespace data. To change a tablespace key, disable and then re-enable encryption for that tablespace.

The `ENCRYPTION_KEY_ADMIN` privilege is required to rotate the master encryption key.

 InnoDB reads the encryption data from the tablespace header, if certain tablespace keys have been encrypted with the prior master key, InnoDB retrieves the master key from the keyring to decrypt the tablespace key. InnoDB re-encrypts the tablespace key with the new Master key.

Rotate the master encryption key with following statement:

```{.bash data-prompt="mysql>"}
mysql> ALTER INSTANCE ROTATE INNODB MASTER KEY;
```

The rotation operation must complete before any tablespace encryption operation
can begin.
    