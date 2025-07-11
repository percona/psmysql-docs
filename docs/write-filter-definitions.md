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

| Benefit                        | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Reduced Log Volume and Storage | By defining specific rules for what events to log (inclusive filters), you significantly reduce the amount of data written to the audit log. This minimizes log file size, reduces storage requirements, and lowers maintenance overhead.                                                                                                                                                                                                                                                                                       |
| Improved Performance           | Smaller log files lead to faster log rotations and less disk I/O, which can improve overall server performance. Reduced log volume also decreases the impact of auditing on the database server itself.                                                                                                                                                                                                                                                                                                                         |
| Enhanced Security Focus        | Instead of logging every single event (which can be overwhelming), you can focus on the most critical events. For example, you can prioritize logging events related to:<br> - Sensitive data access: Log queries that access or modify critical tables.<br> - User account activity: Monitor user logins, password changes, and privilege grants.<br> - DML operations: Log INSERT, UPDATE, and DELETE statements on specific tables.<br> - DDL operations: Log schema changes like CREATE TABLE, ALTER TABLE, and DROP TABLE. |
| Simplified Log Analysis        | By filtering out irrelevant events, you make it easier to analyze and investigate security incidents or performance issues. You can quickly identify and focus on the most important events in the audit log.                                                                                                                                                                                                                                                                                                                   |
| Compliance                     | Many compliance regulations (e.g., PCI DSS, HIPAA) require organizations to audit database activity. Well-defined audit log filters help you meet these compliance requirements by ensuring that the necessary events are being logged.                                                                                                                                                                                                                                                                                         |
| Resource Optimization          | By minimizing log volume and optimizing the auditing process, you can conserve valuable system resources, such as CPU, memory, and disk space.                                                                                                                                                                                                                                                                                                                                                                                  |

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
  "filter": {}
}
```

This setting works the same as `log: true` and logs all events by default.

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

| Option                              | Details                                                                      |
| ----------------------------------- | ---------------------------------------------------------------------------- |
| When you include the log item       | The value you set (`true` or `false`) determines if events are logged.       |
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
    "class": [{ "name": ["connection", "general", "table_access"] }]
  }
}
```

This array object is more concise. You should use it if you do not plan to add additional settings for individual classes.

#### List of event and subclass options

The available event classes and their subclasses are as follows:

##### General

| Class Name | Event Subclass      | Description                                                                  |
| ---------- | ------------------- | ---------------------------------------------------------------------------- |
| General    | GeneralError        | Represents an error event with details about the error code and context.     |
| General    | GeneralCommand      | Represents a command execution event, detailing the command issued.          |
| General    | GeneralQuery        | Represents a query execution event, detailing the query that was run.        |
| General    | GeneralUser         | Represents an event related to a specific user, detailing user information.  |
| General    | GeneralHost         | Represents an event related to a specific host, detailing host information.  |
| General    | GeneralSQLCommand   | Represents an event related to a specific SQL command executed.              |
| General    | GeneralExternalUser | Represents an event related to an external user interacting with the system. |
| General    | GeneralIP           | Represents an event related to a specific IP address involved in the event.  |

A JSON code sample for General class:

```json
{
  "filter": {
    "class": {
      "name": "general",
      "event_subclasses": [
        {
          "subclass": "GeneralError",
          "sample_value": {
            "general_error_code": "404",
            "general_thread_id": "12345",
            "general_user": {
              "str": "admin",
              "length": 5
            },
            "general_command": {
              "str": "SELECT * FROM users",
              "length": 22
            },
            "general_query": {
              "str": "SELECT * FROM users WHERE id = 1",
              "length": 36
            },
            "general_host": {
              "str": "192.168.0.1",
              "length": 11
            },
            "general_sql_command": {
              "str": "SELECT",
              "length": 6
            },
            "general_external_user": {
              "str": "external_user",
              "length": 14
            },
            "general_ip": {
              "str": "192.168.0.1",
              "length": 11
            }
          }
        }
      ],
      "user": ["admin", "developer"],
      "host": ["192.168.0.1"]
    }
  }
}
```
##### Authentication

