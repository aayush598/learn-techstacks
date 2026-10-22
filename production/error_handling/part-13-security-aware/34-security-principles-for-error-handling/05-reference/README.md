# Chapter 34 — Reference

> Part XIII · Chapter 34 · all sections · _Estimated reading time: 13 min_

## Disclosure policy matrix

What each audience may see, per field class. This table *is* the policy; the
[sanitizer](../03-practical-examples/01-error-sanitizer-allowlist-serializer.md) encodes it.

| Field class | Response | Log | Metric | DLQ | Support UI | Tracker |
| ----------- | -------- | --- | ------ | --- | ---------- | ------- |
| **public** (code, message, requestId) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **internal** (class, retryable, provider) | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **tenant** (own-tenant ids) | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| **sensitive** (tenantId, userId) | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| **pii** (email, name, phone) | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ (RBAC) |
| **secret** (tokens, keys, PAN) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

> ⚠️ **secret is denied at every sink including the tracker.** Secrets are never collected into an
> error object; use a fingerprint for correlation.

## Leakage classes → standard → control

| Leakage class | CWE | Standard | Control |
| ------------- | --- | -------- | ------- |
| Stack trace | CWE-209 | OWASP A05 | Generic 500; stack to tracker only |
| Schema/query | CWE-209 | OWASP A05 | Translate by SQLSTATE |
| Infrastructure | CWE-497 | OWASP A05 | Strip hostnames/headers |
| Secrets | CWE-532, CWE-798 | PCI Req 3.3 | Never collect; fingerprint |
| PII | CWE-359 | GDPR Art. 32/33 | Minimize; tracker-only |
| Tenant data | OWASP A01/A04 | — | Tenant-scope all keys/sinks |
| Enumeration | CWE-204 | OWASP A07 | Uniform responses |
| Timing | CWE-203, CWE-208 | OWASP A07 | Constant-time + constant-work |
| Injection via errors | CWE-89/78/117 | OWASP A03 | Parameterize; structured logs |
| Reflection | CWE-79/113 | OWASP A03 | Escape per sink; validate input |
| Pathological-failure DoS | CWE-400 | — | Bound work and serialization |
| Unsafe deserialization | CWE-502 | OWASP A08 | Schema-validate payloads |

## HTTP status quick choices

| Scenario | Status | Rationale |
| -------- | ------ | --------- |
| Unknown exception | `500` | Generic; nothing disclosed |
| Invalid credentials (any case) | `401` | Uniform for login |
| Insufficient role, resource known | `403` | Caller knows it exists |
| Resource opaque or other-tenant | `404` | Do not confirm existence |
| Invalid input | `400`/`422` | Public, non-revealing detail |
| Auth dependency unavailable | `503` | Fail closed; do not leak |

## Constant-time comparison quick reference

| Language | Primitive |
| -------- | --------- |
| Node.js | `crypto.timingSafeEqual` |
| Python | `hmac.compare_digest` |
| Go | `crypto/subtle.ConstantTimeCompare` |
| Java | `java.security.MessageDigest.isEqual` |
| Rust | `subtle::ConstantTimeEq` |

Rules: compare **digests**, keep lengths non-secret (or hash to fixed length), and check both real
and dummy paths.

## Channel → control cheat sheet

| Channel | Control | Gotcha |
| ------- | ------- | ------ |
| Response | Allowlist serializer | Body length can still leak |
| Log | Structured + minimize | Exported widely to vendors |
| Metric | Bounded labels | High cardinality hides PII |
| DLQ | Strip secrets pre-enqueue | Persists for days |
| Support | Tenant-scoped projection | Widest human access |
| Headers | Strip banners at proxy | Easy to forget |
| Tracker | Full detail + RBAC | Sometimes broadly readable |

## 401 vs 403 vs 404 decision

```text
Caller authenticated?
  ├─ no ───────────────────────────▶ 401 (uniform for all credential failures)
  └─ yes
      Resource existence OK to reveal?
        ├─ yes ───────────────────▶ 403 if role insufficient
        └─ no ────────────────────▶ 404 (identical to real not-found)
```

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| **Disclosure channel** | A sink through which an error's data can leave the process |
| **Secure default** | Generic external outcome for any unknown failure |
| **Fail closed** | Deny on error (security default); opposite of fail open |
| **Enumeration oracle** | Any observable difference revealing valid identifiers |
| **Timing oracle** | A latency difference correlating with a secret |
| **Constant-time** | Comparison whose duration is independent of input values |
| **Constant-work** | Same amount of work regardless of input validity |
| **Non-collection** | Never reading a secret into the error (vs redacting) |
| **Allowlist serialization** | Emit only classified-permitted fields; deny unknown |
| **Fingerprint** | Short non-reversible hash prefix for correlation |
| **Canary test** | Injected secret/PII that must not survive any sink |

## Related

- [Chapter 34 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Deep Dive: Information Disclosure Channels](../02-deep-dive/01-information-disclosure-channels.md)
- [Chapter 35 — Auth, Authorization, and Tenant Isolation Errors](../../35-auth-authorization-and-tenant-isolation-errors/README.md)
- [Chapter 36 — Sensitive Data and Error Context](../../36-sensitive-data-and-error-context/README.md)
- [Glossary](../../../GLOSSARY.md)

