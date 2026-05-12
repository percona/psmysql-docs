
The `-y` flag automatically confirms all actions without asking for user input. This makes running commands smoother, especially in situations where you can't or don't want to interact, like during unattended installations or automated scripts. However, keep in mind that using the `-y` flag skips confirmation prompts, which means you won't have a chance to review any changes before they're made. So, it's best to use this flag only when you're sure about the command you're executing.

The recommended syntax for using this flag with the `percona-release setup` is: 

``` {.bash data-prompt="$"}
$ percona-release setup -y ps-97-lts 
``` 