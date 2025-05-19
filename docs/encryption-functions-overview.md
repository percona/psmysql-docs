## Encryption functions overview

This document provides comprehensive information about encryption functions that transform plaintext data into encrypted ciphertext. These functions provide robust security measures that require proper documentation to implement and maintain effectively. This guide offers the necessary information for successful implementation.



## Overview of capabilities

This documentation will guide you through:

* Implementing data encryption protocols

* Executing data decryption procedures

* Implementing digital signature authentication

* Avoiding common implementation pitfalls




First, let's review some key terms you'll encounter throughout this guide.


## Glossary of terms

Here's a quick reference guide to the cryptographic terms used in this document:

* **Encryption**: The process of converting readable data into a coded format that can only be decoded with the correct key.

* **Decryption**: The reverse process of encryption, converting coded data back to its original readable form.

* **Symmetric Encryption**: A type of encryption where the same key is used for both encryption and decryption, like a single key that locks and unlocks the same door.

* **Asymmetric Encryption**: A type of encryption that uses a pair of keys - a public key for encryption and a private key for decryption, or vice versa.

* **RSA** (Rivest-Shamir-Adleman): One of the most widely used asymmetric encryption algorithms, named after its creators.

* **DSA** (Digital Signature Algorithm): An algorithm specifically designed for creating digital signatures.

* **DH** (Diffie-Hellman): A method that allows two parties to establish a shared secret key over an insecure channel without sharing any secret information beforehand.

* **Digest/Hash**: A fixed-size string of bytes generated from input data of any size, functioning like a digital fingerprint of the data.

* **Digital Signature**: An electronic equivalent of a handwritten signature that uses asymmetric cryptography to verify authenticity.

* **Padding**: Additional data added to a message before encryption to enhance security and prevent pattern analysis.

* **PEM Format**: Privacy Enhanced Mail format, a common format for storing and sending cryptographic keys, certificates, and other data.

Now, let's examine common implementation challenges in encryption systems.

## Implementation challenges

> ⚠️ **Common encryption mistakes**
>
> Key management is a critical aspect of encryption systems that requires rigorous planning and careful implementation.
>

Here are the most common implementation issues:

* Key loss: When decryption keys are lost, data becomes permanently inaccessible, even to authorized personnel.

* Algorithm-key mismatch: Using incompatible keys and algorithms results in decryption failures.

* Exceeding size limitations: Attempting to encrypt data larger than algorithm constraints can cause failures in both encryption and decryption processes.

* Insufficient documentation: Failing to properly document the encryption process and key management procedures can lead to system failures.

## Version updates

Percona Server for MySQL 8.0.41 introduces several important new features that enhance security capabilities while requiring careful implementation.

### Padding options for RSA encryption

| Padding type | Security level | Application            | Characteristics                                |
|--------------|----------------|------------------------|------------------------------------------------|
| `pkcs1`      | Basic          | Legacy compatibility   | Standard protection with known limitations    |
| `oaep`       | High           | Modern applications    | Enhanced protection with additional security layers |
| `no`         | None           | Specialized cases only | No protection, vulnerable to multiple attack vectors |

#### Detailed padding explanations

<details>
   <summary> `pkcs1` padding: The nostalgic option</summary>
   
   Think of `pkcs1` padding as the security equivalent of a 90s-era car alarm. It adds random stuffing to your message to stop pattern analysis, making your message look different each time. It's decent protection against casual thieves but not against determined professionals with modern tools. It's like putting your valuables in a safe that shouts "HEY! I'M A SAFE!" when touched.
</details>

<details>
   <summary> `oaep` padding: The recommended secure option</summary>  
   
   `oaep` padding (Optimal Asymmetric Encryption Padding) implements a mathematically robust random mask that significantly increases resistance to cryptanalysis (the science of breaking encryption). This method applies multiple layers of protection to the encrypted data, making it the recommended option for systems requiring high security standards. The additional computational overhead is justified by the enhanced security protections it provides.
