# Section 04: Reverse Proxy Configuration

## Overview

The reverse proxy is the entry point for all HTTP(S) traffic to the platform, responsible for TLS termination, request routing, load balancing, and tenant identification. For a multi-tenant platform with custom domains and subdomains, the reverse proxy must dynamically route requests based on the Host header, mapping incoming domains to the correct tenant's application environment.

Caddy is the recommended reverse proxy for multi-tenant SaaS due to its automatic HTTPS, simple configuration, and dynamic routing capabilities. Caddy automatically provisions and renews Let's Encrypt certificates for both wildcard subdomains and custom domains, eliminating the need for separate SSL automation. Alternative options include NGINX (with Lua scripting for dynamic routing) and Traefik (with Docker/Kubernetes integration).

The proxy configuration includes: default wildcard routing for `*.voiceagent.com`, custom domain routing for verified tenant domains, SSL termination with automatic certificates, health checking for backend services, WebSocket support for real-time features, rate limiting per tenant, and access logging with tenant context.

## Architecture

```
Reverse Proxy Architecture

[Internet] → DNS → Cloudflare CDN
                    │
                    ▼
              [Caddy Reverse Proxy]
                    │
              TLS Termination
              Domain Routing
              Rate Limiting
              Access Logging
                    │
         ┌──────────┴──────────┐
         │                     │
   [Next.js App]         [WebSocket]
   (API + SSR)           (Real-time)
         │                     │
         └──────────┬──────────┘
                    ▼
              [Backend Services]
         (Agents, Calls, Analytics)
```

## Design Decisions

**Decision 1: Caddy over NGINX for dynamic routing.** Caddy's `handle_path` and `route` directives, combined with its JSON API for dynamic configuration, make it ideal for multi-tenant environments with frequent domain additions.

**Decision 2: Domain mapping via Redis/DB, not configuration files.** Store domain-to-tenant mappings in Redis (fast lookup) and database (source of truth). The proxy queries Redis for each request's routing target, avoiding configuration file reloads.

**Decision 3: Rate limiting at proxy level.** Implement per-tenant rate limiting at the reverse proxy layer using Redis-based token buckets. This protects backend services before requests reach application code.

## Implementation Approach

```
Caddyfile Configuration:

{
  # Global settings
  admin off
  ocsp_stapling on
  servers :443 {
    protocols h2 h1
  }
}

# Wildcard subdomain routing
*.voiceagent.com, voiceagent.com {
  tls {
    dns cloudflare {env.CLOUDFLARE_API_TOKEN}
  }
  
  # Route based on subdomain
  @tenant_subdomain {
    host *.voiceagent.com
  }
  
  handle @tenant_subdomain {
    # Extract tenant from subdomain
    vars @tenant {host.1}
    
    # Route to tenant's application
    reverse_proxy localhost:3000 {
      header_up X-Tenant-ID {vars.@tenant}
      header_up X-Forwarded-Host {host}
    }
  }
  
  # Health check endpoint (no routing)
  handle /health {
    respond 200 { "status": "ok" }
  }
  
  # Default route
  handle {
    reverse_proxy localhost:3000
  }
}

# Dynamic custom domain routing
# These are managed via Caddy's JSON API
# Example of a dynamically added domain:
# {
#   "domain": "voiceagent.acmecorp.com",
#   "tenant_id": "tenant_abc",
#   "upstream": "localhost:3000"
# }
```

Dynamic Configuration via API:

