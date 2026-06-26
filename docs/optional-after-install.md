# Optional steps after repository install for Percona Server for MySQL {{vers}}

After you install Percona Server for MySQL from a repository, you can enable the testing repository or install Percona Toolkit user-defined functions (UDFs).

* [Use an APT repository to install Percona Server for MySQL {{vers}}](apt-repo.md)

* [Install using DNF](yum-repo.md)

## Install Percona Toolkit UDFs (optional)

User-defined functions (UDFs) add custom functions to MySQL. Percona Server for MySQL includes UDFs from [Percona Toolkit :octicons-link-external-16:](https://docs.percona.com/percona-toolkit/) for data integrity checks and performance monitoring. The UDFs speed up checksum calculations:

| Function | Description |
|---|---|
| `fnv_64` | Fast 64-bit hash function |
| `fnv1a_64` | Variant of `fnv_64` with improved distribution |
| `murmur_hash` | Fast non-cryptographic hash function |

Install Percona Toolkit UDFs after Percona Server packages are installed:

```{.sql data-prompt="mysql>"}
INSTALL COMPONENT 'file://component_percona_udf';
```

??? example "Expected output"

	```{.text .no-copy}
	Query OK, 0 rows affected (0.01 sec)
	```

You can use the UDFs in SQL queries. Example: `SELECT fnv_64('test_string');`

For UDF details, see [Percona Toolkit UDF functions](udf-percona-toolkit.md).

## Install the Percona testing repository

Do not use testing repository builds in production. Testing builds are pre-release versions. They can contain bugs or incomplete features.

Percona offers pre-release builds from the testing repository for advanced users who want to:

* Evaluate upcoming improvements

* Provide feedback on development versions

* Test features before the official release

The testing repository has the following limitations:

* Features can change without notice

* Percona does not provide production support for testing builds

* The repository can contain experimental or incomplete functionality

* The repository can exclude features from the final release

### APT

Enable the testing repository:

```shell
sudo percona-release enable {{pkg}} testing --scheme https
```

Disable the testing repository and return to stable releases:

```shell
sudo percona-release disable testing
sudo apt update
```

### DNF

Enable the testing repository:

```shell
sudo percona-release enable {{pkg}} testing
```

??? example "Expected output"

	```{.text .no-copy}
	* Enabling Percona Server for MySQL {{vers}} testing repository
	* Running dnf update...
	Last metadata expiration check: 0:01:23 ago on Mon Jan 15 10:30:00 2024.
	All packages are up to date.
	```

Disable the testing repository and return to stable releases:

```shell
sudo percona-release disable testing
sudo dnf update
```

??? example "Expected output"

	```{.text .no-copy}
	* Disabling Percona testing repository
	* Running dnf update...
	Last metadata expiration check: 0:01:23 ago on Mon Jan 15 10:30:00 2024.
	All packages are up to date.
	```
