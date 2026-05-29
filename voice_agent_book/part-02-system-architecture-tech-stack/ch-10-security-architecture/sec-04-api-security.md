# Section 04: API Security

## API Security Controls

Every API request passes through multiple security layers: **TLS 1.3** for transport security, **request signing** for authenticity, **CSRF protection** for browser requests, and **input validation** for injection prevention. The Web Application Firewall (WAF) provides additional protection against common attacks.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    API SECURITY LAYERS                              │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Layer 1: Transport Security (TLS 1.3)                      │   │
│  │  ┌────────────────────────────────────────────────────────┐  │   │
│  │  │  • TLS 1.3 only — no TLS 1.2 fallback                  │  │   │
│  │  │  • Cipher suites: TLS_AES_128_GCM_SHA256 (preferred)   │  │   │
│  │  │  • HSTS: max-age=31536000; includeSubDomains; preload  │  │   │
│  │  │  • Certificate: ECDSA P-256, auto-renewed via ACME     │  │   │
│  │  └────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Layer 2: Authentication                                    │   │
│  │  ┌────────────────────────────────────────────────────────┐  │   │
│  │  │  API Key (machine): SHA-256 hash in Redis              │  │   │
│  │  │  JWT (user): Signed with ES256, validated at gateway   │  │   │
│  │  │  Session (browser): HTTP-only, SameSite=Lax cookie     │  │   │
│  │  │  WebSocket: Token in query param, validated on connect │  │   │
│  │  └────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Layer 3: Authorization                                     │   │
│  │  ┌────────────────────────────────────────────────────────┐  │   │
│  │  │  • Scopes checked for every endpoint                   │  │   │
│  │  │  • Row-Level Security (RLS) for tenant isolation       │  │   │
│  │  │  • Rate limiting per API key / IP / user               │  │   │
│  │  │  • Idempotency key for safe retries                   │  │   │
│  │  └────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Layer 4: Input Validation & Injection Prevention            │   │
│  │  ┌────────────────────────────────────────────────────────┐  │   │
│  │  │  • Zod schema validation for all request bodies        │  │   │
│  │  │  • SQL injection: parameterized queries (Prisma)       │  │   │
│  │  │  • XSS: React auto-escaping + Content-Security-Policy  │  │   │
│  │  │  • Path traversal: normalised paths, reject '..'       │  │   │
│  │  │  • No eval(): disabled via CSP + runtime checks        │  │   │
│  │  └────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Layer 5: WAF (Web Application Firewall)                    │   │
│  │  ┌────────────────────────────────────────────────────────┐  │   │
│  │  │  • ModSecurity / Coraza with OWASP CRS ruleset         │  │   │
│  │  │  • Rate limiting: 1000 req/min per IP (edge)           │  │   │
│  │  │  • Request body limit: 1MB                              │  │   │
│  │  │  • Block: SQL injection patterns, XSS, path traversal  │  │   │
│  │  └────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Request Signing

```typescript
// HMAC request signing for sensitive webhook payloads
interface SignedRequest {
  method: string;
  path: string;
  timestamp: string;        // ISO 8601, must be within 5 minutes
  body: string;              // Raw JSON body
  signature: string;         // HMAC-SHA256 of method + path + timestamp + body
}

function signRequest(payload: SignedRequestPayload, secret: string): string {
  const message = [
    payload.method.toUpperCase(),
    payload.path,
    payload.timestamp,
    payload.body,
  ].join('\n');

  return crypto.createHmac('sha256', secret).update(message).digest('hex');
}

function verifySignature(request: NextRequest, secret: string): boolean {
  const timestamp = request.headers.get('X-Timestamp');
  const signature = request.headers.get('X-Signature');

  if (!timestamp || !signature) return false;

  // Reject requests older than 5 minutes
  const age = Date.now() - new Date(timestamp).getTime();
  if (age > 5 * 60 * 1000) return false;

  const expectedSig = signRequest({
    method: request.method,
    path: request.nextUrl.pathname,
    timestamp,
    body: JSON.stringify(request.body),
  }, secret);

  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expectedSig)
  );
}
```

