# Production readiness and baseline configuration

Prepare each production host after you install Percona Server for MySQL.

This page is a Day-1 **tuning baseline**. The page covers host checks, `my.cnf` sizing, restart safety, and Percona feature activation.

Complete security, recovery, availability, and operating-system hardening in the related guides:

* [First five minutes after installation](first-five-minutes.md)

* [Sanity check: First five minutes](sanity-check.md)

* [Post-installation](post-installation.md)

* [Backup and restore overview](backup-restore-overview.md)

Use these values as a baseline. Test each value with a representative workload. Change one value at a time.

!!! important

    Test this configuration in a test environment before production use.

    Memory, storage latency, concurrency, durability, and replication affect the correct values.

    Stop when a check fails. Fix the issue before you change memory, connections, or restart MySQL.

Example output on this page uses sample paths, numbers, and service names from one host. A **Pass** or **Stop** line is the result you verify. A different path, number, or service name still passes when the **Pass** condition is true. Debian, Ubuntu, Red Hat Enterprise Linux, and Oracle Linux often differ in those sample values.

## Key terms

| Term | Meaning |
|---|---|
| Direct input/output (I/O) | The server writes data files without the operating system page cache. MySQL often uses the `O_DIRECT` flush method for this path. |
| Buffer pool hit rate | The share of InnoDB page reads that MySQL serves from memory. A low hit rate can show that the buffer pool is too small for the working set. |
| Binary logs | Server files that record data changes. Replication and point-in-time recovery use these files. |
| Non-Uniform Memory Access (NUMA) | A memory layout on multi-socket hosts. Nearby memory is faster than remote memory. MySQL can spread allocations across NUMA nodes. |
| Point-in-time recovery | A restore method that applies a full backup, then applies binary log events up to a selected time. |
| Drop-in file | An extra option file that MySQL loads from a configuration directory. Use one controlled drop-in file for production baseline values. |

## Find and edit the active configuration file

Complete these steps before you change production values.

### List every option file that MySQL can load

1. List the default option-file search order:

    ```shell
    mysqld --help --verbose 2>/dev/null | grep -A1 'Default options'
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Default options are read from the following files in the given order:
        /etc/my.cnf /etc/mysql/my.cnf ~/.my.cnf
        ```

        **Pass:** The command prints at least one readable path.

        **Stop:** The command prints no paths, or every listed path is missing and you cannot locate the package configuration.

2. Show which option files a server process would read, including directories:

    ```shell
    mysqld --verbose --help 2>/dev/null | awk '/^Default options/,/^$/'
    ls -la /etc/my.cnf /etc/mysql/my.cnf /etc/mysql/conf.d /etc/mysql/mysql.conf.d /etc/my.cnf.d 2>/dev/null
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        Default options are read from the following files in the given order:
        /etc/my.cnf /etc/mysql/my.cnf ~/.my.cnf

        -rw-r--r-- 1 root root  120 Apr  1 10:00 /etc/my.cnf
        /etc/mysql/mysql.conf.d:
        -rw-r--r-- 1 root root 3122 Apr  1 10:00 mysqld.cnf
        ```

        **Pass:** You can list every file under the included directories for your package.

        **Stop:** You cannot identify which directories MySQL includes. Do not edit random files.

### How duplicate values win

MySQL reads option files in search order. Later values override earlier values for the same option and group.

Rules:

* Values in a later file override values in an earlier file.

* Within one file, a later line for the same option overrides an earlier line.

* Command-line options override option-file values.

* Files in an included directory load in alphabetical order. A `zz-production.cnf` file loads after `mysqld.cnf` and overrides matching options.

* The last file in the default list is `~/.my.cnf` for the operating-system user that starts `mysqld`. Values in that file override the drop-in. `sudo mysqld --validate-config` runs as `root` and can read the root account home file. The running service reads the home file of the service account. Those two files can differ.

Confirm the effective value after restart with `SHOW VARIABLES`. The effective value is the final winner.

### Common package locations

* Debian and Ubuntu often use `/etc/mysql/my.cnf` and files under `/etc/mysql/conf.d/` or `/etc/mysql/mysql.conf.d/`.

* Red Hat Enterprise Linux and Oracle Linux often use `/etc/my.cnf` and files under `/etc/my.cnf.d/`.

Prefer a dedicated drop-in file for production changes:

* `/etc/mysql/mysql.conf.d/zz-production.cnf`

* `/etc/my.cnf.d/zz-production.cnf`

The create steps select one of those two directories only when `/etc/my.cnf` or `/etc/mysql/my.cnf` includes it with `!includedir`. The steps do not open a path named by `--defaults-file`. The steps do not follow `!include`, and they do not read `!includedir` inside a file that another file includes. A directory such as `/etc/mysql/conf.d` is also outside those two paths. Use the fallback when the host uses one of those layouts.

### Create the production drop-in file safely

Use these steps when the drop-in file does not exist.

