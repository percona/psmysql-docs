# Run Percona Server for MySQL with Docker Compose

You are welcome to name any items to match your organization’s standards or use your table structure and data. However, if you do, the results are different from the expected results.

??? example "Docker Compose benefits"

    Using a Docker Compose file offers several significant benefits for managing multi-container Docker applications.
    
    One key advantage is the simplified management of multi-container applications. A single `docker-compose.yml` file defines all the services, networks, and volumes your application requires. With a single command (`docker-compose up`), you can start and manage the entire stack rather than individually managing each container. This streamlines development, testing, and deployment workflows.
    
    Docker Compose also provides declarative configuration. You define your application's desired state in the `docker-compose.yml` file, and Docker Compose ensures that the Docker environment matches this configuration. This declarative approach makes understanding and reproducing your application’s setup easier.
    
    Furthermore, it enables service dependencies and linking. You can explicitly define dependencies between services in the Compose file. For example, you can specify that your web application service depends on the database service. Docker Compose ensures that dependencies are started in the correct order. Services can also easily communicate with each other using their service names as hostnames within the Docker network created by Compose.
    
    Another benefit is volume and network management. Docker Compose allows you to define and manage volumes for persistent data and networks for inter-container communication within the Compose file. This ability simplifies the creation and management of these essential Docker resources.
    
    Finally, Docker Compose promotes reproducibility and portability. The `docker-compose.yml` file is a blueprint for your application's environment. As long as Docker and Docker Compose are installed, you can easily spin up the same application stack on different machines or environments, ensuring consistency across development, testing, and production. This ability makes collaboration and deployment significantly easier.

## Prerequisites

* Docker Engine 24.0 or later

* Docker Compose v2.0 or later

* 2GB RAM minimum

* 10GB free disk space

* Internet connection

## Create a directory

These commands create a directory and then navigate into the directory.

These commands create a directory called `my-percona-server`  and then change the location to that directory. Any new files or folders you make will go into `my-percona-server`.

**Try this now:** Copy and paste the code into your terminal and execute it.

```{.bash data-prompt="$"}
$ mkdir my-percona-server
$ cd my-percona-server
``` 


## Add a docker-compose.yml file

These options define the Docker Compose setup's services, resources, and configuration.

* Defining a single service named `mysql`.

* Specifying the Docker image `percona/percona-server:8.0` to use for the `mysql` container.

* Explicitly naming the Docker container `percona-mysql`.

* Setting environment variables within the `mysql` container for configuration:

    * Using the value of the `MYSQL_ROOT_PASSWORD` environment variable for the MySQL root password.

    * Using the value of the `MYSQL_DATABASE` environment variable for the initial database name.

    * Using the value of the `MYSQL_USER` environment variable for a new MySQL user.

    * Using the value of the `MYSQL_PASSWORD` environment variable for the new MySQL user's password.

* Mapping the host port specified by `MYSQL_PORT` to port `3306` inside the `mysql` container.

* Create a named volume `mysql_data` and mount it to `/var/lib/mysql` inside the container for persistent data storage.

* Defining a top-level `volumes` section for named volumes.

* Defining a named volume called `mysql_data`.

* Specifying the `local` Docker volume driver for the `mysql_data` volume.

```yaml
services:                                                                       
  mysql:                                                                        
  image: percona/percona-server:8.0                                           
  container_name: percona-mysql                                               
  environment:                                                               
    - MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}                              
    - MYSQL_DATABASE=${MYSQL_DATABASE}                                        
    - MYSQL_USER=${MYSQL_USER}                                                
    - MYSQL_PASSWORD=${MYSQL_PASSWORD}                                        
  ports:                                                                     
    - "${MYSQL_PORT}:3306"                                                    
  volumes:                                                                    
    - mysql_data:/var/lib/mysql  
    
volumes:                                                                          mysql_data:                                                                   
    driver: local   
```

## Environmental variables with Docker Compose

Placing an `.env` file in the same directory as your `docker-compose.yml` file offers several advantages for managing your Dockerized application's configuration. Docker Compose automatically detects and loads environment variables defined in this `.env` file.

