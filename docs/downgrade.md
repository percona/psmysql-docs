---
title: Downgrade Percona Server for MySQL
description: Downgrading to a 5.7 or earlier series is not supported.
slug: downgrade
category: Upgrade
stability: stable
technical_preview: false
tags:
- percona-server
author: Percona Documentation Team
last_modified: '2025-12-18'
draft: false
---


# Downgrade Percona Server for MySQL

--8<--- "get-help-snip.md"

Downgrading to a 5.7 or earlier series is not supported.

Between versions within the same Long-Term Support (LTS) series, you can downgrade from 8.4.y LTS to 8.4.x LTS using the following methods:

* Performing an in-place upgrade

* Creating a logical dump and loading it

* Use MySQL Clone functionality

* Set up replication between the versions

Between one LTS or Bugfix series to the previous LTS or Bugfix series, such as moving from 8.4.x LTS to 8.0.y, you have two primary options:

* Create a logical dump of your data and load it into the older version

* Set up replication between the versions. 

!!! important "Important"
    This downgrade path is only supported when no new server functionality has been applied to your data.

Between an LTS or Bugfix series to an earlier Innovation series (after the previous LTS release), such as from 8.4.x LTS to 8.3.0 Innovation, you have the following options:

* Create a logical dump of your data and load it into the older version

* Set up replication between the versions. 

!!! important "Important"
    This downgrade path is only supported when no new server functionality has been applied to your data.

We don't support downgrades with any 8.0.x release below 8.0.34.
Releases in the range above 8.0.34 can be downgraded to any release within that range, including 8.0.34.

## Downgrading risks

Downgrading has the following risks:

| Risk | Description |
|---|---|
| Data loss | If the downgrade process has issues, you may lose your data. It is crucial that you back up your data before attempting to downgrade. |
| Incompatibility | If you use any feature or improvement in the latest version, downgrading could result in incompatibility issues. |
| Performance | Downgrading may result in a loss of performance |
| Security | Newer versions have security updates that are not available in the older versions, which could lead to exposure. |

## Further reading

* [Upgrade overview](./upgrade.md)
* [Upgrade checklist for {{vers}}](./upgrade-checklist-8.4.md)
* [Upgrade procedures for {{vers}}](./upgrade-procedures.md)
* [Upgrade strategies](./upgrade-strategies.md)
* [MySQL upgrade paths and supported methods](./mysql-upgrade-paths.md)
* [Upgrade from plugins to components](./upgrade-components.md)
* [Breaking and incompatible changes in {{vers}}](./8.4-breaking-changes.md)
* [Compatibility and removed items in {{vers}}](./8.4-compatibility-and-removed-items.md)
* [Defaults and tuning guidance for {{vers}}](./8.4-defaults-and-tuning.md)
* [Percona Toolkit updates for {{vers}}](./percona-toolkit-8.4-updates.md)