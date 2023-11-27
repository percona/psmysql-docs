# Audit Log Filter restrictions

## General restrictions

The Audit Log Filter has the following general restrictions:

* Logs only SQL statements. Statements made by NoSQL APIs, such as the Memcached API, are not logged.

* Logs only the top-level statement. Statements within a stored procedure or a trigger are not logged. Does not log the file contents for statements like `LOAD_DATA`.

* If used with a cluster, the component must be installed on each server used to execute SQL on the cluster.

* If used with a cluster, the application or user is responsible for aggregating all the data of each server used in the cluster.