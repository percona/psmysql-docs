# Audit Log Filter Tutorial

This tutorial provides step-by-step instructions for installing and configuring the Audit Log Filter plugin in Percona Server for MySQL using Docker, including comprehensive verification steps.

## Overview

The Audit Log Filter plugin allows you to monitor, log, and block connections or queries executed on your MySQL server. This tutorial covers:

* Docker installation of Percona Server for MySQL 8.0 using Docker volumes

* Manual installation and configuration of Audit Log Filter plugin

* Starting with NEW format logging and changing to JSON format

* Comprehensive verification of plugin, tables, and variables

* Testing audit logging functionality in both formats

* Comparing NEW and JSON audit log outputs

* Troubleshooting common Percona Server initialization issues

## Prerequisites

Before starting, ensure you have:

* Docker and Docker Compose installed

* Basic understanding of MySQL administration

* `AUDIT_ADMIN` privilege (handled automatically with root user)

## Step 1: Prepare Docker Environment


### Create Directory Structure

```{.bash data-prompt="$"}
# Create directories for configuration and logs
mkdir -p percona-audit-tutorial/{config,logs,scripts}

# Navigate to the tutorial directory
cd percona-audit-tutorial

# Create the audit log directory
mkdir -p logs
```

### Create MySQL Configuration File

Create a configuration file with audit log filter settings:

```bash
# Create the config directory
mkdir -p config

# Create a standard MySQL configuration file
cat > config/my.cnf << 'EOF'
[mysqld]
# Basic MySQL configuration
bind-address = 0.0.0.0
port = 3306
max_connections = 200
EOF
```

### Create Docker Compose File

```bash
cat > docker-compose.yml << 'EOF'

services:
  percona-audit:
    image: percona/percona-server:8.0
    container_name: percona-audit-tutorial
    hostname: percona-audit
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: mysecretpassword
      MYSQL_DATABASE: testdb
      MYSQL_USER: audituser
      MYSQL_PASSWORD: AuditUser123!
    volumes:
      - ./config/my.cnf:/etc/mysql/conf.d/audit.cnf:ro
      - ./logs:/var/log/mysql
      - percona-data:/var/lib/mysql
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-pmysecretpassword"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 60s

volumes:
  percona-data:
    driver: local
EOF
```
!!! important

    The passwords are stored in plain text for this demo only. Replace them with secrets in real deployments.

## Step 2: Start Percona Server

### Launch the Container

```bash
# Start the Percona Server container
docker-compose up -d --pull always

# Check container status
docker-compose ps

# View container logs (this will show the initialization process)
# Use the service name from your docker-compose.yml
docker-compose logs -f percona-audit
# OR if your service is named differently (e.g., percona-audit-demo):
# docker-compose logs -f percona-audit-demo
```

??? example "Expected output"

    ```{.text .no-copy}
    [+] Running 1/1
    ✔ percona-audit Pulled                                                                1.1s 
    [+] Running 3/3
    ✔ Network percona-audit-tutorial_default        Created                               0.0s 
    ✔ Volume "percona-audit-tutorial_percona-data"  Created                               0.0s 
    ✔ Container percona-audit-tutorial              Started                               0.1s 
    NAME                     IMAGE                        COMMAND                  SERVICE         CREATED                  STATUS                                     PORTS
    percona-audit-tutorial   percona/percona-server:8.0   "/docker-entrypoint.…"   percona-audit   Less than a second ago   Up Less than a second (health: starting)   0.0.0.0:3306->3306/tcp, [::]:3306->3306/tcp
    percona-audit-tutorial  | Initializing database
    ...
    percona-audit-tutorial  | 2025-10-09T10:36:31.541952Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: ready for connections. Version: '8.0.43-34'  socket: '/var/lib/mysql/mysql.sock'  port: 3306  Percona Server (GPL), Release 34, Revision e2841f91.

    ```

Wait for the container to be healthy and fully initialized. The first startup may take 1-2 minutes as MySQL initializes its system tables.

The key line that indicates the server is ready to accept connections is:

```percona-audit-tutorial | 2025-10-09T10:36:31.541952Z 0 [System] [MY-010931] [Server] /usr/sbin/mysqld: **ready for connections.** Version: '8.0.43-34' socket: '/var/lib/mysql/mysql.sock' port: 3306 Percona Server (GPL), Release 34, Revision e2841f91.```

The message, "ready for connections," confirms that the MySQL server process (mysqld) has completed its startup routine, including initializing the storage engine (InnoDB) and opening the network ports (port 3306 for standard MySQL and port 33060 for the X Plugin), and is now actively listening for client connections.

To exit the log results, use `ctrl-C` twice.

## Step 3: Install Audit Log Filter Plugin

We install the audit plugin manually after MySQL is running. This approach ensures MySQL starts properly first, then we configure the audit logging.

### Connect to the Container

