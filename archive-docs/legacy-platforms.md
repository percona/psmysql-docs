# Legacy Platform Information - Red Hat Enterprise Linux 7

## Limitations

The RPM packages for Red Hat Enterprise Linux 7 and the compatible derivatives do not support TLSv1.3. This version requires OpenSSL 1.1.1, which is currently unavailable on this platform.

**Note:** Red Hat Enterprise Linux 7 reached End of Life (EOL) on June 30, 2024. This information is archived for historical reference.

## Install on Red Hat 7

The first command uses `yum` to install the Percona repository from the Percona website. The second command enables the `ps-80` release series of the Percona Server. The third command allows the `tools` repository. This repository contains additional Percona software. The fourth command installs Percona Server for MySQL.

```{.bash data-prompt="$"}
$ sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
$ sudo percona-release enable-only ps-80 release
$ sudo percona-release enable tools release
$ sudo yum install percona-server-server
```

