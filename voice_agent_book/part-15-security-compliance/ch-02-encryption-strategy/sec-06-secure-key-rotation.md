# Section 06: Secure Key Rotation

Key rotation limits the amount of data encrypted with a single key, reducing the impact of key compromise. The platform automates key rotation: new data is encrypted with the new key, existing data is re-encrypted in the background. Key rotation is scheduled quarterly or triggered by security events.

Rotation process: generate new key version (KMS creates new key material, version ID incremented)→ update key alias to point to new version → new encryption operations use new version → background re-encryption job reads old data, decrypts with old key, re-encrypts with new key → old key version retained for decryption of remaining data → after all data re-encrypted, old version retired.

Monitoring: track data encrypted by each key version, re-encryption progress (percentage complete), failed re-encryption attempts. Alerts fire if re-encryption falls behind schedule. Emergency rotation: if key compromise is suspected, immediate rotation is triggered and all data is re-encrypted urgently.
