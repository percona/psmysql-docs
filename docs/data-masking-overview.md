# Data masking overview

Data masking protects sensitive information by blocking unauthorized users from accessing the real data. This process creates altered versions of data for specific uses, like presentations, sales demonstrations, or software testing. The masked data keeps the same format as the original but contains changed values that cannot be reversed to reveal the true information. By making the data worthless to outsiders, masking helps organizations reduce their risk of data breaches or misuse. Companies can safely use masked data in various scenarios without exposing confidential details to unauthorized parties.

Data masking in Percona Server for MySQL is an essential tool for protecting sensitive information in various scenarios:

| Scenario  | Description  |
|---|----|
| Protecting data in development and testing          | Developers and testers require realistic data to validate applications. By masking sensitive details, such as credit card numbers, Social Security numbers, and addresses, accurate user information can be safeguarded in non-production environments. |
| Compliance with data privacy regulations            | Stringent laws like GDPR, HIPAA, and CCPA mandate the protection of personal data. Data masking enables the anonymization of personal information, facilitating its use for analysis and reporting while ensuring compliance with regulations.               |
| Securing data when collaborating with external entities | Sharing data with third-party vendors demands the masking of sensitive information to prevent access to accurate personal details.                                                                                   |
| Supporting customer service and training            | Customer support teams and trainers often require access to customer data. Through data masking, they can utilize realistic information without compromising actual customer details.                                  |
| Facilitating data analysis and reporting            | Analysts rely on access to data for generating reports and uncovering insights. By employing data masking techniques, they can work with realistic data sets without compromising privacy.                             |

These examples underscore how data masking serves as a crucial safeguard for sensitive information, allowing organizations to leverage their data effectively across diverse functions.

Data masking helps to limit the exposure of sensitive data by preventing access to non-authorized users. Masking provides a way to create a version of the data in situations, such as a presentation, sales demo, or software testing, when the real data should not be used. Data masking changes the data values while using the same format and cannot be reverse engineered. Masking reduces an organization's risk by making the data useless to an outside party.

## Data masking techniques

The common data masking techniques are the following:

| Technique | Description |
| --- | --- |
| Custom string | Replaces sensitive data with a specific string, such as a phone number with XXX-XXX-XXXX |
| Data substitution | Replaces sensitive data with realistic alternative values, such as city name with another name from a dictionary |

## Additional resources

Component:

[Install the data masking component](install-data-masking-component.md)

[Data masking component functions](data-masking-function-list.md)

Plugin:

[Install data masking plugin](install-data-masking-plugin.md)

[Data masking plugin funtions](data-masking-plugin-functions.md)
