# Encryption functions

Percona Server for MySQL adds encryption functions and variables to manage the encryption range. The functions may take an algorithm argument. Encryption converts plaintext into ciphertext using a key and an encryption algorithm.

You can also use the user-defined functions with the PEM format keys generated externally by the OpenSSL utility.

A digest uses plaintext and generates a hash value. This hash value can verify if the plaintext is unmodified. You can also sign or verify on digests to ensure that the original plaintext was not modified. You cannot decrypt the original text from the hash value.

When choosing key lengths, consider the following:

* Encryption strength increases with the key size and, also, the key generation time.

* If performance is important and the functions are frequently used, use symmetric encryption. Symmetric encryption functions are faster than asymmetric encryption functions. Moreover, asymmetric encryption has restrictions on the maximum length of a message being encrypted. For example, for RSA the algorithm maximum message size is the key length in bytes (key length in bits / 8) minus 11.

<!-- Rewrite the following instruction to be valid for 9.7-->

## Version updates

Percona Server for MySQL 8.4.4 adds the following:

* Support for `pkcs1`, `oaep`, or `no` padding for RSA encrypt and decrypt operations

    <details>
       <summary> `pkcs1` padding explanation</summary>
        [`RSAES-PKCS1-v1_5` :octicons-link-external-16:](https://en.wikipedia.org/wiki/PKCS_1) RSA encryption padding scheme prevents patterns that attackers could exploit by including a random sequence of bytes, which ensures that the ciphertext is different no matter how many times it is encrypted.
    </details>
    <details>
       <summary> `oaep` padding explanation</summary>  
        The [`RSAES-OAEP` :octicons-link-external-16:](https://en.wikipedia.org/wiki/PKCS_1)  - [`Optimal Asymmetric Encryption Padding` :octicons-link-external-16:](https://en.wikipedia.org/wiki/Optimal_asymmetric_encryption_padding) RSA encryption padding scheme adds a randomized mask generation function. This function makes it more difficult for attackers to exploit the encryption algorithm's weaknesses or recover the original message.
    </details>
    <details>
       <summary> `no` padding explanation</summary>
       Using `no` padding means the plaintext message is encrypted without adding an extra layer before performing the RSA encryption operation.
    </details>

* Support for `pkcs1` or `pkcs1_pss`  padding for RSA sign and verify operations

    <details>
       <summary> `pkcs1` padding explanation</summary>
        The [`RSASSA-PKCS1-v1_5` :octicons-link-external-16:](https://en.wikipedia.org/wiki/PKCS_1) is a deterministic RSA signature padding scheme that hashes a message, pads the hash with a specific structure, and encrypts it with the signer's private key for signature generation. 
    </details>
    <details>
       <summary> `pkcs1_pss` padding explanation</summary>
        The [`RSASSA-PSS` :octicons-link-external-16:](https://en.wikipedia.org/wiki/PKCS_1) - [`Probabilistic Signature Scheme' :octicons-link-external-16:](https://en.wikipedia.org/wiki/Probabilistic_signature_scheme) is an RSA signature padding scheme used to add randomness to a message before signing it with a private key. This randomness helps to increase the security of the signature and makes it more resistant to various attacks. 
    </details>

* [`encryption_udf.legacy_paddding`](#legacy_padding) system variable

* Character set awareness

## Charset Awareness

All component_encryption_udf functions now handle character sets intelligently:

• Algorithms, digest names, padding schemes, keys, and parameters in PEM format: Automatically converted to the ASCII charset at the MySQL level before passing to the functions.

• Messages, data blocks, and signatures used for digest calculation, encryption, decryption, signing, or verification: Automatically converted to the binary charset at the MySQL level before passing to the functions.

• Function return values in PEM format: Assigned the ASCII charset.

• Function return values for operations like digest calculation, encryption, decryption, and signing: Assigned the binary charset.

## Use user-defined functions

You can also use the user-defined functions with the PEM format keys generated externally by the OpenSSL utility.

A digest uses plaintext and generates a hash value. This hash value can verify if the plaintext is unmodified. You can also sign or verify on digests to ensure that the original plaintext was not modified. You cannot decrypt the original text from the hash value.

When choosing key lengths, consider the following:

* Encryption strength increases with the key size and generation time.

* If performance is essential and the functions are frequently used, use symmetric encryption. Symmetric encryption functions are faster than asymmetric encryption functions. Moreover, asymmetric encryption restricts the maximum length of a message being encrypted. For example, the algorithm's maximum message size for RSA is the key length in bytes (key length in bits / 8) minus 11.

## Install component_encryption_udf

Use the [Install Component Statement](https://dev.mysql.com/doc/refman/{{vers}}/en/install-component.html) to add the component_encryption_udf component. The functions and variables are available. The user-defined functions and the Encryption threshold variables are auto-registered. There is no requirement to invoke `CREATE FUNCTION ... SONAME ...`.

The `INSERT` privilege on the `mysql.component` system table is required to run the `INSTALL COMPONENT` statement. The operation adds a row to this table to register the component.

The following is an example of the installation command:

```sql
INSTALL COMPONENT 'file://component_encryption_udf';
```

!!! note

    When you build Percona Server for MySQL from source code, the Encryption UDF component is included by default. To exclude it, use the `-DWITH_ENCRYPTION_UDF=OFF` option with cmake.



## Functions

The following table and sections describe the functions. For examples, see function examples.

| Function Name                                                                                                                    |
|----------------------------------------------------------------------------------------------------------------------------------|
| [asymmetric_decrypt()](#asymmetric_decrypt()) |
| [asymmetric_derive()](#asymmetric_derive()) |
| [asymmetric_encrypt()](#asymmetric_encrypt()) |
| [asymmetric_sign()](#asymmetric_sign()) |
| [asymmetric_verify()](#asymmetric_verify()) |
| [create_asymmetric_priv_key()](#create_asymmetric_priv_key())   |
| [create_asymmetric_pub_key()](#create_asymmetric_pub_key())  |
| [create_dh_parameters()](#create_dh_parameters())  |
| [create_digest()](#create_digest())  |

The following table describes the encryption threshold variables which can be used to set the maximum value for a key length based on the type of encryption used.

| Variable Name                     |
|-----------------------------------|
| [encryption_udf.dh_bits_threshold](#dh_bits_threshold)  |
| [encryption_udf.dsa_bits_threshold](#dsa_bits_threshold) |
| [encryption_udf.legacy_padding](#legacy_padding)|
| [encryption_udf.rsa_bits_threshold](#rsa_bits_threshold) |


## User-defined functions described

## <a name="asymmetric_decrypt()" style="font-family: 'Open Sans', Arial, sans-serif;">asymmetric_decrypt(*algorithm, crypt_str, key_str*)</a>

Decrypts an encrypted string using the algorithm and a key string.

### Returns

A plaintext as a string.

### Parameters

The following are the function’s parameters:

* algorithm - the encryption algorithm supports RSA in decrypting the string.

  * `crypt_str` - an encrypted string produced by certain encryption functions like AES_ENCRYPT(). This string is typically stored as a binary or blog data type.

* key_str - a string in the PEM format. The key string must have the following attributes:

  * Valid

  * Public or private key string corresponding with the private or public key string used with the [`asymmetric_encrypt`](#asymmetric_encrypt()) function.
  
  * padding - An optional parameter introduced in Percona Server for MySQL 8.4.4. It is used with the RSA algorithm and supports RSA encryption padding schemes like pkcs1, or oaep. If you skip this parameter, the system determines its value based on the [`encryption_udf.legacy_padding`](#legacy_padding) variable.

## <a name="asymmetric_derive()" style="font-family: 'Open Sans', Arial, sans-serif;">asymmetric_derive(*pub_key_str, priv_key_str*)</a>

Derives a symmetric key using a public key generated on one side and a private key generated on another.

### asymmetric_derive output

A key as a binary string.

### asymmetric_derive parameters

The `pub_key_str` must be a public key in the PEM format and generated using the Diffie-Hellman (DH) algorithm.

The `priv_key_str` must be a private key in the PEM format and generated using the Diffie-Hellman (DH) algorithm.

## <a name="asymmetric_encrypt()" style="font-family: 'Open Sans', Arial, sans-serif;">asymmetric_encrypt(*algorithm, str, key_str*)</a>

Encrypts a string using the algorithm and a key string.

### asymmetric_encrypt output

A ciphertext as a binary string.

### asymmetric_encrypt parameters

The parameters are the following:

* algorithm - the encryption algorithm supports RSA to encrypt the string.

* str - measured in bytes. The length of the string must not be greater than the key_str modulus length in bytes - 11 (additional bytes used for PKCS1 padding)

* key_str - a key (either private or public) in the PEM format

* padding - An optional parameter introduced in Percona Server for MySQL 8.4.4. It is used with the RSA algorithm and supports RSA encryption padding schemes like pkcs1, or oaep. If you skip this parameter, the system determines its value based on the  [`encryption_udf.legacy_padding`](#legacy_padding) variable.

##  <a name="asymmetric_sign()" style="font-family: 'Open Sans', Arial, sans-serif;">asymmetric_sign(*algorithm, digest_str, priv_key_str, digest_type*)</a>

Signs a digest string using a private key string.

### asymmetric_sign output

A signature is a binary string.

### asymmetric_sign parameters

The parameters are the following:

* algorithm - the encryption algorithm supports either RSA or DSA in encrypting the string.

* digest_str - the digest binary string that is signed. Invoking create_digest generates the digest.

* priv_key_str - the private key used to sign the digest string. The key must be in the PEM format.

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
    |  |  | blake2s256 |  |
    |  |  | sha3-224 |  |
    |  |  | sha3-384 |  |
    |  |  | sha3-512 |  |
    |  |  | shake128 |  |
    |  |  | shake256 |  |

* padding - An optional parameter introduced in Percona Server for MySQL 8.4.4. It is used with the RSA algorithm and supports RSA signature padding schemes like `pkcs1`, or `pkcs1_pss`. If you skip this parameter, the system determines its value based on the [`encryption_udf.legacy_padding`](#legacy_padding) variable.

## <a name="asymmetric_verify()" style="font-family: 'Open Sans', Arial, sans-serif;">asymmetric_verify(*algorithm, digest_str, sig_str, pub_key_str, digest_type*)</a>

Verifies whether the signature string matches the digest string.


### asymmetric_verify output

A `1` (success) or a `0` (failure).

### asymmetric_verify parameters

The parameters are the following:

* algorithm - supports either ‘RSA’ or ‘DSA’.

* digest_str - invoking create_digest generates this digest binary string.

* sig_str - the signature binary string. Invoking asymmetric_sign generates this string.

* pub_key_str - the signer’s public key string. This string must correspond to the private key passed to asymmetric_sign to generate the signature string. The string must be in the PEM format.

* digest_type - the supported values are listed in the digest type table of create_digest

* padding - An optional parameter introduced in Percona Server for MySQL 8.4.4. It is used with the RSA algorithm and supports RSA signature padding schemes like `pkcs1`, or `pkcs1_pss`. If you skip this parameter, the system determines its value based on the [`encryption_udf.legacy_padding`](#legacy_padding) variable.

## <a name="create_asymmetric_priv_key()" style="font-family: 'Open Sans', Arial, sans-serif;">create_asymmetric_priv_key(*algorithm,(key_len | dh_parameters)*)</a>

Generates a private key using the given algorithm and key length for RSA or DSA
or Diffie-Hellman parameters for DH. For RSA or DSA, if needed, execute `KILL
[QUERY|CONNECTION] <id>` to terminate a long-lasting key generation. The
DH key generation from existing parameters is a quick operation. Therefore, it
does not make sense to terminate that operation with `KILL`.

### create_asymmetric_priv_key output

The key as a string in the PEM format.

### create_asymmetric_priv_key parameters

The parameters are the following:

* algorithm - the supported values are ‘RSA’, ‘DSA’, or ‘DH’.

* key_len - the supported key length values are the following:

    * RSA - the minimum length is 1,024. The maximum length is 16,384.

    * DSA - the minimum length is 1,024. The maximum length is 9,984.

    !!! note 
 
        The key length limits are defined by OpenSSL. To change the maximum key length, use either encryption_udf.rsa_bits_threshold or encryption_udf.dsa_bits_threshold.

* dh_parameters - Diffie-Hellman (DH) parameters. Invoking create_dh_parameter creates the DH parameters.

## <a name="create_asymmetric_pub_key()" style="font-family: 'Open Sans', Arial, sans-serif;">create_asymmetric_pub_key(*algorithm, priv_key_str*)</a>

Derives a public key from the given private key using the given algorithm.

### create_asymmetric_pub_key output

The key as a string in the PEM format.

### create_asymmetric_pub_key parameters

The parameters are the following:

* algorithm - the supported values are ‘RSA’, ‘DSA’, or ‘DH’.

* priv_key_str - must be a valid key string in the PEM format.

## <a name="create_dh_parameters()" style="font-family: 'Open Sans', Arial, sans-serif;">create_dh_parameters(*key_len*)</a>

Creates parameters for generating a Diffie-Hellman (DH) private/public key pair.
If needed, execute `KILL [QUERY|CONNECTION] <id>` to terminate the generation of long-lasting parameters.

Generating the DH parameters can take more time than generating the RSA keys or
the DSA keys.
OpenSSL defines the parameter length limits. To change the maximum parameter length, use [`encryption_udf.dh_bits_threshold`](#dh_bits_threshold).

### create_dh_parameters output

A string in the PEM format and can be passed to [`create_asymmetric_priv_key`](#create_asymmetric_priv_key()).

### create_dh_parameters parameters

The parameters are the following:

* key_len - the range for the key length is from 1024 to 10,000. The default value is 10,000.

## <a name="create_digest()" style="font-family: 'Open Sans', Arial, sans-serif;">create_digest(*digest_type, str*)</a>

Creates a digest from the given string using the given digest type. The digest string can be used with [asymmetric_sign()](#asymmetric_sign()) and [asymmetric_verify()](#asymmetric_verify()).

### create_digest output

The digest of the given string as a binary string

### create_digest parameters

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

The maximum key length limits are defined by OpenSSL. Server administrators can limit the maximum key length using the encryption threshold variables.

The variables are automatically registered when component_encryption_udf is installed.

| Variable Name                    |
|----------------------------------|
| encryption_udf.dh_bits_threshold |

### <a name="dh_bits_threshold" style="font-family: 'Open Sans', Arial, sans-serif;">encryption_udf.dh_bits_threshold</a>

The variable sets the maximum limit for the [create_dh_parameters()](#create_dh_parameters()) user-defined function and takes precedence over the OpenSSL maximum length value.

| Option       | Description      |
|--------------|------------------|
| command-line | Yes              |
| scope        | Global           |
| data type    | unsigned integer |
| default      | 10000            |

The range for this variable is from 1024 to 10,000. The default value is 10,000.

### <a name="dsa_bits_threshold" style="font-family: 'Open Sans', Arial, sans-serif;">encryption_udf.dsa_bits_threshold</a>

The variable sets the threshold limits for [create_asymmetric_priv_key()](#create_asymmetric_priv_key()) user-defined function when the function is invoked with the DSA parameter and takes precedence over the OpenSSL maximum length value.

| Option       | Description      |
|--------------|------------------|
| command-line | Yes              |
| scope        | Global           |
| data type    | unsigned integer |
| default      | 9984             |

The range for this variable is from 1,024 to 9,984. The default value is 9,984.

### <a name="legacy_padding" style="font-family: 'Open Sans', Arial, sans-serif;">encryption_udf.legacy_padding</a>

The variable enables or disables the legacy padding scheme for certain encryption operations.

| Option       | Description      |
|--------------|------------------|
| command-line | Yes              |
| scope        | Global           |
| data type    | Boolean |
| default      | OFF            |

This system variable is a BOOLEAN type and set to `OFF` by default. 

This variable controls how the functions [asymmetric_encrypt()](#asymmetric_encrypt()), [asymmetric_decrypt()](#asymmetric_decrypt()), [asymmetric_sign()](#asymmetric_sign()), and [asymmetric_verify()](#asymmetric_verify()) behave when you don’t explicitly set the padding parameter.

* When encryption_udf.legacy_padding is OFF:

  * [asymmetric_encrypt()](#asymmetric_encrypt()) and [asymmetric_decrypt()](#asymmetric_decrypt()) use OAEP encryption padding.
  
  * [asymmetric_sign()](#asymmetric_sign()) and [asymmetric_verify()](#asymmetric_verify()) use PKCS1_PSS signature padding.
* When encryption_udf.legacy_padding is ON:

  * [asymmetric_encrypt()](#asymmetric_encrypt()) and [asymmetric_decrypt()](#asymmetric_decrypt()) use PKCS1 encryption padding.
  
  * [asymmetric_sign()](#asymmetric_sign()) and [asymmetric_verify()](#asymmetric_verify()) use PKCS1 signature padding.

The [asymmetric_encrypt()](#asymmetric_encrypt()) and [asymmetric_decrypt()](#asymmetric_decrypt()) functions, when the encryption is `RSA`, can accept an optional parameter, `padding`. You can set this parameter to `no`, `pkcs1`, or `oaep`. If you don’t specify this parameter, it defaults based on the [encryption_udf.legacy_padding](#legacy_padding) value. 

The padding schemes have the following limitations:

| Padding Scheme    | Details                                                                                                                                                        |
|-------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `oaep`           | The message you encrypt can be as long as your RSA key size in bytes - 42 bytes.|
| `no`             | The message length must exactly match your RSA key size in bytes. For example, if your key is 1024 bits (128 bytes), the message must also be 128 bytes. If it doesn’t match, it will cause an error. |
| `pkcs1` | Your message can be equal to or smaller than the RSA key size - 11 bytes. For instance, with a 1024-bit RSA key, your message can’t be longer than 117 bytes.|

Similarly, [`asymmetric_sign()`](#asymmetric_sign()) and [`asymmetric_verify()`](#asymmetric_verify()) also have an optional `padding` parameter, either `pkcs1` or `pkcs1_pss`. If not explicitly set, it follows the default based on [`encryption_udf.legacy_padding`](#legacy_padding). You can only use the padding parameter with RSA algorithms.

#### Additional resources

  For more information, read [`Digital Signatures: Another layer of Data Protection in Percona Server for MySQL`](https://www.percona.com/blog/digital-signatures-another-layer-of-data-protection-in-percona-server-for-mysql/)


### <a name="rsa_bits_threshold" style="font-family: 'Open Sans', Arial, sans-serif;">encryption_udf.rsa_bits_threshold</a>
  
The variable sets the threshold limits for the [`create_asymmetric_priv_key`](#create_asymmetric_priv_key()) user-defined function when the function is invoked with the RSA parameter and takes precedence over the OpenSSL maximum length value.

| Option       | Description      |
|--------------|------------------|
| command-line | Yes              |
| scope        | Global           |
| data type    | unsigned integer |
| default      | 16384            |

The range for this variable is from 1,024 to 16,384. The default value is 16,384.

### Examples

Code examples for the following operations:

* Set the threshold variables

* Create a private key

* Create a public key

* Encrypt data

* Decrypt data

```sql
-- Set Global variable
SET GLOBAL encryption_udf.dh_bits_threshold = 4096;

-- Set Global variable
SET GLOBAL encryption_udf.rsa_bits_threshold = 4096;
```

```sql
-- Create private key
SET @private_key = create_asymmetric_priv_key('RSA', 3072);

-- Create public key
SET @public_key = create_asymmetric_pub_key('RSA', @private_key);

-- Encrypt data using the private key (you can also use the public key)
SET @ciphertext = asymmetric_encrypt('RSA', 'This text is secret', @private_key);

-- Decrypt data using the public key (you can also use the private key)
-- The decrypted value @plaintext should be identical to the original 'This text is secret'
SET @plaintext = asymmetric_decrypt('RSA', @ciphertext, @public_key);
```

Code examples for the following operations:

* Generate a digest string

* Generate a digest signature

* Verify the signature against the digest

```sql
-- Generate a digest string
SET @digest = create_digest('SHA256', 'This is the text for digest');

-- Generate a digest signature
SET @signature = asymmetric_sign('RSA', @digest, @private_key, 'SHA256');

-- Verify the signature against the digest
-- The @verify_signature must be equal to 1
SET @verify_signature = asymmetric_verify('RSA', @digest, @signature, @public_key, 'SHA256');
```

Code examples for the following operations:

* Generate a DH parameter

* Generates two DH key pairs

* Generate a symmetric key using the public_1 and the private_2

* Generate a symmetric key using the public_2 and the private_1

```sql
 -- Generate a DH parameter
SET @dh_parameter = create_dh_parameters(3072);

 -- Generate DH key pairs
SET @private_1 = create_asymmetric_priv_key('DH', @dh_parameter);
SET @public_1 = create_asymmetric_pub_key('DH', @private_1);
SET @private_2 = create_asymmetric_priv_key('DH', @dh_parameter);
SET @public_2 = create_asymmetric_pub_key('DH', @private_2);

-- Generate a symmetric key using the public_1 and private_2
-- The @symmetric_1 must be identical to @symmetric_2
SET symmetric_1 = asymmetric_derive(@public_1, @private_2);

-- Generate a symmetric key using the public_2 and private_1
-- The @symmetric_2 must be identical to @symmetric_1
SET symmetric_2 = asymmetric_derive(@public_2, @private_1);
```

Code examples for the following operations:

* Create a private key using a `SET` statement

* Create a private key using a  `SELECT` statement

* Create a private key using an `INSERT` statement

```sql
SET @private_key1 = create_asymmetric_priv_key('RSA', 3072);
SELECT create_asymmetric_priv_key('RSA', 3072) INTO @private_key2;
INSERT INTO key_table VALUES(create_asymmetric_priv_key('RSA', 3072));
```

## Uninstall component_encryption_udf

You can deactivate and uninstall the component using the [Uninstall Component statement](https://dev.mysql.com/doc/refman/{{vers}}/en/uninstall-component.html).

```sql
UNINSTALL COMPONENT 'file://component_encryption_udf';
```
