# Upgrade strategies

There are different strategies to consider when upgrading from 8.0 to {{vers}}.

## In-place upgrade

An upgrade to {{vers}} does not allow a rollback. The in-place upgrade strategy is not recommended, and it should be used only as a last resort.

An in-place upgrade involves shutting down the 8.0 server, and replacing the server binaries, or packages, with new ones. At this point the new server version can be started on the existing data directory. Note that the server should be configured to perform a slow shutdown by setting `innodb_fast_shutdown=0` prior to shutdown.

The benefits are:

* Less additional infrastructure cost compared to a new environment, but nodes must be tested.
* An upgrade can be completed over weeks with cool-down periods between reader node upgrades.
* Requires a failover of production traffic, and for minimal downtime you must have good high-availability tools.

If you use XA transactions with InnoDB, running XA RECOVER before upgrading checks for uncommitted XA transactions. If results are returned, either commit or rollback the XA transactions by issuing an XA COMMIT or XA ROLLBACK statement.

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
