
# Data masking plugin functions

This feature was implemented in *Percona Server for MySQL* version Percona Server for MySQL 8.0.17-8.

The Percona Data Masking plugin is a free and Open Source implementation of the
*MySQL*’s data masking plugin. Data Masking provides a set of functions to hide
sensitive data with modified content.

Data masking can have either of the characteristics:

* Generation of random data, such as an email address

* De-identify data by transforming the data to hide content

The data masking functions have the following categories:

* General purpose

* Special purpose

* Generating Random Data with Defined characteristics

* Using Dictionaries to Generate Random Data

## General purpose

The general purpose data masking functions are the following:

<table style="width=100%">
    <tr>
        <td  style="width:40%">Function</td>
        <td>Description</td>
    </tr>
    <tr> 
        <td> mask_inner(string, margin1, margin2 [, character])</td>
        <td>Returns a result where only the inner part of a string is masked. A different masking character can be specified.</td> . 
    </tr>
    <tr>
        <td>mask_outer(string, margin1, margin2 [, character])</td>
        <td>Masks the outer part of the string. The inner section is not masked. A different masking character can be specified.</td
</td>
    </tr>
</table>

### Examples

An example of `mask_inner`:

```{.bash data-prompt="mysql>"}
mysql> SELECT mask_inner('123456789', 1, 2);
```

??? example "Expected output"

    ```{.text .no-copy}
    +-----------------------------------+
    | mask_inner('123456789', 1, 2)     |
    +-----------------------------------+
    |1XXXXXX89                          |
    +-----------------------------------+
    ```

An example of `mask_outer`:

```{.bash data-prompt="mysql>"}
mysql> SELECT mask_outer('123456789', 2, 2); 
```

??? example "Expected output"

    ```{.text .no-copy}
    +------------------------------------+
    | mask_outer('123456789', 2, 2).     |
    +------------------------------------+
    | XX34567XX                          |
    +------------------------------------+
    ```

## Special Purpose

The special purpose data masking functions are as follows:

<table>
    <tr>
        <td>Parameter</td>
        <td>Description</td>
       
    </tr>
    <tr>
        <td>mask_pan(string)</td>
        <td>Masks the Primary Account Number (PAN) by replacing the
string with an “X” except for the last four characters. The PAN string must be 15 characters or 16 characters in length.</td>

    </tr>
    <tr>
        <td>mask_pan_relaxed(string)</td>
        <td>Returns the first six numbers and the last four numbers. The rest of
the string is replaced by “X”.</td>

    </tr>
    <tr>
        <td>mask_ssn(string)</td>
        <td>Returns a string with only the last four numbers visible. The rest
of the string is replaced by “X”.</td>
            </tr>
</table>

### Examples

An example of `mask_pan`.

```{.bash data-prompt="mysql>"}
mysql> SELECT mask_pan (gen_rnd_pan());
```

??? example "Expected output"

    ```{.text .no-copy}
    +------------------------------------+
    | mask_pan(gen_rnd_pan())            |
    +------------------------------------+
    | XXXXXXXXXXX2345                    |
    +------------------------------------+
    ```

An example of `mask_pan_relaxed`:

```{.bash data-prompt="mysql>"}
mysql> SELECT mask_pan_relaxed(gen_rnd_pan());
```

??? example "Expected output"

    ```{.text .no-copy}
    +------------------------------------------+
    | mask_pan_relaxed(gen_rnd_pan())          |
    +------------------------------------------+
    | 520754XXXXXX4848                         |
    +------------------------------------------+
    ```

An example of `mask_ssn`:

```{.bash data-prompt="mysql>"}
mysql> SELECT mask_ssn('555-55-5555');
```

??? example "Expected output"

    ```{.text .no-copy}
    +-------------------------+
    | mask_ssn('555-55-5555') |
    +-------------------------+
    | XXX-XX-5555             |
    +-------------------------+
    ```

## Generate random data for specific requirements

These functions generate random values for specific requirements.

<table style="width=100%">
    <tr>
        <td style="width:25%">Parameter</td>
        <td>Description</td>
    </tr>
    <tr>
        <td>gen_range(lower, upper)</td>
        <td>Generates a random number based on a selected range and supports negative numbers.</td>
           </tr>
    <tr>
        <td>gen_rnd_email()</td>
        <td>Generates a random email address. The domain is example.com.</td>
            </tr>
    <tr>
        <td>gen_rnd_pan([size in integer])</td>
        <td>Generates a random primary account number. This function should only be used for test purposes.</td>
            </tr>
    <tr>
        <td>gen_rnd_us_phone()</td>
        <td>Generates a random U.S. phone number. The generated number adds the
1 dialing code and is in the 555 area code. The 555 area code
is not valid for any U.S. phone number.</td>
            </tr>
    <tr>
        <td>gen_rnd_ssn()</td>
        <td>Generates a random, non-legitimate US Social Security Number in an AAA-BBB-CCCC format. This function should only be used for test purposes.</td>
           </tr>
</table>

### Examples

An example of `gen_range(lower, upper)`:

```{.bash data-prompt="mysql>"}
mysql> SELECT gen_range(10, 100);
```

??? example "Expected output"

    ```{.text .no-copy}
    +--------------------------------------+
    | gen_range(10,100)                    |
    +--------------------------------------+
    | 56                                   |
    +--------------------------------------+
    ```

An example of `gen_range(lower, upper)` with negative numbers:

```{.bash data-prompt="mysql>"}
mysql> SELECT gen_range(-100,-80);
```

