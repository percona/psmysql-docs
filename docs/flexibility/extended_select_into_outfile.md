# Extended SELECT INTO OUTFILE/DUMPFILE

*Percona Server for MySQL* has extended the `SELECT INTO ... OUTFILE` and `SELECT INTO
DUMPFILE` [commands](http://dev.mysql.com/doc/refman/8.0/en/select-into.html)
to add support for UNIX sockets and named pipes. Before this was implemented
the database would return an error for such files.

This feature allows using `LOAD DATA LOCAL INFILE` in combination with
`SELECT INTO OUTFILE` to quickly load multiple partitions across the network
or in other setups, without having to use an intermediate file that wastes
space and I/O.

## Version Specific Information

    * 8.0.12-1: The feature was ported from *Percona Server for MySQL* 5.7.

## Other Reading

    * *MySQL* bug: [#44835](http://bugs.mysql.com/bug.php?id=44835)
