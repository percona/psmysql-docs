# UUID_VX component

Introduced in Percona Server for MySQL 8.0.39-30, the `UUID_VX` component provides functions for working with various versions of Universally Unique Identifiers (UUIDs). This feature allows for:

* Managing any UUID version: You can handle various UUID versions, including UUIDv1, UUIDv4, and others.  

* Generating UUIDs for specific versions: This includes creating time-based UUIDs (versions 1, 6, and 7) and random UUIDs (version 4).  

* Enhancing support for UUID-based operations: This adds flexibility in how UUIDs are generated and used within the database.  

By utilizing `UUID_VX`, you can tailor UUID generation to suit your application's needs. For instance, time-based UUIDs ensure chronological ordering, which can improve indexing and query performance in distributed systems. Random UUIDs, on the other hand, provide a higher level of uniqueness and are helpful for security-sensitive applications.  

This component empowers developers to optimize their database operations by choosing the most appropriate UUID version for specific scenarios.

## Universally unique identifier (UUID) overview  

A universally unique identifier (UUID) is a 128-bit number used to uniquely identify information in computer systems. It is commonly represented as a 32-character hexadecimal string divided into five groups separated by hyphens.  

## Benefits of using UUIDs  

UUIDs offer several advantages in distributed systems:  

* Global uniqueness: UUIDs ensure each identifier is unique across different databases and systems without a central authority. This prevents ID conflicts when merging data from multiple sources.  

* Decentralized generation: Different systems can generate UUIDs independently, removing the need for coordination. This is particularly useful in distributed environments.  

* Scalability: UUIDs support distributed databases by adding new records without generating duplicate IDs, even with concurrent insertions.  

* Improved data merging: UUIDs prevent conflicts when combining data from different sources, simplifying the merging process.  

* Security: Randomly generated UUIDs (like UUIDv4) are hard to predict, adding an extra security layer when used as identifiers.  

## UUID versions  

The table below describes the different UUID versions and their characteristics:  

| UUID version | Description |
|-------------|-------------|
| Version 1 (time-based) | - Generated using the current time and a node identifier (usually a MAC address). <br> - Ensures uniqueness over time and across nodes. |
| Version 2 (DCE security) | - Similar to version 1 but includes POSIX UID/GID for enhanced security. |
| Version 3 (name-based, MD5 hash) | - Generated from a namespace identifier and a name (string). <br> - Uses the MD5 hashing algorithm to derive the UUID. |
| Version 4 (random) | - Completely random UUIDs. <br> - Offers uniqueness without requiring specific inputs. |
| Version 5 (name-based, SHA-1 hash) | - Similar to version 3 but uses SHA-1 instead of MD5 for a stronger hash function. |
| Version 6 (time-ordered) | - A reordered version of UUIDv1 for better indexing and storage efficiency. |
| Version 7 (Unix epoch time) | - Encodes a high-precision Unix timestamp with random data. <br> - Provides unique, time-ordered UUIDs ideal for database indexing. |
| Version 8 (custom) | - Reserved for user-defined and experimental purposes. <br> - Allows custom formats and structures. |

## Challenges with UUIDv4 in databases  

While UUIDv4 provides strong uniqueness through randomness, using it as a primary key in distributed databases is generally discouraged due to the following issues:  

| Issue | Description |
|-------|-------------|
| Inefficient indexing | UUIDv4 lacks order, making indexing inefficient. Databases struggle to keep records organized, leading to slower query performance. |
| Fragmentation | The random distribution of UUIDv4 causes data fragmentation, reducing storage efficiency. |
| Storage overhead | UUIDs (128 bits) consume more storage space than traditional integer keys, increasing memory usage. |

Consider using UUIDv7 to improve performance in distributed databases. UUIDv7 encodes a Unix timestamp (millisecond precision) in the first 48 bits, followed by six bits for the UUID version and variant, with the remaining 74 bits as random data. This structure makes UUIDv7 nearly sequential, improving indexing and query efficiency.

### Advantages of UUIDv7 

The following advantages make UUIDv7 a better choice for distributed databases:

* Time-ordered values improve indexing performance and data locality. 

* Better scalability for high-insert workloads in distributed databases.

* Maintains uniqueness while allowing an efficient query range.  

## Install the UUID_VX component

