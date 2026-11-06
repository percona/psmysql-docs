# Binary tarball file names available based on the Percona Server for MySQL version 

For later of Percona Server for MySQL, the tar files are organized by the `glibc2` version. You can find this version on your operating system with the following command:

```shell
ldd --version
```

??? example "Expected output"
    ```{.text .no-copy}
    ldd (Ubuntu GLIBC 2.35-0ubuntu3.1) 2.35
    Copyright (C) 2022 Free Software Foundation, Inc.
    This is free software; see the source for copying conditions.  There is NO
    warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    Written by Roland McGrath and Ulrich Drepper.
    ```

The first line of the output ends with the glibc version. Select the tarball with that glibc version. If Percona does not publish that version, select the newest published glibc version that is older than yours. A tarball built for an older glibc runs on a newer glibc. If every published tarball is newer than your glibc, Percona Server for MySQL does not support the operating system.

Run the following command to find the CPU architecture, and select the matching tarball. The example on the install page uses `x86_64`:

```shell
uname -m
```

Generic binary tarballs are built for `x86_64`. If this command prints `aarch64`, Percona does not publish a tarball for that CPU. Use an [APT](apt-repo.md) or [DNF](yum-repo.md) package, a [Docker](docker.md) image with the `{{arm_tag}}` tag, or [compile from source](compile-percona-server.md).

Ubuntu 26.04 reports glibc 2.43. Use the glibc 2.35 tarball on that release. The steps are on the [Install from a binary tarball](binary-tarball-install.md) page.

The tarball links shared libraries from the operating system it was built on. Package names for those libraries are on the [Operating system libraries](os-libraries.md) page.

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
| Full | Percona-Server-&lt;version-number&gt;-Linux.x86_64.&lt;glibc2-version&gt;.tar.gz | Contains all files available |
| Minimal | Percona-Server-&lt;version-number&gt;-Linux.x86_64.&lt;glibc2-version&gt;.minimal.tar.gz | Contains binaries and libraries |
| Debug | Percona-Server-&lt;version-number&gt;-Linux.x86_64.&lt;glibc2-version&gt;.debug.tar.gz | Contains the minimal build files and test files, and debug symbols |
