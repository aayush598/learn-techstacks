# Section 01: Centralized Secrets Store

A centralized secrets store (HashiCorp Vault / AWS Secrets Manager / Azure Key Vault) manages all sensitive configuration: database credentials, API keys, encryption keys, service tokens, and TLS certificates. Secrets are stored encrypted, accessed via authenticated APIs, and rotated automatically. The platform never hard-codes secrets in source code or configuration files.

Secrets store architecture: secrets are organized by environment (production, staging, development) and service (api-server, worker, media-server). Each secret has a name, value (encrypted), metadata (created_at, version, rotation_schedule), and access policy. Secrets are versioned—applications specify a version or use "latest."

Access control: service accounts authenticate to the secrets store using mTLS certificates or short-lived tokens. Each service account has a policy defining which secrets it can read. Read access is audited. The secrets store is replicated across regions for availability. Emergency access procedures (break-glass) are documented and require multi-party approval.
