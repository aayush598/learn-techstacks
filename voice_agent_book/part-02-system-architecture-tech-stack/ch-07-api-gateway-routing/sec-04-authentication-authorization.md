# Section 04: Authentication & Authorization

## Auth Architecture

Authentication uses **Auth.js** for user authentication (OAuth 2.0, email/password, SAML SSO) and **API key validation** for machine-to-machine communication. Authorization is handled via **RBAC** with scope-based permission checks.

```
┌─────────────────────────────────────────────────────────────────────┐
│               AUTHENTICATION & AUTHORIZATION FLOW                   │
│                                                                     │
│  ┌──────────┐    ┌──────────┐    ┌─────────────────────────────┐   │
│  │ Browser  │    │  Mobile  │    │  3rd Party API Client       │   │
│  │ (Session)│    │ (JWT)    │    │  (API Key)                  │   │
│  └────┬─────┘    └────┬─────┘    └──────────┬──────────────────┘   │
│       │               │                     │                      │
│       ▼               ▼                     ▼                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    AUTH MIDDLEWARE                           │   │
│  │                                                              │   │
│  │  ┌──────────────────┐  ┌──────────────────┐                 │   │
│  │  │  Session Auth     │  │  API Key Auth    │                 │   │
│  │  │  (Auth.js)        │  │  (Hash lookup)   │                 │   │
│  │  │                   │  │                  │                 │   │
│  │  │  1. Read session  │  │  1. Extract key  │                 │   │
│  │  │  2. Validate in   │  │  2. SHA-256 hash │                 │   │
│  │  │     DB/lucia      │  │  3. Redis lookup │                 │   │
│  │  │  3. Get user +    │  │  4. Get tenant + │                 │   │
│  │  │     tenant        │  │     scopes       │                 │   │
│  │  │  4. Extract roles │  │  5. Check active │                 │   │
│  │  └──────────────────┘  └──────────────────┘                 │   │
│  │                                                              │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │              AUTHORIZATION CHECK                    │   │   │
│  │  │  1. Extract required scopes from route definition    │   │   │
│  │  │  2. Check user roles → resolved permissions         │   │   │
│  │  │  3. Verify scope intersection: user.scopes ∩ route   │   │   │
│  │  │  4. Deny if empty intersection                      │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                     │
│                              ▼                                     │
│                     ┌──────────────────┐                          │
│                     │  Proceed to      │                          │
│                     │  Route Handler   │                          │
│                     └──────────────────┘                          │
└─────────────────────────────────────────────────────────────────────┘
```

## API Key Validation

```typescript
interface ApiKey {
  id: string;
  keyPrefix: string;       // First 8 chars for identification
  keyHash: string;         // SHA-256 hash of full key
  tenantId: string;
  userId: string;
  name: string;
  scopes: string[];
  expiresAt?: Date;
  isActive: boolean;
  lastUsedAt?: Date;
  createdAt: Date;
}

// API key format: va_live_xxxxxxxxxxxx (prefix: 2 chars type + 4 chars env + _)
// Full key stored only at creation time; only hash persisted

async function validateApiKey(authHeader: string): Promise<AuthResult> {
  const match = authHeader.match(/^Bearer\s+(va_\w+)$/);
  if (!match) {
    return { authenticated: false, error: 'invalid_api_key_format' };
  }

  const apiKey = match[1];
  const keyHash = crypto.createHash('sha256').update(apiKey).digest('hex');
  const keyPrefix = apiKey.slice(0, 8);

  const stored = await redis.get<ApiKey>(`api_key:hash:${keyHash}`);
  if (!stored) {
    return { authenticated: false, error: 'api_key_not_found' };
  }

  if (!stored.isActive) {
    return { authenticated: false, error: 'api_key_disabled' };
  }

  if (stored.expiresAt && new Date() > stored.expiresAt) {
    return { authenticated: false, error: 'api_key_expired' };
  }

  // Update last used timestamp asynchronously
  redis.pipeline()
    .set(`api_key:hash:${keyHash}`, { ...stored, lastUsedAt: new Date() })
    .expire(`api_key:hash:${keyHash}`, 3600)
    .exec();

  return {
    authenticated: true,
    tenantId: stored.tenantId,
    userId: stored.userId,
    scopes: stored.scopes,
    authMethod: 'api_key',
  };
}
```

