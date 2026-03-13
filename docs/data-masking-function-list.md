# Data masking component functions and variables

The feature is in [tech preview](glossary.md#tech-preview). This page is a catalog of individual functions and variables. For the security model, use cases, and when to apply masking (including limitations and failure modes), see [Data masking overview](data-masking-overview.md) and the [Limitations and security considerations](data-masking-overview.md#limitations-and-security-considerations) section. Performance characteristics (latency, complexity, scalability) are not documented; for large result sets or SLA-critical workloads, benchmark and evaluate per-row overhead. The component does not provide a function to test whether a value is already masked; auditing that masking has been applied to required rows must be done by application logic, known patterns, or other tooling.

To find a function by what the function does, use the "Find by task" table or the full list below. Each function name links to that function's definition later on this page.

### Find by task

| If you want to… | Function(s) |
| --- | --- |
| Mask or generate a payment card number (PAN) | [`mask_pan`](#mask_panstr-mask_char), [`mask_pan_relaxed`](#mask_pan_relaxedstr-mask_char), [`gen_rnd_pan`](#gen_rnd_pan) |
| Mask or generate a US Social Security number (SSN) | [`mask_ssn`](#mask_ssnstr-mask_char), [`gen_rnd_ssn`](#gen_rnd_ssn) |
| Mask or generate a Canadian SIN | [`mask_canada_sin`](#mask_canada_sinstr-mask_char), [`gen_rnd_canada_sin`](#gen_rnd_canada_sin) |
| Mask or generate a UK National Insurance number | [`mask_uk_nin`](#mask_uk_ninstr-mask_char), [`gen_rnd_uk_nin`](#gen_rnd_uk_nin) |
| Mask or generate an IBAN | [`mask_iban`](#mask_ibanstr-mask_char), [`gen_rnd_iban`](#gen_rnd_ibancountry-size) |
| Mask or generate a UUID | [`mask_uuid`](#mask_uuidstr-mask_char), [`gen_rnd_uuid`](#gen_rnd_uuid) |
| Generate a random email or US phone number | [`gen_rnd_email`](#gen_rnd_emailname_size-surname_size-domain), [`gen_rnd_us_phone`](#gen_rnd_us_phone) |
| Mask the middle or the ends of any string | [`mask_inner`](#mask_innerstr-margin1-margin2-mask_char), [`mask_outer`](#mask_outerstr-margin1-margin2-mask_char) |
| Replace a value with a random term from a dictionary | [`gen_dictionary`](#gen_dictionarydictionary_name), [`gen_blocklist`](#gen_blockliststr-from_dictionary_name-to_dictionary_name) |
| Generate a number in a range | [`gen_range`](#gen_rangelower-upper) |
| Manage dictionaries (add/remove terms, flush cache) | [`masking_dictionary_term_add`](#masking_dictionary_term_adddictionary_name-term_name), [`masking_dictionary_term_remove`](#masking_dictionary_term_removedictionary_name-term_name), [`masking_dictionary_remove`](#masking_dictionary_removedictionary_name), [`masking_dictionaries_flush`](#masking_dictionaries_flush) |

### Full list (by name)

| Name                                              | Details                                                |
|---------------------------------------------------|-------------------------------------------------------|
| [`gen_blocklist(str, from_dictionary_name, to_dictionary_name)`](#gen_blockliststr-from_dictionary_name-to_dictionary_name) | If the input is in the source dictionary, returns a random term from the target dictionary; otherwise returns the input |
| [`gen_dictionary(dictionary_name)`](#gen_dictionarydictionary_name) | Returns a random term from a dictionary               |
| [`gen_range(lower, upper)`](#gen_rangelower-upper) | Returns a number from a range                       |
| [`gen_rnd_canada_sin()`](#gen_rnd_canada_sin) | Generates a Canadian Social Insurance number          |
| [`gen_rnd_email([name_size, surname_size, domain])`](#gen_rnd_emailname_size-surname_size-domain)    | Generates a random string in name.surname@domain format |
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
| [`masking_dictionaries_flush()`](#masking_dictionaries_flush) | Resyncs the internal dictionary term cache |
| [`masking_dictionary_remove(dictionary_name)`](#masking_dictionary_removedictionary_name)          | Removes the dictionary                                |
| [`masking_dictionary_term_add(dictionary_name, term_name)`](#masking_dictionary_term_adddictionary_name-term_name)     | Adds a term to the masking dictionary                 |
| [`masking_dictionary_term_remove(dictionary_name, term_name)`](#masking_dictionary_term_removedictionary_name-term_name)      | Removes a term from the masking dictionary            |

## Permissions

The dictionary-related functions do not run internal queries as the root user without a password. Following MySQL best practices, many admins disable the `root` user, which previously caused these functions to stop working. The server uses the built-in `mysql.session` user to execute dictionary queries. 

However, for dictionary operations to work, you need to grant the mysql.session user `SELECT`, `INSERT`, `UPDATE`, and `DELETE` privileges on the `masking_dictionaries` table. Granting `UPDATE` and `DELETE` allows the server to modify or remove dictionary data. Compromise of the server or abuse of that user could allow dictionary tampering or deletion, causing dictionary-based functions to fail or return unexpected values; protect the server and the `mysql` schema accordingly.

```sql
GRANT SELECT, INSERT, UPDATE, DELETE ON mysql.masking_dictionaries TO 'mysql.session'@'localhost';
```

If you change the value of the `masking_functions.masking_database` system variable to something other than `mysql`, make sure to update the `GRANT` query to match the new value.

```sql
GRANT SELECT, INSERT, UPDATE, DELETE ON <masking_functions.masking_database>.masking_dictionaries TO 'mysql.session'@'localhost';
```

## Limitations and operational notes

* Character set and collation: Several functions accept a `mask_char` that can be in a different character set than the input string. When the character sets differ, the server must transcode the mask character; in some collations or storage contexts this can produce illegal byte sequences or errors. Prefer using a `mask_char` in the same character set as the input (or the target column) to avoid corruption or storage failures.

* Schema and format: Masking functions return strings (for example, containing `X` or `*`). If the target column or application enforces strict validation (numeric-only, regex, fixed width, or checksums such as Luhn for payment cards), the masked value may cause INSERT or UPDATE failures or break application logic. The component does not guarantee format-preserving or type-preserving output; choose mask character and usage so that results remain valid for the target schema and application.

* Randomness: Functions that return "random" values (for example, `gen_dictionary`, `gen_blocklist`, `gen_rnd_*`) do not document that the randomness is cryptographically secure or unpredictable. The selection or generation logic is not necessarily resistant to prediction; do not rely on that logic to resist inference attacks (for example, an attacker with partial data might infer mappings).

* Collision and uniqueness: The `gen_rnd_*` functions do not document entropy source or collision probability. At scale (for example, millions of rows), duplicate generated values are possible and can violate unique constraints or make the dataset unsuitable for integration testing. Evaluate uniqueness requirements before relying on these generators for large datasets.

* Default mask character: The default masking character (for example, `X` or `*`) may not suit all use cases. For fixed-width fields, padding, or systems that expect specific formats or checksums (for example, Luhn for payment cards), the default can break validation. Choose mask character and format to match the target schema and application requirements.

* Performance at scale: Applying masking functions to very large result sets (for example, tens or hundreds of millions of rows) can add significant CPU and memory cost. No performance guarantees or benchmarks are documented. Test and monitor when using these functions in heavy reporting or large SELECTs to avoid resource exhaustion or denial-of-service risk.

* Aggregation and inference: Row-level masking affects how values are displayed in results; such masking does not necessarily protect against inference via aggregates. Depending on implementation, `SUM()`, `AVG()`, or other aggregates may be computed over unmasked data in the execution engine. Do not assume that masking in the result set prevents leakage through aggregate queries; consider differential privacy or aggregate-level protection if that is a threat.

* Boundary behavior: For `mask_outer`, when the sum of `margin1` and `margin2` is greater than or equal to the string length, the entire string is replaced with the mask character (the whole string is masked). For `mask_inner`, when that sum is greater than or equal to the string length, no masking occurs (the string is returned unchanged).

* Validation: The component does not provide a function to check whether a value is already masked. To audit that required rows or columns have been masked, use application logic, schema conventions, or external tooling.

## gen_blocklist(str, from_dictionary_name, to_dictionary_name)

If `str` is present in the dictionary named `from_dictionary_name`, returns a randomly selected term from the dictionary named `to_dictionary_name`. Otherwise returns `str` unchanged. The selection is not documented as cryptographically secure; do not rely on the selection to resist prediction or inference (see [Limitations and operational notes](#limitations-and-operational-notes)).
  
Percona Server for MySQL uses an internal term cache. The server uses in-memory data structures for lookups instead of querying the `<masking_functions.masking_database>.masking_dictionaries` table every time. This improvement boosts performance, especially when handling multiple rows.

### Parameters

| Parameter | Optional | Description | Type |
| --- | --- | --- | --- |
| `str` | No | The input value to look up and optionally replace | String |
| `from_dictionary_name` | No | The dictionary in which `str` must be found for replacement to occur | String |
| `to_dictionary_name` | No | The dictionary from which a replacement term is chosen at random | String |

### Returns

If `str` is in `from_dictionary_name`, a randomly selected term from `to_dictionary_name`. If `str` is not in `from_dictionary_name` or either dictionary is missing, `str` unchanged. If `to_dictionary_name` does not exist, NULL. Returns NULL if `str` is NULL. The character set of the returned string is the same as `str`.

### Example

```sql
SELECT gen_blocklist('apple', 'fruit', 'nut');
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

Returns a term from a dictionary selected at random. The selection is not documented as cryptographically secure; do not rely on the selection to resist prediction or inference (see [Limitations and operational notes](#limitations-and-operational-notes)).

Percona Server for MySQL uses an internal term cache. The server uses in-memory data structures for lookups instead of querying the `<masking_functions.masking_database>.masking_dictionaries` table every time. This improvement boosts performance, especially when handling multiple rows.

### Parameters

| Parameter | Optional | Description | Type |
| --- | --- | --- | --- |
| `dictionary_name` | No | Select the random term from this dictionary | String |


### Returns

A random term from the dictionary listed in `dictionary_name` in the `utf8mb4` character set. Returns NULL if the `dictionary_name` does not exist.

### Example

```sql
SELECT gen_dictionary('trees');
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

```sql
SELECT gen_range(10, 100);
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

Returns a Canada SIN formatted in three groups of three digits (for example, 123-456-789) in the `utf8mb4` character set. To ensure the number is consistent, the number is verified with the [Luhn algorithm :octicons-link-external-16:](https://en.wikipedia.org/wiki/Luhn_algorithm).

### Example

```sql
SELECT gen_rnd_canada_sin();
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

Generates a random string in the `name.surname@domain` format.

### Parameters

| Parameter | Optional | Description | Type |
| --- | --- | --- | --- |
| `name_size` | Yes | Specifies the number of characters in the name part. The default number is five. The minimum number is one. The maximum number is 1024. | Integer |
| `surname_size` | Yes | Specifies the number of characters in the surname part. The default number is seven. The minimum number is one. The maximum number is 1024. | Integer |
| `domain` | Yes | Specifies the domain name used. The default value is `example.com`. | String |


### Returns

A generated string in the same character set as `domain`. If the `domain` value is not specified, then the string is in the `utf8mb4` character set. The `name` and `surname` are random lower-case letters (a - z). For columns with a unique constraint, duplicates are possible at scale; see Collision and uniqueness in [Limitations and operational notes](#limitations-and-operational-notes).

### Example

```sql
SELECT gen_rnd_email(name_size=4, surname_size=5, domain='example.test');
```

??? example "Expected output"

    ```{.text .no-copy}
    +----------------------------------------+
    | gen_rnd_email(4, 5, 'example.test')   |
    +----------------------------------------+
    | qwer.asdfg@example.test               |
    +----------------------------------------+
    ```

## gen_rnd_iban([country, size])

Generates an International Bank Account Number (IBAN).

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

```sql
SELECT gen_rnd_iban();
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

```sql
SELECT gen_rnd_pan();
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

An SSN string in nine-digit format "AAA-GG-SSSS" in the `utf8mb4` character set. The number has three parts, the first three digits are the area number, the group number, and the serial number. The generated SSN uses '900' or greater numbers for the area number. These numbers are not legitimate because they are outside the approved range.

### Example

```sql
SELECT gen_rnd_ssn();
```

??? example "Expected output"

    ```{.text .no-copy}
    +----------------+
    | gen_rnd_ssn()  |
    +----------------+
    | 970-03-0370    |
    +----------------+
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

```sql
SELECT gen_rnd_uk_nin();
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

```sql
SELECT gen_rnd_us_phone();
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

```sql
SELECT gen_rnd_uuid();
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

If you do not specify a `mask_char`, the default character is `X`. The `mask_char` value can be a multibyte character in any character set and may not be the same character set as `str`. See [Limitations and operational notes](#limitations-and-operational-notes) for character set and collation caveats when `mask_char` differs from the input.

### Returns

A string with the selected characters masked by a specified `mask_char` or the default value for that parameter. The function supports multibyte characters in any character set. The character set of the return value is the same as `str`.

An error is reported if  `str` length is an incorrect length.

Returns a NULL if you invoke this function with NULL as the primary argument.

### Example

```sql
SELECT mask_canada_sin('555-555-555');
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

Masks an International Bank Account Number (IBAN).

### Parameters

| Parameter | Optional | Description | Type |
| --- | --- | --- | --- |
| `str` | No | The string to be masked | String |
| `mask_char` | Yes | Character used for masking | String |

The `str` accepts either of the following:

* No separator symbol

* Groups of four characters. These groups can be separated by a space or any separator character.

The default value for `mask_char` is `*`. The value can be a multibyte character in any character set and may not be the same character set as `str`. See [Limitations and operational notes](#limitations-and-operational-notes) for character set and collation caveats when `mask_char` differs from the input.

### Returns

Returns the masked string. The character set of the result is the same as the character set of `str`.

An error is reported if the `str` length is incorrect.

Returns NULL if you invoke this function with NULL as the primary argument.

### Example

```sql
SELECT mask_iban('DE27 1002 02003 77495 4156');
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
| `str` | No | The string to be masked | String |
| `margin1` | No | The number of characters on the left end of the string to remain unmasked | Integer |
| `margin2` | No | The number of characters on the right end of the string to remain unmasked | Integer |
| `mask_char` | Yes | The masking character | String |

The `margin1` value cannot be a negative number. A value of `0` (zero) masks all characters.

The `margin2` value cannot be a negative number. A value of `0` (zero) masks all characters.

If the sum of `margin1` and `margin2` is greater than or equal to the string length, no masking occurs. See [Limitations and operational notes](#limitations-and-operational-notes) for character set and collation caveats when `mask_char` differs from the input.

If the `mask_char` is not specified, the default is 'X'. The `mask_char` value can be a multibyte character in any character set and may not be the same character set as `str`.

### Returns

A string with the selected characters masked by a specified `mask_char` or that parameter's default value in the character set of `str`.

Returns NULL if you invoke this function with NULL as the primary argument.

### Example

```sql
SELECT mask_inner('123456789', 1, 2);
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
| `str` | No | The string to be masked | String |
| `margin1` | No | On the left end of the string, mask this designated number of characters | Integer |
| `margin2` | No | On the right end of the string, mask this designated number of characters | Integer |
| `mask_char` | Yes | The masking character | String |

The `margin1` cannot be a negative number. A value of `0` (zero) does not mask any characters.

The `margin2` cannot be a negative number. A value of `0` (zero) does not mask any characters.

If the sum of `margin1` and `margin2` is greater than or equal to the string length, the entire string is replaced with the mask character (the whole string is masked). See [Limitations and operational notes](#limitations-and-operational-notes) for character set and collation caveats when `mask_char` differs from the input.

If the `mask_char` is not specified, the default is 'X'. The `mask_char` value can be a multibyte character in any character set and may not be the same character set as `str`.

### Returns

A string with the selected characters masked by a specified `mask_char` or that parameter's default value in the same character set as `str`.

Returns NULL if you invoke this function with NULL as the primary argument.

### Example

```sql
SELECT mask_outer('123456789', 2, 2); 
```

??? example "Expected output"

    ```{.text .no-copy}
    +------------------------------------+
    | mask_outer('123456789', 2, 2)     |
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

If the `mask_char` is not specified, the default value is 'X'. The `mask_char` value can be a multibyte character in any character set and may not be the same character set as `str`. See [Limitations and operational notes](#limitations-and-operational-notes) for character set and collation caveats when `mask_char` differs from the input. For numeric-only columns or systems that validate Luhn checksums, the default character may be invalid; see Schema and format and Default mask character in that section.

### Returns

A string with the selected characters masked by a specified `mask_char` or that parameter's default value. The character set of the result is the same character set as `str`.

An error occurs if the `str` parameter is not the correct length.

Returns NULL if you invoke this function with NULL as the primary argument.

### Example

```sql
SELECT mask_pan (gen_rnd_pan());
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

Returns a masked payment card Primary Account Number (PAN). Leaves the first six and last four digits unmasked; the rest is masked by the specified character or `X`.

### Parameters

| Parameter | Optional | Description | Type |
| --- | --- | --- | --- |
| `str` | No | The string to be masked | String |
| `mask_char` | Yes | The specified character for masking | String |

The `str` must contain a minimum of 14 or a maximum of 19 alphanumeric characters. 

If the `mask_char` is not specified, the default value is 'X'.

### Returns

A string with the first six and last four digits unmasked and the rest masked by a specified `mask_char` or that parameter's default value (`X`). The character set of the result is the same character set as `str`.

The `mask_char` value can be a multibyte character in any character set and may not be the same character set as `str`. See [Limitations and operational notes](#limitations-and-operational-notes) for character set and collation caveats when `mask_char` differs from the input.

Reports an error if the `str` parameter is not the correct length.

Returns NULL if you invoke this function with NULL as the primary argument.

### Example

```sql
SELECT mask_pan_relaxed(gen_rnd_pan());
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
* Nine integers in the `AAA-GG-SSSS` pattern. The `-` (dash symbol) is the separator character.

If the `mask_char` is not specified, the default value is `*`. The `mask_char` value can be a multibyte character in any character set and may not be the same character set as `str`. See [Limitations and operational notes](#limitations-and-operational-notes) for character set and collation caveats when `mask_char` differs from the input.

### Returns

A string with the selected characters masked by a specified `mask_char` or that parameter's default value in the same character set as `str`. 

Reports an error if the value of the `str` is an incorrect length.

Returns a NULL value if you invoke this function with NULL as the primary argument.

### Example

```sql
SELECT mask_ssn('555-55-5555', 'X');
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

Returns a masked United Kingdom National Insurance Number (NIN). The mask replaces the NIN with the specified character except for the first two characters.

### Parameters

| Parameter | Optional | Description | Type |
| --- | --- | --- | --- |
| `str` | No | The string to be masked | String |
| `mask_char` | Yes | The masking character | String |

The `str` accepts an alpha-numeric string and does not check format and the `str` can use any separator character.

If the `mask_char` is not specified, the default value is `*`. The `mask_char` value can be a multibyte character in any character set and may not be the same character set as `str`. See [Limitations and operational notes](#limitations-and-operational-notes) for character set and collation caveats when `mask_char` differs from the input.

### Returns

Returns a string with the selected characters masked by a specified `mask_char` or that parameter's default value in the same character set as `str`.

An error occurs if the `str` parameter is not the correct length. 

Returns a NULL value if you invoke this function with NULL as the primary argument.

### Example

```sql
SELECT mask_uk_nin ('CT 26 46 83 D');
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

If the `mask_char` is not specified, the default value is '*'. The `mask_char` value can be a multibyte character in any character set and may not be the same character set as `str`. See [Limitations and operational notes](#limitations-and-operational-notes) for character set and collation caveats when `mask_char` differs from the input.

### Returns

A string with the characters masked by a specified `mask_char` or that parameter's default value in the same character set as `str`.

An error occurs if the length of `str` is incorrect.

Returns `NULL` if you invoke this function with NULL as the primary argument.

### Example

```sql
SELECT mask_uuid('9a3b642c-06c6-11ee-be56-0242ac120002');
```

??? example "Expected output"

    ```{.text .no-copy}
    +-------------------------------------------------------+
    | mask_uuid('9a3b642c-06c6-11ee-be56-0242ac120002')     |
    +-------------------------------------------------------+
    |********-****-****-****-************                   |
    +-------------------------------------------------------+
    ```


## masking_dictionaries_flush()

Resyncs the internal dictionary term cache.

### Parameters

None

### Returns

Returns an integer value of `1` (one) when successful.

### Example

```sql
SELECT masking_dictionaries_flush();
```
??? example "Expected output"

    ```{.text .no-copy}
    +------------------------------+
    | masking_dictionaries_flush() |
    +------------------------------+
    |                          1   |
    +------------------------------+
    ```
    
## masking_dictionary_remove(dictionary_name)

Removes all of the terms and then removes the dictionary. 

Requires the `MASKING_DICTIONARIES_ADMIN` privilege.

### Parameters

| Parameter | Optional | Description | Type |
| --- | --- | --- | --- |
| `dictionary_name` | No | The dictionary to be removed | String |


### Returns

Returns an integer value of `1` (one) if the operation is successful. Returns the integer value of `0` (zero) for a failure.

### Example

```sql
SELECT masking_dictionary_remove('trees');
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

Returns an integer value of `1` (one) if the operation is successful. Returns an integer value of `0` (zero) for a failure. If the `dictionary_name` does not exist, the operation creates the dictionary.

The operation uses `INSERT IGNORE` and can have the following outcomes:

* The `term_name` is truncated if the `term_name` length is greater than maximum length of the `Term` field in the `mysql.masking_dictionaries` table.

* The character of the `dictionary_name` is not supported by the `Dictionary` field in `mysql.masking_dictionaries` table, the character is implicitly  converted to '?'. 

* If the character of the `term_name` is not supported by the `Term` field in the `mysql.masking_dictionaries` table, the character is implicitly converted to '?'.

The following command returns the table information:

```sql
DESCRIBE mysql.masking_dictionaries;
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

```sql
SELECT masking_dictionary_term_add('trees','pine');
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

Returns an integer value of `1` (one) if the operation is successful. Returns the integer value of `0` (zero) for a failure.

Returns `NULL` if the operation fails. An operation can fail if the following occurs:

* The `term_name` is not available in the dictionary specified by `dictionary_name`
* The `dictionary_name` could not be found

### Example

```sql
SELECT masking_dictionary_term_remove('trees','pine');
```

??? example "Expected output"

    ```{.text .no-copy}
    +-------------------------------------------------------+
    | masking_dictionary_term_remove('trees', 'pine')       |
    +-------------------------------------------------------+
    |                                                     1 |
    +-------------------------------------------------------+
    ```

## System variables


| Name                                              | Details                                                |
|---------------------------------------------------|-------------------------------------------------------|
| [`dictionaries_flush_interval_seconds (integer, unsigned)`](#dictionaries_flush_interval_secondsinteger-unsigned) | The number of seconds between updates to the internal dictionary cache to match changes in the dictionaries table.|
| [`masking_database(string)`](#masking_databasestring) | Set a different database name to use for the dictionaries table. |

### dictionaries_flush_interval_seconds(integer, unsigned)

| Option       | Description      |
|--------------|------------------|
| command-line | Yes              |
| scope        | Global           |
| data type    | unsigned integer |
| default      | 0            |

Variable name: `component_masking_functions.dictionaries_flush_interval_seconds`. You can set the variable at runtime (for example, with `SET GLOBAL`) or on the command line.

The number of seconds between synchronizations of the dictionaries table and the internal dictionary cache. The default value is 0 seconds (disabled). The minimum value is 1 second. The maximum value is 31,536,000 seconds (1 year).

Replication: On replicas that use row-based replication, the dictionary term cache is not updated immediately when dictionary changes are applied from the binary log. Set this variable to a positive value (for example, 60) so that a background process periodically refreshes the cache and keeps replicas in sync with the source.

### masking_database(string)

| Option         | Description        |
| -------------- | ------------------ |
| Scope:         | Global             |
| Read, Write, or Read-Only:     | Read-Only |
| Data type | String |
| Default value | "mysql" |

Specify the name of the database that holds the `masking_dictionaries` table. By default, the setting uses the `mysql` database.
