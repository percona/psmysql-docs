# Use an APT repository to install Percona Server for MySQL {{vers}}

Percona Server for MySQL packages are available from the software repositories and from the [Percona Software Downloads :octicons-link-external-16:](https://www.percona.com/downloads/) page.

The [Percona Release Lifecycle Overview :octicons-link-external-16:](https://www.percona.com/release-lifecycle-overview/#mysql) page lists supported platforms, products, and versions. Debian (DEB) packages support `arm64` and other architectures on documented Debian and Ubuntu releases.

--8<-- "percona-release.md"

We gather [Telemetry data] in the Percona packages and Docker images.

--8<--- "get-help-snip.md"

## Install Percona Server for MySQL using APT

Percona Server for MySQL {{vers}} uses the MySQL 9.x authentication model. Review the following behaviors before you install:

--8<--- "authentication-9x-overview.md:3:8"

When the package manager prompts during installation, follow [Configure authentication](#configure-authentication). Prompts depend on the package and distribution.

Install Percona Server on Debian or Ubuntu with the following steps:

1. Copy the command block in the following section. Run the commands in order.

2. Use [Configure authentication](#configure-authentication) when the package manager prompts for authentication options.

3. Open [Next steps](#next-steps) after the server packages install.

4. Expand the `Step-by-step: what each command does` note for an explanation of each command.

5. For scripted automation, see [Non-interactive APT installation for Percona Server for MySQL {{vers}}](apt-noninteractive-install.md).

Run the commands as the `root` user or with `sudo`:

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

The command sequence matches [Install Percona Server for MySQL and create a database on Ubuntu](quickstart-apt.md). The quickstart includes steps 1 through 6. The quickstart passes `--scheme https` to `percona-release setup` and `enable`. The repository identifier for {{vers}} is `{{pkg}}`.

For another Percona Server for MySQL series, run `sudo percona-release list` or see the [MySQL software repositories :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/mysql.html) reference. Percona can change published repository names when Percona adds a series.

??? note "`percona-release` flag: `--scheme`"

	The examples on this topic pass `--scheme https`. Repository URLs in APT source lists then use HTTPS. The [Percona Software Repositories — `percona-release` :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/percona-release.html) reference documents the `--scheme` flag. Supported values are HTTP and HTTPS. Without `--scheme`, `percona-release` uses HTTP URLs by default.

	You can pass `--scheme https` to subcommands such as `setup`, `enable`, `enable-only`, or `disable`. Use the same pattern as the examples. See the linked reference for all commands.

??? note "Step-by-step: what each command does"

	Each step includes a short explanation:

	1. `apt update` refreshes package lists for upgrades and installs. `sudo` runs the command with superuser privileges. The command reads sources in `/etc/apt/sources.list` and `/etc/apt/sources.list.d/`.

		```shell
		sudo apt update
		```

	2. `sudo apt install -y curl` installs the `curl` package. `curl` transfers data over the network. You need `curl` to download the Percona repository package.

		```shell
		sudo apt install -y curl
		```

	3. `curl -O` downloads `percona-release_latest.generic_all.deb` from the Percona APT repository. The `-O` option saves the file with the URL filename.

		```shell
		curl -O https://repo.percona.com/apt/percona-release_latest.generic_all.deb
		```

	4. The next command installs `gnupg2`, `lsb-release`, and the Percona release package. `gnupg2` verifies package signatures. `lsb-release` reports distribution information. Together with the `.deb` file, these packages configure the Percona APT repository.

		```shell
		sudo apt install -y gnupg2 lsb-release ./percona-release_latest.generic_all.deb
		```

	5. `percona-release setup {{pkg}} --scheme https` disables current Percona repositories. The command enables release repositories for Percona Server for MySQL {{vers}} over HTTPS. See the [Percona Software Repositories :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/percona-release.html) reference. Omit `--scheme https` only when you need HTTP repository URLs.

		```shell
		sudo percona-release setup {{pkg}} --scheme https
		```

	6. `percona-release enable {{pkg}} release --scheme https` enables the Percona Server for MySQL release repository with HTTPS URLs. Run `apt update` next so APT loads indexes for `percona-server-server` and related packages.

		```shell
		sudo percona-release enable {{pkg}} release --scheme https
		sudo apt update
		```

	7. Confirm repository configuration in `.list` files under `/etc/apt/sources.list.d/`. The filename, such as `percona-original-release.list`, depends on the `percona-release` version.

	8. `sudo apt install -y percona-server-server` installs the server package. The package manager can prompt for values such as the `root` password. Some builds use debconf or post-install configuration only. For password prompts and automation, see [Non-interactive APT installation for Percona Server for MySQL {{vers}}](apt-noninteractive-install.md). For authentication defaults and removed plugins, see [Configure authentication](#configure-authentication).

		```shell
		sudo apt install -y percona-server-server
		```

### Configure authentication

The package manager can prompt for passwords and other options during installation. The authentication table above lists MySQL 9.x defaults and removed options. Change authentication after installation when the package skips prompts. For automation, see [Non-interactive APT installation for Percona Server for MySQL {{vers}}](apt-noninteractive-install.md).

!!! warning "Important change in {{vers}}"

	For a migration from native password authentication, update accounts and clients before you deploy {{vers}}. See [Authentication methods](authentication-methods.md) and [Upgrade checklist for {{vers}}](upgrade-checklist-9.7.md).

See [Configuring Percona repositories with `percona-release` :octicons-link-external-16:](https://docs.percona.com/percona-software-repositories/percona-release.html) for repository commands.

--8<--- "storage-engines.md"

## Next steps

After installation, see [Post-installation](post-installation.md) to configure and secure the server.

## Related installation topics

- [Non-interactive APT installation for Percona Server for MySQL {{vers}}](apt-noninteractive-install.md): debconf preseed, unattended installs, and `DEBIAN_FRONTEND=noninteractive`

- [Optional steps after repository install for Percona Server for MySQL {{vers}}](optional-after-install.md): Percona Toolkit UDFs and the testing repository

[Telemetry data]: telemetry.md
