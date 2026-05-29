# Section 02: Bearer Token Implementation

## Overview

Bearer tokens in the Voice Agent API are JWT-encoded, signed with RS256, and contain tenant identity, user claims, and permission scopes. Token validation happens at the API gateway using cached public keys from the Auth Service. The JWT structure follows the standard registered claims (iss, sub, exp, iat) with custom claims for Voice Agent specific needs.

## Architecture

```
Bearer Token Validation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Token Minting:
  [Auth Service] ──→ Generate JWT ──→ Sign with Private Key
                        │
                   Payload:
                   {
                     "iss": "auth.voiceagent.com",
                     "sub": "user_abc123",
                     "tenant_id": "tenant_xyz",
                     "scopes": ["agents:read", "calls:write"],
                     "iat": 1684512345,
                     "exp": 1684515945
                   }

Token Validation:
  [API Gateway] ──→ Extract Bearer Token from Header
                        │
                   ┌────┴────┐
                   │Cache Hit│ ←── Public Key Cache
                   └────┬────┘
                        ↓
                   JWT Verification
                   ├── Signature valid?
                   ├── Token expired?
                   ├── Issuer trusted?
                   └── Scopes sufficient?
                        ↓
                   [Allow] or [401 Unauthorized]

Public Key Rotation:
  Auth Service publishes JWKS endpoint: /.well-known/jwks.json
  Gateway caches keys for 1 hour; refreshes on 401/validation failure
```

## Design Decisions

- **RS256 Over HS256**: Asymmetric signing allows any service to verify tokens without sharing secrets
- **JWKS Endpoint**: Public keys published at standard JWKS URI for automatic key rotation
- **Public Key Caching**: Gateway caches public keys for 1 hour to avoid auth service dependency on every request
- **Minimal Token Payload**: JWT contains only identity and scopes — user profile data is fetched on demand

## Implementation Approach

```typescript
import * as jose from 'jose';

// JWT payload structure
interface VoiceAgentTokenPayload {
  iss: string;
  sub: string;
  tenant_id: string;
  scopes: string[];
  iat: number;
  exp: number;
  jti?: string;  // JWT ID for revocation tracking
}

// Token verification with caching
class TokenValidator {
  private keyCache = new Map<string, jose.KeyLike>();
  private lastFetch = 0;
  private readonly cacheTTL = 3600_000; // 1 hour

  constructor(private jwksUrl: string) {}

  async validate(token: string): Promise<VoiceAgentTokenPayload> {
    const { payload } = await jose.jwtVerify(
      token,
      () => this.getPublicKey(token),
      {
        issuer: 'auth.voiceagent.com',
        algorithms: ['RS256'],
      },
    );

    return payload as unknown as VoiceAgentTokenPayload;
  }

  private async getPublicKey(token: string): Promise<jose.KeyLike> {
    const now = Date.now();

    if (now - this.lastFetch > this.cacheTTL) {
      await this.refreshKeyCache();
    }

    // Extract key ID from JWT header
    const protectedHeader = jose.decodeProtectedHeader(token);
    const keyId = protectedHeader.kid;

    if (!keyId || !this.keyCache.has(keyId)) {
      await this.refreshKeyCache();
    }

    const key = this.keyCache.get(keyId || '');
    if (!key) {
      throw new UnauthorizedError('Unknown key ID');
    }

    return key;
  }

  private async refreshKeyCache(): Promise<void> {
    const response = await fetch(this.jwksUrl);
    const jwks = await response.json() as jose.JSONWebKeySet;

    this.keyCache.clear();

    for (const jwk of jwks.keys) {
      const key = await jose.importJWK(jwk, 'RS256');
      this.keyCache.set(jwk.kid || '', key);
    }

    this.lastFetch = Date.now();
  }
}

// Token generation (Auth Service only)
class TokenMinter {
  private readonly privateKey: jose.KeyLike;

  constructor(privateKeyPem: string) {
    this.privateKey = jose.importPKCS8(privateKeyPem, 'RS256');
  }

  async mintToken(payload: Omit<VoiceAgentTokenPayload, 'iat' | 'exp' | 'iss' | 'jti'>): Promise<string> {
    const token = await new jose.SignJWT({
      ...payload,
      iss: 'auth.voiceagent.com',
      jti: crypto.randomUUID(),
    })
      .setProtectedHeader({ alg: 'RS256', kid: this.currentKeyId })
      .setIssuedAt()
      .setExpirationTime('1h')
      .sign(this.privateKey);

    return token;
  }
}

// Express/Hono middleware
function authenticate(validator: TokenValidator) {
  return async (c: Context, next: Next) => {
    const header = c.req.header('Authorization');

    if (!header?.startsWith('Bearer ')) {
      throw new UnauthorizedError('Missing Authorization header');
    }

    try {
      const token = header.slice(7);
      const payload = await validator.validate(token);
      c.set('authContext', payload);
      await next();
    } catch (error) {
      throw new UnauthorizedError('Invalid or expired token');
    }
  };
}
```

## Integration Points

- **Auth Service**: Central JWKS endpoint for key distribution
- **API Gateway**: Token validation middleware before routing to services
- **SDK**: Automatic token refresh handling for OAuth2 flows

## Production Considerations

- **Token Revocation**: Maintain a revocation list for immediate token invalidation; checked during validation
- **Clock Skew**: Allow 30-second clock skew tolerance for token expiration validation
- **Key Rotation Cadence**: Rotate signing keys every 90 days; keep previous key in JWKS during transition
- **Audit Logging**: Log all token validation failures for security monitoring

## Open-Source Tools

- **Jose**: JWT signing, verification, and JWKS handling
- **JWKS Endpoint**: Standard /\.well-known/jwks.json route
