# MyRocks Information Schema tables

When you install the MyRocks plugin for *MySQL*, the
Information Schema is extended to include the following tables:

## ROCKSDB_GLOBAL_INFO

### Columns

| Column Name | Type         |
|-------------|--------------|
| TYPE        | varchar(513) |
| NAME        | varchar(513) |
| VALUE       | varchar(513) |

## ROCKSDB_CFSTATS

### Columns

| Column Name | Type         |
|-------------|--------------|
| CF_NAME     | varchar(193) |
| STAT_TYPE   | varchar(193) |
| VALUE       | bigint(8)    |

## ROCKSDB_TRX

This table stores mappings of RocksDB transaction identifiers to *MySQL*
client identifiers to enable associating a RocksDB transaction with a *MySQL*
client operation.

### Columns

| Column Name              | Type         |
|--------------------------|--------------|
| TRANSACTION_ID           | bigint(8)    |
| STATE                    | varchar(193) |
| NAME                     | varchar(193) |
| WRITE_COUNT              | bigint(8)    |
| LOCK_COUNT               | bigint(8)    |
| TIMEOUT_SEC              | int(4)       |
| WAITING_KEY              | varchar(513) |
| WAITING_COLUMN_FAMILY_ID | int(4)       |
| IS_REPLICATION           | int(4)       |
| SKIP_TRX_API             | int(4)       |
| READ_ONLY                | int(4)       |
| HAS_DEADLOCK_DETECTION   | int(4)       |
| NUM_ONGOING_BULKLOAD     | int(4)       |
| THREAD_ID                | int(8)       |
| QUERY                    | varchar(193) |

## ROCKSDB_CF_OPTIONS

### Columns

| Column Name | Type         |
|-------------|--------------|
| CF_NAME     | varchar(193) |
| OPTION_TYPE | varchar(193) |
| VALUE       | varchar(193) |

## ROCKSDB_ACTIVE_COMPACTION_STATS

### Columns

| Column Name | Type         |
|-------------|--------------|
| THREAD_ID   | bigint       |
| CF_NAME     | varchar(193) |
| INPUT_FILES | varchar(513) |
| OUTPUT_FILES| varchar(513) |
| COMPACTION_REASON | varchar(513) |

## ROCKSDB_COMPACTION_HISTORY

### Columns

| Column Name | Type         |
|-------------|--------------|
| THREAD_ID   | bigint       |
| CF_NAME     | varchar(513) |
| INPUT_LEVEL | integer      |
| OUTPUT_LEVEL| integer      |
| INPUT_FILES | varchar(513) |
| OUTPUT_FILES| varchar(513) |
| COMPACTION_REASON| varchar(513)|
| START_TIMESTAMP| bigint|
| END_TIMESTAMP| bigint|

## ROCKSDB_COMPACTION_STATS

### Columns

| Column Name | Type         |
|-------------|--------------|
| CF_NAME     | varchar(193) |
| LEVEL       | varchar(513) |
| TYPE        | varchar(513) |
| VALUE       | double       |

## ROCKSDB_DBSTATS

### Columns

| Column Name | Type         |
|-------------|--------------|
| STAT_TYPE   | varchar(193) |
| VALUE       | bigint(8)    |

## ROCKSDB_DDL

### Columns

| Column Name       | Type               |
|-------------------|--------------------|
| TABLE_SCHEMA      | varchar(193)       |
| TABLE_NAME        | varchar(193)       |
| PARTITION_NAME    | varchar(193)       |
| INDEX_NAME        | varchar(193)       |
| COLUMN_FAMILY     | int(4)             |
| INDEX_NUMBER      | int(4)             |
| INDEX_TYPE        | smallint(2)        |
| KV_FORMAT_VERSION | smallint(2)        |
| TTL_DURATION      | bigint(8)          |
| INDEX_FLAGS       | bigint(8)          |
| CF                | varchar(193)       |
| AUTO_INCREMENT    | bigint(8) unsigned |

## ROCKSDB_INDEX_FILE_MAP

### Columns

| Column Name          | Type         |
|----------------------|--------------|
| COLUMN_FAMILY        | int(4)       |
| INDEX_NUMBER         | int(4)       |
| SST_NAME             | varchar(193) |
| NUM_ROWS             | bigint(8)    |
| DATA_SIZE            | bigint(8)    |
| ENTRY_DELETES        | bigint(8)    |
| ENTRY_SINGLEDELETES  | bigint(8)    |
| ENTRY_MERGES         | bigint(8)    |
| ENTRY_OTHERS         | bigint(8)    |
| DISTINCT_KEYS_PREFIX | varchar(400) |

## ROCKSDB_LIVE_FILES_METADATA

| Column Name              | Type         |
|--------------------------|--------------|
| CF_NAME                  | varchar(193) |
| LEVEL                    | varchar(513) |
| NAME                     | varchar(513) |
| DB_PATH                  | varchar(513) |
| FILE_NUMBER              | bigint       |
| FILE_TYPE                | varchar(193) | 
| SIZE                     | bigint       |
| RELATIVE_FILENAME        | varchar(193) | 
| DIRECTORY                | varchar(513) | 
| TEMPERATURE              | varchar(193) |  
| FILE_CHECKSUM            | varchar(513) | 
| FILE_CHECKSUM_FUNC_NAME  | varchar(193) |  
| SMALLEST_SEQNO           | bigint       | 
| LARGEST_SEQNO            | bigint       | 
| SMALLEST_KEY             | varchar(513) |  
| LARGEST_KEY              | varchar(513) |  
| NUM_READS_SAMPLED        | bigint       | 
| BEING_COMPACTED          | tinyint      | 
| NUM_ENTRIES              | bigint       | 
| NUM_DELETIONS            | bigint       | 
| OLDEST_BLOB_FILE_NUMBER  | bigint       | 
| OLDEST_ANCESTER_TIME     | bigint       | 
| FILE_CREATION_TIME       | bigint       |

## ROCKSDB_LOCKS

This table contains the set of locks granted to MyRocks transactions.

### Columns

| Column Name      | Type         |
|------------------|--------------|
| COLUMN_FAMILY_ID | int(4)       |
| TRANSACTION_ID   | bigint      |
| KEY              | varchar(513) |
| MODE             | varchar(32)  |

## ROCKSDB_PERF_CONTEXT

### Columns

| Column Name    | Type         |
|----------------|--------------|
| TABLE_SCHEMA   | varchar(193) |
| TABLE_NAME     | varchar(193) |
| PARTITION_NAME | varchar(193) |
| STAT_TYPE      | varchar(193) |
| VALUE          | bigint(8)    |

## ROCKSDB_PERF_CONTEXT_GLOBAL

### Columns

| Column Name | Type         |
|-------------|--------------|
| STAT_TYPE   | varchar(193) |
| VALUE       | bigint(8)    |

## ROCKSDB_DEADLOCK

This table records information about deadlocks.

### Columns

| Column Name    | Type         |
|----------------|--------------|
| DEADLOCK_ID    | bigint(8)    |
| TRANSACTION_ID | bigint(8)    |
| CF_NAME        | varchar(193) |
| WAITING_KEY    | varchar(513) |
| LOCK_TYPE      | varchar(193) |
| INDEX_NAME     | varchar(193) |
| TABLE_NAME     | varchar(193) |
| ROLLED_BACK    | bigint(8)    |
