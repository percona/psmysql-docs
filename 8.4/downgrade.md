> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# Downgrade Percona Server for MySQL

Review [Get help from Percona](https://docs.percona.com/percona-server/8.4/get-help.html) for ways that we can work with you.

Downgrading to a 5.7 or earlier series is not supported.

Between versions within the same Long-Term Support (LTS) series, you can downgrade from 8.4.y LTS to 8.4.x LTS using the following methods:

- Performing an in-place upgrade
- Creating a logical dump and loading it
- Use MySQL Clone functionality
- Set up replication between the versions

Between one LTS or Bugfix series to the previous LTS or Bugfix series, such as moving from 8.4.x LTS to 8.0.y, you have two primary options:

- Create a logical dump of your data and load it into the older version
- Set up replication between the versions.

Important

This downgrade path is only supported when no new server functionality has been applied to your data.

Between an LTS or Bugfix series to an earlier Innovation series (after the previous LTS release), such as from 8.4.x LTS to 8.3.0 Innovation, you have the following options:

- Create a logical dump of your data and load it into the older version
- Set up replication between the versions.

Important

This downgrade path is only supported when no new server functionality has been applied to your data.

We don’t support downgrades with any 8.0.x release below 8.0.34. Releases in the range above 8.0.34 can be downgraded to any release within that range, including 8.0.34.

## Downgrading risks

Downgrading has the following risks:

| Risk            | Description                                                                                                                           |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Data loss       | If the downgrade process has issues, you may lose your data. It is crucial that you back up your data before attempting to downgrade. |
| Incompatibility | If you use any feature or improvement in the latest version, downgrading could result in incompatibility issues.                      |
| Performance     | Downgrading may result in a loss of performance                                                                                       |
| Security        | Newer versions have security updates that are not available in the older versions, which could lead to exposure.                      |

## Further reading

- [Upgrade overview](https://docs.percona.com/percona-server/8.4/upgrade.html)
- [Upgrade checklist for 8.4](https://docs.percona.com/percona-server/8.4/upgrade-checklist-8.4.html)
- [Upgrade procedures for 8.4](https://docs.percona.com/percona-server/8.4/upgrade-procedures.html)
- [Upgrade strategies](https://docs.percona.com/percona-server/8.4/upgrade-strategies.html)
- [MySQL upgrade paths and supported methods](https://docs.percona.com/percona-server/8.4/mysql-upgrade-paths.html)
- [Upgrade from plugins to components](https://docs.percona.com/percona-server/8.4/upgrade-components.html)
- [Breaking and incompatible changes in 8.4](https://docs.percona.com/percona-server/8.4/8.4-breaking-changes.html)
- [Compatibility and removed items in 8.4](https://docs.percona.com/percona-server/8.4/8.4-compatibility-and-removed-items.html)
- [Defaults and tuning guidance for 8.4](https://docs.percona.com/percona-server/8.4/8.4-defaults-and-tuning.html)
- [Percona Toolkit updates for 8.4](https://docs.percona.com/percona-server/8.4/percona-toolkit-8.4-updates.html)
