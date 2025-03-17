# Cryptographic digest functions vs. encryption

These two fundamental cryptographic technologies serve different security purposes and should not be confused in implementation:

* Cryptographic Digest Functions (hashes):

    * Generate a fixed-length unique data representation that serves as a cryptographic fingerprint

    * Provide data integrity verification by detecting modifications at the bit level

    * Can be digitally signed to verify data origin and authenticate the source

    * Implement mathematically irreversible one-way functions by design

    * Common implementation error: Attempting to retrieve original data from digest values, which is mathematically impossible
    
* Encryption:

    * Implements reversible transformation of data using cryptographic algorithms

    * Renders data unreadable without the appropriate decryption key

    * Ensures complete data recovery with the correct cryptographic key

    * Common implementation error: Inadequate key management leading to permanent data loss


## When to use which

Use digests when:

* You need to verify data hasn't changed

* You want to store passwords (never store actual passwords, ever!)

* You need to create a digital signature

Use encryption when:

* You need to keep data secret but retrieve it later

* You're storing sensitive information that must remain recoverable

* You need to securely transmit data over insecure channels

