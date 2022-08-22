# Improved NUMA support

In cases where the buffer pool memory allocation is bigger than the size of 
the node, the system starts swapping already allocated memory, even if 
memory is available on another node. This happens if the default 
`NUMA` memory allocation policy is selected. In that case, the system 
favors one node more than another, which causes the node to run out of 
memory. If the allocation policy is interleaving, the memory is 
allocated in a round-robin fashion over the available node. This method 
uses the upstream [innodb_numa_interleave](http://dev.mysql.com/doc/refman/5.7/en/innodb-parameters.html#sysvar_innodb_numa_interleave). This feature extends the upstream implementation by implementing the flush_caches variable.

It is generally recommended to enable all options to maximize the performance effects on the `NUMA` architecture.

## Version Specific Information

Percona Server for MySQL 5.7.10-1: Feature ported from *Percona Server for MySQL* 5.6

Percona Server 5.7.22-22: Feature reverted from the upstream implementation back to the one ported from *Percona Server for MySQL* 5.6, in which [innodb_numa_interleave](http://dev.mysql.com/doc/refman/5.7/en/innodb-parameters.html#sysvar_innodb_numa_interleave) variable not only enables NUMA memory interleaving at InnoDB buffer pool allocation but allocates buffer pool with MAP_POPULATE, forcing interleaved allocation at the buffer pool initialization time.

## Command-line Options for mysqld_safe

### `flush_caches`

| Option       | Description |
|--------------|-------------|
| Command-line | Yes         |
| Config file  | Yes         |
| Location     | mysqld_safe |
| Dynamic      | No          |
| Data type    | Boolean     |
| Default      | 0 (OFF)     |
| Range        | 0/1         |

When enabled (set to `1`) this will flush and purge buffers/caches before starting the server to help ensure `NUMA` allocation fairness across nodes. This option is useful for establishing a consistent and predictable behavior for normal usage and/or benchmarking.

!!! admonition "See also"

    [The MySQL “swap insanity” problem and the effects of the NUMA architecture](http://blog.jcole.us/2010/09/28/mysql-swap-insanity-and-the-numa-
    architecture/)

    [A brief update on NUMA and MySQL](http://blog.jcole.us/2012/04/16/a-briefupdate-on-numa-and-mysql/)