??? example ".env file benefits"

    One key benefit is centralized configuration. You keep environment-specific settings, such as database credentials, API keys, and port numbers, in a single, easily manageable file. This separation of configuration from your `docker-compose.yml` makes your Compose file more generic and reusable across different environments (development, testing, production).
    
    Another advantage is improved security. By storing sensitive information in an `.env` file, you avoid hardcoding these values directly into your `docker-compose.yml` or Dockerfile. This reduces the risk of accidentally exposing sensitive data in version control systems. You typically add the `.env` file to your `.gitignore` to prevent accidental commits.
    
    Furthermore, using an `.env` file enhances readability and maintainability. Your `docker-compose.yml` file becomes cleaner as it references environment variables instead of containing raw configuration values. This ability makes understanding the services and their dependencies easier without being cluttered by specific settings. When configuration changes are needed, you modify only the `.env` file, simplifying updates.
    
    Finally, this approach promotes environment-specific overrides. You can have different `.env` files for various environments (for example, `.env.development`, `.env.test`, `.env.production`). You can easily switch configurations without altering your Compose file by copying the appropriate `.env` file to `.env` before running `docker-compose up`. This ability streamlines the deployment process across various stages of your application's lifecycle.

Here is a definition for each of the environment variables listed in the .env file:

| Environment Variable | Description |
|----------------------|-------------|
| `MYSQL_ROOT_PASSWORD` | Sets the root user's password for the MySQL server. The root user has full privileges. Replace the default with a strong password in production. |
| `MYSQL_DATABASE`      | Specifies the name of the default database created on startup (e.g., `myapp`). Applications use it to store and retrieve data. |
| `MYSQL_USER`          | Creates a new MySQL user (e.g., `appuser`). Grant this user specific privileges based on your needs. |
| `MYSQL_PASSWORD`      | Sets the password for `MYSQL_USER`. Replace the default with a secure value to protect access. |
| `MYSQL_PORT`          | Defines the port MySQL listens on (default is `3306`). Change it if needed for security or conflicts. |

```ini
# MySQL environment variables                                                   
MYSQL_ROOT_PASSWORD=change_this_root_password                                   
MYSQL_DATABASE=myapp                                                            
MYSQL_USER=appuser                                                              
MYSQL_PASSWORD=change_this_user_password                                        
MYSQL_PORT=3306    
```


## Validate the docker-compose.yml file

This command validates the syntax and configuration of your `docker-compose.yml` file.

* Executing the `docker-compose config` command.

If your `docker-compose.yml` file is correctly formatted and all options are valid, this command will output the resolved configuration of your services, volumes, and networks. This output represents the final configuration that Docker Compose will use when you run ```docker-compose up```. 

If your `docker-compose.yml` file contains syntax errors or invalid options, the command will instead output error messages indicating the location and nature of the problems, allowing you to correct them before attempting to start your containers.

**Try this now:** Navigate to the directory containing your `docker-compose.yml` file in your terminal and run the following command:

```{.bash data-prompt="$"}
docker-compose config
```

??? example "Expected output"

    ```{.text .no-copy}
    name: percona-mysql
    services:
      mysql:
        container_name: percona-mysql
        environment:
          MYSQL_DATABASE: myapp
          MYSQL_PASSWORD: change_this_user_password
          MYSQL_ROOT_PASSWORD: change_this_root_password
          MYSQL_USER: appuser
        image: percona/percona-server:8.0
        networks:
          default: null
        ports:
          - mode: ingress
            target: 3306
            published: "3306"
            protocol: tcp
        volumes:
          - type: volume
            source: mysql_data
            target: /var/lib/mysql
            volume: {}
    networks:
      default:
        name: percona-mysql_default
    volumes:
      mysql_data:
        name: percona-mysql_mysql_data
        driver: local
    ```
    
## Start the container

This command starts the containers defined in your `docker-compose.yml` file in detached mode.

* Executing the `docker-compose up -d` command.

Running this command instructs Docker Compose to create and start the services defined in your `docker-compose.yml` file. The `-d` flag signifies "detached" mode, which means the containers will run in the background, freeing up your terminal. 

Docker Compose will first pull any necessary images if they are not already present locally, create the containers, configure networks and volumes, and start the services. You can then interact with your application while the containers run in the background.

**Try this now:** Ensure you are in the same directory as your `docker-compose.yml` file in your terminal and run the following command:


```{.bash data-prompt="$"}
docker-compose up -d
```

