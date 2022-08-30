# Multiple page asynchronous I/O requests

The I/O unit size in InnoDB is only one page, even if the server is doing read ahead.
A 16KB I/O unit size is small for sequential reads and less efficient than a
larger I/O unit size. InnoDB uses Linux asynchronous I/O (`aio`) by default.
By submitting multiple consecutive 16KB read requests at once, Linux internally can
merge requests, and reads are more efficient. This feature can submit multiple
page I/O requests and works in the background.

You can manage the feature with the
[linear read-ahead](https://dev.mysql.com/doc/refman/5.7/en/innodb-performance-read_ahead.html) technique.
The technique adds pages to the buffer pool based on the buffer pool pages being accessed
sequentially. The configuration parameter, `innodb_read_ahead_threshold` controls this process.

[On an HDD RAID 1+0 environment](http://yoshinorimatsunobu.blogspot.hr/2013/10/making-full-table-scan-10x-faster-in.html),
more than 1000MB/s disk reads can be achieved by submitting 64 consecutive pages
requests at once, while only
160MB/s disk reads is shown by submitting single page request.

## Version Specific Information

> 
> * Percona Server 5.7.20-18: Feature ported from the *Facebook MySQL* patch.

## Status Variables

### `Innodb_buffered_aio_submitted`

Implemented in Percona Server 5.7.20-18.

| Option    | Description |
|-----------|-------------|
| Data type | Numeric     |
| Scope     | Global      |

This variable shows the number of submitted buffered asynchronous I/O requests.

## See also

> 
> [Optimizing full table scans in
> InnoDB](http://yoshinorimatsunobu.blogspot.hr/2013/10/making-full-table-scan-10x-faster-in.html)

> [Bug #68659  InnoDB Linux native aio should submit more i/o requests at once](https://bugs.mysql.com/bug.php?id=68659)
