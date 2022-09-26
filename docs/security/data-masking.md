# Data Masking

This feature was implemented in *Percona Server for MySQL* version Percona Server for MySQL 8.0.17-8.

The Percona Data Masking plugin is a free and Open Source implementation of the
*MySQL*’s data masking plugin. Data Masking provides a set of functions to hide
sensitive data with modified content.

Data masking can have either of the characteristics:


* Generation of random data, such as an email address


* De-identify data by transforming the data to hide content

### Installing the plugin

The following command installs the plugin:

```sql
$ INSTALL PLUGIN data_masking SONAME 'data_masking.so';
```

### Data Masking functions

The data masking functions have the following categories:


* General purpose


* Special purpose


* Generating Random Data with Defined characteristics


* Using Dictionaries to Generate Random Data

### General Purpose

The general purpose data masking functions are the following:

<table style="width=100%">
    <tr>
        <td  style="width:40%">Parameter</td>
        <td>Description</td>
    </tr>
    <tr> 
        <td> mask_inner(string, margin1, margin2 [, character])</td>
        <td>Returns a result where only the inner part of a string is masked. An optional masking character can be specified.</td>
    </tr>
    <tr>
        <td>mask_outer(string, margin1, margin2 [, character])</td>
        <td>Masks the outer part of the string. The inner section is not masked.</td
</td>
    </tr>
</table>

#### Examples

An example of `mask_inner`:

```sql
mysql> SELECT mask_inner('123456789', 1, 2);
```

The output is the following:

```text
+-----------------------------------+
| mask_inner('123456789', 1, 2)     |
+-----------------------------------+
|1XXXXXX89                          |
+-----------------------------------+
```
An example of `mask_outer`:

```sql
mysql> SELECT mask_outer('123456789', 2, 2); 
```
The output is the following:

```text
+------------------------------------+
| mask_outer('123456789', 2, 2).     |
+------------------------------------+
| XX34567XX                          |
+------------------------------------+
```

### Special Purpose

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

#### Examples

An example of `mask_pan`.

```sql
mysql> SELECT mask_pan (gen_rnd_pan());
```
The output is the following:

```text
+------------------------------------+
| mask_pan(gen_rnd_pan())            |
+------------------------------------+
| XXXXXXXXXXX2345                    |
+------------------------------------+
```
An example of `mask_pan_relaxed`:

```sql
mysql> SELECT mask_pan_relaxed(gen_rnd_pan());
```
The output is the following:

```text
+------------------------------------------+
| mask_pan_relaxed(gen_rnd_pan())          |
+------------------------------------------+
| 520754XXXXXX4848                         |
+------------------------------------------+
```

An example of `mask_ssn`:

```sql
mysql> SELECT mask_ssn('555-55-5555');
```
The output is the following:

```text
+-------------------------+
| mask_ssn('555-55-5555') |
+-------------------------+
| XXX-XX-5555             |
+-------------------------+
```


### Generating Random Data for Specific Requirements

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

#### Examples

An example of `gen_range(lower, upper)`:

```sql
mysql> SELECT gen_range(10, 100);
```
The output is the following:

```text
+--------------------------------------+
| gen_range(10,100)                    |
+--------------------------------------+
| 56                                   |
+--------------------------------------+
```
An example of `gen_range(lower, upper)` with negative numbers:

```sql
mysql> SELECT gen_range(-100,-80);
```
The output is the following:

```text
+--------------------------------------+
| gen_range(-100,-80)                  |
+--------------------------------------+
| -91                                  |
+--------------------------------------+
```
An example of `gen_rnd_email()`:

```sql
<td>mysql> SELECT gen_rnd_email();
```
The output is the following:

```text
+---------------------------------------+
| gen_rnd_email()                       |
+---------------------------------------+
| sma.jrts@example.com                  |
+---------------------------------------+
```

An example of `mask_pan(gen_rnd_pan())`:

```sql
<td>mysql> SELECT mask_pan(gen_rnd_pan());
```
The output is the following:

```text
+-------------------------------------+
| mask_pan(gen_rnd_pan())             |
+-------------------------------------+
| XXXXXXXXXXXX4444                    |
+-------------------------------------+
```

An example of `gen_rnd_us_phone()`:

```sql
mysql> SELECT gen_rnd_us_phone();
```
The output is the following:

```text
+-------------------------------+
| gen_rnd_us_phone()            |
+-------------------------------+
| 1-555-635-5709                |
+-------------------------------+
```
An example of `gen_rnd_ssn()`:

```sql
mysql> SELECT gen_rnd_ssn()
```

The output is the following:

```text
+-----------------------------+
| gen_rnd_ssn()               |
+-----------------------------+
| 995-33-5656                 |
+-----------------------------+
```



### Using Dictionaries to Generate Random Terms

Use a selected dictionary to generate random terms. The dictionary must be loaded from a file with the following characteristics:


* Plain text


* One term per line


* Must contain at least one entry

Copy the dictionary files to a directory accessible to MySQL. The [secure-file-priv](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_secure_file_priv) option defines the directories where gen_dictionary_load() loads the dictionary files.

!!! note

    *Percona Server for MySQL* 8.0.21-12 enabled using the `secure-file-priv` option for gen_dictionary_load().

<table style="width:100%">
    <tr>
        <td>Parameter</td>
        <td>Description</td>
        <td style="width:30%">Returns</td>
      
    </tr>
    <tr>
        <td>gen_blacklist(str, dictionary_name, replacement_dictionary_name)</td>
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

#### Example

An example of `gen_blacklist()`:

```sql
mysql> SELECT gen_blacklist('apple', 'fruit', 'nut');
```

The output is the following:

```text
+-----------------------------------------+
| gen_blacklist('apple', 'fruit', 'nut')  |
+-----------------------------------------+
| walnut                                  |
+-----------------------------------------+
```
An example of `gen_dictionary()`:

```sql
mysql> SELECT gen_dictionary('trees');
```

The output is the following:

```text
+--------------------------------------------------+
| gen_dictionary('trees')          |
+--------------------------------------------------+
| Norway spruce                                    |
+--------------------------------------------------+
```
An example of `gen_dictionary_drop()`:

```sql
mysql> SELECT gen_dictionary_drop('mytestdict')
```

The output is the following:

```text
+-------------------------------------+
| gen_dictionary_drop('mytestdict')   |
+-------------------------------------+
| Dictionary removed                  |
+-------------------------------------+
```

An example of `gen_dictionary_load(path, name)`:

```sql
mysql> SELECT gen_dictionary_load('/usr/local/mysql/dict-files/testdict', 'testdict');
```

The output is the following:

```text
+-------------------------------------------------------------------------------+
| gen_dictionary_load('/usr/local/mysql/mysql/dict-files/testdict', 'testdict') |
+-------------------------------------------------------------------------------+
| Dictionary load successfully                                                  |
+-------------------------------------------------------------------------------+
```


### Uninstalling the plugin

The [UNINSTALL PLUGIN](https://dev.mysql.com/doc/refman/8.0/en/uninstall-plugin.html) statement disables and uninstalls the plugin.
