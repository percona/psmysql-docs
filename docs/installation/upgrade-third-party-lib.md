
# Upgrade third-party libraries

The following are generic instructions for updating libraries using a package manager. Your environment may differ. Upgrading libraries can have unintended consequences. Test the upgrade on a staging environment before upgrading production.

## Prepare

These steps apply to any package manager. The example updates the OpenSSL library.
{.power-number}

1. Create a full server backup to ensure data integrity in case of issues.
2. Identify the library and review the installation method.
3. Research the compatibility between the new library and your current MySQL version.
4. Stop the server.

## Upgrade

=== "Distributions using the APT package manager"

    Install the update:

    ```{.bash data-prompt="$"}
    $ sudo apt update
    $ sudo apt install libssl-dev openssl
    ```

=== "Distributions using the YUM package manager"

    Install the update:

    ```{.bash data-prompt="$"}
    $ sudo yum update
    $ sudo yum install openssl
    ```

## Verify

After the upgrade, do the following:
{.power-number}

1. Restart the server to ensure the library is loaded correctly.

    ```{.bash data-prompt="$"}
    $ sudo systemctl restart mysql
    ```

2. Connect to the server and verify the update with either `SHOW PLUGINS;` or `SHOW VARIABLES LIKE '%library_name%';`.

3. Test the library functionality by running scripts or applications that rely on the upgraded library.

## Troubleshoot

If you find issues:

* Check the error logs.
* Consult the documentation for the library and online resources for any troubleshooting steps specific to this library. Look for any potential compatibility issues.