# Audit log filter reference

This reference guide provides comprehensive tables and technical details for MySQL audit log filter definitions. Use this reference guide as a quick lookup for field names, event types, functions, and system variables.

## Event class and subclass combinations

The following table shows which event subclasses are valid for each event class in audit log filters:

| Event Class | Event Subclass | Description |
|-------------|----------------|-------------|
| connection | connect | Client connection established |
| connection | disconnect | Client connection terminated |
| connection | change_user | User changed during session |
| general | status | General status events (queries, commands) |
| table_access | read | Table read operations (SELECT) |
| table_access | insert | Table insert operations (INSERT) |
| table_access | update | Table update operations (UPDATE) |
| table_access | delete | Table delete operations (DELETE) |

### Usage examples

Log all connection events:
```json
{
  "filter": {
    "class": {
      "name": "connection",
      "event": [
        { "name": "connect" },
        { "name": "disconnect" }
      ]
    }
  }
}
```

Log only data modification operations:
```json
{
  "filter": {
    "class": {
      "name": "table_access",
      "event": [
        { "name": "insert" },
        { "name": "update" },
        { "name": "delete" }
      ]
    }
  }
}
```

## Available field names by event type

### Connection event fields

| Field Name | Data Type | Description | Example Value |
|-------------|-----------|-------------|---------------|
| `status` | integer | Event status (0 for OK, non-zero for failure) | `0` |
| `connection_id` | integer | Unique connection identifier | `12345` |
| `user.str` | string | Username for the connection | `"admin"` |
| `host.str` | string | Client hostname | `"localhost"` |
| `ip.str` | string | Client IP address | `"192.168.1.100"` |
| `database.str` | string | Database name specified at connect | `"myapp"` |
| `connection_type` | integer | Connection type (1=TCP/IP, 4=SSL) | `1` |

### General event fields

| Field Name | Data Type | Description | Example Value |
|-------------|-----------|-------------|---------------|
| `general_error_code` | integer | Event status (0 for OK, non-zero for failure) | `0` |
| `general_thread_id` | integer | Connection/thread ID | `12345` |
| `general_command.str` | string | Command name (Query, Execute) | `"Query"` |
| `general_query.str` | string | SQL statement text | `"SELECT * FROM users"` |
| `general_host.str` | string | Host executing query | `"localhost"` |
| `general_sql_command.str` | string | SQL command type | `"select"` |

**Note:** User filtering (`user.str`) is not available for `general` class events. The user information appears in the top-level `account` object in the audit log output, but it is not accessible as a filterable field for `general` events. User filtering is also not available for `table_access` events. To filter by user, use `connection` events instead.

### Table access event fields

| Field Name | Data Type | Description | Example Value |
|-------------|-----------|-------------|---------------|
| `connection_id` | integer | Event connection ID | `12345` |
| `sql_command_id` | integer | SQL command ID | `1` |
| `query.str` | string | SQL statement text | `"INSERT INTO users VALUES (...)"` |
| `table_database.str` | string | Database containing table | `"myapp"` |
| `table_name.str` | string | Name of accessed table | `"users"` |

### Field usage examples

Filter by specific table:
```json
{
  "filter": {
    "class": {
      "name": "table_access",
      "event": [
        {
          "name": "insert",
          "log": {
            "field": {
              "name": "table_name.str",
              "value": "sensitive_data"
            }
          }
        }
      ]
    }
  }
}
```

Filter by database:
```json
{
  "filter": {
    "class": {
      "name": "table_access",
      "event": {
        "name": ["insert", "update", "delete", "read"],
        "log": {
          "field": {
            "name": "table_database.str",
            "value": "production"
          }
        }
      }
    }
  }
}
```

## Predefined functions reference

### Query digest function

The `query_digest` function provides statement digest functionality for audit log filters.

| Function | Arguments | Return Type | Description |
|----------|-----------|-------------|-------------|
| `query_digest` | none | string | Returns digest of current statement |
| `query_digest` | `"digest"` | boolean | Compares current statement digest with provided digest |

Usage Examples:

Replace statement text with digest:
```json
{
  "filter": {
    "class": {
      "name": "general",
      "event": [
        {
          "name": "status",
          "print": {
            "field": {
              "name": "general_query.str",
              "print": false,
              "replace": {
                "function": {
                  "name": "query_digest"
                }
              }
            }
          }
        }
      ]
    }
  }
}
```

## System variables reference

### Audit log filter configuration variables

| Variable_name                                         | Value            |
|-------------------------------------------------------|------------------|
| audit_log_filter_buffer_size                          | 1048576          |
| audit_log_filter_compression                          | NONE             |
| audit_log_filter_database                             | mysql            |
| audit_log_filter_disable                              | OFF              |
| audit_log_filter_encryption                           | NONE             |
| audit_log_filter_file                                 | audit_filter.log |
| audit_log_filter_filter_id                            | 1                |
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

### Log file management examples

Configure 1GB file rotation:
```sql
SET GLOBAL audit_log_filter_rotate_on_size = 1073741824;
```

Set 2GB total log size limit:
```sql
SET GLOBAL audit_log_filter_max_size = 2147483648;
```

Remove logs older than 7 days:
```sql
SET GLOBAL audit_log_filter_prune_seconds = 604800;
```

## Logical operators reference

### Supported logical operators

| Operator | Syntax | Description | Example |
|----------|--------|-------------|---------|
| `and` | `{"and": [condition1, condition2]}` | All conditions must be true | `{"and": [{"field": {"name": "user.str", "value": "admin"}}, {"field": {"name": "table_name.str", "value": "users"}}]}` |
| `or` | `{"or": [condition1, condition2]}` | Any condition can be true | `{"or": [{"field": {"name": "table_name.str", "value": "users"}}, {"field": {"name": "table_name.str", "value": "accounts"}}]}` |
| `not` | `{"not": condition}` | Inverts the condition result | `{"not": {"field": {"name": "general_sql_command.str", "value": "select"}}}` |