```{.bash data-prompt="mysql>"}
mysql> INSTALL COMPONENT 'file://component_uuid_vx_udf';
```

??? example "Expected output" 

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.03 sec) 
    ```

### Character sets available

The following character sets are used in the component:

| Character set | Description                                                                                      |
|---------------|--------------------------------------------------------------------------------------------------|
| ascii         | Used everywhere UUID strings are returned by functions or accepted as function arguments.       |
| utf8mb4       | Used for string arguments in hash-based UUID generators, like `UUID_V3()` and `UUID_V5()` functions. |
| binary        | Used for arguments in the `BIN_TO_UUID_VX()` function and for results from the `UUID_VX_TO_BIN()` function. |

## Functions available in UUID_VX

The following functions are compatible with all UUID versions:

| Function name        | Argument | Description |
|----------------------|----------|---|
| `BIN_TO_UUID_VX()` | One string argument that must be hexadecimal of exactly 32 characters (16 bytes) | The function returns a UUID with binary data from the argument. It returns an error for all other inputs. |
| `IS_MAX_UUID_VX()`   |  One string argument representing a UUID in standard or hexadecimal form. | The function returns true if the argument is a valid UUID and is a MAX UUID. It returns false for all other inputs. If the argument is NULL, it returns NULL. The function throws an error if the argument cannot be parsed as a UUID. |
| `IS_NIL_UUID_VX()`   | One string argument representing a UUID in standard or hexadecimal form. | The function returns true if the string is a NIL UUID. If the argument is NULL, it returns NULL. If the argument is not a valid UUID, it throws an error. |
| `IS_UUID_VX()`       | One string argument representing a UUID in either standard or hexadecimal form. | The function returns true if the argument is a valid UUID. If the argument is NULL, it returns NULL. For any other input, it returns false. |
| `MAX_UUID_VX()`      | No argument | This function generates a MAX UUID, which has all 128 bits set to one (FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF). This function result is the opposite of the NIL UUID. |
| `NIL_UUID_VX()`     | No argument. | This function generates a NIL UUID, which has all 128 bits set to zero (00000000-0000-0000-0000-000000000000). |
| `UUID_VX_TO_BIN()`   | One string argument, formatted as a UUID or in hexadecimal form | The function converts the string argument to its binary representation. |
| `UUID_VX_VARIANT()`  | One string argument representing a UUID in either standard or hexadecimal format. | The function returns the UUID version (1-8) or an error if the argument is not a valid UUID or returns NULL if the input is NULL. |
| `UUID_VX_VERSION()`  | One string representing a UUID in standard or hexadecimal form. | The function returns version of UUID(1-8). The function throws an error if the argument is not a valid UUID in formatted or hexadecimal form or returns a NULL if the argument is NULL. If the argument is a valid UUID string with an unknown value (outside of the 1-8 range), the function returns `-1`. |


### Examples of functions for all UUID versions

```{.bash data-prompt="mysql>"}
mysql> SELECT is_uuid_vx('01900bf6-0eb0-715a-80f4-636367e07777');
```

??? example "Expected output" 

    ```{.text .no-copy}
    +----------------------------------------------------+
    | is_uuid_vx('01900bf6-0eb0-715a-80f4-636367e07777') |
    +----------------------------------------------------+
    |                                                  1 |
    +----------------------------------------------------+
    ```


```{.bash data-prompt="mysql>"}
mysql> SELECT uuid_vx_version('01900bf6-0eb0-715a-80f4-636367e07777');
```

??? example "Expected output" 

    ```{.text .no-copy}
    +---------------------------------------------------------+
    | uuid_vx_version('01900bf6-0eb0-715a-80f4-636367e07777') |
    +---------------------------------------------------------+
    |                                                       7 |
    +---------------------------------------------------------+
    ```

```{.bash data-prompt="mysql>"}
 mysql> SELECT uuid_vx_variant('01900bf6-0eb0-715a-80f4-636367e07777');
