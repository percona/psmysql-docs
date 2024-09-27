# Extended SELECT INTO OUTFILE/DUMPFILE

Percona Server for MySQL improves the `SELECT INTO ... OUTFILE` and `SELECT ... INTO DUMPFILE` commands by allowing them to work with UNIX sockets and named pipes. In the past, using these types of files would cause an error.

This feature lets you quickly combine `LOAD DATA LOCAL INFILE` with `SELECT INTO ... OUTFILE` to transfer data across the network or between different partitions. It avoids creating an intermediate file, saves disk space, and reduces I/O usage. This ability makes data loading more efficient, especially for large datasets or complex configurations.

## Version specific information

* 8.0.12-1: The feature was ported from Percona Server for MySQL 5.7.

