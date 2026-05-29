# Section 07: API Security Headers

## Overview

Security headers protect the Voice Agent API users from common web vulnerabilities. The API Gateway sets strict security headers on all responses, covering CORS (Cross-Origin Resource Sharing), CSP (Content Security Policy), HSTS (HTTP Strict Transport Security), and content-type options. These headers defend against XSS, clickjacking, MIME-type sniffing, and protocol downgrade attacks.

## Architecture

```
Security Headers Applied
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Response Headers:
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Content-Security-Policy: default-src 'self'
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  X-XSS-Protection: 0
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=()
  Cache-Control: no-store
  X-Request-Id: req_abc_123

CORS Configuration (per environment):
  Production:
    Access-Control-Allow-Origin: https://app.voiceagent.com
    Access-Control-Allow-Methods: GET, POST, PATCH, DELETE
    Access-Control-Allow-Headers: Authorization, Content-Type, Idempotency-Key
    Access-Control-Max-Age: 86400

  Development:
    Access-Control-Allow-Origin: *
```

## Design Decisions

- **Strict Defaults**: Start with the most restrictive security headers and relax only when necessary
- **Environment-Specific CORS**: Production locks origins to known domains; development allows all for DX
- **Preflight Caching**: 24-hour preflight cache reduces OPTIONS request overhead
- **Security Headers at Gateway Level**: Headers set at the API Gateway, not individual services — consistent across all endpoints

## Implementation Approach

```typescript
// Security header configuration
interface SecurityHeadersConfig {
  environment: 'production' | 'staging' | 'development';
  allowedOrigins: string[];
  hstsMaxAge?: number; // seconds
  cspDirectives?: Record<string, string[]>;
}

class SecurityHeadersMiddleware {
  private config: SecurityHeadersConfig;

  constructor(config: SecurityHeadersConfig) {
    this.config = config;
  }

  apply(c: Context): void {
    // HSTS — force HTTPS
    c.header('Strict-Transport-Security',
      `max-age=${this.config.hstsMaxAge || 31536000}; includeSubDomains`);

    // Content Security Policy
    c.header('Content-Security-Policy', this.buildCsp());

    // MIME sniffing protection
    c.header('X-Content-Type-Options', 'nosniff');

    // Clickjacking protection
    c.header('X-Frame-Options', 'DENY');

    // Modern XSS protection (disable legacy XSS filter)
    c.header('X-XSS-Protection', '0');

    // Referrer policy
    c.header('Referrer-Policy', 'strict-origin-when-cross-origin');

    // Permissions policy — restrict sensitive APIs
    c.header('Permissions-Policy', 'geolocation=(), microphone=()');

    // Request ID for debugging
    c.header('X-Request-Id', c.get('requestId'));

    // CORS
    this.applyCors(c);
  }

  private buildCsp(): string {
    const defaultDirectives: Record<string, string[]> = {
      'default-src': ["'self'"],
      'script-src': ["'self'"],
      'style-src': ["'self'", "'unsafe-inline'"],
      'img-src': ["'self'", 'data:'],
      'connect-src': ["'self'"],
      'font-src': ["'self'"],
      'object-src': ["'none'"],
      'base-uri': ["'self'"],
      'form-action': ["'self'"],
    };

    const directives = { ...defaultDirectives, ...this.config.cspDirectives };

    return Object.entries(directives)
      .map(([key, values]) => `${key} ${values.join(' ')}`)
      .join('; ');
  }

  private applyCors(c: Context): void {
    const origin = c.req.header('Origin');

    if (this.config.environment === 'development') {
      c.header('Access-Control-Allow-Origin', '*');
    } else if (origin && this.config.allowedOrigins.includes(origin)) {
      c.header('Access-Control-Allow-Origin', origin);
      c.header('Vary', 'Origin');
    }

    if (c.req.method === 'OPTIONS') {
      c.header('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS');
      c.header('Access-Control-Allow-Headers',
        'Authorization, Content-Type, Idempotency-Key, X-Signature, X-Signature-Timestamp');
      c.header('Access-Control-Expose-Headers',
        'X-Request-Id, X-RateLimit-*, Retry-After');
      c.header('Access-Control-Max-Age', '86400');
      c.status(204);
      return;
    }
  }
}

// Usage in Hono
const securityHeaders = new SecurityHeadersMiddleware({
  environment: 'production',
  allowedOrigins: [
    'https://app.voiceagent.com',
    'https://dashboard.voiceagent.com',
  ],
});

app.use('*', async (c, next) => {
  securityHeaders.apply(c);
  await next();
});
```

## Integration Points

- **API Gateway**: Security headers set at gateway level before routing
- **CDN/Proxy**: CloudFront/Cloudflare may add additional security headers
- **Browser SDK**: CORS configuration enables browser SDK to make cross-origin requests

## Production Considerations

- **CORS Preflight Overhead**: 24-hour cache reduces OPTIONS requests but requires origin change coordination
- **CSP Reporting**: Use `report-uri` or `report-to` directive with a reporting endpoint for CSP violation monitoring
- **HSTS Preload**: Submit domain to browser HSTS preload list for protection before first request
- **Certificate Transparency**: Expect-CT header enforces certificate transparency requirements

## Open-Source Tools

- **Helmet.js**: Reference implementation for security headers in Express/Node.js
- **Hono**: Security header middleware compatible with Edge runtimes
