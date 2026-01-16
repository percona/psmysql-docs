# Audit Log Filter security

The Audit Log Filter component generates audit log filter files. The directory 
that contains these files should be accessible only to the following:

* Users who must be able to view the log

* Server must be able to write to the directory

The files are not encrypted by default and may contain sensitive information.

The default name for the file in the data directory is `audit_filter.log`. If needed, use the `audit_log_filter.file` system variable at server startup to change the location. Due to the log rotation, multiple audit log files may exist.

## Encryption best practices

### When to use encryption

Enable encryption for audit log files when:
* Logs contain sensitive data (PII, financial information, etc.)
* Compliance requirements mandate encrypted audit logs
* Logs are stored in shared or untrusted storage
* Regulatory requirements (HIPAA, PCI DSS, etc.) require encryption

### Enabling encryption

**Step 1: Install keyring component**
```sql
INSTALL COMPONENT 'file://component_keyring_file';
-- Or use another keyring component (vault, KMIP, AWS KMS)
```

**Step 2: Set encryption password**
```sql
SELECT audit_log_encryption_password_set('your_secure_password');
```

**Step 3: Enable encryption (requires restart)**
```sql
SET GLOBAL audit_log_filter.encryption = 'AES';
-- Restart server for change to take effect
```

### Key management

**Using keyring components:**
* Store encryption passwords in keyring (recommended)
* Keyring provides secure password storage
* Supports password rotation
* Multiple keyring backends available (file, vault, KMIP, AWS KMS)

**Password rotation:**
```sql
-- Set new password (old password is archived)
SELECT audit_log_encryption_password_set('new_secure_password');

-- Old password remains available for reading old files
-- New password is used for new log files
```

**Password history:**
```sql
-- Configure password retention (in days)
SET GLOBAL audit_log_filter.password_history_keep_days = 90;
-- Passwords older than 90 days may be removed
-- But remain available if needed for old files
```

### Encryption performance

**Impact:**
* Minimal performance overhead (typically < 5%)
* Encryption happens during log write operations
* CPU usage increases slightly
* Disk I/O remains similar

**Best practices:**
* Use hardware acceleration if available
* Monitor performance after enabling encryption
* Test in non-production environment first

## Access control recommendations

### File permissions

**Recommended permissions:**
```bash
# Audit log directory
chmod 750 /var/lib/mysql/audit
chown mysql:mysql /var/lib/mysql/audit

# Audit log files
chmod 640 /var/lib/mysql/audit/audit_filter.log*
chown mysql:mysql /var/lib/mysql/audit/audit_filter.log*
```

**Permissions breakdown:**
* Directory: `750` - Owner (mysql) can read/write/execute, group can read/execute, others have no access
* Files: `640` - Owner (mysql) can read/write, group can read, others have no access

### Directory access

**Who should have access:**
* MySQL server process (must have write access)
* Database administrators (read access for log analysis)
* Security team (read access for audits)
* Backup systems (read access for backups)

**Who should NOT have access:**
* Application users
* General system users
* Unauthorized personnel

### Protecting encrypted files

**Additional security measures:**
1. **Separate storage:** Store encrypted logs on separate, secure storage
2. **Backup encryption:** Ensure backups are also encrypted
3. **Access logging:** Log who accesses audit log files
4. **Network security:** If logs are on network storage, use encrypted connections
5. **Physical security:** Secure physical access to log storage

### Log file integrity

**Verification:**
* Use file system integrity checks
* Monitor for unauthorized modifications
* Implement file checksums/hashes
* Regular integrity audits

**Tamper detection:**
* Encrypted files are harder to tamper with
* Monitor file modification times
* Compare file sizes and checksums
* Alert on unexpected changes

## Compliance considerations

### PCI DSS compliance

**Requirements:**
* Audit all access to cardholder data
* Log all administrative access
* Protect audit logs from modification
* Retain logs for specified period

**How audit log filter helps:**
* Logs all database access
* Encryption protects log integrity
* Access controls prevent unauthorized modification
* Supports retention requirements

### HIPAA compliance

**Requirements:**
* Audit access to protected health information (PHI)
* Log all database access
* Protect audit logs
* Retain logs as required

**How audit log filter helps:**
* Logs access to PHI-containing tables
* Encryption ensures log security
* Access controls meet HIPAA requirements
* Supports audit trail requirements

### SOX compliance

**Requirements:**
* Audit financial data access
* Log all changes to financial data
* Protect audit logs
* Demonstrate compliance

**How audit log filter helps:**
* Logs all financial database operations
* Tracks who accessed what data
* Encryption protects audit trail
* Provides compliance evidence

### General compliance best practices

1. **Define audit requirements:** Identify what must be logged
2. **Configure filters:** Set up filters to meet requirements
3. **Enable encryption:** Protect audit logs
4. **Control access:** Limit who can view/modify logs
5. **Retain logs:** Configure retention policies
6. **Monitor compliance:** Regularly verify logging is working
7. **Document procedures:** Document audit log management procedures

### Retention requirements

**Configure retention:**
```sql
-- Time-based retention (30 days)
SET GLOBAL audit_log_filter.prune_seconds = 2592000;

-- Size-based retention (10GB total)
SET GLOBAL audit_log_filter.max_size = 10737418240;
```

**Compliance considerations:**
* Ensure retention meets regulatory requirements
* Some regulations require longer retention (7 years for SOX)
* Balance retention with storage costs
* Archive old logs before pruning if needed

### Immutability considerations

**Challenges:**
* MySQL audit logs are files that can be modified
* File system permissions help but don't guarantee immutability

**Mitigation strategies:**
1. **Encryption:** Makes tampering more difficult
2. **Access controls:** Limit who can modify files
3. **Backup immediately:** Copy logs to immutable storage
4. **External logging:** Send logs to external SIEM systems
5. **Write-once storage:** Use WORM (Write Once Read Many) storage
6. **Integrity checks:** Regular checksums/hash verification
