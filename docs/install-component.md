# INSTALL COMPONENT

The `INSTALL COMPONENT` does the following:

* Installs the component
* Activates the component

If an error, such as a misspelled component name, occurs, the statement fails and nothing happens.

You can install multiple components at the same time. 

## Example

The following is an example of the `INSTALL COMPONENT` statement.

```{.bash data-prompt="mysql>"}
mysql> INSTALL COMPONENT 'file://componentA';
```