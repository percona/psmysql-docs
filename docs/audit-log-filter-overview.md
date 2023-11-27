# Audit Log Filter overview

The Audit Log Filter component allows you to monitor, log, and block a connection or query actively executed on the selected server. 

Enabling the component produces a log file that contains a record of server activity. The log file has information on connections and databases accessed by that connection. 

The component uses the `mysql` system database to store filter and user account data. Set the [`audit_log_filter.database`](audit-log-filter-variables.md#audit_log_filter.database) variable at server startup to select a different database.

The `AUDIT_ADMIN` privilege is required to enable users to manage the Audit Log Filter component.

## Privileges

Define the privilege at runtime at the startup of the server. The associated Audit Log Filter privilege can be unavailable if the component is not enabled.

### `AUDIT_ADMIN`

This privilege is defined by the server and enables the user to configure the component.

### `AUDIT_ABORT_EXEMPT`

This privilege allows queries from a user account to always be executed. An `abort` item does not block them. This ability lets the user account regain access to a system if an audit is misconfigured. The query is logged due to the privilege. User accounts with the `SYSTEM_USER` privilege have the `AUDIT_ABORT_EXEMPT` privilege.

## Audit Log Filter tables

The Audit Log Filter component uses `mysql` system database tables in the `InnoDB` storage engine. These tables store user account data and filter data. When you start the server, change the component's database with the `audit_log_filter.database` variable.

The `audit_log_filter` table stores the definitions of the filters and has the following column definitions:

<!DOCTYPE html>
<html>
<head>
    <title>HTML Table Generator</title> 
    <style>
        #demTable {
            width:100%;
            height:100%;
            border:1px solid #b3adad;
            border-collapse:collapse;
            padding:5px;
        }
        #demTable th {
            border:1px solid #b3adad;
            padding:5px;
            background: #f0f0f0;
            color: #313030;
        }
        #demTable td {
            border:1px solid #b3adad;
            text-align:left;
            padding:5px;
            background: #ffffff;
            color: #313030;
        }
    </style>
</head>
<body>
    <table id="demTable">
        <thead>
            <tr>
                <th><div style="color: #333333;background-color: #f5f5f5;font-family: Menlo, Monaco, 'Courier New', monospace;font-weight: normal;font-size: 14px;line-height: 21px;white-space: pre;">Column name</div></th>
                <th><div style="color: #333333;background-color: #f5f5f5;font-family: Menlo, Monaco, 'Courier New', monospace;font-weight: normal;font-size: 14px;line-height: 21px;white-space: pre;">Description</div></th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>&nbsp;NAME</td>
                <td>&nbsp;Name of the filter</td>
            </tr>
            <tr>
                <td>&nbsp;FILTER</td>
                <td>&nbsp;Definition of the filter linked to the name as a JSON value</td>
            </tr>
        </tbody>
    </table>
</body>
</html>

The `audit_log_user` table stores account data and has the following column definitions:

<!DOCTYPE html>
<html>
<head>
    <title>HTML Table Generator</title> 
    <style>
        #demTable {
            width:100%;
            height:100%;
            border:1px solid #b3adad;
            border-collapse:collapse;
            padding:5px;
        }
        #demTable th {
            border:1px solid #b3adad;
            padding:5px;
            background: #f0f0f0;
            color: #313030;
        }
        #demTable td {
            border:1px solid #b3adad;
            text-align:left;
            padding:5px;
            background: #ffffff;
            color: #313030;
        }
    </style>
</head>
<body>
    <table id="demTable">
        <thead>
            <tr>
                <th><div style="color: #333333;background-color: #f5f5f5;font-family: Menlo, Monaco, 'Courier New', monospace;font-weight: normal;font-size: 14px;line-height: 21px;white-space: pre;">Column name</div></th>
                <th><div style="color: #333333;background-color: #f5f5f5;font-family: Menlo, Monaco, 'Courier New', monospace;font-weight: normal;font-size: 14px;line-height: 21px;white-space: pre;">Description</div></th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>&nbsp;USER</td>
                <td>&nbsp;The account name of the user</td>
            </tr>
            <tr>
                <td>&nbsp;HOST</td>
                <td>&nbsp;The account name of the host</td>
            </tr>
            <tr>
                <td>&nbsp;FILTERNAME</td>
                <td>&nbsp;The account filter name</td>
            </tr>
        </tbody>
    </table>
</body>
</html>