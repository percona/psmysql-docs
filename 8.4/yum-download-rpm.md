> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# Install Percona Server for MySQL using downloaded RPM packages

Download the packages from [Percona Product Downloads](https://www.percona.com/downloads) . If needed, [Instructions for the Percona Product Download](https://docs.percona.com/percona-server/8.4/download-instructions.md) are available.

The RPM builds for *RHEL* 8 and *RHEL* 9 contain ARM packages with the aarch64.rpm extension. This means that Percona Server for MySQL is available for users on ARM-based systems.

The following example downloads *Percona Server for MySQL* 8.4.11-12 release `x86_64` packages for *RHEL* 8.

1. Use `wget` to download the tar file.

   The download filename includes a `<revision-identifier>` value. This value is *build-specific* and must be obtained from the [Percona Product Downloads](https://www.percona.com/downloads) page for the exact release you are installing. Select the product, version, and operating system, and find the link with the required `<revision identifier>` under the **Download all packages** button. For more details, see the [Instructions for Percona Product Downloads](https://docs.percona.com/percona-server/8.4/download-instructions.md).

   ```shell
   wget https://downloads.percona.com/downloads/Percona-Server-8.4/Percona-Server-8.4.11-12/binary/redhat/8/x86_64/Percona-Server-8.4.11-12-<revision identifier>-el8-x86_64-bundle.tar
   ```

1. Unpack the bundle to get the packages:

   ```shell
   tar xvf Percona-Server-8.4.11-12-<revision identifier>-el8-x86_64-bundle.tar
   ```

1. To view a list of packages, run the following command:

   ```shell
   ls *.rpm
   ```

   The output should look like the following:

   Expected output

   ```text
   percona-icu-data-files-8.4.11-12.1.el8.x86_64.rpm
   percona-mysql-router-8.4.11-12.1.el8.x86_64.rpm
   percona-mysql-router-debuginfo-8.4.11-12.1.el8.x86_64.rpm
   percona-server-client-8.4.11-12.1.el8.x86_64.rpm
   percona-server-client-debuginfo-8.4.11-12.1.el8.x86_64.rpm
   percona-server-debuginfo-8.4.11-12.1.el8.x86_64.rpm
   percona-server-debugsource-8.4.11-12.1.el8.x86_64.rpm
   percona-server-devel-8.4.11-12.1.el8.x86_64.rpm
   percona-server-rocksdb-8.4.11-12.1.el8.x86_64.rpm
   percona-server-rocksdb-debuginfo-8.4.11-12.1.el8.x86_64.rpm
   percona-server-server-8.4.11-12.1.el8.x86_64.rpm
   percona-server-server-debuginfo-8.4.11-12.1.el8.x86_64.rpm
   percona-server-shared-8.4.11-12.1.el8.x86_64.rpm
   percona-server-shared-compat-8.4.11-12.1.el8.x86_64.rpm
   percona-server-shared-debuginfo-8.4.11-12.1.el8.x86_64.rpm
   percona-server-test-8.4.11-12.1.el8.x86_64.rpm
   percona-server-test-debuginfo-8.4.11-12.1.el8.x86_64.rpm
   ```

1. Install `jemalloc` with the following command, if needed. See [When to install jemalloc](#when-to-install-jemalloc) for guidance:

   ```shell
   wget https://repo.percona.com/yum/release/8/RPMS/x86_64/jemalloc-3.6.0-1.el8.x86_64.rpm
   ```

1. An EL8-based *RHEL* distribution or derivatives package installation requires the mysql module to be disabled before installing the packages:

   ```shell
   sudo yum module disable mysql
   ```

1. Download the `percona-telemetry-agent` package into the same directory. The `percona-server-server` package depends on it, but the bundle does not include it. Hosts without the Percona repositories cannot install the server without this package. For example, for *RHEL* 8:

   ```shell
   wget https://repo.percona.com/telemetry/yum/release/8/RPMS/x86_64/percona-telemetry-agent-1.0.17-1.el8.x86_64.rpm
   ```

1. Install the packages with `dnf localinstall`. Unlike `rpm -ivh`, `dnf` also installs the required packages from your distribution repositories, for example, `libaio` and `libatomic`:

   ```shell
   sudo dnf localinstall ./percona-server-server-8.4.11-12.1.el8.x86_64.rpm ./percona-server-client-8.4.11-12.1.el8.x86_64.rpm ./percona-server-shared-8.4.11-12.1.el8.x86_64.rpm ./percona-icu-data-files-8.4.11-12.1.el8.x86_64.rpm ./percona-telemetry-agent-*.rpm
   ```

   Note

   Do not use `sudo rpm -ivh *.rpm`. The `rpm` tool does not resolve dependencies and fails with `Failed dependencies`, for example, for `libaio`, `libatomic`, and `percona-telemetry-agent`.

## When to install jemalloc

`jemalloc` is an alternative memory allocator that can improve performance and reduce memory fragmentation in certain scenarios. Consider the following when deciding whether to install `jemalloc`:

### Install jemalloc when:

- You have high-concurrency workloads with many threads
- You experience memory fragmentation issues that impact performance
- You run multi-threaded applications that perform frequent memory allocation and deallocation
- You want to use [memory profiling features](https://docs.percona.com/percona-server/8.4/jemalloc-profiling.md) to investigate memory-related issues.
- You observe performance degradation related to memory allocation in your current setup

### Do not install jemalloc when:

- Your current memory allocator (typically glibc malloc) performs adequately for your workload
- You have single-threaded or low-concurrency workloads where jemalloc’s benefits are minimal
- You encounter compatibility issues with jemalloc in your environment
- You need to debug memory issues that may be complicated by using an alternative allocator
- Your system is already optimized and stable with the default memory allocator
