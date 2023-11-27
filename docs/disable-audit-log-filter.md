# Disable Audit Log Filter logging

The `audit_log_filter.disable` system variable lets you disable or enable logging for all connections.

You can set the variable in the following ways:

* Option file
* Command-line startup string
* SET statement during runtime


```{.bash data-prompt="mysql>"}
mysql> SET GLOBAL audit_log_filter.disable = true;
```

Setting `audit_log_filter.disable` has the following effect:

| Value | Actions |
|---|---|
| true | Generates a warning. Audit log function calls and changes in variables generate session warnings. Disables the component. |
| false | Re-enables the component and generates a warning. This is the default value. |

## Privileges required

Setting the value of `audit_log_filter.disable` at runtime requires the following:

* `AUDIT_ADMIN` privilege
* `SYSTEM_VARIABLES_ADMIN` privilege