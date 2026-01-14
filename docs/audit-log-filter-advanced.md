# Advanced audit log filter definitions

This guide covers advanced features for MySQL audit log filters, including conditional logging, event blocking, field replacement, and dynamic filter management.

## Inclusive and exclusive logging

### Basic logging control

Use the `log` field to control whether events are recorded. The first example enables logging of all events. The second example disables all logging:

```json
{
  "filter": {
    "log": true
  }
}
```

```json
{
  "filter": {
    "log": false
  }
}
```

### Selective class logging

Log only specific event classes:

```json
{
  "filter": {
    "class": [
      { "name": "connection" },
      { "name": "table_access" }
    ]
  }
}
```

### Mixed logging control

Combine global and class-specific logging controls:

```json
{
  "filter": {
    "log": false,
    "class": [
      { "name": "connection", "log": true },
      { "name": "table_access", "log": false }
    ]
  }
}
```

## Testing event field values

### Field value matching

Test specific field values within events:

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

### Multiple field conditions

Test multiple field conditions using logical operators:

```json
{
  "filter": {
    "class": {
      "name": "general",
      "event": [
        {
          "name": "status",
          "log": {
            "and": [
              {
                "field": {
                  "name": "general_sql_command.str",
                  "value": "create_user"
                }
              },
              {
                "field": {
                  "name": "general_host.str",
                  "value": "localhost"
                }
              }
            ]
          }
        }
      ]
    }
  }
}
```

**Note:** User filtering is not available for `general` class events because the user information is in the top-level `account` object, not in the `general_data` structure that filter fields reference. User filtering (`user.str`) is also not available for `table_access` events. To filter by user, use `connection` events instead.

## Blocking execution of specific events

### Event blocking with abort

Prevent execution of specific events:

```json
{
  "filter": {
    "class": {
      "name": "table_access",
      "event": [
        {
          "name": "delete",
          "abort": true
        }
      ]
    }
  }
}
```

### Conditional blocking

Block events based on field conditions:

```json
{
  "filter": {
    "class": {
      "name": "table_access",
      "event": [
        {
          "name": "update",
          "abort": {
            "field": {
              "name": "table_name.str",
              "value": "critical_table"
            }
          }
        }
      ]
    }
  }
}
```

## Logical operators

### AND operations

Require multiple conditions to be true:

```json
{
  "filter": {
    "class": {
      "name": "general",
      "event": [
        {
          "name": "status",
          "log": {
            "and": [
              {
                "field": {
                  "name": "general_sql_command.str",
                  "value": "alter_user"
                }
              },
              {
                "field": {
                  "name": "general_command.str",
                  "value": "Query"
                }
              }
            ]
          }
        }
      ]
    }
  }
}
```

### OR operations

Log if any condition is true:

```json
{
  "filter": {
    "class": {
      "name": "table_access",
      "event": [
        {
          "name": "insert",
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
      ]
    }
  }
}
```

### NOT operations

Invert condition results:

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

### Complex logical combinations

Combine multiple logical operators:

```json
{
  "filter": {
    "class": {
      "name": "table_access",
      "event": [
        {
          "name": "update",
          "log": {
            "and": [
              {
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
                      "value": "accounts"
                    }
                  }
                ]
              },
              {
                "not": {
                  "field": {
                    "name": "table_database.str",
                    "value": "system"
                  }
                }
              }
            ]
          }
        }
      ]
    }
  }
}
```

## Predefined functions

Apply functions to field values for pattern matching and filtering. This example uses the `string_find` function to log only `general|status` events where `general_sql_command.str` starts with `show_`, capturing all SHOW statements (such as `SHOW TABLES`, `SHOW DATABASES`, `SHOW VARIABLES`, etc.):

```json
{
  "filter": {
    "class": {
      "name": "general",
      "event": [
        {
          "name": "status",
          "log": {
            "function": {
              "name": "string_find",
              "args": [
                "general_sql_command.str",
                "show_"
              ]
            }
          }
        }
      ]
    }
  }
}
```

## Event field value replacement

### Basic field replacement

Replace sensitive field values in audit logs. This example replaces SQL statement text in `general|status` events with query digests using the `query_digest` function, hiding the actual query content:

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

### Conditional replacement

Replace values only under specific conditions. This example replaces SQL statement text with query digests, but only for statements that do NOT match the digest `SELECT ?`. Simple SELECT queries matching this digest keep their original text, while all other statements are replaced with their digest:

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

### Multiple field replacement

Replace query text with digests across multiple event classes. This example replaces SQL statement text in both `general` and `table_access` events with their query digests, ensuring that all query text in the audit log is replaced with digests regardless of event class. The `general` class uses `general_query.str` while `table_access` uses `query.str`:

```json
{
  "filter": {
    "class": [
      {
        "name": "general",
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
      },
      {
        "name": "table_access",
        "print": {
          "field": {
            "name": "query.str",
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
```

## Dynamic filter replacement

### Basic filter replacement

Create filters that can change dynamically. This example monitors `table_access` events for `update` or `delete` operations on `temp_1` or `temp_2` tables. When these conditions are met, the filter switches to logging only the corresponding `general|status` event, then returns to the main filter:

