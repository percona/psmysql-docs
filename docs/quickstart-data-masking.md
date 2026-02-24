# Get started with Data Masking

This quickstart gets the data masking component installed and lets you try the component with a test database. You need access to a Percona Server for MySQL 8.4 server. Follow the steps to install, set permissions, create sample data, and run masking examples. For production use and limitations, see the [Data masking overview](data-masking-overview.md).

## Prerequisites

* Percona Server for MySQL (latest recommended).
* The `component_masking_functions` library in the server plugin directory. Run `SHOW VARIABLES LIKE 'plugin_dir';` and confirm the library exists in that directory. If the library is missing, see [Install the data masking component](install-data-masking-component.md).

## Install the component and set permissions

Do these once, in order. Full details: [Install the data masking component](install-data-masking-component.md).
{.power-number}

1. Create the dictionary table (required before step 2):

    ```sql
    CREATE TABLE IF NOT EXISTS
    mysql.masking_dictionaries(
        Dictionary VARCHAR(256) NOT NULL,
        Term VARCHAR(256) NOT NULL,
        UNIQUE INDEX dictionary_term_idx (Dictionary, Term)
    ) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4;
    ```

    ??? example "Expected output"
        ```{.text .no-copy}
        Query OK, 0 rows affected (0.01 sec)
        ```

2. Install the component:

    ```sql
    INSTALL COMPONENT 'file://component_masking_functions';
    ```

    ??? example "Expected output"
        ```{.text .no-copy}
        Query OK, 0 rows affected (0.00 sec)
        ```

3. Grant `mysql.session` access to the dictionary table (required for `gen_dictionary` and `gen_blocklist` on 8.4.4-1 and later):

    ```sql
    GRANT SELECT, INSERT, UPDATE, DELETE ON mysql.masking_dictionaries TO 'mysql.session'@'localhost';
    ```

    ??? example "Expected output"
        ```{.text .no-copy}
        Query OK, 0 rows affected (0.00 sec)
        ```

