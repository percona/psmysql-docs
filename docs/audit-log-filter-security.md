# Audit Log Filter security

The Audit Log Filter component generates audit log filter files. The directory 
that contains these files should be accessible only to the following:

* Users who must be able to view the log

* Server must be able to write to the directory

The files are not encrypted by default and may contain sensitive information.

The default name for the file in the data directory is `audit_filter.log`. If needed, use the `audit_log_filter.file` system variable at server startup to change the location. Ensure the directory specified in `audit_log_filter.file` exists before starting the server; if the parent directory does not exist, the component reports an error and the server starts without the audit log filter component active. Due to the log rotation, multiple audit log files may exist.
