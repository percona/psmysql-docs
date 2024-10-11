# Data masking component functions

The feature is in [tech preview](glossary.md#tech-preview).

| **Name**                                          | **Usage**                                             |
|---------------------------------------------------|-------------------------------------------------------|
| [`gen_blocklist(str, from_dictionary_name, to_dictionary_name)`](#gen_blockliststr-from_dictionary_name-to_dictionary_name) | Replace a term from a dictionary                      |
| [`gen_dictionary(dictionary_name)`](#gen_dictionarydictionary_name) | Returns a random term from a dictionary               |
| [`gen_range(lower, upper)`](#gen_rangelower-upper) | Returns a number from a range                       |
| [`gen_rnd_canada_sin()`](#gen_rnd_canada_sin) | Generates a Canadian Social Insurance number          |
| [`gen_rnd_email([name_size, surname_size, domain])`](#gen_rnd_emailname_size-surname_size-domain)    | Generates an email address                            |
| [`gen_rnd_iban([country, size])`](#gen_rnd_ibancountry-size)                                    | Generates an International Bank Account number        |
| [`gen_rnd_pan()`](#gen_rnd_pan)                                     | Generates a Primary account number for a payment card |
| [`gen_rnd_ssn()`](#gen_rnd_ssn)                                     | Generates a US Social Security number                 |
| [`gen_rnd_uk_nin()`](#gen_rnd_uk_nin)                                  | Generates a United Kingdom National Insurance number  |
| [`gen_rnd_us_phone()`](#gen_rnd_us_phone)                                | Generates a US phone number                           |
| [`gen_rnd_uuid()`](#gen_rnd_uuid)                                    | Generates a Universally Unique Identifier             |
| [`mask_canada_sin(str [,mask_char])`](#mask_canada_sinstr-mask_char)                                 | Masks the Canadian Social Insurance number            |
| [`mask_iban(str [,mask_char])`](#mask_ibanstr-mask_char)                                      | Masks the International Bank Account number           |
| [`mask_inner(str, margin1, margin2 [,mask_char])`](#mask_innerstr-margin1-margin2-mask_char)   | Masks the inner part of a string                      |
| [`mask_outer(str, margin1, margin2 [,mask_char])`](#mask_outerstr-margin1-margin2-mask_char)  | Masks the outer part of the string                    |
| [`mask_pan(str [,mask_char])`](#mask_panstr-mask_char)     | Masks the Primary Account number for a payment card   |
| [`mask_pan_relaxed(str [,mask_char])`](#mask_pan_relaxedstr-mask_char)   | Partially masks the Primary Account number for a payment card   |
| [`mask_ssn(str [,mask_char])`](#mask_ssnstr-mask_char)    | Masks the US Social Security number                   |
| [`mask_uk_nin(str [,mask_char])`](#mask_uk_ninstr-mask_char)     | Masks the United Kingdom National Insurance number    |
| [`mask_uuid(str [,mask_char])`](#mask_uuidstr-mask_char)         | Masks the Universally Unique Identifier               |
| [`masking_dictionary_remove(dictionary_name)`](#masking_dictionary_removedictionary_name)          | Removes the dictionary                                |
| [`masking_dictionary_term_add(dictionary_name, term_name)`](#masking_dictionary_term_adddictionary_name-term_name)     | Adds a term to the masking dictionary                 |
| [`masking_dictionary_term_remove(dictionary_name, term_name)`](#masking_dictionary_term_removedictionary_name-term_name)      | Removes a term from the masking dictionary            |

## gen_blocklist(str, from_dictionary_name, to_dictionary_name)

Replaces a term from one dictionary with a randomly selected term in another dictionary.

### Parameters

| Parameter | Optional | Description | Type |
| --- | --- | --- | --- |
| `term` | No | The term to replace | String |
| `from_dictionary_name` | No | The dictionary that stores the term. | String |
| `to_dictionary_name` | No | The dictionary that stores the replacement term | String |

### Returns

A term, selected at random, from the dictionary listed in `to_dictionary_name` that replaces the selected term. If the selected `term` is not listed in the `from_dictionary_name` or a dictionary is missing, then the `term` is returned. If the `to_dictionary_name` does not exist, then returns NULL. The character set of the returned string is the same character set of the `term` parameter.

Returns NULL if you invoke this function with NULL as the primary argument.

### Example

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

## gen_dictionary(dictionary_name)

Returns a term from a dictionary selected at random.

### Parameters

| Parameter | Optional | Description | Type |
| --- | --- | --- | --- |
| `dictionary_name` | No | Select the random term from this dictionary | String |


### Returns

A random term from the dictionary listed in `dictionary_name` in the `utf8mb4` character set. Returns NULL if the `dictionary_name` does not exist.

### Example

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

## gen_range(lower, upper)

Returns a number from a defined range.

### Parameters

| Parameter | Optional | Description | Type |
| --- | --- | --- | --- |
| `lower` | No | The lower boundary of the range | Integer |
| `upper` | No | The upper boundary of the range | Integer |

The `upper` parameter value must be an integer either greater than or equal to the `lower` parameter value.

### Returns

An integer, selected at random, from an inclusive range defined by the `lower` parameter value and the `upper` parameter value, or NULL if the `upper` boundary is less than the `lower` boundary.

### Example

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

## gen_rnd_canada_sin()

Generates a Canada Social Insurance Number (SIN).

!!! important

Only use this function for testing because the result could be a legitimate SIN. Use [`mask_canada_sin`](#mask_canada_sinstr-mask_char) to disguise the result if you must publish the result.

### Parameters

None.

### Returns

Returns a Canada SIN formatted in three groups of three digits (for example, 123-456-789) in the `utf8mb4` character set. To ensure the number is consistent, the number is verified with the [Luhn algorithm](https://en.wikipedia.org/wiki/Luhn_algorithm).

### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT gen_rnd_canada_sin();
```

??? example "Expected output"

    ```{.text .no-copy}
    +-------------------------+
    | gen_rnd_canada_sin()    |
    +-------------------------+
    | 506-948-819             |
    +-------------------------+
    ```

## gen_rnd_email([name_size, surname_size, domain])

Generates a random email address in the `name.surname@domain` format.

### Parameters

| Parameter | Optional | Description | Type |
| --- | --- | --- | --- |
| `name_size` | Yes | Specifies the number of characters in the name part. The default number is five. The minimum number is one. The maximum number is 1024. | Integer |
| `surname_size` | Yes | Specifies the number of characters in the surname part. The default number is seven. The minimum number is one. The maximum number is 1024. | Integer |
| `domain` | Yes | Specifies the domain name used. The default value is `example.com`. | Integer |


### Returns

A generated email address as a string in the same character set as `domain`. If the `domain` value is not specified, then the string is in the `utf8mb4` character set. The `name` and `surname` are random lower-case letters (a - z).

### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT gen_rnd_email(name_size=4, surname_size=5, domain='mydomain.edu');
```

??? example "Expected output"

    ```{.text .no-copy}
    +-------------------------------------+
    | gen_rnd_email(4, 5, 'mydomain.edu') |
    +-------------------------------------+
    | qwer.asdfg@mydomain.edu             |
    +-------------------------------------+
    ```

## gen_rnd_iban([country, size])

Generates an Internal Bank Account Number (IBAN).

!!! important

Generating an IBAN with a valid country code should only be used for testing. The function does not check if the generated value is a legitimate bank account. If you must publish the result, consider using [`mask_iban`](#mask_ibanstr-mask_char) to disguise the result. The function does not perform a checksum on the bank account number.

### Parameters

| Parameter | Optional | Description | Type |
| --- | --- | --- | --- |
| `country` | Yes | A two-character country code | String |
| `size` | Yes | Number of characters | Integer |

If the `country` is not specified, the default value is `ZZ`. The value must be two upper-case characters (A-Z) or an error is returned.

The default value for `size` is 16. The minimum value is 15. The maximum value is 34.

### Returns

The function returns a string that is the length of the `size` value. The string consists of `country` (two characters) followed by the (size - 2) random digits.

The character set is the same as the `country` parameter or if that parameter is not specified, the character set is `utf8mb4`.

### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT gen_rnd_iban();
```

??? example "Expected output"

    ```{.text .no-copy}
    +-------------------+
    | gen_rnd_iban()    |
    +-------------------+
    |ZZ78959120078536   |
    +-------------------+
    ```

## gen_rnd_pan()

Generates a Primary Account Number (PAN) for a payment card that passes basic checksum validation.

The generated PAN can be one of the following:

* American Express

* Visa

* Mastercard

* Discover

!!! important

    Generating the PAN should only be used for testing. The function does not check if the generated value is a legitimate primary account number. If you must publish the result, consider using [`mask_pan`](#mask_panstr-mask_char) or [`mask_pan_relaxed()`](#mask_pan_relaxedstr-mask_char) to disguise the result.

### Parameters

None

### Returns

A random PAN string in `utf8mb4` character set.

### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT gen_rnd_pan();
```

??? example "Expected output"

    ```{.text .no-copy}
    +-------------------+
    | gen_rnd_pan()     |
    +-------------------+
    | 1234567898765432  |
    +-------------------+
    ```

## gen_rnd_ssn()

Generates a United States Social Security Account Number (SSN).

### Parameters

None


### Returns

A SSN string in a nine-digit number format "AAA-GG-SSSS" in the `utf8mb4` character set. The number has three parts, the first three digits are the area number, the group number, and the serial number. The generated SSN uses '900' or greater numbers for the area number. These numbers are not legitimate because they are outside the approved range.

### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT gen_rnd_ssn();
```

??? example "Expected output"

    ```{.text .no-copy}
    +----------------+
    | gen_rnd_ssn()  |
    +----------------+
    | 970-03-0370    |
    -----------------+
    ```

## gen_rnd_uk_nin()

Generates a United Kingdom National Insurance Number (NIN).

!!! important

    This function should only be used for testing. The function does not check if the generated value is a legitimate United Kingdom National Insurance number. If you must publish the result, consider masking the result with [`mask_uk_nin`](#mask_uk_ninstr-mask_char).

### Parameters

None.

### Returns

A NIN string in the `utf8mb4` character set. The string is nine (9) characters in length, always starts with 'AA' and ends with 'C'.

### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT gen_rnd_uk_nin();
```

??? example "Expected output"

    ```{.text .no-copy}
    +----------------------+
    | gen_rnd_uk_nin()     |
    +----------------------+
    | AA123456C            |
    +----------------------+
    ```

## gen_rnd_us_phone()

Generates a United States phone number with the `555` area code. The '555' area code represents fictional numbers.

### Parameters

None

### Returns

Returns a United States phone number in the `utf8mb4` character set.

### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT gen_rnd_us_phone();
```

??? example "Expected output"

    ```{.text .no-copy}
    +--------------------+
    | gen_rnd_us_phone() |
    +--------------------+
    | 1-555-249-2029     |
    +--------------------+
    ```

## gen_rnd_uuid()

Generates a version 4 Universally Unique Identifier (UUID).

### Parameters

None.

### Returns

Returns a UUID as a string in the `utf8mb4` character set.

### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT gen_rnd_uuid();
```

??? example "Expected output"

    ```{.text .no-copy}
    +------------------------------------+
    | gen_rnd_uuid()                     |
    +------------------------------------+
    |9a3b642c-06c6-11ee-be56-0242ac120002|
    +------------------------------------+
    ```

## mask_canada_sin(str [,mask_char])

Masks a Canada Social Insurance Number (SIN).

### Parameters

| Parameter | Optional | Description | Type |
| --- | --- | --- | --- |
| `str` | No | The string to be masked | String |
| `mask_char` | Yes | The masking character | String |

The `str` accepts an alphanumeric string.

If you do not specify a `mask_char`, the default character is `X`. The `mask_char` value can be a multibyte character in any character set and may not be same character set as `str`.

### Returns

A string with the selected characters masked by a specified `mask_char` or the default value for that parameter. The function supports multibyte characters in any character set. The character set of the return value is the same as `str`.

An error is reported if  `str` length is an incorrect length.

Returns a NULL if you invoke this function with NULL as the primary argument.

### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT mask_canada_sin('555-555-555');
```

??? example "Expected output"

    ```{.text .no-copy}
    +--------------------------------+
    | mask_canada_sin('555-555-555') |
    +--------------------------------+
    | XXX-XXX-XXX                    |
    +--------------------------------+
    ```

## mask_iban(str [,mask_char])

Masks an Internal Bank Account Number (IBAN).

### Parameters

| Parameter | Optional | Description | Type |
| --- | --- | --- | --- |
| `str` | No | The string to be masked | String |
| `mask_char` | Yes | Character used for masking | String |

The `str` accepts either of the following:

* No separator symbol

* Groups of four characters. These groups can be separated by a space or any separator character.

The default value for `mask_char` is `*`. The value can be a multibyte character in any character set and may not be same character set as `str`.

### Returns

Returns the masked string. The character set of the result is the same as the character set of `str`.

An error is reported if the `str` length is incorrect.

Returns NULL if you invoke this function with NULL as the primary argument.

### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT mask_iban('DE27 1002 02003 77495 4156');
```

??? example "Expected output"

    ```{.text .no-copy}
    +---------------------------------------------+
    | mask_iban('DE27 1002 02003 77495 4156')     |
    +---------------------------------------------+
    | DE** **** **** **** ****                    |
    +---------------------------------------------+
    ```

## mask_inner(str, margin1, margin2 [,mask_char])

Returns the string where a selected inner portion is masked with a substitute character.

### Parameters

| Parameter | Optional | Description | Type |
| --- | --- | --- | --- |
| `string` | No | The string to be masked | String |
| `margin1` | No | The number of characters on the left end of the string to remain unmasked | Integer |
| `margin2` | No | The number of characters on the right end of the string to remain unmasked | Integer |
| `mask_char` | Yes | The masking character | String |

The `margin1` value cannot be a negative number. A value of `0` (zero) masks all characters.

The `margin2` value cannot be a negative number. A value of `0` (zero) masks all characters.

If the sum of `margin1` and `margin2` is greater than or equal to the string length, no masking occurs.

If the `mask_char` is not specified, the default is 'X'. The `mask_char` value can be a multibyte character in any character set and may not be same character set as `str`.

### Returns

A string with the selected characters masked by a specified `mask_char` or that parameter's default value in the character set of the `string` parameter.

Returns NULL if you invoke this function with NULL as the primary argument.

### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT mask_inner('123456789', 1, 2);
```

??? example "Expected output"

    ```{.text .no-copy}
    +-----------------------------------+
    | mask_inner('123456789', 1, 2)     |
    +-----------------------------------+
    | 1XXXXXX89                          |
    +-----------------------------------+
    ```

## mask_outer(str, margin1, margin2 [,mask_char])

Returns the string where a selected outer portion is masked with a substitute character.

### Parameters

| Parameter | Optional | Description | Type |
| --- | --- | --- | --- |
| `string` | No | The string to be masked | String |
| `margin1` | No | On the left end of the string, mask this designated number of characters | Integer |
| `margin2` | No | On the right end of the string, mask this designated number of characters | Integer |
| `mask_char` | Yes | The masking character | String |

The `margin1` cannot be a negative number. A value of `0` (zero) does not mask any characters.

The `margin2` cannot be a negative number. A value of `0` (zero) does not mask any characters.

If the sum of `margin1` and `margin2` is greater than or equal to the string length, the string is masked.

If the `mask_char` is not specified, the default is 'X'. The `mask_char` value can be a multibyte character in any character set and may not be same character set as `str`.

### Returns

A string with the selected characters masked by a specified `mask_char` or that parameter's default value in the same character set as `string`.

Returns NULL if you invoke this function with NULL as the primary argument.

### Example

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

## mask_pan(str [,mask_char])

Returns a masked payment card Primary Account Number (PAN). The mask replaces the PAN number with the specified character except for the last four digits.

### Parameters

| Parameter | Optional | Description | Type |
| --- | --- | --- | --- |
| `str` | No | The string to be masked | String |
| `mask_char` | Yes | The masking character | String |

The `str` contains a minimum of 14 or a maximum of 19 alphanumeric characters. 

If the `mask_char` is not specified, the default value is 'X'. The `mask_char` value can be a multibyte character in any character set and may not be same character set as `str`.

### Returns

A string with the selected characters masked by a specified `mask_char` or that parameter's default value. The character set of the result is the same character set as `str`.

An error occurs if the `str` parameter is not the correct length.

Returns NULL if you invoke this function with NULL as the primary argument.

### Example

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

## mask_pan_relaxed(str [,mask_char])

Returns a masked payment card Primary Account Number (PAN). The first six numbers and the last four numbers and the rest of the string masked by specified character or `X`.

### Parameters

| Parameter | Optional | Description | Type |
| --- | --- | --- | --- |
| `str` | No | The string to be masked | String |
| `mask_char` | Yes | The specified character for masking | String |

The `str` must contain a minimum of 14 or a maximum of 19 alphanumeric characters. 

If the `mask_char` is not specified, the default value is 'X'.

### Returns

A string with the first six numbers and the last four numbers and the rest of the string masked by a specified `mask_char` or that parameter's default value (`X`). The character set of the result is the same character set as `str`.

The `mask_char` value can be a multibyte character in any character set and may not be same character set as `str`.

Reports an error is the `str` parameter is not the correct length.

Returns NULL if you invoke this function with NULL as the primary argument.

### Example

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

## mask_ssn(str [,mask_char])

Returns a masked United States Social Security Number(SSN). The mask replaces the SSN number with the specified character except for the last four digits.

### Parameters

| Parameter | Optional | Description | Type |
| --- | --- | --- | --- |
| `str` | No | The string to be masked | String |
| `mask_char` | Yes | The masking character | String |

The `str` accepts either of the following:

* Nine integers, no separator symbol
* Nine integers in the `AAA-GG-SSS` pattern. The `-` (dash symbol) is the separator character.

If the `mask_char` is not specified, the default value is `*`. The `mask_char` value can be a multibyte character in any character set and may not be same character set as `str`.

### Returns

A string with the selected characters masked by a specified `mask_char` or that parameter's default value in the same character set of `str`. 

Reports an error if the value of the `str` is an incorrect length.

Returns a NULL value if you invoke this function with NULL as the primary argument.

### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT mask_ssn('555-55-5555', 'X');
```

??? example "Expected output"

    ```{.text .no-copy}
    +-----------------------------+
    | mask_ssn('555-55-5555','X') |
    +-----------------------------+
    | XXX-XX-5555                 |
    +-----------------------------+
    ```

## mask_uk_nin(str [,mask_char])

Returns a masked a United Kingdom National Insurance Number (NIN). The mask replaces the NIN number with the specified character except for the first two digits.

### Parameters

| Parameter | Optional | Description | Type |
| --- | --- | --- | --- |
| `str` | No | The string to be masked | String |
| `mask_char` | Yes | The masking character | String |

The `str` accepts an alpha-numeric string and does not check format and the `str` can use any separator character.

If the `mask_char` is not specified, the default value is `*`. The `mask_char` value can be a multibyte character in any character set and may not be same character set as `str`.

### Returns

Returns a string with the selected characters masked by a specified `mask_char` or that parameter's default value in the same character set as `str`.

An error occurs if the `str` parameter is not the correct length. 

Returns a NULL value if you invoke this function with NULL as the primary argument.

### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT mask_uk_nin ('CT 26 46 83 D');
```

??? example "Expected output"

    ```{.text .no-copy}
    +------------------------------------+
    | mask_uk_nin('CT 26 46 83 D')       |
    +------------------------------------+
    | CT ** ** ** *                      |
    +------------------------------------+
    ```

## mask_uuid(str [,mask_char])

Masks a Universally Unique Identifier (UUID).

### Parameters

| Parameter | Optional | Description | Type |
| --- | --- | --- | --- |
| `str` | No | The string to be masked | String |
| `mask_char` | Yes | The masking character | String |

The `str` format is `********-****-****-****-************`.

If the `mask_char` is not specified, the default value is '*'. The `mask_char` value can be a multibyte character in any character set and may not be same character set as `str`.

### Returns

A string with the characters masked by a specified `mask_char` or that parameter's default value in the same character set as `str`.

Returns an error if the length of `str` is incorrect.

Returns `NULL` if you invoke this function with NULL as the primary argument.

### Example


```{.bash data-prompt="mysql>"}
mysql> SELECT mask_uuid('9a3b642c-06c6-11ee-be56-0242ac120002');
```

??? example "Expected output"

    ```{.text .no-copy}
    +-------------------------------------------------------+
    | mask_uuid('9a3b642c-06c6-11ee-be56-0242ac120002')     |
    +-------------------------------------------------------+
    |********_****_****_****_************                   |
    +-------------------------------------------------------+
    ```

## masking_dictionary_remove(dictionary_name)

Removes all of the terms and then removes the dictionary. 

Requires the `MASKING_DICTIONARIES_ADMIN` privilege.

### Parameters

| Parameter | Optional | Description | Type |
| --- | --- | --- | --- |
| `dictionary_name` | No | The dictionary to be removed | String |


### Returns

Returns a string value of `1` (one) in the `utf8mb4` character set if the operation is successful or `NULL` if the operation could not find the `dictionary_name`.

### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT masking_dictionary_remove('trees');
```

??? example "Expected output"

    ```{.text .no-copy}
    +------------------------------------------+
    | masking_dictionary_remove('trees')       |
    +------------------------------------------+
    |                                        1 |
    +------------------------------------------+
    ```

## masking_dictionary_term_add(dictionary_name, term_name)

Adds a term to the dictionary and requires the `MASKING_DICTIONARIES_ADMIN` privilege.

### Parameters

| Parameter | Optional | Description | Type |
| --- | --- | --- | --- |
| `dictionary_name` | No | The dictionary where the term is added | String |
| `term_name` | No | The term added to the selected dictionary | String |


### Returns

Returns a string value of `1` (one) in the `utf8mb4` character set if the operation is successful. If the `dictionary_name` does not exist, the operation creates the dictionary.

Returns `NULL` if the operation fails. An operation can fail if the `term_name` is already available in the dictionary specified by `dictionary_name`.

The operation uses `INSERT IGNORE` and can have the following outcomes:

* The `term_name` is truncated if the `term_name` length is greater than maximum length of the `Term` field in the `mysql.masking_dictionaries` table.

* The character of the `dictionary_name` is not supported by the `Dictionary` field in `mysql.masking_dictionaries` table, the character is implicitly  converted to '?'. 

* If the character of the `term_name` is not supported by the `Term` field in the `mysql.masking_dictionaries` table, the character is implicitly converted to '?'.

The following command returns the table information:

```{.bash data-prompt="mysql>"}
mysql> DESCRIBE mysql.masking_dictionaries;
```

The result returns the table structure.

??? example "Expected output"

    ```{.text .no-copy}
    +------------+--------------+------+-----+---------+-------+
    | Field      | Type         | Null | Key | Default | Extra |
    +------------+--------------+------+-----+---------+-------+
    | Dictionary | varchar(256) | NO   | PRI | NULL    |       |
    | Term       | varchar(256) | NO   | PRI | NULL    |       |
    +------------+--------------+------+-----+---------+-------+
    2 rows in set (0.02 sec)
    ```

Modify the table with an `ALTER TABLE` statement, if needed.

### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT masking_dictionary_term_add('trees','pine');
```

??? example "Expected output"

    ```{.text .no-copy}
    +-----------------------------------------------+
    | masking_dictionary_term_add('trees', 'pine')  |
    +-----------------------------------------------+
    |                                             1 |
    +-----------------------------------------------+
    ```

## masking_dictionary_term_remove(dictionary_name, term_name)

Removes the selected term from the dictionary. 

Requires the `MASKING_DICTIONARIES_ADMIN` privilege.

### Parameters

| Parameter | Optional | Description | Type |
| --- | --- | --- | --- |
| `dictionary_name` | No | The dictionary that contains the `term_name` | String |
| `term_name` | No | The term to be removed | String |

### Returns

Returns a string value of `1` (one) in the `utf8mb4` character set if the operation is successful.

Returns `NULL` if the operation fails. An operation can fail if the following occurs:

* The `term_name` is not available in the dictionary specified by `dictionary_name`
* The `dictionary_name` could not be found


### Parameters

| Parameter | Optional | Description | Type |
| --- | --- | --- | --- |
| `dictionary_name` | No | The dictionary for the term | String |
| `term_name` | No | The term to be added | String |

### Example

```{.bash data-prompt="mysql>"}
mysql> SELECT masking_dictionary_term_remove('trees','pine');
```

??? example "Expected output"

    ```{.text .no-copy}
    +-------------------------------------------------------+
    | masking_dictionary_term_remove('trees', 'pine')       |
    +-------------------------------------------------------+
    |                                                     1 |
    +-------------------------------------------------------+
    ```