```json
{
  "filter": {
    "id": "main",
    "class": {
      "name": "table_access",
      "event": [
        {
          "name": "update",
          "log": false,
          "filter": {
            "class": {
              "name": "general",
              "event": [
                {
                  "name": "status",
                  "filter": {
                    "ref": "main"
                  }
                }
              ]
            },
            "activate": {
              "or": [
                {
                  "field": {
                    "name": "table_name.str",
                    "value": "temp_1"
                  }
                },
                {
                  "field": {
                    "name": "table_name.str",
                    "value": "temp_2"
                  }
                }
              ]
            }
          }
        },
        {
          "name": "delete",
          "log": false,
          "filter": {
            "class": {
              "name": "general",
              "event": [
                {
                  "name": "status",
                  "filter": {
                    "ref": "main"
                  }
                }
              ]
            },
            "activate": {
              "or": [
                {
                  "field": {
                    "name": "table_name.str",
                    "value": "temp_1"
                  }
                },
                {
                  "field": {
                    "name": "table_name.str",
                    "value": "temp_2"
                  }
                }
              ]
            }
          }
        }
      ]
    }
  }
}
```

### Conditional filter activation

Activate different filters based on conditions. This example monitors `table_access|insert` events and only activates enhanced logging (logging the `general|status` event) when inserts occur on the `financial_data` table:

```json
{
  "filter": {
    "class": {
      "name": "table_access",
      "event": [
        {
          "name": "insert",
          "filter": {
            "class": {
              "name": "general",
              "event": [
                {
                  "name": "status",
                  "log": true
                }
              ]
            },
            "activate": {
              "field": {
                "name": "table_name.str",
                "value": "financial_data"
              }
            }
          }
        }
      ]
    }
  }
}
```

## Advanced filtering patterns

### Account management monitoring

Monitor specific account management operations. This filter logs `alter_user`, `create_user`, and `drop_user` commands while replacing the SQL statement text with query digests to hide credential and data values:

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
          },
          "log": {
            "or": [
              {
                "field": {
                  "name": "general_sql_command.str",
                  "value": "alter_user"
                }
              },
              {
                "field": {
                  "name": "general_sql_command.str",
                  "value": "create_user"
                }
              },
              {
                "field": {
                  "name": "general_sql_command.str",
                  "value": "drop_user"
                }
              }
            ]
          }
        }
      ]
    }
  }
}
```

### Data modification tracking

Track only data modification operations, excluding the audit log table itself. This filter logs all `insert`, `update`, and `delete` operations on `table_access` events, except those targeting the `audit_log` table to prevent recursive logging:

```json
{
  "filter": {
    "class": {
      "name": "table_access",
      "event": [
        {
          "name": "insert",
          "log": {
            "not": {
              "field": {
                "name": "table_name.str",
                "value": "audit_log"
              }
            }
          }
        },
        {
          "name": "update",
          "log": {
            "not": {
              "field": {
                "name": "table_name.str",
                "value": "audit_log"
              }
            }
          }
        },
        {
          "name": "delete",
          "log": {
            "not": {
              "field": {
                "name": "table_name.str",
                "value": "audit_log"
              }
            }
          }
        }
      ]
    }
  }
}
```


## Best practices

### Performance considerations

* Use specific field conditions to reduce processing overhead

* Avoid overly complex logical combinations

* Test filter performance with production workloads

### Security guidelines

* Replace sensitive data in audit logs using field replacement

* Block dangerous operations when appropriate

* Use dynamic filters for temporary security measures

### Maintenance tips

* Document complex filter logic

* Test filters in non-production environments

* Monitor filter performance impact

* Use filter references for maintainable configurations

## Troubleshooting advanced filters

### Common issues

1. Filter not activating: Check `activate` conditions

2. Unexpected blocking: Verify `abort` field conditions  

3. Performance problems: Simplify logical operators

4. Replacement not working: Check field names and function syntax

### Debugging steps

1. Test filter conditions individually

2. Use simple filters first, then add complexity

3. Check MySQL error logs for filter syntax errors

4. Verify field names match actual event structure

### Testing advanced filters

```sql
-- Test filter activation
SELECT * FROM mysql.audit_log_filter WHERE name = 'your_filter';

-- Check filter assignments
SELECT * FROM mysql.audit_log_user;

-- Monitor audit log output
SELECT * FROM information_schema.plugins WHERE plugin_name = 'audit_log';
```

## Authentication stage considerations

### Pre-authenticate stage behavior

During the pre-authenticate stage, no authenticated user is associated with the event. This behavior affects filter application:

* User-specific filters cannot be applied during pre-authentication

* Default rule for `%` is selected instead of user-specific rules

* This behavior applies to both connection and general events

### Example scenario

If you have a filter assigned to `excludeUserTest@` but the event occurs before authentication, the system will use the default rule for `%` instead of the `excludeUserTest@` rule, because no authenticated user exists yet. This example shows a connection filter that would be used as the default:

```json
{
  "filter": {
    "class": {
      "name": "connection",
      "log": false
    }
  }
}
```

### Best practices

1. Design default filters to handle pre-authentication events appropriately

   * Create a default filter assigned to `%`@`%` that logs connection events

   * Use global logging controls for events that occur before user authentication

   * Example: `{"filter":{"class":[{"name":"connection","log":true}]}}`

2. Use global logging controls for events that occur before user authentication

   * Set `log: true` at the filter level for connection events

   * Avoid user-specific conditions in default filters

   * Test with anonymous connections to verify behavior

3. Test filter behavior during connection establishment phases

   * Connect without authentication to test default filter behavior

   * Verify that connection events are logged according to default rules

   * Check that user-specific filters don't interfere with pre-authentication

4. Consider authentication timing when designing user-specific filters

   * Remember that user-specific filters only apply after successful authentication

   * Design filters that work for both authenticated and pre-authenticated scenarios

   * Use the Reference guide for complete field names and event types

## Related topics

* [Audit Log Filter Overview](audit-log-filter-overview.md) - Introduction to audit log filtering concepts

* [Write Audit Log Filter Definitions](write-audit-log-filter-definitions.md) - Quick start guide for basic filter creation

* [Audit Log Filter Reference](audit-log-filter-reference.md) - Complete reference tables and technical details
