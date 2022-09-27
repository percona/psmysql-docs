# Per-session server-id

Variable server_id is a global variable. In multi-source replication setups or for external replication, server_id can be useful as a session variable. In that case a session replaying a binary log from another server would set it to that server’s id. That way binary log has the ultimate source server id attached to it no matter how many hosts it passes, and it would provide loop detection for multi-source replication.

This was implemented by introducing the new pseudo_server_id variable. This variable, when set to non-zero value, will cause all binary log events in that session to have that server_id value. A new variable was introduced instead of converting server_id to have both global and session scope in order to preserve compatibility.

You should use this option at your own risk because it is very easy to break replication when using pseudo_server_id. One special case is circular replication which definitely will be broken if you set pseudo_server_id to a value not assigned to any participating server (ie., setup is `1->2->3->4->1`, and pseudo_server_id is set to `5`). It is also possible to create a temporary table `foo`, then change pseudo_server_id and from now `foo` will not be visible by this session until pseudo_server_id gets restored.

## Version Specific Information

* Percona Server for MySQL 5.7.10-1: Feature ported from *Percona Server for MySQL* 5.6

## System Variables

### `pseudo_server_id`

| Option       | Description |
|--------------|-------------|
| Command-line | Yes         |
| Config file  | No          |
| Scope        | Session     |
| Dynamic      | Yes         |
| Default      | 0           |

When this variable is set to `0` (default), it will use the global server_id value. **Note:** this is different from the setting the global server_id to `0` which disables replication. Setting this variable to non-zero value will cause binary log events in that session to have it as server_id value. Setting this variable requires `SUPER` privileges.

## Other Reading

* [MDEV-500](https://mariadb.atlassian.net/browse/MDEV-500) -  Session variable for server_id

* Upstream bug [#35125](http://bugs.mysql.com/bug.php?id=35125) -  allow the ability to set the server_id for a connection for logging to binary log
