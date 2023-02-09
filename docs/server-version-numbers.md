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

| 8.0.29| -21 |
|---|---|
| Base version | Minor build version |

Percona uses semantic version numbering, which follows the pattern of base version and minor build version. Percona assigns unique, non-negative integers in increasing order for each minor build release. The version number combines the base [MySQL 8.0](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/) version number and the minor build version.

The version numbers for Percona Server for MySQL 8.0.29-21 define the following information:

* Base version - the leftmost numbers indicate [MySQL 8.0](https://dev.mysql.com/doc/relnotes/mysql/8.0/en/) version used as a base. 

* Minor build version - an internal number that increases by one every time Percona Server for MySQL is released.

Percona Server for MySQL 8.0.28-19 and 8.0.28-20 are both based on MySQL 8.0.28. 
