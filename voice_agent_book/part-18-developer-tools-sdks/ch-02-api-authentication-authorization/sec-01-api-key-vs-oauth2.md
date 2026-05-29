# Section 01: API Key vs OAuth2

## Overview

The Voice Agent API supports two authentication models: API keys for server-to-server machine communication and OAuth2 for user-facing applications. API keys are simple bearer tokens that identify a tenant, while OAuth2 provides delegated access with scoped permissions. The choice depends on the integration pattern — backend services use API keys for simplicity, while third-party integrations and user-facing dashboards use OAuth2 for granular permission control.

## Architecture

```
Authentication Model Comparison
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

API Key Flow (Machine-to-Machine):
  [Service A] ──→ Authorization: Bearer va_live_abc123 ──→ [API Gateway]
                                                                 │
                                                    [Validate Key]
                                                    [Check Scopes]

OAuth2 Flow (User-Facing):
  [User] ──→ [Client App] ──→ [Auth Server]
    │                              │
    │←─ Authorization Code ───────│
    │                              │
    ├─→ [Client App] ──→ [Token Exchange]
    │                              │
    │←─ Access Token (JWT) ───────│
    │                              │
    └─→ [API Gateway] ──→ Validate JWT ──→ [Service]

Use Case Comparison:
  API Key                          OAuth2
  ───────                          ──────
  Server-to-server                 User-facing apps
  Long-lived credentials           Short-lived tokens + refresh
  Simple to implement              Complex but flexible
  Single scope per key             Granular scope per user
  No user context                  User identity in token
  Ideal for SDK/CLI               Ideal for web dashboard
  Revoked manually                 Auto-expiring + refresh
```

## Design Decisions

- **Both Models Supported**: API keys for automation/backend; OAuth2 for end-user applications and marketplace integrations
- **API Key Prefix**: `va_live_` for production, `va_test_` for sandbox — instant environment identification
- **OAuth2 Authorizaton Code Flow**: Standard OAuth2 flow with PKCE for public clients (SPAs, mobile apps)
- **Scope Mapping**: Both models resolve to the same internal permission system — unified authorization regardless of auth method

## Implementation Approach

```typescript
// Authentication strategy pattern
interface AuthStrategy {
  type: 'api_key' | 'oauth2';
  authenticate(request: Request): Promise<AuthContext>;
}

interface AuthContext {
  tenantId: string;
  userId?: string;
  scopes: string[];
  authMethod: 'api_key' | 'oauth2';
  keyId?: string;
}

// API key strategy
class ApiKeyStrategy implements AuthStrategy {
  type = 'api_key' as const;

  async authenticate(request: Request): Promise<AuthContext> {
    const header = request.headers.get('Authorization');
    if (!header?.startsWith('Bearer ')) {
      throw new UnauthorizedError('Missing or invalid Authorization header');
    }

    const apiKey = header.slice(7);
    const { tenantId, keyId, scopes } = await this.apiKeyService.validateKey(apiKey);

    return { tenantId, scopes, authMethod: 'api_key', keyId };
  }
}

// OAuth2 strategy
class OAuth2Strategy implements AuthStrategy {
  type = 'oauth2' as const;

  async authenticate(request: Request): Promise<AuthContext> {
    const header = request.headers.get('Authorization');
    if (!header?.startsWith('Bearer ')) {
      throw new UnauthorizedError('Missing or invalid Authorization header');
    }

    const token = header.slice(7);
    const payload = await this.jwtService.verify(token);

    return {
      tenantId: payload.tenant_id,
      userId: payload.sub,
      scopes: payload.scopes,
      authMethod: 'oauth2',
    };
  }
}

// Strategy router
class AuthRouter {
  constructor(
    private apiKeyStrategy: ApiKeyStrategy,
    private oauth2Strategy: OAuth2Strategy,
  ) {}

  async authenticate(request: Request): Promise<AuthContext> {
    const apiKey = request.headers.get('Authorization');

    // API keys start with known prefixes
    if (apiKey?.startsWith('Bearer va_live_') || apiKey?.startsWith('Bearer va_test_')) {
      return this.apiKeyStrategy.authenticate(request);
    }

    // Otherwise, attempt OAuth2
    return this.oauth2Strategy.authenticate(request);
  }
}

// Strategic decision matrix
function recommendAuthMethod(context: {
  isServerToServer: boolean;
  hasUserContext: boolean;
  needsGranularPermissions: boolean;
  isThirdPartyApp: boolean;
}): 'api_key' | 'oauth2' {
  if (context.isServerToServer && !context.needsGranularPermissions) {
    return 'api_key';
  }
  if (context.hasUserContext || context.isThirdPartyApp) {
    return 'oauth2';
  }
  return 'api_key'; // Default for simple integrations
}
```

## Integration Points

- **SDK Authentication**: SDK accepts `apiKey` string for API key auth or `oauth2Token` for OAuth2; auto-detects which
- **API Gateway**: Gateway routes auth method to appropriate validation handler based on token prefix
- **Developer Portal**: Key management UI for API keys; OAuth2 app registration flow in developer settings

## Production Considerations

- **API Key Rotation**: Automated key rotation policy — keys older than 90 days trigger renewal reminders
- **OAuth2 Token Lifetime**: Access tokens expire in 1 hour; refresh tokens in 30 days with rolling rotation
- **Audit Trail**: Every authenticated request is logged with auth method, key ID, and user ID for audit compliance
- **Rate Limit Separation**: API keys and OAuth2 tokens have separate rate limit pools

## Open-Source Tools

- **Lucia Auth**: OAuth2 server implementation with refresh token support
- **Jose**: JWT verification and signing library
