# Percona Tools that can help with an upgrade

Percona has several tools in our Percona Toolkit that can help with upgrade planning, and  make the entire process much easier and less prone to downtime or issues.

| Name | Description |
| --- | --- |
| [pt-upgrade](https://docs.percona.com/percona-toolkit/pt-upgrade.html) | tool helps you run application SELECT queries and generates reports on how each query pattern performs on the servers across different versions of MySQL |
| [pt-query-digest](https://docs.percona.com/percona-toolkit/pt-query-digest.html) | As best practice dictates gathering and testing all application queries by activating the slow log for a period of time, most companies will end up with an enormous amount of slow log data. The pt-query-digest tool can assist in query digest preparation for your upgrade testing. |
| [pt-config-diff](https://docs.percona.com/percona-toolkit/pt-config-diff.html) | The pt-config-diff tool helps in determining the differences in MySQL settings between files and server variables. This allows comparison of the upgraded version to the previous version, allowing validation of configuration differences. |
| [pt-show-grants](https://docs.percona.com/percona-toolkit/pt-show-grants.html) | The pt-show-grants tool extracts, orders, and then prints grants for MySQL user accounts. This can help to export and backup your MySQL grants prior to an upgrade, or allow you to easily replicate users from one server to another by simply extracting the grants from the first server and piping the output directly into another server. | 

For more information, see [Percona Toolkit](https://docs.percona.com/percona-toolkit/)
