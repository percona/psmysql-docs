# Metrics for scalability measurement

**NOTE**: This feature has been deprecated in *Percona Server for MySQL* Percona Server for MySQL 5.7.16-10. Users
who have installed this plugin but are not using its capability are advised
to uninstall the plugin due to known crashing bugs.

*Percona Server for MySQL* has implemented extra scalability metrics. These metrics allow using Little’s Law, queuing theory, and Universal Scalability Law to gain insights into server performance. This feature is implemented as a plugin.

## Installation

Scalability Metrics plugin is shipped with *Percona Server for MySQL*, but it is not installed by default. To enable the plugin you must run the following command:

```
INSTALL PLUGIN scalability_metrics SONAME 'scalability_metrics.so';
```

You can check if the plugin is loaded correctly by running:

```
SHOW PLUGINS;
```

The plugin should be listed in the output:

```
+--------------------------------+----------+--------------------+------------------------+---------+
| Name                           | Status   | Type               | Library                | License |
+--------------------------------+----------+--------------------+------------------------+---------+
...
| scalability_metrics            | ACTIVE   | AUDIT              | scalability_metrics.so | GPL     |
+--------------------------------+----------+--------------------+------------------------+---------+
```

## System Variables

### `scalability_metrics_control`


| Option | Description |
| --- | --- |
| Command-line | Yes |
| Scope | Global |
| Dynamic | Yes |
| Data type | String |
| Default | OFF |
| Values | OFF, ON, RESET |

This variable can be used to enable and disable the collection of metrics for scalability measurement. By setting the value to `RESET` all counters will be reset while continuing to count metrics.

## Status Variables

### `scalability_metrics_elapsedtime`

| Option | Description |
| --- | --- |
| Data type | Numeric |

This status variable shows total time elapsed, in microseconds, since metrics collection was started.

### `scalability_metrics_queries`

| Option | Description |
| --- | --- |
| Data type | Numeric |

This status variable shows number of completed queries since metrics collection was started.

### `scalability_metrics_concurrency`

| Option | Description |
| --- | --- |
| Data type | Numeric |

This status variable shows number of queries currently executed.

### `scalability_metrics_totaltime`

| Option | Description |
| --- | --- |
| Data type | Numeric |

This status variable shows total execution time of all queries, including the in-progress time of currently executing queries, in microseconds (ie. if two queries executed with 1 second of response time each, the result is 2 seconds).

### `scalability_metrics_busytime`

| Option | Description |
| --- | --- |
| Data type | Numeric |

This counter accounts the non-idle server time, that is, time when at least one query was executing.

## Version Specific Information

> 
> * Percona Server for MySQL 5.7.10-1
> Feature ported from *Percona Server for MySQL* 5.6


> * Percona Server for MySQL 5.7.16-10
> Feature has been deprecated.

## Other Reading


* [Fundamental performance and scalability instrumentation](http://www.xaprb.com/blog/2011/10/06/fundamental-performance-and-scalability-instrumentation/)


* [Forecasting MySQL Scalability with the Universal Scalability Law Whitepaper](http://www.percona.com/files/white-papers/forecasting-mysql-scalability.pdf)
