<!--- Check wheher the info is actual ----->

# Binary tarball file names available based on the Percona Server for MySQL version 

For later of Percona Server for MySQL, the tar files are organized by the `glibc2` version. You can find this version on your operating system with the following command:

```{.bash data-prompt="$"}
$ ldd --version
```

??? example "Expected output"
    ```text
    ldd (Ubuntu GLIBC 2.35-0ubuntu3.1) 2.35
    Copyright (C) 2022 Free Software Foundation, Inc.
    This is free software; see the source for copying conditions.  There is NO
    warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    Written by Roland McGrath and Ulrich Drepper.
    ```

If the `glibc2` version from your operating system is not listed, then this Percona Server for MySQL version does not support that operating system.

## Binary tarball file name organization

The following lists the platform and the associated full binary file name used by Percona Server for MySQL tar files {{release}}.

| Platform             | Percona Server for MySQL tarball name                   | glibc2 version |
|----------------------|--------------------------------------------------------------|-----------|
| Ubuntu 22.04         | Percona-Server-{{release}}-Linux.x86_64.glibc2.35.tar.gz     | glibc2.35 |
| Ubuntu 20.04         | Percona-Server-{{release}}-Linux.x86_64.glibc2.31.tar.gz     | glibc2.31 |
| Red Hat Enterprise 9 | Percona-Server-{{release}}-Linux.x86_64.glibc2.34.tar.gz     | glibc2.34 |
| Red Hat Enterprise 8 | Percona-Server-{{release}}-Linux.x86_64.glibc2.28.tar.gz     | glibc2.28 |
| Red Hat Enterprise 7 | Percona-Server-{{release}}-Linux.x86_64.glibc2.17.tar.gz     | glibc2.17 |

The types of files are as follows:

| Type | Name | Description |
|---|---|---|
| Full | Percona-Server-<version-number>-Linux.x86_64.<glibc2-version>.tar.gz | Contains all files available |
| Minimal | Percona-Server-&lt;version-number&gt;-Linux.x86_64.&lt;glibc2-version&gt;.minimal.tar.gz | Contains binaries and libraries |
| Debug | Percona-Server-&lt;version-number&gt;-Linux.x86_64.&lt;glibc2-version&gt;.debug.tar.gz | Contains the minimal build files and test files, and debug symbols |
