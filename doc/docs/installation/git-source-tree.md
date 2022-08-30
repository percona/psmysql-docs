
# Installing Percona Server for MySQL 5.7 from the Git Source Tree

!!! note

    The following instructions install Percona Server for MySQL 5.7 from the Git Source tree. 
    The instruction to install the [Percona Server for MySQL 8.0 from a Git Source tree are available in this location](https://docs.percona.com/percona-server/latest/installation.html#source-from-git).

Percona uses the [GitHub](http://github.com/) revision
control system for development. To build the latest *Percona Server for MySQL*
from the source tree you must have `git` installed on your system.

You can now fetch the latest *Percona Server for MySQL* 5.7 sources.

```shell
$ git clone https://github.com/percona/percona-server.git
$ cd percona-server
$ git checkout 5.7
$ git submodule init
$ git submodule update
```

If you are going to be making changes to *Percona Server for MySQL* 5.7 and wanting
to distribute the resulting work, generate a new source tarball, which 
is process we follow for release:

```
$ cmake .
$ make dist
```

Follow the instructions in [Compiling Percona Server for MySQL from 
Source](compile.md).
