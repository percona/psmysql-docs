# Audit Log Filter restrictions

## General restrictions

The Audit Log Filter has the following general restrictions:

The Audit Log Filter has the following general restrictions:

* Log only SQL statements. Statements made by NoSQL APIs, such as the 
  Memcached API, are not logged.

* Log only the top-level statement. Statements within a stored procedure 
  or a trigger are not logged. Do not log the file contents for statements 
  like `LOAD_DATA`.

* Require the component to be installed on each server used to execute SQL 
  on the cluster if used with a cluster.

* Hold the application or user responsible for aggregating all the data from 
  each server used in the cluster if used with a cluster.