```

??? example "Expected output" 

    ```{.text .no-copy}
    +---------------------------------------------------------+
    | uuid_vx_variant('01900bf6-0eb0-715a-80f4-636367e07777') |
    +---------------------------------------------------------+
    |                                                       1 |
    +---------------------------------------------------------+
    ```

## UUID generator functions

The following functions generate specific UUID versions:

| UUID Version | Arguement | Description |
|--------------|-----------|---|
| `UUID_V1()` | No argument | Generates a version 1 UUID based on a timestamp. If possible, use UUID_V7() instead. |
| `UUID_V3()` | One or two arguments: the first argument is a string that is hashed with MD5 and used in the UUID; the second argument is optional and specifies a namespace (integer values: DNS: 0, URL: 1, OID: 2, X.500: 3; default is 1 or URL). | Generates a version 3 UUID based on a name. Note: MD5 is outdated and not secure. Be sure to use caution and avoid exposing sensitive data. |
| `UUID_V4()` |  No argument | The function generates a version 4 UUID using random numbers, similar to the built-in UUID() function. |
| `UUID_V5()` | One or two arguments: the first argument is a string that is hashed with SHA1 and used in the UUID; the second argument is optional and specifies a namespace (integer values: DNS: 0, URL: 1, OID: 2, X.500: 3; default is 1 or URL).| Generates a version 5 UUID based on a name. Note: SHA1 is better than MD5 but still not secure. Use with caution and avoid exposing sensitive data. |
| `UUID_V6()` |  No argument | Generates a version 6 UUID based on a timestamp. If possible, use UUID_V7() instead. |
| `UUID_V7()` | Can have either no argument or a one integer argument: the argument is the number of milliseconds to adjust the timestamp forward or backward (negative values). | Generates a version 7 UUID based on a timestamp. If there is no argument, no timestamp shift occurs. Timestamp shift can hide the actual creation time of the record. |

The `UUID_v3()` function and `UUID_v5()` function do not validate the string argument, such as whether the URL is formatted correctly or the DNS name is correct. These functions generate a string hash and then add that hash to a UUID with the defined namespace. The user specifies the string.

### UUID generator examples

UUID version 1:

```{.bash data-prompt="mysql>"}
mysql> SELECT uuid_v1();
```

??? example "Expected output" 

    ```{.text .no-copy}
    +--------------------------------------+
    | uuid_v1()                            |
    +--------------------------------------+
    | 14c22f93-2962-11ef-9078-c3abf1c446bb |
    +--------------------------------------+
    ```

UUID version 3 takes one argument and uses the default UUID namespace as “URL”.

```{.bash data-prompt="mysql>"}
mysql> SELECT uuid_v3('http://example.com');
```

??? example "Expected output" 

    ```{.text .no-copy}
    +--------------------------------------+
    | uuid_v3('http://example.com')        |
    +--------------------------------------+
    | d632b50c-7913-3137-ae9a-2d93f56e70d5 |
    +--------------------------------------+
    ```

UUID version 3 takes one argument and uses an explicit UUID namespace “URL”.

```{.bash data-prompt="mysql>"}
mysql> SELECT uuid_v3('http://example.com', 1);
```

??? example "Expected output" 

    ```{.text .no-copy}
    +--------------------------------------+
    | uuid_v3('http://example.com')        |
    +--------------------------------------+
    | d632b50c-7913-3137-ae9a-2d93f56e70d5 |
    +--------------------------------------+
    ```

UUID version 3 takes one argument, with the explicit UUID namespace set to “DNS”.

```{.bash data-prompt="mysql>"}
mysql> SELECT uuid_v3('example.com',0);
```

??? example "Expected output" 

    ```{.text .no-copy}
    +--------------------------------------+
    | uuid_v3('example.com',0)             |
    +--------------------------------------+
    | 9073926b-929f-31c2-abc9-fad77ae3e8eb |
    +--------------------------------------+
    ```

UUID version 4:

```{.bash data-prompt="mysql>"}
mysql> SELECT uuid_v4();
```

??? example "Expected output" 

    ```{.text .no-copy}
    +--------------------------------------+
    | uuid_v4()                            |
    +--------------------------------------+
    | a408e4ad-9b98-4edb-a105-40f22648a928 |
    +--------------------------------------+
    ```

UUID version 5:

```{.bash data-prompt="mysql>"}
mysql> SELECT uuid_v5("http://example.com");
```

??? example "Expected output" 

    ```{.text .no-copy}
    +--------------------------------------+
    | uuid_v5("http://example.com")        |
    +--------------------------------------+
    | 8c9ddcb0-8084-5a7f-a988-1095ab18b5df |
    +--------------------------------------+
    ```

UUID version 6:

```{.bash data-prompt="mysql>"}
mysql> SELECT uuid_v6();
```

??? example "Expected output" 

    ```{.text .no-copy}
    +--------------------------------------+
    | uuid_v6()                            |
    +--------------------------------------+
    | 1ef29686-2168-64a7-b9a2-adb13f80f118 |
    +--------------------------------------+
    ```

UUID version 7 generation:

```{.bash data-prompt="mysql>"}
mysql>SELECT uuid_v7();
```

??? example "Expected output" 

    ```{.text .no-copy}
    +--------------------------------------+
    | uuid_v7()                            |
    +--------------------------------------+
    | 019010f6-0426-70f0-80b0-b63decd3d7d1 |
    +--------------------------------------+
    1 row in set (0.00 sec)
    ```

UUID version 7 with timestamp offset in 84000 seconds in the future

```{.bash data-prompt="mysql>"}
mysql> SELECT uuid_v7(84000000);
```

??? example "Expected output" 

    ```{.text .no-copy}
    +--------------------------------------+
    | uuid_v7(84000000)                    |
    +--------------------------------------+
    | 019015f8-c7c4-70b4-8043-fe241c2be36c |
    +--------------------------------------+
    ```

## Time-based functions

The following functions are used only with time-based UUIDs, specifically versions 1, 6, and 7.


| Function name     | Argument          | Description                                                                                                                                                    |
|-----------------------------|---|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| UUID_VX_TO_TIMESTAMP()      | One string argument | Returns a timestamp string like “2024-05-29 18:04:14.201”. The function throws an error if the argument is not parsable as UUID v.1,6,7. The function always uses UTC, regardless of MySQL's system or time zone settings. |
| UUID_VX_TO_TIMESTAMP_TZ()   | One string argument | Returns a timestamp string with the time zone like “Wed May 29 18:05:07 2024 GMT”. The function throws an error if the argument is not parsable as UUID v.1,6,7. The function always uses UTC (GMT zone), regardless of MySQL's system or time zone settings. |
| UUID_VX_TO_UNIXTIME()       | One string argument | Returns the number of milliseconds since the Epoch. The function throws an error if the argument is not parsable as UUID v.1,6,7. |

### Timestamp-based function examples

```{.bash data-prompt="mysql>"}
mysql> SELECT uuid_vx_to_timestamp('01900bf6-0eb0-715a-80f4-636367e07777');
```

??? example "Expected output" 

    ```{.text .no-copy}
    +--------------------------------------------------------------+
    | uuid_vx_to_timestamp('01900bf6-0eb0-715a-80f4-636367e07777') |
    +--------------------------------------------------------------+
    | 2024-06-12 10:19:53.392                                      |
    +--------------------------------------------------------------+
    1 row in set (0.00 sec)
    ```

```{.bash data-prompt="mysql>"}
mysql> SELECT uuid_vx_to_timestamp_tz('01900bf6-0eb0-715a-80f4-636367e07777');
```

??? example "Expected output" 

    ```{.text .no-copy}
    +-----------------------------------------------------------------+
    | uuid_vx_to_timestamp_tz('01900bf6-0eb0-715a-80f4-636367e07777') |
    +-----------------------------------------------------------------+
    | Wed Jun 12 10:19:53 2024 GMT                                    |
    +-----------------------------------------------------------------+
    ```

```{.bash data-prompt="mysql>"}
mysql> SELECT uuid_vx_to_unixtime('01900bf6-0eb0-715a-80f4-636367e07777');
```

??? example "Expected output" 

    ```{.text .no-copy}
    +-------------------------------------------------------------+
    | uuid_vx_to_unixtime('01900bf6-0eb0-715a-80f4-636367e07777') |
    +-------------------------------------------------------------+
    |                                               1718187593392 |
    +-------------------------------------------------------------+
    ```

## Uninstall the UUID_VX component


```{.bash data-prompt="mysql>"}
mysql> UNINSTALL COMPONENT 'file://component_uuid_vx_udf';
```

??? example "Expected output" 

    ```{.text .no-copy}
    Query OK, 0 rows affected (0.03 sec)
    ```
