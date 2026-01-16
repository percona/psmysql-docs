# Manage the Audit Log Filter files

The Audit Log Filter files have the following potential results:

* Consume a large amount of disk space
* Grow large

You can manage the space by using log file rotation. This operation renames and then rotates the current log file and then uses the original name on a new current log file. You can rotate the file either manually or automatically.

If automatic rotation is enabled, you can prune the log file. This pruning operation can be based on either the log file age or combined log file size.

## Manual log rotation

The default setting for [`audit_log_filter.rotate_on_size`](audit-log-filter-variables.md#audit_log_filterrotate_on_size) is 1GB. If this option is set to `0`, the audit log filter component does not do an automatic rotation of the log file. You must do the rotation manually with this setting.

The `SELECT audit_log_rotate()` command renames the file and creates a new audit log filter file with the original name. You must have the `AUDIT_ADMIN` privilege. 

The files are pruned if either `audit_log_filter.max_size` or `audit_log_filter.prune_seconds` have a value greater than 0 (zero) and `audit_log_filter.rotate_on_size` > 0.

After the files have been renamed, you must manually remove any archived audit log filter files. The renamed audit log filter files can be read by `audit_log_read()`. The `audit_log_read()` does not find the logs if the name pattern differs from the current pattern.

## Changing log format

When you change the `audit_log_filter.format` system variable, the component handles the transition automatically.

### Format change behavior

**What happens:**
1. Current log file is rotated (renamed with timestamp)
2. New log file is created with the new format
3. Old format files remain accessible but are not appended to

**Example:**
```sql
-- Current format: NEW (XML)
-- Current file: audit_filter.log

-- Change to JSON format
SET GLOBAL audit_log_filter.format = 'JSON';
-- Requires server restart to take effect

-- After restart:
-- Old file: audit_filter.log.20240101120000 (XML format)
-- New file: audit_filter.log (JSON format)
```

### Backward compatibility

**Reading old format files:**
* `audit_log_read()` function only works with JSON format
* XML format files (OLD or NEW) must be read manually or with external tools
* Old format files remain readable after format change

**Recommendation:**
Change the log filename when changing format to avoid confusion:

```sql
-- Before changing format, update filename
SET GLOBAL audit_log_filter.file = 'audit_filter.json';
-- Then change format
SET GLOBAL audit_log_filter.format = 'JSON';
-- Restart server
```

This ensures:
* Clear distinction between format types
* Easier log file management
* Better organization of historical logs

### Format change procedure

1. **Plan the change:**
   * Decide on new format (OLD, NEW, or JSON)
   * Choose new filename if changing format type
   * Schedule during maintenance window (requires restart)

2. **Update configuration:**
   ```sql
   -- Optionally change filename first
   SET GLOBAL audit_log_filter.file = 'audit_filter.json';
   -- Change format
   SET GLOBAL audit_log_filter.format = 'JSON';
   ```

3. **Restart server:**
   * Format change requires server restart
   * Old file is automatically rotated
   * New file is created with new format

4. **Verify:**
   * Check that new log file exists
   * Verify format is correct
   * Test reading logs (if using JSON format)

## Rotation scenarios and examples

### Manual rotation

**When to use:**
* `audit_log_filter.rotate_on_size` is set to 0
* You need to rotate logs on demand
* Before maintenance operations
* When changing log format

**Example:**
```sql
-- Rotate log file manually
SELECT audit_log_rotate();
```

**Result:**
* Current file is renamed (e.g., `audit_filter.log.20240101120000`)
* New file is created with original name (`audit_filter.log`)
* Old file can be read by `audit_log_read()` if format is JSON

### Automatic rotation

**Configuration:**
```sql
-- Enable automatic rotation at 1GB
SET GLOBAL audit_log_filter.rotate_on_size = 1073741824;
```

**Behavior:**
* When log file reaches specified size, it's automatically rotated
* New file is created immediately
* Rotation happens transparently during normal operation

**Example scenario:**
```
audit_filter.log (1GB) → audit_filter.log.20240101120000
New audit_filter.log created (0 bytes)
```

### Rotation with compression

**Configuration:**
```sql
-- Enable compression
SET GLOBAL audit_log_filter.compression = 'GZIP';
-- Requires server restart
```

**Behavior:**
* Rotated files are compressed automatically
* File extension may change (e.g., `.log.gz`)
* Compression happens after rotation
* Reading compressed files requires decompression

### Rotation with encryption

**Configuration:**
```sql
-- Enable encryption
SET GLOBAL audit_log_filter.encryption = 'AES';
-- Requires server restart and password setup
```

**Behavior:**
* Rotated files remain encrypted
* Need encryption password to read old files
* Each rotated file uses same encryption key
* Password rotation affects new files, not old ones

### Reading rotated files

**JSON format:**
```sql
-- audit_log_read() can read rotated files
-- if they match the current file pattern
SELECT audit_log_read();
-- Reads from current and rotated files matching pattern
```

**XML format:**
* Must read manually or with external tools
* Cannot use `audit_log_read()` function

**File naming pattern:**
* Rotated files: `audit_filter.log.YYYYMMDDHHMMSS`
* Current file: `audit_filter.log`
* Pattern matching is based on base filename

## Pruning behavior and configuration

Pruning removes old audit log files based on size or age limits.

### Pruning requirements

To enable pruning, you must configure at least one of the following:

1. **Enable rotation:**
   ```sql
   SET GLOBAL audit_log_filter.rotate_on_size = 1073741824;
   ```
   Pruning only works when rotation is enabled.

2. **Configure size-based pruning:**
   ```sql
   SET GLOBAL audit_log_filter.max_size = 5368709120; -- 5GB
   ```

3. **Configure time-based pruning:**
   ```sql
   SET GLOBAL audit_log_filter.prune_seconds = 2592000; -- 30 days
   ```

### Size-based pruning

**Configuration:**
```sql
SET GLOBAL audit_log_filter.max_size = 10737418240; -- 10GB
```

**Behavior:**
* When combined size of all audit log files exceeds `max_size`, oldest files are pruned
* Pruning continues until total size is below limit
* Current active file is never pruned
* Files are pruned in order of age (oldest first)

**Example:**
```
Total size: 12GB (max_size: 10GB)
Files:
  audit_filter.log.20240101 (2GB) → Pruned (oldest)
  audit_filter.log.20240102 (3GB) → Pruned
  audit_filter.log.20240103 (4GB) → Kept
  audit_filter.log (3GB) → Kept (current file)
```

### Time-based pruning

**Configuration:**
```sql
SET GLOBAL audit_log_filter.prune_seconds = 604800; -- 7 days
```

**Behavior:**
* Files older than `prune_seconds` are automatically pruned
* Age is calculated from file modification time
* Current active file is never pruned
* Pruning happens during rotation operations

**Example:**
```
prune_seconds: 7 days (604800 seconds)
Current date: 2024-01-08

Files:
  audit_filter.log.20240101 (7 days old) → Pruned
  audit_filter.log.20240102 (6 days old) → Kept
  audit_filter.log.20240103 (5 days old) → Kept
  audit_filter.log (current) → Kept
```

### Combined size and time pruning

You can configure both size and time-based pruning:

```sql
SET GLOBAL audit_log_filter.max_size = 10737418240; -- 10GB
SET GLOBAL audit_log_filter.prune_seconds = 2592000; -- 30 days
```

**Behavior:**
* Files are pruned if they exceed EITHER limit
* Size limit: Total size of all files
* Time limit: Age of individual files
* Whichever condition is met first triggers pruning

**Recommendation:**
When both are configured, set `max_size` to at least 7 times `rotate_on_size` to allow multiple rotated files before pruning.

### Pruning with encryption

**Behavior:**
* Encrypted files can be pruned normally
* Pruning does not require decryption
* Pruned files are permanently deleted
* Ensure you have backups before enabling aggressive pruning

### Pruning with compression

**Behavior:**
* Compressed files are pruned based on compressed size
* Pruning considers total compressed size of all files
* Compression reduces storage, allowing more files before pruning

### Monitoring pruning

**Check current file sizes:**
```sql
SHOW STATUS LIKE 'audit_log_filter_current_size';
SHOW STATUS LIKE 'audit_log_filter_total_size';
```

**Verify pruning is working:**
* Monitor disk space usage
* Check that old files are being removed
* Verify files older than `prune_seconds` are pruned
* Ensure total size stays below `max_size`
