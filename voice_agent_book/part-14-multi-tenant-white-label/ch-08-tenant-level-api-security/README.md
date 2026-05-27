# Chapter 08: Tenant-Level API Security

> **Part:** 14 - Multi-Tenant & White-Label

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [API Key Scoping per Tenant](sec-01-api-key-scoping.md) | Tenant-scoped key model, key metadata, permission boundaries, multi-tenant key isolation |
| 02 | [Tenant-Specific Key Generation](sec-02-tenant-key-generation.md) | Key generation algorithms (SHA-256 hashing), key prefixes, entropy sources, collision prevention |
| 03 | [API Key Rotation Policies](sec-03-api-key-rotation.md) | Rotation schedules, dual-key overlap period, rotation notification, automated rotation |
| 04 | [Permission Boundaries & RBAC](sec-04-permission-boundaries-rbac.md) | IAM-style permission policies, resource-level restrictions, action-based permissions, boundary evaluation |
| 05 | [Request Validation & Tenant Context](sec-05-request-validation-tenant-context.md) | Tenant ID extraction from key, request validation pipeline, tenant mismatch detection |
| 06 | [Rate Limiting per Tenant](sec-06-rate-limiting-per-tenant.md) | Distributed rate limiting (Redis), per-tenant buckets, burst allowance, rate limit tiers |
| 07 | [API Audit Logging per Tenant](sec-07-api-audit-logging.md) | Per-request audit trail, tenant context in logs, immutable log storage, log retention |
| 08 | [Key Compromise Response](sec-08-key-compromise-response.md) | Immediate key revocation, compromised key detection, alerting workflow, incident response playbook |

---

## API Key Model

```
{
  key_prefix: "sk_live_tenant_abc123_",
  key_hash: "sha256$<hashed_value>",
  tenant_id: "tenant_uuid",
  permissions: ["calls:read", "calls:write", "agents:read"],
  rate_limit: { tier: "professional", rpm: 1000 },
  created_at: "2025-01-01T00:00:00Z",
  expires_at: "2026-01-01T00:00:00Z",
  last_used_at: "2025-06-01T00:00:00Z"
}
```

---

## Learning Objectives

- Design tenant-scoped API keys with permission boundaries
- Implement secure key generation with hashing and prefixing
- Create key rotation policies with dual-key overlap
- Build permission boundary evaluation engine
- Implement request validation with tenant context extraction
- Design distributed rate limiting per tenant
- Create per-tenant API audit logging pipeline
- Develop key compromise detection and response workflow
