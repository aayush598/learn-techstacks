# Section 06: Password Policies & Hashing

Password policies enforce minimum security standards for user-created passwords. Combined with bcrypt/argon2 hashing, they protect user accounts even if the database is compromised. The platform never stores plaintext passwords and uses constant-time comparison for verification.

Password policy: minimum length (12 characters), complexity (uppercase, lowercase, number, special character), common password blocking (check against 10,000 most common passwords via Have I Been Pwned API), password history (cannot reuse last 5 passwords), maximum age (90 days, configurable per tenant), and account lockout (5 failed attempts → 15-minute lockout).

Hashing algorithm: Argon2id (memory-hard, resistant to GPU/ASIC attacks) with parameters: memory cost 64MB, time cost 3, parallelism 4. For legacy support, bcrypt with cost factor 12. Hash format includes algorithm, parameters, salt, and hash in a single string. Password change requires re-hash with new salt.
