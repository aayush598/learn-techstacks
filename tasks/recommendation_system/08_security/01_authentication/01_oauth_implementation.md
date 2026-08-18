# OAuth 2.0 Implementation for Recommendation APIs

## Overview

OAuth 2.0 provides the authorization framework for recommendation system APIs, controlling
who can access personalized recommendations, user data, and administrative endpoints. This
covers authorization flows for different client types, JWT token design, API key management,
multi-tenant authorization, and security best practices for production deployments.

## OAuth 2.0 Flows for Recommendation Systems

### Flow Selection Matrix

| Client Type          | Flow                        | Use Case                              |
|---------------------|----------------------------|---------------------------------------|
| Web application     | Authorization Code + PKCE   | User-facing recommendation UI         |
| Mobile app          | Authorization Code + PKCE   | Native mobile recommendation feed     |
| Server-to-server    | Client Credentials          | Batch recommendation generation       |
| Single-page app     | Authorization Code + PKCE   | React/Vue recommendation dashboard    |
| CLI / internal tool | Client Credentials          | Admin tools, debugging endpoints      |

### Authorization Code Flow (Web + PKCE)

**Step 1: Client initiates authorization**
```
GET /oauth/authorize?
  response_type=code
  &client_id=rec-app-web
  &redirect_uri=https://app.example.com/callback
  &scope=recommendations.read user.profiles.read
  &state=xyz123
  &code_challenge=E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM
  &code_challenge_method=S256
```

**Step 2: Resource owner authenticates and authorizes**
- User logs in and consents to requested scopes
- Authorization server issues authorization code

**Step 3: Client exchanges code for tokens**
```
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
&code=SplxlOBeZQQYbYS6WxSbIA
&redirect_uri=https://app.example.com/callback
&client_id=rec-app-web
&code_verifier=dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk
```

**Step 4: Token response**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "tGzv3JOkF0XG5Qx2TlKWIA",
  "scope": "recommendations.read user.profiles.read"
}
```

### Client Credentials Flow (Service-to-Service)

Used when the recommendation engine needs to call batch processing services, feature pipelines,
or other internal APIs without a user context:

```
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
&client_id=batch-processor-service
&client_secret=service-secret-key
&scope=recommendations.write features.read events.write
```

### PKCE for Mobile Applications

PKCE (Proof Key for Code Exchange) is mandatory for all public clients:

**Code Verifier Generation**:
- Cryptographically random string (43-128 characters)
- Characters: [A-Z] / [a-z] / [0-9] / "-" / "." / "_" / "~"
- Store in secure enclave (iOS Keychain, Android Keystore)

**Code Challenge Computation**:
- S256 method: `BASE64URL(SHA256(code_verifier))`
- Plain method: only for localhost development, never production

## JWT Token Design

### Access Token Structure

```json
{
  "header": {
    "alg": "RS256",
    "typ": "JWT",
    "kid": "rec-api-key-2024-01"
  },
  "payload": {
    "iss": "https://auth.rec-system.com",
    "sub": "user:a1b2c3d4",
    "aud": "https://api.rec-system.com",
    "exp": 1704067200,
    "iat": 1704063600,
    "jti": "unique-token-id-uuid",
    "scope": "recommendations.read user.profiles.read",
    "tenant": "enterprise-acme",
    "roles": ["user", "beta-tester"],
    "metadata": {
      "client_id": "rec-app-web",
      "device_type": "mobile",
      "session_id": "sess-xyz"
    }
  }
}
```

### Refresh Token Design

Refresh tokens should be:
- Opaque (not JWT) to prevent token introspection attacks
- Stored server-side with associated metadata
- Bound to the original client (client_id, device fingerprint)
- Rotated on each use (one-time use refresh tokens)
- Revocable immediately on security events

### Token Validation Checklist

Every API endpoint receiving a JWT must validate:

1. **Signature**: Verify using public key from authorization server
2. **Expiration**: Check `exp` claim is in the future
3. **Not Before**: Check `nbf` claim if present
4. **Issuer**: Verify `iss` matches expected authorization server
5. **Audience**: Verify `aud` includes this API's identifier
6. **Token ID**: Check `jti` is not in the revocation list
7. **Scope**: Verify token scope covers the requested operation
8. **Tenant**: Validate tenant context for multi-tenant systems

### Key Rotation Strategy

| Key Type            | Rotation Period | Grace Period | Method                      |
|---------------------|----------------|-------------|------------------------------|
| JWT signing key     | 90 days        | 7 days      | Dual-key publishing          |
| Client secrets      | 180 days       | 30 days     | Secret versioning            |
| API keys            | 365 days       | 60 days     | Key lifecycle management     |
| Encryption keys     | 365 days       | 30 days     | Envelope encryption          |

## Token Refresh Strategy

### Silent Token Refresh

For web and mobile clients, refresh tokens before they expire:

```
Client-side refresh logic:
1. On API call, check token expiration (exp claim)
2. If token expires within 5 minutes, initiate refresh
3. Use refresh token to obtain new access + refresh tokens
4. Update stored tokens atomically
5. Retry original API call with new access token
```

### Refresh Token Rotation

Implement one-time-use refresh tokens to prevent token theft:

1. Client uses refresh token to get new access token
2. Server issues new refresh token and invalidates the old one
3. If an already-used refresh token is presented, revoke entire token family
4. Alert security team on refresh token reuse detection

### Token Revocation

Implement token revocation for:
- User logout (revoke all tokens for the user)
- Security incident (revoke all tokens for a client or tenant)
- Password change (revoke all refresh tokens for the user)
- Admin action (revoke specific token by jti)

## API Key Management

### When to Use API Keys vs. OAuth Tokens

| Use Case                        | Mechanism         | Rationale                            |
|--------------------------------|-------------------|--------------------------------------|
| Public API access              | API keys          | Simple, rate-limited                 |
| User-context operations        | OAuth tokens      | User authorization, audit trail      |
| Service-to-service (internal)  | mTLS + tokens     | Strong identity verification         |
| Third-party integrations       | OAuth + API keys  | Fine-grained scope control           |

### API Key Lifecycle

```
Creation → Distribution → Rotation → Deactivation → Deletion
    │           │             │             │            │
    ▼           ▼             ▼             ▼            ▼
