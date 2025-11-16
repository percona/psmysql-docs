# Write audit_log_filter definitons

When you’re setting up audit log filters in Percona Server for MySQL, you use JSON values to define those filters. At their core, a filter is just a JSON object with a very simple structure.

<style>
  table {
    width: 100%;
    border-collapse: collapse;
  }

  th, td {
    padding: 8px;
    text-align: left;
    border: 1px solid #ddd;
  }

  /* Ensure the first column's width matches its content */
  th:first-child, td:first-child {
    white-space: nowrap;
    width: 1%; /* Allows the column to shrink or expand to fit its content */
  }
</style>

| Benefit | Description |
|---|---|
| Reduced Log Volume and Storage | By defining specific rules for what events to log (inclusive filters), you significantly reduce the amount of data written to the audit log. This minimizes log file size, reduces storage requirements, and lowers maintenance overhead. |
| Improved Performance | Smaller log files lead to faster log rotations and less disk I/O, which can improve overall server performance. Reducing log volume also decreases the impact of auditing on the database server itself. |
| Enhanced Security Focus | Instead of logging every single event (which can be overwhelming), you can focus on the most critical events. For example, you can prioritize logging events related to:<br> * Sensitive data access: Log queries that access or modify critical tables.<br> * User account activity: Monitor user logins, password changes, and privilege grants.<br> * DML operations: Log INSERT, UPDATE, and DELETE statements on specific tables.<br> * DDL operations: Log schema changes like CREATE TABLE, ALTER TABLE, and DROP TABLE. |
| Simplified Log Analysis | By filtering out irrelevant events, you make it easier to analyze and investigate security incidents or performance issues. You can quickly identify and focus on the most important events in the audit log. |
| Compliance | Many compliance regulations (for example, PCI DSS, HIPAA) require organizations to audit database activity. Well-defined audit log filters help you meet these compliance requirements by ensuring that the necessary events are being logged. |
| Resource Optimization | By minimizing log volume and optimizing the auditing process, you can conserve valuable system resources, such as CPU, memory, and disk space. |

## Basic structure

The following is an example of the basic structure of a filter.

```json
{
  "filter": {
    "class": [
      {
        "name": "class_type",
        "option1": ["value1", "value2"],
        "option2": ["value3"]
      }
    ]
  }
}
```

The `filter` is the root key in the configuration, which tells the system that you're setting up a filter for capturing or excluding specific events. Inside the filter, there's a key called `class`, which holds an array of different filter definitions. Each object in that array represents a specific rule for filtering events based on certain conditions.

Inside each filter object, you'll have a few essential parts: The name is where you define the `event class` you're targeting, like `connection` or `table_access`. This name tells the filter what type of event you want to track. For example, `class_type` is just a placeholder name for any event class you can filter.

Then, you have option1, which specifies additional filtering criteria. This criteria could be specific users, actions, or other event properties. For example, if you have ["value1", "value2"] in option1, the filter will include events that match either value1 or value2. The filter also includes option2, which is another set of filtering criteria. It works similarly to option1 but focuses on a different property. So if option2 has ["value3"], it will capture events that match value3.

### Practical example

The following code is an example of a filter:

```json
{
  "filter": {
    "class": [
      {
        "name": "connection",
        "user": ["admin", "developer"],
        "host": ["192.168.0.1"]
      }
    ]
  }
}
```

This filter targets the `connection` class. It matches connections made by users admin or developer from the host `192.168.0.1`. Events meeting these criteria would be logged or processed.

### Log all events

You can enable or disable logging for all events in Percona Server for MySQL using an audit log filter definition.

To start, you can explicitly enable or disable logging for all events by adding a log item to your filter like the following example:

```json
{
  "filter": { "log": true }
}
```

Setting `log`: `true` means all events are logged. If you want to turn logging off completely, set the value to `false`.

You can also leave the `log` item out, like this example:

```json
{
  "filter": { }
}
```

This setting works the same as  `log: true` and logs all events by default.

Now, let’s break down how logging behaves depending on whether the log item is included or not:

<style>
  table {
    width: 100%;
    border-collapse: collapse;
  }

  th, td {
    padding: 8px;
    text-align: left;
    border: 1px solid #ddd;
  }

  /* Ensure the first column's width matches its content */
  th:first-child, td:first-child {
    white-space: nowrap;
    width: 1%; /* Allows the column to shrink or expand to fit its content */
  }
</style>

| Option                     | Details                                                                 |
|----------------------------|-------------------------------------------------------------------------|
| When you include the log item | The value you set (`true` or `false`) determines if events are logged. |
| When you don’t include the log item | If no `class` or `event` items are specified, logging is enabled by default. |

However, if you define specific class or event items, they can have their own log settings to control logging for just those events.

### Log specific event classes

If you want to log specific types of activities, such as connection-related events, you can define `class` item in your filter. 

For example, to log events in the “connection” class, your filter might look like this example.

```json
{
  "filter": {
    "class": { "name": "connection" }
  }
}
```

In the example, the outermost element is "filter", which represents the audit log filter you’re defining. Everything within this key specifies what you want to track in the audit logs.

