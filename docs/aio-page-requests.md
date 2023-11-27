# Multiple page asynchronous I/O requests

The I/O unit size in *InnoDB* is only one page, even if the server doing read ahead. A 16KB
I/O unit size is too small for sequential reads, and less efficient than a larger I/O unit size. *InnoDB* uses Linux asynchronous I/O (`aio`) by default. By submitting multiple, consecutive 16KB read requests at the same time, Linux internally merges the requests and
reads more efficiently. 

This feature is able to submit multiple page I/O requests and works in the background. You can manage the feature with the [linear read-ahead technique]. This technique adds pages to the buffer pool based on the buffer pool pages being accessed sequentially. The [`innodb_read_ahead_threshold`] configuration parameter controls this operation.

[On a HDD RAID 1+0 environment](http://yoshinorimatsunobu.blogspot.hr/2013/10/making-full-table-scan-10x-faster-in.html),
more than 1000MB/s disk reads can be achieved by submitting 64 consecutive pages
requests at once, while only
160MB/s disk reads is shown by submitting single page request.

## Status variables

### `Innodb_buffered_aio_submitted`

| Option         | Description        |
| -------------- | ------------------ |
| Scope:         | Global             |
| Data type:     | Numeric            |

This variable shows the number of submitted buffered asynchronous I/O requests.

## Other reading

* [Making full table scan 10x faster in InnoDB](https://yoshinorimatsunobu.blogspot.hr/2013/10/making-full-table-scan-10x-faster-in.html)

* [Bug #68659  InnoDB Linux native aio should submit more i/o requests at once](https://bugs.mysql.com/bug.php?id=68659)

[linear read-ahead technique]: https://dev.mysql.com/doc/refman/{{vers}}/en/innodb-performance-read_ahead.html

[`innodb_read_ahead_threshold`]: https://dev.mysql.com/doc/refman/{{vers}}/en/innodb-parameters.html#sysvar_innodb_read_ahead_threshold 