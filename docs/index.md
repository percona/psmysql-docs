<!-- Percona Server documentation master file, created by
sphinx-quickstart on Mon Aug  8 01:24:46 2011.
You can adapt this file completely to your liking, but it should at least
contain the root `toctree` directive. -->
# *Percona Server for MySQL* 8.0 - Documentation

*Percona Server for MySQL* is a free, fully compatible, enhanced, and open source drop-in replacement for any MySQL database. It provides superior performance, scalability, and instrumentation.

*Percona Server for MySQL* is trusted by thousands of enterprises to provide better performance and concurrency for their most demanding workloads. It delivers higher value to MySQL server users with optimized performance, greater performance scalability and availability, enhanced backups, and increased visibility.

## Introduction


* The Percona XtraDB Storage Engine


* List of features available in *Percona Server for MySQL* releases


* *Percona Server for MySQL* Feature Comparison


* Changed in Percona Server 8.0


## Installation


* Installing *Percona Server for MySQL* 8.0.29-21


    * Installing *Percona Server for MySQL* from Repositories


    * Installing *Percona Server for MySQL* from a Binary Tarball


    * Installing *Percona Server for MySQL* from a Source Tarball


    * Installing *Percona Server for MySQL* from the Git Source Tree


    * Compiling *Percona Server for MySQL* from Source


    * Building *Percona Server for MySQL* Debian/Ubuntu packages


* Post-Installation


    * Initializing the Data Directory


    * Secure the Installation


    * Testing the Server


    * Configuring the Server to Start at Startup


    * Testing the Server


    * Populating the Time Zone Tables


## In-place upgrades


* *Percona Server for MySQL* In-Place Upgrading Guide: From 5.7 to 8.0


* Upgrading using the Percona repositories


    * DEB-based distributions


    * RPM-based distributions


* Upgrading from Systems that Use the *MyRocks* or *TokuDB* Storage Engine and Partitioned Tables


    * Performing a Distribution upgrade in-place on a System with installed Percona packages


* Upgrading using Standalone Packages


    * DEB-based distributions


    * RPM-based distributions


## Run in Docker


* Running *Percona Server for MySQL* in a Docker Container


## Scalability Improvements


* Improved InnoDB I/O Scalability


## Performance Improvements


* Adaptive Network Buffers


* Multiple page asynchronous I/O requests


* Thread Pool


* XtraDB Performance Improvements for I/O-Bound Highly-Concurrent Workloads


* Prefix Index Queries Optimization


* Limiting the Estimation of Records in a Query


* Jemalloc Memory Allocation Profiling


* The ProcFS plugin


## Flexibility Improvements


* Binlogging and replication improvements


* Compressed columns with dictionaries


* Extended `SELECT INTO OUTFILE/DUMPFILE`


* Extended SET VAR Optimizer Hint


* `Improved MEMORY` Storage Engine


* Suppress Warning Messages


* Limiting the disk space used by binary log files


* Support for PROXY protocol


* SEQUENCE_TABLE(n) Function


* Slow Query Log Rotation and Expiration


## Reliability Improvements


* Too Many Connections Warning


* Handle Corrupted Tables


## Management Improvements


* *Percona Toolkit* UDFs


* Kill Idle Transactions


* XtraDB changed page tracking


* Enforcing Storage Engine


* PAM Authentication Plugin


* Expanded Fast Index Creation


* Backup Locks


* Audit Log Plugin


* Start transaction with consistent snapshot


* Extended `SHOW GRANTS`


* Utility user


## Security Improvements


* PAM Authentication Plugin


* Using Simple LDAP Authentication


* Simple LDAP Variables


* Working with SELinux


* Working with AppArmor


* Data at Rest Encryption


* Information about HashiCorp Vault


* Using the Keyring Plugin


* Using the Key Management Interoperability Protocol (KMIP)


* Encryption functions


* Using the Amazon Key Management Service (AWS KMS)


* Rotating the Master Key


* Encrypting File-Per-Table Tablespace


* Encrypting a Schema or a General Tablespace


* Encrypting the System Tablespace


* Encrypting Temporary Files


* Encrypting Binary Log Files and Relay Log Files


* Encrypting the Redo Log files


* Encrypting the Undo Tablespace


* Working with Advanced Encryption Key Rotation


* Encrypting Doublewrite Buffers


* Verifying the Encryption for Tables, Tablespaces, and Schemas


* SSL Improvements


* Data Masking


* Server variables


## Diagnostics Improvements


* User Statistics


* Slow Query Log


* Extended Show Engine InnoDB Status


* Show Storage Engines


* Process List


* Misc. INFORMATION_SCHEMA Tables


* Thread Based Profiling


* InnoDB Page Fragmentation Counters


* Stack Trace


* Using libcoredumper


## Percona MyRocks


* MyRocks Introduction


* MyRocks Installation


* MyRocks Supported Features


* MyRocks Limitations


* MyRocks Differences


* MyRocks Information Schema Tables


* MyRocks Server Variables


* MyRocks Status Variables


* MyRocks Gap Locks Detection


* MyRocks Data Loading


* MyRocks ZenFS


## TokuDB


* TokuDB Introduction


* TokuDB Installation


* Using TokuDB


* Fast Updates with TokuDB


* TokuDB files and file types


* TokuDB file management


* TokuDB Background ANALYZE TABLE


* TokuDB Variables


* TokuDB Status Variables


* TokuDB Fractal Tree Indexing


* TokuDB Troubleshooting


* TokuDB Performance Schema Integration


* Frequently Asked Questions


* Migrating and Removing the TokuDB storage engine


## Release notes


* *Percona Server for MySQL* 8.0 Release notes


## Reference


* List of upstream *MySQL* bugs fixed in *Percona Server for MySQL*  8.0


* List of variables introduced in *Percona Server for MySQL* 8.0


* Development of *Percona Server for MySQL*


* Trademark Policy


* Index of `INFORMATION_SCHEMA` Tables


* Frequently Asked Questions


* Copyright and Licensing Information


* Glossary



* Index


* Module Index
