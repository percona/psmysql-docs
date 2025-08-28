
The `-y` flag automatically confirms all actions without prompting the user for input. This feature streamlines the execution of commands, making it particularly advantageous for scenarios where user interaction is not possible or desired, for example, unattended installations or automated scripts. While using the `-y` option eliminates confirmation prompts, the flag also removes the ability to review any changes before they are applied. Use this option only when you are confident in the command being executed.

The recommended syntax for using this flag with the `percona-release setup` is: 

``` {.bash data-prompt="$"}
$ percona-release setup -y ps-84-lts 
``` 