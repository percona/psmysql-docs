# FIPS compliance

The Federal Information Processing Standards (FIPS) are a set of U.S. government standards that ensure the security of computer systems for non-military government agencies and contractors. These standards specify how to perform cryptographic operations, such as encryption, hashing, and digital signatures. FIPS mode is a mode of operation that enforces these standards and rejects any non-compliant algorithms or parameters.

Percona Server for MySQL implements the same level of FIPS support as MySQL. Percona Server for MySQL can run in FIPS mode if a FIPS-enabled OpenSSL library and FIPS Object Module are available at runtime or if compiled using a FIPS-validated version of OpenSSL. You can also receive this functionality by [building Percona Server for MySQL from source code](compile-percona-server.md).

## Prerequisites

To prepare Percona Server for MySQL for FIPS certification, do the following:

* Check that your operating system includes FIPS pre-approved OpenSSL library in version 3.0.x or higher. The following distributions includes FIPS pre-approved OpenSSL library in version 3.0.x or higher:

    * RedHat Enterprise Linux 9

    * Oracle Linux 9

    The following distributions also includes OpenSSL library in version 3.0.x but do not have FIPS-approved crypto provider installed by default (you can build the crypto provider from the source for testing):

    * Debian 12 `Bookworm`

    * Ubuntu 22.04 Pro `Jammy` (the OpenSSL FIPS 140-3 certification is under implementation)

* Deploy Percona Server for MySQL from the Pro build, which is built and tested on operating systems with FIPS pre-approved OpenSSL packages.

## The FIPS mode variables

Percona Server for MySQL uses the same variables and values as MySQL. Percona Server for MySQL enables control of FIPS mode on the server side and the client side:

* The `ssl_fips_mode` system variable shows whether the server operates in FIPS mode. This variable is disabled by default.

    The `ssl_fips_mode` system variable has these values:

    * `0` - disables FIPS mode
    * `1` - enables FIPS mode
    * `2` - enables `strict` FIPS mode. This value provides more restrictions than the  `1 ` value. However, MySQL itself does not have any FIPS-specific code other than to specify the FIPS mode value to OpenSSL. The exact behavior of FIPS mode for `1` or `2` depends on the OpenSSL version.

* The `--ssl-fips-mode` client/server option controls whether a given MySQL client operates in FIPS mode. This setting does not change the server setting. This option is disabled by default.

    The `--ssl-fips-mode` client/server option has these values:

    * `OFF` - disables FIPS mode
    * `ON` - enables FIPS mode
    * `STRICT` - enables `strict` FIPS mode. This value provides more restrictions than the `ON` value. However, MySQL itself does not have any FIPS-specific code other than to specify the FIPS mode value to OpenSSL. The exact behavior of FIPS mode for `ON` or `STRICT` depends on the OpenSSL version.
     
    The MySQL server operation in FIPS mode does not depend on which crypto module (regular or FIPS-approved) is set as the default in the OpenSSL configuration file. The server always respects the value of `--ssl-fips-mode` server command line option (`OFF`, `ON`, or `STRICT`). The `ssl_fips_mode` global system variable is read-only and cannot be changed at runtime.
  
    ### Enable the FIPS mode

    To enable the FIPS mode, pass `--ssl-fips-mode=ON` to mysqld as a command line argument or add `ssl-fips-mode=ON` to the configuration file. Ignore the warning that the `--ssl-fips-mode` client/server option is deprecated.
    
    ## Check that FIPS mode is enabled

    To ensure that the FIPS mode is enabled, do the following:

    * Pass `--log-error-verbosity=3` to mysqld as a command line argument or add `log-error-verbosity=3` to the configuration file.
    
    * Check that the error log contains the following message:

        ```{.text .no-copy}
        A FIPS-approved version of the OpenSSL cryptographic library has been detected in the operating system with a properly configured FIPS module available for loading. Percona Server for MySQL will load this module and run in FIPS mode.
        ```



