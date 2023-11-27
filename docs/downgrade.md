# Downgrade Percona Server for MySQL

Downgrading to a 5.7 or earlier series is not supported.

The following table lists the downgrade paths:

| Path | Examples | Methods |
|---|---|---|
| Within a bugfix release series or an LTS release | 8.0.35 to 8.0.34 | in-place downgrade, logical downgrade, asynchronous replication, MySQL Clone plugin |
| A bugfix or LTS release to the last bugfix or LTS release series | 8.4.x to 8.0.x | logical downgrade, asynchronous replication |
| A bugfix or LTS release to an innovation release after the last LTS series | 8.4.x to 8.3.0 | logical downgrade, asynchronous replication |
| An innovation release to another innovation release after the last LTS series | 8.3.0 to 8.2.0 | logical downgrade, asynchronous replication |

We don't support downgrades with any 8.0.x release below 8.0.34.
A releases in the range above 8.0.34 can be downgraded to any release within that range, including 8.0.34.

## Downgrading risks

Downgrading has the following risks:

| Risk | Description |
|---|---|
| Data loss | If the downgrade process has issues, you may lose your data. It is crucial that you back up your data before attempting to downgrade. |
| Incompatibility | If you use any feature or improvement in the latest version, downgrading could result in incompatibility issues. |
| Performance | Downgrading may result in a loss of performance |
| Security | Newer versions have security updates that are not available in the older versions, which could lead to exposure. |
