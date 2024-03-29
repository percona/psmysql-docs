# Run Percona Server for MySQL in a Docker container

You are welcome to name any items to match your organization's standards or use your table structure and data. If you do, the results are different from the expected results.

## Prerequisites

* Docker Engine installed and running
* Stable internet connection
* Basic understanding of the command-line interface (CLI)

Always adapt the commands and configurations to your specific environment and security requirements.


## Start a Docker container

To use the "Docker run" command, specify the name or ID of the image you want to use and, optionally, some flags and arguments that modify the container's behavior. The command has the following options:

| Option | Description |
|---|---|
| `-d` | Runs the container in detached mode, allowing the container to operate in the background. |
| `-p 3306:3306` |Maps the container's MySQLport (3306) tothe same port yourhost, enabling external access.|
| `--name psmysql` | Provides a meaningful name to the container. If you do not use this option, Docker adds a random name. |
| `-e MYSQL_ROOT_PASSWORD=secret` | Adds an environmental variable and changes the password from the default password. |
|  `--v myvol:/var/lib/mysql` | Mounts a host directory (myvol) as the container's data volume, ensuring persistent storage for the database between container lifecycles. |
| `percona/percona-server:8.0.34` | The image with the tag (8.0.34) to specify a specific release. |

You must provide at least one environment variable to access the database, such as `MYSQL_ROOT_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_USER`, and `MYSQL_PASSWORD` or the instance refuses to initialize.