```bash
# Connect to MySQL as root
# Use the container name from your docker-compose.yml
docker exec -it percona-audit-tutorial mysql -uroot -pmysecretpassword
# OR if your container is named differently (e.g., percona-audit-demo):
# docker exec -it percona-audit-demo mysql -uroot -pmysecretpassword
```

??? example "Expected output"

    ```{.text .no-copy}
    mysql: [Warning] Using a password on the command line interface can be insecure.
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 32
    Server version: 8.0.43-34 Percona Server (GPL), Release 34, Revision e2841f91

    Copyright (c) 2009-2025 Percona LLC and/or its affiliates
    Copyright (c) 2000, 2025, Oracle and/or its affiliates.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    mysql>
    ```

### Install and Configure the Plugin

-- Step 1: Install the audit log filter plugin

```mysql

mysql> SOURCE /usr/share/mysql/audit_log_filter_linux_install.sql;
```

??? example "Expected output"

    ```{.text .no-copy}
    Empty set, 1 warning (0.00 sec)

    Query OK, 0 rows affected (0.00 sec)

    Query OK, 0 rows affected (0.00 sec)

    Query OK, 0 rows affected (0.00 sec)

    Query OK, 0 rows affected (0.01 sec)
    Statement prepared

    Query OK, 0 rows affected (0.01 sec)

    Query OK, 0 rows affected (0.00 sec)

    Query OK, 0 rows affected (0.00 sec)
    Statement prepared

    Query OK, 0 rows affected (0.01 sec)

    Query OK, 0 rows affected (0.00 sec)

    Query OK, 0 rows affected, 1 warning (0.01 sec)

    Query OK, 0 rows affected (0.00 sec)

    Query OK, 0 rows affected (0.00 sec)

    Query OK, 0 rows affected (0.00 sec)
    ```

```mysql
mysql> exit
```

??? example "Expected output"

    mysql> 
    ```{.text .no-copy}
    Bye
    ```



```bash

cat >> config/my.cnf << 'EOF'

# Audit Log Configuration
audit_log_filter_format=NEW
audit_log_filter_file=audit.log
audit_log_filter_strategy=ASYNCHRONOUS
EOF

# Restart the container (required for audit log configuration changes to take effect)
docker-compose down
docker-compose up -d --force-recreate
```

??? example "Expected output"

    ```{.text .no-copy}
    [+] Running 2/2
    ✔ Container percona-audit-tutorial        Remov...                                    3.4s 
    ✔ Network percona-audit-tutorial_default  Removed                                     0.2s 
    [+] Running 2/2
    ✔ Network percona-audit-tutorial_default  Created                                     0.0s 
    ✔ Container percona-audit-tutorial        Start...
    ```

```bash
docker exec -it percona-audit-tutorial mysql -uroot -pmysecretpassword
```

??? example "Expected output"

    ```{.text .no-copy}
    mysql: [Warning] Using a password on the command line interface can be insecure.
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 16
    Server version: 8.0.43-34 Percona Server (GPL), Release 34, Revision e2841f91

    Copyright (c) 2009-2025 Percona LLC and/or its affiliates
    Copyright (c) 2000, 2025, Oracle and/or its affiliates.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    mysql>
    ```

```mysql
mysql> SHOW GLOBAL VARIABLES LIKE "audit%";
```

??? example "Expected output"

    ```{.text .no-copy}
    +-------------------------------------------------------+------------------+
    | Variable_name                                         | Value            |
    +-------------------------------------------------------+------------------+
    | audit_log_filter_buffer_size                          | 1048576          |
    | audit_log_filter_compression                          | NONE             |
    | audit_log_filter_database                             | mysql            |
    | audit_log_filter_disable                              | OFF              |
    | audit_log_filter_encryption                           | NONE             |
    | audit_log_filter_file                                 | audit_filter.log |
    | audit_log_filter_filter_id                            | 0                |
    | audit_log_filter_format                               | NEW              |
    | audit_log_filter_format_unix_timestamp                | OFF              |
    | audit_log_filter_handler                              | FILE             |
    | audit_log_filter_key_derivation_iterations_count_mean | 600000           |
    | audit_log_filter_max_size                             | 1073741824       |
    | audit_log_filter_password_history_keep_days           | 0                |
    | audit_log_filter_prune_seconds                        | 0                |
    | audit_log_filter_read_buffer_size                     | 32768            |
    | audit_log_filter_rotate_on_size                       | 1073741824       |
    | audit_log_filter_strategy                             | ASYNCHRONOUS     |
    | audit_log_filter_syslog_facility                      | LOG_USER         |
    | audit_log_filter_syslog_priority                      | LOG_INFO         |
    | audit_log_filter_syslog_tag                           | audit-filter     |
    +-------------------------------------------------------+------------------+
    20 rows in set (0.01 sec)
    ```

## Step 4: Comprehensive Verification

