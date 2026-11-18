> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Install Percona Server for MySQL 9.7 using downloaded DEB packages

Download the packages from [Percona Product Downloads](https://www.percona.com/downloads) . If needed, [Instructions for the Percona Product Download](https://docs.percona.com/percona-server/9.7/download-instructions.html) are available.

The following example downloads *Percona Server for MySQL* 9.7.2-3 release `x86_64` packages for Debian 13 (`trixie`). For other distributions, replace `trixie` with the codename of your distribution, for example, `bookworm` or `noble`.

1. Use `wget` to download the tar file:

   The download filename includes a `<revision-identifier>` value. This value is *build-specific* and must be obtained from the [Percona Product Downloads](https://www.percona.com/downloads) page for the exact release you are installing. Select the product, version, and operating system, and find the link with the required `<revision identifier>` under the **Download all packages** button. For more details, see the [Instructions for Percona Product Downloads](https://docs.percona.com/percona-server/9.7/download-instructions.html).

   ```
   wget https://downloads.percona.com/downloads/Percona-Server-9.7/Percona-Server-9.7.2-3/binary/debian/trixie/x86_64/Percona-Server-9.7.2-3-<revision-identifier>-trixie-x86_64-bundle.tar
   ```

1. Unpack the download to get the packages:

   ```
   tar xvf Percona-Server-9.7.2-3-<revision-identifier>-trixie-x86_64-bundle.tar
   ```

   Expected output

   ```
   libperconaserverclient24-dbgsym_9.7.2-3-1.trixie_amd64.deb
   libperconaserverclient24-dev-dbgsym_9.7.2-3-1.trixie_amd64.deb
   libperconaserverclient24-dev_9.7.2-3-1.trixie_amd64.deb
   libperconaserverclient24_9.7.2-3-1.trixie_amd64.deb
   percona-client_9.7.2-3-1.trixie_amd64.deb
   percona-mysql-router-dbgsym_9.7.2-3-1.trixie_amd64.deb
   percona-mysql-router_9.7.2-3-1.trixie_amd64.deb
   percona-server-client-core-dbgsym_9.7.2-3-1.trixie_amd64.deb
   percona-server-client-core_9.7.2-3-1.trixie_amd64.deb
   percona-server-client-dbgsym_9.7.2-3-1.trixie_amd64.deb
   percona-server-client-plugins-dbgsym_9.7.2-3-1.trixie_amd64.deb
   percona-server-client-plugins_9.7.2-3-1.trixie_amd64.deb
   percona-server-client_9.7.2-3-1.trixie_amd64.deb
   percona-server-common_9.7.2-3-1.trixie_amd64.deb
   percona-server-js-dbgsym_9.7.2-3-1.trixie_amd64.deb
   percona-server-js_9.7.2-3-1.trixie_amd64.deb
   percona-server-rocksdb-dbgsym_9.7.2-3-1.trixie_amd64.deb
   percona-server-rocksdb_9.7.2-3-1.trixie_amd64.deb
   percona-server-server-core-dbgsym_9.7.2-3-1.trixie_amd64.deb
   percona-server-server-core_9.7.2-3-1.trixie_amd64.deb
   percona-server-server_9.7.2-3-1.trixie_amd64.deb
   percona-server-source_9.7.2-3-1.trixie_amd64.deb
   percona-server-test-dbgsym_9.7.2-3-1.trixie_amd64.deb
   percona-server-test_9.7.2-3-1.trixie_amd64.deb
   percona-server_9.7.2-3-1.trixie_amd64.deb
   percona-testsuite_9.7.2-3-1.trixie_amd64.deb
   ```

1. Download the `percona-telemetry-agent` package into the same directory. The `percona-server-server` package depends on `percona-telemetry-agent`, which is not included in the bundle and is not available in the distribution repositories. Find the package for your distribution in the [Percona telemetry repository](https://repo.percona.com/telemetry/apt/pool/main/p/percona-telemetry-agent/) . For example, for Debian 13:

   ```
   wget https://repo.percona.com/telemetry/apt/pool/main/p/percona-telemetry-agent/percona-telemetry-agent_1.0.17-1.trixie_amd64.deb
   ```

1. Install the packages with `apt`. Run this command as root or use the sudo command:

   ```
   sudo apt install ./*.deb
   ```

   `apt` installs the local packages and resolves the remaining dependencies, such as `libaio1t64`, `libatomic1`, `libmecab2`, `libnuma1`, and `zlib1g-dev` on Debian 13, from the distribution repositories.

Warning

Do not install the bundle with `sudo dpkg -i *.deb`. `dpkg` does not resolve dependencies and leaves the server packages unconfigured. If that happens, do not run `apt -f install` (`apt --fix-broken install`): without `percona-telemetry-agent` available, it removes `percona-server-server` and the packages that depend on it.
