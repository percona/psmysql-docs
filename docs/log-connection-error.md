---
title: Too many connections warning
description: If the [log_error_verbosity] system variable is set to `2` or higher,
  this feature generates the `Too many connections` warning in the log.
slug: log-connection-error
category: Troubleshoot
stability: stable
technical_preview: false
tags:
- percona-server
author: Percona Documentation Team
last_modified: '2025-12-18'
draft: false
---


# Too many connections warning

If the [log_error_verbosity] system variable is set to `2` or higher, this 
feature generates the `Too many connections` warning in the log.

!!! tip "Troubleshooting Connection Issues"
    For comprehensive guidance on managing database connections and 
    performance, [Percona Support](https://www.percona.com/services/support) 
    can provide expert assistance in diagnosing and resolving connection 
    management challenges.

[log_error_verbosity]: https://dev.mysql.com/doc/refman/{{vers}}/en/server-system-
variables.html#sysvar_log_error_verbosity