??? example "Expected output"

    ```{.text .no-copy}
    [+] Running 11/11
     ✔ mysql Pulled                                                               32.3s 
       ✔ 56631da24b0d Pull complete                                                7.5s 
       ✔ 5aee836c3728 Pull complete                                                7.6s 
       ✔ a5fd539367b0 Pull complete                                                7.6s 
       ✔ fc4a4cc146b3 Pull complete                                                8.6s 
       ✔ 7a3939b8d92c Pull complete                                               30.5s 
       ✔ 6fdbd2a9e883 Pull complete                                               30.5s 
       ✔ 70ac4d191dd1 Pull complete                                               30.5s 
       ✔ 5872370b843d Pull complete                                               30.5s 
       ✔ 8310fa1d2765 Pull complete                                               30.5s 
       ✔ 4437564bc659 Pull complete                                               30.6s 
    [+] Running 3/3
     ✔ Network percona-mysql_default      Creat...                                 0.0s 
     ✔ Volume "percona-mysql_mysql_data"  C...                                     0.0s 
     ✔ Container percona-mysql            Started                                  0.3s 
    ```
     
## Connect to the database

This command executes the `mysql` client command-line tool inside the running `mysql` container, allowing you to interact with the database as the `appuser`.

* Executing the `docker compose exec mysql mysql` command to run a command within the `mysql` service container.

* Specifying the user as `appuser` using the `-u` flag.

* Specifying the password as `myapp` using the `-p` flag. Note that this way of providing the password on the command line is generally discouraged for security reasons in production environments.

After you enter the correct password (which you defined in your `.env` file as the value for `MYSQL_PASSWORD`), you will be connected to the MySQL server running inside the `percona-mysql` container as the appuser. You will then see the MySQL command prompt (`mysql>`), allowing you to execute SQL queries against the `myapp` database (which was defined by the `MYSQL_DATABASE` environment variable).

**Try this now:** If your `percona-mysql` container is running (started with `docker-compose up -d`), copy and paste the following command into your terminal and press Enter. You will then be prompted to enter the password for the `appuser`.


```{.bash data-prompt="$"}
docker compose exec mysql mysql -u appuser -p myapp
Enter password:
```

??? example "Expected output"

    ```{.text .no-copy}
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 14
    Server version: 8.0.41-32 Percona Server (GPL), Release 32, Revision b8e378ec
    
    Copyright (c) 2009-2025 Percona LLC and/or its affiliates
    Copyright (c) 2000, 2025, Oracle and/or its affiliates.
    
    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.
    
    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
    
    mysql>
    ```

## Determine the Current Database

This section demonstrates how to identify the database currently selected within your MySQL session using a simple SQL query.

```{.bash data-prompt="mysql>"}
mysql> SELECT DATABASE();
```

??? example "Expected output"

    ```{.text .no-copy}
    +------------+
    | DATABASE() |
    +------------+
    | myapp      |
    +------------+
    1 row in set (0.00 sec)
    
    mysql>
    ```
  
## Create the employees table

The `CREATE TABLE` statement defines a new table named `employees` in the current database. This table includes several columns to store information about employees.

The first column is `id`, which stores integer values. The `AUTO_INCREMENT` attribute ensures that each new row automatically receives a unique, incrementing integer value for this column. The `PRIMARY KEY` constraint indicates that this column uniquely identifies each record in the `employees` table and does not allow null values.

The next two columns, `first_name` and `last_name`, store strings of up to 50 characters. The `NOT NULL` constraint specifies that these columns must have a value for every row; they cannot be left empty.

The `department` column stores strings of up to 50 characters and holds the employee's department. This column allows null values.

The `salary` column stores decimal numbers. The `DECIMAL(10,2)` data type indicates that this column can store numbers with 10 digits, with two digits after the decimal point.

Finally, the `hire_date` column stores date values, representing the employee's hire date.

```{.bash data-prompt="mysql>"}
mysql> CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    department VARCHAR(50),
    salary DECIMAL(10,2),
    hire_date DATE
);
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.03 sec)
    
    mysql>
    ```

## Basic queries

### Insert operations

The `INSERT INTO` statement adds a new row of data to the `employees` table.

* Specifying the `employees` table as the target for the insertion.

* Listing the columns for the new data: `first_name`, `last_name`, `department`, `salary`, and `hire_date`.

* Providing the values for the new row in the order of the listed columns: `'John'`, `'Smith'`, `'Engineering'`, `75000.00`, and `'2024-01-15'`.

**Try this now:** Copy and paste the code into your SQL editor and execute it.

