# Install Percona Server for MySQL using downloaded RPM packages

Download the packages from [Percona Product Downloads :octicons-link-external-16:](https://www.percona.com/downloads). If needed, [Instructions for the Percona Product Download](download-instructions.md) are available.

The RPM builds for *RHEL* 8 and *RHEL* 9 contain ARM packages with the aarch64.rpm extension. This means that Percona Server for MySQL is available for users on ARM-based systems.

The following example downloads *Percona Server for MySQL* {{release}} release `x86_64` packages for *RHEL* 8.
{.power-number}

1. Use `wget` to download the tar file:

    The download filename includes a `<revision-identifier>` value. This value is *build-specific* and must be obtained from the [Percona Product Downloads :octicons-link-external-16:](https://www.percona.com/downloads) page for the exact release you are installing. Select the product, version, and operating system, and find the link with the required `<revision identifier>` under the **Download all packages** button. For more details, see the [Instructions for Percona Product Downloads](download-instructions.md).

	```shell
	wget https://downloads.percona.com/downloads/Percona-Server-{{vers}}/Percona-Server-{{release}}/binary/redhat/8/x86_64/Percona-Server-{{release}}-<revision identifier>-el8-x86_64-bundle.tar
	```

2. Unpack the bundle to get the packages: 

    ```shell
    tar xvf Percona-Server-{{release}}-<revision identifier>-el8-x86_64-bundle.tar
    ```

3. To view a list of packages, run the following command:

	```shell
	ls *.rpm
	```
	The output should look like the following:
	
    ??? example "Expected output"

        ```{.text .no-copy}
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
	

4. Install `jemalloc` with the following command, if needed. See [When to install jemalloc](#when-to-install-jemalloc) for guidance:
	
	```shell
	wget https://repo.percona.com/yum/release/8/RPMS/x86_64/jemalloc-3.6.0-1.el8.x86_64.rpm
	```

5. An EL8-based *RHEL* distribution or derivatives package installation requires the mysql module to be disabled before installing the packages:

	```shell
	sudo yum module disable mysql
	```

6. Install all the packages (for debugging, testing, etc.) with the following command:

	```shell
	sudo rpm -ivh *.rpm
	```

	!!! note
	
	    When installing packages manually, you must make sure to resolve all dependencies and install any missing packages yourself.

## When to install jemalloc

`jemalloc` is an alternative memory allocator that can improve performance and reduce memory fragmentation in certain scenarios. Consider the following when deciding whether to install `jemalloc`:

### Install jemalloc when:

* You have high-concurrency workloads with many threads

* You experience memory fragmentation issues that impact performance

* You run multi-threaded applications that perform frequent memory allocation and deallocation

* You want to use [memory profiling features](jemalloc-profiling.md) to investigate memory-related issues.

* You observe performance degradation related to memory allocation in your current setup

### Do not install jemalloc when:

* Your current memory allocator (typically glibc malloc) performs adequately for your workload

* You have single-threaded or low-concurrency workloads where jemalloc's benefits are minimal

* You encounter compatibility issues with jemalloc in your environment

* You need to debug memory issues that may be complicated by using an alternative allocator

* Your system is already optimized and stable with the default memory allocator
