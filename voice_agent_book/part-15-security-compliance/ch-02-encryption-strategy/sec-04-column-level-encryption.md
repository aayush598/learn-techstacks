# Section 04: Column-Level Encryption (PII)

Column-level encryption selectively encrypts sensitive data fields within the database, allowing the rest of the data to remain queryable. This is used for PII fields like email addresses, phone numbers, names, and custom fields that tenants mark as sensitive. The encrypted columns use deterministic encryption for exact-match queries and randomized encryption for maximum security.

Deterministic encryption (pgcrypto with IV derived from data) enables WHERE clauses on encrypted columns (email lookups, phone number searches). Randomized encryption (unique IV per value) is used for fields that don't need to be searched. Both use AES-256 with the tenant's encryption key from KMS.

Search strategies for encrypted data: blind indexing (store a deterministic hash alongside encrypted value for indexing), searchable encryption (Ciphertext-Policy ABE for complex queries), or application-level indexing (Elasticsearch with encrypted fields). The trade-off is between searchability and security—more searchable means less secure.
