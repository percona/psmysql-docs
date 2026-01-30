# Use Docker Compose and named volumes

Docker Compose simplifies managing containerized services. This guide shows how to run Percona Server for MySQL 8.4 with persistent storage for data, logs, and backups using named Docker volumes.

## Benefits

Creating a `docker-compose.yml` file offers numerous advantages for managing containerized applications effectively:

| Benefit                                | Description                                                                                               |
|----------------------------------------|-----------------------------------------------------------------------------------------------------------|
| Simplifies multi-container management  | Define and manage multiple services (containers) in a single configuration file, making it easy to run, stop, and scale your application. |
| Automates dependency handling          | Specify dependencies between services, ensuring containers start in the correct order, such as databases starting before application servers. |
| Enhances portability                   | Share the docker-compose.yml file across environments (development, staging, production) to ensure consistent behavior regardless of system setup. |
| Supports scalability                   | Easily scale services using the docker-compose up --scale command, allowing you to run multiple instances of specific containers. |
| Improves readability                   | Centralizes configuration in a human-readable YAML format, making it easier to understand and modify compared to command-line options. |
| Enables reproducibility                | Store application settings and container configurations in version control to ensure consistent deployments. |
| Allows persistent data                 | Define volumes directly in the file to persist data for services, ensuring storage remains intact even when containers are stopped. |
| Facilitates networking                 | Automatically sets up networks for containers to communicate with each other without requiring manual configuration. |
| Simplifies environment variables management | Integrate .env files to externalize sensitive information like database passwords and access tokens. |
| Reduces errors                         | Avoid repetitive CLI commands by storing configurations in the file, reducing the chance of mistakes during deployment. |


## Directory structure

Docker automatically manages volumes, so you don't create folders manually.

```text
percona-compose/
├── .env
└── docker-compose.yml
```

### Create .env

Using an `.env` file for MySQL Docker containers has several advantages:

| Benefit                         | Description                                                                                               |
|---------------------------------|-----------------------------------------------------------------------------------------------------------|
| Keeps sensitive data secure | Stores environment variables (e.g., passwords) in an `.env` file, keeping them out of `docker-compose.yml` to avoid exposure. |
| Simplifies configuration    | Centralizes environment variables, making it easier to manage and update configurations in one place.     |
| Improves portability        | Enables reuse of variables across different environments (development, staging, production) without changes to configuration files. |
| Enhances readability        | Keeps `docker-compose.yml` or Dockerfiles cleaner by externalizing environment variables.                 |
| Facilitates collaboration   | Allows the use of shared templates (e.g., `.env.example`) for required variables, while hiding actual secrets. |
| Supports dynamic updates    | Makes it easy to update environment variables without modifying Docker configurations or scripts.         |


By leveraging an `.env` file, you streamline both security and ease of use for MySQL container deployments. This approach ensures better organization and adaptability for various environments.

```text
MYSQL_ROOT_PASSWORD=supersecurepassword
MYSQL_DATABASE=mydb
MYSQL_USER=myuser
MYSQL_PASSWORD=myuserpassword
```

### Create docker-compose.yml

By using a `docker-compose.yml` file, you streamline container orchestration, ensure consistency, and simplify collaboration across teams.

```text
services:
  mysql:
    image: percona/percona-server:8.4
    container_name: percona-server
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    volumes:
      - percona-data:/var/lib/mysql              # Database data
      - percona-logs:/var/log/mysql              # MySQL logs
      - percona-backups:/backups                 # XtraBackup output (optional, for future use)
    restart: unless-stopped
volumes:
  percona-data:
  percona-logs:
  percona-backups:
```


## Start the Container

The command has the following options:

* `up`: Starts the containers specified in the docker-compose.yml file.

* `-d`: Runs the containers in detached mode, meaning they operate in the background.

```shell
docker-compose up -d
```

??? example "Expected output"

    ```text
    [+] Running 11/11
     ✔ mysql Pulled                                                                34.1s 
       ✔ 56631da24b0d Pull complete                                                28.9s 
       ✔ 5aee836c3728 Pull complete                                                28.9s 
       ✔ a5fd539367b0 Pull complete                                                28.9s 
       ✔ fc4a4cc146b3 Pull complete                                                28.9s 
       ✔ 7a3939b8d92c Pull complete                                                32.1s 
       ✔ 6fdbd2a9e883 Pull complete                                                32.1s 
       ✔ 70ac4d191dd1 Pull complete                                                32.1s 
       ✔ 5872370b843d Pull complete                                                32.1s 
       ✔ 8310fa1d2765 Pull complete                                                32.1s 
       ✔ 4437564bc659 Pull complete                                                32.2s 
    [+] Running 5/5
     ✔ Network percona-compose_default           Created                            0.0s 
     ✔ Volume "percona-compose_percona-data"     Created                            0.0s 
     ✔ Volume "percona-compose_percona-logs"     Created                            0.0s 
     ✔ Volume "percona-compose_percona-backups"  Created                            0.0s 
     ✔ Container percona-server                  Star...                            0.3s
     ```
            
Docker automatically creates the volumes:

•	percona-data: stores MySQL tables

•	percona-logs: stores logs generated by the database

•	percona-backups: a mount point you can use for Percona XtraBackup

## Connect to the server and run a simple query

After the container is up, you can connect to the running server instance using the mysql client included in the container.

Run the following command to open a MySQL shell in the container:

```shell
docker exec -it percona-server mysql -u root -p
```

You must enter the root password.

??? example "Expected output"

    ```text
    Enter password: 
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 9
    Server version: 8.4.4-4 Percona Server (GPL), Release 32, Revision b8e378ec

    Copyright (c) 2009-2025 Percona LLC and/or its affiliates
    Copyright (c) 2000, 2025, Oracle and/or its affiliates.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    ```

Run a simple query:

```sql
SHOW DATABASES;
```

??? example "Expected output"

    ```text
    +--------------------+
    | Database           |
    +--------------------+
    | information_schema |
    | mydb               |
    | mysql              |
    | performance_schema |
    | sys                |
    +--------------------+
    5 rows in set (0.02 sec) 
    ```

## Create a test database and table

The following query creates a `test_db` database and `test_table`:

```sql
CREATE DATABASE test_db;
USE test_db;
CREATE TABLE test_table (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100));
INSERT INTO test_table (name) VALUES ('Sample Data');
SELECT * FROM test_table;
```

??? example "Expected output"

    ```text
    Query OK, 1 row affected (0.02 sec)

    Database changed
    Query OK, 0 rows affected (0.01 sec)

    Query OK, 1 row affected (0.01 sec)

    +----+-------------+
    | id | name        |
    +----+-------------+
    |  1 | Sample Data |
    +----+-------------+
    1 row in set (0.00 sec)

    ```

Remember to `exit` when you are finished working with the server.

## Use the backup volume with XtraBackup

When you run XtraBackup inside a container, either in the same network or another container, you can target `/backups` to store backup files.

An example of using Docker to backup the server:

```shell
docker run --rm \
  --volumes-from percona-server \
  -v percona_backups:/backup \
  percona/percona-xtrabackup:8.0 \
  xtrabackup --backup \
  --target-dir=/backup \
  --host=percona-server \
  --user=myuser \
  --password=mypassword
```


## Best practices

*	Use named volumes to simplify backup and migration.

* Mount logs separately for easier troubleshooting and rotation.

* Use docker volume inspect to view volume metadata and mount points.


## Shut down and clean up

You can stop the stack but retain volumes:

```shell
docker-compose down
```

You can also remove all resources, including volumes:

```shell
docker-compose down -v
```