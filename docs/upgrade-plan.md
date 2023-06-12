# Plan an upgrade

A database upgrade must be [planned and tested](./upgrade-plan.md). The downtime requirements are a major factor in the upgrade strategy.

The following steps should be reviewed and tested:
 
| Step | Description |
|--- | --- |
| Review current environment | Research which server components/plugins are used, application versions are used, user connections and when is the database has the heaviest traffic. |
| Hardware and software requirements | Review if any infrastructure upgrades are required to support the database upgrade. Consider if the hardware and the software must be upgraded. |
| Do regression testing | Perform regression testing in the test environment. |
| Upgrade sequence | Review the high priority processes to plan testing the process. |
| Back up and rollback | Plan what happens if the upgrade fails. Back up the important files, including configuration files. Be aware that after the database server is upgraded, [downgrading](./downgrade.md) is not supported. |
| Release notes | Review the release notes for the new version. |