### 4.1 Verify Plugin Installation

```sql
-- Check if the audit log filter plugin is installed and active
SELECT 
    PLUGIN_NAME, 
    PLUGIN_STATUS, 
    PLUGIN_TYPE,
    PLUGIN_LIBRARY,
    PLUGIN_LICENSE
FROM INFORMATION_SCHEMA.PLUGINS 
WHERE PLUGIN_NAME LIKE 'audit%';
```


**Expected Output:**
```
+------------------+---------------+-------------+---------------------+----------------+
| PLUGIN_NAME      | PLUGIN_STATUS | PLUGIN_TYPE | PLUGIN_LIBRARY      | PLUGIN_LICENSE |
+------------------+---------------+-------------+---------------------+----------------+
| audit_log_filter | ACTIVE        | AUDIT       | audit_log_filter.so | GPL            |
+------------------+---------------+-------------+---------------------+----------------+
1 row in set (0.00 sec)

### 4.2 Verify Audit Log Filter Tables

```sql

SHOW TABLES FROM mysql LIKE 'audit_log%';
```

```
+------------------------------+
| Tables_in_mysql (audit_log%) |
+------------------------------+
| audit_log_filter             |
| audit_log_user               |
+------------------------------+
2 rows in set (0.00 sec)
```

```mysql
DESCRIBE mysql.audit_log_filter;
DESCRIBE mysql.audit_log_user;
```

```
+-----------+--------------+------+-----+---------+----------------+
| Field     | Type         | Null | Key | Default | Extra          |
+-----------+--------------+------+-----+---------+----------------+
| filter_id | int unsigned | NO   | PRI | NULL    | auto_increment |
| name      | varchar(255) | NO   | UNI | NULL    |                |
| filter    | json         | NO   |     | NULL    |                |
+-----------+--------------+------+-----+---------+----------------+
3 rows in set (0.00 sec)

+------------+--------------+------+-----+---------+-------+
| Field      | Type         | Null | Key | Default | Extra |
+------------+--------------+------+-----+---------+-------+
| username   | varchar(32)  | NO   | PRI | NULL    |       |
| userhost   | varchar(255) | NO   | PRI | NULL    |       |
| filtername | varchar(255) | NO   | MUL | NULL    |       |
+------------+--------------+------+-----+---------+-------+
3 rows in set (0.00 sec)
```

-- Check table contents (should be empty initially)
SELECT COUNT(*) as filter_count FROM mysql.audit_log_filter;
SELECT COUNT(*) as user_count FROM mysql.audit_log_user;
```


```
+--------------+
| filter_count |
+--------------+
|            0 |
+--------------+
1 row in set (0.01 sec)

+------------+
| user_count |
+------------+
|          0 |
+------------+
1 row in set (0.00 sec)
```

### 4.3 Verify Audit Log Filter Variables

```sql
-- Check all audit log filter variables
SHOW VARIABLES LIKE 'audit_log_filter%';

-- Check specific important variables
SELECT 
    VARIABLE_NAME,
    VARIABLE_VALUE,
    @@GLOBAL.audit_log_filter as plugin_status
FROM INFORMATION_SCHEMA.GLOBAL_VARIABLES 
WHERE VARIABLE_NAME IN (
    'audit_log_filter',
    'audit_log_filter_format',
    'audit_log_filter_file',
    'audit_log_filter_database',
    'audit_log_filter_strategy',
    'audit_log_filter_buffer_size',
    'audit_log_filter_rotate_on_size',
    'audit_log_filter_max_size'
);
```

**Expected Output:**
```
+--------------------------------+------------------+
| VARIABLE_NAME                  | VARIABLE_VALUE   |
+--------------------------------+------------------+
| audit_log_filter               | ON               |
| audit_log_filter_buffer_size   | 1048576          |
| audit_log_filter_compression   | NONE             |
| audit_log_filter_database      | mysql            |
| audit_log_filter_disable       | OFF              |
| audit_log_filter_encryption    | NONE             |
| audit_log_filter_file          | audit.json       |
| audit_log_filter_format        | JSON             |
| audit_log_filter_handler       | FILE             |
| audit_log_filter_max_size      | 1073741824       |
| audit_log_filter_rotate_on_size| 1073741824       |
| audit_log_filter_strategy      | ASYNCHRONOUS     |
+--------------------------------+------------------+
```


## Step 5: Create Filters and Test Audit Logging

### 5.1 Create a Test Filter

```sql
-- Create a filter that logs all events
SELECT audit_log_filter_set_filter('log_all', '{ "filter": { "log": true } }');
```

```
-------------------------------------------------------------------------+
| audit_log_filter_set_filter('log_all', '{ "filter": { "log": true } }') |
+-------------------------------------------------------------------------+
| OK                                                                      |
+-------------------------------------------------------------------------+
1 row in set (0.01 sec)
```

