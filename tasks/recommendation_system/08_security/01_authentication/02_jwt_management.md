# JWT Management

## 1. Overview

JSON Web Tokens (JWT) are the primary authentication mechanism for recommendation system
APIs. JWTs enable stateless authentication where the token itself carries identity and
authorization information. This document covers token design, validation, refresh flows,
revocation, JWKS endpoints, and storage security for production recommendation systems.

### 1.1 JWT Structure

```
Header.Payload.Signature

Header:  {"alg": "RS256", "kid": "key-2026-01", "typ": "JWT"}
Payload: {"sub": "usr_a1b2c3d4", "iss": "auth.rec.example.com",
          "aud": "api.rec.example.com", "exp": 1705312800,
          "iat": 1705312200, "scope": "read:recommendations"}
Signature: RSASHA256(base64(header) + "." + base64(payload), private_key)
```

### 1.2 JWT Algorithm Selection

| Algorithm | Security | Performance | Use Case |
|---|---|---|---|
| RS256 (RSA) | High | Moderate | Standard API authentication |
| ES256 (ECDSA) | High | Fast | High-throughput services |
| EdDSA | Highest | Fastest | New implementations |
| HS256 (HMAC) | Moderate | Fastest | Internal service-to-service |

**Recommendation:** Use RS256 or ES256 for external APIs, HS256 for internal services only.

---

## 2. Token Design

### 2.1 Standard Claims

| Claim | Name | Required | Description |
|---|---|---|---|
| `iss` | Issuer | Yes | Token issuer URL |
| `sub` | Subject | Yes | User or service identifier |
| `aud` | Audience | Yes | Intended recipient(s) |
| `exp` | Expiration | Yes | Token expiry (Unix timestamp) |
| `iat` | Issued At | Yes | Token creation time |
| `nbf` | Not Before | Recommended | Token activation time |
| `jti` | JWT ID | Recommended | Unique token identifier |

### 2.2 Custom Claims for Recommendation Systems

| Claim | Type | Purpose |
|---|---|---|
| `scope` | string | API permission scope |
| `user_type` | string | Consumer, admin, service |
| `tenant_id` | string | Multi-tenant isolation |
| `device_id` | string | Device-level tracking |
| `region` | string | Geographic region |
| `rate_limit_tier` | string | Rate limit classification |
| `experiment_groups` | array | A/B test assignments |

### 2.3 Token Expiry Strategy

| Token Type | Expiry | Refresh | Rationale |
|---|---|---|---|
| Access token | 15 minutes | Yes (refresh token) | Short-lived for security |
| Refresh token | 7 days | Yes (rotation) | Long enough for UX |
| ID token | 1 hour | No (re-auth) | Session representation |
| Service token | 1 hour | Automatic | Service-to-service |

### 2.4 Token Size Considerations

Keep JWTs small to minimize network overhead:

- **Target size**: < 1KB per token
- **Large claims**: Move to server-side session, reference by ID
- **Role arrays**: Consider compressed encoding for many roles
- **Avoid PII**: Never include email, name, or other PII in JWT payload

---

## 3. Token Validation

### 3.1 Signature Validation

Every API endpoint must validate the JWT signature:

```
Validation Steps:
1. Extract algorithm from header
2. Verify algorithm is in allowed list (prevent algorithm confusion)
3. Fetch public key from JWKS endpoint (cached with TTL)
4. Verify signature matches payload using public key
5. Reject if signature invalid
```

**Critical security checks:**

- **Algorithm whitelisting**: Only accept RS256, ES256, EdDSA (never "none")
- **Key ID matching**: Verify `kid` header matches a known key in JWKS
- **Key type verification**: RSA key for RS256, EC key for ES256
- **Replay prevention**: Check `jti` against seen token cache

### 3.2 Expiry Validation

```
Current Time Validation:
├── exp > current_time + clock_skew_tolerance (not expired)
├── nbf <= current_time + clock_skew_tolerance (already active)
├── iat < current_time (not issued in future)
└── Clock skew tolerance: 30 seconds maximum
```

### 3.3 Audience Validation

| Validation | Check | Failure |
|---|---|---|
| Single audience | `aud` matches expected service | 401 Unauthorized |
| Multiple audiences | `aud` contains expected service | 401 Unauthorized |
| Wildcard audience | `aud` = `*` (rejected for security) | 401 Unauthorized |
| Missing audience | `aud` claim absent | 401 Unauthorized |

### 3.4 Issuer Validation

- Verify `iss` matches the expected issuer URL exactly
- Maintain allowlist of trusted issuers
- Reject tokens from unknown issuers
- Cache issuer public keys with appropriate TTL

### 3.5 Validation Failure Handling

| Failure Type | Response | Logging |
|---|---|---|
| Expired token | 401 with `token_expired` error | Log attempt |
| Invalid signature | 401 with `invalid_token` error | Log with IP, alert security |
| Wrong audience | 401 with `invalid_audience` error | Log attempt |
| Missing claims | 401 with `missing_claims` error | Log attempt |
| Algorithm not allowed | 401 with `invalid_algorithm` error | Alert security |

---

## 4. Token Refresh Flow

### 4.1 Standard Refresh Flow

```
Client                    Auth Server               API Gateway
  │                           │                          │
  │─── API Request ──────────>│                          │
  │    (access token expired) │                          │
  │<── 401 Unauthorized ─────│                          │
  │                           │                          │
  │─── Refresh Token ────────>│                          │
  │                           │── Validate refresh token │
  │                           │── Generate new tokens    │
  │<── New access + refresh ──│                          │
  │                           │                          │
  │─── API Request ──────────────────────────────────────>│
  │    (new access token)     │                          │
  │<── 200 OK ───────────────────────────────────────────│
```

