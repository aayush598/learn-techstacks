# Section 07: Client-Side Encryption

Client-side encryption allows tenants to encrypt data before it reaches the platform, ensuring that even the platform cannot read the raw content. This is used for highly sensitive data where the tenant requires guaranteed confidentiality. The tenant manages their own encryption keys; the platform only stores and transmits ciphertext.

Client-side encryption flow: tenant generates encryption key (in their browser or SDK) → tenant encrypts data before API call → platform receives ciphertext → stores encrypted blob → when tenant retrieves, returns ciphertext → tenant decrypts locally. The platform never has access to the plaintext or the encryption key.

Challenges: no server-side search, indexing, or analytics on encrypted data; data cannot be processed (STT, AI analysis) by the platform; key management is the tenant's responsibility (key loss = data loss). Implementation uses the Web Crypto API for browser-based encryption and the platform's SDK for server-side encryption. Metadata (timestamps, sizes) remains unencrypted for operational purposes.
