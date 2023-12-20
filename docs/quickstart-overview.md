# Overview

Percona Server for MySQL is a freely available, fully compatible, enhanced, and open source drop-in replacement for any MySQL database. Percona Server for MySQL provides enterprise-grade features in security, availability, data management, visibility, instrumentation, and performance. To start with Percona Server for MySQL quickly, we recommend using Docker and this Quickstart guide focuses on this installation method. You can explore alternative installation options in the [Install] section.

Docker lets developers build, deploy, run, update, and manage containers, which isolate applications from the host system. Docker containers are made from Docker images, which are snapshots of the configuration needed to run an application, such as the code and libraries.

??? Information "Reasons for deploying Percona Server in Docker"

    Deploying a Percona Server for MySQL container is an efficient, fast solution to setting up a database quickly without using too many resources. This type of deployment works best for small to medium applications.

    You should deploy a Percona Server for MySQL database in Docker for several reasons. Here are some of them:

    - Portability: Docker containers can run on any platform that supports Docker. This flexibility lets you move your database or installation steps from one platform to another.
    - Isolation: Docker containers are isolated from each other and the host system. This isolation means you can run multiple instances of MySQL on the same machine without interfering with each other or affecting the host's performance. You can also isolate your database from other applications or services that might pose a security risk or consume too many resources.
    - Scalability: Depending on the load and demand, you can scale docker containers up or down. You can use tools like Docker Compose or Kubernetes to orchestrate multiple containers and manage their configuration, networking, and deployment. You can also use Docker Swarm or Amazon ECS to distribute your containers across multiple nodes and achieve high availability and fault tolerance.
    - Versioning: Docker images and containers contain all the dependencies and configurations needed to run your application. You can use tags to specify different versions of your images and easily switch between them. You can also use Docker Hub or other registries to store and share your images with others.
    - Development: Docker containers can help you create a consistent and reproducible development environment that matches your production environment. You can use tools like Dockerfile or Docker Build to automate the creation of your images and ensure they have the same settings and packages as your production images. You can also use tools like Docker Volumes or Bind Mounts to persist and share your data between containers or the host system.

## Purpose of the Quickstart

This document is an introduction to our Percona Server for MySQL server and guides you through the basic steps to create and run a database using a Docker container. These steps describe one way to use Percona Server for MySQL. You can also do the following:

* [Download and install Percona Server for MySQL packages for your operating system](installation.md)

* Work with [the Quickstart for the Percona Operator for MySQL based on the Percona Server for MySQL using Helm] or [the Quickstart for the Percona Operator for MySQL based on the Percona Server for MySQL using Minikube] to find out more about the Percona Operator.

??? information "Percona solutions"

    Percona provides a range of solutions and services for open source databases. Some of the critical solutions offered are the following:

    * Database Distributions: Percona offers enhanced, enterprise-ready versions of popular open source databases, such as MySQL, MongoDB, and PostgreSQL
  
    * Backup Solutions: They provide tools for backing up your databases.

    * Clustering Solutions: Percona offers solutions for setting up and managing database clusters.

    * Observability, Monitoring, and Management Solutions: Percona Monitoring and Management (PMM) is an open source platform for managing and monitoring MySQL, MongoDB, and PostgreSQL performance.

    * Kubernetes Operators: Percona provides Kubernetes operators for automated provisioning and managing databases in Kubernetes.

    These databases are supported across traditional deployments, cloud-based platforms, and hybrid IT environments. Percona’s solutions are designed for peak performance, security, scalability, and availability. They also offer support and services for these databases, ensuring they run faster and more reliably.

You are welcome to name any items to match your organization's standards or use your table structure and data. If you do, the results are different from the expected results. 

For this document, container refers to the Docker container and instance refers to the database server in the container.

## Prerequisites

[Install Docker](https://docs.docker.com/get-docker/) on your system.

## Steps for first-time users

The following steps guide you through a key process for a developer:
{.power-number}

1. [Start and connect to a Docker container](quickstart-docker.md)

2. [Create a database and table](quickstart-database.md)

3. [Run queries](quickstart-queries.md)

4. [Clean up](quickstart-exit.md)

5. [Choose your next steps](quickstart-next-steps.md)

## Next step

[Start and connect to a Docker container :material-arrow-right:](quickstart-docker.md){.md-button}


[the Quickstart for the Percona Operator for MySQL based on the Percona Server for MySQL using Helm]: https://docs.percona.com/percona-operator-for-mysql/ps/helm.html

[the Quickstart for the Percona Operator for MySQL based on the Percona Server for MySQL using Minikube]: https://docs.percona.com/percona-operator-for-mysql/ps/minikube.html

[Install]: installation.md