Inside "filter", you have a "class" element. This tells the server the general category of events you’re interested in. In this example, "class" is set to { "name": "connection" }. The "name" key within the "class" specifies the type of events within the connection category that should be logged. By using "connection", you’re instructing the server to monitor connection-related events, such as when users connect to or disconnect from the database.

This structure makes it easy to focus your logging on specific areas of activity in the server, helping you capture only the data you need without cluttering your logs with unnecessary details.

The following filter definition does the same thing, but explicitly states that no other logging is filtered.

```json
{
  "filter": {
    "log": false,
    "class": { 
      "log": true, 
      "name": "connection" 
    }
  }
}
```

### Log multiple classes or events

To log multiple classes at the same time, you have two options.

Both filters achieve the same goal: they define an audit log filter to log events related to "connection", "general", and "table_access". These examples only differ in how the event classes are listed. 

It’s a comprehensive configuration for monitoring activities at the connection level, general server operations, and specific table interactions. This setup is useful for administrators who want broad visibility into user activity and server behavior.

#### A list

A list is useful when you want to expand the filter later to include more granular settings for each class.

```json
{
  "filter": {
    "class": [
      { "name": "connection" },
      { "name": "general" },
      { "name": "table_access" }
    ]
  }
}
```

#### An array

To simplify, when you have multiple items, you can combine their values into a single array:

```json
{
  "filter": {
    "class": [
      { "name": [ "connection", "general", "table_access" ] }
    ]
  }
}
```
This array object is more concise. You should use it if you do not plan to add additional settings for individual classes.


#### List of event and subclass options

The table shows the available event classes and their subclasses:

<style>
  table {
    width: 100%;
    border-collapse: collapse;
  }

  th, td {
    padding: 8px;
    text-align: left;
    border: 1px solid #ddd;
  }

  /* Ensure the first column's width matches its content */
  th:first-child, td:first-child {
    white-space: nowrap;
    width: 1%; /* Allows the column to shrink or expand to fit its content */
  }
</style>

| Class name        | Event subclass | Details                                                                 |
|---|---|---|
| `connection`      | `connect`        | Tracks when a connection is initiated (successful or not)              |
| `connection`      | `change_user`    | Tracks when a user changes during a session                            |
| `connection`      | `disconnect`     | Tracks when a connection is terminated                                 |
| `general`         | `status`         | Tracks the status of general server operations (for example, query success or failure) |
| `general`         | `command`        | Logs SQL commands issued to the server                                 |
| `table_access`    | `read`           | Logs read statements, like `SELECT` or `INSERT INTO … SELECT`          |
| `table_access`    | `delete`         | Logs delete statements, like `DELETE` or `TRUNCATE TABLE`              |
| `table_access`    | `insert`         | Logs insert statements, like `INSERT` or `REPLACE`                     |
| `table_access`    | `update`         | Logs update statements, like `UPDATE`                                  |

This setup gives you the flexibility to monitor the exact events that are important to you while controlling logging behavior in a detailed way.

### Inclusive filters

Inclusive filters capture specific database events you want to log. They allow you to precisely target and record only the actions you care about.

#### Basic Structure

An inclusive filter uses a JSON configuration that defines which events to include in your audit logging. The filter specifies:

* What type of events to capture

* Which users to track

* What specific actions to log

Common use cases for inclusive filters include security audits, compliance tracking, performance monitoring, and user behavior analysis.

Event tracking can be more precise, which helps reduce unnecessary log noise. By focusing on the specific events that matter, you can enhance security monitoring and ensure that only the most relevant data is logged. This approach not only improves the clarity of your logs but also helps optimize performance by limiting the number of events being recorded, reducing overhead and making it easier to manage the system.

It’s important to consider the performance impact of logging and how it might affect your server. Before deploying your filters in a production environment, test them thoroughly to ensure everything works as expected. 

#### Inclusive filter example 

This filter is useful for monitoring and auditing database changes made by administrative users, particularly to ensure that updates and deletions are tracked.

```json
{
  "filter": {
    "class": [
      {
        "name": "table_access",
        "event": [ 
          { "name": "update"},
          { "name": "delete"}
        ]
      }
    ]
  }
}
```

This filter does one thing: log all update and delete operations performed by admin users. The filter uses the following components:

* "class": The top-level key specifies that the filter applies to the `table_access` class. This class monitors events related to database table interactions.

* "name": "table_access": This defines the event class you want to track. This class captures interactions with database tables, such as read, insert, update, and delete modifications. Specifies the specific class of events

* user: ["admin"]: This specifies that the filter applies only to events performed by the admin user and restricts the filter to only log actions executed by this user.

* event: ["update", "delete"]: This narrows down the filter to track only specific actions. In this case, the filter captures update and delete modifications. Any SELECT (read) or INSERT modifications on tables will not be logged, as they are excluded by this filter.

Inclusive filters give you granular control over your MySQL audit logging, allowing you to capture exactly the information you need without overwhelming your logging system.

### Exclusive filters