| Class Name        | Event Subclass         | Description                                                        |
|--------------------|------------------------|--------------------------------------------------------------------|
| Authentication     | AuthenticationEvent     | Represents an event related to user authentication.                |
| Authentication     | AuthStatusEvent         | Represents an event detailing the status of an authentication attempt. |
| Authentication     | AuthQueryEvent          | Represents an event that includes the query related to authentication. |
| Authentication     | UserInfoEvent           | Represents an event that includes information about the user attempting authentication. |
| Authentication     | HostInfoEvent           | Represents an event that includes information about the host from which authentication is attempted. |
| Authentication     | PluginInfoEvent         | Represents an event that includes details about the authentication plugin used. |
| Authentication     | NewUserEvent            | Represents an event that includes information about a new user being created during authentication. |
| Authentication     | RoleEvent               | Represents an event indicating whether the authentication is for a role. |

A JSON code sample for Authentication class:

```json
{
  "filter": {
    "class": {
      "name": "authentication",
      "event_subclasses": [
        {
          "subclass": "AuthenticationEvent",
          "sample_value": {
            "status": "success",
            "connection_id": "conn12345",
            "sql_command_id": "cmd67890",
            "query": {
              "str": "SELECT * FROM users WHERE username = 'admin'",
              "length": 45
            },
            "user": {
              "str": "admin",
              "length": 5
            },
            "host": {
              "str": "192.168.0.1",
              "length": 11
            },
            "authentication_plugin": {
              "str": "mysql_native_password",
              "length": 20
            },
            "new_user": {
              "str": "new_admin",
              "length": 9
            },
            "new_host": {
              "str": "192.168.0.2",
              "length": 11
            },
            "is_role": "0"
          }
        }
      ],
      "user": ["admin", "developer"],
      "host": ["192.168.0.1"]
    }
  }
}
```

##### StartAudit

| Class Name      | Event Subclass      | Description                                                        |
|------------------|---------------------|--------------------------------------------------------------------|
| StartAudit       | StartAuditEvent      | Represents an event related to the initiation of an audit process. |
| StartAudit       | ServerInfoEvent      | Represents an event that includes information about the server initiating the audit. |

A JSON code sample for Start Audit class:

```json
{
  "filter": {
    "class": {
      "name": "start_audit",
      "event_subclasses": [
        {
          "subclass": "StartAuditEvent",
          "sample_value": {
            "server_id": "server123"
          }
        }
      ],
      "user": ["admin"],
      "host": ["192.168.0.1"]
    }
  }
}
```

##### StopAudit

| Class Name      | Event Subclass      | Description                                                        |
|------------------|---------------------|--------------------------------------------------------------------|
| StopAudit        | StopAuditEvent       | Represents an event related to the termination of an audit process. |
| StopAudit        | ServerInfoEvent      | Represents an event that includes information about the server stopping the audit. |

A JSON code sample for Stop Audit class:

```json
{
  "filter": {
    "class": {
      "name": "stop_audit",
      "event_subclasses": [
        {
          "subclass": "StopAuditEvent",
          "sample_value": {
            "server_id": "server123"
          }
        }
      ],
      "user": ["admin"],
      "host": ["192.168.0.1"]
    }
  }
}
```

##### Command

| Class Name | Event Subclass | Description                                                       |
| ---------- | -------------- | ----------------------------------------------------------------- |
| Command    | CommandEvent   | Represents an event related to the execution of a command.        |
| Command    | CommandStatus  | Represents an event detailing the status of a command execution.  |
| Command    | CommandIDEvent | Represents an event that includes the ID of the executed command. |

A JSON code sample for Command class:

```json
{
  "filter": {
    "class": {
      "name": "command",
      "event_subclasses": [
        {
          "subclass": "CommandEvent",
          "sample_value": {
            "status": "success",
            "connection_id": "conn12345",
            "command_id": "cmd67890"
          }
        }
      ],
      "user": ["admin", "developer"],
      "host": ["192.168.0.1"]
    }
  }
}
```

##### Connection

