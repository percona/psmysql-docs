MySQL 9.x removes `mysql_native_password` and changes default password authentication.

| Topic | Behavior |
|-------|----------|
| `mysql_native_password` | Removed. The server has no `--mysql-native-password=ON`, `mysql_native_password=ON`, or other way to load the plugin. |
| `default_authentication_plugin` | Unavailable. Password-based accounts use `caching_sha2_password` by default. |
| Client compatibility | Applications and drivers must support `caching_sha2_password`. |
| TLS | Optional unless a security policy or deployment mandates encrypted traffic. `caching_sha2_password` works without TLS for some connection types. |
