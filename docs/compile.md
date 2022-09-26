# Compiling Percona Server for MySQL from Source

After either fetching the source repository or extracting a source tarball
(from Percona or one you generated yourself), you must
configure and build Percona Server. Do the following:

1. Run `cmake` to configure the build. Specify the
build options like you would for a [MySQL build](https://dev.mysql.com/doc/mysql-sourcebuild-excerpt/5.7/en/installing-source-distribution.html). You may require other options on your sever. 

   This example configures _Percona Server for 
   MySQL_ with similar options to what Percona uses to produce the 
   binaries:

```shell
$ cmake . -DCMAKE_BUILD_TYPE=RelWithDebInfo -DBUILD_CONFIG=mysql_release -DFEATURE_SET=community -DWITH_EMBEDDED_SERVER=OFF
```

Second, compile using `make`:

```shell
$ make
```

Third, install the compiled file:

```shell
$ make install
```
Percona Server 5.7 is installed on your system.
