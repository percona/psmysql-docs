# Compile Percona Server for MySQL 8.0 from source

The following instructions install Percona Server for MySQL 8.0.

## Install Percona Server for MySQL from the Git Source Tree

Percona uses the [Github](https://github.com/) revision
control system for development. To build the latest Percona Server for MySQL
from the source tree, you will need `git` installed on your system.

You can now fetch the latest Percona Server for MySQL 8.0 sources.

```{.bash data-prompt="$"}
$ git clone https://github.com/percona/percona-server.git
$ cd percona-server
$ git checkout 8.0
$ git submodule init
$ git submodule update
```

If you are going to be making changes to Percona Server for MySQL 8.0 and wanting
to distribute the resulting work, you can generate a new source tarball
(exactly the same way as we do for release):

```{.bash data-prompt="$"}
$ cmake .
$ make dist
```

After either fetching the source repository or extracting a source tarball
(from Percona or one you generated yourself), you will now need to
configure and build Percona Server for MySQL.

First, run CMake to configure the build. Here you can specify all the normal
build options as you do for a normal MySQL build. Depending on what
options you wish to compile Percona Server for MySQL with, you may need other
libraries installed on your system. Here is an example using a
configure line similar to the options that Percona uses to produce
binaries:

```{.bash data-prompt="$"}
$ cmake . -DCMAKE_BUILD_TYPE=RelWithDebInfo -DBUILD_CONFIG=mysql_release -DFEATURE_SET=community
```

## Compile from source

Now, compile using make:

```{.bash data-prompt="$"}
$ make
```

Install:

```{.bash data-prompt="$"}
$ make install
```

Percona Server for MySQL 8.0 is installed on your system.