If needed, you can replace the `secret` password with a [stronger password](#security-measures).

For this document, we add the `8.0.34` tag. In Docker, a tag is a label assigned to an image and is used to maintain different versions of an image. If we did not add a tag, Docker uses `latest` as the default tag and downloads the latest image from [percona/percona-server on the Docker Hub].

To run the Docker ARM64 version of Percona Server for MySQL, use the `8.0.34-26 1-aarch64` tag instead of `8.0.34`.

```{.bash data-prompt="$"}
$ docker run -d -p 3306:3306 --name psmysql \
-e MYSQL_ROOT_PASSWORD=secret \
-v myvol:/var/lib/mysql \
percona/percona-server:8.0.34
```

??? example "Expected output"

    ```{.text .no-copy}
    Unable to find image 'percona/percona-server:8.0.34' locally
    8.0.34: Pulling from percona/percona-server
    d6f6a69cdebb: Pull complete
    4f8794caafba: Pull complete
    d80629460c71: Pull complete
    f550e519928f: Pull complete
    fb91f65fb039: Pull complete
    e8f7e0c2fbae: Pull complete
    Digest: sha256:4944f9b365e0dc88f41b3b704ff2a02d1459fd07763d7d1a444b263db8498e1f
    Status: Downloaded newer image for percona/percona-server:8.0.34
    01d4f6d188b609ff92158605f8528d640aa28ff5720efa0286b36f51d4bec11c
    ```

## Connect to the database instance

To connect to a MySQL database on a container, use the Docker exec command with the database instance connect command. You must know the name or ID of the container that runs the database server and the database credentials.

The Docker exec command runs a specified command in a running container. The database instance connect command connects to a MySQL server with the user name and password.

For this example, we have the following options:

| Option      | Description                                                                        |
| ----------- | ---------------------------------------------------------------------------------- |
| `it`        | Interact with the container and be a pseudo-terminal                               |
| `psmysql` | Running container name                                                             |
| `mysql`   | Connects to a database instance                                                    |
| `-u`      | Specifies the user account used to connect                                         |
| `-p`      | Use this password when connecting |

You must enter the password when the server prompts you.

Connect to the database instance example

```{.bash data-prompt="$"}
$ docker exec -it psmysql mysql -uroot -p
```

You are prompted to enter the password, which is `secret`. If you have changed the password, use your password. You will not see any characters as you type.

```{.text .no-copy}
Enter password:
```

You should see the following result.

??? example "Expected output"

    ```{.text .no-copy}
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 8
    Server version: 8.0.34-26 Percona Server (GPL), Release 26, Revision 0fe62c85

    Copyright (c) 2009-2023 Percona LLC and/or its affiliates
    Copyright (c) 2000, 2023, Oracle and/or its affiliates.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    mysql>
    ```

## Create a database

??? Example "Benefits and what to watch out for when creating databases and tables"

    Creating a database and table has the following benefits:

    - Store and organize your data in a structured and consistent way.
    - Query and manipulate your data using SQL.
    - Enforce data integrity and security using constraints, triggers, views, roles, and permissions.
    - Optimize your data access and performance using indexes, partitions, caching, and other techniques.

    When you create a table, design your database schema carefully, changing it later may be difficult and costly. You should experiment with concurrency, transactions, locking, isolation, and other issues that may arise when multiple users access the same data. You must backup and restore your data regularly, as data loss or corruption may occur due to hardware failures, human errors, or malicious attacks.

To create a database, use the `CREATE DATABASE` statement. You can optionally specify the character set and collation for the database in the statement. After the database is created, select the database using the `USE` statement or the `-D` option in the MySQL client.

```{.bash data-prompt="mysql>"}
mysql> CREATE DATABASE mydb;
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 1 row affected (0.01 sec)
    ```

```{.bash data-prompt="mysql>"}
mysql> use mydb;
```

??? example "Expected output"

    ```{.text .no-copy}
    Database changed
    ```

## Create a table

Create a table using the `CREATE TABLE` statement. You can specify the values for each column or use the DEFAULT keyword for columns with default values, data types, constraints, indexes, and other options.

```{.bash data-prompt="mysql>"}
mysql> CREATE TABLE `employees` (
    `id` mediumint(8) unsigned NOT NULL auto_increment,
    `name` varchar(255) default NULL,
    `email` varchar(255) default NULL,
    `country` varchar(100) default NULL,
    PRIMARY KEY (`id`)
) AUTO_INCREMENT=1;
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected, 1 warning (0.03 sec)
    ```

## Insert data into the table

Insert data into the table using the `INSERT INTO` SQL statement. This statement adds multiple records into a table in one statement.


```{.bash data-prompt="mysql>"}
mysql> INSERT INTO `employees` (`name`,`email`,`country`)
VALUES
    ("Erasmus Richardson","posuere.cubilia.curae@outlook.net","England"),
    ("Jenna French","rhoncus.donec@hotmail.couk","Canada"),
    ("Alfred Dejesus","interdum@aol.org","Austria"),
    ("Hamilton Puckett","dapibus.quam@outlook.com","Canada"),
    ("Michal Brzezinski","magna@icloud.pl","Poland"),
    ("Zofia Lis","zofial00@hotmail.pl","Poland"),
    ("Aisha Yakubu","ayakubu80@outlook.com","Nigeria"),
    ("Miguel Cardenas","euismod@yahoo.com","Peru"),
    ("Luke Jansen","nibh@hotmail.edu","Netherlands"),
    ("Roger Pettersen","nunc@protonmail.no","Norway");
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 10 rows affected (0.02 sec)
    Records: 10  Duplicates: 0  Warnings: 0
    ```

## Run a SELECT query

SELECT queries retrieve data from one or more tables based on specified criteria. They are the most common type of query and can be used for various purposes, such as displaying, filtering, sorting, aggregating, or joining data. SELECT queries do not modify the data in the database but can affect the performance if the query involves large or complex datasets.



```{.bash data-prompt="mysql>"}
mysql>SELECT id, name, email, country FROM employees WHERE country = 'Poland';
```

??? example "Expected output"

    ```{.text .no-copy}
    +----+-------------------+---------------------+---------+
    | id | name              | email               | country |
    +----+-------------------+---------------------+---------+
    |  5 | Michal Brzezinski | magna@icloud.pl     | Poland  |
    |  6 | Zofia Lis         | zofial00@hotmail.pl | Poland  |
    +----+-------------------+---------------------+---------+
    2 rows in set (0.00 sec)
    ```

## Run an Update query

UPDATE queries modify existing data in a table. They are used to change or correct the information stored in the database. UPDATE queries can update one or more columns and rows simultaneously, depending on the specified conditions. They may also fail if they violate any constraints or rules defined on the table.

 An example of an UPDATE query and then run a [SELECT](#select-query) with a WHERE clause to verify the update.

```{.bash data-prompt="mysql>"}
mysql> UPDATE employees SET name = 'Zofia Niemec' WHERE id = 6;
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 1 row affected (0.01 sec)
    Rows matched: 1  Changed: 1  Warnings: 0
    ```

```{.bash data-prompt="mysql>"}
mysql> SELECT name FROM employees WHERE id = 6;
```

??? example "Expected output"

    ```{.text .no-copy}
    +--------------+
    | name         |
    +--------------+
    | Zofia Niemec |
    +--------------+
    1 row in set (0.00 sec)
    ```

## Run an INSERT query

INSERT queries add new data to a table. They are used to populate the database with new information. INSERT queries can insert one or more rows at a time, depending on the syntax. The query may fail if it violates any constraints or rules defined on the table, such as primary keys, foreign keys, unique indexes, or triggers.

Insert a row into a table and then run a [SELECT](#select-query) with a WHERE clause to verify the record was inserted.

```{.bash data-prompt="mysql>"}
mysql> INSERT INTO `employees` (`name`,`email`,`country`)
VALUES
("Kenzo Sasaki","KenSasaki@outlook.com","Japan");
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 1 row affected (0.01 sec)
    ```

```{.bash data-prompt="mysql>"}
mysql> SELECT id, name, email, country FROM employees WHERE id = 11;
```

??? example "Expected output"

    ```{.text .no-copy}
    +----+--------------+-----------------------+---------+
    | id | name         | email                 | country |
    +----+--------------+-----------------------+---------+
    | 11 | Kenzo Sasaki | KenSasaki@outlook.com | Japan   |
    +----+--------------+-----------------------+---------+
    1 row in set (0.00 sec)
    ```

## Run a Delete query

DELETE queries remove existing data from a table. They are used to clean up the information no longer needed or relevant in the database. The DELETE queries can delete one or more rows at a time, depending on the specified conditions. They may also trigger cascading deletes on related tables if foreign key constraints are enforced.

Delete a row in the table and run a [SELECT](#select-query) with a WHERE clause to verify the deletion.

```{.bash data-prompt="mysql>"}
mysql> DELETE FROM employees WHERE id >= 11;
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 1 row affected (0.01 sec)
    ```

```{.bash data-prompt="mysql>"}
mysql> SELECT id, name, email, country FROM employees WHERE id > 10;
```

??? example "Expected output"

    ```{.text .no-copy}
    Empty set (0.00 sec)
    ```

## Clean up

The following steps do the following:

* Exits the MySQL command client shell and the Docker container

* Removes the Docker container and the Docker image

* Removes the Docker volume.

The steps are as follows:
{.power-number}

1. To exit the MySQL command client shell we use `exit`. You can also use the `\q` or `quit` commands. The execution of the statement also closes the connection.

    * An example of exiting the MySQL command client shell and closing the connection.

        ```{.bash data-prompt="mysql>"}
        mysql> exit
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            Bye
            ```

2. You may want to remove the docker container and the image if they are no longer needed or to free up disk space. To remove a docker container, use the command `docker rm` followed by `psmysql`, the container ID or name. To remove a docker image, use the command `docker rmi` followed by `percona/percona-server:8.0.34`, the image ID or name and the tag. If you are running the ARM64 version of Percona Server, edit the Docker command to use the `8.0.34-26.1-aarch64` tag with `docker image rmi percona/percona-server:8.0.34-26.1-aarch64`

    * An example of removing a Docker container.

        ```{.bash data-prompt="$"}
        $ docker container rm psmysql -f
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            psmysql
            ```
    * An example of removing a Docker image. If running the ARM64 version of Percona Server, edit the Docker command to use the `8.0.34-26.1-aarch64` tag. This edit changes the command to `docker image rmi percona/percona-server:8.0.34-26.1-aarch64`
        ```
        $ docker image rmi percona/percona-server:8.0.34
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            Untagged: percona/percona-server:8.0.34
            Untagged: percona/percona-server@sha256:4944f9b365e0dc88f41b3b704ff2a02d1459fd07763d7d1a444b263db8498e1f
            Deleted: sha256:b2588da614b1f382468fc9f44600863e324067a9cae57c204a30a2105d61d9d9
            Deleted: sha256:1ceaa6dc89e328281b426854a3b00509b5df13826a9618a09e819a830b752ebd
            Deleted: sha256:77471692427a227eb16d06907357956c3bb43f0fdc3ecf6f8937e1acecae24fe
            Deleted: sha256:8db06cc7b0430437edc7f118b139d2195cb65e2e8025f9a4517d16778f615384
            Deleted: sha256:e5a57a2fafec4ab9482240f28927651d56545c19626e344aceb8be3704c3c397
            Deleted: sha256:f86198f39b893674d44d424c958f23183bf919d2ced20e1f519714d0972d75ed
            Deleted: sha256:db9672f7e12e374d5e9016b758a29d5444e8b0fd1246a6f1fc5c2b3c847dddcf
            ```

3. Remove the docker volume if a container does not use the volume and you no longer need it.

    * An example of removing a Docker volume.

        ```{.bash data-prompt="$"}
        $ docker volume rm myvol
        ```

        ??? example "Expected output"

            ```{.text .no-copy}
            myvol
            ```

## Troubleshooting

* Connection Refusal: Ensure Docker is running and the container is active. Verify port 3306 is accessible on the container's IP address.

* Incorrect Credentials: Double-check the root password you set during container launch.

* Data Loss: Always back up your data regularly outside the container volume.

## Security measures

* Strong Passwords: Utilize complex, unique passwords for the root user and any additional accounts created within the container. The alphanumeric password should contain at least 12 characters. The password should include uppercase and lowercase letters, numbers, and symbols.

* Network Restrictions: Limit network access to the container by restricting firewall rules to only authorized IP addresses.

* Periodic Updates: Regularly update the Percona Server image and Docker Engine to mitigate known vulnerabilities.

* Data Encryption: Consider encrypting the data directory within the container volume for an additional layer of security.

* Monitor Logs: Actively monitor container logs for suspicious activity or errors.

Remember, responsible container management and robust security practices are crucial for safeguarding your MySQL deployment. By following these guidelines, you can leverage the benefits of Docker and Percona Server while prioritizing the integrity and security of your data.

## Next step

[Choose your next steps:material-arrow-right:](quickstart-next-steps.md){.md-button}


[Percona Server for MySQL documentation]: https://docs.percona.com/percona-server/8.0/

[percona/percona-server on the Docker Hub]: https://hub.docker.com/r/percona/percona-server
