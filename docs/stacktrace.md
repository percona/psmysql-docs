---
title: Stack trace
description: Developers use the stack trace in the debug process, either an interactive
  investigation or during the post-mortem. No configuration is required to generate
  a stack trace.
slug: stacktrace
stability: stable
technical_preview: false
tags:
- percona-server
author: Percona Documentation Team
last_modified: '2025-12-18'
draft: false
---


# Stack trace

Developers use the stack trace in the debug process, either an interactive 
investigation or during the post-mortem. No configuration is required to 
generate a stack trace.

Stack trace adds the following:

| Name                                 | Description                                                     |
|--------------------------------------|------------------------------------------------------------------|
| Prints binary BuildID                | The Strip utility removes unneeded sections and debugging        |
|                                      | information to reduce the size. This method is standard with     |
|                                      | containers where the image size is essential. The BuildID lets   |
|                                      | you resolve the stack trace when the Strip utility removes the   |
|                                      | binary symbols table.                                            |
| Print the server version information | The version information establishes the starting point for        |
|                                      | analysis. Some applications, such as MySQL, only print this      |
|                                      | information to a log on startup, and when the crash occurs, the  |
|                                      | log may be large, rotated, or truncated.                         |

!!! tip "Need Help Interpreting Stack Traces?"
    [Percona Support](https://www.percona.com/services/support) offers 
    expert debugging and performance analysis to help you understand 
    complex stack trace diagnostics.