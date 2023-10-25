# Extended SELECT INTO OUTFILE/DUMPFILE

Percona Server for MySQL extends the `SELECT INTO ... OUTFILE` and `SELECT INTO
DUMPFILE` [commands] to add support for UNIX sockets and named pipes. Before this was implemented
the database would return an error for such files.

This feature allows using `LOAD DATA LOCAL INFILE` in combination with
`SELECT INTO OUTFILE` to quickly load multiple partitions across the network
or in other setups, without having to use an intermediate file that wastes
space and I/O.

[commands]: https://dev.mysql.com/doc/refman/{{vers}}/en/select-into.html
