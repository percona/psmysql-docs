> For the complete documentation index, see [llms.txt](https://docs.percona.com/percona-server/8.4/llms.txt).

# MySQL upgrade paths and supported methods

MySQL supports different upgrade paths depending on the source and target versions. Choose the appropriate method based on your current version and target.

## Upgrade path matrix

| Upgrade Path                                                                      | Path Examples                                                                        | Supported Upgrade Methods                                             |
| --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | --------------------------------------------------------------------- |
| Within an LTS or Bugfix series                                                    | 8.0.37 to 8.0.41 or 8.4.0 to 8.4.4                                                   | In-place upgrade, logical dump and load, replication, and MySQL Clone |
| From an LTS or Bugfix series to the next LTS series                               | 8.0.37 to 8.4.x LTS                                                                  | In-place upgrade, logical dump and load, and replication              |
| From an LTS or Bugfix release to an Innovation release before the next LTS series | 8.0.34 to 8.3.0 or 8.4.0 to 9.0.0                                                    | In-place upgrade, logical dump and load, and replication              |
| From the Innovation series to the next LTS series                                 | 8.3.0 to 8.4 LTS                                                                     | In-place upgrade, logical dump and load, and replication              |
| From an Innovation series to an Innovation release after the next LTS series      | Not allowed, two steps are required: 8.3.0 to 8.4 LTS, and 8.4 LTS to 9.x Innovation | In-place upgrade, logical dump and load, and replication              |

## Key considerations

- **LTS to LTS**: Direct upgrade from 8.0 LTS to 8.4 LTS is supported with multiple methods.
- **Innovation to Innovation**: Cannot skip LTS releases; must upgrade through the LTS series first.
- **MySQL Clone**: Only available for upgrades within the same major version series.
- **Replication**: Available for most upgrade paths but requires careful planning for cross-version replication.

## Choosing your upgrade method

- **In-place upgrade**: Fastest but highest risk; requires downtime.
- **Logical dump and load**: Cleanest but slowest for large datasets; requires downtime.
- **Replication**: Minimal downtime but requires additional infrastructure; good for high-availability setups.
- **MySQL Clone**: Fastest for same-series upgrades; requires compatible versions.

## Further reading

- [Upgrade overview](https://docs.percona.com/percona-server/8.4/upgrade.md)
- [Upgrade checklist for 8.4](https://docs.percona.com/percona-server/8.4/upgrade-checklist-8.4.md)
- [Upgrade procedures for 8.4](https://docs.percona.com/percona-server/8.4/upgrade-procedures.md)
- [Upgrade strategies](https://docs.percona.com/percona-server/8.4/upgrade-strategies.md)
- [Upgrade from plugins to components](https://docs.percona.com/percona-server/8.4/upgrade-components.md)
- [Downgrade options](https://docs.percona.com/percona-server/8.4/downgrade.md)
- [Breaking and incompatible changes in 8.4](https://docs.percona.com/percona-server/8.4/8.4-breaking-changes.md)
- [Compatibility and removed items in 8.4](https://docs.percona.com/percona-server/8.4/8.4-compatibility-and-removed-items.md)
- [Defaults and tuning guidance for 8.4](https://docs.percona.com/percona-server/8.4/8.4-defaults-and-tuning.md)
- [Percona Toolkit updates for 8.4](https://docs.percona.com/percona-server/8.4/percona-toolkit-8.4-updates.md)
