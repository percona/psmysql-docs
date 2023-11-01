# Uninstall Audit Log Filter

The feature is in [tech preview](glossary.md#tech-preview).

To remove the plugin, run the following:

```{.bash data-prompt="mysql>"}
mysql> DROP TABLE IF EXISTS mysql.audit_log_user;
mysql> DROP TABLE IF EXISTS mysql.audit_log_filter;
mysql> UNINSTALL PLUGIN audit_log_filter;
```
