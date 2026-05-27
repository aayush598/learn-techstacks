# Chapter 02: API Authentication & Authorization

> **Part:** 18 - Developer Tools, SDKs & API Layer

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [API Key vs OAuth2](sec-01-api-key-vs-oauth2.md) | Use case comparison, machine-to-machine vs user-facing, security trade-offs, implementation complexity |
| 02 | [Bearer Token Implementation](sec-02-bearer-token-implementation.md) | JWT as bearer token, token validation middleware, public key caching, token introspection |
| 03 | [API Key Generation & Hashing](sec-03-api-key-generation-hashing.md) | Secure random generation, key prefixing, bcrypt/ SHA-256 hashing, constant-time comparison |
| 04 | [Permission Scoping for APIs](sec-04-permission-scoping-apis.md) | Scope strings, resource-level restrictions, wildcard scopes, scope validation |
| 05 | [Idempotency Keys](sec-05-idempotency-keys.md) | Idempotency key header, key storage and expiry, replay detection, response caching |
| 06 | [Request Signing](sec-06-request-signing.md) | HMAC request signing, nonce + timestamp, signature verification middleware |
| 07 | [API Security Headers](sec-07-api-security-headers.md) | CORS configuration, CSP headers, X-Content-Type-Options, Strict-Transport-Security |
| 08 | [Authentication Error Handling](sec-08-authentication-error-handling.md) | 401 vs 403 semantics, WWW-Authenticate header, error responses, rate limiting on auth failures |

---

## Authentication Flow

```
[Client]                          [API Gateway]                       [Auth Service]
   │                                    │                                  │
   │── Request + Authorization: Bearer ─→│                                  │
   │                                    │── Validate Token ──────────────→│
   │                                    │←── Token Claims + User Info ────│
   │                                    │                                  │
   │                                    │── Check Permissions ───────────│
   │                                    │←── Allowed / Denied ────────────│
   │                                    │                                  │
   │←── Response / 403 ────────────────│                                  │
```

---

## Learning Objectives

- Compare API key vs OAuth2 for different use cases
- Implement bearer token validation with public key caching
- Generate secure API keys with proper hashing
- Design permission scoping for API access
- Implement idempotency keys for safe retries
- Build request signing with HMAC
- Configure API security headers
- Handle authentication errors with proper HTTP semantics
