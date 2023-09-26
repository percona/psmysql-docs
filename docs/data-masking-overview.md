# Data masking overview

Data masking helps to limit the exposure of sensitive data by preventing access to non-authorized users. Masking provides a way to create a version of the data in situations, such as a presentation, sales demo, or software testing, when the real data should not be used. Data masking changes the data values while using the same format and cannot be reverse engineered. Masking reduces an organization's risk by making the data useless to an outside party.

## Data masking techniques

The common data masking techniques are the following:

| Technique | Description |
| --- | --- |
| Custom string | Replaces sensitive data with a specific string, such as a phone number with XXX-XXX-XXXX |
| Data substitution | Replaces sensitive data with realistic alternative values, such as city name with another name from a dictionary |