# Install Percona Server for MySQL using downloaded RPM packages

You should be aware that when you install packages manually, you must resolve and install any dependencies. This process may involve finding and installing the necessary dependencies before installing the packages. Dependencies are other packages that a package may need to function correctly. For example, a package may rely on a specific library. If that library is not installed, or if the installed library is the wrong version, the package may not work correctly.

Package managers, like `APT` or `YUM` install the dependencies for you.

Download the packages from [Percona Product Downloads](https://www.percona.com/downloads). If needed, [Instructions for the Percona Product Download](download-instructions.md) are available.

## Version changes

Starting with Percona Server 8.0.33-25, the RPM builds for *RHEL* 8 and *RHEL* 9 contain ARM packages with the `aarch64.rpm` extension. This means that Percona Server for MySQL is available for users on ARM-based systems.

## Download and install RPM packages

The following example downloads *Percona Server for MySQL* 8.0.32-24 release packages for *RHEL* 8.

1. Using [`Wget`](https://www.gnu.org/software/wget/), the following command downloads a specific version of Percona Server for MySQL on Red Hat Enterprise Linux 8 from the Percona website. 

	```{.bash data-prompt="$"}
	$ wget https://downloads.percona.com/downloads/Percona-Server-8.0/Percona-Server-8.0.32-24/binary/redhat/8/x86_64/Percona-Server-8.0.32-24-re5c6e9d2-el8-x86_64-bundle.tar
	```

2. The following command extracts the contents of Percona Server for MySQL tarball. The `tar` command uses these options for the extraction:

    * `x` - extract

    * `v` - a verbose description of the `tar` extraction

    * `f` - name of the archive file

    ```{.bash data-prompt="$"}
    $ tar xvf Percona-Server-8.0.32-24-re5c6e9d2-el8-x86_64-bundle.tar
    ```

3. The following command uses the `ls` utility to list the RPM files in the current directory. The command uses the `*.rpm` pattern. The `*` is a wildcard that matches any number of characters. The `.rpm` specifies that we only want the files that end in this extension.

	```{.bash data-prompt="$"}
	$ ls *.rpm
	```
	The output should look like the following:
	
    ??? example "Expected output"

        ```text
        percona-icu-data-files-8.0.32-24.1.el8.x86_64.rpm
        percona-mysql-router-8.0.32-24.1.el8.x86_64.rpm
        percona-mysql-router-debuginfo-8.0.32-24.1.el8.x86_64.rpm
        percona-server-client-8.0.32-24.1.el8.x86_64.rpm
        percona-server-client-debuginfo-8.0.32-24.1.el8.x86_64.rpm
        percona-server-debuginfo-8.0.32-24.1.el8.x86_64.rpm
        percona-server-debugsource-8.0.32-24.1.el8.x86_64.rpm
        percona-server-devel-8.0.32-24.1.el8.x86_64.rpm	
        percona-server-rocksdb-8.0.32-24.1.el8.x86_64.rpm
        percona-server-rocksdb-debuginfo-8.0.32-24.1.el8.x86_64.rpm
        percona-server-server-8.0.32-24.1.el8.x86_64.rpm
        percona-server-server-debuginfo-8.0.32-24.1.el8.x86_64.rpm
        percona-server-shared-8.0.32-24.1.el8.x86_64.rpm
        percona-server-shared-compat-8.0.32-24.1.el8.x86_64.rpm
        percona-server-shared-debuginfo-8.0.32-24.1.el8.x86_64.rpm
        percona-server-test-8.0.32-24.1.el8.x86_64.rpm
        percona-server-test-debuginfo-8.0.32-24.1.el8.x86_64.rpm
        ```
	
4. [Optional] Install `jemalloc`. The following command downloads a specific version of `jemalloc` for RHEL 8 from the Percona repository.
	
	```{.bash data-prompt="$"}
	$ wget https://repo.percona.com/yum/release/8/RPMS/x86_64/jemalloc-3.6.0-1.el8.x86_64.rpm
	```

5. An EL8-based RHEL distribution or derivatives package installation requires you to disable the `mysql` module. We are installing a different version than the one provided by the module, so we must disable the module before installation. 

	```{.bash data-prompt="$"}
	$ sudo yum module disable mysql
	```

6. The following command uses superuser privileges to install RPM packages in the current directory using the `rpm` command. The `rpm` command uses the following options:

    * `i` - install

    * `v` - verbose, describe the process in detail

    * `h` - display hash marks (`#`) to display installation progress

    ```{.bash data-prompt="$"}
    $ sudo rpm -ivh *.rpm
    ```
