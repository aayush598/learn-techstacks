# Section 03: Key Management Service (KMS)

The Key Management Service centralizes encryption key lifecycle management: generation, storage, rotation, access control, and auditing. Keys never leave the KMS in plaintext—all encryption/decryption operations are performed inside the KMS boundary. The platform uses AWS KMS / HashiCorp Vault / Azure Key Vault depending on deployment.

Key hierarchy: master key (root key, generated in HSM, never exported), tenant keys (AES-256, encrypted by master key, stored in database), data keys (ephemeral, generated per-encryption operation, wrapped by tenant key). This hierarchy limits blast radius: compromising a tenant key only affects that tenant's data.

Key operations: CreateKey (generates new key material), Encrypt (takes plaintext + key ID, returns ciphertext), Decrypt (takes ciphertext, returns plaintext), GenerateDataKey (returns plaintext and encrypted data key for client-side encryption), RotateKey (creates new key material, re-encrypts data with old key). All operations are logged.