| Class Name | Event Subclass          | Description                                                                                                  |
| ---------- | ----------------------- | ------------------------------------------------------------------------------------------------------------ |
| Connection | ConnectionEstablished   | Represents a successful connection establishment to a database or service.                                   |
| Connection | ConnectionClosed        | Indicates that a connection has been closed, either normally or due to an error.                             |
| Connection | ConnectionFailed        | Represents a failed attempt to establish a connection, often including error codes or messages.              |
| Connection | ConnectionTimeout       | Indicates that a connection attempt timed out before it could be established.                                |
| Connection | ConnectionDropped       | Represents a connection that was unexpectedly terminated, possibly due to network issues or server problems. |
| Connection | ConnectionReused        | Indicates that an existing connection was reused for a new request.                                          |
| Connection | ConnectionAuthenticated | Represents an event where a connection was successfully authenticated.                                       |
| Connection | ConnectionUnauthorized  | Indicates an attempt to connect that was rejected due to insufficient permissions or invalid credentials.    |

A JSON code sample for Connection class:

```JSON
{
  "filter": {
    "class": {
      "name": "connection",
      "event_subclasses": [
        {
          "subclass": "ConnectionEstablished",
          "sample_value": {
            "timestamp": "2025-07-11T10:00:00Z",
            "user": "admin",
            "host": "192.168.0.1",
            "connection_id": "conn12345"
          }
        },
        {
          "subclass": "ConnectionClosed",
          "sample_value": {
            "timestamp": "2025-07-11T10:05:00Z",
            "user": "developer",
            "host": "192.168.0.1",
            "connection_id": "conn12345"
          }
        },
        {
          "subclass": "ConnectionFailed",
          "sample_value": {
            "timestamp": "2025-07-11T10:10:00Z",
            "user": "admin",
            "host": "192.168.0.1",
            "error_code": "ERR_CONN_TIMEOUT"
          }
        },
        {
          "subclass": "ConnectionTimeout",
          "sample_value": {
            "timestamp": "2025-07-11T10:15:00Z",
            "user": "developer",
            "host": "192.168.0.1",
            "timeout_duration": "30s"
          }
        },
        {
          "subclass": "ConnectionDropped",
          "sample_value": {
            "timestamp": "2025-07-11T10:20:00Z",
            "user": "admin",
            "host": "192.168.0.1",
            "connection_id": "conn12345",
            "reason": "Network issue"
          }
        },
        {
          "subclass": "ConnectionReused",
          "sample_value": {
            "timestamp": "2025-07-11T10:25:00Z",
            "user": "developer",
            "host": "192.168.0.1",
            "previous_connection_id": "conn12345",
            "new_connection_id": "conn67890"
          }
        },
        {
          "subclass": "ConnectionAuthenticated",
          "sample_value": {
            "timestamp": "2025-07-11T10:30:00Z",
            "user": "admin",
            "host": "192.168.0.1",
            "authentication_method": "password"
          }
        },
        {
          "subclass": "ConnectionUnauthorized",
          "sample_value": {
            "timestamp": "2025-07-11T10:35:00Z",
            "user": "developer",
            "host": "192.168.0.1",
            "error_code": "ERR_UNAUTHORIZED"
          }
        }
      ],
      "user": ["admin", "developer"],
      "host": ["192.168.0.1"]
    }
  }
}
```

##### GlobalVariable

| Class Name     | Event Subclass       | Description                                                              |
| -------------- | -------------------- | ------------------------------------------------------------------------ |
| GlobalVariable | GlobalVariableEvent  | Represents an event related to accessing or modifying a global variable. |
| GlobalVariable | VariableAccess       | Represents an event detailing the access of a specific global variable.  |
| GlobalVariable | VariableModification | Represents an event that indicates a modification to a global variable.  |
| GlobalVariable | VariableQuery        | Represents an event that includes a query related to a global variable.  |

A JSON code sample for GlobalVariable class:

```json
{
  "filter": {
    "class": {
      "name": "global_variable",
      "event_subclasses": [
        {
          "subclass": "GlobalVariableEvent",
          "sample_value": {
            "connection_id": "conn12345",
            "sql_command_id": "cmd67890",
            "variable_name": {
              "str": "max_connections",
              "length": 15
            },
            "variable_value": {
              "str": "100",
              "length": 3
            }
          }
        }
      ],
      "user": ["admin", "developer"],
      "host": ["192.168.0.1"]
    }
  }
}
```

##### Message

| Class Name      | Event Subclass      | Description                                                        |
|------------------|---------------------|--------------------------------------------------------------------|
| Message          | MessageEvent        | Represents an event related to a log message from a component.     |
| Message          | ComponentInfo       | Represents an event that includes information about the component generating the message. |
| Message          | ProducerInfo        | Represents an event that includes information about the producer of the message. |
| Message          | MessageContent      | Represents an event that includes the actual content of the message. |


