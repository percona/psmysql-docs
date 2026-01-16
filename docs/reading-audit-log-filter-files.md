# Reading Audit Log Filter files

The Audit Log Filter functions can provide a SQL interface to read JSON-format audit log files. The functions cannot read log files in other formats. Configuring the component for JSON logging lets the functions use the directory that contains the current audit log filter file and search in that location for readable files. The value of the `audit_log_filter.file` system variable provides the file location, base name, and the suffix and then searches for names that match the pattern.

If the file is renamed and no longer fits the pattern, the file is ignored.

## Functions used for reading the files

The following functions read the files in the JSON-format:

* [`audit_log_read`](audit-log-filter-variables.md#audit_log_read) - reads audit log filter events

* [`audit_log_read_bookmark`](audit-log-filter-variables.md#audit_log_read_bookmark) - for the most recently read event, returns a bookmark. This bookmark can be passed to `audit_log_read()`.

Initialize a read sequence by using a bookmark or an argument that specifies the start position:

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_read(audit_log_read_bookmark());
```

The following example continues reading from the current position:

```{.bash data-prompt="mysql>"}
mysql> SELECT audit_log_read();
```

Reading a file is closed when the session ends or calling `audit_log_read()` with another argument.

## Reading different formats

### JSON format reading

The `audit_log_read()` and `audit_log_read_bookmark()` functions work only with JSON format files.

**Requirements:**
* `audit_log_filter.format` must be set to `JSON`
* Files must be in JSON format
* Function returns error if format is not JSON

**Example:**
```sql
-- Ensure format is JSON
SHOW VARIABLES LIKE 'audit_log_filter.format';
-- Should show: JSON

-- Read audit log
SELECT audit_log_read();
```

### XML format reading

XML format files (OLD or NEW style) cannot be read using `audit_log_read()` function.

**Options for reading XML files:**
1. **Manual parsing:** Use text editors or XML parsers
2. **External tools:** Use log analysis tools that support XML
3. **Convert to JSON:** Change format to JSON for future logs (requires restart)

**XML file structure:**
* OLD style: Traditional XML format with specific schema
* NEW style: Updated XML format with enhanced structure
* Both formats are human-readable but require XML parsing tools

### Converting between formats

**To read logs programmatically:**
1. Change `audit_log_filter.format` to `JSON`
2. Restart server
3. Future logs will be in JSON format
4. Use `audit_log_read()` function

**Note:** Old XML format files remain in XML and cannot be converted. Only new logs use the new format.

## Reading historical log files

### Reading rotated files

The `audit_log_read()` function can read rotated files if they match the current file naming pattern.

**Requirements:**
* Files must have the same base name as `audit_log_filter.file`
* Files must be in JSON format
* Files must be in the same directory as the current log file

**Example:**
```
Current file: audit_filter.log
Rotated files:
  audit_filter.log.20240101120000
  audit_filter.log.20240102120000
  audit_filter.log.20240103120000

audit_log_read() reads from all matching files
```

**File pattern matching:**
* Base name must match: `audit_filter.log`
* Timestamp suffix is ignored for pattern matching
* Files with different base names are ignored

### Reading specific time ranges

Use bookmarks to read from specific positions:

**Read from bookmark:**
```sql
-- Get bookmark for most recent event
SELECT audit_log_read_bookmark();
-- Returns: {"timestamp": "2024-01-01 12:00:00", "id": 12345}

-- Read from that bookmark
SELECT audit_log_read('{"timestamp": "2024-01-01 12:00:00", "id": 12345}');
```

**Read with max array length:**
```sql
-- Limit number of events returned
SELECT audit_log_read(NULL, 100);
-- Returns maximum 100 events
```

### Limitations of reading old files

**File naming:**
* If rotated files are renamed with different patterns, they won't be found
* Files moved to different directories won't be accessible
* Files with different base names are ignored

**Format compatibility:**
* Only JSON format files can be read
* XML format files cannot be read with functions
* Mixed format files cause errors

**File access:**
* Files must be readable by MySQL server process
* Encrypted files require password/keyring access
* Compressed files may need decompression

## Reading errors and troubleshooting

### File doesn't exist

**Error:** Function returns NULL or empty result

**Causes:**
* Log file hasn't been created yet (no events logged)
* File was deleted or moved
* Incorrect file path configuration

**Solution:**
```sql
-- Check file location
SHOW VARIABLES LIKE 'audit_log_filter.file';

-- Verify file exists
-- Check data directory or specified path

-- Generate some events to create file
-- Then try reading again
```

### Format is not JSON

**Error:** Function returns error or NULL

**Causes:**
* `audit_log_filter.format` is set to OLD or NEW (XML)
* File is in XML format

**Solution:**
```sql
-- Check current format
SHOW VARIABLES LIKE 'audit_log_filter.format';

-- Change to JSON (requires restart)
SET GLOBAL audit_log_filter.format = 'JSON';
-- Restart server

-- Note: Old XML files still cannot be read
-- Only new logs will be in JSON format
```

### File is corrupted

**Error:** Function returns error or partial data

**Causes:**
* File system corruption
* Incomplete writes
* Disk errors

**Solution:**
1. Check file system for errors
2. Verify disk health
3. Check MySQL error log for I/O errors
4. Restore from backup if available
5. Corrupted files may need manual repair or recreation

### File is encrypted

**Error:** Cannot read encrypted files without proper setup

**Causes:**
* Encryption is enabled but keyring/password not accessible
* Encryption password not set
* Keyring component not loaded

**Solution:**
```sql
-- Check encryption status
SHOW VARIABLES LIKE 'audit_log_filter.encryption';

-- If encryption is AES, ensure:
-- 1. Keyring component is loaded
-- 2. Encryption password is set
-- 3. Keyring has access to password

-- Get encryption password (if accessible)
SELECT audit_log_encryption_password_get();
```

### File is compressed

**Behavior:** Compressed files may need special handling

**Causes:**
* `audit_log_filter.compression` is set to GZIP
* Files are compressed with gzip

**Solution:**
* `audit_log_read()` should handle compressed files automatically
* If issues occur, check compression configuration
* Verify gzip support is available

### Reading performance issues

**Symptoms:**
* Slow read operations
* Timeout errors
* High CPU usage during reads

**Causes:**
* Very large log files
* Many rotated files to process
* Complex JSON parsing

**Solutions:**
1. Use `max_array_length` parameter to limit results
2. Read in smaller chunks using bookmarks
3. Consider archiving old files
4. Use external tools for bulk analysis
5. Increase `audit_log_filter.read_buffer_size` if available

### Best practices for reading logs

1. **Use JSON format** for programmatic access
2. **Read in chunks** using bookmarks and max_array_length
3. **Archive old files** to reduce reading overhead
4. **Monitor file sizes** to prevent performance issues
5. **Use external tools** for complex analysis of large log sets
6. **Test reading** in non-production environment first