```{.bash data-prompt="mysql>"}
mysql> 
INSERT INTO employees (first_name, last_name, department, salary, hire_date)
VALUES ('John', 'Smith', 'Engineering', 75000.00, '2024-01-15');
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 1 row affected (0.01 sec)
    ```

This query shows all information about the employee record you just created.
The query works by:

* Getting all employee data (`SELECT *` where the asterisk (*) means "select all columns")

* Looking only for the most recently added record (using `WHERE id = LAST_INSERT_ID()`)

`LAST_INSERT_ID()` is a special MySQL function that finds the ID of the last record you inserted

The query results will show you the complete record of the employee you just added, including any automatically generated fields like the ID.

This function only works if your employee table has an auto-increment ID column and you've just performed an INSERT operation in the same session.

**Try it now:** Copy and paste this code into your SQL editor and execute it immediately after adding a new employee.

```{.bash data-prompt="mysql>"}
mysql> SELECT * FROM employees WHERE id = LAST_INSERT_ID();
```


??? example "Expected output"

    ```{.text .no-copy}
    +----+-----------+-----------+-------------+---------+------------+
    | id | first_name| last_name | department  | salary  | hire_date  |
    +----+-----------+-----------+-------------+---------+------------+
    |  1 | John      | Smith     | Engineering | 75000.00| 2024-01-15|
    +----+-----------+-----------+-------------+---------+------------+
    1 row in set (0.00 sec)
    ```

This query adds several new employees to your database in a single operation.
The query works by:

* Specifying which table to add data to (`INSERT INTO employees`)

* Listing which columns will receive data (`first_name, last_name, department, salary, hire_date`)

* Providing the values for each new employee record (`VALUES` followed by data sets in parentheses).

To add your employees instead, replace the values inside each set of parentheses with your employee information. You can add as many employees as needed by adding more values, separated by commas.

The date format uses `YYYY-MM-DD` (Year-Month-Day), which is the standard SQL date format regardless of your country's date conventions.

**Try it now:** Copy and paste this code into your SQL editor and execute it to add these three employees simultaneously.

```{.bash data-prompt="mysql>"}
mysql> INSERT INTO employees (first_name, last_name, department, salary, hire_date) VALUES 
  ('Sarah', 'Johnson', 'Marketing', 65000.00, '2024-02-01'),
  ('Michael', 'Brown', 'Engineering', 78000.00, '2024-01-20'),
  ('Lisa', 'Davis', 'HR', 62000.00, '2024-03-10');
```



