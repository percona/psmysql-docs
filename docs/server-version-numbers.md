# Understand version numbers

A version number identifies the product release. The product contains the latest Generally Available (GA) features at the time of that release.

<style>
    table {
        border-collapse: collapse;
        width=100%;
    }
    table td {
        border: 2px solid black;
        padding: 8px;
        text-align: center;
    }
    tr:nth-child(even){
        background-color:#f5f5f5
    }
</style>

| 5.7.39| -42 |
|---|---|
| Base version | Minor build version |

Percona uses semantic version numbering, which follows the pattern of base version and minor build version. Percona assigns unique, non-negative integers in increasing order for each minor build release. The version number combines the base [MySQL 5.7](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/) version number and the minor build version.

The version numbers for Percona Server for MySQL 5.7.39-42 define the following information:

* Base version - the leftmost numbers indicate [MySQL 5.7](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/) version used as a base. An increase in base version resets the minor build version to 0.

* Minor build version - an internal number that increases by one every time Percona Server for MySQL is released.

Percona Server for MySQL 5.7.18-14, 5.7.18-15, and 5.7.18-16 are multiple releases based on MySQL 5.7.18. 

