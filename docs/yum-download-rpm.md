# Install Percona Server for MySQL using downloaded RPM packages

Download the packages from [Percona Product Downloads](https://www.percona.com/downloads). If needed, [Instructions for the Percona Product Download](download-instructions.md) are available.

The following example downloads *Percona Server for MySQL* {{release}} release packages for *RHEL* 8.
{.power-number}

1. Use `wget` to download the tar file.

	```{.bash data-prompt="$"}
	$ wget https://downloads.percona.com/downloads/Percona-Server-innovative-release/Percona-Server-{{release}}/binary/redhat/8/x86_64/Percona-Server-{{release}}-r582ebeef-el8-x86_64-bundle.tar
	```

2. Unpack the bundle to get the packages: `tar xvf Percona-Server-{{release}}-rc59f87d2854-el8-x86_64-bundle.tar`

3. To view a list of packages, run the following command:

	```{.bash data-prompt="$"}
	$ ls *.rpm
	```
	The output should look like the following:
	
    ??? example "Expected output"

        ```text
        percona-icu-data-files-{{release}}.1.el8.x86_64.rpm
        percona-mysql-router-{{release}}.1.el8.x86_64.rpm
        percona-mysql-router-debuginfo-{{release}}.1.el8.x86_64.rpm
        percona-server-client-{{release}}.1.el8.x86_64.rpm
        percona-server-client-debuginfo-{{release}}.1.el8.x86_64.rpm
        percona-server-debuginfo-{{release}}.1.el8.x86_64.rpm
        percona-server-debugsource-{{release}}.1.el8.x86_64.rpm
        percona-server-devel-{{release}}.1.el8.x86_64.rpm
        percona-server-rocksdb-{{release}}.1.el8.x86_64.rpm
        percona-server-rocksdb-debuginfo-{{release}}.1.el8.x86_64.rpm
        percona-server-server-{{release}}.1.el8.x86_64.rpm
        percona-server-server-debuginfo-{{release}}.1.el8.x86_64.rpm
        percona-server-shared-{{release}}.1.el8.x86_64.rpm
        percona-server-shared-compat-{{release}}.1.el8.x86_64.rpm
        percona-server-shared-debuginfo-{{release}}.1.el8.x86_64.rpm
        percona-server-test-{{release}}.1.el8.x86_64.rpm
        percona-server-test-debuginfo-{{release}}.1.el8.x86_64.rpm
        ```
	

4. Install `jemalloc` with the following command, if needed:
	
	```{.bash data-prompt="$"}
	$ wget https://repo.percona.com/yum/release/8/RPMS/x86_64/jemalloc-3.6.0-1.el8.x86_64.rpm
	```

5. An EL8-based *RHEL* distribution or derivatives package installation requires the mysql module to be disabled before installing the packages:

	```{.bash data-prompt="$"}
	$ sudo yum module disable mysql
	```

6. Install all the packages (for debugging, testing, etc.) with the following command:

	```{.bash data-prompt="$"}
	$ sudo rpm -ivh *.rpm
	```

	!!! note
	
	    When installing packages manually, you must make sure to resolve all dependencies and install any missing packages yourself.