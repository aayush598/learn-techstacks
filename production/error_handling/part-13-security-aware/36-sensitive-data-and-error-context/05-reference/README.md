# Chapter 36 — Reference

> Part XIII · Chapter 36 · all sections · _Estimated reading time: 13 min_

## Data classification table

| Class | Examples | Response | Log | Metric | DLQ | Support | Tracker |
| ----- | -------- | -------- | --- | ------ | --- | ------- | ------- |
| **public** | code, message, requestId | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **internal** | class, provider, retryable | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **tenant** | own resource ids | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| **sensitive** | tenantId, userId | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| **pii** | email, name, phone, IP | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ (RBAC) |
| **payment** | last4, brand | ❌ | ❌ | ❌ | ❌ | ❌ | ⚠️ minimize |
| **secret** | tokens, keys, passwords | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **PAN / CVC** | full card, security code | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

## Control selection guide

| Control | Use for | Fails when |
| ------- | ------- | ---------- |
| **Omission** | Secrets, PAN, config values, raw payloads | Never (by construction) |
| **Allowlist** | All sink output | A needed field is unclassified |
| **Pseudonymize** | Values needing correlation (user id, email) | Salt not protected |
| **Sanitization** | Untrusted text (provider, driver) | New payload type appears |
| **Redaction** | Backstop for unavoidable third-party text | A sink forgets / new shape |

Preferred order: **omit → allowlist → pseudonymize → sanitize → redact.**

## Redaction pattern reference (backstop only)

| Category | Pattern target | Replacement |
| -------- | -------------- | ----------- |
| Bearer token | `Bearer <token>` | `Bearer [REDACTED]` |
| Stripe key | `sk_live_*`, `rk_live_*` | `[REDACTED_KEY]` |
| AWS key | `AKIA[0-9A-Z]{16}` | `[REDACTED_AWS_KEY]` |
| JWT | `eyJ*.eyJ*.*` | `[REDACTED_JWT]` |
| PEM | `-----BEGIN ... KEY-----` | `[REDACTED_PEM]` |
| Authorization/Cookie header | `authorization: ...` | `$1: [REDACTED]` |
| Email | `user@host.tld` | `[REDACTED_EMAIL]` |
| PAN-like | 13–19 digits | `[REDACTED_PAN]` |
| SSN-like | `ddd-dd-dddd` | `[REDACTED_SSN]` |
| Query secret | `?token=|?key=|?password=` | `[REDACTED]` |

> ⚠️ Regexes over-match. Keep patterns conservative; prefer omission/allowlist for values you control.

## Sensitive-data hiding places

| Hiding place | Typical content | Control |
| ------------ | --------------- | ------- |
| Message | echoed input, provider text | Constant message; reference value |
| Payload context | body, params | Never collect |
| Query string | tokens, email | Never log raw URL |
| Provider payload | request echo, card data, keys | Allowlist provider fields |
| Cause chain | raw driver/client errors | Per-node sanitize + bounds |
| Config error | passwords, keys | Reference config key name only |
| Webhook body | customer data, signature | Redact + tenant-scope |
| LLM prompt | user content, secrets | Stable code; no prompt |

## Bounds quick reference

| Bound | Default |
| ----- | ------- |
| Cause depth | 6 |
| Chain nodes | 10 |
| Message length | 300 chars |
| Stack length | 8000 chars |
| Total serialized size | a few KB |

## Standards & weaknesses

| Topic | Reference |
| ----- | --------- |
| Personal data definition | GDPR Art. 4(1) |
| Data minimization | GDPR Art. 5(1)(c), Art. 25 |
| Breach notification (72 h) | GDPR Art. 33 |
| Access / erasure | GDPR Art. 15 / 17 |
| Card data no store/log | PCI DSS v4.0 Req 3.3, 10.3 |
| Audit trails / log access | PCI DSS Req 10.5 |
| California personal info | CCPA / CPRA |
| Sensitive info in logs | CWE-532 |
| Info in error messages | CWE-209 |
| Private personal information | CWE-359 |
| Unsafe deserialization | CWE-502 |
| Log injection | CWE-117 |

## Chapter glossary

| Term | Meaning |
| ---- | ------- |
| **Sensitive metadata** | Error context that must not reach every sink |
| **Non-collection** | Never reading a value into an error (strongest control) |
| **Omission** | Not attaching a value at all |
| **Redaction** | Masking a collected value before a sink |
| **Sanitization** | Neutralizing untrusted text (control chars, length) |
| **Allowlist** | Emitting only classified-permitted fields; deny unknown |
| **Pseudonymization** | Replacing a value with a salted hash for correlation |
| **Fingerprint** | Short non-reversible hash prefix for correlation |
| **PAN** | Primary Account Number (full card number); never store/log |
| **Cause chain** | Nested error causes; a common leakage path |

## Related

- [Chapter 36 Do's and Don'ts](../04-dos-and-donts/README.md)
- [Deep Dive: Privacy-Aware Standards](../02-deep-dive/03-privacy-aware-standards.md)
- [Deep Dive: Safe Serialization and Context Allowlists](../02-deep-dive/02-safe-serialization-and-context-allowlists.md)
- [Chapter 34 — Security Principles for Error Handling](../../34-security-principles-for-error-handling/README.md)
- [Glossary](../../../GLOSSARY.md)

