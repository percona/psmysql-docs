# Use an APT repository to install Percona Server for MySQL {{vers}}

Ready-to-use packages are available from the Percona Server for MySQL software repositories and the [Percona downloads :octicons-link-external-16:](https://www.percona.com/downloads/Percona-Server-{{vers}}/) page.

The [Percona Software and Platform Lifecycle :octicons-link-external-16:](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql) page lists supported platforms, products, and versions. Debian (DEB) packages support `arm64` and other architectures across the documented Debian and Ubuntu releases.

--8<-- "percona-release.md"

We gather [Telemetry data] in the Percona packages and Docker images.

--8<--- "get-help-snip.md"

## Install Percona Server for MySQL using APT

To install Percona Server on Debian or Ubuntu, follow these steps:

1. Copy the command block in the following section and run the commands in order.

2. Use [Configure authentication](#configure-authentication) when the package manager prompts for authentication options.

3. Open [Next steps](#next-steps) to secure and configure the instance after the server packages install.

4. Expand the `Step-by-step: what each command does` note for an explanation of each command.

5. Use [Non-interactive installs and debconf](#non-interactive-installs-and-debconf) and [Unattended installations](#unattended-installations) only for scripted automation.

Run the following commands as a `root` user or with sudo:

```shell
sudo apt update
sudo apt install -y curl
curl -O https://repo.percona.com/apt/percona-release_latest.generic_all.deb
sudo apt install -y gnupg2 lsb-release ./percona-release_latest.generic_all.deb
sudo percona-release setup {{pkg}} --scheme https
sudo percona-release enable {{pkg}} release --scheme https
sudo apt update
sudo apt install -y percona-server-server
```

The command sequence matches [Install Percona Server for MySQL and create a database on Ubuntu](quickstart-apt.md). The quickstart covers installation steps one through six and includes `--scheme https` on `percona-release setup` and `enable`. The repository identifier for {{vers}} is `{{pkg}}`.

For another Percona Server for MySQL series, use the name shown by `sudo percona-release list`, or consult the [MySQL software repositories :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/mysql.html) reference. Published names can change as Percona adds new series.

??? note "`percona-release` flag: `--scheme`"

	The command examples on this page pass `--scheme https` so repository URLs in APT source lists use HTTPS. The [Percona Software Repositories — `percona-release` :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/percona-release.html) reference documents the `--scheme` flag. Supported values are HTTP and HTTPS. Without `--scheme`, `percona-release` defaults to HTTP URLs.

	You can add `--scheme https` to subcommands such as `setup`, `enable`, `enable-only`, or `disable` following the same pattern as the examples. See the linked documentation for the full command reference.

Percona Server for MySQL {{vers}} follows the MySQL 9.x authentication model documented for [MySQL 9.6 :octicons-link-external-16:](https://dev.mysql.com/doc/refman/9.6/en/). Key behaviors include the following:

- The `default_authentication_plugin` system variable is not available.

- MySQL removes the `mysql_native_password` plugin in the 9.x series.

- MySQL 9.x removes the server-side native-password option.

- New accounts use the `caching_sha2_password` plugin.

- Applications and drivers must support `caching_sha2_password`.

- TLS is required only when a security policy or deployment mandates encrypted traffic. The `caching_sha2_password` plugin does not require TLS for every connection type.

When the package manager prompts during installation, follow the steps in [Configure authentication](#configure-authentication). Prompt behavior depends on the package and distribution.

??? note "Step-by-step: what each command does"

	The following sections provide detailed explanations for each step:

	1. The following `apt update` command updates the package lists for upgrades and package installations. `sudo` runs the command with superuser privileges. `apt update` resynchronizes the package index files from the sources configured in `/etc/apt/sources.list` and `/etc/apt/sources.list.d/`.

		```shell
		sudo apt update
		```

	2. The `sudo apt install -y curl` command installs the `curl` package. `curl` is a command-line tool used to transfer data over networks and is required to download the Percona repository package.

		```shell
		sudo apt install -y curl
		```

	3. The following `curl -O` command downloads the `percona-release_latest.generic_all.deb` file from the Percona APT repository. The `-O` option saves the file with the same name as in the URL.

		```shell
		curl -O https://repo.percona.com/apt/percona-release_latest.generic_all.deb
		```

	4. The `sudo apt install -y gnupg2 lsb-release ./percona-release_latest.generic_all.deb` command installs `gnupg2` (for package signature verification), `lsb-release` (for distribution information), and the downloaded Percona release package. Together, `gnupg2`, `lsb-release`, and the Percona release `.deb` configure the Percona APT repository on your system.

		```shell
		sudo apt install -y gnupg2 lsb-release ./percona-release_latest.generic_all.deb
		```

	5. The `percona-release setup {{pkg}} --scheme https` command disables all current Percona repositories on the system. The command then enables the release repositories matching Percona Server for MySQL {{vers}} for your distribution over HTTPS. See the [Percona Software Repositories :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/percona-release.html) reference. Omit `--scheme https` only when you require HTTP repository URLs, which is the `percona-release` default.

		```shell
		sudo percona-release setup {{pkg}} --scheme https
		```

	6. The `percona-release enable {{pkg}} release --scheme https` command enables the Percona Server for MySQL release repository with HTTPS URLs. Run `apt update` afterward so APT loads package indexes for the Percona APT repository, including `percona-server-server` and related packages.

		```shell
		sudo percona-release enable {{pkg}} release --scheme https
		sudo apt update
		```

	7. Verify the repository configuration by inspecting the `.list` files under `/etc/apt/sources.list.d/`. The exact filename, such as `percona-original-release.list`, depends on the `percona-release` version.

	8. The `sudo apt install -y percona-server-server` command installs the `percona-server-server` package. During installation, the package manager may prompt for configuration values such as the `root` password. Some builds use debconf or post-install configuration only. For password prompts and automation, see [Non-interactive installs and debconf](#non-interactive-installs-and-debconf). For account authentication defaults and removed plugins, see [Configure authentication](#configure-authentication).

		```shell
		sudo apt install -y percona-server-server
		```

### Configure authentication

The package manager may prompt for passwords or other options during installation. Adjust authentication after installation when the package skips prompts. Review the package manager output and [Non-interactive installs and debconf](#non-interactive-installs-and-debconf) when automating.

!!! warning "Important change in {{vers}}"

	Percona Server for MySQL {{vers}} inherits MySQL 9.x behavior. The `mysql_native_password` plugin is removed. The `default_authentication_plugin` system variable is no longer used. Default authentication uses `caching_sha2_password`.

	When migrating from a server that used native password authentication, update accounts and clients before deploying {{vers}}. See [Authentication methods](authentication-methods.md) and [Upgrade checklist for {{vers}}](upgrade-checklist-9.7.md).

For new installations on {{vers}}, the server uses the `caching_sha2_password` plugin for password-based authentication. Ensure your client libraries and connectors support the `caching_sha2_password` plugin and TLS when required. The default `caching_sha2_password` configuration requires no additional server settings.

See [Configuring Percona repositories with `percona-release` :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/percona-release.html) for more information.

--8<--- "storage-engines.md"

## Next steps

After installation completes, see [Post-installation](post-installation.md) for steps to configure and secure your Percona Server for MySQL installation.

## Non-interactive installs and debconf

Adding `-y` to `apt install` only skips APT confirmation prompts. The `percona-server-server` packages still run maintainer scripts that may ask debconf questions. Common prompts include the following:

- The MySQL `root` password

- Whether to reuse an existing data directory

- Lowercase table names

The exact prompts depend on the `percona-server-server` package version and the data already present on the disk.

### Lab baseline and validating debconf on your OS

Debconf template names and valid answers depend on the Linux distribution, the release (for example, 22.04 compared with 24.04), and the exact `percona-server-server` package version. Template names do not depend on the Percona Server {{vers}} product line alone.

Solution: Treat every preseed example in this section as illustrative until you confirm the keys on a disposable host that matches production.

1. Pick a reference lab image that mirrors production. Match the `.list` repositories, the distribution release, and the architecture. The following examples were drafted against Ubuntu 22.04 LTS (Jammy) and Percona Server for MySQL {{vers}} packages from the Percona APT repository. On Debian, Ubuntu 24.04 LTS, or another SKU, keys can differ or additional questions can appear.

2. On the lab host, or on a CI image built the same way, install the package version you plan to use in production, then capture the output:

	```shell
	lsb_release -a
	dpkg-query -W percona-server-server
	sudo debconf-show percona-server-server | tee debconf-percona-server-server.txt
	```

	Archive `debconf-percona-server-server.txt` next to your automation, such as Ansible or cloud-init. Run the capture again after any base-image or package upgrade.

3. For automation, pin the `percona-server-server` version or document the build ID from `dpkg-query`. Pinning keeps preseed scripts tied to a known `debconf-show` result.

To automate those prompts:

1. Discover the questions your package version uses. On a lab host, install once interactively or inspect templates, then run:

	```shell
	sudo debconf-show percona-server-server
	```

	The package also ships template definitions at paths such as `/var/lib/dpkg/info/percona-server-server.templates`.

	Verify the templates for each target. Preseed names and choices can differ by distribution, point release, and `percona-server-server` package version. Re-run `debconf-show` after upgrades or after a base-image change. For production automation, keep a checklist that maps distribution and package version to the saved `debconf-show` output. The checklist keeps scripts aligned with the package prompts.

2. Preseed answers with `debconf-set-selections` before `apt install`. The templates shipped with many Percona Server for MySQL {{vers}} packages use the `percona-server-server/root-pass` and `percona-server-server/re-root-pass` names for password prompts. For example:

	```shell
	echo "percona-server-server percona-server-server/root-pass password <strong-password>" | sudo debconf-set-selections
	echo "percona-server-server percona-server-server/re-root-pass password <strong-password>" | sudo debconf-set-selections
	```

	Other prompts, such as `percona-server-server/lowercase-table-names` or `percona-server-server/remove-data-dir`, appear only in some upgrade or edge-case paths. Use the `debconf-show` output to add matching lines. Do not commit real passwords to version control or broad shell history.

3. Optional: set `DEBIAN_FRONTEND=noninteractive` for the `percona-server-server` install so debconf does not open a UI. Combine non-interactive installs with preseeding. Without defaults for required questions, the Debian package `configure` step can fail or leave the server in an unexpected state.

	```shell
	sudo DEBIAN_FRONTEND=noninteractive apt install -y percona-server-server
	```

#### Default authentication plugin

When a distribution or package adds a debconf choice related to authentication, the prompt appears in `debconf-show` output for `percona-server-server`. On {{vers}}, native-password authentication is not available. Unattended installs must assume `caching_sha2_password` and client compatibility as described in [Configure authentication](#configure-authentication).

### See also

- [Telemetry](telemetry.md) — disable collection for package installs with `PERCONA_TELEMETRY_DISABLE=1` on the same `apt` command line

- [Authentication methods](authentication-methods.md) — `caching_sha2_password` and related settings

- [Post-installation](post-installation.md) — secure and configure the server after packages install

- [Debian Wiki — debconf :octicons-link-external-16:](https://wiki.debian.org/debconf) — how debconf and preseeding work on Debian-derived systems

## Unattended installations

Use the same `apt` and `percona-release` sequence shown in [Install Percona Server for MySQL using APT](#install-percona-server-for-mysql-using-apt). Add `-y` to each `sudo apt install` line that needs non-interactive APT confirmations. Use non-interactive options for `percona-release` as shown in the following snippet.

--8<-- "install-flag.md"

## Install Percona Toolkit UDFs (optional)

User-defined functions (UDFs) extend MySQL with custom functions. Percona Server for MySQL includes UDFs from [Percona Toolkit :octicons-link-external-16:](https://docs.percona.com/percona-toolkit/) for data integrity checks and performance monitoring. These UDFs provide faster checksum calculations:

| Function | Description |
|---|---|
| `fnv_64` | Fast 64-bit hash function |
| `fnv1a_64` | Variant of `fnv_64` with improved distribution |
| `murmur_hash` | High-performance non-cryptographic hash function |

To install the Percona Toolkit UDFs after the Percona Server packages are installed:

```{.sql data-prompt="mysql>"}
INSTALL COMPONENT 'file://component_percona_udf';
```

??? example "Expected output"

	```{.text .no-copy}
	Query OK, 0 rows affected (0.01 sec)
	```

You can now use the UDFs in your SQL queries. For example: `SELECT fnv_64('test_string');`

For detailed information about the UDFs, see [Percona Toolkit UDF functions](udf-percona-toolkit.md).

## Install the Percona testing repository using APT

Percona offers pre-release builds from the testing repository. As a superuser, run `percona-release` with the `testing` argument to enable the testing repository:

```shell
sudo percona-release enable {{pkg}} testing --scheme https
```

Do not run testing repository builds in production. The build may not contain all the features available in the final release and may change without notice.

[Telemetry data]: telemetry.md
