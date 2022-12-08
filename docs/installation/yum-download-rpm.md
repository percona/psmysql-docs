# Install Percona Server for MySQL using downloaded RPM packages

1. Download the packages of the desired series for your architecture from the
[download page](http://www.percona.com/downloads/Percona-Server-8.0/). The
easiest way is to download the bundle which contains all the packages. The following example downloads *Percona Server for MySQL* 8.0.21-12 release packages for *RHEL* 8.

	```shell
	$ wget https://downloads.percona.com/downloads/Percona-Server-LATEST/Percona-Server-8.0.29-21/binary/redhat/8/x86_64/Percona-Server-8.0.29-21-rc59f87d2854-el8-x86_64-bundle.tar
	```

2. Unpack the bundle to get the packages: `tar xvf Percona-Server-8.0.29-21-rc59f87d2854-el8-x86_64-bundle.tar`

3. To view a list of packages, run the following command:

	```shell
	$ ls *.rpm
	```
	The output should look like the following:
	
    ??? example "Expected output"

        ```text
        percona-icu-data-files-8.0.29-21.1.el8.x86_64.rpm
        percona-mysql-router-8.0.29-21.1.el8.x86_64.rpm
        percona-mysql-router-debuginfo-8.0.29-21.1.el8.x86_64.rpm
        percona-server-client-8.0.29-21.1.el8.x86_64.rpm
        percona-server-client-debuginfo-8.0.29-21.1.el8.x86_64.rpm
        percona-server-debuginfo-8.0.29-21.1.el8.x86_64.rpm
        percona-server-debugsource-8.0.29-21.1.el8.x86_64.rpm
        percona-server-devel-8.0.29-21.1.el8.x86_64.rpm
        percona-server-rocksdb-8.0.29-21.1.el8.x86_64.rpm
        percona-server-rocksdb-debuginfo-8.0.29-21.1.el8.x86_64.rpm
        percona-server-server-8.0.29-21.1.el8.x86_64.rpm
        percona-server-server-debuginfo-8.0.29-21.1.el8.x86_64.rpm
        percona-server-shared-8.0.29-21.1.el8.x86_64.rpm
        percona-server-shared-compat-8.0.29-21.1.el8.x86_64.rpm
        percona-server-shared-debuginfo-8.0.29-21.1.el8.x86_64.rpm
        percona-server-test-8.0.29-21.1.el8.x86_64.rpm
        percona-server-test-debuginfo-8.0.29-21.1.el8.x86_64.rpm
        ```
	

4. Install `jemalloc` with the following command, if needed:
	
	```shell
	$ wget https://repo.percona.com/yum/release/8/RPMS/x86_64/jemalloc-3.6.0-1.el8.x86_64.rpm
	```

5. An EL8-based *RHEL* distribution or derivatives package installation requires the mysql module to be disabled before installing the packages:

	```shell
	$ sudo yum module disable mysql
	```

6. Install all the packages (for debugging, testing, etc.) with the following command:

	```shell
	$ sudo rpm -ivh *.rpm
	```

	!!! note
	
	    When installing packages manually, you must make sure to resolve all dependencies and install any missing packages yourself.