??? example "Expected output"

    ```{.text .no-copy}
    +--------------------------------------+
    | gen_range(-100,-80)                  |
    +--------------------------------------+
    | -91                                  |
    +--------------------------------------+
    ```

An example of `gen_rnd_email()`:

```{.bash data-prompt="mysql>"}
mysql> SELECT gen_rnd_email();
```

??? example "Expected output"

    ```{.text .no-copy}
    +---------------------------------------+
    | gen_rnd_email()                       |
    +---------------------------------------+
    | sma.jrts@example.com                  |
    +---------------------------------------+
    ```

An example of `mask_pan(gen_rnd_pan())`:

```{.bash data-prompt="mysql>"}
mysql> SELECT mask_pan(gen_rnd_pan());
```

??? example "Expected output"

    ```{.text .no-copy}
    +-------------------------------------+
    | mask_pan(gen_rnd_pan())             |
    +-------------------------------------+
    | XXXXXXXXXXXX4444                    |
    +-------------------------------------+
    ```

An example of `gen_rnd_us_phone()`:

```{.bash data-prompt="mysql>"}
mysql> SELECT gen_rnd_us_phone();
```

??? example "Expected output"

    ```{.text .no-copy}
    +-------------------------------+
    | gen_rnd_us_phone()            |
    +-------------------------------+
    | 1-555-635-5709                |
    +-------------------------------+
    ```

An example of `gen_rnd_ssn()`:

```{.bash data-prompt="mysql>"}
mysql> SELECT gen_rnd_ssn()
```

??? example "Expected output"

    ```{.text .no-copy}
    +-----------------------------+
    | gen_rnd_ssn()               |
    +-----------------------------+
    | 995-33-5656                 |
    +-----------------------------+
    ```

## Use dictionaries to generate random terms

Use a selected dictionary to generate random terms. The dictionary must be loaded from a file with the following characteristics:


* Plain text


* One term per line


* Must contain at least one entry

Copy the dictionary files to a directory accessible to MySQL. Percona Server for MySQL* 8.0.21-12 enabled using the `secure-file-priv` option for gen_dictionary_load(). The [secure-file-priv](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_secure_file_priv) option defines the directories where gen_dictionary_load() loads the dictionary files.

!!! note

     Percona Server for MySQL 8.0.34 deprecates the `gen_blacklist()` function. Use `gen_blocklist()` instead.


<table style="width:100%">
    <tr>
        <td>Parameter</td>
        <td>Description</td>
        <td style="width:30%">Returns</td>
      
    </tr>
        <tr>
        <td>gen_blacklist(str, dictionary_name, replacement_dictionary_name)</td>
        <td>Replaces a term with a term from a second dictionary. Deprecated in Percona Server for MySQL 8.0.34.</td>
        <td>A dictionary term</td>
           </tr>
    <tr>
    <tr>
        <td>gen_blocklist(str, dictionary_name, replacement_dictionary_name)</td>
        <td>Replaces a term with a term from a second dictionary.</td>
        <td>A dictionary term</td>
           </tr>
    <tr>
        <td>gen_dictionary(dictionary_name)</td>
        <td>Randomizes the dictionary terms</td>
        <td>A random term from the selected dictionary.</td>
        
    </tr>
    <tr>
        <td>gen_dictionary_drop(dictionary_name)</td>
        <td>Removes the selected dictionary from the dictionary registry.</td>
        <td>Either success or failure</td>
            </tr>
    <tr>
        <td>gen_dictionary_load(dictionary path, dictionary name)</td>
        <td>Loads a file into the dictionary registry and configures the dictionary name. The name can be used with any function. If the dictionary is edited, you must drop and then reload the dictionary to view the changes.</td>
        <td>Either success or failure</td>
            </tr>
</table>

### Example

An example of `gen_blocklist()`:

```{.bash data-prompt="mysql>"}
mysql> SELECT gen_blocklist('apple', 'fruit', 'nut');
```

??? example "Expected output"

    ```{.text .no-copy}
    +-----------------------------------------+
    | gen_blocklist('apple', 'fruit', 'nut')  |
    +-----------------------------------------+
    | walnut                                  |
    +-----------------------------------------+
    ```
An example of `gen_dictionary()`:

```{.bash data-prompt="mysql>"}
mysql> SELECT gen_dictionary('trees');
```

??? example "Expected output"

    ```{.text .no-copy}
    +--------------------------------------------------+
    | gen_dictionary('trees')                          |
    +--------------------------------------------------+
    | Norway spruce                                    |
    +--------------------------------------------------+
    ```

An example of `gen_dictionary_drop()`:

```{.bash data-prompt="mysql>"}
mysql> SELECT gen_dictionary_drop('mytestdict')
```

??? example "Expected output"

    ```{.text .no-copy}
    +-------------------------------------+
    | gen_dictionary_drop('mytestdict')   |
    +-------------------------------------+
    | Dictionary removed                  |
    +-------------------------------------+
    ```

An example of `gen_dictionary_load(path, name)`:

```{.bash data-prompt="mysql>"}
mysql> SELECT gen_dictionary_load('/usr/local/mysql/dict-files/testdict', 'testdict');
```

??? example "Expected output"

    ```{.text .no-copy}
    +-------------------------------------------------------------------------------+
    | gen_dictionary_load('/usr/local/mysql/mysql/dict-files/testdict', 'testdict') |
    +-------------------------------------------------------------------------------+
    | Dictionary load successfully                                                  |
    +-------------------------------------------------------------------------------+
    ```