## OAuth 2.0 / SSO Integration

```typescript
// Auth.js configuration
export const authConfig = {
  providers: [
    // Email/Password (Credentials provider)
    Credentials({
      async authorize(credentials) {
        const user = await db.user.findUnique({
          where: { email: credentials.email },
          include: { tenant: true, roles: true },
        });
        if (!user || !await verifyPassword(credentials.password, user.passwordHash)) {
          return null;
        }
        return { id: user.id, email: user.email, tenantId: user.tenantId, roles: user.roles };
      },
    }),
    // Google OAuth
    GoogleProvider({ clientId: env.GOOGLE_CLIENT_ID, clientSecret: env.GOOGLE_CLIENT_SECRET }),
    // Microsoft Entra ID (SAML/SSO)
    AzureADProvider({ clientId: env.AZURE_CLIENT_ID, clientSecret: env.AZURE_CLIENT_SECRET, tenantId: env.AZURE_TENANT_ID }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.tenantId = user.tenantId;
        token.roles = user.roles;
        token.permissions = await resolvePermissions(user.roles);
      }
      return token;
    },
  },
};
```

## Role-Based Access Control

```typescript
// Permission model
type Permission = `agents:${Action}` | `calls:${Action}` | `campaigns:${Action}` | `billing:${Action}` | `users:${Action}` | `settings:${Action}`;
type Action = 'read' | 'write' | 'delete' | 'admin' | 'export';

interface Role {
  id: string;
  name: string;
  permissions: Permission[];
  isSystem: boolean; // Cannot be modified
}

const SYSTEM_ROLES: Role[] = [
  { id: 'owner', name: 'Owner', permissions: ['*'], isSystem: true },
  { id: 'admin', name: 'Admin', permissions: ['agents:*', 'calls:*', 'campaigns:*', 'billing:read', 'users:*', 'settings:*'], isSystem: true },
  { id: 'operator', name: 'Operator', permissions: ['agents:read', 'calls:*', 'campaigns:read', 'billing:read'], isSystem: true },
  { id: 'analyst', name: 'Analyst', permissions: ['calls:read', 'campaigns:read', 'billing:read'], isSystem: true },
  { id: 'developer', name: 'Developer', permissions: ['agents:*', 'calls:read', 'campaigns:read'], isSystem: true },
];

// Authorization check middleware
function authorize(scopes: string[]) {
  return (req: NextRequest, ctx: GatewayContext) => {
    if (!ctx.userId) {
      return formatError('unauthorized', 'Authentication required', 401);
    }

    const userPermissions = resolveUserPermissions(ctx.userId, ctx.tenantId);
    const hasScope = scopes.every(scope =>
      userPermissions.includes('*') ||
      userPermissions.includes(scope) ||
      userPermissions.includes(scope.split(':')[0] + ':*')
    );

    if (!hasScope) {
      return formatError('forbidden', 'Insufficient permissions', 403, {
        required: scopes,
        missing: scopes.filter(s => !userPermissions.includes(s)),
      });
    }

    return null; // Continue
  };
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Auth library | Auth.js (NextAuth v5) | Framework-native, multiple providers, session management |
| API key format | `va_{env}_{random}` with hash storage | Identifiable prefix, secure hash-only persistence |
| Token storage | JWT with HTTP-only cookies (web) + Bearer header (API) | Secure, stateless, cross-origin compatible |
| Authorization model | RBAC + Scopes | Simple to understand, scalable, auditable |
| Session management | Database sessions via lucia | Revocable, no JWT expiry issues |

## Integration Points

- **Ch 02 (Next.js Architecture)** — Auth middleware in Next.js middleware.ts
- **Ch 05 (Microservices)** — Service-to-service auth uses mTLS + JWT
- **Ch 10 (Security)** — Rate limiting on auth endpoints, brute force protection

## Production Considerations

- **Brute Force Protection**: 5 failed attempts → 15-minute lockout; exponential backoff after
- **Key Rotation**: API keys rotated every 90 days; dual-key window for 7 days during rotation
- **Audit Logging**: All auth events logged (login, key usage, permission denied) to ClickHouse
- **Session Expiry**: Web sessions expire after 24h, refresh token after 7 days
- **MFA**: Time-based One-Time Password (TOTP) via `otplib` for admin roles