A JSON code sample for Message class:

```json
{
  "filter": {
    "class": {
      "name": "message",
      "event_subclasses": [
        {
          "subclass": "MessageEvent",
          "sample_value": {
            "component": {
              "str": "auth_service",
              "length": 13
            },
            "producer": {
              "str": "system",
              "length": 6
            },
            "message": {
              "str": "User admin logged in successfully.",
              "length": 31
            }
          }
        }
      ],
      "user": ["admin", "developer"],
      "host": ["192.168.0.1"]
    }
  }
}
```


##### Query

| Class Name | Event Subclass | Description                                                           |
| ---------- | -------------- | --------------------------------------------------------------------- |
| Query      | QueryEvent     | Represents an event related to the execution of a query.              |
| Query      | QueryStatus    | Represents an event detailing the status of a query execution.        |
| Query      | QueryIDEvent   | Represents an event that includes the ID of the executed SQL command. |
| Query      | QueryString    | Represents an event that includes the actual SQL query string.        |

A JSON code sample for the Query class:

```json
{
  "filter": {
    "class": {
      "name": "query",
      "event_subclasses": [
        {
          "subclass": "QueryEvent",
          "sample_value": {
            "status": "success",
            "connection_id": "conn12345",
            "sql_command_id": "cmd67890",
            "query": {
              "str": "SELECT * FROM users WHERE id = 1",
              "length": 36
            }
          }
        }
      ],
      "user": ["admin", "developer"],
      "host": ["192.168.0.1"]
    }
  }
}
```

##### ServerShutdown

| Class Name     | Event Subclass      | Description                                                       |
| -------------- | ------------------- | ----------------------------------------------------------------- |
| ServerShutdown | ServerShutdownEvent | Represents an event related to the shutdown of the server.        |
| ServerShutdown | ShutdownReason      | Represents an event detailing the reason for the server shutdown. |
| ServerShutdown | ExitCodeEvent       | Represents an event that includes the exit code of the server.    |

A JSON code sample for Server Shutdown Class:

```json
{
  "filter": {
    "class": {
      "name": "server_shutdown",
      "event_subclasses": [
        {
          "subclass": "ServerShutdownEvent",
          "sample_value": {
            "exit_code": "0",
            "reason": "Maintenance"
          }
        }
      ],
      "user": ["admin"],
      "host": ["192.168.0.1"]
    }
  }
}

```

##### ServerStartup

| Class Name    | Event Subclass     | Description                                                             |
| ------------- | ------------------ | ----------------------------------------------------------------------- |
| ServerStartup | ServerStartupEvent | Represents an event related to the startup of the server.               |
| ServerStartup | ConfigurationLoad  | Represents an event indicating the loading of server configurations.    |
| ServerStartup | Initialization     | Represents an event detailing the initialization process of the server. |
| ServerStartup | ServiceStart       | Represents an event indicating that a specific service has started.     |

A JSON code sample for Server Startup class:

```json
{
  "filter": {
    "class": {
      "name": "server_startup",
      "event_subclasses": [
        {
          "subclass": "ServerStartupEvent",
          "sample_value": {
            "startup_time": "2025-07-11T09:00:00Z",
            "configuration_file": {
              "str": "/etc/server/config.yaml",
              "length": 25
            },
            "service_status": "running"
          }
        }
      ],
      "user": ["admin"],
      "host": ["192.168.0.1"]
    }
  }
}

```

##### StoredProgram

| Class Name    | Event Subclass         | Description                                                                                         |
| ------------- | ---------------------- | --------------------------------------------------------------------------------------------------- |
| StoredProgram | StoredProgramEvent     | Represents an event related to the execution of a stored program.                                   |
| StoredProgram | ProgramExecutionStatus | Represents an event detailing the status of a stored program execution.                             |
| StoredProgram | ProgramIDEvent         | Represents an event that includes the ID of the executed SQL command related to the stored program. |
| StoredProgram | ProgramQuery           | Represents an event that includes the actual SQL query string executed within the stored program.   |
| StoredProgram | ProgramDatabase        | Represents an event that includes the database context of the stored program.                       |

A JSON code sample for Stored Program class:

