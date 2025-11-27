# Encryption functions

## Quick start guide

> ⚡ **Get Started in 5 Minutes**
> 
> ```sql
> -- Install the encryption component
> INSTALL COMPONENT 'file://component_encryption_udf';
> 
> -- Create keys
> SET @private_key = create_asymmetric_priv_key('RSA', 3072);
> SET @public_key = create_asymmetric_pub_key('RSA', @private_key);
> 
> -- Encrypt data
> SET @ciphertext = asymmetric_encrypt('RSA', 'Secret message', @public_key);
> 
> -- Decrypt data
> SET @plaintext = asymmetric_decrypt('RSA', @ciphertext, @private_key);
> ```
>
> See [complete examples](#examples-you-can-try) for more detailed use cases.

## Functions

> 🧰 **Cryptographic function library**
>
> The following section documents each cryptographic function available in the library. Each function is categorized by purpose with detailed implementation specifications.


### Function quick reference

| Category | Function   | What It Does  | Common Use Case  |
|----------|------------|---------------|-------------------|
| **Encryption**  | [asymmetric_encrypt()](#asymmetric_encryptalgorithm-str-key_str) | Puts your data in a math lockbox             | Protecting sensitive data   |
|                 | [asymmetric_decrypt()](#asymmetric_decryptalgorithm-crypt_str-key_str) | Opens the lockbox and gets your data back    | Retrieving protected data   |
| **Key Management** | [create_asymmetric_priv_key()](#create_asymmetric_priv_keyalgorithm-key_len) | Makes your secret key    | Creating your private key   |
|               | [create_asymmetric_pub_key()](#create_asymmetric_pub_keyalgorithm-priv_key_str) | Creates a shareable public key | Generating keys to distribute |
| **Digital Signatures** | [asymmetric_sign()](#asymmetric_signalgorithm-digest_str-priv_key_str-digest_type-padding) | Stamps your message with your secret key   | Proving a message is from you |
|                    | [asymmetric_verify()](#asymmetric_verifyalgorithm-digest_str-sig_str-pub_key_str-digest_type-padding) | Checks if a signature is real or fake  | Verifying message authenticity |


### Asymmetric encryption functions

These functions implement public key cryptography utilizing key pairs. The encryption and decryption operations require different keys from the same key pair.

| Function Name | Purpose |
| --- | --- |
| [asymmetric_encrypt](#asymmetric_encryptalgorithm-str-key_str) | Encrypts plaintext data using asymmetric cryptography. Only the corresponding key can decrypt. |
| [asymmetric_decrypt](#asymmetric_decryptalgorithm-crypt_str-key_str) | Decrypts ciphertext that was encrypted with the corresponding asymmetric key. |


### Asymmetric key management functions

These functions facilitate the generation and management of asymmetric cryptographic key pairs:

| Function Name | Description |
| --- | --- |
| [create_asymmetric_priv_key](#create_asymmetric_priv_keyalgorithm-key_len) | Generates a private key with specified algorithm and security parameters |
| [create_asymmetric_pub_key](#create_asymmetric_pub_keyalgorithm-priv_key_str) | Derives the corresponding public key from a private key for distribution |


### Digital Signature functions

These functions implement digital signature operations for message authentication and verification:

| Function Name | Description |
| --- | --- |
| [asymmetric_sign](#asymmetric_signalgorithm-digest_str-priv_key_str-digest_type-padding) | Applies a cryptographic signature to a message digest using a private key |
| [asymmetric_verify](#asymmetric_verifyalgorithm-digest_str-sig_str-pub_key_str-digest_type-padding) | Validates the authenticity of a digital signature using the corresponding public key |

### Diffie-Hellman functions

> 🤝 **Shared secret generation**
>
> These functions facilitate secure key exchange between parties through the Diffie-Hellman protocol without transmitting sensitive key material.

| Function Name | Description | Application |
| --- | --- | --- |
| [asymmetric_derive](#asymmetric_derivepub_key_str-priv_key_str) | Generates a shared cryptographic secret through asymmetric key combination | When implementing secure communication channels between parties |
| [create_dh_parameters](#create_dh_parameterskey_len) | Generates the prime numbers and parameters required for Diffie-Hellman key exchange | As a prerequisite for Diffie-Hellman key generation |


### Encryption threshold variables

> ⚙️ **System configuration**
>
> These settings let you control how strong your encryption can be. They're like speed limits for your security system.

Keys that are too strong might slow down your system. It's like having a super-heavy padlock that takes forever to open.

| Setting Name | What It Does | Default | Range  | Performance Impact |
|--------------|--------------|---------|--------|--------------------|
| [encryption_udf.dh_bits_threshold](#encryption_udfdh_bits_threshold) | Sets how strong Diffie-Hellman keys can be  | 10000   | 1024-10000   | Higher values significantly increase key generation time |
| [encryption_udf.dsa_bits_threshold](#encryption_udfdsa_bits_threshold) | Sets how strong DSA keys can be  | 9984  | 1024-9984 | Higher values increase key generation time   |
| [encryption_udf.rsa_bits_threshold](#encryption_udfrsa_bits_threshold) | Sets how strong RSA keys can be | 16384   | 1024-16384 | Higher values increase key generation and encryption/decryption time |
| [encryption_udf.legacy_padding](#encryption_udflegacy_padding_scheme) | Turns old-style padding on or off | OFF | ON/OFF | Minor impact on encryption speed, major impact on security  |

---


## Install component_encryption_udf

> 📦 **Installation Guide**
>
> Before you can lock up your data, you need to install your security tools.


### Quick installation steps

1. Use a simple command to add the encryption tools
2. Once you run the command, all the tools are ready right away
3. Best part: You don't need to run any complex setup commands!

You'll need the `INSERT` permission on the `mysql.component` table to install this. The system just adds one row to this table to remember the tools are installed.

```sql
-- Install the encryption component
INSTALL COMPONENT 'file://component_encryption_udf';

-- Verify installation
SELECT * FROM mysql.component;
```

!!! note

    If you're building Percona Server for MySQL from scratch, the encryption UDF component can be enabled or disabled using the `-DWITH_ENCRYPTION_UDF` CMake flag. By default, this flag is set to `ON`, meaning the encryption UDF component is built and included in the installation. If you want to build Percona Server without this component, you can disable it by setting `-DWITH_ENCRYPTION_UDF=OFF` during the CMake configuration stage of the build process.

## User-defined functions described

---


## Asymmetric_decrypt(*algorithm, crypt_str, key_str*)

> 🔓 **Data Decryption Function**
>
> This function decrypts ciphertext to recover the original plaintext using asymmetric cryptography.


### Quick reference

| Parameter | Required | Description |
|-----------|----------|-------------|
| algorithm | Yes | Cryptographic algorithm identifier (currently only 'RSA') |
| crypt_str | Yes | The encrypted data (ciphertext) to be decrypted |
| key_str | Yes | The decryption key in PEM format |
| padding | No | Padding scheme: 'no', 'pkcs1', or 'oaep' |


### Return value

The function returns the original plaintext message decoded from the ciphertext.


### Parameter details

* **algorithm** - Specifies the cryptographic algorithm to be used for decryption (currently only RSA is supported)

* **key_str** - The decryption key in PEM format. Requirements:
  * Must be properly formatted and valid
  * Must correspond to the encryption key used (public key if encrypted with private key, or private key if encrypted with public key)

* **crypt_str** - The encrypted binary data to be decrypted

* **padding** - Specifies the padding scheme implemented in version 8.0.41:
  * `no` - No padding (requires exact-size messages)
  * `pkcs1` - PKCS#1 v1.5 padding scheme
  * `oaep` - Optimal Asymmetric Encryption Padding (more secure)
  
  If not specified, the system uses the value from the encryption_udf.legacy_padding_scheme variable.

<details>
   <summary>Example usage</summary>
   
   ```sql
   -- Decrypt data using a private key
   SET @plaintext = asymmetric_decrypt('RSA', @ciphertext, @private_key, 'oaep');
   
   -- Verify the decrypted result
   SELECT @plaintext;
   ```
</details>
---


## Asymmetric_derive(*pub_key_str, priv_key_str*)

> 🤝 **Shared secret generation**
>
> This function implements the Diffie-Hellman key exchange protocol to establish a shared cryptographic secret between two parties without transmitting sensitive key material.


### Quick reference

| Parameter | Required | Description |
|-----------|----------|-------------|
| pub_key_str | Yes | The recipient's public key |
| priv_key_str | Yes | The initiator's private key |


### Required parameters

* **pub_key_str** - The recipient party's public key in PEM format

* **priv_key_str** - The initiator's private key in PEM format


### Return value

* Returns a cryptographic key value that will be identical for both parties when they perform their respective calculations

* The function enables secure symmetric key establishment without transmitting the actual secret key

<details>
   <summary>Example usage</summary>
   
   ```sql
   -- Generate a shared secret
   SET @shared_secret = asymmetric_derive(@their_public_key, @my_private_key);
   
   -- Use the shared secret for symmetric encryption
   -- Both parties will have the same shared secret
   ```
</details>
---


## Asymmetric_encrypt(*algorithm, str, key_str*)

> 🔒 **Data Encryption Function**
>
> This function transforms plaintext data into encrypted format using asymmetric cryptography. The encrypted data can only be decrypted with the corresponding key.


### Quick reference

| Parameter | Required | Description |
|-----------|----------|-------------|
| algorithm | Yes | Cryptographic algorithm identifier (currently only 'RSA') |
| str | Yes | The plaintext message to encrypt |
| key_str | Yes | The encryption key (public or private) in PEM format |
| padding | No | Padding scheme: 'no', 'pkcs1', or 'oaep' |


### Return value

The function returns the encrypted ciphertext as binary data.


### Parameter details

* **algorithm** - Specifies the cryptographic algorithm to be used for encryption (currently only RSA is supported)

* **str** - The plaintext data to be encrypted. Note that message length is constrained by the key size and padding scheme selected. Maximum message length must not exceed the key size minus padding overhead.

* **key_str** - The encryption key in PEM format (can be either a public or private key depending on implementation requirements)

* **padding** - A parameter added in version 8.0.41 that specifies the padding scheme:
  * `no` - No padding (requires exact-size messages, not recommended for production)
  * `pkcs1` - PKCS#1 v1.5 padding scheme (standard protection)
  * `oaep` - Optimal Asymmetric Encryption Padding (enhanced security)
  
  If not specified, the system uses the value from the encryption_udf.legacy_padding_scheme variable.

<details>
   <summary>Example usage</summary>
   
   ```sql
   -- Encrypt sensitive data using a public key
   SET @ciphertext = asymmetric_encrypt('RSA', 'Secret message', @public_key, 'oaep');
   
   -- Store or transmit the encrypted data
   INSERT INTO secure_messages VALUES (@ciphertext);
   ```
</details>

⚠️ **Size Limits**: Remember that your message size is limited by your key size and padding method. For a 2048-bit key with OAEP padding, your message must be smaller than (2048/8)-42 = 214 bytes.

---


## Asymmetric_sign(*algorithm, digest_str, priv_key_str, digest_type, [padding]*)

> ✍️ **Digital Signature Function**
>
> This function applies a cryptographic signature to a message digest using a private key. The signature provides authentication, non-repudiation, and integrity verification capabilities. Each signature is unique even when signing the same content multiple times.


### Quick reference

| Parameter | Required | Description |
|-----------|----------|-------------|
| algorithm | Yes | Signature algorithm ('RSA' or 'DSA') |
| digest_str | Yes | The message digest (hash value) |
| priv_key_str | Yes | The signer's private key in PEM format |
| digest_type | Yes | The hash algorithm identifier (e.g., 'SHA256') |
| padding | No | For RSA only: 'pkcs1' or 'pkcs1_pss' |


### Security considerations

⚠️ **Implementation Risks**:
* Using public key instead of private key for signing operations
* Signing raw message data instead of message digest
* Inconsistent algorithm selection across systems
* Inadequate private key protection and backup procedures


### Return value

The function returns a digital signature as binary data that cryptographically proves the authenticity of the message.


### Parameter details

1. **algorithm** - Specifies the signature algorithm:
   * 'RSA' - RSA signature algorithm (widely implemented)
   * 'DSA' - Digital Signature Algorithm (alternative implementation)

2. **digest_str** - The cryptographic hash of the message 
   * Generate using the create_digest function
   * Always sign the digest rather than the raw message for security and performance

3. **priv_key_str** - The signer's private key
   * Requires secure storage and access controls
   * Must be in PEM format (standard key encoding format)

4. **digest_type** - The hash algorithm identifier
   * Common implementations include 'SHA256', 'SHA512', etc.
   * Reference the digest type table for all supported algorithms

5. **padding** - Signature padding scheme (for RSA algorithm only)
   * Options: 'pkcs1' or 'pkcs1_pss'
   * Default is determined by the encryption_udf.legacy_padding_scheme setting

<details>
   <summary>Example usage</summary>
   
   ```sql
   -- Generate a message digest
   SET @digest = create_digest('SHA256', 'Important message');
   
   -- Sign the digest
   SET @signature = asymmetric_sign('RSA', @digest, @private_key, 'SHA256', 'pkcs1_pss');
   
   -- Store the signature with the message
   INSERT INTO signed_messages VALUES ('Important message', @signature);
   ```
</details>

---


## Asymmetric_verify(*algorithm, digest_str, sig_str, pub_key_str, digest_type, [padding]*)

> 🔍 **Signature verification function**
>
> This function validates the authenticity of a digital signature by verifying it against the original message digest using the signer's public key. It provides cryptographic proof of message integrity and sender identity.


### Quick reference

| Parameter | Required | Description |
|-----------|----------|-------------|
| algorithm | Yes | Signature algorithm ('RSA' or 'DSA') |
| digest_str | Yes | The message digest (hash value) |
| sig_str | Yes | The digital signature to verify |
| pub_key_str | Yes | The signer's public key in PEM format |
| digest_type | Yes | The hash algorithm identifier (e.g., 'SHA256') |
| padding | No | For RSA only: 'pkcs1' or 'pkcs1_pss' |


### Return value

The function returns a binary verification result:
* `1` - Signature verified successfully (authentic)
* `0` - Signature verification failed (inauthentic or corrupted)


### Parameter details

1. **algorithm** - Specifies the signature algorithm for verification
   * Must match the algorithm used during signature creation
   * Supported values: 'RSA' or 'DSA'

2. **digest_str** - The cryptographic hash of the message
   * Generate using the create_digest function
   * Must use identical hashing algorithm as used during signing

3. **sig_str** - The digital signature to be verified
   * Generated by the asymmetric_sign function
   * Binary data containing cryptographic validation information

4. **pub_key_str** - The signer's public key
   * Must correspond to the private key used for signature creation
   * Required in PEM format

5. **digest_type** - The hash algorithm identifier
   * Must match the algorithm used during signature creation
   * Reference the algorithm table for supported options

6. **padding** - The signature padding scheme
   * Applicable only for RSA signatures
   * Must match the padding scheme used during signature creation
   * Default is determined by [`encryption_udf.legacy_padding_scheme`](#encryption_udflegacy_padding_scheme)


### ⚠️ Common Verification Pitfalls

| Mistake | What Happens | How to Avoid |
|---------|-------------|--------------|
| Using wrong public key | Verification always fails | Double-check key ownership |
| Verifying tampered message | Verification correctly fails | Don't change the message after signing |
| Using wrong digest type | Verification fails mysteriously | Use same digest type as signing |
| Mismatched padding | Verification fails with no clear reason | Use same padding as signing |

<details>
   <summary>Example usage</summary>
   
   ```sql
   -- Retrieve a signed message and its signature
   SELECT message, signature INTO @message, @signature FROM signed_messages LIMIT 1;
   
   -- Generate the message digest
   SET @digest = create_digest('SHA256', @message);
   
   -- Verify the signature (1 = valid, 0 = invalid)
   SET @is_valid = asymmetric_verify('RSA', @digest, @signature, @public_key, 'SHA256', 'pkcs1_pss');
   
   -- Check the result
   SELECT IF(@is_valid = 1, 'Signature is valid', 'Signature is forged or corrupted') AS verification_result;
   ```
</details>

---
## Create_asymmetric_priv_key(*algorithm, key_len*)

> 🔑 **Private key generation function**
>
> This function generates a cryptographic private key using the specified algorithm and security parameters. The private key serves as the foundation for asymmet

| Mistake | Consequence | Better Approach |
|---------|-------------|-----------------|
| Too small key | Vulnerable to attacks | Use at least 2048 bits for RSA |
| Too large key | Extremely slow operations | Balance security with performance |
| Unsecured storage | Key theft | Store keys in secure, restricted locations |
| No backup | Permanent data loss | Backup keys with proper security |

### Taking too long?

Some keys (especially strong ones) take a while to create. If you're getting impatient:

```sql
KILL QUERY <id>;
-- or
KILL CONNECTION <id>;
```

This works for RSA and DSA keys. DH keys are quick, so no worries there.

<details>
   <summary>Example usage</summary>
   
   ```sql
   -- Create a 3072-bit RSA private key
   SET @private_key = create_asymmetric_priv_key('RSA', 3072);
   
   -- Create a 2048-bit DSA private key
   SET @dsa_key = create_asymmetric_priv_key('DSA', 2048);
   
   -- Create DH parameters and then a DH key
   SET @dh_params = create_dh_parameters(2048);
   SET @dh_key = create_asymmetric_priv_key('DH', 2048, @dh_params);
   
   -- Save your key for future use
   INSERT INTO secure_keys (key_id, key_content) VALUES ('my_primary_key', @private_key);
   ```
</details>

---

## Create_asymmetric_pub_key(*algorithm, priv_key_str*)

> 🔓 **Public key extraction function**
>
> This function extracts a public key from your private key. Think of it as creating a deposit-only ATM card - people can put money in, but they can't take any out.

### Quick reference

| Parameter | Required | Description |
|-----------|----------|-------------|
| algorithm | Yes | Key algorithm ('RSA', 'DSA', or 'DH') |
| priv_key_str | Yes | Your private key in PEM format |

### What you get back

A public key in PEM format - another block of garbled text you can freely share.

### What you need to extract your public key

1. **algorithm** - What kind of key are we working with?
   * Must match the private key type: 'RSA', 'DSA', or 'DH'
   * Get this wrong and you'll get errors

2. **priv_key_str** - Your secret private key
   * Must be in PEM

## Create_dh_parameters(*key_len*)

This function creates the special math values for Diffie-Hellman keys. It's like creating a recipe that two people will follow to create identical secret sauces without ever sharing their individual ingredients.

### Warning: Patience required!
This can take a LONG time - much longer than making regular keys. Cancel with:

```
KILL [QUERY|CONNECTION] <id>
```

Think of it like the difference between:
* Making regular keys = making a sandwich
* Creating DH parameters = baking bread from scratch

### What you get back
A block of special values in PEM format. You'll use these later when creating DH keys.

### What you need to create parameters

**key_len** - How mathematically strong should these be?
* Choose between 1,024 and 10,000 bits
* Default is 10,000 (strongest but slowest)
* Admins can adjust the maximum with encryption_udf.dh_bits_threshold

## Create_digest(*digest_type, str*)

Creates a digest from the given string using the given digest type. The digest string can be used with asymmetric_sign and asymmetric_verify.

### Create_digest output

The digest of the given string as a binary string

### Create_digest parameters

The parameters are the following:

* digest_type - the OpenSSL version installed on your system determines the available hash functions. The following table lists these functions:

    | OpenSSL 1.0.2 | OpenSSL 1.1.0 | OpenSSL 1.1.1 | OpenSSL 3.0.x |
    |---|---|---|---|
    | md5 | md5 | md5 | md5 |
    | sha1 | sha1 | sha1 | sha1 |
    | sha224 | sha224 | sha224 | sha224 |
    | sha384 | sha384 | sha384 | sha384 |
    | sha512 | sha512 | sha512 | sha512 |
    | md4 | md4 | md4 | md4 |
    | sha | md5-sha1 | md5-sha1 | md5-sha1 |
    | ripemd160 | ripemd160 | ripemd160 | sha512-224 |
    | whirlpool | whirlpool | sha512-224 | sha512-256 |
    |  | blake2b512 | sha512-256 | sha3-224 |
    |  | blake2s256 | whirlpool | sha3-256 |
    |  |  | sm3 | sha3-384 |
    |  |  | blake2b512 | sha3-512 |
    |  |  | blake2s256 | sm3 |
    |  |  | sha3-224 | blake2b512 |
    |  |  | sha3-384 | blake2s256 |
    |  |  | sha3-512 | blake2b512 |
    |  |  | shake128 | blake2s256 |
    |  |  | shake256 |  |

* str - String used to generate the digest string.

### Encryption threshold variables

OpenSSL defines the maximum key length limits. Server administrators can limit the maximum key length using the encryption threshold variables.

The variables are automatically registered when component_encryption_udf is installed.

| Variable Name                    |
|----------------------------------|
| encryption_udf.dh_bits_threshold |

### `encryption_udf.dh_bits_threshold`

The variable sets the maximum limit for the create_dh_parameters user-defined function and precedes the OpenSSL maximum length value.

| Option       | Description      |
|--------------|------------------|
| command-line | Yes              |
| scope        | Global           |
| data type    | unsigned integer |
| default      | 10000            |

The range for this variable is from 1024 to 10,000. The default value is 10,000.

### encryption_udf.dsa_bits_threshold

The variable sets the threshold limits for the create_asymmetric_priv_key user-defined function when it is invoked with the DSA parameter and takes precedence over the OpenSSL maximum length value.

| Option       | Description      |
|--------------|------------------|
| command-line | Yes              |
| scope        | Global           |
| data type    | unsigned integer |
| default      | 9984             |

The range for this variable is from 1,024 to 9,984. The default value is 9,984.

### Encryption_udf.legacy_padding_scheme

The variable enables or disables the legacy padding scheme for certain encryption operations.

895|

| Option       | Description      |
|--------------|------------------|
| command-line | Yes              |
| scope        | Global           |
| data type    | Boolean |
| default      | OFF            |

This system variable is a BOOLEAN type and is set to `OFF` by default. 

This variable controls how the functions `asymmetric_encrypt()`, `asymmetric_decrypt()`, `asymmetric_sign()`, and `asymmetric_verify()` behave when you don’t explicitly set the padding parameter.

### Understanding padding schemes

Think of padding like packing a box:
* `oaep` is like using a big box with lots of bubble wrap
* `no` padding is like using an exact-size box with no padding 
* `pkcs1` is like using a box with just a thin layer of protection

When `encryption_udf.legacy_padding_scheme` is OFF (default):

* For locking data: Functions use `oaep` padding (the big box with lots of bubble wrap)
* For signing data: Functions use `pkcs1_pss` padding (the fancy signature style)

When `encryption_udf.legacy_padding_scheme` is ON:

* For locking data: Functions use `pkcs1` padding (the box with thin protection)
* For signing data: Functions use `pkcs1` padding (the basic signature style)

You can also pick a padding style yourself in the `asymmetric_encrypt()` and `asymmetric_decrypt()` functions with RSA encryption. Just add `'no'`, `'pkcs1'`, or `'oaep'` as the last parameter. If you don't pick one, the system uses whatever `encryption_udf.legacy_padding_scheme` is set to.

### Size limits for each padding style

| Padding Box | How much can fit inside |
|-------------|-------------------------|
| `oaep`      | Your key size minus 42 bytes (less room, but most secure) |
| `no`        | Must be EXACTLY your key size (like a perfect-fit box) |
| `pkcs1`     | Your key size minus 11 bytes (more room than oaep) |

#### Example: How much fits in a pkcs1 box

Let's say you have a 1024-bit RSA key:

1. First, convert bits to bytes:
   * 1024 bits ÷ 8 = 128 bytes

2. Then, subtract the padding space:
   * 128 bytes - 11 bytes = 117 bytes

3. Result: Your message must be 117 bytes or less

If your message is bigger than what fits, you'll need:
* A bigger key size, or
* A different padding style

### Padding for signatures

When you sign data with `asymmetric_sign()` or verify with `asymmetric_verify()`, you can choose a padding style too:
* `pkcs1` - the basic style
* `pkcs1_pss` - the extra-secure style

If you don't pick one, the system checks the `encryption_udf.legacy_padding_scheme` setting. You can only use padding with RSA algorithms.

#### Want to learn more?

Check out this article: [`Digital Signatures: Another layer of Data Protection in Percona Server for MySQL` :octicons-link-external-16:](https://www.percona.com/blog/digital-signatures-another-layer-of-data-protection-in-percona-server-for-mysql/)

### Encryption_udf.rsa_bits_threshold

This setting controls how strong RSA keys can be when you create them with the create_asymmetric_priv_key function. Think of it as setting a limit on how big of a padlock you can make.

| Option       | What it means     |
|--------------|-------------------|
| command-line | You can set it when starting MySQL |
| scope        | Affects the whole server |
| data type    | A number without decimals |
| default      | 16384 (strongest possible) |

You can choose any number between 1,024 (good) and 16,384 (extremely strong). The default is set to the maximum of 16,384.

## Examples you can try

Here are some simple examples to help you get started:

### Example 1: Setting limits and working with keys

This example shows how to:
* Set how strong keys can be
* Create your private key (your secret key)
* Create your public key (the key you can share)
* Lock (encrypt) some text
* Unlock (decrypt) it again

```{.bash data-prompt="mysql>"}
-- Set Global variable
mysql> SET GLOBAL encryption_udf.dh_bits_threshold = 4096;

-- Set Global variable
mysql> SET GLOBAL encryption_udf.rsa_bits_threshold = 4096;
```

```{.bash data-prompt="mysql>"}
-- Create a private key
mysql> SET @private_key = create_asymmetric_priv_key('RSA', 3072);

-- Create a public key
mysql> SET @public_key = create_asymmetric_pub_key('RSA', @private_key);

-- Encrypt data using the private key (you can also use the public key)
mysql> SET @ciphertext = asymmetric_encrypt('RSA', 'This text is secret', @private_key);

-- Decrypt data using the public key (you can also use the private key)
-- The decrypted value @plaintext should be identical to the original 'This text is secret'
mysql> SET @plaintext = asymmetric_decrypt('RSA', @ciphertext, @public_key);
```

### Example 2: Creating digital signatures

This example shows how to:
* Create a fingerprint (digest) of your message
* Sign that fingerprint with your private key
* Check if the signature is real

```{.bash data-prompt="mysql>"}
-- Generate a digest string
mysql> SET @digest = create_digest('SHA256', 'This is the text for digest');

-- Generate a digest signature
mysql> SET @signature = asymmetric_sign('RSA', @digest, @private_key, 'SHA256');

-- Verify the signature against the digest
-- The @verify_signature must be equal to 1
mysql> SET @verify_signature = asymmetric_verify('RSA', @digest, @signature, @public_key, 'SHA256');
```

### Example 3: Creating a shared secret

This example shows how two people can create the same secret key without ever sharing their private keys:

* Create the recipe (DH parameter) for making the shared secret
* Make two sets of keys (one for each person)
* Person 1 creates the shared secret using their private key and Person 2's public key
* Person 2 creates the SAME shared secret using their private key and Person 1's public key

This is like two people who each have half of a recipe - when combined, they both end up with the same final dish!

```{.bash data-prompt="mysql>"}
 -- Generate a DH parameter
 mysql> SET @dh_parameter = create_dh_parameters(3072);

 -- Generate DH key pairs
 mysql> SET @private_1 = create_asymmetric_priv_key('DH', @dh_parameter);
 mysql> SET @public_1 = create_asymmetric_pub_key('DH', @private_1);
 mysql> SET @private_2 = create_asymmetric_priv_key('DH', @dh_parameter);
 mysql> SET @public_2 = create_asymmetric_pub_key('DH', @private_2);

-- Generate a symmetric key using the public_1 and private_2
-- The @symmetric_1 must be identical to @symmetric_2
mysql> SET symmetric_1 = asymmetric_derive(@public_1, @private_2);

-- Generate a symmetric key using the public_2 and private_1
-- The @symmetric_2 must be identical to @symmetric_1
mysql> SET symmetric_2 = asymmetric_derive(@public_2, @private_1);
```

### Example 4: Different ways to create keys

Here are three different ways to create and save your keys:
* Using a simple variable with `SET`
* Using a query with `SELECT INTO`
* Saving directly to a table with `INSERT`

```{.bash data-prompt="mysql>"}
mysql> SET @private_key1 = create_asymmetric_priv_key('RSA', 3072);
mysql> SELECT create_asymmetric_priv_key('RSA', 3072) INTO @private_key2;
mysql> INSERT INTO key_table VALUES(create_asymmetric_priv_key('RSA', 3072));
```

## Removing the encryption toolbox

When you're done using these tools, you can remove them from your system. Think of it like uninstalling an app when you no longer need it.

Use this simple command:

```{.bash data-prompt="mysql>"}
mysql> UNINSTALL COMPONENT 'file://component_encryption_udf';
```

This removes all the encryption functions from your MySQL server.
