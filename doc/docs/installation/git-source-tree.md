
# Installing *Percona Server for MySQL* from the Git Source Tree

Percona uses the [GitHub](http://github.com/) revision
control system for development. To build the latest *Percona Server for MySQL*
from the source tree you must have `git` installed on your system.

You can now fetch the latest *Percona Server for MySQL* 5.7 sources.

```
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

Follow the instructions in Compiling Percona Server for MySQL from 
Source.