```
-- Assign the filter to all users
SELECT audit_log_filter_set_user('%', 'log_all');
```

```
+-------------------------------------------+
| audit_log_filter_set_user('%', 'log_all') |
+-------------------------------------------+
| OK                                        |
+-------------------------------------------+
1 row in set (0.01 sec)
```

```
-- Verify filter creation
SELECT * FROM mysql.audit_log_filter;
SELECT * FROM mysql.audit_log_user;
```

```
+-----------+---------+---------------------------+
| filter_id | name    | filter                    |
+-----------+---------+---------------------------+
|         1 | log_all | {"filter": {"log": true}} |
+-----------+---------+---------------------------+
1 row in set (0.00 sec)

+----------+----------+------------+
| username | userhost | filtername |
+----------+----------+------------+
| %        | %        | log_all    |
+----------+----------+------------+
1 row in set (0.00 sec)
```

### 5.2 Perform Test Operations

```sql
-- Create test database and table
CREATE DATABASE audit_test;
USE audit_test;
CREATE TABLE test_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert test data
INSERT INTO test_table (name) VALUES ('Test User 1'), ('Test User 2'), ('Test User 3');

-- Query the data
SELECT * FROM test_table;
SELECT COUNT(*) FROM test_table WHERE name LIKE 'Test%';

-- Update data
UPDATE test_table SET name = 'Updated User' WHERE id = 1;

-- Delete data
DELETE FROM test_table WHERE id = 3;

-- Drop the test database
DROP DATABASE audit_test;
```

### 5.3 Verify Audit Log Generation

```sql
-- Check audit log statistics
SELECT 
    VARIABLE_NAME,
    VARIABLE_VALUE
FROM performance_schema.global_status 
WHERE VARIABLE_NAME LIKE 'audit_log_filter%'
ORDER BY VARIABLE_NAME;
```


```
+--------------------------------------+----------------+
| VARIABLE_NAME                        | VARIABLE_VALUE |
+--------------------------------------+----------------+
| Audit_log_filter_current_size        | 41300          |
| Audit_log_filter_direct_writes       | 0              |
| Audit_log_filter_event_max_drop_size | 0              |
| Audit_log_filter_events              | 1019           |
| Audit_log_filter_events_filtered     | 0              |
| Audit_log_filter_events_lost         | 0              |
| Audit_log_filter_events_written      | 102            |
| Audit_log_filter_total_size          | 41300          |
| Audit_log_filter_write_waits         | 0              |
+--------------------------------------+----------------+
9 rows in set (0.01 sec)
```

### 5.4 Read Audit Log (NEW Format)

For NEW format, you need to read the physical log file directly since the `audit_log_read_bookmark()` and `audit_log_read()` functions are only available for JSON format.

First, exit MySQL and return to your host terminal:

```sql
mysql> exit
```

Then run these commands from your host terminal:

```bash
# Check if audit log file exists in the MySQL data directory
docker exec percona-audit-tutorial ls -la /var/lib/mysql/audit_filter.log

# View the audit log file content (NEW format)
docker exec percona-audit-tutorial head -20 /var/lib/mysql/audit_filter.log

# View the last 20 lines of the log
docker exec percona-audit-tutorial tail -20 /var/lib/mysql/audit_filter.log

# Check log file size
docker exec percona-audit-tutorial du -h /var/lib/mysql/audit_filter.log
```


-rw-r----- 1 mysql mysql 534726 Oct 10 14:24 /var/lib/mysql/audit_filter.log
<?xml version="1.0" encoding="utf-8"?>
<AUDIT>
  <AUDIT_RECORD>
    <NAME>Audit</NAME>
    <RECORD_ID>0_2025-10-10T14:05:54</RECORD_ID>
    <TIMESTAMP>2025-10-10T14:05:54</TIMESTAMP>
    <SERVER_ID>1</SERVER_ID>
  </AUDIT_RECORD>
  <AUDIT_RECORD>
    <NAME>Execute</NAME>
    <RECORD_ID>1_2025-10-10T14:05:54</RECORD_ID>
    <TIMESTAMP>2025-10-10T14:05:54</TIMESTAMP>
    <COMMAND_CLASS>change_db</COMMAND_CLASS>
    <CONNECTION_ID>4</CONNECTION_ID>
    <HOST></HOST>
    <IP></IP>
    <USER>skip-grants user[] @  []</USER>
    <OS_LOGIN></OS_LOGIN>
    <SQLTEXT>USE mysql</SQLTEXT>
    <STATUS>0</STATUS>
        <VALUE>aarch64</VALUE>
      </ATTRIBUTE>
      <ATTRIBUTE>
        <NAME>_os</NAME>
        <VALUE>Linux</VALUE>
      </ATTRIBUTE>
      <ATTRIBUTE>
        <NAME>_client_name</NAME>
        <VALUE>libmysql</VALUE>
      </ATTRIBUTE>
      <ATTRIBUTE>
        <NAME>_client_version</NAME>
        <VALUE>8.0.43-34</VALUE>
      </ATTRIBUTE>
      <ATTRIBUTE>
        <NAME>program_name</NAME>
        <VALUE>mysqladmin</VALUE>
      </ATTRIBUTE>
    </CONNECTION_ATTRIBUTES>
  </AUDIT_RECORD>
