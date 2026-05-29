# Section 07: Tenant-Specific Secrets Isolation

Tenant-specific secrets isolation ensures that one tenant's credentials, API keys, and integrations cannot be accessed by another tenant. Each tenant's secrets are stored in a separate namespace or path within the secrets store, with access policies that restrict each service to only its tenant's secrets. This is critical for multi-tenant key management.

Isolation architecture: secrets store path structure /tenants/{tenant_id}/{service}/{secret_name}. Access policies use path-based rules: path "tenants/abc123/api/*" grants read access to service-api for tenant abc123. Tenant secrets include: ML API keys (OpenAI, Anthropic), SMS provider credentials (Twilio), email service keys (SendGrid), and storage keys (S3).

Cross-tenant secret boundary: enforcement is at the secrets store level (path-based ACL) and the application level (tenant context from authentication). The application service never requests secrets for a tenant different from the authenticated tenant. Audit logs include tenant ID for verification. Regular penetration testing validates isolation.
