# Section 07: Inter-Service Auth & Security

## Service Security Architecture

Inter-service communication must be authenticated and authorized at multiple layers — transport (mTLS), application (JWT), and data (scope-based access). This defense-in-depth approach prevents unauthorized access even if one layer is compromised.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    INTER-SERVICE SECURITY LAYERS                       │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  LAYER 1: TRANSPORT SECURITY (mTLS via Istio)                  │    │
│  │                                                                  │    │
│  │  ┌──────────┐     ┌──────────┐     ┌──────────┐                │    │
│  │  │ Service A │────▶│  Envoy   │────▶│ Service B │               │    │
│  │  │           │     │ Sidecar  │     │           │               │    │
│  │  │ App:      │     │          │     │ App:      │               │    │
│  │  │ call-svc  │     │ mTLS     │     │ agent-svc │               │    │
│  │  └──────────┘     └──────────┘     └──────────┘                │    │
│  │                                                                  │    │
│  │  Identity: spiffe://cluster.local/ns/voice-platform/sa/call-svc │    │
│  │  Verified by: Istio Citadel (SPIFFE-compatible)                │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  LAYER 2: APPLICATION AUTH (Service-to-Service JWT)              │    │
│  │                                                                  │    │
│  │  ┌──────────────────────────────────────────────────────────┐   │    │
│  │  │  Service A generates short-lived JWT for Service B        │   │    │
│  │  │                                                          │   │    │
│  │  │  Header: Authorization: Bearer <service-jwt>            │   │    │
│  │  │                                                          │   │    │
│  │  │  JWT Claims:                                            │   │    │
│  │  │  {                                                      │   │    │
│  │  │    "iss": "call-service",                               │   │    │
│  │  │    "sub": "spiffe://.../sa/call-service",               │   │    │
│  │  │    "aud": "agent-service",                              │   │    │
│  │  │    "scope": ["agents:read", "calls:write"],             │   │    │
│  │  │    "iat": 1700000000,                                   │   │    │
│  │  │    "exp": 1700000300                                    │   │    │
│  │  }                                                          │   │    │
│  │  └──────────────────────────────────────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │  LAYER 3: AUTHORIZATION (Scope Enforcement)                     │    │
│  │                                                                  │    │
│  │  ┌──────────────┐     ┌──────────────┐                          │    │
│  │  │  Request      │────▶│  AuthZ       │────▶ Allow/Deny         │    │
│  │  │  + JWT Scopes │     │  Check       │                          │    │
│  │  └──────────────┘     └──────────────┘                          │    │
│  │                                                                  │    │
│  │  Rules:                                                         │    │
│  │  • Call Service → Agent Service: agents:read only               │    │
│  │  • Agent Service → Call Service: calls:read only                │    │
│  │  • Voice Service → AI Service: ai:transcript only               │    │
│  │  • Campaign Service → Call Service: calls:write only            │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Service Identity & JWT

