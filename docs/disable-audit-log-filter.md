# Disable Audit Log Filter logging

The `audit_log_filter.disable` system variable lets you disable or enable logging for all connections based on the value:

| Value | Actions |
|---|---|
| `audit_log_filter.disable = true` |Disables logging. |
| `audit_log_filter.disable = false` | Enables logging. |

You can set the variable in the following ways:

* Specify in the option file.

* Include in the command-line startup string.

* Use a SET statement during runtime.

```{.bash data-prompt="mysql>"}
mysql> SET GLOBAL audit_log_filter.disable = true;
```

## Privileges required

Setting the value of `audit_log_filter.disable` at runtime requires the following:

* `AUDIT_ADMIN` privilege
* `SYSTEM_VARIABLES_ADMIN` privilege