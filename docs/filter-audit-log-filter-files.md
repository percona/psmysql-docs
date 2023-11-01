# Filter the Audit Log Filter logs

The feature is in [tech preview](glossary.md#tech-preview).

The audit filter log filtering is based on rules. The filter rule definition has the ability to include or exclude events based on the following attributes:

* User account
* Audit event class
* Audit event subclass
* Audit event fields (for example, `COMMAND_CLASS` or `STATUS`)

You can define multiple filters and assign any filter to multiple accounts. You can also create a default filter for specific user accounts. The filters are defined using function calls. After the filter is defined, the filter is stored in `mysql` system tables. 

## Audit Log Filter functions

The Audit Log filter functions require `AUDIT_ADMIN` or `SUPER` privilege. 

The following functions are used for rule-based filtering:

| Function | Description | Example |
|---|---|---|
| audit_log_filter_flush() | Manually flush the filter tables | `SELECT audit_log_filter_flush()`
| audit_log_filter_set_filter() | Defines a filter | `SELECT audit_log_filter_set_filter('log_connections','{ "filter":{}}'`')
| audit_log_filter_remove_filter() | Removes a filter |
| audit_log_filter_set_user() | Assigns a filter to a specific user account |
| audit_log_filter_remove_user() | Removes the filters from a specific user account |

Using a SQL interface, you can define, display, or modify audit log filters. The filters are stored in the `mysql` system database. 

A read-only variable, `audit_log_filter_id`, signals if a filter is assigned to a specific session.

Filter definitions are `JSON` values.

The function, `audit_log_filter_flush()`, forces reloading all filters and should only be invoked when modifying the audit tables. This function affects all users. Users in current sessions must either execute change-user or disconnect and reconnect.

## Constraints

The `audit_log_filter` plugin must be enabled and the audit tables must exist to use the audit log filter functions. The user account must have the required privileges. 

## Using the audit log filter functions

With a new connection, the audit log filter plugin finds the user account name in the filter assignments. If a filter has been assigned, the plugin uses that filter. If no filter has been assigned, but there is a default account filter, the plugin uses that filter. If there is no filter assigned, and there is no default account filter, then the plugin does not process any event.

The default account is represented by `%` as the account name.

You can assign filters to a specific user account or disassociate a user account from a filter. To disassociate a user account, either unassign a filter or assign a different filter. If you remove a filter, that filter is unassigned from all users, including current users in current sessions.





