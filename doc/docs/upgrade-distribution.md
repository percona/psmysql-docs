# Performing a Distribution upgrade in-place on a System with installed Percona packages

The recommended process for performing a distribution upgrade on a system with
the Percona packages installed is the following:

> 
> 1. Record the installed Percona packages


> 2. Backup the data and configurations


> 3. Uninstall the Percona packages without removing the configurations or
> data


> 4. Perform the upgrade by following the distribution upgrade instructions


> 5. Reboot the system


> 6. Install the Percona packages intended for the upgraded version of the
> distribution