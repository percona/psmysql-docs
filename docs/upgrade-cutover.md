# Upgrade by migrating from one environment to another

A cut over upgrade involves migrating an exact copy of the database server from one environment to an upgraded server without redesigning the database, code or supported features. The environments must have the same hardware and operating system. 

During the migration, all writes on the current server are stopped and application traffic is redirected to the new server. After the application begins writing to the new server, you can start tear down the old environment.

The benefits are the following:

* Can upgrade the operating system and database server at the same time

* Allows an upgrade of the hardware

* Requires only one migration

The disadvantage is an entire environment must be built.
