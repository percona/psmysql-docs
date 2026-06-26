# Non-interactive DNF installation for Percona Server for MySQL {{vers}}

Automate Percona Server for MySQL installation with DNF on Red Hat Enterprise Linux (RHEL), Rocky Linux, or AlmaLinux. Use Ansible, Kickstart, cloud-init, or a continuous integration (CI) image. For an interactive install, see [Install using DNF](yum-repo.md).

## Non-interactive installs and DNF

The `-y` flag (or `--assumeyes`) on `dnf` or `yum` skips transaction confirmation prompts. DNF does not use debconf. RPM `%post` scripts for `percona-server-server` do not ask for a `root` password during a fresh install on RHEL and derivatives.

After a fresh install, the server starts with a temporary `root` password. The password appears in the error log, usually `/var/log/mysqld.log`. Your automation must read that password and set a permanent one.

Common automation tasks include the following:

* Disable the distribution MySQL module without prompts

* Install `percona-release` and server packages with `-y`

* Run `percona-release` with non-interactive flags where supported

* Start the service, read the temporary password, and run `ALTER USER`

### Lab baseline and package validation

Package names and versions depend on the Linux distribution, the release (such as 9.4), and the `percona-server-server` build. Treat each example as illustrative until you confirm names on a disposable host that matches production.

1. Pick a lab image that matches production. Match repositories, distribution release, and architecture.

2. On the lab host, list available server packages:

	```shell
	dnf search percona-server-server
	rpm -q percona-server-server
	```

	Store the output with your automation. Run the check again after a base-image or package upgrade.

3. For automation, pin the `percona-server-server` version or record the build from `rpm -q`. Pinning ties scripts to a known package.

To automate the install sequence:

1. Use the DNF steps in [Install using DNF (RHEL 8 and later)](yum-repo.md#install-using-dnf-rhel-8-and-later). Add `-y` to each `sudo dnf` or `sudo yum` command that must skip confirmations.

2. Disable the MySQL module when step 1 of that procedure shows an `[e]` marker:

	```shell
	sudo dnf module disable mysql -y
	```

3. Install repository and server packages:

	```shell
	sudo dnf install -y https://repo.percona.com/yum/percona-release-latest.noarch.rpm
	sudo percona-release enable-only {{pkg}} release
	sudo dnf install -y percona-server-server
	```

	If your playbook uses `percona-release setup` instead of `enable-only`, add `-y` to `setup` as shown in [Unattended installations](#unattended-installations).

4. Start the server and enable it at boot:

	```shell
	sudo systemctl enable --now mysqld
	```

	The service name can be `mysqld` or `mysql` depending on the distribution. Confirm with `systemctl status mysqld` or `systemctl status mysql`.

5. Read the temporary password and set a permanent password. Use `caching_sha2_password` on {{vers}}:

	```shell
	TMP_PASS=$(sudo grep 'temporary password' /var/log/mysqld.log | tail -1 | awk '{print $NF}')
	mysql --connect-expired-password -uroot -p"${TMP_PASS}" -e \
	  "ALTER USER 'root'@'localhost' IDENTIFIED WITH caching_sha2_password BY '<strong-password>';"
	```

	Replace `<strong-password>` with a value that meets your password policy. Do not commit real passwords to version control or shell history. For manual steps and policy errors, see [Post-installation — Update the root password](post-installation.md#update-the-root-password).

6. Optional: run hardening after the password is set. The `mysql_secure_installation` script is interactive by default. For unattended hardening, apply equivalent SQL or use your configuration management tool. See [Post-installation — Secure the server](post-installation.md#secure-the-server) and [Sanity check](sanity-check.md).

#### Default authentication plugin

On {{vers}}, native-password authentication is unavailable. Unattended installs must use `caching_sha2_password` and compatible clients. See [Authentication methods](authentication-methods.md).

### See also

* [Telemetry](telemetry.md): Set `PERCONA_TELEMETRY_DISABLE=1` on the `dnf` or `yum` command line to disable collection

* [Authentication methods](authentication-methods.md): `caching_sha2_password` and related settings

* [Post-installation](post-installation.md): Secure and configure the server after package install

* [DNF documentation — assumeyes :octicons-link-external-16:](https://dnf.readthedocs.io/en/latest/conf_ref.html#assumeyes-options): Global non-interactive DNF behavior

## Unattended installations

Use the DNF sequence in [Install using DNF (RHEL 8 and later)](yum-repo.md#install-using-dnf-rhel-8-and-later). Add `-y` to each `sudo dnf install` or `sudo yum install` command that must skip confirmations. For `percona-release setup`, use the non-interactive options in the following snippet.

--8<-- "install-flag.md"
