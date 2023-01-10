# Data scrubbing

**Starting with Percona Server for MySQL 8.0.30-22, this feature is removed.**

The `DELETE` statement does the following:


* Marks the rows as deleted


* Added to `unused`


* Records the deleted row position


* Records the time when delete was committed

The data is not immediately removed from disk storage. When a new row is inserted, the row is stored without fragmentation on a page with free space. The deleted data remains on the disk until new data overwrites it.

Using Data Scrubbing, you have two options to remove the data and reclaim the space:

| How data is removed | Descriptions                                                                       |
|---------------------|------------------------------------------------------------------------------------|
| Immediate           | The data is removed immediately, independent of key rotation or background threads |
| Background          | The moment when the data is removed can be unpredictable                           |


Once enabled, data scrubbing works automatically on each tablespace.

To enable data scrubbing, you must enable either one or both of the following variables:

* innodb-background-scrub-data-uncompressed

* innodb-background-scrub-data-compressed

Uncompressed tables can also be scrubbed immediately, independent of key
rotation or background threads. Setting the variable
innodb-immediate-scrub-data-uncompressed enables this operation. This variable does not support operations on compressed tables.

For background scrubbing, you must set the innodb_encryption_threads variable to a value greater than **zero** when you enable data scrubbing. Intermediate scrubbing does not use encryption threads. A separate thread performs log scrubbing.

## System variables

### `innodb_background_scrub_data_compressed`

| Option       | Description                               |
|--------------|-------------------------------------------|
| Command-line | --innodb-background-scrub-data-compressed |
| Scope        | Global                                    |
| Dynamic      | Yes                                       |
| Data type    | Boolean                                   |
| Default      | OFF                                       |

Enables compressed data scrubbing.

### `innodb_background_scrub_data_uncompressed`

| Option       | Description                                 |
|--------------|---------------------------------------------|
| Command-line | --innodb-background-scrub-data-uncompressed |
| Scope        | Global                                      |
| Dynamic      | Yes                                         |
| Data type    | Boolean                                     |
| Default      | OFF                                         |


Enables uncompressed data scrubbing.

### `innodb_scrub_log`

| Option       | Description        |
|--------------|--------------------|
| Command-line | --innodb-scrub-log |
| Scope        | Global             |
| Dynamic      | No                 |
| Data type    | Boolean            |
| Default      | OFF                |

Enables redo log scrubbing.

### `innodb_scrub_log_speed`

| Option       | Description              |
|--------------|--------------------------|
| Command-line | --innodb-scrub-log-speed |
| Scope        | Global                   |
| Dynamic      | Yes                      |
| Data type    | Numeric                  |
| Default      | 256                      |

Defines the scrubbing speed in bytes/sec of the redo log.

### `innodb_immediate_scrub_data_uncompressed`

| Option       | Description                                |
|--------------|--------------------------------------------|
| Command-line | --innodb-immediate-scrub-data-uncompressed |
| Scope        | Global                                     |
| Dynamic      | Yes                                        |
| Data type    | Boolean                                    |
| Default      | OFF                                        |

Enables data scrubbing of uncompressed data.
