# Install Percona Server for MySQL from Percona RPM repository

<!-- package name: percona-server-server-8.0.13-3.1.el7.x86_64.rpm -->
Ready-to-use packages are available from the Percona Server for MySQL software
repositories and the [download page](http://www.percona.com/downloads/Percona-Server-8.0/). The
Percona yum repository supports popular RPM-based
operating systems. The easiest way to install the Percona RPM repository is to install an RPM
that configures yum and installs the [Percona GPG key](https://www.percona.com/downloads/RPM-GPG-KEY-percona).

Specific information on the supported platforms, products, and versions are described in [Percona Software and Platform Lifecycle](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql).

Percona Server for MySQL is certified for Red Hat Enterprise Linux 8. This certification is based on common and secure best practices and successful interoperability with the operating system. Percona Server is listed in the [Red Hat Ecosystem Catalog](https://catalog.redhat.com/software/applications/detail/5869161).

!!! note

    The RPM packages for Red Hat Enterprise Linux 7 and the compatible derivatives do not support TLSv1.3, as it requires OpenSSL 1.1.1, which is currently not available on this platform.



You can install Percona yum repository by running the following commands as a `root` user or with sudo.


1. Install the Percona repository

	```shell
	$ sudo yum install https://repo.percona.com/yum/percona-release-latest.noarch.rpm
	```
	
	??? example "Expected output"
	
	    ```text
	    percona-release-latest.noarch-rpm               36 kB/s | 19 kb 00:00
	    =====================================================================
	      Package         Architecture      Version    Repository    Size
	    =====================================================================
	    Installing:
	       percona release noarch         1.0-25     @commandline  19k
	    ...
	    ```
    
2. Enable the repository:

	```shell
	$ sudo percona-release setup ps80
	```
	
	If you see the following message, enter 'y' to disable the mysql module:
	
	```text
	On RedHat 8 systems it is needed to disable dnf mysql module to install Percona-Server
	Do you want to disable it? [y/N] 
	...
	```


3. Install the packages:

	```shell
	$ sudo yum install percona-server-server
	```
	{% include './snippets/install/_storage-engines.md'%}

### Percona yum Testing repository

Percona offers pre-release builds from our testing repository. To
subscribe to the testing repository, you enable the testing
repository in `/etc/yum.repos.d/percona-release.repo`. To do so,
set both `percona-testing-$basearch` and `percona-testing-noarch`
to `enabled = 1` (Note that there are three sections in this file:
release, testing, and experimental - in this case, it is the second section that requires updating).

!!! note

    You must install the Percona repository first if the installation has not been done already.