Exclusive filters in the audit_log_filter for Percona Server for MySQL let you exclude certain activities from being logged, helping you reduce log size and focus on what matters most. For example, you can filter out routine operations like health checks or background processes to avoid unnecessary clutter in your logs. 

This example defines a filter that `excludes` (negate: true) all table access events ("table_access") by the user "readonly_user". Events for other users or other classes of activity are still being logged unless additional filters are defined.

```json
{
  "filter": {
    "class": [
      {
        "name": "table_access",
        "user": ["readonly_user"],
        "negate": true
      }
    ]
  }
}
```

### Exclusive filter example

```json
{
  "filter": {
    "class": [
      {
        "name": "table_access",
        "user": ["admin", "developer"],
        "database": ["financial"],
        "event": [
          {"name":"update"},
          {"name":"delete"}
        ],
        "status": [1] 
      },
      {
        "name": "connection",
        "user": ["external_service"],
        "status": [0]  
      }
    ]
  }
}
```

This filter captures failed update/delete modifications by admin and developer users in the financial database and successful connections for the `external_service` user

## Best practices

Following a systematic approach helps ensure successful deployment and maintenance when implementing audit log filters. Start by creating broad, inclusive filters that capture a wide range of events, giving you a comprehensive view of your database activity. For example, you might begin by logging all actions from administrative users or all changes on critical databases. As you analyze the captured data, you can refine these filters to focus on specific events, users, or changes that matter most to your organization.

Testing is crucial before deploying filters in production. Set up a non-production environment that mirrors your production setup as closely as possible. This non-production environment allows you to verify that your filters capture the intended events without missing critical information. During testing, pay particular attention to how different filter combinations interact and ensure they don't create any unexpected gaps in your audit coverage.

Log file management requires careful attention. Audit logs can grow rapidly, especially with detailed filtering configurations. Monitor your log file sizes regularly and implement appropriate rotation policies. Consider storage capacity, retention requirements, and system performance when determining how much detail to include in your logs. It's often helpful to calculate expected log growth based on your typical database activity and adjust your rotation policies accordingly.

Performance impact is a critical consideration when implementing detailed logging. More granular filters typically require more system resources to process and store the audit data. Monitor your system's performance metrics while testing different filter configurations. Look for significant changes in query response times, CPU usage, or I/O operations. If you notice performance degradation, consider adjusting your filters to balance capturing necessary audit data and maintaining acceptable system performance. Remember that starting with less detailed logging is often better and gradually increasing it as needed, rather than implementing overly aggressive logging that impacts system performance.


## Implement the filter

Here's how to define and implement an audit log filter in Percona Server for MySQL 8.4.6:

### Create a filter

To create an audit log filter, use the `audit_log_filter_set_filter()` function. This function takes two parameters: the filter name and the filter definition as a JSON string.

```sql
SELECT audit_log_filter_set_filter('log_all', '{ "filter": { "log": true } }');
```

### Assign filter to users

To assign a filter to specific users, use the `audit_log_filter_set_user()` function. This function takes three parameters: username, userhost, and filtername.

```sql
SELECT audit_log_filter_set_user('%', 'log_all');
```

### Example: Financial tracking filter

Here's a complete example of creating and assigning a comprehensive financial tracking filter:

```sql
-- Create the filter
SELECT audit_log_filter_set_filter('financial_tracking', '{
  "filter": {
    "class": [
      {
        "name": "table_access",
        "user": ["admin", "finance_team"],
        "database": ["financial_db"],
        "table": ["accounts", "transactions"],
        "event": [
          {"name":"insert"},
          {"name":"update"},
          {"name":"delete"],
        ],
        "status": [0, 1]
      },
      {
        "name": "connection",
        "user": ["admin", "finance_team"],
        "event": [
          {"name":"connect"},
          {"name":"disconnect"}
        ],
        "status": [0, 1]
      }
    ]
  }
}');

-- Assign the filter to all users
SELECT audit_log_filter_set_user('%', '%', 'financial_tracking');
```

The filter monitors two main types of activities. First, it watches all changes to your accounts and transactions tables. This monitoring means that the filter logs when someone adds new data, changes existing information, or removes records. You get a complete picture of who's touching your financial data and what they do with it.

The filter tracks both successes and failures. This tracking gives you valuable information about attempted changes that didn't work out, which is helpful for troubleshooting and security monitoring.

Here's what gets logged:

* Every insert, update, and delete action on your financial tables

* All connection attempts from your admin and finance teams, including when they log in and out

* Whether each action has succeeded (status 0) or failed (status 1)

The filter focuses only on activity in your `financial_db` database. This targeted approach makes it easier to find the information you need when you need it.

Tracking all these elements gives you a comprehensive view of who's accessing your financial data, what changes they're making, and whether those changes are successful. This ability is beneficial for security monitoring and compliance requirements.


To verify your filter, you can check the audit tables:

```sql
-- Check created filters
SELECT * FROM mysql.audit_log_filter;

-- Check user assignments
SELECT * FROM mysql.audit_log_user;
```

You can examine your audit log file (the default location is the data directory) to check if events are being logged.
