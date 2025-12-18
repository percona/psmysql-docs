---
title: Audit Log Filter restrictions
description: The Audit Log Filter has the following general restrictions:.
slug: audit-log-filter-restrictions
stability: stable
technical_preview: false
tags:
- audit-log
- percona-server
author: Percona Documentation Team
last_modified: '2025-12-18'
draft: false
---


# Audit Log Filter restrictions

## General restrictions

The Audit Log Filter has the following general restrictions:

The Audit Log Filter has the following general restrictions:

* Log only SQL statements. Statements made by NoSQL APIs, such as the 
  Memcached API, are not logged.

* Log only the top-level statement. Statements within a stored procedure 
  or a trigger are not logged. Do not log the file contents for statements 
  like `LOAD_DATA`.

* Require the component to be installed on each server used to execute SQL 
  on the cluster if used with a cluster.

* Hold the application or user responsible for aggregating all the data from 
  each server used in the cluster if used with a cluster.

* Each server must have its own audit log filter rules. If you do not set up the rules on the replica server, that server does not record the corresponding entries in the audit log. This design requires that the audit log configuration be performed separately for each server.

  As by default the content of the `mysql.audit_log_filter` and `mysql.audit_log_user` tables may be replicated from source to replica and may affect audit log rules created on the replica, it is recommended to configure replication in such a way that the changes in these tables are simply ignored.

  Please notice that just changing the content of these tables (via replication channel) is not enough to automatically make changes to in-memory data structures in the `audit_log_filter` component that store information about active audit log filtering rules. However, this may happen after component reloading / server restart or manually calling `audit_log_filter_flush()`.