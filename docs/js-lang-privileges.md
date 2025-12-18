---
title: JS privileges
description: Privileges control what users can do. You use them to give specific permissions
  to different users.
slug: js-lang-privileges
since: '8.4'
until: null
stability: tech-preview
technical_preview: true
tags:
- percona-server
- tech-preview
author: Percona Documentation Team
last_modified: '2025-12-18'
draft: false
---


# JS privileges

--8<--- "experimental.md"

Privileges control what users can do. You use them to give specific permissions to different users. This ability helps you keep your data secure by only allowing authorized users to access and change information in the database. 

## Privileges

To create routines within a database, you must be granted the `CREATE_JS_ROUTINE` privilege and the standard `CREATE ROUTINE` privilege.

```{.bash data-prompt="mysql>"}
mysql> GRANT CREATE_JS_ROUTINE ON *.* TO user1@localhost;
```

If a user is granted the ability to create routines and holds the CREATE_JS_ROUTINE privilege, they are capable of creating stored functions and procedures using JS.

However, it is important to note that at this time, the creation of JS triggers or events is not supported.