### 4.2 Refresh Token Rotation

Refresh tokens must be rotated on each use to prevent token reuse:

- **One-time use**: Each refresh token is valid for exactly one refresh operation
- **Token family**: Track token lineage to detect stolen refresh tokens
- **Reuse detection**: If a previously used refresh token is presented, revoke entire family
- **Grace period**: Short window (30s) to handle concurrent refresh requests

### 4.3 Refresh Token Family Tracking

```
Token Family Tree:
Token A (initial) → Token B (rotation 1) → Token C (rotation 2) → ...
                          ↓ (stolen and reused)
                    → Revoke entire family
                    → Require re-authentication
```

### 4.4 Proactive Token Refresh

Clients should refresh tokens proactively before expiry:

- **Refresh window**: Refresh when token has < 5 minutes remaining
- **Background refresh**: Refresh during low-activity periods
- **Retry logic**: If refresh fails, retry with exponential backoff
- **Offline handling**: Queue refresh attempts when offline

---

## 5. Token Revocation

### 5.1 Revocation Strategies

| Strategy | Implementation | Latency | Use Case |
|---|---|---|---|
| Token expiry | Natural expiry | Passive | Normal token lifecycle |
| Revocation list | Check against revocation set | < 5ms | User logout, compromise |
| Short expiry + no refresh | Token expires quickly | Passive | Low-security endpoints |
| JWKS key rotation | Rotate signing keys | Minutes | Key compromise |

### 5.2 Revocation Implementation

**Approach 1: Token blacklist (Redis)**

- Store revoked token `jti` in Redis with TTL matching token expiry
- Check blacklist on every request (negligible latency with Redis)
- Automatic cleanup when tokens expire

**Approach 2: Key rotation**

- Rotate signing keys on revocation
- Old tokens signed with revoked key are invalid
- Clients must obtain new tokens with new key
- Applicable for mass revocation scenarios

### 5.3 Revocation Scenarios

| Scenario | Scope | Method | SLA |
|---|---|---|---|
| User logout | Single user | Blacklist current token | Immediate |
| Password change | Single user | Blacklist all user tokens | Immediate |
| Account compromise | Single user | Blacklist all user tokens | Immediate |
| Key compromise | All tokens | Rotate signing key | < 5 minutes |
| Security incident | All tokens | Rotate key + force re-auth | < 15 minutes |

### 5.4 Revocation Propagation

In distributed systems, revocation must propagate quickly:

- **Redis pub/sub**: Broadcast revocation events across instances
- **Local cache**: Cache revocation decisions locally (10s TTL)
- **Event streaming**: Kafka topic for revocation events
- **Consistency window**: Acceptable propagation delay < 10 seconds

---

## 6. JWKS Endpoint

### 6.1 JWKS Endpoint Design

```
GET /.well-known/jwks.json

Response:
{
  "keys": [
    {
      "kty": "RSA",
      "kid": "key-2026-01",
      "use": "sig",
      "alg": "RS256",
      "n": "0vx7agoebGcQSuu...",
      "e": "AQAB"
    },
    {
      "kty": "RSA",
      "kid": "key-2025-12",
      "use": "sig",
      "alg": "RS256",
      "n": "yK4FJXz0Bf9...",
      "e": "AQAB"
    }
  ]
}
```

### 6.2 Key Rotation via JWKS

- **New key generation**: Generate new key pair before old key expires
- **Key publication**: Add new key to JWKS endpoint
- **Overlap period**: Keep old key in JWKS for at least 24 hours
- **Key retirement**: Remove old key after overlap period
- **Signing transition**: Sign new tokens with new key immediately

### 6.3 JWKS Caching

API consumers must cache JWKS responses:

- **Cache TTL**: 1 hour (respect `Cache-Control` headers)
- **Key ID cache**: Cache public keys by `kid` for fast lookup
- **Invalidation**: Force JWKS refresh on `kid` not found
- **Stale-while-revalidate**: Serve cached keys while refreshing

---

## 7. Token Storage Security

### 7.1 Client-Side Storage

| Storage Method | Security | Persistence | Use Case |
|---|---|---|---|
| Memory (JavaScript) | Highest | Session only | SPA applications |
| HttpOnly secure cookie | High | Session/cookie TTL | Web applications |
| Secure enclave | High | Persistent | Mobile applications |
| LocalStorage | Low (XSS risk) | Persistent | Not recommended |

### 7.2 Server-Side Token Storage

| Storage | Security | Use Case |
|---|---|---|
| Encrypted database | High | Long-lived tokens, audit trail |
| Redis (encrypted) | High | Revocation lists, session mapping |
| In-memory (encrypted) | High | Token cache for validation |
| Vault/KMS | Highest | Signing keys, master secrets |

### 7.3 Token Transmission Security

- **HTTPS only**: All token transmission over TLS 1.3
- **No URL tokens**: Never pass tokens in URL query parameters
- **Authorization header**: Use `Authorization: Bearer <token>` header
- **CORS restrictions**: Limit token transmission to trusted origins
- **No logging**: Never log full tokens in application logs

### 7.4 Token Compromise Response

If a token is suspected compromised:

1. **Immediate revocation**: Blacklist the specific token
2. **Family revocation**: If refresh token, revoke entire token family
3. **User notification**: Notify user of potential compromise
4. **Session invalidation**: Invalidate all sessions for affected user
5. **Security audit**: Review access logs for suspicious activity
6. **Key rotation**: If signing key compromised, rotate immediately
