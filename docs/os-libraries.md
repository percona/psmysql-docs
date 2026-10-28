# Operating system libraries

Percona Server for MySQL loads shared libraries from the operating system. The generic binary tarball bundles many of those libraries. The DEB and RPM packages link the operating system copies instead, and `apt` or `dnf` installs them.

Install the libraries on this page before you start the server. Use the row for the tarball or package you installed.

## Generic binary tarball

`bin/mysqld` loads bundled libraries from `lib/private`. The glibc 2.35 tarball bundles `libaio` and `libnuma`. It does not bundle OpenSSL.

The [binary tarball file names](binary-tarball-names.md) page lists the operating system each tarball was built on. That build selects the shared library file names. A tarball built against OpenSSL 1.1 looks for `libssl.so.1.1`. The glibc 2.35 tarball looks for `libssl.so.3`.

### Libraries the server needs to start

These libraries are not in the glibc 2.35 tarball. Install them before you run `bin/mysqld`. `libstdc++6` and `libgcc-s1` are part of a normal Ubuntu installation.

| Library | Needed by | Ubuntu 22.04 | Ubuntu 24.04 and 26.04 | RHEL 9 |
|---------|-----------|--------------|------------------------|--------|
| `libssl.so.3` and `libcrypto.so.3` | `bin/mysqld` and the client programs | `libssl3` | `libssl3t64` | `openssl-libs` |
| `libstdc++.so.6` | `bin/mysqld` and the client programs | `libstdc++6` | `libstdc++6` | `libstdc++` |
| `libgcc_s.so.1` | `bin/mysqld` and the client programs | `libgcc-s1` | `libgcc-s1` | `libgcc` |

RHEL 8 provides `libssl.so.1.1`, not `libssl.so.3`. On RHEL 8, use the glibc 2.28 tarball.

On Ubuntu 26.04, install the OpenSSL package with this command:

```
sudo apt install libssl3t64
```

### Libraries for optional features

Install a package in this table only when you use the feature. These file names are the ones the glibc 2.35 tarball loads.

| Feature | Library | Ubuntu 22.04 | Ubuntu 24.04 and 26.04 | RHEL 9 |
|---------|---------|--------------|------------------------|--------|
| UUID_VX component | `libatomic.so.1` | `libatomic1` | `libatomic1` | `libatomic` |
| OpenID Connect authentication | `libcurl.so.4` | `libcurl4` | `libcurl4t64` | `libcurl` |
| LDAP authentication | `libldap-2.5.so.0` and `liblber-2.5.so.0` | `libldap-2.5-0` | No package provides this file name | No package provides this file name |
| LDAP SASL client | `libsasl2.so.2` | `libsasl2-2` | `libsasl2-2` | No package provides this file name |
| Group Replication | `libtirpc.so.3` | `libtirpc3` | `libtirpc3t64` | `libtirpc` |
| PAM authentication | `libpam.so.0` | `libpam0g` | `libpam0g` | `pam` |
| Kerberos authentication | `libcom_err.so.2`, `libk5crypto.so.3`, `libkeyutils.so.1`, and `libkrb5support.so.0` | `libcom-err2`, `libk5crypto3`, `libkeyutils1`, and `libkrb5support0` | `libcom-err2`, `libk5crypto3`, `libkeyutils1`, and `libkrb5support0` | `libcom_err`, `krb5-libs`, and `keyutils-libs` |
| WebAuthn authentication | `libudev.so.1` | `libudev1` | `libudev1` | `systemd-libs` |

Ubuntu 24.04, Ubuntu 26.04, and RHEL 9 ship `libldap.so.2`. The glibc 2.35 LDAP plugins look for `libldap-2.5.so.0`. Installing `libldap2` or `openldap` does not satisfy that lookup. RHEL provides `libsasl2.so.3`. The LDAP SASL client plugin looks for `libsasl2.so.2`.

On Ubuntu, install a package from the table with this command. Replace `<package>` with the package name:

```
sudo apt install <package>
```

On RHEL, use this command:

```
sudo dnf install <package>
```

### Tarballs built against OpenSSL 1.1

The glibc 2.28 and glibc 2.31 tarballs link OpenSSL 1.1 and OpenLDAP 2.4. On Ubuntu 22.04, `ldd` reports these files as not found:

| Library | Needed by | Package that provides the file |
|---------|-----------|--------------------------------|
| `libssl.so.1.1` and `libcrypto.so.1.1` | `bin/mysqld` | `libssl1.1` on Ubuntu 20.04. `openssl-libs` on RHEL 8. Ubuntu 22.04 and later do not ship this file. |
| `libasn1.so.8` | LDAP authentication plugins, through the bundled `libgssapi.so.3` and `libldap_r-2.4.so.2` libraries | `libasn1-8-heimdal` on Ubuntu |
| `libatomic.so.1` | UUID_VX component | `libatomic1` on Ubuntu. `libatomic` on RHEL. |

Use the glibc 2.35 tarball on Ubuntu 22.04 and later so the server loads `libssl.so.3`.

## DEB and RPM packages

The `percona-server-server` package links the operating system libraries in the following table. It does not use the libraries bundled in the generic tarball. `apt` and `dnf` install these packages when you install the server. Install them yourself only when you install downloaded packages with `dpkg` or `rpm`. Those tools do not resolve dependencies. See [Downloaded DEB packages](apt-download-deb.md) and [Downloaded RPM packages](yum-download-rpm.md).

| Library | Ubuntu 22.04 | Ubuntu 24.04 and 26.04 | RHEL 8 | RHEL 9 |
|---------|--------------|------------------------|--------|--------|
| `libaio.so.1` | `libaio1` | `libaio1t64` | `libaio` | `libaio` |
| `libatomic.so.1` | `libatomic1` | `libatomic1` | `libatomic` | `libatomic` |
| `libcurl.so.4` | `libcurl4` | `libcurl4t64` | `libcurl` | `libcurl` |
| MeCab | `libmecab2` | `libmecab2` | Not required by the RPM | Not required by the RPM |
| `libnuma.so.1` | `libnuma1` | `libnuma1` | `numactl-libs` | `numactl-libs` |
| `libpam.so.0` | `libpam0g` | `libpam0g` | `pam` | `pam` |
| SASL | `libsasl2-2` | `libsasl2-2` | `cyrus-sasl-lib` | `cyrus-sasl-lib` |
| OpenSSL | `libssl3` | `libssl3t64` | `openssl-libs` | `openssl-libs` |
| `libtirpc.so.3` | `libtirpc3` | `libtirpc3t64` | `libtirpc` | `libtirpc` |
| LDAP | `libldap-2.5-0` | `libldap2` | `openldap` | `openldap` |
| Kerberos | `libkrb5-3` | `libkrb5-3` | `krb5-libs` | `krb5-libs` |
| FIDO | `libfido2-1` | `libfido2-1` | Not required by the RPM | Not required by the RPM |

On Ubuntu 24.04 and later, `libaio1t64` provides `libaio.so.1t64`. The DEB package for those releases is built against that file name. The generic tarball bundles its own `libaio` and does not load `libaio.so.1`.
