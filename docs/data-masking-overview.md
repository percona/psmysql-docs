# Data masking overview

Data masking protects sensitive information by changing or replacing values so that readers see altered data instead of the originals. Use masking when you need to present, demonstrate, or test software without revealing real data. Masking keeps a similar data format, which reduces the risk of recovering originals.

Masking is a data transformation, not a substitute for access control. It works alongside MySQL privileges (RBAC—role-based access control). RBAC is MySQL’s privilege system: it determines which users and roles can read, write, or administer tables. Users who have permission to read the table see the masked result; the component does not by itself restrict access or prevent privilege escalation. You still need to grant only the minimum required privileges so that only authorized users can access the data at all. For small value domains (for example, gender or state codes), inference or frequency analysis may still reveal or narrow down originals. Treat masking as one layer of protection, not a guarantee of irreversibility.

Typical use cases:

| Use case | Description |
| --- | --- |
| Development and testing | Supply non-production environments with masked copies of sensitive fields (for example, payment card numbers, Social Security numbers, addresses) so applications can be validated without exposing real data. |
| Compliance (GDPR, HIPAA, CCPA, and similar) | Anonymize or pseudonymize personal data so that analysis and reporting can use the data while meeting regulatory requirements for protection of personal information. |
| Sharing data with third parties | Provide vendors or partners with datasets where sensitive columns are masked so that accurate personal details are not exposed. |
| Customer service and training | Give support or training staff access to data that looks realistic but does not contain real customer identifiers or PII. |
| Analysis and reporting on masked data | Run queries and reports on privacy-safe data. Generated values do not guarantee the same statistical distribution as originals; use for privacy-safe environments or design generation to preserve distributions where needed. |

Use masking as part of a broader data-protection and access-control strategy, not as the only safeguard.

The component offers two kinds of functions: those that mask existing values (for example, replace digits with a character) and those that generate replacement values (for example, random SSNs or emails). See [Data masking component functions](data-masking-function-list.md) for the full catalog and to find a function by task.

Next steps: [Install the data masking component](install-data-masking-component.md), then follow the [Data masking quickstart](quickstart-data-masking.md) to create a test database and try masking. The quickstart covers required privileges and working examples.

## Version updates

Percona Server for MySQL 8.4.4-4 adds an internal term cache that speeds up dictionary lookups. The cache affects [gen_blocklist()](data-masking-function-list.md#gen_blockliststr-from_dictionary_name-to_dictionary_name) and [gen_dictionary()](data-masking-function-list.md#gen_dictionarydictionary_name). Lookups are faster than querying the dictionary table each time, especially when processing many rows.

Memory use grows with the size of your dictionaries. For very large dictionaries, consider server memory and monitor resource use.

Cache and table can get out of sync if you change the dictionary table directly instead of using the management functions. Use the management functions to add or remove terms:

* [masking_dictionary_term_add()](data-masking-function-list.md#masking_dictionary_term_adddictionary_name-term_name)
* [masking_dictionary_term_remove()](data-masking-function-list.md#masking_dictionary_term_removedictionary_name-term_name)
* [masking_dictionary_remove()](data-masking-function-list.md#masking_dictionary_removedictionary_name)

If the cache and table do get out of sync, call [masking_dictionaries_flush()](data-masking-function-list.md#masking_dictionaries_flush) to resync them. The function returns `1` when successful.

Replication: Dictionary changes on the source are written to the binary log and applied to the replica’s table, but the replica’s term cache does not update immediately. During that lag, queries on the replica can see stale or inconsistent dictionary data. In sensitive or high-traffic setups, unmasked or incorrectly masked data may be visible until the cache is refreshed.

To reduce that risk, set the [component_masking_functions.dictionaries_flush_interval_seconds](data-masking-function-list.md#dictionaries_flush_interval_secondsinteger-unsigned) variable to a positive value (for example, 60). A background process then refreshes the cache at that interval so replicas stay in sync. The default is 0 (no automatic refresh). 

## Limitations and security considerations

This component is a data-presentation tool, not a data-redaction tool. The component changes how data is shown in query results; the component does not redact stored data or enforce a full secure data lifecycle.

Referential integrity: The component does not enforce consistency across tables. The same logical identifier (for example, a customer ID) can be masked to different values in different tables. If you need consistent masked identities for joins or testing, use deterministic masking so the same input always maps to the same output (for example, [`gen_blocklist()`](data-masking-function-list.md#gen_blockliststr-from_dictionary_name-to_dictionary_name) with the same dictionaries, or a single mapping in application logic).

Access control: Masking in a `SELECT` only protects that query. Users with `SELECT` on the base table can bypass masking by querying the table directly. Restrict access to views or stored procedures that apply the masking functions.

Views are not a complete boundary. Users with `SHOW CREATE VIEW` can see underlying table and column names; users with `FILE` or other privileges may read data outside the SQL layer. Secure the rest of the stack separately. Do not grant `UPDATE` or `INSERT` to users who should only see masked data; writing masked values back into the database corrupts real data. Treat masking as read-only presentation and control write access separately.

Partial masking: Functions that leave part of a value visible (for example, last four digits) can allow re-identification when combined with other data. Consider k-anonymity and your threat model.

Logs (slow query log, general query log, binary logs) may record query text or parameters. Restrict log access or redact as required. The component transforms values at query time; stored data is not altered. Behavior for empty strings or malformed identifiers is not fully specified; poor data quality can undermine masking.

Granting privileges to `mysql.session` on the dictionary table has security implications; the documentation does not prove the absence of privilege escalation. Regional functions (for example, `mask_canada_sin`, `mask_uk_nin`, `mask_iban`) are not documented as compliant with current regulatory or format requirements in those jurisdictions; verify for your use case.

Masking is applied per query, so the same column can appear differently in different contexts. Use views or standardized patterns for a consistent policy. For very large dictionaries, performance and memory use depend on size and workload; see the [function list](data-masking-function-list.md) for cache behavior and operational notes.

## Additional resources

* [Install the data masking component](install-data-masking-component.md)
* [Uninstall the data masking component](uninstall-data-masking-component.md)
* [Data masking component functions](data-masking-function-list.md)
* [Data masking quickstart](quickstart-data-masking.md) — test database and examples