```typescript
class ReverseProxyManager {
  private caddyApi: string;

  async addCustomDomain(domain: string, tenantId: string): Promise<void> {
    const config = {
      match: [{ host: [domain] }],
      handle: [{
        handler: "reverse_proxy",
        upstreams: [{ dial: "localhost:3000" }],
        headers: {
          request: {
            set: {
              "X-Tenant-ID": [tenantId],
              "X-Forwarded-Host": ["{http.request.host}"],
            }
          }
        }
      }],
      terminal: true,
    };

    // Add route via Caddy's admin API
    await fetch(`${this.caddyApi}/config/apps/http/servers/srv0/routes/`, {
      method: 'POST',
      body: JSON.stringify(config),
    });
  }

  async removeCustomDomain(domain: string): Promise<void> {
    // Find and remove the route for this domain
    const routes = await this.getRoutes();
    const routeIndex = routes.findIndex(r => 
      r.match?.[0]?.host?.includes(domain)
    );
    
    if (routeIndex >= 0) {
      await fetch(
        `${this.caddyApi}/config/apps/http/servers/srv0/routes/${routeIndex}`,
        { method: 'DELETE' }
      );
    }
  }

  async addRateLimit(tenantId: string, rps: number): Promise<void> {
    await fetch(`${this.caddyApi}/config/apps/http/servers/srv0/routes/`, {
      method: 'POST',
      body: JSON.stringify({
        match: [{ header: { "X-Tenant-ID": [tenantId] } }],
        handle: [{
          handler: "rate_limit",
          rate: { rps, burst: rps * 2 },
          key: "{http.request.header.X-Tenant-ID}",
          storage: "redis",
        }],
      }),
    });
  }
}

// Alternative: Domain resolution middleware in application
class TenantDomainResolver {
  private domainCache: RedisCache;

  async resolveTenant(host: string): Promise<string | null> {
    // Check cache first
    const cached = await this.domainCache.get(`domain:${host}`);
    if (cached) return cached;

    // Check database
    const result = await this.pool.query(
      `SELECT tenant_id FROM custom_domains 
       WHERE domain = $1 AND status = 'active'`,
      [host]
    );

    if (result.rows.length > 0) {
      const tenantId = result.rows[0].tenant_id;
      await this.domainCache.setex(`domain:${host}`, 300, tenantId); // 5 min cache
      return tenantId;
    }

    // Check for wildcard subdomain: tenant.voiceagent.com
    const parts = host.split('.');
    if (parts.length >= 3 && host.endsWith('voiceagent.com')) {
      return parts[0]; // Subdomain is the tenant slug
    }

    return null;
  }
}
```

## Integration Points

- **Domain Verification (Sec 02):** Verified domains are added to proxy configuration
- **SSL Certificates (Sec 03):** Caddy auto-provisions from Let's Encrypt
- **Tenant Context (Ch 02 Sec 03):** X-Tenant-ID header drives tenant middleware
- **Rate Limiting (Ch 08):** Per-tenant rate limits enforced at proxy
- **WebSocket Support:** Real-time call events need WebSocket proxy upgrade

## Open-Source Tools

- **Caddy** — Go web server with automatic HTTPS and dynamic routing
- **NGINX + Lua** — Traditional reverse proxy with scripting for dynamic config
- **Traefik** — Cloud-native reverse proxy with Docker/K8s integration
- **HAProxy** — High-performance TCP/HTTP proxy
- **Vulcand** — Programmatic reverse proxy from Mailgun

## Production Considerations

- **Hot Reload Configuration:** Changing proxy configuration should not drop existing connections. Caddy's API allows live configuration changes without reloads. Test dynamic route changes in staging.
- **WebSocket Support:** Ensure WebSocket upgrade headers (Upgrade, Connection) are properly forwarded. Confiure read/write timeouts appropriate for long-lived voice connections.
- **TLS Termination Options:** Terminate TLS at the proxy (Caddy) for simplicity, or pass through to backend (NGINX) for end-to-end encryption. Caddy termination is sufficient for most deployments.
- **Health Checks:** Configure passive health checks for backend services. If a backend is unhealthy, the proxy should remove it from rotation. Active health checks (periodic pings) for critical services.
- **Request Logging:** Log all requests with tenant ID, status code, latency, and bytes transferred. Ship logs to centralized logging (ELK, Datadog) for analysis and troubleshooting.
- **Proxy Redundancy:** Run at least 2 proxy instances behind a load balancer. The proxy is a critical infrastructure component—single-instance deployments have availability risks.
- **Performance Tuning:** Connection pooling, keep-alive timeouts, buffer sizes, and worker counts should be tuned for your traffic patterns. Voice applications have different profiles (long-lived connections) compared to typical web apps.
