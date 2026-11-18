> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/9.7/llms.txt).

# Install Percona Server for MySQL using downloaded RPM packages

Download the packages from [Percona Product Downloads](https://www.percona.com/downloads) . If needed, [Instructions for the Percona Product Download](https://docs.percona.com/percona-server/9.7/download-instructions.html) are available.

The RPM builds for *RHEL* 8 and *RHEL* 9 contain ARM packages with the aarch64.rpm extension. This means that Percona Server for MySQL is available for users on ARM-based systems.

The following example downloads *Percona Server for MySQL* 9.7.2-3 release `x86_64` packages for *RHEL* 9. For *RHEL* 8 or *RHEL* 10, replace `redhat/9` and `el9` with `redhat/8` and `el8` or with `redhat/10` and `el10`.

1. Use `wget` to download the tar file:

   The download filename includes a `<revision-identifier>` value. This value is *build-specific* and must be obtained from the [Percona Product Downloads](https://www.percona.com/downloads) page for the exact release you are installing. Select the product, version, and operating system, and find the link with the required `<revision identifier>` under the **Download all packages** button. For more details, see the [Instructions for Percona Product Downloads](https://docs.percona.com/percona-server/9.7/download-instructions.html).

   ```
   wget https://downloads.percona.com/downloads/Percona-Server-9.7/Percona-Server-9.7.2-3/binary/redhat/9/x86_64/Percona-Server-9.7.2-3-<revision identifier>-el9-x86_64-bundle.tar
   ```

1. Unpack the bundle to get the packages:

   ```
   tar xvf Percona-Server-9.7.2-3-<revision identifier>-el9-x86_64-bundle.tar
   ```

1. To view a list of packages, run the following command:

   ```
   ls *.rpm
   ```

   The output should look like the following:

   Expected output

   ```
   percona-icu-data-files-9.7.2-3.1.el9.x86_64.rpm
   percona-mysql-router-9.7.2-3.1.el9.x86_64.rpm
   percona-mysql-router-debuginfo-9.7.2-3.1.el9.x86_64.rpm
   percona-server-client-9.7.2-3.1.el9.x86_64.rpm
   percona-server-client-debuginfo-9.7.2-3.1.el9.x86_64.rpm
   percona-server-client-plugins-9.7.2-3.1.el9.x86_64.rpm
   percona-server-client-plugins-debuginfo-9.7.2-3.1.el9.x86_64.rpm
   percona-server-debuginfo-9.7.2-3.1.el9.x86_64.rpm
   percona-server-debugsource-9.7.2-3.1.el9.x86_64.rpm
   percona-server-devel-9.7.2-3.1.el9.x86_64.rpm
   percona-server-js-9.7.2-3.1.el9.x86_64.rpm
   percona-server-js-debuginfo-9.7.2-3.1.el9.x86_64.rpm
   percona-server-rocksdb-9.7.2-3.1.el9.x86_64.rpm
   percona-server-rocksdb-debuginfo-9.7.2-3.1.el9.x86_64.rpm
   percona-server-server-9.7.2-3.1.el9.x86_64.rpm
   percona-server-server-debuginfo-9.7.2-3.1.el9.x86_64.rpm
   percona-server-shared-9.7.2-3.1.el9.x86_64.rpm
   percona-server-shared-compat-9.7.2-3.1.el9.x86_64.rpm
   percona-server-shared-debuginfo-9.7.2-3.1.el9.x86_64.rpm
   percona-server-test-9.7.2-3.1.el9.x86_64.rpm
   percona-server-test-debuginfo-9.7.2-3.1.el9.x86_64.rpm
   ```

1. Install `jemalloc` with the following command, if needed. See [When to install jemalloc](#when-to-install-jemalloc) for guidance:

   ```
   wget https://repo.percona.com/yum/release/8/RPMS/x86_64/jemalloc-3.6.0-1.el8.x86_64.rpm
   ```

1. An EL8-based *RHEL* distribution or derivatives package installation requires the mysql module to be disabled before installing the packages:

   ```
   sudo yum module disable mysql
   ```

1. Install the server, the client, and the required libraries with `dnf localinstall`. Run this command as root or use the sudo command:

   ```
   sudo dnf localinstall ./percona-server-server-[0-9]*.rpm ./percona-server-client-[0-9]*.rpm ./percona-server-client-plugins-[0-9]*.rpm ./percona-server-shared-[0-9]*.rpm ./percona-icu-data-files-[0-9]*.rpm
   ```

   `dnf` installs the local packages and resolves the remaining dependencies, such as `libaio` and `libatomic`, from the configured repositories. Do not use `rpm -ivh *.rpm`: `rpm` does not resolve dependencies and fails with `Failed dependencies`.

   Note

   The `percona-server-server` package depends on `percona-telemetry-agent`, which is not included in the bundle. `dnf` installs the agent from the Percona telemetry repository if the repository is configured (for example, by `percona-release`). Otherwise, the installation fails with `nothing provides percona-telemetry-agent`. In that case, download the agent package for your distribution from the [Percona telemetry repository](https://repo.percona.com/telemetry/yum/release/) (for example, `https://repo.percona.com/telemetry/yum/release/9/RPMS/x86_64/`) into the same directory and add `./percona-telemetry-agent-*.rpm` to the `dnf localinstall` command.

   The optional packages in the bundle have additional dependencies. For example, `percona-server-shared-compat` requires `compat-openssl11`, and `percona-server-test` requires Perl modules such as `perl-JSON`.

## When to install jemalloc

`jemalloc` is an alternative memory allocator that can improve performance and reduce memory fragmentation in certain scenarios. Consider the following when deciding whether to install `jemalloc`:

### Install jemalloc when:

- You have high-concurrency workloads with many threads
- You experience memory fragmentation issues that impact performance
- You run multi-threaded applications that perform frequent memory allocation and deallocation
- You want to use [memory profiling features](https://docs.percona.com/percona-server/9.7/jemalloc-profiling.html) to investigate memory-related issues.
- You observe performance degradation related to memory allocation in your current setup

### Do not install jemalloc when:

- Your current memory allocator (typically glibc malloc) performs adequately for your workload
- You have single-threaded or low-concurrency workloads where jemalloc’s benefits are minimal
- You encounter compatibility issues with jemalloc in your environment
- You need to debug memory issues that may be complicated by using an alternative allocator
- Your system is already optimized and stable with the default memory allocator
