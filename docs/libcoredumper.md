<!-- libcoredumper: -->
# Using libcoredumper

A core dump file is the documented moment of a computer when either the computer or an application exits. Developers examine the dump as one of the tasks when searching for the cause of a failure.

The `libcoredumper` is a free and Open Source fork of `google-coredumper`,
enhanced to work on newer Linux versions, and GCC and CLANG.

### Enabling the `libcoredumper`

Enable core dumps for troubleshooting purposes.

To enable the `libcoredumper`, add the `coredumper` variable to the
`mysqld` section of `my.cnf`. This variable is independent of the
older `core-file` variable.

The variable can have the following possible values:

| Value                     | Description                                                          |
|---------------------------|----------------------------------------------------------------------|
| Blank                     | The core dump is saved under MySQL datadir and named core.           |
| A path ending with /      | The core dump is saved under the specified directory and named core. |
| Full path with a filename | The core dump is saved under the specified directory and filename    |

Restart the server.

### Verifying the `libcoredumper` is active

MySQL writes to the log when generating a core file and delegates the core
dump operation to the Linux kernel. 

```{.text .no-copy}
Writing a core file
```

MySQL using the `libcoredumper` to generate the file creates the following
message in the log:

```{.text .no-copy}
Writing a core file using lib coredumper
```

Every core file adds a crash timestamp instead of a PID for the following
reasons:

* Correlates the core file with the crash. MySQL prints a UTC timestamp on the crash log.

```{.text .no-copy}
10:02:09 UTC - mysqld got signal 11;
```

* Stores multiple core files.

!!! note

    For example, operators and containers run as the process id of PID 1. If the process ID is used to identify the core file, each container crash generates a core dump that overwrites the previous core file.

### Disabling the libcoredumper

You can disable the libcoredumper. A core file may contain sensitive data and
takes disk space.

To disable the `libcoredumper` you must do the following:
{.power-number}

1. In the `mysqld` section of my.cnf, remove the `libcoredumper` variable.

2. Restart the server.
