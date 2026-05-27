# Chapter 09: API Key Management & Scoping

> **Part:** 16 - User Management & Access Control

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [API Key Generation](sec-01-api-key-generation.md) | Secure random generation, key format (prefix + random + suffix), hashing for storage, key prefixes for identification |
| 02 | [Key Permission Scoping](sec-02-key-permission-scoping.md) | API key-specific permissions, scope restriction patterns, resource-level scoping, wildcard scopes |
| 03 | [Key Rotation & Expiry](sec-03-key-rotation-expiry.md) | Automatic expiry policies, rotation schedules, dual-key overlap, grace period handling |
| 04 | [Rate Limit per Key](sec-04-rate-limit-per-key.md) | Per-key rate limiting, burst allowance, rate limit tiers, distributed enforcement with Redis |
| 05 | [Usage Tracking & Quotas](sec-05-usage-tracking-quotas.md) | Per-key usage counters, monthly/ daily quotas, usage reset cycles, overage handling |
| 06 | [Key Revocation Flow](sec-06-key-revocation-flow.md) | Immediate revocation, cached key invalidation, in-flight request handling, user notification |
| 07 | [Developer Key Dashboard](sec-07-developer-key-dashboard.md) | Key listing with masked values, last used timestamp, usage graphs, quick revoke/create actions |
| 08 | [Key Security Best Practices](sec-08-key-security-best-practices.md) | Keys in environment variables, never log keys, key scanning prevention, client-side best practices |

---

## API Key Format

```
sk_live_tenant_abc123_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p
├── Prefix ─┘    ├── Tenant ──┘   ├── Secret (60+ bits entropy)
```

```typescript
// Key generation
function generateApiKey(tenantId: string): { key: string; hash: string } {
  const prefix = `sk_live_${tenantId.slice(0, 8)}_`;
  const secret = crypto.randomBytes(32).toString('hex');
  const key = prefix + secret;
  const hash = crypto.createHash('sha256').update(key).digest('hex');
  return { key, hash };
}
```

---

## Learning Objectives

- Implement secure API key generation with hashing
- Design key permission scoping with resource-level restrictions
- Create key rotation policies with dual-key overlap
- Build per-key rate limiting with Redis
- Implement per-key usage tracking and quota enforcement
- Design key revocation flow with immediate effect
- Build developer dashboard for key management
- Document key security best practices for developers
