# Non-interactive APT installation for Percona Server for MySQL {{vers}}

Automate Percona Server for MySQL installation with APT on Debian or Ubuntu. Use cloud-init, Ansible, or a continuous integration (CI) image. For an interactive install, see [Use an APT repository to install Percona Server for MySQL {{vers}}](apt-repo.md).

## Non-interactive installs and debconf

The `-y` flag on `apt install` skips APT confirmation prompts only. Maintainer scripts for `percona-server-server` can still ask debconf questions. Common prompts include the following:

* The MySQL `root` password

* Whether to reuse an existing data directory

* Lowercase table names

Prompts depend on the `percona-server-server` package version and on data on the disk.

### Lab baseline and debconf validation

Debconf template names and valid answers depend on the Linux distribution, the release (such as 22.04 or 24.04), and the `percona-server-server` package version. Template names do not depend on the Percona Server {{vers}} product line alone.

Treat each preseed example as illustrative until you confirm keys on a disposable host that matches production.

1. Pick a lab image that matches production. Match `.list` repositories, distribution release, and architecture. The examples target Ubuntu 22.04 LTS (Jammy) and Percona Server for MySQL {{vers}} packages from the Percona APT repository. On Debian, Ubuntu 24.04 LTS, or other distributions, keys can differ. Extra questions can appear.

2. On the lab host or on a CI image with the same configuration, install the package version you plan for production. Capture the output:

	```shell
	lsb_release -a
	dpkg-query -W percona-server-server
	sudo debconf-show percona-server-server | tee debconf-percona-server-server.txt
	```

	Store `debconf-percona-server-server.txt` with your automation (Ansible, cloud-init, or similar). Run the capture again after a base-image or package upgrade.

3. For automation, pin the `percona-server-server` version or record the build ID from `dpkg-query`. Pinning ties preseed scripts to a known `debconf-show` result.

To automate prompts:

1. Discover questions for your package version. On a lab host, install once interactively or inspect templates. Run:

	```shell
	sudo debconf-show percona-server-server
	```

	The package ships template definitions at paths such as `/var/lib/dpkg/info/percona-server-server.templates`.

	Verify templates for each target. Preseed names and choices can differ by distribution, point release, and package version. Run `debconf-show` again after upgrades or after a base-image change. For production automation, keep a checklist that maps distribution and package version to saved `debconf-show` output.

2. Preseed answers with `debconf-set-selections` before `apt install`. Many Percona Server for MySQL {{vers}} packages use `percona-server-server/root-pass` and `percona-server-server/re-root-pass` for password prompts:

	```shell
	echo "percona-server-server percona-server-server/root-pass password <strong-password>" | sudo debconf-set-selections
	echo "percona-server-server percona-server-server/re-root-pass password <strong-password>" | sudo debconf-set-selections
	```

	Other prompts, such as `percona-server-server/lowercase-table-names` or `percona-server-server/remove-data-dir`, appear only on some upgrade or edge-case paths. Add lines from `debconf-show` output. Do not commit real passwords to version control or shell history.

3. Optional: set `DEBIAN_FRONTEND=noninteractive` for the `percona-server-server` install so debconf does not open a user interface. Combine non-interactive installs with preseeding. Without defaults for required questions, the Debian package `configure` step can fail or leave the server in an unexpected state.

	```shell
	sudo DEBIAN_FRONTEND=noninteractive apt install -y percona-server-server
	```

#### Default authentication plugin

When a distribution or package adds a debconf choice for authentication, the prompt appears in `debconf-show` output for `percona-server-server`. On {{vers}}, native-password authentication is unavailable. Unattended installs must use `caching_sha2_password` and compatible clients. See [Configure authentication during APT install](apt-repo.md#configure-authentication) and [Authentication methods](authentication-methods.md).

### See also

* [Telemetry](telemetry.md): Set `PERCONA_TELEMETRY_DISABLE=1` on the `apt` command line to disable collection

* [Authentication methods](authentication-methods.md): `caching_sha2_password` and related settings

* [Post-installation](post-installation.md): Secure and configure the server after package install

* [Debian Wiki — debconf :octicons-link-external-16:](https://wiki.debian.org/debconf): Debconf and preseeding on Debian-derived systems

## Unattended installations

Use the `apt` and `percona-release` sequence in [Install Percona Server for MySQL using APT](apt-repo.md#install-percona-server-for-mysql-using-apt). Add `-y` to each `sudo apt install` command that must skip APT confirmations. For `percona-release`, use the non-interactive options in the following snippet.

--8<-- "install-flag.md"
