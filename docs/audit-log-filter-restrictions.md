# Audit Log Filter restrictions

## General restrictions

The Audit Log Filter has the following general restrictions:

* Log only SQL statements. Statements made by NoSQL APIs, such as the 
  Memcached API, are not logged.

* Log only the top-level statement. Statements within a stored procedure 
  or a trigger are not logged. Do not log the file contents for statements 
  like `LOAD_DATA`.

* Require the component to be installed on each server used to execute SQL 
  on the cluster if used with a cluster.

* Hold the application or user responsible for aggregating all the data from 
  each server used in the cluster if used with a cluster.

* Each server must have its own audit log filter rules. If you do not set up the rules on the replica server, that server does not record the corresponding entries in the audit log. This design requires that the audit log configuration be performed separately for each server.

  As by default the content of the `mysql.audit_log_filter` and `mysql.audit_log_user` tables may be replicated from source to replica and may affect audit log rules created on the replica, it is recommended to configure replication in such a way that the changes in these tables are simply ignored.

  Please notice that just changing the content of these tables (via replication channel) is not enough to automatically make changes to in-memory data structures in the `audit_log_filter` component that store information about active audit log filtering rules. However, this may happen after component reloading / server restart or manually calling `audit_log_filter_flush()`.

* Filter only on string values. The audit log filter does not filter on integer values. All filter criteria must be specified as strings, even when the underlying value is numeric. For example, `connection_id` values must be specified as strings (for example, `"123"` rather than `123`), and status values must be specified as `"0"` or `"1"` rather than `0` or `1`. If you use integer values in your filter definition, you will see the error: `ERROR: Incorrect rule definition.`

## Synchronizing audit log filters between source and replica

You can keep audit log filter definitions in sync between a source and a replica by replicating the filter tables and periodically calling `audit_log_filter_flush()` on the replica. That reloads the filter tables and makes the replicated changes effective on the replica.

### Procedure: MySQL event to flush filters on the replica

1. Install MySQL on the source with the audit log filter component.

2. Create a replica from a source backup.

3. Create a MySQL event on the replica that runs every minute:

       ```sql
       USE mysql;
       CREATE EVENT auditflush
           ON SCHEDULE EVERY 1 MINUTE
           COMMENT 'Flush audit log filters every minute'
           DO
             SELECT audit_log_filter_flush();
       ```

    This event runs `audit_log_filter_flush()` every minute on the replica, so replicated changes to the filter tables become effective shortly after they are applied.

4. Create a filter on the source and assign the filter to a user using the usual filter functions or by modifying the filter tables and calling `audit_log_filter_flush()` on the source.

5. After a minute, check that the filter is available on the replica. Run some queries on the replica as that user and confirm that the expected messages appear in the audit log file. 

If the filter is not yet visible or the audit log does not show the expected entries, wait for the next event run (within a minute) or run `SELECT audit_log_filter_flush();` on the replica to refresh the filter tables immediately; also confirm that replication has applied the changes to the filter tables and that the event is enabled. If the filter or expected log entries still do not appear, the cause may be a problem in replication between source and replica; troubleshooting replication may help.

Another possible scenario is that the source and replica are set up and replication is working, but the audit log component is not installed on either the source or the replica. In that case, install the audit log component on both the source and the replica separately.

### Limitation

If a user modifies the filter tables directly on the source (for example, with `INSERT`, `UPDATE`, or `DELETE`) but does not run `audit_log_filter_flush()` on the source, the table changes will be replicated to the replica and the event will run `audit_log_filter_flush()` there, so the filters become effective on the replica. The filters will then work correctly on the replica but will not be effective on the source until `audit_log_filter_flush()` is run on the source.
