# Section 01: Zero-Trust Security Model

## Zero-Trust Principles

The platform follows a **zero-trust security model**: never trust, always verify. Every request is authenticated and authorized regardless of origin (internal or external), with micro-perimeters around each service, least-privilege access, and continuous validation.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ZERO-TRUST SECURITY MODEL                        │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Traditional (Perimeter-Based)         Zero-Trust           │   │
│  │                                                              │   │
│  │  ┌──────────────────────┐    ┌──┐ ┌──┐ ┌──┐ ┌──┐ ┌──┐     │   │
│  │  │     Corporate         │    │  │ │  │ │  │ │  │ │  │     │   │
│  │  │     Network           │    │S1│ │S2│ │S3│ │S4│ │S5│     │   │
│  │  │                       │    └──┘ └──┘ └──┘ └──┘ └──┘     │   │
│  │  │  ┌──┐ ┌──┐ ┌──┐      │     │   │    │    │   │         │   │
│  │  │  │S1│ │S2│ │S3│      │     └───┴────┴────┴───┘          │   │
│  │  │  └──┘ └──┘ └──┘      │      mTLS between every pair     │   │
│  │  └──────────────────────┘    Every request: AuthN + AuthZ   │   │
│  │      🔓 Trusted inside       No implicit trust              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  ZERO-TRUST CONTROLS                                         │   │
│  │                                                              │   │
│  │  1. Verify every request                                     │   │
│  │     ┌────────────────────────────────────────────────────┐   │   │
│  │     │  External: API Key / JWT + Scope check             │   │   │
│  │     │  Internal: mTLS certificate + JWT + Scope check    │   │   │
│  │     └────────────────────────────────────────────────────┘   │   │
│  │                                                              │   │
│  │  2. Micro-perimeters per service                            │   │
│  │     ┌────────────────────────────────────────────────────┐   │   │
│  │     │  Service A can ONLY talk to Service B on port 443  │   │   │
│  │     │  NetworkPolicy: allow from agent-service to        │   │   │
│  │     │    call-service on tcp/443                         │   │   │
│  │     └────────────────────────────────────────────────────┘   │   │
│  │                                                              │   │
│  │  3. Least privilege                                         │   │
│  │     ┌────────────────────────────────────────────────────┐   │   │
│  │     │  Service A has scope: calls:read, calls:write      │   │   │
│  │     │  Service A does NOT have scope: billing:admin      │   │   │
│  │     └────────────────────────────────────────────────────┘   │   │
│  │                                                              │   │
│  │  4. Continuous validation                                   │   │
│  │     ┌────────────────────────────────────────────────────┐   │   │
│  │     │  Certificate rotation: every 24h                   │   │   │
│  │     │  Token expiry: 15 minutes (JWT)                    │   │   │
│  │     │  Session validation: every request                 │   │   │
│  │     └────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## mTLS Implementation

```typescript
// mTLS configuration for inter-service communication
import * as fs from 'fs';
import * as tls from 'tls';

interface mTLSConfig {
  ca: string;           // CA certificate for verification
  cert: string;         // Service certificate
  key: string;          // Service private key
  requireClientCert: boolean; // Enforce client certificate
}

// Loaded from Vault, not filesystem
const mtlsConfig: mTLSConfig = {
  ca: await vault.read('secret/mtls/ca-cert'),
  cert: await vault.read(`secret/mtls/services/${serviceName}/cert`),
  key: await vault.read(`secret/mtls/services/${serviceName}/key`),
  requireClientCert: true,
};

// HTTP client with mTLS
async function createSecureClient(): Promise<typeof fetch> {
  const agent = new tls.TLSSocket({
    ca: [mtlsConfig.ca],
    cert: mtlsConfig.cert,
    key: mtlsConfig.key,
    rejectUnauthorized: true,
    checkServerIdentity: (hostname, cert) => {
      // Verify service identity matches expected name
      if (!cert.subject.CN?.startsWith('svc-')) {
        return new Error('Invalid service certificate');
      }
      return undefined;
    },
  });

  return (url: string, options?: RequestInit) =>
    fetch(url, { ...options, agent });
}
```

## Network Policies (Kubernetes)

```yaml
# Kubernetes NetworkPolicy — micro-perimeter for call-service
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: call-service-policy
spec:
  podSelector:
    matchLabels:
      app: call-service
  policyTypes:
    - Ingress
    - Egress
  ingress:
    # Allow only API gateway ingress
    - from:
        - podSelector:
            matchLabels:
              app: api-gateway
      ports:
        - port: 3000
          protocol: TCP
    # Allow health checks from kubelet
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: kube-system
      ports:
        - port: 8080
          protocol: TCP
  egress:
    # Allow only to PostgreSQL
    - to:
        - podSelector:
            matchLabels:
              app: postgres
      ports:
        - port: 5432
          protocol: TCP
    # Allow to Redis
    - to:
        - podSelector:
            matchLabels:
              app: redis
      ports:
        - port: 6379
          protocol: TCP
    # Allow to Kafka
    - to:
        - podSelector:
            matchLabels:
              app: kafka
      ports:
        - port: 9092
          protocol: TCP
    # Allow DNS resolution
    - to:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: kube-system
      ports:
        - port: 53
          protocol: UDP
```

## Service Identity and Access

```typescript
// Service-to-service JWT
interface ServiceToken {
  sub: string;           // Service name: 'call-service'
  aud: string;           // Target service: 'billing-service'
  exp: number;           // Expiry: 15 minutes
  iat: number;
  jti: string;           // Unique token ID
  scopes: string[];      // ['billing:meter:write']
}

async function generateServiceToken(targetService: string, scopes: string[]): Promise<string> {
  const signingKey = await vault.read(`secret/jwt/service-${serviceName}-key`);

  return new SignJWT({
    sub: serviceName,
    aud: targetService,
    scopes,
  })
    .setProtectedHeader({ alg: 'ES256' })
    .setExpirationTime('15m')
    .setIssuedAt()
    .sign(signingKey);
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Identity model | SPIFFE-inspired (service identity via mTLS certs) | Industry standard for zero-trust |
| Service auth | mTLS + JWT | mTLS for transport, JWT for scoped authorization |
| Certificate rotation | 24-hour auto-rotation via cert-manager | Short-lived certs limit blast radius |
| Network segmentation | Kubernetes NetworkPolicies | Declarative, auditable, per-service rules |
| Session lifetime | 15 minutes (JWT), 24 hours (web session) | Balance between security and UX |

## Integration Points

- **Ch 10 (Network Security)** — Network policies implement micro-perimeters
- **Ch 10 (API Security)** — API request verification builds on zero-trust
- **Ch 10 (Secrets Management)** — Certificates and keys stored in Vault
- **Ch 05 (Service Mesh)** — Istio/Linkerd can provide mTLS at mesh level

## Production Considerations

- **Performance Impact**: mTLS handshake adds ~5ms to first request; reused connections have no overhead
- **Certificate Management**: cert-manager with Let's Encrypt for external certs; internal CA for mTLS
- **Audit**: All access attempts (allowed and denied) logged to ClickHouse for security analysis
- **Revocation**: Compromised certificate revoked via CRL; service has 60-second CRL cache
- **Break Glass**: Emergency access procedure documented; requires 2-person approval and full audit trail
