---
title: INSTALL COMPONENT
description: The `INSTALL COMPONENT` does the following:.
slug: install-component
category: Install
stability: stable
technical_preview: false
tags:
- installation
- percona-server
author: Percona Documentation Team
last_modified: '2025-12-18'
draft: false
---


# INSTALL COMPONENT

The `INSTALL COMPONENT` does the following:

* Installs the component
* Activates the component

If an error, such as a misspelled component name, occurs, the statement fails and nothing happens.

You can install multiple components at the same time. 

## Example

The following is an example of the `INSTALL COMPONENT` statement.

```{.bash data-prompt="mysql>"}
mysql> INSTALL COMPONENT 'file://componentA';
```