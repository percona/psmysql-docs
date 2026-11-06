# Size MyRocks background jobs

Select [`rocksdb_max_background_jobs`](myrocks-server-variables.md#rocksdb_max_background_jobs) from the workload of the host. The value shares CPU cores with foreground query threads. Compaction receives roughly three quarters of the configured jobs. See [Slot distribution between flushes and compaction](myrocks-server-variables.md#slot-distribution-between-flushes-and-compaction).

## Dedicated MyRocks instance

Set `rocksdb_max_background_jobs` equal to the physical CPU core count. RocksDB `IncreaseParallelism()` uses a one-to-one mapping for dedicated key-value workloads. MyRocks applies the same limit through `rocksdb_max_background_jobs`. Use the one-to-one ratio when MyRocks can consume host CPU for flush and compaction.

## Database server with mixed query traffic

Set `rocksdb_max_background_jobs` to the CPU core count divided by four. The result is 25 percent of available cores. The one-to-four ratio leaves CPU for foreground query threads.

## Write-heavy workload on NVMe storage

Set `rocksdb_max_background_jobs` to the CPU core count divided by two. The result is 50 percent of available cores. Cap the value at eight to 16 jobs. Values above 16 add thread contention and latency variance without higher throughput.

## Starting values by core count

| Available CPU cores | Dedicated instance (1:1) | Database server (1:4) | Write-heavy NVMe (1:2, cap 8 to 16) |
|---------------------|--------------------------|-----------------------|-------------------------------------|
| 4                   | 4                        | 1                     | 2                                   |
| 8                   | 8                        | 2                     | 4                                   |
| 16                  | 16                       | 4                     | 8                                   |
| 32                  | 32                       | 8                     | 8 to 16                             |
| 64 or more          | 64                       | 16                    | 16                                  |

The database-server column uses integer division. Four cores produce one job. Raise that value to two only when write stalls persist and the host retains spare CPU.

## Combined thread budget

Keep the sum of active client threads and `rocksdb_max_background_jobs` at or below the logical CPU thread count. A sum above that count increases latency through CPU context switches.

On a server that also runs InnoDB, include InnoDB purge threads and page-cleaner threads in the same budget.