528K	/var/lib/mysql/audit_filter.log
```




## Step 6: Change Audit Log Format from NEW to JSON

### 6.1 Stop the Container and Change Format


```bash
# Stop the container
docker-compose down

# Remove existing audit log files (format change requires clean start)
docker exec percona-audit-tutorial bash -c "rm -f /var/lib/mysql/audit_filter.log /var/lib/mysql/audit_filter.*.log" 2>/dev/null || true

# Update the configuration file to use JSON format
cat > config/my.cnf << 'EOF'
[mysqld]
# Basic MySQL configuration
bind-address = 0.0.0.0
port = 3306
max_connections = 200

# Audit Log Configuration - JSON Format
audit_log_filter_format=JSON
audit_log_filter_file=audit_filter.json
audit_log_filter_strategy=ASYNCHRONOUS
EOF
```
```
[+] Running 2/2
 ✔ Container percona-audit-tutorial        Remov...                                    3.3s 
 ✔ Network percona-audit-tutorial_default  Removed                                     0.2s 
zsh: no matches found: /var/lib/mysql/audit_filter.*.log
```

### 6.2 Restart Container with New Configuration

```bash
# Restart the container with new configuration (required for format change to take effect)
docker-compose up -d

# Wait for the container to be healthy (non-interactive)
echo Waiting for container to be ready...
sleep 10
echo Container should be ready now!

# Alternative: Interactive approach (uncomment if you prefer)
# docker-compose logs -f percona-audit
# Press Ctrl+C to exit the logs when you see "ready for connections"
```

**Expected Output:**
```
[+] Running 2/2
 ✔ Network percona-audit-tutorial_default  Created                                     0.0s 
 ✔ Container percona-audit-tutorial        Start...                                    0.2s 
Waiting for container to be ready...
Container should be ready now!
```

### 6.3 Perform New Operations to Generate JSON Logs

```bash
# Connect to MySQL
docker exec -it percona-audit-tutorial mysql -uroot -pmysecretpassword
```

```
mysql: [Warning] Using a password on the command line interface can be insecure.
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 21
Server version: 8.0.43-34 Percona Server (GPL), Release 34, Revision e2841f91

Copyright (c) 2009-2025 Percona LLC and/or its affiliates
Copyright (c) 2000, 2025, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 
```

```sql
-- Create a new test database to generate fresh audit events
CREATE DATABASE json_audit_test;
USE json_audit_test;

-- Create a test table
CREATE TABLE json_test_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert test data
INSERT INTO json_test_table (message) VALUES 
    ('JSON Format Test 1'), 
    ('JSON Format Test 2'), 
    ('JSON Format Test 3');

-- Query the data
SELECT * FROM json_test_table;
SELECT COUNT(*) FROM json_test_table WHERE message LIKE 'JSON%';

-- Update data
UPDATE json_test_table SET message = 'Updated JSON Test' WHERE id = 1;

-- Delete data
DELETE FROM json_test_table WHERE id = 3;

-- Drop the test database
DROP DATABASE json_audit_test;
```

### 6.4 Read Audit Log (JSON Format)

```sql
-- Get the latest bookmark for JSON format
SELECT audit_log_read_bookmark();

-- Read recent audit events in JSON format
SELECT audit_log_read(audit_log_read_bookmark());

-- Read specific number of events
SELECT audit_log_read(audit_log_read_bookmark(), 10);
```

### 6.5 Check Physical Log File (JSON Format)

```bash
# Check if the new JSON audit log file exists
docker exec percona-audit-tutorial ls -la /var/lib/mysql/audit_filter.json

# View the JSON audit log file content
docker exec percona-audit-tutorial head -20 /var/lib/mysql/audit_filter.json

# Check JSON log file size
docker exec percona-audit-tutorial du -h /var/lib/mysql/audit_filter.json