### Complex logical examples

Log admin operations on sensitive tables:
```json
{
  "filter": {
    "class": {
      "name": "table_access",
      "event": {
        "name": "update",
        "log": {
          "or": [
            {
              "field": {
                "name": "table_name.str",
                "value": "users"
              }
            },
            {
              "field": {
                "name": "table_name.str",
                "value": "payments"
              }
            }
          ]
        }
      }
    }
  }
}
```

**Note:** User filtering (`user.str`) is not available for `table_access` events. To restrict this filter to specific users (e.g., "admin"), assign the filter only to those users using `audit_log_filter_set_user('admin@localhost', 'filter_name')` instead of filtering by user within the filter definition.

## Field value testing patterns

### Common field value tests

| Pattern | Use Case | Example |
|---------|----------|---------|
| Exact match | Filter by specific values | `{"field": {"name": "user.str", "value": "admin"}}` |
| Multiple values | Filter by any of several values | `{"or": [{"field": {"name": "table_name.str", "value": "users"}}, {"field": {"name": "table_name.str", "value": "accounts"}}]}` |
| Exclude values | Filter out specific values | `{"not": {"field": {"name": "general_sql_command.str", "value": "select"}}}` |
| Function-based | Use predefined functions | `{"function": {"name": "query_digest", "args": "SELECT ?"}}` |

### Field value examples

Log all operations except SELECT statements:
```json
{
  "filter": {
    "class": {
      "name": "general",
      "event": [
        {
          "name": "status",
          "log": {
            "not": {
              "field": {
                "name": "general_sql_command.str",
                "value": "select"
              }
            }
          }
        }
      ]
    }
  }
}
```

Log operations on multiple sensitive tables:
```json
{
  "filter": {
    "class": {
      "name": "table_access",
      "event": {
        "name": ["insert", "update", "delete", "read"],
        "log": {
          "or": [
            {
              "field": {
                "name": "table_name.str",
                "value": "financial_data"
              }
            },
            {
              "field": {
                "name": "table_name.str",
                "value": "user_credentials"
              }
            },
            {
              "field": {
                "name": "table_name.str",
                "value": "payment_info"
              }
            }
          ]
        }
      }
    }
  }
}
```

## Dynamic filter reference

### Filter replacement patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| `"id": "filter_name"` | Assigns unique identifier to filter | Referencing filters in dynamic replacements |
| `"ref": "filter_name"` | References another filter by ID | Returning to original filter after temporary replacement |
| `"activate": condition` | Condition for filter activation | Triggering filter changes based on events |

### Dynamic filter example

Temporary enhanced logging for specific operations:
```json
{
  "filter": {
    "id": "monitor_sensitive",
    "class": {
      "name": "table_access",
      "event": {
        "name": ["insert", "update", "delete"],
        "log": false,
        "filter": {
          "class": {
            "name": "general",
            "event": {
              "name": "status",
              "log": true,
              "filter": {
                "ref": "monitor_sensitive"
              }
            }
          },
          "activate": {
            "field": {
              "name": "table_name.str",
              "value": "sensitive_data"
            }
          }
        }
      }
    }
  }
}
```

## Print and replace operations

### Print control options

| Option | Description | Use Case |
|--------|-------------|----------|
| `"print": true` | Include field in audit log | Default behavior for most fields |
| `"print": false` | Exclude field from audit log | Hide sensitive information |
| `"replace": value` | Replace field value | Mask or transform sensitive data |

### Field replacement examples

Replace SQL statements with digests:
```json
{
  "filter": {
    "class": {
      "name": "general",
      "event": [
        {
          "name": "status",
          "print": {
              "field": {
                "name": "general_query.str",
                "print": true,
                "replace": {
                "function": {
                  "name": "query_digest"
                }
              }
            }
          }
        }
      ]
    }
  }
}
```

Conditional field replacement:
```json
{
  "filter": {
    "class": {
      "name": "general",
      "event": {
        "name": "status",
        "print": {
          "field": {
            "name": "general_query.str",
            "print": {
              "not": {
                "function": {
                  "name": "query_digest",
                  "args": "SELECT ?"
                }
              }
            },
            "replace": {
              "function": {
                "name": "query_digest"
              }
            }
          }
        }
      }
    }
  }
}
```

## Troubleshooting reference

### Common field name issues

| Problem | Solution | Example |
|---------|----------|---------|
| Field not found | Check field name spelling and event type | Use `table_name.str` for table_access events, not `table_name` |
| Wrong data type | Verify field data type in reference | `connection_id` is integer, not string |
| Case sensitivity | Field names are case-sensitive | Use `general_query.str`, not `General_Query.str` |

### Validation commands

Check filter syntax:
```sql
SELECT audit_log_filter_set_filter('test_filter', '{"filter":{"class":{"name":"connection"}}}');
```

Verify filter assignment:
```sql
SELECT * FROM mysql.audit_log_filter WHERE name = 'your_filter';
SELECT * FROM mysql.audit_log_user WHERE filter_name = 'your_filter';
```

Test filter activation:

1. Connect as test user and run operations

2. Check audit log file for expected entries

3. Verify filter behavior matches expectations

## Related topics

* [Audit Log Filter Overview](audit-log-filter-overview.md) - Introduction to audit log filtering concepts

* [Write Audit Log Filter Definitions](write-audit-log-filter-definitions.md) - Quick start guide for basic filter creation

* [Advanced Audit Log Filter Definitions](audit-log-filter-advanced.md) - Advanced features and complex configurations
