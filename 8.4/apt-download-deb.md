> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# Install Percona Server for MySQL 8.4 using downloaded DEB packages

Download the packages from [Percona Product Downloads](https://www.percona.com/downloads) . If needed, [Instructions for the Percona Product Download](https://docs.percona.com/percona-server/8.4/download-instructions.md) are available.

The following example downloads *Percona Server for MySQL* 8.4.11-12 release `x86_64` packages for Ubuntu 22.04:

1. Use `wget` to download the tar file:

   The download filename includes a `<revision-identifier>` value. This value is *build-specific* and must be obtained from the [Percona Product Downloads](https://www.percona.com/downloads) page for the exact release you are installing. Select the product, version, and operating system, and find the link with the required `<revision identifier>` under the **Download all packages** button. For more details, see the [Instructions for Percona Product Downloads](https://docs.percona.com/percona-server/8.4/download-instructions.md).

   ```shell
   wget https://downloads.percona.com/downloads/Percona-Server-8.4/Percona-Server-8.4.11-12/binary/debian/jammy/x86_64/Percona-Server-8.4.11-12-<revision-identifier>-jammy-x86_64-bundle.tar
   ```

1. Unpack the download to get the packages:

   ```shell
   tar xvf Percona-Server-8.4.11-12-<revision-identifier>-jammy-x86_64-bundle.tar
   ```

   Expected output

   ```text
   libperconaserverclient21_8.4.11-12-1.buster_amd64.deb
   libperconaserverclient21-dev_8.4.11-12-1.buster_amd64.deb
   percona-mysql-router_8.4.11-12-1.buster_amd64.deb
   percona-server-client_8.4.11-12-1.buster_amd64.deb
   percona-server-common_8.4.11-12-1.buster_amd64.deb
   percona-server-dbg_8.4.11-12-1.buster_amd64.deb
   percona-server-rocksdb_8.4.11-12-1.buster_amd64.deb
   percona-server-server_8.4.11-12-1.buster_amd64.deb
   percona-server-source_8.4.11-12-1.buster_amd64.deb
   percona-server-test_8.4.11-12-1.buster_amd64.deb
   ```

1. Download the `percona-telemetry-agent` package for your distribution into the same directory. The `percona-server-server` package depends on it, but the bundle does not include it, and the distribution repositories do not provide it. For example, for Ubuntu 22.04:

   ```shell
   wget https://repo.percona.com/telemetry/apt/pool/main/p/percona-telemetry-agent/percona-telemetry-agent_1.0.17-1.jammy_amd64.deb
   ```

   For other distributions, replace `jammy` with your distribution codename, for example, `noble` or `bookworm`.

1. Install the packages with `apt`. Run this command as root or use the sudo command:

   ```shell
   sudo apt install ./*.deb
   ```

   Unlike `dpkg -i`, `apt` also installs the required packages from your distribution repositories, for example, `libaio1` (`libaio1t64` on Ubuntu 24.04 and later), `libatomic1`, `libmecab2`, `libnuma1`, and `zlib1g-dev`.

Warning

Do not install the packages with `sudo dpkg -i *.deb`. The `dpkg` tool does not resolve dependencies, so the packages remain unconfigured. Do not try to recover with `sudo apt -f install` (`apt --fix-broken install`) either: if `percona-telemetry-agent` is not available, `apt` fixes the broken state by removing `percona-server-server` and the packages that depend on it.