# View both log files for comparison
docker exec percona-audit-tutorial ls -la /var/lib/mysql/audit_filter*
```

**Expected JSON Format Output:**
```json
{"timestamp":"2024-01-15T10:35:45 UTC","id":1,"class":"connection","event":"connect","connection_id":6,"status":0,"user":"root","priv_user":"root","external_user":"","proxy_user":"","host":"localhost","ip":"127.0.0.1","database":"json_audit_test","connection_data":{"os_user":"","os_priv_user":"","os_proxy_user":""}}
{"timestamp":"2024-01-15T10:35:46 UTC","id":2,"class":"general","event":"query","connection_id":6,"status":0,"user":"root","priv_user":"root","external_user":"","proxy_user":"","host":"localhost","ip":"127.0.0.1","database":"json_audit_test","sqltext":"CREATE DATABASE json_audit_test","connection_data":{"os_user":"","os_priv_user":"","os_proxy_user":""}}
{"timestamp":"2024-01-15T10:35:47 UTC","id":3,"class":"general","event":"query","connection_id":6,"status":0,"user":"root","priv_user":"root","external_user":"","proxy_user":"","host":"localhost","ip":"127.0.0.1","database":"json_audit_test","sqltext":"CREATE TABLE json_test_table ( id INT AUTO_INCREMENT PRIMARY KEY, message VARCHAR(100), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP )","connection_data":{"os_user":"","os_priv_user":"","os_proxy_user":""}}
```

### 6.6 Compare Both Formats

```bash
# Compare the two log files side by side
docker exec percona-audit-tutorial echo "=== NEW FORMAT (audit_filter.log) ==="
docker exec percona-audit-tutorial head -5 /var/lib/mysql/audit_filter.log

docker exec percona-audit-tutorial echo "=== JSON FORMAT (audit_filter.json) ==="
docker exec percona-audit-tutorial head -5 /var/lib/mysql/audit_filter.json
```

**Key Differences:**
- **NEW Format**: XML-like structure with tags, more verbose, human-readable
- **JSON Format**: Compact JSON structure, machine-readable, better for parsing and analysis

## Step 7: Advanced Testing

### 7.1 Test Different Filter Types

```sql
-- Create a filter for specific events only
SELECT audit_log_filter_set_filter('connection_only', 
    '{ "filter": { "class": { "name": "connection", "log": true } } }');

-- Create a filter for specific users
SELECT audit_log_filter_set_filter('user_specific', 
    '{ "filter": { "log": true, "user": { "name": "audituser", "log": true } } }');

-- Assign user-specific filter
SELECT audit_log_filter_set_user('audituser@%', 'user_specific');

-- List all filters
SELECT * FROM mysql.audit_log_filter;
SELECT * FROM mysql.audit_log_user;
```

### 7.2 Test Filter Removal

```sql
-- Remove user assignment
SELECT audit_log_filter_remove_user('audituser@%');

-- Remove filter
SELECT audit_log_filter_remove_filter('user_specific');

-- Verify removal
SELECT * FROM mysql.audit_log_filter;
SELECT * FROM mysql.audit_log_user;
```

## Step 8: Monitoring and Maintenance

### 8.1 Monitor Audit Log Performance

```sql
-- Check for lost events
SELECT 
    audit_log_filter_events_lost,
    audit_log_filter_events_written,
    audit_log_filter_write_waits
FROM performance_schema.global_status 
WHERE VARIABLE_NAME LIKE 'audit_log_filter%';
```

### 8.2 Log Rotation Test

```sql
-- Manually rotate the log file
SELECT audit_log_rotate();

-- Check if new file was created
SELECT audit_log_filter_current_size FROM performance_schema.global_status 
WHERE VARIABLE_NAME = 'audit_log_filter_current_size';
```

### 8.3 Cleanup Commands

```bash
# Stop and remove containers
docker-compose down

# Remove volumes (optional - this will delete all data)
docker-compose down -v

# Remove the entire tutorial directory
cd ..
rm -rf percona-audit-tutorial
```

## Troubleshooting

### Quick Reset (If you're having persistent issues)

If you're having persistent issues, use the reset script:

```bash
# Run the reset script to clean everything
./reset-environment.sh

# Then start fresh with the tutorial
mkdir -p percona-audit-tutorial/{config,logs,data,scripts}
cd percona-audit-tutorial
# ... continue with tutorial steps
```

### Common Issues and Solutions

**1. Plugin not loading:**
```sql
-- Check plugin directory
SHOW VARIABLES LIKE 'plugin_dir';

-- Check for plugin file
docker exec percona-audit-tutorial ls -la /usr/lib64/mysql/plugin/audit_log_filter.so
```

**2. Permission errors:**
```sql
-- Grant necessary privileges
GRANT AUDIT_ADMIN ON *.* TO 'audituser'@'%';
FLUSH PRIVILEGES;
```

**3. Configuration not taking effect:**
```bash
# Restart container with new configuration
docker-compose restart
```

**4. No audit events being logged:**
```sql
-- Check if filter is assigned
SELECT * FROM mysql.audit_log_user;

-- Verify filter definition
SELECT * FROM mysql.audit_log_filter;

-- Check if logging is disabled
SHOW VARIABLES LIKE 'audit_log_filter_disable';
```

**5. MySQL system tables missing (mysql.user, mysql.component errors):**
```bash
# Stop the container and remove volumes to force re-initialization
docker-compose down -v

# Remove any existing data directory
rm -rf data/

