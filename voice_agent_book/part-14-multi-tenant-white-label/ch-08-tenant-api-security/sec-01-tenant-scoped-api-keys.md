# Section 01: Tenant-Scoped API Keys

Tenant-scoped API keys authenticate API requests and identify the tenant context. Each API key is bound to a specific tenant and carries that tenant's identity throughout request processing. Keys are hashed (SHA-256) before storage and presented as a bearer token in the Authorization header. The key system supports rotation, expiration, and revocation.

Key generation uses cryptographically random tokens (48 bytes from /dev/urandom, base64-encoded, prefixed with tenant type identifier). Keys have configurable expiration (never, 1 year, custom). Revoked keys are added to a Redis deny list. Key rotation is supported via dual-key pattern: secondary key becomes primary when rotation occurs.

For a voice agent platform, API keys also encode the key scope (read-only, read-write, admin) and allowed IP ranges. Key usage is audited with every request. Tenants can generate multiple keys for different applications or developers within their account.
