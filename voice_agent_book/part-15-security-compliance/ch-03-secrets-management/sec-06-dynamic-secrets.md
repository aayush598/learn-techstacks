# Section 06: Dynamic Secrets & Ephemeral Credentials

Dynamic secrets are generated on-demand with short lifetimes, eliminating the risk of standing credentials. Each service request or database connection gets unique, temporary credentials. If credentials are compromised, they expire within minutes, drastically reducing the attack surface.

Database dynamic credentials: Vault's database secrets engine creates a database user on-the-fly with a random password, grants specific permissions (read-only or read-write per service), sets TTL (1 hour default, max 24 hours). When the lease expires, Vault removes the database user. Applications request new credentials at startup and refresh before expiry.

API credential generation: for tenant-scoped tokens, the platform generates short-lived credentials (15 minutes for user sessions, 1 hour for service tokens). The issuing service signs the credential with a rotating signing key. Verification uses a key set (JWKS) that supports multiple active signing keys for rotation without invalidation.
