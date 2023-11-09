# UNINSTALL COMPONENT

The `UNINSTALL COMPONENT` does the following:

* Deactivates the component
* Uninstalls the component

If the statement does not undo any persisted variables. 

If an error, such as a misspelled component name, occurs, the statement fails and nothing happens.

You can uninstall multiple components at the same time.

## Required privilege

The statement requires the `DELETE` privilege for the `mysql.component` system table. Executing the statement removes the registration row from this table. 

## Example

The following is an example of the `UNINSTALL COMPONENT` statement.

```{.bash data-prompt="mysql>"}
mysql > UNINSTALL COMPONENT 'file://componentA' ;
```

Find more information in the [UNINSTALL COMPONENT](uninstall-component.md) document.



