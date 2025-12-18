---
title: Uninstall Audit Log Filter
description: If you no longer need the audit log filter functionality, you can remove
  the component from server using the following command:.
slug: uninstall-audit-log-filter
category: Install
stability: stable
technical_preview: false
tags:
- audit-log
- installation
- percona-server
author: Percona Documentation Team
last_modified: '2025-12-18'
draft: false
---


# Uninstall Audit Log Filter

If you no longer need the audit log filter functionality, you can remove the component from server using the following command:

```{.bash data-prompt="mysql>"}
mysql> UNINSTALL COMPONENT 'file://component_audit_log_filter';
```

This command does the following:

*	`UNINSTALL COMPONENT`: This tells the server to remove a plugin or feature that was previously installed.
	
*	`file://component_audit_log_filter`: This is the identifier for the Audit Log Filter Component, which is responsible for applying rules to decide which audit log events are recorded.