```typescript
// lib/auth/service-auth.ts
import { SignJWT, jwtVerify, type JWTPayload } from 'jose'
import { Redis } from 'ioredis'

interface ServiceToken {
  iss: string       // Issuer (service name)
  sub: string       // Subject (SPIFFE ID)
  aud: string       // Audience (target service)
  scope: string[]   // Permissions
  iat: number       // Issued at
  exp: number       // Expires
  jti: string       // JWT ID (unique)
}

export class ServiceAuth {
  private redis: Redis
  private readonly JWT_EXPIRY = 300  // 5 minutes
  private readonly JWT_LEEWAY = 30    // 30 seconds clock skew

  constructor(redis: Redis) {
    this.redis = redis
  }

  // Generate service-to-service JWT
  async generateServiceToken(
    audience: string,
    scope: string[]
  ): Promise<string> {
    const serviceName = process.env.SERVICE_NAME ?? 'unknown'
    const spiffeId = process.env.SPIFFE_IDENTITY
      ?? `spiffe://cluster.local/ns/${process.env.NAMESPACE}/sa/${serviceName}`

    const now = Math.floor(Date.now() / 1000)

    const token = await new SignJWT({
      iss: serviceName,
      sub: spiffeId,
      aud: audience,
      scope,
      jti: crypto.randomUUID()
    } satisfies ServiceToken)
      .setProtectedHeader({ alg: 'RS256' })
      .setIssuedAt(now)
      .setExpirationTime(now + this.JWT_EXPIRY)
      .sign(await this.getPrivateKey())

    return token
  }

  // Verify service-to-service JWT
  async verifyServiceToken(
    token: string,
    expectedAudience: string
  ): Promise<ServiceToken> {
    try {
      const { payload } = await jwtVerify(token, await this.getPublicKey(), {
        audience: expectedAudience,
        issuer: [
          'call-service',
          'agent-service',
          'voice-service',
          'ai-service',
          'campaign-service',
          'billing-service',
          'auth-service',
          'notification-service'
        ],
        clockTolerance: this.JWT_LEEWAY
      })

      // Check if token has been revoked
      const jti = payload.jti as string
      const revoked = await this.redis.exists(`revoked:jwt:${jti}`)
      if (revoked) {
        throw new Error('Token has been revoked')
      }

      return payload as unknown as ServiceToken
    } catch (error) {
      throw new ServiceAuthError('Invalid service token', { cause: error })
    }
  }

  // Revoke a token (for security incidents)
  async revokeToken(jti: string): Promise<void> {
    await this.redis.set(`revoked:jwt:${jti}`, '1', { ex: this.JWT_EXPIRY })
  }

  private async getPrivateKey(): Promise<CryptoKey> {
    // Load from Vault or mounted secret
    const keyPem = await this.loadSecret('service-private-key')
    return await crypto.subtle.importKey(
      'pkcs8',
      this.pemToBuffer(keyPem),
      { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' },
      false,
      ['sign']
    )
  }

  private async getPublicKey(): Promise<CryptoKey> {
    const keyPem = await this.loadSecret('service-public-key')
    return await crypto.subtle.importKey(
      'spki',
      this.pemToBuffer(keyPem),
      { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' },
      false,
      ['verify']
    )
  }

  private async loadSecret(name: string): Promise<string> {
    // Try environment first (K8s secret mounted as env)
    const envVar = process.env[name.toUpperCase().replace(/-/g, '_')]
    if (envVar) return envVar

    // Fallback to Vault
    const response = await fetch(
      `${process.env.VAULT_URL}/v1/secret/data/${name}`,
      { headers: { 'X-Vault-Token': process.env.VAULT_TOKEN! } }
    )
    const data = await response.json()
    return data.data.data[name]
  }

  private pemToBuffer(pem: string): ArrayBuffer {
    const pemHeader = '-----BEGIN KEY-----'
    const pemFooter = '-----END KEY-----'
    const pemContents = pem.substring(pemHeader.length, pem.length - pemFooter.length)
    const binaryDer = atob(pemContents)
    const bytes = new Uint8Array(binaryDer.length)
    for (let i = 0; i < binaryDer.length; i++) {
      bytes[i] = binaryDer.charCodeAt(i)
    }
    return bytes.buffer
  }
}
```

## Request Interception & Validation

```typescript
// Middleware for incoming service requests
import { ServiceAuth } from '@/lib/auth/service-auth'
import { logger } from '@/lib/logger'

interface AuthenticatedRequest extends Request {
  serviceToken?: ServiceToken
}

export function requireServiceAuth(
  allowedScopes: string[],
  audience: string
): (handler: Function) => Function {
  const serviceAuth = new ServiceAuth(redis)

  return (handler: Function) => {
    return async (req: AuthenticatedRequest, ...args: unknown[]) => {
      try {
        // Extract token
        const authHeader = req.headers.get('authorization')
        if (!authHeader?.startsWith('Bearer ')) {
          return new Response(
            JSON.stringify({ error: 'Missing service token' }),
            { status: 401, headers: { 'Content-Type': 'application/json' } }
          )
        }

        const token = authHeader.slice(7)

        // Verify token
        const serviceToken = await serviceAuth.verifyServiceToken(token, audience)
        req.serviceToken = serviceToken

        // Check scopes
        const hasScope = allowedScopes.some(s => serviceToken.scope.includes(s))
        if (!hasScope) {
          logger.warn({
            service: serviceToken.iss,
            requiredScopes: allowedScopes,
            hasScopes: serviceToken.scope
          }, 'Service authorization denied')

          return new Response(
            JSON.stringify({ error: 'Insufficient permissions' }),
            { status: 403, headers: { 'Content-Type': 'application/json' } }
          )
        }

        // Call handler
        return handler(req, ...args)

      } catch (error) {
        if (error instanceof ServiceAuthError) {
          return new Response(
            JSON.stringify({ error: error.message }),
            { status: 401 }
          )
        }

        logger.error({ error }, 'Service auth middleware error')
        return new Response(
          JSON.stringify({ error: 'Internal error' }),
          { status: 500 }
        )
      }
    }
  }
}

// Usage in service
import { requireServiceAuth } from '@/lib/auth/service-auth'

export const GET = requireServiceAuth(
  ['agents:read'],
  'agent-service'
)(async (req: AuthenticatedRequest) => {
  const agents = await agentService.listAgents()
  return Response.json({ data: agents })
})
```

## Network Policies

```yaml
# Kubernetes NetworkPolicy for service isolation
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: call-service-network-policy
  namespace: voice-platform
spec:
  podSelector:
    matchLabels:
      app: call-service
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: api-gateway
        - podSelector:
            matchLabels:
              app: campaign-service
        - podSelector:
            matchLabels:
              app: voice-service
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: istio-system
      ports:
        - protocol: TCP
          port: 3002  # REST API
        - protocol: TCP
          port: 50052 # gRPC
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: agent-service
      ports:
        - protocol: TCP
          port: 3001
    - to:
        - podSelector:
            matchLabels:
              app: billing-service
      ports:
        - protocol: TCP
          port: 3005
    - to:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: kube-system
      ports:
        - protocol: UDP
          port: 53  # DNS
    - to:
        - ipBlock:
            cidr: 0.0.0.0/0
            except:
              - 10.0.0.0/8
              - 172.16.0.0/12
              - 192.168.0.0/16
      ports:
        - protocol: TCP
          port: 443  # External HTTPS
```

## Secret Propagation

```typescript
// lib/secrets/vault.ts
// HashiCorp Vault integration for dynamic secrets

import Vault from 'node-vault'

export class VaultManager {
  private client: Vault.client

  constructor() {
    this.client = Vault({
      endpoint: process.env.VAULT_URL!,
      token: process.env.VAULT_TOKEN!
    })
  }

  // Get database credentials (dynamic, rotated)
  async getDatabaseCredentials(): Promise<{
    username: string
    password: string
  }> {
    const result = await this.client.read('database/creds/voice-platform-role')
    return {
      username: result.data.username,
      password: result.data.password
    }
  }

  // Get API key for external service
  async getApiKey(service: string): Promise<string> {
    const result = await this.client.read(`secret/data/api-keys/${service}`)
    return result.data.data.key
  }

  // Rotate a secret
  async rotateSecret(path: string): Promise<void> {
    await this.client.write(`${path}/rotate`, {})
    logger.info({ path }, 'Secret rotated')
  }
}

// Auto-refresh database credentials
export function setupCredentialRotation(prisma: PrismaClient): void {
  const vault = new VaultManager()

  // Refresh every 24 hours (Vault dynamic creds default TTL)
  setInterval(async () => {
    try {
      const creds = await vault.getDatabaseCredentials()
      await prisma.$executeRawUnsafe(
        `SELECT set_config('app.db_username', $1, false)`,
        creds.username
      )
      // Prisma will use new credentials on next connection
      await prisma.$disconnect()
      logger.info('Database credentials rotated')
    } catch (error) {
      logger.error({ error }, 'Failed to rotate database credentials')
    }
  }, 24 * 60 * 60 * 1000)
}
```

## Access Control Matrix

| Service | Can Read | Can Write | Via |
|---------|----------|-----------|-----|
| Call Service | agents:read, billing:read | calls:write | REST API |
| Agent Service | calls:read | agents:write | REST API |
| Voice Service | agents:read | voice:write | gRPC |
| AI Service | agents:read, calls:read, knowledge:read | ai:write | gRPC |
| Campaign Service | agents:read | calls:write, campaigns:write | REST API |
| Billing Service | subscriptions:read | billing:write | REST API |
| Auth Service | users:read, tenants:read | auth:write | REST API |
| Notification Service | — | notifications:write | BullMQ |

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Transport Security | mTLS (Istio) | Zero-trust, automatic certificate management |
| Application Auth | Short-lived JWT (5 min) | Limits blast radius of compromised token |
| Authorization | Scope-based (OAuth 2.0 style) | Fine-grained, auditable, standard |
| Secrets Management | HashiCorp Vault | Dynamic secrets, auto-rotation, audit |
| Network Isolation | Kubernetes NetworkPolicies | Defense in depth, default deny |

## Integration Points

- **Part 15 (Security)** — Overall security architecture
- **Part 10 (Security)** — Zero-trust model implementation
- **Part 23 (DevOps)** — Network policies and secret deployment
- **Part 05 (Microservices)** — Every service uses these auth patterns

## Production Considerations

- **Key Rotation**: Service signing keys rotated every 90 days; Vault handles automatically
- **Audit Trail**: All service auth attempts logged with identity, scope, timestamp
- **Failure Mode**: If auth service is down, cached JWTs still work for 5 minutes
- **Revocation**: Emergency revocation of all service tokens via Vault policy change
- **Compliance**: SOC 2 requires service-to-service authentication; mTLS + JWT satisfies this
- **Performance**: JWT verification adds ~1ms per request; negligible at scale