??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 3 rows affected (0.01 sec)
    Records: 3  Duplicates: 0  Warnings: 0
    ```

This query gets all information about employees hired after a specific date and sorts them chronologically.
The query works by:

* Getting all employee data (`SELECT *` where the asterisk (*) means "select all columns")

* Adding a filter that only returns employees hired on or after February 1, 2024 (using `WHERE hire_date >= '2024-02-01'`)

* Sorting results by hire date from earliest to most recent (using `ORDER BY hire_date`)

To change the date, simply replace '2024-02-01' with your desired cutoff date using the `YYYY-MM-DD` format (Year-Month-Day, like '2024-03-15' for March 15, 2024).

SQL databases use the `YYYY-MM-DD` format regardless of your country's date format. This international standard avoids confusion between different formats (such as `MM/DD/YYYY` or `DD/MM/YYYY`).

**Try it now:** Copy and paste this code into your SQL editor and execute it to see immediate results. 

```{.bash data-prompt="mysql>"}
mysql> SELECT * FROM employees 
WHERE hire_date >= '2024-02-01' 
ORDER BY hire_date;
```

??? example "Expected output"

    ```{.text .no-copy}
    +----+------------+-----------+------------+----------+------------+
    | id | first_name | last_name | department | salary   | hire_date  |
    +----+------------+-----------+------------+----------+------------+
    |  2 | Sarah      | Johnson   | Marketing  | 65000.00 | 2024-02-01 |
    |  4 | Lisa       | Davis     | HR         | 62000.00 | 2024-03-10 |
    +----+------------+-----------+------------+----------+------------+
    2 rows in set (0.00 sec)
    ```

The `SELECT COUNT(*)` statement determines the total number of records in the `employees` table.

* Counting all rows within the `employees` table using the `COUNT(*)` function.

* Assigning the alias `total_employees` to the resulting count for clarity in the output.

Executing this command returns a single row with one column labeled total_employees. The value in this column represents the total number of employees currently stored in the employees table.

**Try this now:** Copy and paste the code into your SQL editor and execute it.

```{.bash data-prompt="mysql>"}
mysql> SELECT COUNT(*) as total_employees FROM employees;
```


??? example "Expected output"

    ```{.text .no-copy}
    +-----------------+
    | total_employees |
    +-----------------+
    |               4 |
    +-----------------+
    1 row in set (0.01 sec)
    ```

### Update operations   
   
The `UPDATE employees` statement changes information in the `employees` table.

* Specifying the `employees` table as the one to modify.

* Setting the `salary` column to the value `80000.00`.

* Filtering the update only the row where the `id` column equals `1`.

Running this command modifies the record for the employee with an ID of `1`. The salary is updated to 80000.00. You will see a confirmation indicates the change.

**Try this now:** Copy and paste the code into your SQL editor and execute it.


```{.bash data-prompt="mysql>"}
mysql> UPDATE employees 
SET salary = 80000.00 
WHERE id = 1;
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 1 row affected (0.01 sec)
    Records: 1  Changed: 1  Warnings: 0
    ```

The `SELECT` statement retrieves specific details for an employee from the `employees` table.

* Selecting the `id`, `first_name`, `last_name`, and `salary` columns.

* Specifying the `employees` table as the source of the data.

* Filtering the results to show only the employee where the `id` equals `1`.

This command displays the `id`, `first_name`, l`ast_name`, and the updated `salary` for the employee with an id of `1`. You can verify the changes made by the previous `UPDATE` statement.

**Try this now:** Copy and paste the code into your SQL editor and execute it.

```{.bash data-prompt="mysql>"}
mysql> SELECT id, first_name, last_name, salary 
FROM employees 
WHERE id = 1;
```

??? example "Expected output"

    ```{.text .no-copy}
    +----+------------+-----------+----------+
    | id | first_name | last_name | salary   |
    +----+------------+-----------+----------+
    |  1 | John       | Smith     | 80000.00 |
    +----+------------+-----------+----------+
    1 row in set (0.00 sec)
    ```

The `UPDATE employees` statement modifies the employees' salaries in the 'Engineering' department.

* Specifying the `employees` table as the one to update.

* Setting the `salary` column to its current value multiplied by `1.05`, effectively increasing it by 5%.

* Filtering the update to affect only the rows where the `department` column equals `'Engineering'`.

Running this query increases the salary of all employees in the 'Engineering' department by 5%. You will see a confirmation indicating the number of rows you changed.

**Try this now:** Copy and paste the code into your SQL editor and execute it.

```{.bash data-prompt="mysql>"} 
mysql> UPDATE employees 
SET salary = salary * 1.05 
WHERE department = 'Engineering';
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 2 rows affected (0.00 sec)
    Rows matched: 2  Changed: 2  Warnings: 0
    ```
    The `SELECT` statement retrieves specific details for employees in the 'Engineering' department.
    
    * Selecting the `id`, `first_name`, `last_name`, `department`, and `salary` columns.
    
    * Specifying the `employees` table as the source of the data.
    
    * Filtering the results to show only the employees if the `department` is equal to `'Engineering'`.
    
    This command displays the `id`, `first_name`, `last_name`, `department`, and the updated `salary` for all employees in the 'Engineering' department. 
    
    **Try this now:** Copy and paste the code into your SQL editor and execute it.


```{.bash data-prompt="mysql>"} 
mysql> SELECT id, first_name, last_name, department, salary 
FROM employees 
WHERE department = 'Engineering';
```

??? example "Expected output"

    ```{.text .no-copy}
    +----+------------+-----------+-------------+----------+
    | id | first_name | last_name | department  | salary   |
    +----+------------+-----------+-------------+----------+
    |  1 | John       | Smith     | Engineering | 84000.00 |
    |  3 | Michael    | Brown     | Engineering | 81900.00 |
    +----+------------+-----------+-------------+----------+
    2 rows in set (0.00 sec)
    ```

The `SELECT` statement calculates the average salary for each department in the `employees` table.

* Selecting the `department` column.

* Calculating the average of the `salary` column using the `AVG()` function and assigning the alias `avg_salary` to the result.

* Grouping the rows by the `department` column using the `GROUP BY` clause. This grouping ensures that the average salary is calculated separately for each unique department.

Executing this command returns a table showing each distinct department in the employees table and the corresponding average salary for the employees within that department.

**Try this now:** Copy and paste the code into your SQL editor and execute it.

```{.bash data-prompt="mysql>"} 
mysql> SELECT department, 
       AVG(salary) as avg_salary 
