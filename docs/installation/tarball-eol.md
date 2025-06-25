# Download a {{eol}} binary tarball

Percona Server for MySQL {{release}} contains fixes as part of the [MySQL 5.7 post-EOL support from Percona program], available to customers. Community members can [compile and install from source code](git-source-tree.md) from publicly available source code, which is released quarterly.

As a Percona customer, request access to the Percona 5.7 Post-EOL repository from [Percona Support](https://www.percona.com/services/support/mysql-support) and receive your `CLIENTID` and `TOKEN`. Use these credentials to download the appropriate binary tarball.

| Type    | Name                                                                |Description         |
|---------|---------------------------------------------------------------------|--------------------|
| Full    | https://repo.percona.com/private/[CLIENTID-[TOKEN]/ps-57-eol/tarballs/Percona-Server-&lt;release&gt;/binary/tarball/Percona-Server-&lt;release&gt;-Linux.x86_64.glibc2.17.tar.gz   | Contains binaries, libraries, test files, and debug symbols   |
| Minimal | https://repo.percona.com/private/[CLIENTID-[TOKEN]/ps-57-eol/tarballs/Percona-Server-&lt;release&gt;-Linux.x86_64.glibc2.12-minimal.tar.gz | Contains binaries, and libraries but does not include test files, or debug symbols. |

Fetch and extract the correct binary tarball using your `CLIENTID` and `TOKEN`. For example, for Oracle Linux 9, use the following command:

```{.bash data-prompt="$"}
 $ wget https://repo.percona.com/private/[CLIENTID-[TOKEN]/Percona-Server-5.7/Percona-Server-{{release}}/binary/tarball/Percona-Server-{{release}}-Linux.x86_64.glibc2.17.tar.gz 
```

[MySQL 5.7 post-EOL support from Percona program]: https://www.percona.com/post-mysql-5-7-eol-support