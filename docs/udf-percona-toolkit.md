# Percona Toolkit UDFs

These Percona Toolkit user-defined functions (UDFs) offer faster checksum calculations compared to standard methods:

* `libfnv1a_udf`

* `libfnv_udf`

* `libmurmur_udf`

## Other information

* Author/Origin: Baron Schwartz

## Installation

Once the installation is complete, execute the following command to install these functions:

```sql
mysql -e "INSTALL COMPONENT 'file://component_percona_udf'"
```

## Troubleshooting

If the `INSTALL COMPONENT` command fails, try these steps:

* Check the error message for clues about what went wrong.

* Verify the component path `'file://component_percona_udf'`
  is correct and accessible.
  
* Ensure you have the necessary permissions to install
  components in MySQL.
  
If you're still facing issues, consider reaching out to
  [Percona Support :octicons-link-external-16:](https://www.percona.com/services/expert-support/)
  for further assistance.

## Other reading

* Percona Toolkit [documentation :octicons-link-external-16:](https://docs.percona.com/percona-toolkit/)
