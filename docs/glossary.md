# Glossary

## ACID

Set of properties that guarantee database transactions are processed reliably. Stands for [Atomicity](#atomicity), [Consistency](#consistency), [Isolation](#isolation), [Durability](#durability).

## Atomicity

Atomicity means that database operations are applied following a “all or nothing” rule. A transaction is either fully applied or not at all.

## Consistency

Consistency means that each transaction that modifies the database takes it from one consistent state to another.

## Durability

Once a transaction is committed, it will remain so.

## Environment Variable

A variable that stores configuration settings for a software program or operating system.

## Foreign Key

A referential constraint between two tables. Example: A purchase order in the purchase\_orders table must have been made by a customer that exists in the customers table.

## General Availability (GA)

A finalized version of the product which is made available to the general public. It is the final stage in the software release cycle.

## Isolation

The Isolation requirement means that no transaction can interfere with another.

## InnoDB

A [Storage Engine](#storage-engine) for MySQL and derivatives ([Percona Server](#percona-server-for-mysql), [MariaDB](#mariadb)) originally written by Innobase Oy, since acquired by Oracle. It provides [ACID](#acid) compliant storage engine with [foreign key](#foreign-key) support. As of [MySQL](#mysql) version 5.5, InnoDB became the default storage engine on all platforms.

## JSON (JavaScript Object Notation)

A common file format used to store data in a human-readable and machine-readable way using key-value pairs.
 
## Jenkins

[Jenkins](https://www.jenkins-ci.org) is a continuous integration system that we use to help ensure the continued quality of the software we produce. It helps us achieve the aims of:

* no failed tests in the trunk on any platform

* aid developers in ensuring merge requests build and test on all platform

* no known performance regressions (without a damn good explanation).

## LSN

The Log Sequence Number (LSN) is an 8-byte number. Every data change adds an entry to the redo log and generates an LSN. The server increments the LSN with every change.

## Mandatory Dependency

A software package that another software package absolutely needs to function correctly. Removing a mandatory dependency can cause the main software to malfunction.

## MariaDB

A fork of [MySQL](#mysql) that is maintained primarily by Monty Program AB. It aims to add features, and fix bugs while maintaining 100% backward compatibility with MySQL.

## Metrics

Measurable data points collected by telemetry about software usage.

## my.cnf

A configuration file used by MySQL databases.

## MyISAM

A [MySQL](#mysql) [Storage Engine](#storage-engine) that was the default until MySQL 5.5.

## MySQL

An open source database that has spawned several distributions and forks. MySQL AB was the primary maintainer and distributor until bought by Sun Microsystems, which was then acquired by Oracle. As Oracle owns the MySQL trademark, the term MySQL is often used for the Oracle distribution of MySQL as distinct from the drop-in replacements such as [MariaDB](#mariadb) and [Percona Server for MySQL](#percona-server-for-mysql).

## NUMA

Non-Uniform Memory Access ([NUMA](https://en.wikipedia.org/wiki/Non-Uniform_Memory_Access)) is a computer memory design used in multiprocessing, where the memory access time depends on the memory location relative to a processor. Under NUMA, a processor can access its own local memory faster than non-local memory, that is, memory local to another processor or memory shared between processors. The whole system may still operate as one unit, and all memory is basically accessible from everywhere but at a potentially higher latency and lower performance.

## Percona Server for MySQL

The Percona branch of [MySQL](#mysql) with performance and management improvements.

## Storage Engine

A storage engine is a piece of software that implements the details of data storage and retrieval for a database system. This term is primarily used within the [MySQL](#mysql) ecosystem due to it being the first widely used relational database to have an abstraction layer around storage. It is analogous to a Virtual File System layer in an Operating System. A VFS layer allows an operating system to read and write multiple file systems (e.g. FAT, NTFS, XFS, ext3) and a Storage Engine layer allows a database server to access tables stored in different engines (for example, [MyISAM](#myisam) or InnoDB).

## Tech Preview

A tech preview item can be a feature, a variable, or a value within a variable. Before using this feature in production, we recommend that you test restoring production from physical backups in your environment and also use an alternative backup method for redundancy. A tech preview item is included in a release for users to provide feedback. The item is either updated, released as [general availability(GA)](#general-availability-ga), or removed if not useful. The functionality can change from tech preview to GA.

## Telemetry

Telemetry automatically collects usage data from software to understand how users interact with it.

## Uninstall Component

A way to remove a specific component or functionality within a software package.


## Universally Unique Identifier (UUID)

A unique identifier used to ensure no two entities share the same ID.

## XtraDB

The Percona improved version of [InnoDB](#innodb) provides performance, features, and reliability above what is shipped by Oracle in InnoDB.