# Remove the Docker volume to ensure clean initialization
docker volume rm percona-audit-tutorial_percona-data 2>/dev/null || true

# Start the container again (this will trigger MySQL initialization)
docker-compose up -d

# Wait for initialization to complete (this may take 2-3 minutes)
docker-compose logs -f percona-audit
```

**Alternative fix if the above doesn't work:**
```bash
# Complete cleanup and restart
docker-compose down -v
docker system prune -f
docker-compose up -d
```

**6. Container fails to start with privilege table errors:**
```bash
# Check if the container is using the correct image
docker-compose down
docker-compose pull
docker-compose up -d

# If still failing, check the logs for specific errors
docker-compose logs percona-audit
```

**7. Data directory unusable errors:**
```bash
# Complete cleanup of data directory
docker-compose down -v

# Remove the Docker volume completely
docker volume rm percona-audit-tutorial_percona-data 2>/dev/null || true

# Remove any local data directories
rm -rf data/ logs/

# Start fresh
docker-compose up -d

# Monitor the logs
docker-compose logs -f percona-audit
```

**7a. Data directory has files error (bind mount cleanup):**
```bash
# Stop everything
docker-compose down

# Remove ALL local directories completely
rm -rf data/ logs/ config/

# Recreate directories
mkdir -p config logs data

