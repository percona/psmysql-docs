# MySQL upgrade paths and supported methods

MySQL supports different upgrade paths depending on the source and target versions. Choose the appropriate method based on your current version and target.

<!-- Update this doc to be valid for 9.7-->

## Upgrade path matrix

| Upgrade Path | Path Examples | Supported Upgrade Methods |
| --- | --- | --- |
| Within an LTS or Bugfix series | 8.0.37 to 8.0.41 or 8.4.0 to 8.4.4 | In-place upgrade, logical dump and load, replication, and MySQL Clone |
| From an LTS or Bugfix series to the next LTS series | 8.0.37 to 8.4.x LTS | In-place upgrade, logical dump and load, and replication |
| From an LTS or Bugfix release to an Innovation release before the next LTS series | 8.0.34 to 8.3.0 or 8.4.0 to 9.0.0 | In-place upgrade, logical dump and load, and replication |
| From the Innovation series to the next LTS series | 8.3.0 to 8.4 LTS | In-place upgrade, logical dump and load, and replication |
| From an Innovation series to an Innovation release after the next LTS series | Not allowed, two steps are required: 8.3.0 to 8.4 LTS, and 8.4 LTS to 9.x Innovation | In-place upgrade, logical dump and load, and replication |

## Key considerations

* **LTS to LTS**: Direct upgrade from 8.0 LTS to 8.4 LTS is supported with multiple methods.
* **Innovation to Innovation**: Cannot skip LTS releases; must upgrade through the LTS series first.
* **MySQL Clone**: Only available for upgrades within the same major version series.
* **Replication**: Available for most upgrade paths but requires careful planning for cross-version replication.

## Choosing your upgrade method

* **In-place upgrade**: Fastest but highest risk; requires downtime.
* **Logical dump and load**: Cleanest but slowest for large datasets; requires downtime.
* **Replication**: Minimal downtime but requires additional infrastructure; good for high-availability setups.
* **MySQL Clone**: Fastest for same-series upgrades; requires compatible versions.

## Further reading

* [Upgrade overview](./upgrade.md)
* [Upgrade checklist for {{vers}}](./upgrade-checklist-9.7.md)
* [Upgrade procedures for {{vers}}](./upgrade-procedures.md)
* [Upgrade strategies](./upgrade-strategies.md)
* [Upgrade from plugins to components](./upgrade-components.md)
* [Downgrade options](./downgrade.md)
* [Breaking and incompatible changes in {{vers}}](./9.7-breaking-changes.md)
* [Compatibility and removed items in {{vers}}](./9.7-compatibility-and-removed-items.md)
* [Defaults and tuning guidance for {{vers}}](./9.7-defaults-and-tuning.md)
* [Percona Toolkit updates for {{vers}}](./percona-toolkit-9.7-updates.md)
