
The `-y` flag automatically confirms all actions without asking for user input. This makes running commands smoother, especially in situations where you can't or don't want to interact, like during unattended installations or automated scripts. However, keep in mind that using the `-y` flag skips confirmation prompts, which means you won't have a chance to review any changes before they're made. So, it's best to use this flag only when you're sure about the command you're executing.

The `-y` flag applies to `percona-release setup`. With `percona-release` 1.0-34, `percona-release setup ps-97-lts` disables all Percona repositories but does not enable the Percona Server for MySQL 9.7 repository. For unattended installations, enable the repository with `enable-only` instead:

``` shell
percona-release enable-only ps-97-lts release
```