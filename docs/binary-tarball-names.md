# Binary tarball file names available based on the Percona Server for MySQL version 

For later version of Percona Server for MySQL, the tar files are organized by the `glibc2` version. You can find this version on your operating system with the following command:

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


=== "8.0.26-16 and later"

    The following lists the platform and the associated full binary file name used by Percona Server for MySQL tar files from version 8.0.26-16 and later.

    | Platform             | Percona Server for MySQL tarball name                    | glibc2 version |
    |----------------------|--------------------------------------------------------------|---|
    | Ubuntu 22.04         | Percona-Server-8.0.30-22-Linux.x86_64.glibc2.35-zenfs.tar.gz | glibc2.35 |
    | Ubuntu 20.04         | Percona-Server-8.0.30-22-Linux.x86_64.glibc2.31.tar.gz       | glibc2.31 |
    | Ubuntu 18.04         | Percona-Server-8.0.30-22-Linux.x86_64.glibc2.27.tar.gz       | glibc2.27 |
    | Red Hat Enterprise 9 | Percona-Server-8.0.30-22-Linux.x86_64.glibc2.34.tar.gz       | glibc2.34 |
    | Red Hat Enterprise 8 | Percona-Server-8.0.30-22-Linux.x86_64.glibc2.28.tar.gz       | glibc2.28 |
    | Red Hat Enterprise 7 | Percona-Server-8.0.30-22-Linux.x86_64.glibc2.17.tar.gz       | glibc2.17 |
    | Red Hat Enterprise 6 | Percona-Server-8.0.20-11-Linux.x86_64.glibc2.12.tar.gz       | glibc2.12 |

    The types of files are as follows:

    | Type | Name | Description |
    |---|---|---|
    | Full | Percona-Server-<version-number>-Linux.x86_64.<glibc2-version>.tar.gz | Contains all files available |
    | Minimal | Percona-Server-&lt;version-number&gt;-Linux.x86_64.&lt;glibc2-version&gt;.minimal.tar.gz | Contains binaries and libraries |
    | Debug | Percona-Server-&lt;version-number&gt;-Linux.x86_64.&lt;glibc2-version&gt;.debug.tar.gz | Contains the minimal build files and test files, and debug symbols |
    | Zenfs | Percona-Server-&lt;version-number&gt;-Linux.x86_64.&lt;glibc2-version&gt;-zenfs.tar.gz | Contains the zenfs files and can be either a full or minimal installation |

=== "8.0.20-11 to 8.0.25-17"

    The multiple binary tarballs from earlier versions are replaced with the following:

    | Type    | Name                                                                        | Operating systems                                                  | Description                                                                       |
    |---------|-----------------------------------------------------------------------------|--------------------------------------------------------------------|-----------------------------------------------------------------------------------|
    | Full    | Percona-Server-&lt;version number&gt;-Linux.x86_64.glibc2.12.tar.gz         | Built for CentOS 6                                                 | Contains binaries, libraries, test files, and debug symbols                       |
    | Minimal | Percona-Server-&lt;version number&gt;-Linux.x86_64.glibc2.12-minimal.tar.gz | Built for CentOS 6                                                 | Contains binaries and libraries but does not include test files, or debug symbols |
    | Full    | Percona-Server-&lt;version number&gt;-Linux.x86_64.glibc2.17.tar.gz         | Compatible with any supported operating system except for CentOS 6 | Contains binaries, libraries, test files, and debug symbols                       |
    | Minimal | Percona-Server-&lt;version number&gt;-Linux.x86_64.glibc2.17-minimal.tar.gz | Compatible with any supported operating system except for CentOS 6 | Contains binaries and libraries but does not include test files or debug symbols  |

    The tarball file has the following characteristics:

    | Type | Name | Description |
    |---|---|---|
    | Full | Percona-Server-<version-number>-Linux.x86_64.<glibc2-version>.tar.gz | Contains all files available |
    | Minimal | Percona-Server-&lt;version-number&gt;-Linux.x86_64.&lt;glibc2-version&gt;.minimal.tar.gz | Contains binaries and libraries |
    | Debug | Percona-Server-&lt;version-number&gt;-Linux.x86_64.&lt;glibc2-version&gt;.debug.tar.gz | Contains the minimal build files and test files, and debug symbols |

=== "8.0.19-10 and earlier"

    For *Percona Server for MySQL* 8.0.19-10 and earlier, multiple tarballs are provided based on the *OpenSSL* library available in the distribution:

      * ssl100 - for *Debian* prior to 9 and *Ubuntu* prior to 14.04 versions (`libssl.so.1.0.0 => /usr/lib/x86_64-linux-gnu/libssl.so.1.0.0`);

      * ssl102 - for *Debian* 9 and *Ubuntu* versions starting from 14.04 (`libssl.so.1.1 => /usr/lib/libssl.sl.1.1`)

      * ssl101 - for *CentOS* 6 and *CentOS* 7 (`libssl.so.10 => /usr/lib64/libssl.so.10`);

      * ssl102 - for *CentOS* 8 and *RedHat* 8  (`libssl.so.1.1 => /usr/lib/libssl.so.1.1.1b`);

