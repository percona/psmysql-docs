# Data masking overview

Data masking protects sensitive information by restricting data access to authorized users only. When you need to present, demonstrate, or test software without revealing actual data, masking creates safe versions of your data. The masking process changes values while keeping the same data format, making the original values impossible to recover. This security approach reduces organizational risk because any exposed data becomes worthless to unauthorized parties.

Data masking in Percona Server for MySQL is an essential tool for protecting sensitive information in various scenarios:

| Scenario  | Description  |
|---|----|
| Protecting data in development and testing          | Developers and testers require realistic data to validate applications. By masking sensitive details, such as credit card numbers, Social Security numbers, and addresses, accurate user information can be safeguarded in non-production environments. |
| Compliance with data privacy regulations            | Stringent laws like GDPR, HIPAA, and CCPA mandate the protection of personal data. Data masking enables the anonymization of personal information, facilitating its use for analysis and reporting while ensuring compliance with regulations.               |
| Securing data when collaborating with external entities | Sharing data with third-party vendors demands the masking of sensitive information to prevent access to accurate personal details.                                                                                   |
| Supporting customer service and training            | Customer support teams and trainers often require access to customer data. Through data masking, they can utilize realistic information without compromising actual customer details.                                  |
| Facilitating data analysis and reporting            | Analysts rely on access to data for generating reports and uncovering insights. By employing data masking techniques, they can work with realistic data sets without compromising privacy.                             |

These examples underscore how data masking serves as a crucial safeguard for sensitive information, allowing organizations to leverage their data effectively across diverse functions.


## Version updates

Percona Server for MySQL 8.4.4-4 introduces performance improvements for data masking through an internal term cache. The cache affects the following functions in the [data masking component](data-masking-function-list.md):

* [gen_blocklist()](data-masking-function-list.md#gen_blockliststr-from_dictionary_name-to_dictionary_name)

* [gen_dictionary()](data-masking-function-list.md#gen_dictionarydictionary_name)

The new cache stores dictionary data in memory, making lookups faster than the previous method of querying the `<masking_functions.masking_database>.masking_dictionaries` table each time. This speed boost is especially noticeable when you're working with many rows of data.

However, the cache brings some new considerations. If you change the dictionary table directly (instead of using the proper dictionary management functions), your cache and table data can become different. 

The dictionary manipulation functions are the following:

* [`masking_dictionary_term_add()`](data-masking-function-list.md#masking_dictionary_term_adddictionary_name-term_name)

* [`masking_dictionary_term_remove()`](data-masking-function-list.md#masking_dictionary_term_removedictionary_name-term_name)

* [`masking_dictionary_remove()`](data-masking-function-list.md#masking_dictionary_removedictionary_name)

To fix this, you can use the new [`masking_dictionaries_flush()`](data-masking-function-list.md#masking_dictionaries_flush) function to sync them back up. This function returns `1` when successful.

The changes also affect how row-based replication works. When dictionary changes happen on the source server, they travel through the binary log to the replica server. While the replica applies these changes to its table correctly, the dictionary term cache doesn't update right away.

To handle this, there's a new component system variable called  [`component_masking_functions.dictionaries_flush_interval_seconds()`](data-masking-function-list.html#dictionaries_flush_interval_secondsinteger-unsigned)

By default, it's set to 0. When you set it higher, the system starts a background process that refreshes the cache at your specified interval. This helps replicas stay in sync after receiving binary log updates. The value specifies the number of seconds between each sync. 

## Data masking techniques

The common data masking techniques are the following:

| Technique | Description |
| --- | --- |
| Character substitution | Replaces sensitive data with a matching symbol (X,*). For example, a phone number becomes XXX-XXX-XXXX. |
| Value generation | Replaces sensitive data with realistic-looking alternative values. For example, for testing purposes, you can generate a realistic alternative United States Social Security Number. |

## Additional resources

Component:

[Install the data masking component](install-data-masking-component.md)

[Data masking component functions](data-masking-function-list.md)

Plugin:

[Install data masking plugin](install-data-masking-plugin.md)

[Data masking plugin funtions](data-masking-plugin-functions.md)
