# Auth Provider Abstraction

## Overview

An auth provider abstraction layer decouples the application from specific authentication providers (NextAuth/Auth.js, Clerk, Auth0), enabling future provider swaps without major application rewrites. This section covers the abstraction interface design, adapter pattern implementation, and provider-specific bridge modules.

## Abstraction Interface

```
┌─────────────────────────────────────────────────┐
│                  Application Code               │
│  (routes, middleware, API handlers, components) │
└──────────────────┬──────────────────────────────┘
                   │ uses
┌──────────────────▼──────────────────────────────┐
│            AuthService Interface                │
│  (abstracted, provider-agnostic)                │
│  - authenticate()                               │
│  - getUserSession()                             │
│  - createUser()                                 │
│  - updateUser()                                 │
│  - verifyToken()                                │
│  - refreshSession()                             │
└──────────────────┬──────────────────────────────┘
                   │ implemented by
        ┌──────────┼──────────────┐
        ▼          ▼              ▼
┌────────────┐┌──────────┐┌────────────┐
│ Auth.js    ││ Clerk   ││ Auth0      │
│ Adapter    ││ Adapter ││ Adapter    │
└────────────┘└──────────┘└────────────┘
```

## TypeScript Interface Design

```typescript
export interface AuthProviderConfig {
  type: 'authjs' | 'clerk' | 'auth0';
  clientId?: string;
  clientSecret?: string;
  issuer?: string;
  apiKey?: string;
}

export interface AuthUser {
  id: string;
  email: string;
  name: string;
  image?: string;
  tenantId: string;
  roles: string[];
  permissions: string[];
  mfaEnabled: boolean;
  metadata: Record<string, unknown>;
}

export interface SessionInfo {
  userId: string;
  tenantId: string;
  expiresAt: Date;
  accessToken: string;
  refreshToken?: string;
  mfaVerified: boolean;
}

export interface AuthResult {
  success: boolean;
  user?: AuthUser;
  session?: SessionInfo;
  error?: {
    code: string;
    message: string;
  };
}

export interface AuthService {
  authenticate(credentials: Record<string, unknown>): Promise<AuthResult>;
  getSession(token: string): Promise<SessionInfo | null>;
  getUser(userId: string): Promise<AuthUser | null>;
  createUser(userData: Partial<AuthUser>): Promise<AuthUser>;
  updateUser(userId: string, updates: Partial<AuthUser>): Promise<AuthUser>;
  deleteUser(userId: string): Promise<void>;
  verifyToken(token: string): Promise<{ valid: boolean; userId?: string }>;
  refreshSession(refreshToken: string): Promise<AuthResult>;
  revokeSession(userId: string, sessionId: string): Promise<void>;
  getSessions(userId: string): Promise<SessionInfo[]>;
}
```

## Adapter Pattern Implementation

The adapter pattern wraps each provider behind the `AuthService` interface:

```typescript
class AuthJsAdapter implements AuthService {
  private provider: AuthJsProvider;

  constructor(config: AuthProviderConfig) {
    this.provider = new AuthJsProvider({
      secret: config.clientSecret,
      trustHost: true,
    });
  }

  async authenticate(credentials: Record<string, unknown>): Promise<AuthResult> {
    try {
      const result = await this.provider.signIn('credentials', {
        ...credentials,
        redirect: false,
      });
      if (result?.error) {
        return { success: false, error: { code: 'AUTH_FAILED', message: result.error } };
      }
      const session = await this.provider.getSession();
      return {
        success: true,
        user: this.mapToAuthUser(session.user),
        session: this.mapToSessionInfo(session),
      };
    } catch (error) {
      return { success: false, error: { code: 'PROVIDER_ERROR', message: String(error) } };
    }
  }

  async getSession(token: string): Promise<SessionInfo | null> {
    const session = await this.provider.validateSessionToken(token);
    return session ? this.mapToSessionInfo(session) : null;
  }

  async verifyToken(token: string): Promise<{ valid: boolean; userId?: string }> {
    const decoded = await this.provider.decodeToken(token);
    if (!decoded || this.isExpired(decoded)) return { valid: false };
    return { valid: true, userId: decoded.sub };
  }

  private mapToAuthUser(providerUser: any): AuthUser {
    return {
      id: providerUser.id,
      email: providerUser.email,
      name: providerUser.name,
      image: providerUser.image,
      tenantId: providerUser.tenantId || 'default',
      roles: providerUser.roles || ['viewer'],
      permissions: providerUser.permissions || [],
      mfaEnabled: providerUser.mfaEnabled || false,
      metadata: providerUser.metadata || {},
    };
  }

  private mapToSessionInfo(providerSession: any): SessionInfo {
    return {
      userId: providerSession.userId,
      tenantId: providerSession.tenantId || 'default',
      expiresAt: new Date(providerSession.expires),
      accessToken: providerSession.accessToken,
      refreshToken: providerSession.refreshToken,
      mfaVerified: providerSession.mfaVerified || false,
    };
  }
}
```

## Provider Configuration Management

Store provider configuration in a database table to support multi-tenant provider selection:

```typescript
interface TenantAuthConfig {
  tenantId: string;
  provider: AuthProviderConfig;
  enabledProviders: string[];
  defaultProvider: string;
  allowSocialLogin: boolean;
  samlEnabled: boolean;
  oidcEnabled: boolean;
}
```

## Factory Pattern for Provider Selection

```typescript
class AuthServiceFactory {
  private static instances = new Map<string, AuthService>();

  static getProvider(tenantId: string): AuthService {
    const cacheKey = `${tenantId}:provider`;
    if (this.instances.has(cacheKey)) {
      return this.instances.get(cacheKey)!;
    }

    const config = loadTenantConfig(tenantId);
    const provider = this.createProvider(config.provider);
    this.instances.set(cacheKey, provider);
    return provider;
  }

  private static createProvider(config: AuthProviderConfig): AuthService {
    switch (config.type) {
      case 'authjs':
        return new AuthJsAdapter(config);
      case 'clerk':
        return new ClerkAdapter(config);
      case 'auth0':
        return new Auth0Adapter(config);
      default:
        throw new Error(`Unsupported auth provider: ${config.type}`);
    }
  }
}
```

## Cross-Cutting Concerns

### Caching
Cache provider instances per tenant and cache session lookups in Redis with TTL proportional to session lifetime.

### Error Translation
Map provider-specific errors to a canonical error set (`INVALID_CREDENTIALS`, `SESSION_EXPIRED`, `PROVIDER_UNAVAILABLE`, `RATE_LIMITED`).

### Health Checks
Each adapter must implement a `healthCheck()` method that verifies connectivity to the upstream provider.

```typescript
interface AuthService {
  // ... other methods
  healthCheck(): Promise<{ healthy: boolean; latency: number; message?: string }>;
}
```

## Open-Source Tools

- **Auth.js / NextAuth** — Primary open-source auth provider
- **Clerk** — Commercial provider with generous free tier
- **Auth0** — Enterprise identity platform
- **casbin** — Authorization integration alongside authentication
- **ioredis** — Redis client for session caching

## Production Considerations

- Warm provider instances on tenant creation to avoid cold-start latency on first auth
- Implement circuit breaker around provider calls to handle upstream outages gracefully
- Log all provider interactions for audit and debugging
- Add metrics for each provider operation (latency, error rate, success rate)
- Fallback chain: if primary provider is down, attempt secondary provider if configured
- Rate-limit provider creation to prevent resource exhaustion
