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

| 5.7.39| -42. | 2|
|---|---|---|
| Base version | Minor build version | Custom build |

Percona uses semantic version numbering, which follows the pattern of base version, minor build version, and an optional custom build. Percona assigns unique, non-negative integers in increasing order for each minor build release. The version number combines the base [MySQL 5.7](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/) version number, the minor build version, and the custom build version, if needed.

For example, the version numbers for Percona Server for MySQL 5.7.39-42.2 define the following information:

* Base version - the leftmost numbers indicate [MySQL 5.7](https://dev.mysql.com/doc/relnotes/mysql/5.7/en/) version used as a base. An increase in base version resets the minor build version to 0.

* Minor build version - an internal number that increases by one every time Percona Server for MySQL is released.

* Custom build version - an optional number assigned to custom builds used for bug fixes. The software features, unless they’re included in the bug fix, don’t change.

Percona Server for MySQL 5.7.18-14, 5.7.18-15, and 5.7.18-16 are multiple releases based on MySQL 5.7.18. 

