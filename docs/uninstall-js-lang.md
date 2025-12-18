---
title: Uninstall the js_lang component
description: The uninstall works only when no connections are using JavaScript stored
  programs. If there are connections, the procedure fails with an error.
slug: uninstall-js-lang
category: Install
since: '8.4'
until: null
stability: stable
technical_preview: false
tags:
- installation
- percona-server
author: Percona Documentation Team
last_modified: '2025-12-18'
draft: false
---


# Uninstall the js_lang component

The uninstall works only when no connections are using JavaScript stored programs. If there are connections, the procedure fails with an error.

To remove the component, run the following:

```{.bash data-prompt="mysql>"}
mysql> UNINSTALL COMPONENT 'file://component_js_lang';
```