```json
{
  "filter": {
    "class": {
      "name": "stored_program",
      "event_subclasses": [
        {
          "subclass": "StoredProgramEvent",
          "sample_value": {
            "connection_id": "conn12345",
            "sql_command_id": "cmd67890",
            "query": {
              "str": "CALL my_stored_procedure(1)",
              "length": 30
            },
            "database": {
              "str": "my_database",
              "length": 12
            },
            "name": {
              "str": "my_stored_procedure",
              "length": 20
            }
          }
        }
      ],
      "user": ["admin", "developer"],
      "host": ["192.168.0.1"]
    }
  }
}
```

##### TableAccess

| Class Name  | Event Subclass   | Description                                                                   |
| ----------- | ---------------- | ----------------------------------------------------------------------------- |
| TableAccess | TableAccessEvent | Represents an event related to accessing a specific table in the database.    |
| TableAccess | TableQuery       | Represents an event detailing the query executed on a specific table.         |
| TableAccess | TableDatabase    | Represents an event related to the database containing the accessed table.    |
| TableAccess | TableName        | Represents an event detailing the name of the table being accessed.           |
| TableAccess | ConnectionInfo   | Represents an event that includes information about the connection used.      |
| TableAccess | SQLCommandInfo   | Represents an event that includes information about the SQL command executed. |

A JSON code sample for TableAccess class:

```json
{
  "filter": {
    "class": {
      "name": "table_access",
      "event_subclasses": [
        {
          "subclass": "TableAccessEvent",
          "sample_value": {
            "connection_id": "conn12345",
            "sql_command_id": "cmd67890",
            "query": {
              "str": "SELECT * FROM users WHERE id = 1",
              "length": 36
            },
            "table_database": {
              "str": "user_database",
              "length": 15
            },
            "table_name": {
              "str": "users",
              "length": 5
            }
          }
        }
      ],
      "user": ["admin", "developer"],
      "host": ["192.168.0.1"]
    }
  }
}
```

This setup gives you the flexibility to monitor the exact events that are important to you while controlling logging behavior in a detailed way.

### Inclusive filters

Inclusive filters capture specific database events you want to log. They allow you to precisely target and record only the actions you care about.

#### Basic Structure

An inclusive filter uses a JSON configuration that defines which events to include in your audit logging. The filter specifies:

- What type of events to capture

- Which users to track

- What specific actions to log

Common use cases for inclusive filters include security audits, compliance tracking, performance monitoring, and user behavior analysis.

Event tracking can be more precise, which helps reduce unnecessary log noise. By focusing on the specific events that matter, you can enhance security monitoring and ensure that only the most relevant data is logged. This approach not only improves the clarity of your logs but also helps optimize performance by limiting the number of events being recorded, reducing overhead and making it easier to manage the system.

It’s important to consider the performance impact of logging and how it might affect your server. Before deploying your filters in a production environment, test them thoroughly to ensure everything works as expected.

#### Inclusive filter example

This filter is useful for monitoring and auditing changes to the database performed by administrative users, particularly to ensure that updates and deletions are tracked.

```json
{
  "filter": {
    "class": [
      {
        "name": "table_access",
        "user": ["admin"],
        "operation": ["update", "delete"]
      }
    ]
  }
}
```

This filter does one thing: log all update and delete operations performed by admin users. The filter uses the following components:

- "class": The top-level key specifies that the filter applies to the `table_access` class. This class monitors events related to database table interactions.

- "name": "table_access": This defines the event class you want to track. This class captures interactions with database tables such as read, insert, update, and delete operations. Specifies the specific class of events

- user: ["admin"]: This specifies that the filter applies only to events performed by the admin user. It restricts the filter to only log actions executed by this user.

- operation: ["update", "delete"]: This narrows down the filter to track only specific operations. In this case, it captures update and delete operations. Any SELECT (read) or INSERT operations on tables will not be logged, as they are excluded by this filter.

Inclusive filters give you granular control over your MySQL audit logging, allowing you to capture exactly the information you need without overwhelming your logging system.

### Exclusive filters

Exclusive filters in the audit_log_filter for Percona Server for MySQL let you exclude certain activities from being logged, helping you reduce log size and focus on what matters most. For example, you can filter out routine operations like health checks or background processes to avoid unnecessary clutter in your logs.