Generate    Secure         Auto-rotate   Grace period   Remove
random key  delivery       before expiry before removal from all
                           (90 days)     (30 days)      systems
```

### API Key Security

- Never expose API keys in URLs, logs, or error messages
- Store hashed API keys in the database (bcrypt/argon2)
- Rate limit per API key, not per IP
- Require API key + OAuth token for sensitive operations
- Monitor for API key usage from unexpected IP ranges or user agents

## Multi-Tenant Authorization

### Tenant Isolation Model

```
Request Flow:
  Client → API Gateway → Tenant Resolver → Authorization → Handler

Tenant Resolution:
1. Extract tenant from JWT claim, API key, or subdomain
2. Validate tenant exists and is active
3. Attach tenant context to request
4. All downstream services operate within tenant scope
```

### Data Isolation Strategies

| Strategy              | Isolation Level  | Cost    | Use Case                    |
|----------------------|-----------------|---------|------------------------------|
| Shared DB, shared schema | Lowest      | Low     | SaaS with trust between tenants |
| Shared DB, separate schema | Medium   | Medium  | Most multi-tenant SaaS      |
| Separate database      | High           | High    | Enterprise / regulated       |
| Separate cluster       | Highest        | Very High | Government / military      |

### Scope and Permission Matrix

| Role                  | Scopes                                                    |
|----------------------|-----------------------------------------------------------|
| Anonymous user       | recommendations.popular, items.read                       |
| Authenticated user   | recommendations.*, user.preferences.*, items.read         |
| Premium user         | recommendations.*, user.*, items.read, features.advanced  |
| Content creator      | items.create, items.update, analytics.own                 |
| Admin                | recommendations.*, user.*, items.*, admin.*              |
| Service account      | recommendations.write, features.*, events.*               |

## Security Best Practices

### OWASP Top 10 Mitigations

1. **Broken Authentication**: Use PKCE, rotate secrets, enforce MFA for admin
2. **Injection**: Validate all inputs, parameterize queries, escape outputs
3. **Sensitive Data Exposure**: Encrypt tokens at rest, use TLS everywhere
4. **XML External Entities**: Use JSON, disable XML processing
5. **Broken Access Control**: Validate scopes on every endpoint, least privilege
6. **Security Misconfiguration**: Hardened default configs, no debug in production
7. **Cross-Site Scripting**: Content Security Policy, output encoding
8. **Insecure Deserialization**: Validate message schemas, reject unknown fields
9. **Using Components with Known Vulnerabilities**: Automated dependency scanning
10. **Insufficient Logging**: Log all auth events, monitor for anomalies

### Rate Limiting for Auth Endpoints

| Endpoint               | Rate Limit                    | Rationale                      |
|------------------------|-------------------------------|--------------------------------|
| /oauth/authorize       | 10 requests/min per client    | Prevent authorization flooding  |
| /oauth/token           | 20 requests/min per client    | Prevent token brute force       |
| /oauth/token/revoke    | 5 requests/min per user       | Prevent token revocation abuse  |
| /api/v1/recommendations| 100 requests/min per user     | Normal usage protection         |
| /api/v1/recommendations| 1000 requests/min per service | Service-level protection        |

### Audit Logging

Every authentication and authorization event must be logged:

- Token issuance (who, when, what scopes, from which client)
- Token refresh (success and failure)
- Authorization failures (who tried, what they accessed, why denied)
- Token revocation (who revoked, what tokens, what reason)
- API key usage (key identifier, endpoint, timestamp, IP)

Logs must be tamper-proof, stored separately from application logs, and retained per compliance
requirements (typically 1-7 years depending on regulation).
