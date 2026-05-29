# Section 03: Automatic Secret Rotation

Automatic secret rotation reduces the window of exposure if a secret is compromised. The rotation system updates secrets on a schedule (database passwords every 90 days, API keys every 180 days, TLS certificates every 60 days) or on-demand (triggered by security events). Rotation is performed without service downtime.

Rotation workflow: generate new secret value → store as new version in secrets store → update dependent services (new deployment with updated secret reference) → validate service health with new secret → deactivate old secret after cooldown period (allowing connections to drain) → delete old secret after observation window.

Zero-downtime rotation: for database credentials, the application connects using a connection pool that supports credential refresh. The pool is configured with both old and new credentials during rotation. Existing connections continue with old credentials until they close. New connections use new credentials. This eliminates connection drops during rotation.
