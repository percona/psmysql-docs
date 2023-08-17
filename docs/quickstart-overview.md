# Quickstart guide for Percona Server for MySQL

Percona Server for MySQL is a freely available, fully compatible, enhanced, and open source drop-in replacement for any MySQL database. It provides superior and optimized performance, greater scalability and availability, enhanced backups, increased visibility, and instrumentation.
Percona Server for MySQL is trusted by thousands of enterprises to provide better performance and concurrency for their most demanding workloads.

## Install Percona Server for MySQL

You can install Percona Server for MySQL using different methods. 

* [Use the Percona Repositories](installation.md)
* [Use APT](apt-repo.md)
* [Use YUM](yum-repo.md)
* [Use binary tarballs](binary-tarball-install.md)
* [Use Docker](docker.md)

## For backups and restores

Percona XtraBackup (PXB) is a 100% open source backup solution for all versions of Percona Server for MySQL and MySQL® that performs online non-blocking, tightly compressed, highly secure full backups on transactional systems. Maintain fully available applications during planned maintenance windows with Percona XtraBackup.

[Install Percona XtraBackup](https://docs.percona.com/percona-xtrabackup/8.0/installation.html)

## For Monitoring and Management

Percona Monitoring and Management (PMM )monitors and provides actionable performance data for MySQL variants, including Percona Server for MySQL, Percona XtraDB Cluster, Oracle MySQL Community Edition, Oracle MySQL Enterprise Edition, and MariaDB. PMM captures metrics and data for the InnoDB, XtraDB, and MyRocks storage engines, and has specialized dashboards for specific engine details.

[Install PMM and connect your MySQL instances to it](https://docs.percona.com/percona-monitoring-and-management/get-started/index.html).

## For high availability

Percona XtraDB Cluster (PXC) is a 100% open source, enterprise-grade, highly available clustering solution for MySQL multi-master setups based on Galera. PXC helps enterprises minimize unexpected downtime and data loss, reduce costs, and improve performance and scalability of your database environments supporting your critical business applications in the most demanding public, private, and hybrid cloud environments.

[Percona XtraDB Cluster Quick start guide](https://docs.percona.com/percona-xtradb-cluster/8.0/overview.html)