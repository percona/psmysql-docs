# Load the Clone plugin
    
You cannot use the `--plugin-load-add` option to load the clone plugin during an upgrade from a previous MySQL version. Attempting to do so will raise an error. Upgrade the server first, then start it with `plugin-load-add=mysql_clone.so`.

## Load the plugin

Locate the Plugin Library File: Ensure the plugin library file (`mysql_clone.so`) is in the MySQL plugin directory (`plugin_dir` system variable). Set `plugin_dir` at server startup if necessary.

=== "At server startup"

    Load the Plugin at Server Startup: Use the `--plugin-load-add` option to name the library file. Add the following lines to your `my.cnf` file:
    
      ```ini
      [mysqld]
      plugin-load-add=mysql_clone.so
      ```
      Restart the server to apply the new settings.
      
  
=== "At runtime"

    Load the Plugin at Runtime: Alternatively, you can load the plugin at runtime with the following SQL statement:
    
      ```sql
      INSTALL PLUGIN clone SONAME 'mysql_clone.so';
      ```
      
      This command loads the plugin and registers it in the `mysql.plugins` table, ensuring it loads automatically at subsequent server startups without `--plugin-load-add`.

## Verify Plugin installation

Check the `INFORMATION_SCHEMA.PLUGINS` table or use the `SHOW PLUGINS` statement to verify the plugin installation:

```sql
SELECT PLUGIN_NAME, PLUGIN_STATUS
FROM INFORMATION_SCHEMA.PLUGINS
WHERE PLUGIN_NAME = 'clone';
```
If the plugin fails to initialize, check the server error log for diagnostic messages.

## Control plugin activation state

If the plugin is registered with `INSTALL PLUGIN` or loaded with `--plugin-load-add`, use the `--clone` option at server startup to control its activation state. To load the plugin at startup and prevent it from being removed at runtime, add these options:

```ini
[mysqld]
plugin-load-add=mysql_clone.so
clone=FORCE_PLUS_PERMANENT
```
   
To prevent the server from running without the clone plugin, use `--clone` with `FORCE` or `FORCE_PLUS_PERMANENT`. These options ensure the server startup fails if the plugin does not initialize successfully.
