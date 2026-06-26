The following example is a global manifest file that does not use local manifests:

```json
{
 "read_local_manifest": false,
 "components": "file://component_keyring_vault"
}
```

The following is an example of a global manifest file that points to a local manifest file:

```json
{
 "read_local_manifest": true
}
```

The following is an example of a local manifest file:

```json
{
 "components": "file://component_keyring_vault"
}
```

The configuration settings are either in a global configuration file or a local configuration file.

The following example is a global manifest file that does not use local
manifests:

```json
{
 "read_local_manifest": false,
 "components": "file://component_keyring_kms"
}
```

The following is an example of a global manifest file that points to a local manifest file:

```json
{
 "read_local_manifest": true
}
```

The following is an example of a local manifest file:

```json
{
 "components": "file://component_keyring_kms"
}
```

The configuration settings are either in a global configuration file or a local
configuration file. The settings are the same.

The following is an example of a global manifest file that does not use local manifests:

```json
{
 "read_local_manifest": false,
 "components": "file://component_keyring_kmip"
}
```

The following is an example of a global manifest file that points to a local manifest file:

```json
{
 "read_local_manifest": true
}
```

The following is an example of a local manifest file:

```json
{
 "components": "file://component_keyring_kmip"
}
```

The configuration settings are either in a global configuration file or a local configuration file. The settings are the same.