1. Select the drop-in directory that this host already has, and confirm that a main option file includes it:

    ```shell
    DROPIN_DIR=
    INCLUDED=$(sed -n 's/^[[:space:]]*!includedir[[:space:]][[:space:]]*//p' /etc/my.cnf /etc/mysql/my.cnf 2>/dev/null | tr -d '\r' | sed 's/[[:space:]]*$//; s:/*$::')
    for dir in /etc/mysql/mysql.conf.d /etc/my.cnf.d; do
      if [ -d "$dir" ] && printf '%s\n' "$INCLUDED" | grep -qxF -- "$dir"; then
        DROPIN_DIR=$dir
        break
      fi
    done
    if [ -z "$DROPIN_DIR" ]; then
      echo "STOP: no included drop-in directory. Checked /etc/mysql/mysql.conf.d and /etc/my.cnf.d."
    fi
    echo "DROPIN_DIR=${DROPIN_DIR:-unset}"
    if [ -n "$DROPIN_DIR" ]; then
      ls -ld "$DROPIN_DIR"
    fi
    grep -nE '^[[:space:]]*!includedir' /etc/my.cnf /etc/mysql/my.cnf 2>/dev/null
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        DROPIN_DIR=/etc/mysql/mysql.conf.d
        drwxr-xr-x 2 root root 4096 Apr  1 10:00 /etc/mysql/mysql.conf.d
        /etc/mysql/my.cnf:23:!includedir /etc/mysql/mysql.conf.d/
        ```

        On Red Hat Enterprise Linux and Oracle Linux the directory is often `/etc/my.cnf.d`, included from `/etc/my.cnf`.

        **Pass:** `DROPIN_DIR` is set, the directory belongs to `root`, and an `!includedir` line names that directory. The script ignores a trailing slash, trailing spaces, Windows line endings, and commented lines.

        **Stop:** The script prints `STOP: no included drop-in directory`. Install the server package, or use only a directory that a main option file already includes. Do not create a new directory that MySQL never reads. When the package is installed and the script still stops, follow [Fallback for other configuration layouts](#fallback-for-other-configuration-layouts).

#### Fallback for other configuration layouts

Use this fallback when step 1 prints `STOP: no included drop-in directory`. Do not create `zz-production.cnf` until this fallback names an existing directory or an existing file. Steps 2 through 4 still search only `/etc/mysql/mysql.conf.d` and `/etc/my.cnf.d`. When the directory you must use is different, run the block at the end of this fallback and do not run steps 2 through 4.

With `--defaults-file`, MySQL reads that file and the files it includes. MySQL does not read the other default option files.

Read the service unit for `--defaults-file`, then list include directives:

```shell
DEFAULTS_FILE=
for unit in mysql.service mysqld.service; do
  found=$(systemctl cat "$unit" 2>/dev/null | sed -n 's/.*--defaults-file=\([^[:space:]"]*\).*/\1/p' | head -n 1)
  if [ -n "$found" ]; then
    DEFAULTS_FILE=$found
    echo "unit=$unit"
    break
  fi
done
echo "DEFAULTS_FILE=${DEFAULTS_FILE:-unset}"
if [ -n "$DEFAULTS_FILE" ]; then
  echo "The server reads this file only, plus files it includes."
  grep -nE '^[[:space:]]*!include' -- "$DEFAULTS_FILE"
else
  echo "No --defaults-file in mysql.service or mysqld.service."
  grep -nE '^[[:space:]]*!include' /etc/my.cnf /etc/mysql/my.cnf 2>/dev/null
  grep -nE '^[[:space:]]*!include' /etc/mysql/conf.d/*.cnf /etc/mysql/mysql.conf.d/*.cnf /etc/my.cnf.d/*.cnf 2>/dev/null
fi
```

Ignore a `--defaults-file` match that appears only in a comment. Use a match on an `ExecStart` or `Environment` line.

??? example "Expected output"

    ```{.text .no-copy}
    No --defaults-file in mysql.service or mysqld.service.
    /etc/mysql/my.cnf:22:!includedir /etc/mysql/conf.d/
    ```

    The paths and line numbers depend on the host. `grep` matches both `!include` and `!includedir`.

    **Pass:** `grep` prints an `!includedir` line in the file the server reads, and that directory exists. When more than one such line is printed, use the last directory that exists. Continue with the create block in this fallback. Do not add a new `!includedir` line. Do not create a directory.

    **Stop:** `grep` prints only `!include` of a single file. Back up that file, then edit that file. Do not create `zz-production.cnf` in a directory the server does not read.

    **Stop:** The only `!includedir` line is inside a file under `/etc/mysql/conf.d`, `/etc/mysql/mysql.conf.d`, or `/etc/my.cnf.d`, and the file the server reads does not itself name a directory. That line is a nested include. Use that directory only after you confirm the include chain, and only when the directory exists.

    **Stop:** `grep` prints no include line. Do not create a drop-in file. Return to [List every option file that MySQL can load](#list-every-option-file-that-mysql-can-load).

Replace the sample directory in the first line with the directory you selected. The block creates `zz-production.cnf` only when that file is absent, then saves a timestamped backup.

```shell
DROPIN_DIR=/etc/mysql/conf.d
DROPIN="$DROPIN_DIR/zz-production.cnf"
echo "DROPIN=$DROPIN"
if [ ! -d "$DROPIN_DIR" ]; then
  echo "STOP: directory does not exist: $DROPIN_DIR"
elif [ -e "$DROPIN" ]; then
  echo "STOP: file exists: $DROPIN"
else
  sudo tee "$DROPIN" >/dev/null <<'EOF'
[mysqld]
# Add production baseline settings in later steps.
EOF
  sudo chmod 644 "$DROPIN"
  sudo chown root:root "$DROPIN"
  sudo cp "$DROPIN" "$DROPIN.bak.$(date +%Y%m%d%H%M%S)"
  ls -l "$DROPIN" "$DROPIN".bak.*
fi
```

??? example "Expected output"

    ```{.text .no-copy}
    DROPIN=/etc/mysql/conf.d/zz-production.cnf
    -rw-r--r-- 1 root root 62 Aug  3 10:00 /etc/mysql/conf.d/zz-production.cnf
    -rw-r--r-- 1 root root 62 Aug  3 10:00 /etc/mysql/conf.d/zz-production.cnf.bak.20260803100000
    ```

    **Pass:** The command creates a new `root`-owned file with mode `644`, and a `.bak.<timestamp>` file appears beside it.

    **Stop:** The script prints `STOP: directory does not exist` or `STOP: file exists`. Do not overwrite an existing file.

Keep this shell open. Edit with `sudoedit "$DROPIN"`. On rollback, restore that same path with `sudo cp "$DROPIN.bak.TIMESTAMP" "$DROPIN"`. Replace `TIMESTAMP` with the suffix from the `ls` line. Then validate and restart with [Apply the baseline](#apply-the-baseline) and [Roll back after a failed restart](#roll-back-after-a-failed-restart). The rollback script does not search this directory.

2. Create the drop-in file only if the file is absent. Stay in the same shell so `DROPIN_DIR` is still set. This block selects the directory again so you can paste it alone. It does not close the shell when the file is already present:

    ```shell
    DROPIN_DIR=
    INCLUDED=$(sed -n 's/^[[:space:]]*!includedir[[:space:]][[:space:]]*//p' /etc/my.cnf /etc/mysql/my.cnf 2>/dev/null | tr -d '\r' | sed 's/[[:space:]]*$//; s:/*$::')
    for dir in /etc/mysql/mysql.conf.d /etc/my.cnf.d; do
      if [ -d "$dir" ] && printf '%s\n' "$INCLUDED" | grep -qxF -- "$dir"; then
        DROPIN_DIR=$dir
        break
      fi
    done
    if [ -z "$DROPIN_DIR" ]; then
      echo "STOP: no included drop-in directory. Checked /etc/mysql/mysql.conf.d and /etc/my.cnf.d."
    else
      DROPIN="$DROPIN_DIR/zz-production.cnf"
      echo "DROPIN=$DROPIN"
      if [ -e "$DROPIN" ]; then
        echo "STOP: file exists: $DROPIN"
      else
        sudo tee "$DROPIN" >/dev/null <<'EOF'
    [mysqld]
    # Add production baseline settings in later steps.
    EOF
        sudo chmod 644 "$DROPIN"
        sudo chown root:root "$DROPIN"
        ls -l "$DROPIN"
      fi
    fi
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        DROPIN=/etc/mysql/mysql.conf.d/zz-production.cnf
        -rw-r--r-- 1 root root 62 Aug  3 10:00 /etc/mysql/mysql.conf.d/zz-production.cnf
        ```

        On Red Hat Enterprise Linux and Oracle Linux the path is `/etc/my.cnf.d/zz-production.cnf`.

        **Pass:** The command creates a new `root`-owned file with mode `644`.

        **Stop:** The script prints `STOP: file exists` or `STOP: no included drop-in directory`. Do not overwrite an existing file. Save a backup first, then edit that file.

3. Save a timestamped backup after the file exists and before every edit:

    ```shell
    DROPIN_DIR=
    INCLUDED=$(sed -n 's/^[[:space:]]*!includedir[[:space:]][[:space:]]*//p' /etc/my.cnf /etc/mysql/my.cnf 2>/dev/null | tr -d '\r' | sed 's/[[:space:]]*$//; s:/*$::')
    for dir in /etc/mysql/mysql.conf.d /etc/my.cnf.d; do
      if [ -d "$dir" ] && printf '%s\n' "$INCLUDED" | grep -qxF -- "$dir"; then
        DROPIN_DIR=$dir
        break
      fi
    done
    if [ -z "$DROPIN_DIR" ]; then
      echo "STOP: no included drop-in directory. Checked /etc/mysql/mysql.conf.d and /etc/my.cnf.d."
    fi
    if [ -n "$DROPIN_DIR" ]; then
      DROPIN="$DROPIN_DIR/zz-production.cnf"
      echo "DROPIN=$DROPIN"
      sudo cp "$DROPIN" "$DROPIN.bak.$(date +%Y%m%d%H%M%S)"
      ls -l "$DROPIN".bak.*
    fi
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        DROPIN=/etc/mysql/mysql.conf.d/zz-production.cnf
        -rw-r--r-- 1 root root 62 Aug  3 10:01 /etc/mysql/mysql.conf.d/zz-production.cnf.bak.20260803100100
        ```

        **Pass:** A new `.bak.<timestamp>` file appears beside the drop-in file.

        **Stop:** The copy fails, or the script prints `STOP: no included drop-in directory`. Fix permissions or free space before you edit.

4. Edit the drop-in file as the `root` operating system user. Place production settings under the `[mysqld]` section.

    ```shell
    DROPIN_DIR=
    INCLUDED=$(sed -n 's/^[[:space:]]*!includedir[[:space:]][[:space:]]*//p' /etc/my.cnf /etc/mysql/my.cnf 2>/dev/null | tr -d '\r' | sed 's/[[:space:]]*$//; s:/*$::')
    for dir in /etc/mysql/mysql.conf.d /etc/my.cnf.d; do
      if [ -d "$dir" ] && printf '%s\n' "$INCLUDED" | grep -qxF -- "$dir"; then
        DROPIN_DIR=$dir
        break
      fi
    done
    if [ -z "$DROPIN_DIR" ]; then
      echo "STOP: no included drop-in directory. Checked /etc/mysql/mysql.conf.d and /etc/my.cnf.d."
    fi
    if [ -n "$DROPIN_DIR" ]; then
      DROPIN="$DROPIN_DIR/zz-production.cnf"
      echo "DROPIN=$DROPIN"
      sudoedit "$DROPIN"
    fi
    ```

5. Validate the configuration before you restart:

    ```shell
    sudo mysqld --validate-config
    echo "exit_status=$?"
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        exit_status=0
        ```

        **Pass:** No error text. Exit status is `0`.

        Exit status `0` means the server parsed the option files. The check does not allocate `innodb_buffer_pool_size`. A parsed file can still fail at restart when the buffer pool does not fit in memory. See the 16 GiB example under [Buffer pool size](#buffer-pool-size).

        **Stop:** Any error text, or a non-zero exit status. Fix the option file before restart.

!!! tip

    Keep one production drop-in file under version control. Avoid mixed edits across many option files when one controlled file can hold the baseline.

## Day-1 host checks

Run these checks on the database host before you tune MySQL.

Open a client for the SQL on this page. After `mysql_secure_installation`, connect with the root password:

```shell
mysql -u root -p
```

If that client rejects the password, start the client as the operating-system `root` user:

```shell
sudo mysql
```

Use that same form in shell commands that call `mysql`. When password login fails, replace `mysql -u root -p` with `sudo mysql`.

For each check:

* **Pass** means continue.

* **Stop** means fix the issue before memory or connection changes.

### Storage and free space

Check free space for the data directory and related mounts:

```shell
df -hT /
df -hT /var/lib/mysql
```

??? example "Expected output"

    ```{.text .no-copy}
    Filesystem     Type  Size  Used Avail Use% Mounted on
    /dev/sda1      ext4  200G   40G  160G  20% /
    /dev/sdb1      xfs   500G  120G  380G  24% /var/lib/mysql
    ```

    **Pass:** Each MySQL mount has free space for data growth, binary logs, and temporary files. A starting point is to investigate when use reaches 80%. Your growth rate and backup size can require an earlier or later point. 80% is not a universal failure rule.

    **Stop:** A MySQL mount is read-only, missing, or reports an unexpected file system type for your plan. Also stop when use reaches the percentage in your capacity plan. When the plan sets no percentage, investigate at 80%.

Confirm MySQL paths:

```sql
SHOW VARIABLES WHERE Variable_name IN (
    'datadir',
    'innodb_log_group_home_dir',
    'tmpdir',
    'log_bin_basename',
    'slow_query_log_file',
    'log_error'
);
```

??? example "Expected output"

    ```{.text .no-copy}
    +---------------------------+----------------------------------+
    | Variable_name             | Value                            |
    +---------------------------+----------------------------------+
    | datadir                   | /var/lib/mysql/                  |
    | innodb_log_group_home_dir | ./                               |
    | log_bin_basename          | /var/lib/mysql/binlog            |
    | log_error                 | /var/log/mysql/error.log         |
    | slow_query_log_file       | /var/lib/mysql/host-slow.log     |
    | tmpdir                    | /tmp                             |
    +---------------------------+----------------------------------+
    ```

    Paths depend on the install method and configuration.

    **Pass:** Each path exists on a mount with free space, and you know which mount holds data, logs, and temporary files.

    **Stop:** A required path is missing, points to a full mount, or places temporary files on an unsuitable filesystem.

### Direct I/O and flush method

Confirm the active flush method:

```sql
SHOW VARIABLES LIKE 'innodb_flush_method';
```

??? example "Expected output"

    ```{.text .no-copy}
    +---------------------+----------+
    | Variable_name       | Value    |
    +---------------------+----------+
    | innodb_flush_method | O_DIRECT |
    +---------------------+----------+
    ```

    **Pass:** The value is `O_DIRECT` on a supported Linux data filesystem.

    **Stop and review:** The value is `fsync` and you expected direct I/O. Confirm filesystem support before you force `O_DIRECT`.

Test direct I/O on the same filesystem as the data directory. The script writes only when it can place the test directory on that filesystem and outside the data directory. A directory inside the data directory is a schema. When the data directory is the mount point, the script stops and does not create a directory. The script creates a new, uniquely named directory with `mktemp -d`. The script never changes the owner or mode of an existing directory. `dd` uses `conv=excl`, so `dd` fails when the test file already exists and does not overwrite that file. The cleanup removes only the one file and the empty directory that the script created. When the directory check fails, the script removes the empty directory it just created and does not remove anything else.

The client prompts for the root password. If that login fails, rerun the block with `sudo mysql` in place of `mysql -u root -p`.

```shell
if ! DATADIR=$(mysql -u root -p -Nse "SELECT @@datadir"); then
  DATADIR=$(sudo mysql -Nse "SELECT @@datadir")
fi
DATADIR=${DATADIR%/}
FS_ROOT=$(df --output=target "$DATADIR" | tail -n 1)
echo "DATADIR=$DATADIR"
echo "FS_ROOT=$FS_ROOT"
if [ -z "$DATADIR" ] || [ -z "$FS_ROOT" ]; then
  echo "STOP: could not resolve datadir or its mount"
elif [ "$FS_ROOT" = "$DATADIR" ]; then
  echo "STOP: datadir is the mount point. Do not create a directory inside it. Use the innodb_flush_method value from the previous query."
else
  case "$FS_ROOT/" in
    "$DATADIR"/*)
      echo "STOP: mount point is inside datadir: $FS_ROOT"
      ;;
    *)
      TESTDIR=$(sudo mktemp -d "$FS_ROOT/mysql-dio-check.XXXXXX")
      if [ -z "$TESTDIR" ] || [ ! -d "$TESTDIR" ] || [ "$(sudo stat -c '%U:%a' "$TESTDIR")" != "root:700" ]; then
        echo "STOP: could not create a root-owned test directory under $FS_ROOT"
        if [ -n "$TESTDIR" ] && [ -d "$TESTDIR" ]; then
          if ! sudo rmdir -- "$TESTDIR"; then
            echo "STOP: left test directory in place: $TESTDIR"
          fi
        fi
      else
        echo "TESTDIR=$TESTDIR"
        sudo dd if=/dev/zero of="$TESTDIR/dio-test" bs=4096 count=1 oflag=direct conv=excl
        echo "dd_exit_status=$?"
        sudo rm -f -- "$TESTDIR/dio-test"
        sudo rmdir -- "$TESTDIR"
      fi
      ;;
  esac
fi
```

??? example "Expected output"

    When `datadir` is the mount point, as in the storage example above:

    ```{.text .no-copy}
    DATADIR=/var/lib/mysql
    FS_ROOT=/var/lib/mysql
    STOP: datadir is the mount point. Do not create a directory inside it. Use the innodb_flush_method value from the previous query.
    ```

    When the mount point is a parent of `datadir`:

    ```{.text .no-copy}
    DATADIR=/var/lib/mysql/data
    FS_ROOT=/var/lib/mysql
    TESTDIR=/var/lib/mysql/mysql-dio-check.a1B2c3
    1+0 records in
    1+0 records out
    4096 bytes (4.1 kB, 4.0 KiB) copied, 0.000123 s, 33.3 MB/s
    dd_exit_status=0
    ```

    **Pass:** `dd` writes one 4096-byte record, exit status is `0`, and the cleanup commands remove only the test file and the empty directory that the script created.

    **Skipped test:** The script prints `STOP: datadir is the mount point`. The script created nothing and did not test direct I/O. Keep the current `innodb_flush_method`. A skipped test is not a pass.

    **Stop:** `dd` prints `Invalid argument`, another I/O error, or a non-zero exit status. Do not force `innodb_flush_method=O_DIRECT` on that filesystem. Also stop when the script prints `STOP: could not resolve datadir`, `STOP: mount point is inside datadir`, `STOP: could not create a root-owned test directory`, or `STOP: left test directory in place`.

    A passing `dd` test does not prove that every InnoDB I/O operation works on this filesystem. After you restart MySQL with direct I/O, check the error log for I/O warnings.

### Memory and swap

Check physical memory and swap:

```shell
free -h
swapon --show
```

??? example "Expected output"

    ```{.text .no-copy}
                  total        used        free      shared  buff/cache   available
    Mem:           15Gi       2.1Gi       8.0Gi       100Mi       5.0Gi        12Gi
    Swap:         2.0Gi          0B       2.0Gi

    NAME      TYPE      SIZE USED PRIO
    /swapfile file      2.0G   0B   -2
    ```

    **Pass:** Available memory covers the planned buffer pool plus operating-system headroom. Swap used stays near zero under normal load.

    **Stop:** Available memory cannot support the planned buffer pool. Sustained swap use already appears for MySQL. Resolve memory pressure before you raise `innodb_buffer_pool_size`.

### Logs

Confirm that error and slow query logging are active:

```sql
SHOW VARIABLES WHERE Variable_name IN (
    'log_error',
    'slow_query_log',
    'slow_query_log_file',
    'long_query_time',
    'log_output'
);
```

??? example "Expected output"

    ```{.text .no-copy}
    +---------------------+------------------------------+
    | Variable_name       | Value                        |
    +---------------------+------------------------------+
    | log_error           | /var/log/mysql/error.log     |
    | log_output          | FILE                         |
    | long_query_time     | 1.000000                     |
    | slow_query_log      | ON                           |
    | slow_query_log_file | /var/lib/mysql/host-slow.log |
    +---------------------+------------------------------+
    ```

    **Pass:** `log_error` points to a writable file. For this baseline, `slow_query_log` is `ON` and `log_output` includes `FILE`.

    **Stop:** `log_error` is empty or unwritable. Slow logging remains off when you planned to enable it. Fix logging before you continue.

Check recent error log lines. Read the path from the server. Package layouts differ: some use `/var/log/mysql/error.log`, and the Oracle Linux quickstart records the temporary password in `/var/log/mysqld.log`.

```shell
if ! LOG_ERROR=$(mysql -u root -p -Nse "SELECT @@log_error"); then
  LOG_ERROR=$(sudo mysql -Nse "SELECT @@log_error")
fi
echo "LOG_ERROR=$LOG_ERROR"
if [ -z "$LOG_ERROR" ]; then
  echo "STOP: @@log_error is empty"
else
  sudo tail -n 50 -- "$LOG_ERROR"
fi
```

??? example "Expected output"

    ```{.text .no-copy}
    LOG_ERROR=/var/log/mysql/error.log
    ...
    [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections.
    ```

    The printed path is the file you tail. A Red Hat or Oracle Linux package often prints `/var/log/mysqld.log`.

    **Pass:** The log shows a ready-for-connections message. No unresolved `[ERROR]` lines block startup.

    **Stop:** The log shows startup failures, permission errors, or repeated severe errors. Resolve those errors before configuration changes.

## Day-1 checklist

### Storage

* Place data files, redo logs, binary logs, and temporary files on storage with predictable latency.

* Confirm that the Linux file system supports direct I/O.

* Monitor free space for each data directory and log directory.

* Store backups outside the database host.

* Test a restore from the backup.

### Memory

* Set `innodb_buffer_pool_size` to 60–70% of physical random-access memory (RAM) on a dedicated database host.

* Use a lower percentage when MySQL shares the host with other services.

* Reserve memory for the operating system, Performance Schema, connections, temporary tables, sorts, replication, and backup tools.

* Test the highest expected connection count.

* Monitor swap use, resident memory, buffer pool hit rate, and temporary table use.

Connection buffers use memory only when a connection needs each buffer. Actual use depends on workload concurrency.

Check the buffer pool hit rate:

```sql
SHOW GLOBAL STATUS WHERE Variable_name IN (
    'Innodb_buffer_pool_read_requests',
    'Innodb_buffer_pool_reads'
);
```

??? example "Expected output"

    ```{.text .no-copy}
    +-----------------------------------+-------------+
    | Variable_name                     | Value       |
    +-----------------------------------+-------------+
    | Innodb_buffer_pool_read_requests  | 125000000   |
    | Innodb_buffer_pool_reads          | 250000      |
    +-----------------------------------+-------------+
    ```

Calculate the hit rate:

`1 - (Innodb_buffer_pool_reads / Innodb_buffer_pool_read_requests)`

`Innodb_buffer_pool_read_requests` and `Innodb_buffer_pool_reads` are cumulative since server startup. For the sample values, the hit rate is `1 - (250000 / 125000000) = 0.998`. If `Innodb_buffer_pool_read_requests` is `0`, do not divide. Wait for representative load, then run the query again.

A result near `1` means MySQL serves most reads from memory.

**Pass:** After representative load, the hit rate is at or above [Insert hit-rate starting point]. That starting point depends on your working set and latency goal. It is not a universal pass rule. The sample result `0.998` shows the formula only.

**Stop and review:** The hit rate stays below [Insert hit-rate starting point] after representative load. Confirm that the working set exceeds the buffer pool before you raise memory further.

### Connections

* Add all application connection pool limits.

* Add connections for administration and metrics collection.

* Add a small margin for failures.

* Use the result for `max_connections`.

* Set limits on application connection pools.

* Queue or reject excess application work before MySQL reaches capacity.

* Reserve an administrative connection that still accepts logins when `max_connections` is exhausted. The server opens this interface only when `admin_address` is set at startup. `admin_port` defaults to `33062`. Add these lines to the drop-in file under `[mysqld]`, then restart during the maintenance window in [Apply the baseline](#apply-the-baseline):

    ```ini
    [mysqld]
    admin_address=127.0.0.1
    admin_port=33062
    ```

    The `admin` account must already exist. The `GRANT` statement does not create an account. Create the account with the steps in [First five minutes after installation](first-five-minutes.md). Then grant `SERVICE_CONNECTION_ADMIN` before client traffic returns:

    ```sql
    GRANT SERVICE_CONNECTION_ADMIN ON *.* TO 'admin'@'localhost';
    ```

    The administrative interface accepts TCP/IP connections only. A Unix-socket login never uses this interface. A Unix-socket login matches an account whose host is `localhost`. A TCP connection to `127.0.0.1` matches by host name resolution. When `@@skip_name_resolve` is `ON`, the server matches only IP addresses, so `'admin'@'localhost'` does not match. Check the setting:

    ```sql
    SELECT @@skip_name_resolve;
    ```

    When the value is `1`, create the account and grant the privilege for the loopback address instead:

    ```sql
    CREATE USER 'admin'@'127.0.0.1' IDENTIFIED BY 'YourStrongPassword_12';
    GRANT SERVICE_CONNECTION_ADMIN ON *.* TO 'admin'@'127.0.0.1';
    ```

    After the restart, confirm that the server listens on the administrative port:

    ```shell
    sudo ss -ltn 'sport = :33062'
    ```

    Connect on the administrative port with a TCP connection, and confirm which account matched:

    ```shell
    mysql --protocol=TCP --host=127.0.0.1 --port=33062 -u admin -p -e "SELECT CURRENT_USER();"
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        State   Recv-Q  Send-Q  Local Address:Port  Peer Address:Port
        LISTEN  0       151     127.0.0.1:33062     0.0.0.0:*

        +----------------------+
        | CURRENT_USER()       |
        +----------------------+
        | admin@localhost      |
        +----------------------+
        ```

        With `skip_name_resolve` enabled, `CURRENT_USER()` returns `admin@127.0.0.1`.

        **Pass:** `ss` lists a `LISTEN` line for `127.0.0.1:33062`, and the connection returns the account that you granted.

        **Stop:** `ss` prints no `LISTEN` line, or the client prints `Access denied`. Check that the `[mysqld]` lines are in the file that the server loads, that the account exists, and that the host part matches the connection.

    When the administrative interface is not available, MySQL permits one extra connection on the ordinary interfaces to an account that has the `CONNECTION_ADMIN` privilege, such as `root`. Connect on the Unix socket with `sudo mysql` and use that connection to check or stop sessions. If the restart fails after you add the `admin_address` and `admin_port` lines, follow [Roll back after a failed restart](#roll-back-after-a-failed-restart).

* Create an alert when `Threads_connected` approaches `max_connections`. In Percona Monitoring and Management (PMM), create an alert rule from the built-in `MySQL connections in use` template. By default, the template alerts when active connections exceed 80% of the maximum. Read [List of available alert templates](https://docs.percona.com/percona-monitoring-and-management/3/alert/templates_list.html) and [Alert rules and alert templates](https://docs.percona.com/percona-monitoring-and-management/3/alert/alert_rules.html).

Use the default one-thread-per-connection model for most workloads. Consider the Percona thread pool when many active threads compete for CPU and tests with representative load show a throughput benefit. Connection count alone does not decide this. During peak load, compare `Threads_running` with the number of CPU cores. Read [Thread pool](threadpool.md).

Check active, peak, and maximum connection values:

```sql
SHOW GLOBAL STATUS WHERE Variable_name IN ('Threads_connected', 'Max_used_connections');
SHOW VARIABLES LIKE 'max_connections';
```

??? example "Expected output"

    ```{.text .no-copy}
    +----------------------+-------+
    | Variable_name        | Value |
    +----------------------+-------+
    | Max_used_connections | 84    |
    | Threads_connected    | 32    |
    +----------------------+-------+

    +-----------------+-------+
    | Variable_name   | Value |
    +-----------------+-------+
    | max_connections | 200   |
    +-----------------+-------+
    ```

    The connection values depend on the workload. `Max_used_connections` must remain below `max_connections`.

    **Pass:** `Max_used_connections` stays below `max_connections`. A starting point is to keep the peak under 80% of `max_connections`, the same default as the PMM template on this page. Traffic spikes can require a larger or smaller margin. 80% is not a universal failure rule.

    **Stop:** `Max_used_connections` equals `max_connections`, or applications already hit connection errors. Raise capacity only after you confirm application pool limits.

### Logs and observability

* Collect, retain, and monitor the error log.

* Enable the slow query log with a cautious threshold.

* Adjust the threshold and sample rate after you measure log volume.

* Use `log_output=FILE` when Percona Monitoring and Management (PMM) Query Analytics reads the slow query log.

* Define retention and rotation for error, slow, binary, and audit logs.

* Create alerts for availability, disk space, replication lag, connection pressure, and resource saturation.

Logs can use substantial I/O capacity and disk space.

## Calculate memory and connection settings

### Buffer pool size

Use this formula on a dedicated MySQL host:

`innodb_buffer_pool_size ≈ total_RAM × 0.60 to 0.70`

Example for a 16 GiB host:

* `16 × 0.70 ≈ 11.2`

* Use `innodb_buffer_pool_size = 11G`

MySQL 8.4 sets `temptable_max_ram` to 3% of total memory, with a minimum of 1 GiB. 3% of 16 GiB is below 1 GiB, so the minimum applies. `11G` plus that 1 GiB leaves about 4 GiB for the operating system and the other consumers below.

Leave memory for the following consumers:

* Operating system caches and kernel work

* Performance Schema

* Per-connection buffers

* Temporary tables and sort buffers

* Replication and backup tools

Use a lower percentage when other services share the host.

#### Worked memory budget

The 60–70% figure is a starting point. Total RAM is the wrong input when a container or a service unit limits memory. Read the limit that applies to MySQL:

```shell
cat /sys/fs/cgroup/memory.max
systemctl show mysql -p MemoryMax
```

On cgroup version 1, read `/sys/fs/cgroup/memory/memory.limit_in_bytes` instead. The value `max` in the file, or `infinity` from `systemctl`, means that no limit is set. Use `mysqld` in the `systemctl` command when your unit has that name. When a limit is set, use the limit in place of total RAM in the formula.

Measure the per-connection buffers and the Performance Schema memory on your server:

```sql
SELECT @@sort_buffer_size, @@join_buffer_size, @@read_buffer_size,
       @@read_rnd_buffer_size, @@thread_stack, @@binlog_cache_size,
       @@max_connections;

SELECT ROUND(SUM(CURRENT_NUMBER_OF_BYTES_USED) / 1024 / 1024) AS performance_schema_mib
FROM performance_schema.memory_summary_global_by_event_name
WHERE EVENT_NAME LIKE 'memory/performance_schema/%';
```

Add the first six values of the first query to estimate the worst case for one connection. A connection allocates a buffer only when a statement needs the buffer.

The following example assumes that the first query returns a worst case of 2 MiB for one connection. The example assumes that the second query returns 512 MiB. Replace both values with your measurements:

| Consumer | Calculation | Memory |
|---|---|---|
| Buffer pool | `innodb_buffer_pool_size` | 11 GiB |
| Redo log buffer | `innodb_log_buffer_size` default of 64 MiB | 0.06 GiB |
| Temporary tables | `temptable_max_ram` minimum of 1 GiB | 1 GiB |
| Connection buffers | 200 connections × 2 MiB | 0.39 GiB |
| Performance Schema | Measured value of 512 MiB | 0.5 GiB |
| Total for MySQL | Sum of the rows above | about 12.95 GiB |
| Remainder on a 16 GiB host | 16 GiB − 12.95 GiB | about 3 GiB |

The remaining 3 GiB must cover the operating system, file system cache, replication, and backup tools. Lower `innodb_buffer_pool_size` when the remainder is too small for your workload.

### Connection limit

Use this formula:

`max_connections = application_pool_total + admin_connections + monitoring_connections + margin`

Example:

* Three application pools use 50 connections each: `150`

* Administration needs `10`

* Monitoring needs `10`

* Margin is `30`

* Result: `max_connections = 200`

Keep each application pool below its own limit. Do not rely on MySQL alone to absorb unbounded connection growth.

Each connection can allocate buffers, so `max_connections` sets the worst-case connection memory. With the 2 MiB assumption from the [memory budget](#worked-memory-budget), 200 connections can use up to 400 MiB. Raising `max_connections` to `400` raises that worst case to 800 MiB. Raising the limit does not make a query run faster.

When applications report `Too many connections`, read the observed peak before you raise the limit:

```sql
SHOW GLOBAL STATUS WHERE Variable_name IN (
    'Connection_errors_max_connections',
    'Max_used_connections',
    'Threads_connected'
);
SHOW VARIABLES LIKE 'max_connections';
```

??? example "Expected output"

    ```{.text .no-copy}
    +-----------------------------------+-------+
    | Variable_name                     | Value |
    +-----------------------------------+-------+
    | Connection_errors_max_connections | 0     |
    | Max_used_connections              | 84    |
    | Threads_connected                 | 32    |
    +-----------------------------------+-------+

    +-----------------+-------+
    | Variable_name   | Value |
    +-----------------+-------+
    | max_connections | 200   |
    +-----------------+-------+
    ```

    **Pass:** `Max_used_connections` is below `max_connections`, and `Connection_errors_max_connections` is `0`.

    **Stop and review:** `Connection_errors_max_connections` is greater than `0`, or `Max_used_connections` equals `max_connections`. Compare the peak with the total of your application pool limits. When the peak exceeds that total, fix the application pool or connection leak first. Raise `max_connections` only when the peak matches pool limits that you set, and recheck the memory budget.

## Recommended production `my.cnf` baseline

Configure a dedicated MySQL host as follows:

* Run a Linux operating system.

* Allocate 16 GiB of RAM.

* Use a solid-state drive (SSD) or Non-Volatile Memory Express (NVMe) storage device.

In this example, replace each value marked `CHANGE` before deployment.

```ini
[mysqld]

# Memory
# CHANGE: Use 60-70% of RAM on a dedicated database host.
# 11G is about 70% of the RAM on a 16 GiB host.
innodb_buffer_pool_size = 11G

# Connections
# CHANGE: Add application pool limits, metrics collection, and an administrative margin.
max_connections = 200

# Storage and durability
# MySQL 8.4 selects O_DIRECT on supported Linux systems.
# Set this value only after you validate the file system and storage.
# innodb_flush_method = O_DIRECT
innodb_flush_log_at_trx_commit = 1
sync_binlog = 1

# Logs
log_output = FILE
slow_query_log = ON
long_query_time = 1
log_slow_verbosity = standard

# Keep binary logs for point-in-time recovery and replication.
# CHANGE: Choose a retention period from the backup and recovery policy.
# 604800 seconds is 7 days. This value is an example.
binlog_expire_logs_seconds = 604800
```

??? example "Expected result"

    The configuration file contains one `[mysqld]` section with the selected production values.

The durability values protect committed transactions during an operating system or host failure.

Lower values for `innodb_flush_log_at_trx_commit` or `sync_binlog` can increase throughput. This change can also create a documented data loss period.

The value `604800` seconds is 7 days. This value is an example and not a universally safe retention period. Choose a retention period that covers all of the following:

* The interval between full backups, plus the time that a restore needs.

* The point-in-time recovery window that your policy requires.

* The longest replication delay that a replica can reach before the replica catches up.

`binlog_expire_logs_seconds` removes old binary logs only. The setting does not enable binary logging. MySQL 8.4 enables binary logging by default, unless the server starts with `--skip-log-bin` or `--disable-log-bin`. Point-in-time recovery and replication from this server require binary logging. Confirm `log_bin` in the [Apply the baseline](#apply-the-baseline) procedure.

### Apply the baseline

1. Save a copy of the active configuration. See [Find and edit the active configuration file](#find-and-edit-the-active-configuration-file).

2. Replace the memory, connection, and retention values.

3. Validate the configuration:

    ```shell
    sudo mysqld --validate-config
    echo "exit_status=$?"
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        exit_status=0
        ```

        **Pass:** No error text. Exit status is `0`.

        Exit status `0` means the server parsed the option files. The check does not allocate `innodb_buffer_pool_size`. A parsed file can still fail at restart when the buffer pool does not fit in memory.

        **Stop:** Any error text, or a non-zero exit status. Do not restart.

4. Record the service unit and the error-log path before you restart. A server that fails to start cannot answer the SQL query for `@@log_error`. Keep this shell open until the restart check passes, and write down both values:

    ```shell
    if systemctl cat mysql.service >/dev/null 2>&1; then
      MYSQL_UNIT=mysql
    elif systemctl cat mysqld.service >/dev/null 2>&1; then
      MYSQL_UNIT=mysqld
    else
      echo "STOP: neither mysql.service nor mysqld.service is installed"
      MYSQL_UNIT=
    fi
    echo "MYSQL_UNIT=${MYSQL_UNIT:-unset}"
    if ! LOG_ERROR=$(mysql -u root -p -Nse "SELECT @@log_error"); then
      LOG_ERROR=$(sudo mysql -Nse "SELECT @@log_error")
    fi
    echo "LOG_ERROR=${LOG_ERROR:-unset}"
    if [ -z "$LOG_ERROR" ]; then
      echo "STOP: @@log_error is empty. Do not restart until you know where the server writes its error log."
    elif [ "$LOG_ERROR" = "stderr" ]; then
      echo "The server logs to stderr. Read the journalctl output for $MYSQL_UNIT after the restart."
    else
      sudo ls -l -- "$LOG_ERROR"
    fi
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        MYSQL_UNIT=mysql
        LOG_ERROR=/var/log/mysql/error.log
        -rw-r----- 1 mysql adm 8421 Aug  3 09:58 /var/log/mysql/error.log
        ```

        **Pass:** `MYSQL_UNIT` names a unit, and `LOG_ERROR` names an existing file or `stderr`.

        **Stop:** `MYSQL_UNIT` is `unset`, or the script prints `STOP: @@log_error is empty`. Do not restart.

5. Restart MySQL during a maintenance period. The block selects the `mysql` unit or the `mysqld` unit, whichever is installed:

    ```shell
    if systemctl cat mysql.service >/dev/null 2>&1; then
      MYSQL_UNIT=mysql
    elif systemctl cat mysqld.service >/dev/null 2>&1; then
      MYSQL_UNIT=mysqld
    else
      echo "STOP: neither mysql.service nor mysqld.service is installed"
      MYSQL_UNIT=
    fi
    echo "MYSQL_UNIT=${MYSQL_UNIT:-unset}"
    if [ -n "$MYSQL_UNIT" ]; then
      sudo systemctl restart "$MYSQL_UNIT"
    fi
    ```

6. Check the service state and error log. The check uses the path that you recorded and does not query MySQL:

    ```shell
    if systemctl cat mysql.service >/dev/null 2>&1; then
      MYSQL_UNIT=mysql
    elif systemctl cat mysqld.service >/dev/null 2>&1; then
      MYSQL_UNIT=mysqld
    else
      echo "STOP: neither mysql.service nor mysqld.service is installed"
      MYSQL_UNIT=
    fi
    echo "MYSQL_UNIT=${MYSQL_UNIT:-unset}"
    if [ -n "$MYSQL_UNIT" ]; then
      sudo systemctl status "$MYSQL_UNIT" --no-pager
      sudo journalctl -u "$MYSQL_UNIT" -n 50 --no-pager
    fi
    echo "LOG_ERROR=${LOG_ERROR:-unset}"
    if [ -z "$LOG_ERROR" ]; then
      echo "STOP: LOG_ERROR is not set. Use the path that you recorded before the restart."
    elif [ "$LOG_ERROR" = "stderr" ]; then
      echo "The server logs to stderr. Read the journalctl lines above."
    else
      sudo tail -n 100 -- "$LOG_ERROR"
    fi
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        MYSQL_UNIT=mysql
        Active: active (running)
        LOG_ERROR=/var/log/mysql/error.log
        ...
        [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections.
        ```

        **Pass:** The unit is `active (running)`. The error log shows ready for connections.

        **Stop:** The unit is `failed` or `inactive`, or the error log shows startup errors. Follow [Roll back after a failed restart](#roll-back-after-a-failed-restart).

7. Confirm the active values:

    ```sql
    SHOW VARIABLES WHERE Variable_name IN (
        'binlog_expire_logs_seconds',
        'innodb_buffer_pool_size',
        'innodb_flush_log_at_trx_commit',
        'innodb_flush_method',
        'log_bin',
        'log_output',
        'log_slow_verbosity',
        'long_query_time',
        'max_connections',
        'slow_query_log',
        'sync_binlog'
    );
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        +------------------------------------+-------------+
        | Variable_name                      | Value       |
        +------------------------------------+-------------+
        | binlog_expire_logs_seconds         | 604800      |
        | innodb_buffer_pool_size            | 11811160064 |
        | innodb_flush_log_at_trx_commit     | 1           |
        | innodb_flush_method                | O_DIRECT    |
        | log_bin                            | ON          |
        | log_output                         | FILE        |
        | log_slow_verbosity                 | standard    |
        | long_query_time                    | 1.000000    |
        | max_connections                    | 200         |
        | slow_query_log                     | ON          |
        | sync_binlog                        | 1           |
        +------------------------------------+-------------+
        ```

        MySQL can return `fsync` for `innodb_flush_method`. The value depends on direct I/O support.

        **Pass:** Each value matches the drop-in file that you intended to load. `log_bin` is `ON` when you need point-in-time recovery or replication from this server.

        **Stop:** A value still comes from an older option file. Recheck file order and duplicate settings. Also stop when `log_bin` is `OFF` and you need point-in-time recovery or replication. Search the option files for `skip-log-bin` or `disable-log-bin`, remove the line, and restart.

### Roll back after a failed restart

If MySQL fails to start after a configuration change, restore the previous file and restart.

1. Check the service state and the last error lines. Do not query MySQL for the log path. Use the `LOG_ERROR` value that you recorded before the restart:

    ```shell
    if systemctl cat mysql.service >/dev/null 2>&1; then
      MYSQL_UNIT=mysql
    elif systemctl cat mysqld.service >/dev/null 2>&1; then
      MYSQL_UNIT=mysqld
    else
      echo "STOP: neither mysql.service nor mysqld.service is installed"
      MYSQL_UNIT=
    fi
    echo "MYSQL_UNIT=${MYSQL_UNIT:-unset}"
    if [ -n "$MYSQL_UNIT" ]; then
      sudo systemctl status "$MYSQL_UNIT" --no-pager
      sudo journalctl -u "$MYSQL_UNIT" -n 50 --no-pager
    fi
    echo "LOG_ERROR=${LOG_ERROR:-unset}"
    if [ -z "$LOG_ERROR" ]; then
      echo "LOG_ERROR is not set. These option-file lines set the error log:"
      grep -rhE '^[[:space:]]*log[-_]error' /etc/my.cnf /etc/my.cnf.d /etc/mysql 2>/dev/null
    elif [ "$LOG_ERROR" = "stderr" ]; then
      echo "The server logs to stderr. Read the journalctl lines above."
    else
      sudo tail -n 100 -- "$LOG_ERROR"
    fi
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        MYSQL_UNIT=mysql
        Active: failed
        ...
        LOG_ERROR=/var/log/mysql/error.log
        [ERROR] [MY-000067] [Server] unknown variable 'example_bad_setting=1'.
        ```

        In a new shell, `LOG_ERROR` is `unset`. The script then prints the option-file lines that set the error log.

2. Restore the backup that you created before the edit:

    ```shell
    DROPIN_DIR=
    INCLUDED=$(sed -n 's/^[[:space:]]*!includedir[[:space:]][[:space:]]*//p' /etc/my.cnf /etc/mysql/my.cnf 2>/dev/null | tr -d '\r' | sed 's/[[:space:]]*$//; s:/*$::')
    for dir in /etc/mysql/mysql.conf.d /etc/my.cnf.d; do
      if [ -d "$dir" ] && printf '%s\n' "$INCLUDED" | grep -qxF -- "$dir"; then
        DROPIN_DIR=$dir
        break
      fi
    done
    if [ -z "$DROPIN_DIR" ]; then
      echo "STOP: no included drop-in directory. Checked /etc/mysql/mysql.conf.d and /etc/my.cnf.d."
    fi
    if [ -n "$DROPIN_DIR" ]; then
      DROPIN="$DROPIN_DIR/zz-production.cnf"
      echo "DROPIN=$DROPIN"
      ls -l "$DROPIN".bak.*
      sudo cp "$DROPIN.bak.TIMESTAMP" "$DROPIN"
    fi
    ```

    Replace `TIMESTAMP` with the backup suffix from your copy step. The `ls` line prints that suffix.

    When the drop-in file is not under `/etc/mysql/mysql.conf.d` or `/etc/my.cnf.d`, this script prints `STOP: no included drop-in directory`. Restore the backup path from [Fallback for other configuration layouts](#fallback-for-other-configuration-layouts) instead.

3. Validate the restored configuration:

    ```shell
    sudo mysqld --validate-config
    ```

    ??? example "Expected output"

        A valid configuration produces no output. The command returns exit status zero.

4. Start MySQL:

    ```shell
    if systemctl cat mysql.service >/dev/null 2>&1; then
      MYSQL_UNIT=mysql
    elif systemctl cat mysqld.service >/dev/null 2>&1; then
      MYSQL_UNIT=mysqld
    else
      echo "STOP: neither mysql.service nor mysqld.service is installed"
      MYSQL_UNIT=
    fi
    echo "MYSQL_UNIT=${MYSQL_UNIT:-unset}"
    if [ -n "$MYSQL_UNIT" ]; then
      sudo systemctl start "$MYSQL_UNIT"
    fi
    ```

5. Confirm that the service is active and that clients can connect:

    ```shell
    if systemctl cat mysql.service >/dev/null 2>&1; then
      MYSQL_UNIT=mysql
    elif systemctl cat mysqld.service >/dev/null 2>&1; then
      MYSQL_UNIT=mysqld
    else
      echo "STOP: neither mysql.service nor mysqld.service is installed"
      MYSQL_UNIT=
    fi
    echo "MYSQL_UNIT=${MYSQL_UNIT:-unset}"
    if [ -n "$MYSQL_UNIT" ]; then
      sudo systemctl is-active "$MYSQL_UNIT"
    fi
    mysql -u root -p -e "SELECT 1;" || sudo mysql -e "SELECT 1;"
    ```

    ??? example "Expected output"

        ```{.text .no-copy}
        MYSQL_UNIT=mysql
        active
        +---+
        | 1 |
        +---+
        | 1 |
        +---+
        ```

6. Fix the rejected setting offline. Validate again. Apply the change in a new maintenance window.

### MySQL 8.4 defaults

Review each MySQL 8.0 override before you use the override with MySQL 8.4.

MySQL 8.4 has the following defaults:

* `innodb_adaptive_hash_index=OFF`.

* `innodb_change_buffering=none`.

* `innodb_flush_method=O_DIRECT` on supported Linux systems. MySQL uses `fsync` as the fallback.

* `innodb_io_capacity=10000`. This value targets SSD and NVMe storage. Hard disk drives may require a lower value.

* `innodb_log_buffer_size=64M`.

* `innodb_numa_interleave=ON`.

* `temptable_max_ram` uses 3% of total memory. The minimum value is 1 GiB. The maximum value is 4 GiB.

Read [Defaults and tuning guidance for MySQL 8.4](8.4-defaults-and-tuning.md) for more details.

## Percona feature quick-activation matrix

Each command requires the related package or component library. Run Structured Query Language (SQL) commands with the required administrative privileges.

Some features also require tables or policy definitions. Follow the linked procedure before activation.

Each feature below lists prerequisites, activation, restart behavior, verification, and rollback separately.

### Thread pool

**Prerequisites:** Run a high-concurrency test with representative load. Use the thread pool only when that test shows a throughput benefit. Read [Thread pool](threadpool.md).

**Activation:** Add `thread_handling=pool-of-threads` under `[mysqld]` in the drop-in file.

**Restart:** Required. In [Thread pool](threadpool.md), `thread_handling` is not dynamic. The server reads the value at startup.

**Verification:** `SHOW VARIABLES LIKE 'thread_handling';` returns `pool-of-threads`.

**Rollback:** Remove `thread_handling=pool-of-threads` from the drop-in file and restart MySQL. The default in [Thread pool](threadpool.md) is `one-thread-per-connection`.

### Audit Log Filter

**Prerequisites:** Complete [Audit Log Filter installation](install-audit-log-filter.md) and [Audit Log Filter quickstart](audit-log-filter-quickstart.md). Define production filters and retention before you rely on the log.

**Activation:** Install the component and assign a filter with those pages. `audit_log_filter.disable` defaults to `OFF`, which leaves logging enabled. Run `SET GLOBAL audit_log_filter.disable = false;` only after a user set the variable to `ON`.

**Restart:** The installation procedure is SQL and does not include a server restart. Set `plugin_dir` at startup when the component library is not in the default directory. That `plugin_dir` change requires a restart. `SET GLOBAL audit_log_filter.disable` takes effect at runtime. Read [Disable Audit Log Filter logging](disable-audit-log-filter.md).

**Verification:** `SHOW GLOBAL STATUS LIKE 'audit_log_filter_events_written';` returns a row after the component writes events.

**Rollback:** To stop logging without removing the component, follow [Disable Audit Log Filter logging](disable-audit-log-filter.md). To remove the component, follow [Uninstall Audit Log Filter](uninstall-audit-log-filter.md):

```sql
UNINSTALL COMPONENT 'file://component_audit_log_filter';
```

### Data Masking

**Prerequisites:** The component library must be present in the directory named by `plugin_dir`. On Percona Server for MySQL 8.4.4-1 and later, grant `mysql.session` the privileges named on the install page. Use views and privileges to restrict access to unmasked data.

**Activation:** Follow [Install the data masking component](install-data-masking-component.md). Create `mysql.masking_dictionaries` with the schema on that page, then run `INSTALL COMPONENT 'file://component_masking_functions';`. Do not invent the table definition.

**Restart:** Not required to load the component. [Install the data masking component](install-data-masking-component.md) states that `INSTALL COMPONENT` registers the component and that the server loads it again on a later restart.

**Verification:** The `mysql.component` query returns a row whose `component_urn` is `file://component_masking_functions`.

**Rollback:** Follow [Uninstall the data masking component](uninstall-data-masking-component.md). That page covers privilege cleanup and the optional table drop. The uninstall command is:

```sql
UNINSTALL COMPONENT 'file://component_masking_functions';
```

### Extended Slow Log

**Prerequisites:** Read [Slow query log](slow-extended.md). Start with `long_query_time=1`. Measure log volume. Use `log_slow_rate_limit` when you need a sample.

**Activation:** Add these lines under `[mysqld]` in the drop-in file:

```ini
slow_query_log = ON
log_slow_verbosity = standard
```

[Slow query log](slow-extended.md) states that you can enable or disable the slow query log at runtime, and that `log_slow_verbosity` is dynamic. Option-file lines apply at the next restart. To enable them on the running server before that restart:

```sql
SET GLOBAL slow_query_log = ON;
SET GLOBAL log_slow_verbosity = 'standard';
```

**Restart:** Not required when you use the `SET GLOBAL` statements. Required when you add only the option-file lines.

**Verification:** `SHOW VARIABLES` for `slow_query_log`, `log_slow_verbosity`, and `long_query_time` returns `ON`, `standard`, and `1.000000` for this baseline.

**Rollback:** Disable logging on the running server, and remove or comment the drop-in lines so the next restart does not enable them again:

```sql
SET GLOBAL slow_query_log = OFF;
```

Run the statements for each feature you activated. The statements are in the same order as the features. The sample shows one possible result for every feature. A feature you left disabled does not match its sample rows.

```sql
SHOW VARIABLES LIKE 'thread_handling';
SHOW GLOBAL STATUS LIKE 'audit_log_filter_events_written';
SELECT * FROM mysql.component
WHERE component_urn = 'file://component_masking_functions';
SHOW VARIABLES WHERE Variable_name IN (
    'slow_query_log',
    'log_slow_verbosity',
    'long_query_time'
);
```

??? example "Expected output"

    ```{.text .no-copy}
    +-----------------+-----------------+
    | Variable_name   | Value           |
    +-----------------+-----------------+
    | thread_handling | pool-of-threads |
    +-----------------+-----------------+

    +---------------------------------+-------+
    | Variable_name                   | Value |
    +---------------------------------+-------+
    | audit_log_filter_events_written | 42    |
    +---------------------------------+-------+

    +--------------+--------------------+------------------------------------+
    | component_id | component_group_id | component_urn                      |
    +--------------+--------------------+------------------------------------+
    | 2            | 2                  | file://component_masking_functions |
    +--------------+--------------------+------------------------------------+

    +--------------------+----------+
    | Variable_name      | Value    |
    +--------------------+----------+
    | log_slow_verbosity | standard |
    | long_query_time    | 1.000000 |
    | slow_query_log     | ON       |
    +--------------------+----------+
    ```

    Event counts and component identifiers depend on the server.