# Ensure data directory is completely empty
rm -rf data/*

# Recreate minimal setup
cat > config/my.cnf << 'EOF'
[mysqld]
bind-address = 0.0.0.0
port = 3306
max_connections = 200
EOF

# Start fresh
docker-compose up -d
```

**7b. If still having issues, use a different data directory:**
```bash
# Stop everything
docker-compose down

# Remove all directories
rm -rf data/ logs/ config/

# Create with different names
mkdir -p config logs mysql-data

# Update docker-compose.yml to use ./mysql-data instead of ./data
# Then start fresh
docker-compose up -d
```

**7c. Percona Server specific fix - use Docker volume instead of bind mount:**
```bash
# Stop everything
docker-compose down

# Remove ALL directories and files
rm -rf data/ logs/ config/ docker-compose.yml

# Create new docker-compose.yml using Docker volume (not bind mount)
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  percona-audit:
    image: percona/percona-server:8.0
    container_name: percona-audit-tutorial
    hostname: percona-audit
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: mysecretpassword
      MYSQL_DATABASE: testdb
      MYSQL_USER: audituser
      MYSQL_PASSWORD: AuditUser123!
    volumes:
      - ./config/my.cnf:/etc/mysql/conf.d/audit.cnf:ro
      - ./logs:/var/lib/mysql/audit
      - percona-data:/var/lib/mysql
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-pmysecretpassword"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 60s

volumes:
  percona-data:
EOF

# Create minimal config
mkdir -p config logs
cat > config/my.cnf << 'EOF'
[mysqld]
bind-address = 0.0.0.0
port = 3306
max_connections = 200
EOF

# Start fresh
docker-compose up -d
```

**7d. If still failing, try Percona Server with different initialization:**
```bash
# Stop everything
docker-compose down -v

# Remove the volume
docker volume rm percona-audit-tutorial_percona-data 2>/dev/null || true

# Use a different approach - let Percona Server handle initialization
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  percona-audit:
    image: percona/percona-server:8.0
    container_name: percona-audit-tutorial
    hostname: percona-audit
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: mysecretpassword
      MYSQL_DATABASE: testdb
      MYSQL_USER: audituser
      MYSQL_PASSWORD: AuditUser123!
    volumes:
      - ./config/my.cnf:/etc/mysql/conf.d/audit.cnf:ro
      - ./logs:/var/lib/mysql/audit
      - percona-data:/var/lib/mysql
    restart: unless-stopped
    command: >
      --initialize-insecure
      --user=mysql
      --datadir=/var/lib/mysql
      --basedir=/usr
      --log-error=/var/log/mysql/error.log
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-pmysecretpassword"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 60s

volumes:
  percona-data:
EOF

# Start fresh
docker-compose up -d
```

**7e. Nuclear option - Complete Docker cleanup:**
```bash
# Stop everything
docker-compose down -v

# Remove ALL Docker volumes
docker volume prune -a -f

# Remove ALL containers
docker container prune -f

# Remove ALL images (optional - will require re-downloading)
docker image prune -a -f

# Remove ALL networks
docker network prune -f

# Remove ALL directories
rm -rf data/ logs/ config/ docker-compose.yml

# Recreate everything from scratch
mkdir -p config logs
cat > config/my.cnf << 'EOF'
[mysqld]
bind-address = 0.0.0.0
port = 3306
max_connections = 200
EOF

# Create docker-compose.yml with fresh volume name
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  percona-audit:
    image: percona/percona-server:8.0
    container_name: percona-audit-tutorial
    hostname: percona-audit
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: mysecretpassword
      MYSQL_DATABASE: testdb
      MYSQL_USER: audituser
      MYSQL_PASSWORD: AuditUser123!
    volumes:
      - ./config/my.cnf:/etc/mysql/conf.d/audit.cnf:ro
      - ./logs:/var/lib/mysql/audit
      - mysql-data-fresh:/var/lib/mysql
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-pmysecretpassword"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 60s

volumes:
  mysql-data-fresh:
EOF

# Start fresh
docker-compose up -d
```

**7f. Alternative - Use standard MySQL image:**
```bash
# Stop everything
docker-compose down

# Remove ALL directories and files
rm -rf data/ logs/ config/ docker-compose.yml

# Create a completely new setup with standard MySQL
mkdir -p mysql-audit-tutorial/{config,logs,data}
cd mysql-audit-tutorial

# Create docker-compose.yml with standard MySQL
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  mysql-audit:
    image: mysql:8.0
    container_name: mysql-audit-tutorial
    hostname: mysql-audit
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: TutorialPassword123!
      MYSQL_DATABASE: testdb
      MYSQL_USER: audituser
      MYSQL_PASSWORD: AuditUser123!
    volumes:
      - ./config/my.cnf:/etc/mysql/conf.d/audit.cnf:ro
      - ./logs:/var/lib/mysql/audit
      - ./data:/var/lib/mysql
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-pTutorialPassword123!"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 60s
EOF

# Create minimal config
cat > config/my.cnf << 'EOF'
[mysqld]
bind-address = 0.0.0.0
port = 3306
max_connections = 200
EOF

# Start fresh
docker-compose up -d
```

**8. MySQL initialization fails with existing files:**
```bash
# Stop everything
docker-compose down -v

# Remove all volumes and containers
docker system prune -a -f

# Remove any local directories
rm -rf data/ logs/ config/

# Recreate the minimal setup
mkdir -p config logs
cat > config/my.cnf << 'EOF'
[mysqld]
bind-address = 0.0.0.0
port = 3306
max_connections = 200
EOF

# Start completely fresh
docker-compose up -d
```

## Summary

This tutorial has covered:

✅ **Docker Installation**: Set up Percona Server for MySQL 8.0 using Docker volumes  
✅ **Manual Plugin Installation**: Installed and configured the Audit Log Filter plugin after MySQL startup  
✅ **Configuration**: Started with NEW format logging and changed to JSON format  
✅ **Verification**: Comprehensive verification of plugin, tables, and variables  
✅ **Format Comparison**: Demonstrated both NEW and JSON audit log formats  
✅ **Testing**: Created and tested audit filters in both formats  
✅ **Monitoring**: Set up monitoring and maintenance procedures  
✅ **Troubleshooting**: Provided comprehensive troubleshooting for Percona Server initialization issues  

The Audit Log Filter is now fully functional and ready for production use. The Docker volume approach with manual plugin installation ensures reliable startup and proper plugin configuration. You can customize filters based on your specific auditing requirements, choose between NEW and JSON formats based on your needs, and monitor the system using the provided SQL queries and monitoring commands.

https://app.warp.dev/block/ESdMWqrX4sXrL9GDrihMsp

### Reset Script (Use if you need to start completely fresh)

Create a reset script to completely clean your environment:

```bash
# Create the reset script
cat > reset-environment.sh << 'EOF'
#!/bin/bash

echo "🧹 Cleaning up audit log filter tutorial environment..."

# Stop and remove all containers
echo "Stopping containers..."
docker-compose down -v 2>/dev/null || true

# Remove all tutorial-related containers
echo "Removing containers..."
docker rm -f percona-audit-tutorial mysql-audit-tutorial mysql-audit-tutorial-2 2>/dev/null || true

# Remove all tutorial-related volumes
echo "Removing volumes..."
docker volume rm percona-audit-tutorial_percona-data 2>/dev/null || true
docker volume rm percona-audit-tutorial_mysql-data 2>/dev/null || true
docker volume rm mysql-audit-tutorial_mysql-data 2>/dev/null || true

# Remove all tutorial directories
echo "Removing directories..."
rm -rf percona-audit-tutorial/ percona-audit-tutorial-2/ mysql-audit-tutorial/ mysql-audit-tutorial-2/
rm -rf data/ logs/ config/ scripts/

# Remove any remaining Docker volumes
echo "Cleaning up unused volumes..."
docker volume prune -f

# Remove any remaining networks
echo "Cleaning up networks..."
docker network prune -f

# Optional: Remove Percona Server image (uncomment if you want to start completely fresh)
# echo "Removing Percona Server image..."
# docker rmi percona/percona-server:8.0.43-34 2>/dev/null || true

echo "✅ Environment reset complete!"
echo "You can now start fresh with the tutorial."
EOF

# Make the script executable
chmod +x reset-environment.sh

# Run the reset script
./reset-environment.sh
```