</details>   
   
<details>
   <summary> `no` padding: Non-secure implementation option</summary>
   
   The unpadded encryption implementation provides no additional cryptographic protection for the message content. This approach eliminates randomization elements, exposing the encrypted data to various cryptanalytic attacks including pattern analysis. This option should only be implemented in specialized circumstances where compatibility with specific systems is required or where separate security controls are implemented at another layer. Not recommended for standard security implementations.
</details>


### Signature padding options

| Padding Type | Security Level | Characteristics | Best For |
|-------------|---------------|-----------------|----------|
| `pkcs1` | Standard | Consistent signatures | Compatibility with older systems |
| `pkcs1_pss` | High | Unique signature every time | Modern security needs |

<details>
   <summary> `pkcs1` padding: The basic signature</summary>
   
   `pkcs1` padding for signatures is like signing your name the same way every time. It takes your message, creates a fingerprint, adds some standard framing, and locks it with your private key. It works fine until someone figures out how to copy your signature style, at which point your security is compromised. It's simple and compatible with older systems, but not the strongest option available.
</details>

<details>
   <summary> `pkcs1_pss` padding: The signature with flair</summary>
   
   `pkcs1_pss` padding is like adding a unique flourish to your signature every single time. Even when signing the exact same document twice, the signatures will look completely different - yet both will verify correctly. This makes signature forgery dramatically harder, as there's no consistent pattern to copy. If you're serious about security (and if you're reading this, you should be), this is your go-to option.
</details>


### Other new features

* [`encryption_udf.legacy_padding_scheme`](#encryption_udflegacy_padding_scheme) system variable - provides compatibility with legacy systems and previous implementations

* Character set awareness - ensures proper handling of different character encodings during encryption operations

Percona Server for MySQL 8.0.28-20 introduces tools for selective data encryption, allowing precise control over which data elements receive encryption protections.

## Character sets and component encryption UDFs

> 🏭 **Automated feature**
>
> These functions automatically manage character sets, eliminating the need for manual character encoding management during encryption operations.

The implementation handles complex character set conversions internally, allowing developers to focus on encryption logic rather than encoding issues.

### What happens to your input

| Input Type | What Happens | Why It Matters |
|------------|--------------|----------------|
| Algorithms, digest names, keys | Automatically converted to ASCII | Prevents character encoding mismatches between encryption and decryption operations |
| Messages and signatures | Transformed into raw binary | Computers process binary, not human-readable formats |


### What you get back

| Output Type | Format | What to Expect |
|------------|--------|----------------|
| Key files | Human-readable ASCII text | Viewable without terminal issues |
| Encrypted messages & signatures | Binary data | Looks like gibberish (this is correct!) |

## External key management

> 🔒 **External Key Management**
>
> For enhanced security, cryptographic keys can be generated outside the database server using dedicated cryptographic tools and hardware.

Keys can be generated externally with OpenSSL and imported into the system. This approach separates key generation from the database environment, reducing the attack surface and allowing for specialized key generation hardware if required.


### External key generation

| Tool | Command Example | What It Creates |
|------|----------------|-----------------|
| OpenSSL | `openssl genrsa -out private.pem 2048` | RSA private key |
| OpenSSL | `openssl rsa -in private.pem -pubout -out public.pem` | RSA public key from private key |
| OpenSSL | `openssl dsaparam -genkey 2048 -out dsaprivate.pem` | DSA private key |

Your OpenSSL-generated keys work seamlessly with these functions - just read the PEM file and pass its content to the encryption functions.


### How you might break this

⚠️ **Common Mistakes With External Keys:**

* Importing a key in the wrong format

* Using a key type incompatible with your chosen algorithm

* Forgetting to remove newlines from PEM files when storing in variables

* Storing keys directly in your database without proper protection

If you encounter any of these issues, you may receive a non-descriptive error message. Ensure that your keys are correctly formatted and stored securely.


