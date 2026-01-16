# Audit Log Filter restrictions

## General restrictions

The Audit Log Filter has the following general restrictions:

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

## Replication and cluster behavior

### Replication scenarios

The audit log filter tables (`mysql.audit_log_filter` and `mysql.audit_log_user`) are replicated by default, but filter rules stored in these tables do not automatically become active on replica servers.

**Scenario 1: Source server creates filter**

1. On source server: Administrator creates a filter and assigns it to users
2. Filter is stored in `mysql.audit_log_filter` and `mysql.audit_log_user` tables
3. Filter is immediately active on source server (in-memory)
4. Table changes replicate to replica server
5. On replica server: Filter exists in tables but is NOT active in memory
6. To activate on replica: Call `audit_log_filter_flush()` or restart server

**Example:**
```sql
-- On source server
SELECT audit_log_filter_set_filter('log_all', '{"filter": {"log": true}}');
SELECT audit_log_filter_set_user('%', 'log_all');
-- Filter is immediately active

-- On replica server (after replication)
-- Filter exists in tables but is not active
-- Must run:
SELECT audit_log_filter_flush();
-- Now filter is active on replica
```

**Scenario 2: Direct table modification on source**

1. On source server: Administrator modifies tables directly (INSERT/UPDATE/DELETE)
2. Changes replicate to replica
3. On source: Must call `audit_log_filter_flush()` to activate changes
4. On replica: Must also call `audit_log_filter_flush()` to activate changes

**Recommended replication configuration:**

To avoid conflicts and ensure independent filter configuration on each server, configure replication to ignore audit log filter tables:

```ini
# In my.cnf on replica server
[mysqld]
replicate-ignore-table=mysql.audit_log_filter
replicate-ignore-table=mysql.audit_log_user
```

**Benefits:**
* Each server can have independent filter configuration
* No conflicts between source and replica filters
* Better control over audit logging on each server
* Avoids accidental filter activation from replication

### Cluster scenarios

When using audit log filter in a cluster environment:

**Each server needs independent configuration:**
* Install the component on each server in the cluster
* Configure filters separately on each server
* Filters are not shared between cluster nodes

**Aggregating logs:**
* Each server generates its own audit log files
* You must aggregate logs from all servers manually
* Consider using external log aggregation tools
* Ensure consistent time synchronization across servers

**Example cluster setup:**
```
Server 1 (Primary):   audit_filter.log
Server 2 (Replica):   audit_filter.log
Server 3 (Replica):   audit_filter.log

Aggregate all three files for complete audit trail
```

## What gets logged vs not logged

### Top-level statements only

The audit log filter logs only top-level SQL statements. Statements executed within stored procedures, functions, or triggers are not logged.

**What gets logged:**
* `CALL stored_procedure_name();` → Logged (top-level statement)
* `SELECT * FROM table;` → Logged (top-level statement)
* `INSERT INTO table VALUES (...);` → Logged (top-level statement)

**What does NOT get logged:**
* Statements inside stored procedures:
  ```sql
  CREATE PROCEDURE my_proc()
  BEGIN
    SELECT * FROM table1;  -- NOT logged
    INSERT INTO table2 ...; -- NOT logged
  END;
  ```
* Statements inside triggers:
  ```sql
  CREATE TRIGGER my_trigger
  BEFORE INSERT ON table1
  FOR EACH ROW
  BEGIN
    INSERT INTO table2 ...; -- NOT logged
  END;
  ```
* Statements inside functions:
  ```sql
  CREATE FUNCTION my_func() RETURNS INT
  BEGIN
    SELECT COUNT(*) INTO @count FROM table1; -- NOT logged
    RETURN @count;
  END;
  ```

**Why this limitation exists:**
* Performance: Logging every statement in procedures/triggers would generate excessive log volume
* Complexity: Nested statement execution makes it difficult to track context
* Focus: Top-level statements represent user-initiated actions

**Workaround if full statement capture is needed:**
* Enable general query log for complete statement capture
* Use application-level logging
* Modify stored procedures to include logging statements

### LOAD_DATA file content

When using `LOAD DATA` statements:

**What gets logged:**
* The `LOAD DATA` statement itself is logged
* File path may be logged (depending on configuration)
* Number of rows affected is logged

**What does NOT get logged:**
* File contents are NOT logged (for security and privacy)
* Data values being loaded are NOT logged

**Example:**
```sql
LOAD DATA INFILE '/path/to/data.csv' INTO TABLE customers;
```

**Logged information:**
* Statement: `LOAD DATA INFILE '/path/to/data.csv' INTO TABLE customers`
* User, host, database, table
* Execution status (success/failure)
* Rows affected

**Not logged:**
* Contents of `/path/to/data.csv`
* Individual data values being inserted

This behavior protects sensitive data that might be in the file and prevents log files from becoming excessively large.

## Performance considerations

### Impact of logging all events

Logging all events can have significant performance impact:

**Typical performance impact:**
* Query performance: 30-70% reduction in queries per second (QPS) when logging everything
* Disk I/O: Substantial increase in write operations
* CPU usage: Increased CPU usage for log processing
* Memory: Buffer usage for asynchronous logging

**Recommendations:**
* Start with selective logging (specific users, databases, or event types)
* Monitor performance metrics using status variables
* Gradually increase logging scope if needed
* Use asynchronous logging strategy (default)

### Impact of complex filters

Complex filters with multiple conditions can have additional overhead:

**Factors affecting performance:**
* Number of filter conditions
* Number of event classes being filtered
* Use of wildcards in filters
* Filter evaluation for each event

**Best practices:**
* Keep filters as simple as possible
* Use specific conditions rather than broad wildcards when possible
* Test filter performance in non-production environment
* Monitor `audit_log_filter_events_filtered` to see filter effectiveness

### Impact of blocking queries

Blocking queries (using `abort: true`) has minimal additional overhead compared to logging:

**Performance impact:**
* Similar to logging, but query execution is prevented
* Slightly faster than logging (no disk write needed for blocked queries)
* Network overhead for error messages to client

**Considerations:**
* Blocking can affect application behavior
* Ensure applications handle blocked query errors gracefully
* Test blocking filters thoroughly before production deployment

### Monitoring performance impact

Use status variables to monitor performance:

**Key metrics:**
* `audit_log_filter_events` - Total events processed
* `audit_log_filter_events_written` - Events written to log
* `audit_log_filter_events_filtered` - Events filtered out
* `audit_log_filter_events_lost` - Events lost (buffer overflow)
* `audit_log_filter_write_waits` - Buffer wait count (async mode)

**Thresholds:**
* `audit_log_filter_events_lost > 0` → Increase buffer size or reduce logging
* `audit_log_filter_write_waits` increasing → Performance degradation, consider reducing logging scope
* High ratio of `events_filtered` to `events` → Filters are working effectively

**Performance tuning:**
* If `events_lost > 0`: Increase `audit_log_filter.buffer_size`
* If high `write_waits`: Reduce logging scope or use `PERFORMANCE` strategy
* If high CPU usage: Use more selective filters
* If high disk I/O: Enable compression or reduce logging scope
