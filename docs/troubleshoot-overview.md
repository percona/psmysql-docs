# Troubleshooting overview

Use this section when something goes wrong or you need to diagnose an issue with Percona Server for MySQL. The topics below point you to the right guide.

--8<--- "get-help-snip.md"

## Topics

| Topic | When to use it |
|-------|----------------|
| [Use PMM Advisors](advisors.md) | Run automated checks on your database settings and get recommendations. |
| [Too many connections warning](log-connection-error.md) | Diagnose and address connection limit messages in the log. |
| [Handle corrupted tables](innodb-corrupt-table-action.md) | React when InnoDB encounters a corrupted table without crashing the server. |
| [Thread-based profiling](thread-based-profiling.md) | Profile queries and understand where time is spent. |
| [Stack trace](stacktrace.md) | Capture and interpret stack traces for debugging. |
| [Core dumps (libcoredumper)](libcoredumper.md) | Capture and analyze core dumps for crash diagnosis. |

## Troubleshooting by topic

These guides live under their topic sections but are useful when you are troubleshooting:

| Topic | Guide |
|-------|-------|
| SELinux | [Troubleshoot SELinux issues](troubleshoot-selinux.md) |
| AppArmor | [Troubleshoot AppArmor profiles](troubleshoot-apparmor.md) |
| SQL | [Troubleshoot SQL code](troubleshooting-sql.md) |

## What to do next

* [Get help from Percona](get-help.md) — community forum and expert support
* [Documentation home](index.md) — return to the main guide
* [Quickstart guide](quickstart-overview.md) — get a fresh installation up and running