FROM employees 
GROUP BY department;
```
    
??? example "Expected output"

    ```{.text .no-copy}
    +-------------+--------------+
    | department  | avg_salary   |
    +-------------+--------------+
    | Engineering | 82950.000000 |
    | Marketing   | 65000.000000 |
    | HR          | 62000.000000 |
    +-------------+--------------+
    3 rows in set (0.00 sec)
    ```    
    
### Delete operations

If you delete a record using these queries, you cannot retrieve that record without specific rollback mechanisms in place. Exercise caution when using the `DELETE` statement.

Most database systems are designed with rollback mechanisms and archives. These mechanisms change how you delete a record. The deleted record is often not entirely removed from the database. Instead, it is removed from the active data set but stored in a different table, which is an archive. This non-removal allows for potential recovery of the data if needed. Always check your database's documentation to understand how it handles deletions and whether rollback options are available.

The `DELETE FROM` statement removes a specific record from the `employees` table.

* Specifying the `employees` table as the target for deletion.

* Filtering the deletion only affects the row where the `id` column equals `4`.

Running this command removes the employee record with an id of `4` from the employees table. You will see a confirmation that one row has been affected.

**Try this now:** Copy and paste the code into your SQL editor and execute it.

```{.bash data-prompt="mysql>"} 
mysql> DELETE FROM employees 
WHERE id = 4;
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 1 row affected (0.00 sec)
    ```

The `SELECT * FROM employees` statement attempts to retrieve all columns for a specific employee from the `employees` table.

* Selecting all columns (`*`) from the `employees` table.

* Filtering the results to show only the employee where the `id` is equal to `4`.

Executing this command returns an empty set. This result is because the employee record with an id of `4` was previously removed from the table using the `DELETE` statement. Once you delete a record, that record is no longer available in the table for querying.

**Try this now:** Copy and paste the code into your SQL editor and execute it.

```{.bash data-prompt="mysql>"} 
mysql> SELECT * FROM employees WHERE id = 4;
```

??? example "Expected output"

    ```{.text .no-copy}
    Empty set (0.00 sec)
    ```

The `SELECT COUNT(*)` statement determines the current total number of records in the `employees` table.

* Counting all rows within the `employees` table using the `COUNT(*)` function.

* Assigning the alias `remaining_employees` to the resulting count for clarity in the output.

Executing this command returns a single row with one column labeled `remaining_employees`. The value in this column represents the current total number of employees in the table after the deletion operation. You will observe that this number is one less than the total count before the deletion.

**Try this now:** Copy and paste the code into your SQL editor and execute it.

```{.bash data-prompt="mysql>"} 
mysql> SELECT COUNT(*) as remaining_employees FROM employees;
```
    
??? example "Expected output"

    ```{.text .no-copy}
    +---------------------+
    | remaining_employees |
    +---------------------+
    |                   3 |
    +---------------------+
    1 row in set (0.00 sec)
    ```    
    
## Close the current session

The `exit` command closes the current MySQL client session.

* Executing the `exit` command terminates the connection between your client and the server.

Running this command will close your current interaction with the MySQL server, and you will return to your operating system's command prompt. To run more database commands, you first need to connect to the server again using the [`mysql` command followed by your login credentials](#connect-to-the-database)

**Try this now:** Copy and paste the code into your SQL editor and execute it.

```{.bash data-prompt="mysql>"} 
mysql> exit
```

??? example "Expected output"

    ```{.text .no-copy}
    Bye
    ```   

## Stop the container

Use these Docker Compose commands to stop containers, remove them without a prompt, and clean up everything.

•	Stopping running containers to pause the services without deleting them.

•	Removing stopped containers without confirmation to clean up resources quickly.

•	Deleting all containers, networks, volumes, and images created by Compose to reset the environment completely.

The first command stops the running containers. The second command deletes the stopped containers right away. The third command clears everything, including any persistent data and images created by Compose.

**Try this now:** Copy and paste the code into your terminal.

```{.bash data-prompt="$"}
# stop running containers
docker-compose down
```

Use these commands to remove your setup or start fresh.

```{.bash data-prompt="$"}
# Remove stopped containers without a prompt
docker-compose rm -f
```

```{.bash data-prompt="$"}
# Remove everything: containers, networks, volumes, and images
docker-compose down --volumes --rmi all
```
