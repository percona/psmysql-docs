# Install Percona Server for MySQL {{vers}} using downloaded DEB packages

Download the packages from [Percona Product Downloads :octicons-link-external-16:](https://www.percona.com/downloads). If needed, [Instructions for the Percona Product Download](download-instructions.md) are available.

The following example downloads *Percona Server for MySQL* {{release}} release `x86_64` packages for Debian 13 (`trixie`). For other distributions, replace `trixie` with the codename of your distribution, for example, `bookworm` or `noble`.
{.power-number}

1. Use `wget` to download the tar file:

    The download filename includes a `<revision-identifier>` value. This value is *build-specific* and must be obtained from the [Percona Product Downloads :octicons-link-external-16:](https://www.percona.com/downloads) page for the exact release you are installing. Select the product, version, and operating system, and find the link with the required `<revision identifier>` under the **Download all packages** button. For more details, see the [Instructions for Percona Product Downloads](download-instructions.md).

    ```shell
    wget https://downloads.percona.com/downloads/Percona-Server-{{vers}}/Percona-Server-{{release}}/binary/debian/trixie/x86_64/Percona-Server-{{release}}-<revision-identifier>-trixie-x86_64-bundle.tar
    ```

2. Unpack the download to get the packages:

    ```shell
    tar xvf Percona-Server-{{release}}-<revision-identifier>-trixie-x86_64-bundle.tar
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        libperconaserverclient24-dbgsym_{{release}}-1.trixie_amd64.deb
        libperconaserverclient24-dev-dbgsym_{{release}}-1.trixie_amd64.deb
        libperconaserverclient24-dev_{{release}}-1.trixie_amd64.deb
        libperconaserverclient24_{{release}}-1.trixie_amd64.deb
        percona-client_{{release}}-1.trixie_amd64.deb
        percona-mysql-router-dbgsym_{{release}}-1.trixie_amd64.deb
        percona-mysql-router_{{release}}-1.trixie_amd64.deb
        percona-server-client-core-dbgsym_{{release}}-1.trixie_amd64.deb
        percona-server-client-core_{{release}}-1.trixie_amd64.deb
        percona-server-client-dbgsym_{{release}}-1.trixie_amd64.deb
        percona-server-client-plugins-dbgsym_{{release}}-1.trixie_amd64.deb
        percona-server-client-plugins_{{release}}-1.trixie_amd64.deb
        percona-server-client_{{release}}-1.trixie_amd64.deb
        percona-server-common_{{release}}-1.trixie_amd64.deb
        percona-server-js-dbgsym_{{release}}-1.trixie_amd64.deb
        percona-server-js_{{release}}-1.trixie_amd64.deb
        percona-server-rocksdb-dbgsym_{{release}}-1.trixie_amd64.deb
        percona-server-rocksdb_{{release}}-1.trixie_amd64.deb
        percona-server-server-core-dbgsym_{{release}}-1.trixie_amd64.deb
        percona-server-server-core_{{release}}-1.trixie_amd64.deb
        percona-server-server_{{release}}-1.trixie_amd64.deb
        percona-server-source_{{release}}-1.trixie_amd64.deb
        percona-server-test-dbgsym_{{release}}-1.trixie_amd64.deb
        percona-server-test_{{release}}-1.trixie_amd64.deb
        percona-server_{{release}}-1.trixie_amd64.deb
        percona-testsuite_{{release}}-1.trixie_amd64.deb
        ```

3. Download the `percona-telemetry-agent` package into the same directory. The `percona-server-server` package depends on `percona-telemetry-agent`, which is not included in the bundle and is not available in the distribution repositories. Find the package for your distribution in the [Percona telemetry repository :octicons-link-external-16:](https://repo.percona.com/telemetry/apt/pool/main/p/percona-telemetry-agent/). For example, for Debian 13:

    ```shell
    wget https://repo.percona.com/telemetry/apt/pool/main/p/percona-telemetry-agent/percona-telemetry-agent_1.0.17-1.trixie_amd64.deb
    ```

4. Install the packages with `apt`. Run this command as root or use the sudo command:

    ```shell
    sudo apt install ./*.deb
    ```

    `apt` installs the local packages and resolves the remaining dependencies, such as `libaio1t64`, `libatomic1`, `libmecab2`, `libnuma1`, and `zlib1g-dev` on Debian 13, from the distribution repositories.

!!! warning

    Do not install the bundle with `sudo dpkg -i *.deb`. `dpkg` does not resolve dependencies and leaves the server packages unconfigured. If that happens, do not run `apt -f install` (`apt --fix-broken install`): without `percona-telemetry-agent` available, it removes `percona-server-server` and the packages that depend on it.