This example defines a filter that `excludes` (negate: true) all table access events ("table_access") by the user "readonly_user". Events for other users or other classes of activity are still be logged unless additional filters are defined.

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
        "operation": ["update", "delete"],
        "status": [1] // Failed operations only
      },
      {
        "name": "connection",
        "user": ["external_service"],
        "status": [0] // Successful connections
      }
    ]
  }
}
```

This filter captures failed update/delete operations by admin and developer users in the financial database and successful connections for the `external_service` user

## Best practices

Following a systematic approach helps ensure successful deployment and maintenance when implementing audit log filters. Start by creating broad, inclusive filters that capture a wide range of events, giving you a comprehensive view of your database activity. For example, you might begin by logging all actions from administrative users or all operations on critical databases. As you analyze the captured data, you can refine these filters to focus on specific events, users, or operations that matter most to your organization.

Testing is crucial before deploying filters in production. Set up a non-production environment that mirrors your production setup as closely as possible. This non-production environment allows you to verify that your filters capture the intended events without missing critical information. During testing, pay particular attention to how different filter combinations interact and ensure they don't create any unexpected gaps in your audit coverage.

Log file management requires careful attention. Audit logs can grow rapidly, especially with detailed filtering configurations. Monitor your log file sizes regularly and implement appropriate rotation policies. Consider storage capacity, retention requirements, and system performance when determining how much detail to include in your logs. It's often helpful to calculate expected log growth based on your typical database activity and adjust your rotation policies accordingly.

Performance impact is a critical consideration when implementing detailed logging. More granular filters typically require more system resources to process and store the audit data. Monitor your system's performance metrics while testing different filter configurations. Look for significant changes in query response times, CPU usage, or I/O operations. If you notice performance degradation, consider adjusting your filters to balance capturing necessary audit data and maintaining acceptable system performance. Remember that starting with less detailed logging is often better and gradually increasing it as needed rather than implementing overly aggressive logging that impacts system performance.

## Implement the filter

Here's how to define and implement an audit log filter:

### Add filter identifier

An audit log filter identifier is your filter's unique name within the `audit_log_filter` system. You create this name to label and track your specific filter setup. The `audit_log_filter_id` system variable stores this name, and you should choose descriptive identifiers like 'finance_audit' or 'security_tracking'.

After you name your filter with an identifier, you attach your rules. The identifier makes it easy to manage multiple filter setups and update them as needed. When you want to change your logging rules, you first reference your chosen identifier and then add your new filter settings.

Remember that when you apply new filter settings to an existing identifier, the system replaces the old settings. It doesn't add the new rules to what's already there.

```sql
SET GLOBAL audit_log_filter_id = 'financial_tracking';
```

### Add filter definition

```sql
SET GLOBAL audit_log_filter = '{
  "filter": {
    "class": [
      {
        "name": "table_access",
        "user": ["admin", "finance_team"],
        "database": ["financial_db"],
        "table": ["accounts", "transactions"],
        "operation": ["insert", "update", "delete"],
        "status": [0, 1]
      },
      {
        "name": "connection",
        "user": ["admin", "finance_team"],
        "operation": ["connect", "disconnect"],
        "status": [0, 1]
      }
    ]
  }
}';
```

The filter monitors two main types of activities. First, it watches all changes to your accounts and transactions tables. This monitoring means that the filter logs when someone adds new data, changes existing information, or removes records. You get a complete picture of who's touching your financial data and what they do with it.

The filter doesn't just track successful operations—it monitors both successes and failures. This tracking gives you valuable information about attempted changes that didn't work out, which is helpful for troubleshooting and security monitoring.

Here's what gets logged:

- Every insert, update, and delete operation on your financial tables

- All connection attempts from your admin and finance teams, including when they log in and out

- Whether each operation succeeded (status 0) or failed (status 1)

The filter focuses only on activity in your `financial_db` database. This targeted approach makes it easier to find the information you need when you need it.

Tracking all these elements gives you a comprehensive view of who's accessing your financial data, what changes they're making, and whether those changes are successful. This ability is beneficial for security monitoring and compliance requirements.

To verify your filter:

```sql
SHOW GLOBAL VARIABLES LIKE 'audit_log_filter';
```

To check if events are being logged, you can examine your audit log file (default location is the data directory).