4. Grant dictionary management to your user (required for the [dictionary-based masking](#optional-dictionary-based-masking) section below; skip if you will not try that section). Replace `<user>` and `<host>` with the MySQL user you connect as (for example, `root` and `localhost`):

    ```sql
    GRANT MASKING_DICTIONARIES_ADMIN ON *.* TO '<user>'@'<host>';
    ```

    ??? example "Expected output"
        ```{.text .no-copy}
        Query OK, 0 rows affected (0.00 sec)
        ```

    No `FLUSH PRIVILEGES` is needed; the grant takes effect immediately. If the privilege does not appear, reconnect to the server.

## Create the test database and tables

Run the following script to create the database and both tables with sample rows. The script drops the database if the database already exists so you can run the script again without creating duplicate rows. The column types and values are chosen so you can try masking functions in the next sections.

```sql
DROP DATABASE IF EXISTS masking_demo;
CREATE DATABASE masking_demo;
USE masking_demo;

CREATE TABLE contacts (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100),
    ssn         VARCHAR(11),
    card_no     VARCHAR(19),
    email       VARCHAR(255),
    phone       VARCHAR(20),
    notes       VARCHAR(255)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO contacts (name, ssn, card_no, email, phone, notes)
VALUES
    ('Priya Sharma',  '123-45-6789', '4111111111111111', 'priya.sharma@example.com',  '1-555-010-1234', 'VIP'),
    ('Yuki Tanaka',   '987-65-4321', '5500000000000004', 'yuki.tanaka@example.com',    '1-555-010-5678', 'Newsletter'),
    ('Fatima Hassan', '111-22-3333', '340000000000009',  'fatima.hassan@example.com',  '1-555-010-9012', NULL);

CREATE TABLE contacts_intl (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100),
    country     VARCHAR(50),
    canada_sin  VARCHAR(11),
    uk_nin      VARCHAR(20),
    iban        VARCHAR(40)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO contacts_intl (name, country, canada_sin, uk_nin, iban)
VALUES
    ('Jean Lefebvre',   'Canada',  '506-948-819', NULL, NULL),
    ('Siobhan O''Brien', 'UK',     NULL, 'CT264683D', NULL),
    ('Hans Mueller',    'Germany', NULL, NULL, 'DE27 1002 02003 77495 4156');
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.00 sec)
    Query OK, 1 row affected (0.00 sec)
    Database changed
    Query OK, 0 rows affected (0.01 sec)
    Query OK, 3 rows affected (0.00 sec)
    Query OK, 0 rows affected (0.00 sec)
    Query OK, 3 rows affected (0.00 sec)
    ```

## View raw data

```sql
SELECT id, name, ssn, card_no, email, phone FROM contacts;
```

??? example "Expected output"

    ```{.text .no-copy}
    +----+--------------+-------------+------------------+-------------------------+----------------+
    | id | name         | ssn         | card_no          | email                   | phone          |
    +----+--------------+-------------+------------------+-------------------------+----------------+
    |  1 | Priya Sharma | 123-45-6789 | 4111111111111111 | priya.sharma@example.com| 1-555-010-1234 |
    |  2 | Yuki Tanaka  | 987-65-4321 | 5500000000000004 | yuki.tanaka@example.com | 1-555-010-5678 |
    |  3 | Fatima Hassan| 111-22-3333 | 340000000000009  | fatima.hassan@example.com| 1-555-010-9012 |
    +----+--------------+-------------+------------------+-------------------------+----------------+
    3 rows in set (0.00 sec)
    ```

## Mask sensitive columns in queries

The examples below use masking functions in `SELECT`; the table data is unchanged. Expected outputs in this guide are illustrative; results from random or dictionary-based functions vary on each run and may not match the examples. To enforce masking for other users, use a view (see [Expose masked data via a view](#expose-masked-data-via-a-view)) and restrict access to the base table. For limitations and security, see the [Data masking overview](data-masking-overview.md#limitations-and-security-considerations).

### Payment card and SSN

[`mask_pan`](data-masking-function-list.md#mask_panstr-mask_char) leaves the last four digits visible; [`mask_ssn`](data-masking-function-list.md#mask_ssnstr-mask_char) does the same for SSN.

```sql
SELECT
    name,
    mask_pan(card_no)   AS card_masked,
    mask_ssn(ssn)      AS ssn_masked
FROM contacts;
```

??? example "Expected output"

    ```{.text .no-copy}
    +--------------+------------------+-------------+
    | name         | card_masked      | ssn_masked  |
    +--------------+------------------+-------------+
    | Priya Sharma | XXXXXXXXXXXX1111 | ***-**-6789 |
    | Yuki Tanaka  | XXXXXXXXXXXX0004 | ***-**-4321 |
    | Fatima Hassan| XXXXXXXXXX0009   | ***-**-3333 |
    +--------------+------------------+-------------+
    3 rows in set (0.00 sec)
    ```

### Inner and outer parts of a string

[`mask_inner`](data-masking-function-list.md#mask_innerstr-margin1-margin2-mask_char) keeps the first and last character(s); [`mask_outer`](data-masking-function-list.md#mask_outerstr-margin1-margin2-mask_char) masks the left and right ends. The third and fourth arguments are the number of characters to keep unmasked on the left and right.

```sql
SELECT
    name,
    mask_inner(name, 1, 1)     AS name_inner_masked,
    mask_outer(phone, 2, 4)    AS phone_outer_masked
FROM contacts;
```

??? example "Expected output"

    ```{.text .no-copy}
    +--------------+------------------+------------------+
    | name         | name_inner_masked| phone_outer_masked|
    +--------------+------------------+------------------+
    | Priya Sharma | PXXXXXXXXXXa     | XX5-010-1234      |
    | Yuki Tanaka  | YXXXXXXXXa      | XX5-010-5678      |
    | Fatima Hassan| FXXXXXXXXXXn     | XX5-010-9012      |
    +--------------+------------------+------------------+
    3 rows in set (0.00 sec)
    ```

### Generated values (for testing)

[`gen_rnd_email()`](data-masking-function-list.md#gen_rnd_emailname_size-surname_size-domain) and [`gen_rnd_ssn()`](data-masking-function-list.md#gen_rnd_ssn) return new values each time. They are useful for generating test data, not for masking existing values in place.

```sql
SELECT
    id,
    gen_rnd_email(5, 8, 'test.example') AS generated_email,
    gen_rnd_ssn()                         AS generated_ssn
FROM contacts;
```

??? example "Expected output"

    ```{.text .no-copy}
    +----+---------------------------+-------------+
    | id | generated_email           | generated_ssn|
    +----+---------------------------+-------------+
    |  1 | abcde.fghijkl@test.example| 912-34-5678 |
    |  2 | vwxyz.abcdefg@test.example| 987-65-4321 |
    |  3 | qwert.yuiopas@test.example| 923-45-6789 |
    +----+---------------------------+-------------+
    3 rows in set (0.00 sec)
    ```

Output will vary on each run and may not match the expected results above. For constraints and caveats, see [Data masking component functions and variables](data-masking-function-list.md).

### International data masking functions

The component includes functions for region-specific identifiers: Canadian Social Insurance Number (SIN) ([`mask_canada_sin`](data-masking-function-list.md#mask_canada_sinstr-mask_char)), United Kingdom National Insurance Number (NIN) ([`mask_uk_nin`](data-masking-function-list.md#mask_uk_ninstr-mask_char)), and International Bank Account Number (IBAN) ([`mask_iban`](data-masking-function-list.md#mask_ibanstr-mask_char)). The script above already created the `contacts_intl` table. View the raw data, then apply the region-specific masking functions:

```sql
SELECT name, country, canada_sin, uk_nin, iban FROM contacts_intl;
```

??? example "Expected output"

    ```{.text .no-copy}
    +----------------+---------+-------------+----------------+------------------------------+
    | name           | country | canada_sin  | uk_nin     | iban                         |
    +----------------+---------+-------------+----------------+------------------------------+
    | Jean Lefebvre  | Canada  | 506-948-819 | NULL       | NULL                         |
    | Siobhan O'Brien| UK      | NULL        | CT264683D | NULL                         |
    | Hans Mueller   | Germany | NULL        | NULL       | DE27 1002 02003 77495 4156   |
    +----------------+---------+-------------+----------------+------------------------------+
    3 rows in set (0.00 sec)
    ```

```sql
SELECT
    name,
    country,
    mask_canada_sin(canada_sin)  AS canada_sin_masked,
    mask_uk_nin(uk_nin)          AS uk_nin_masked,
    mask_iban(iban)              AS iban_masked
FROM contacts_intl;
```

??? example "Expected output"

    ```{.text .no-copy}
    +----------------+---------+------------------+---------------+----------------------------+
    | name           | country | canada_sin_masked| uk_nin_masked | iban_masked                |
    +----------------+---------+------------------+---------------+----------------------------+
    | Jean Lefebvre  | Canada  | XXX-XXX-XXX      | NULL          | NULL                       |
    | Siobhan O'Brien| UK      | NULL             | CT*******     | NULL                       |
    | Hans Mueller   | Germany | NULL             | NULL          | DE** **** **** **** ****   |
    +----------------+---------+------------------+---------------+----------------------------+
    3 rows in set (0.00 sec)
    ```

Each function returns NULL when the input is NULL. For more options (for example, custom mask characters) and the corresponding generators ([`gen_rnd_canada_sin`](data-masking-function-list.md#gen_rnd_canada_sin), [`gen_rnd_uk_nin`](data-masking-function-list.md#gen_rnd_uk_nin), [`gen_rnd_iban`](data-masking-function-list.md#gen_rnd_ibancountry-size)), see [Data masking component functions and variables](data-masking-function-list.md).

### Expose masked data via a view

To ensure that only masked data is visible, define a view that applies the masking functions and grant `SELECT` on the view (not on the base table) to users who should see masked data. Example:

```sql
DROP VIEW IF EXISTS contacts_masked;
CREATE VIEW contacts_masked AS
SELECT
    id,
    name,
    mask_pan(card_no)       AS card_no,
    mask_ssn(ssn)          AS ssn,
    mask_outer(email, 2, 4) AS email,
    mask_outer(phone, 2, 4) AS phone,
    notes
FROM contacts;

SELECT id, name, card_no, ssn, email, phone FROM contacts_masked;
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.00 sec)
    Query OK, 0 rows affected (0.00 sec)

    +----+--------------+------------------+-------------+--------------------------+------------------+
    | id | name         | card_no          | ssn         | email                     | phone            |
    +----+--------------+------------------+-------------+--------------------------+------------------+
    |  1 | Priya Sharma | XXXXXXXXXXXX1111 | ***-**-6789 | XXriya.sharma@exampXXXX  | XX5-010-1234     |
    |  2 | Yuki Tanaka  | XXXXXXXXXXXX0004 | ***-**-4321 | XXuki.tanaka@exampXXXX   | XX5-010-5678     |
    |  3 | Fatima Hassan| XXXXXXXXXX0009   | ***-**-3333 | XXtima.hassan@examXXXX  | XX5-010-9012     |
    +----+--------------+------------------+-------------+--------------------------+------------------+
    3 rows in set (0.00 sec)
    ```

The view uses [`mask_outer(..., 2, 4)`](data-masking-function-list.md#mask_outerstr-margin1-margin2-mask_char) for email and phone. Grant `SELECT` on the view (not the base table) to users who should see masked data only. For access control and limitations, see the [Data masking overview](data-masking-overview.md#limitations-and-security-considerations).

## Optional: dictionary-based masking

Functions such as [`gen_dictionary`](data-masking-function-list.md#gen_dictionarydictionary_name) and [`gen_blocklist`](data-masking-function-list.md#gen_blockliststr-from_dictionary_name-to_dictionary_name) use the `mysql.masking_dictionaries` table. 

You need the [step 4 grant (MASKING_DICTIONARIES_ADMIN)](#install-the-component-and-set-permissions) and, on 8.4.4-1 and later, the step 3 grant to `mysql.session` described in the [install guide](install-data-masking-component.md).

Add a small dictionary with [`masking_dictionary_term_add`](data-masking-function-list.md#masking_dictionary_term_adddictionary_name-term_name), then try [`gen_dictionary`](data-masking-function-list.md#gen_dictionarydictionary_name). 

The role column is chosen at random from the dictionary; your output will vary and may not match the expected results.

```sql
SELECT masking_dictionary_term_add('roles', 'Engineer');
SELECT masking_dictionary_term_add('roles', 'Analyst');
SELECT masking_dictionary_term_add('roles', 'Manager');

SELECT id, name, gen_dictionary('roles') AS role FROM contacts;
```

??? example "Expected output (role column varies; your output may not match)"

    ```{.text .no-copy}
    +-----------------------------------------------+
    | masking_dictionary_term_add('roles', 'Engineer')|
    +-----------------------------------------------+
    |                                             1 |
    +-----------------------------------------------+
    1 row in set (0.00 sec)

    +----------------------------------------------+
    | masking_dictionary_term_add('roles', 'Analyst')|
    +----------------------------------------------+
    |                                            1 |
    +----------------------------------------------+
    1 row in set (0.00 sec)

    +----------------------------------------------+
    | masking_dictionary_term_add('roles', 'Manager') |
    +----------------------------------------------+
    |                                            1 |
    +----------------------------------------------+
    1 row in set (0.00 sec)

    +----+---------------+----------+
    | id | name          | role     |
    +----+---------------+----------+
    |  1 | Priya Sharma  | Manager  |
    |  2 | Yuki Tanaka   | Engineer |
    |  3 | Fatima Hassan | Manager  |
    +----+--------------+----------+
    3 rows in set (0.00 sec)
    ```

To remove the dictionary when finished: `SELECT masking_dictionary_remove('roles');` ([`masking_dictionary_remove`](data-masking-function-list.md#masking_dictionary_removedictionary_name)). For large dictionaries or production use, see the [Data masking overview](data-masking-overview.md) and [function list](data-masking-function-list.md).

## Clean up (optional)

To remove the test database and all objects in the database (tables, the `contacts_masked` view, and data):

```sql
DROP DATABASE IF EXISTS masking_demo;
```

??? example "Expected output"

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.01 sec)
    ```

## Additional resources

* [Data masking overview](data-masking-overview.md)
* [Install the data masking component](install-data-masking-component.md)
* [Data masking component functions and variables](data-masking-function-list.md)