## CSRF Protection

```typescript
// Double-submit cookie pattern
function csrfProtection(request: NextRequest): boolean {
  // For state-changing requests (POST, PUT, DELETE, PATCH)
  if (['POST', 'PUT', 'DELETE', 'PATCH'].includes(request.method)) {
    const csrfCookie = request.cookies.get('csrf-token')?.value;
    const csrfHeader = request.headers.get('X-CSRF-Token');

    if (!csrfCookie || !csrfHeader) return false;
    if (csrfCookie !== csrfHeader) return false;
  }

  return true;
}

// CSRF token generation
function generateCsrfToken(): string {
  return crypto.randomBytes(32).toString('hex');
}

// Set CSRF cookie on login
function setCsrfCookie(response: NextResponse): void {
  const token = generateCsrfToken();
  response.cookies.set('csrf-token', token, {
    httpOnly: true,
    sameSite: 'lax',
    secure: true,
    path: '/',
  });
}
```

## Content Security Policy

```typescript
// Strict CSP headers
const CSP_HEADERS = {
  'Content-Security-Policy': [
    "default-src 'self'",
    "script-src 'self' 'strict-dynamic' 'nonce-{nonce}'",
    "style-src 'self' 'unsafe-inline'",    // Required for Tailwind
    "img-src 'self' https://cdn.voiceagent.dev data: blob:",
    "font-src 'self' https://fonts.googleapis.com",
    "connect-src 'self' wss://api.voiceagent.dev https://api.openai.com",
    "frame-ancestors 'none'",
    "form-action 'self'",
    "base-uri 'self'",
    "object-src 'none'",
    "upgrade-insecure-requests",
  ].join('; '),
  'X-Content-Type-Options': 'nosniff',
  'X-Frame-Options': 'DENY',
  'X-XSS-Protection': '0',               // Deprecated, CSP handles this
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
};

function applySecurityHeaders(response: NextResponse): void {
  for (const [key, value] of Object.entries(CSP_HEADERS)) {
    response.headers.set(key, key.includes('nonce')
      ? value.replace('{nonce}', generateNonce())
      : value
    );
  }
}
```

## SQL Injection Prevention

```typescript
// Prisma uses parameterized queries by default — no raw SQL in application code
// Example: Safe query
const agent = await prisma.agent.findMany({
  where: {
    tenantId: user.tenantId,  // Parameterized
    name: { contains: userInput }, // Still parameterized
  },
});

// Raw SQL is strongly discouraged; if necessary, use tagged template
// import { sql } from '@vercel/postgres';
// const result = await sql`SELECT * FROM agents WHERE id = ${agentId}`;
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| TLS version | TLS 1.3 only | Faster handshake, stronger crypto, no legacy |
| CSRF protection | Double-submit cookie pattern | Stateless, no server-side token storage |
| Injection prevention | Prisma ORM (parameterized queries) | Type-safe, no raw SQL in application code |
| XSS prevention | React auto-escaping + CSP | Defense in depth — framework + browser |
| Request signing | HMAC-SHA256 | Simple, fast, supported everywhere |

## Integration Points

- **Ch 10 (Zero-Trust)** — API auth builds on zero-trust principles
- **Ch 07 (API Gateway)** — Security middleware in gateway pipeline
- **Ch 10 (Network Security)** — WAF at network perimeter
- **Ch 07 (Rate Limiting)** — Rate limiting as API security layer

## Production Considerations

- **TLS Certificate Management**: Auto-renewed via cert-manager + Let's Encrypt; 30-day expiry
- **Security Headers**: HSTS preload submitted for voiceagent.dev domain
- **API Key Compromise**: Key revocation in real-time via Redis; affected tenant notified
- **Penetration Testing**: Quarterly third-party pen tests; annual red team exercise
- **Bug Bounty**: Public program via HackerOne; $500-$5000 per valid finding
