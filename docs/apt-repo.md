# Use an APT repository to install Percona Server for MySQL {{vers}}

Ready-to-use packages are available from the Percona Server for MySQL software repositories and the [Percona downloads :octicons-link-external-16:](https://www.percona.com/downloads/Percona-Server-{{vers}}/) page.

Specific information on the supported platforms, products, and versions—including which Debian and Ubuntu releases and CPU architectures (DEB packages include `arm64`, among others)—is described in [Percona Software and Platform Lifecycle :octicons-link-external-16:](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql).

--8<-- "percona-release.md"

We gather [Telemetry data] in the Percona packages and Docker images.

--8<--- "get-help-snip.md"

## Install Percona Server for MySQL using APT

If you are new to installing Percona Server on Debian or Ubuntu, copy the first command block below and run the commands in order. Use [Configure authentication](#configure-authentication) when the installer asks about the default authentication plugin. After the server packages are installed, open [Next Steps](#next-steps) for securing and configuring the instance. Expand the step-by-step section when you want an explanation of each command; use [Non-interactive installs and debconf](#non-interactive-installs-and-debconf) and [Unattended installations](#unattended-installations) only for scripted automation.

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

The command sequence matches [Install Percona Server for MySQL and create a database on Ubuntu](quickstart-apt.md) (installation steps 1–6 there).

??? note "`percona-release` flag: `--scheme`"

	The command examples on the page pass `--scheme https` so repository URLs in APT source lists use HTTPS. The [Percona Software Repositories — `percona-release` :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/percona-release.html) documentation describes the Flags section: the available flag is `--scheme`, with supported values HTTP and HTTPS; without the flag, the tool defaults to HTTP.

	You can add `--scheme https` to subcommands such as `setup`, `enable`, `enable-only`, or `disable` following the same pattern as the examples. See the linked documentation for the full command reference.

Starting in {{vers}}, the `mysql_native_password` plugin is no longer loaded by default. When the package manager may prompt you during installation (depending on the package and distribution), follow the choices and steps in [Configure authentication](#configure-authentication). If you choose legacy authentication but do not enable the plugin in configuration, clients may be unable to connect or the Percona Server service may fail to start.

??? note "Step-by-step: what each command does"

	The following sections provide detailed explanations for each step:

	1. The `apt update` command shown below updates the package lists for upgrades and new package installations. `sudo` runs the command with superuser privileges; `apt update` resynchronizes the package index files from the sources configured in `/etc/apt/sources.list` and `/etc/apt/sources.list.d/`.

		```shell
		sudo apt update
		```

	2. The `sudo apt install -y curl` command installs the `curl` package. `curl` is a command-line tool used to transfer data over networks and is required to download the Percona repository package.

		```shell
		sudo apt install -y curl
		```

	3. The `curl -O` command shown below downloads the `percona-release_latest.generic_all.deb` file from the Percona APT repository. The `-O` option saves the file with the same name as in the URL.

		```shell
		curl -O https://repo.percona.com/apt/percona-release_latest.generic_all.deb
		```

	4. The `sudo apt install -y gnupg2 lsb-release ./percona-release_latest.generic_all.deb` command installs `gnupg2` (for package signature verification), `lsb-release` (for distribution information), and the downloaded Percona release package. Together, `gnupg2`, `lsb-release`, and the Percona release `.deb` configure the Percona APT repository on your system.

		```shell
		sudo apt install -y gnupg2 lsb-release ./percona-release_latest.generic_all.deb
		```

	5. The `percona-release setup {{pkg}} --scheme https` command disables all current Percona repository locations on the system, then enables the release repositories that match Percona Server for MySQL {{vers}} for your distribution over HTTPS (see the [Percona Software Repositories :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/percona-release.html) documentation). Omit `--scheme https` only if you intentionally want HTTP repository URLs (the tool default).

		```shell
		sudo percona-release setup {{pkg}} --scheme https
		```

	6. The `percona-release enable {{pkg}} release --scheme https` command turns on the Percona Server for MySQL release repository location with HTTPS URLs. Run `apt update` afterward so APT loads package indexes for that repository (including `percona-server-server` and related packages).

		```shell
		sudo percona-release enable {{pkg}} release --scheme https
		sudo apt update
		```

	7. You can verify the repository setup by inspecting the `.list` files under `/etc/apt/sources.list.d/` (for example `percona-original-release.list`, depending on your `percona-release` version).

	8. The `sudo apt install -y percona-server-server` command installs the `percona-server-server` package. During installation, the package manager may prompt you to select the default authentication plugin (some builds use only debconf or post-install configuration); follow the [Configure authentication](#configure-authentication) section when a prompt or post-install step applies.

		```shell
		sudo apt install -y percona-server-server
		```

### Configure authentication

During the installation process, the package manager may prompt you to select the default authentication plugin, or you may need to adjust authentication only after install—see your installer output and [Non-interactive installs and debconf](#non-interactive-installs-and-debconf) when automating.

!!! warning "Important change in {{vers}}"

	Percona Server for MySQL {{vers}} inherits the upstream change where the `mysql_native_password` plugin is disabled by default.

=== "Option 1: Recommended (Strong Password Encryption)"

	Select Option 1 if you are setting up a new server or using modern application drivers.

	The recommended option uses the `caching_sha2_password` plugin, providing superior security and performance. No further configuration is required.

=== "Option 2: Legacy (Native Password)"

	Select Option 2 only if you must support legacy applications that cannot be updated.

	If you choose Option 2, you must manually enable the plugin after installation, or the server will fail to authenticate users who rely on native-password authentication.

	1. Open your configuration file (e.g., `/etc/mysql/mysql.conf.d/mysqld.cnf`).

	2. Add the following to the `[mysqld]` section:
		```ini
		[mysqld]
		mysql_native_password=ON
		```

	3. Restart the service:
		```bash
		sudo systemctl restart mysql
		```

See [Configuring Percona repositories with `percona-release` :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/percona-release.html) for more information.

--8<--- "storage-engines.md"

## Next Steps

After successful installation, see [Post-installation](post-installation.md) for detailed steps to configure and secure your Percona Server for MySQL installation.

## Non-interactive installs and debconf

Adding `-y` to `apt install` only skips APT confirmation prompts. The `percona-server-server` packages still run maintainer scripts that may ask debconf questions (for example the MySQL `root` password, whether to reuse an existing data directory, or lowercase table names, depending on your version and what is already on the disk).

To automate those prompts:

1. Discover the questions your package version uses. On a lab host, install once interactively or inspect templates, then run:

	```shell
	sudo debconf-show percona-server-server
	```

	Template definitions are also shipped with the package (paths such as `/var/lib/dpkg/info/percona-server-server.templates`).

	Verify for each target: preseed names and choices can differ by distribution, point release, and `percona-server-server` package version. Re-run `debconf-show` after upgrades or when you change base image. For production automation, keep a short checklist (distro + package version → saved `debconf-show` output) so scripts stay aligned with what the package actually asks.

2. Preseed answers with `debconf-set-selections` before `apt install`. For the templates shipped with many Percona Server for MySQL {{vers}} packages, password prompts use the `percona-server-server/root-pass` and `percona-server-server/re-root-pass` names—for example:

	```shell
	echo "percona-server-server percona-server-server/root-pass password choose-a-strong-secret" | sudo debconf-set-selections
	echo "percona-server-server percona-server-server/re-root-pass password choose-a-strong-secret" | sudo debconf-set-selections
	```

	Other prompts (for example `percona-server-server/lowercase-table-names` or `percona-server-server/remove-data-dir`) appear only in some upgrade or edge-case paths—use `debconf-show` output to add matching lines. Do not commit real passwords to version control or broad shell history.

3. Optional: set `DEBIAN_FRONTEND=noninteractive` for the install so debconf does not try to open a UI. Noninteractive installs are usually combined with preseeding; without defaults for required questions, the configure step can still fail or leave the server in an unexpected state.

	```shell
	sudo DEBIAN_FRONTEND=noninteractive apt install -y percona-server-server
	```

Default authentication plugin: if your distribution or package adds a debconf choice for the authentication plugin, that question shows up under `debconf-show` for `percona-server-server`. If the distribution or package does not add such a question, unattended installs still follow the same rules as an interactive install: use [Configure authentication](#configure-authentication) after the package is installed (for example `mysql_native_password=ON` in `my.cnf` when you need legacy auth).

See also

* [Telemetry](telemetry.md) — disable collection for package installs with `PERCONA_TELEMETRY_DISABLE=1` on the same `apt` command line.
* [Authentication methods](authentication-methods.md) — options for `mysql_native_password`, `caching_sha2_password`, and related settings.
* [Post-installation](post-installation.md) — secure and configure the server after packages are installed.
* [Debian Wiki — debconf :octicons-link-external-16:](https://wiki.debian.org/debconf) — how debconf and preseeding work on Debian-derived systems.

## Unattended installations

For the same `apt` / `percona-release` sequence as in [Install Percona Server for MySQL using APT](#install-percona-server-for-mysql-using-apt), add `-y` to each `sudo apt install` line where you need non-interactive APT confirmations, and use non-interactive options for `percona-release` as in the following snippet.

--8<-- "install-flag.md"

## Install Percona Toolkit UDFs (Optional)

Percona Server for MySQL includes user-defined functions (UDFs) from [Percona Toolkit :octicons-link-external-16:](https://docs.percona.com/percona-toolkit/). These UDFs provide faster checksum calculations:

* `fnv_64`: Fast hash function

* `fnv1a_64`: Alternative fast hash function  

* `murmur_hash`: High-performance hash function

User-Defined Functions (UDFs) are custom functions you can add to MySQL to extend MySQL capabilities. The Percona Toolkit UDFs are useful for data integrity checks and performance monitoring.

To install the Percona Toolkit UDFs after installation:

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
