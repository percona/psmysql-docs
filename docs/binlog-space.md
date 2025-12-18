---
title: Managing binary log disk space
description: Controlling binary log disk usage can be difficult because binary log
  sizes vary.
slug: binlog-space
stability: stable
technical_preview: false
tags:
- percona-server
author: Percona Documentation Team
last_modified: '2025-12-18'
draft: false
---


# Managing binary log disk space

Controlling binary log disk usage can be difficult because binary log sizes vary. The database writes each transaction in full to a single binary log file and cannot split a write across multiple files. This requirement can lead to large log files, especially when transactions are large.

## binlog_space_limit

| Attribute | Description |
| --- | --- |
| Uses the command line | Yes |
| Uses the configuration file | Yes |
| Scope | Global |
| Dynamic | No |
| Variable type | ULONG_MAX |
| Default value | 0 (unlimited) |
| Maximum value - 64-bit platform | 18446744073709547520 |

This variable sets an upper limit on the total size of all binary logs in bytes. When the combined size exceeds this limit, the server automatically purges the oldest binary logs until the total size falls below the limit or only the active log remains.

A default value of 0 disables this feature. In this case, the server does not enforce a size limit and continues to write binary logs until the binary logs exhaust the available disk space.

## Example

Set the `binlog_space_limit` to 50 GB in the `my.cnf` file:

```text
[mysqld]
...
binlog_space_limit = 50G
...
```