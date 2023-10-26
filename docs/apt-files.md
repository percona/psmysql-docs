# Files in the DEB package built for Percona Server for MySQL {{vers}}

| Package                      | Contains                                                                                                                                                                        |
|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| percona-server-server   | The database server itself, the mysqld binary and associated files.                                                                                                             |
| percona-server-common        | The files common to the server and client.                                                                                                                                      |
| percona-server-client        | The command line client.                                                                                                                                                        |
| percona-server-dbg           | Debug symbols for the server.                                                                                                                                                   |
| percona-server-test          | The database test suite.                                                                                                                                                        |
| percona-server-source        | The server source.                                                                                                                                                              |
| libperconaserverclient21-dev | Header files needed to compile software to use the client library.                                                                                                              |
| libperconaserverclient21     | The client-shared library. The version is incremented when there is an ABI change that requires software using the client library to be recompiled or its source code modified. |