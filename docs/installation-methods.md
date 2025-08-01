# Installation methods

This guide outlines the primary methods for installing Percona Server for MySQL, comparing their advantages and use cases to help you choose the right approach for your environment.

## APT/YUM or DNF (package managers)

* [Install with APT](apt-repo.md)

* [Install with YUM/DNF](yum-repo.md)

This is the standard and recommended method for most users on a supported Linux distribution. This method uses the Percona release tool with a package manager to handle the installation from a pre-configured repository. The package manager automatically resolves and installs all required dependencies.
  
  * Common Use Cases:
  
    * Production servers where stability and easy maintenance are critical.
  
    * Automated deployments and provisioning.
    
    * Users who want a simple, clean, and reliable installation process.
  
  * Pros:
  
    * Dependency Management: All dependencies are handled automatically.
  
    * Easy Updates: Upgrading to new versions or applying security patches is a single command.
  
    * Reliability: Packages are tested for the specific operating system and architecture.
  
    * Clean Uninstallation: Removes all files without leaving orphaned data.
  
  * Cons:
  
    * Version Availability: You are limited to the versions available in the repository.
    
### Manual Package Installation (.deb/.rpm)

* [Download and install with APT packages](apt-download-deb.md)

* [Download and install with RPM packages](yum-download-rpm.md)



This method is a hybrid approach, offering more control than a repository but still leveraging the package manager for the final installation. It's used when you have the package file but don't want to use an online repository. You download a specific package file (for example, a .deb or .rpm) directly from the Percona website. You then install the package file using a local command-line tool like apt or dnf, which processes the file.

  * Common Use Cases:

    * Installing on a system with no internet access to the public repositories.

    * Deploying a specific point release for testing or compatibility.

    * Troubleshooting when repository access is an issue.

  * Pros:

    * Precise Version Control: You get exactly the version of the package you download.

    * No Repository Required: The server doesn't need to access an online repository.

    * Uses Package Manager: The package file can still manage dependencies and is easy to remove.

  * Cons:

    * Manual Dependencies: You must manually download and install any required dependency packages first.

    * Manual Updates: You have to manually download and install new versions.

    * No Automatic Security Patches: You are responsible for monitoring and installing security updates.

### Tar Files

* [Download and install .tar file](binary-tarball-install.md)

This method gives you more control than a package manager but still provides a pre-compiled binary that does not require compilation. You download a compressed tarball (.tar.gz) containing the pre-compiled binaries directly from the Percona website. You then extract the files to a directory of your choice and manually configure the environment.
  
  * Common Use Cases:
  
    * Installing on unsupported Linux distributions or non-standard environments.
    
    * Testing a specific version that isn't yet available in a repository.
    
    * Installing for Local development.
  
  * Pros:
  
    * Flexibility: Provides the latest versions directly from the source.
    
    * Portability: The installation is often self-contained within a directory.
    
    * Control: You decide exactly where to install the files.
  
  * Cons:
  
    * Manual Dependencies: You are responsible for manually installing any required libraries.
    
    * Manual Maintenance: Updating to a new version requires you to download, extract, and re-link the new files.

## Compile from source

* [Compile from source](compile-percona-server.md)

This is the most hands-on method, offering the highest level of customization and control over the final installation. You download the raw source code, use a C++ compiler and other tools to build the software on your local machine, and then install the resulting binaries. This method requires a comprehensive build environment.
  
  * Common Use Cases:
  
    * Building for an unsupported architecture.
    
    * Debugging or modifying the server's code.
    
    * Optimizing the server for a specific hardware configuration.
  
  * Pros:
  
    * Ultimate Control: You can customize every aspect of the build, including which features to enable or disable.
    
    * Platform Flexibility: Can be compiled and run on virtually any system that has the required build tools.
  
  * Cons:
  
    * Complex Dependencies: Requires you to manually manage all build-time dependencies, which can be extensive.
    
    * Time-Consuming: The compilation process can take a significant amount of time.
    
    * Difficult Maintenance: Updating or uninstalling requires manual, complex steps.