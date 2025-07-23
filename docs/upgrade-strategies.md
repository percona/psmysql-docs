# Upgrade strategies

For critical production systems, consider engaging [Percona Support](https://www.percona.com/services/support) to assist with your upgrade process. Our experts can help ensure a smooth transition and minimize potential risks during this sensitive operation.

## Downgrade options

Review the [Downgrade options](downgrade.md) to ensure that your downgrade path is supported.

## In-place upgrade

Use the in-place upgrade strategy only as a last resort. This approach involves shutting down the server and replacing the server binaries or packages with new ones. The new server version then starts using the existing data directory. Configure the server to perform a slow shutdown by setting `innodb_fast_shutdown=0` before shutting down.

The benefits are:

* Lower infrastructure costs compared to creating a new environment, though nodes require testing.

* Ability to complete an upgrade over weeks with cool-down periods between reader node upgrades.

* Requires a failover of production traffic, and achieving minimal downtime demands robust high-availability tools.

If you use XA transactions with InnoDB, running `XA RECOVER` before upgrading checks for uncommitted XA transactions. If results are returned, either commit or rollback the XA transactions by issuing an `XA COMMIT` or `XA ROLLBACK` statement.

## New environment with cut over

Upgrading with a new environment involves provisioning a duplicate environment with the same number of servers with the same hardware specs and same operating system as the current production nodes.

On the newly provided hardware, the target MySQL version will be installed. The new environment will be set up, and the production data will be recovered. Remember that you can use pt-config-diff to verify MySQL configurations. 

Replication from the current source to the newly built environment will be established.
At cutover time, all writes on the current source will be halted, and the application traffic will need to be redirected to the new source. The cutover can be done using a Virtual IP address or manually redirecting the application itself. Once writes are being received on the new environment, you are in a fail forward situation, and the old environment can be torn down.

The new environment strategy has the following pros and cons:

* Additional infrastructure cost since a new environment must be built.

* Ability to upgrade both the OS and the DBMS at the same time.

* Allows upgrade of hardware easily.

* Requires only a single cutover window.
