# Improved InnoDB I/O scalability

Because *InnoDB* is a complex storage engine it must be configured properly in
order to perform at its best. Some points are not configurable in standard
*InnoDB*. The goal of this feature is to provide a more exhaustive set of
options for *XtraDB*.

## System variables

### `innodb_flush_method`

| Option         | Description                                                     |
|----------------|-----------------------------------------------------------------|
| Command-line   | Yes                                                             |
| Config file    | Yes                                                             |
| Scope          | Global                                                          |
| Dynamic        | No                                                              |
| Data type      | Enumeration                                                     |
| Default        | NULL                                                            |
| Allowed values | fsync, O_DSYNC, O_DIRECT, O_DIRECT_NO_FSYNC, littlesync, nosync |

The following values are allowed:

* `fdatasync`: use `fsync()` to flush data, log, and parallel doublewrite files.

* `O_SYNC`: use `O_SYNC` to open and flush the log and parallel doublewrite files; use `fsync()` to flush the data files. Do not use `fsync()` to flush the parallel doublewrite file.

* `O_DIRECT`: use O_DIRECT to open the data files and `fsync()` system call to flush data, log, and parallel doublewrite files.

* `O_DIRECT_NO_FSYNC`: use O_DIRECT to open the data files and parallel doublewrite files, but does not use the `fsync()` system call to flush the data files, log files, and parallel doublewrite files. Do not use this option for the *XFS* file system.

!!! note

    On an ext4 filesystem, set `innodb_log_write_ahead_size` to match the filesystem's write-ahead block size. This variable avoids `unaligned AIO/DIO` warnings.

## Status variables

The following information has been added to `SHOW ENGINE INNODB STATUS` to confirm the checkpointing activity:

```text
The current checkpoint age target
The current age of the oldest page modification which has not been flushed to disk yet.
The current age of the last checkpoint
...
---
LOG
---
Log sequence number 0 1059494372
Log flushed up to   0 1059494372
Last checkpoint at  0 1055251010
Max checkpoint age  162361775
Checkpoint age target 104630090
Modified age        4092465
Checkpoint age      4243362
0 pending log writes, 0 pending chkp writes
...
```

