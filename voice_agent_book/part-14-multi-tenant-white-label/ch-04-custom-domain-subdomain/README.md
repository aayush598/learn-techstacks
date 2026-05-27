# Chapter 04: Custom Domain & Subdomain Support

> **Part:** 14 - Multi-Tenant & White-Label

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Wildcard DNS Configuration](sec-01-wildcard-dns-configuration.md) | A/AAAA records, CNAME wildcard, DNS propagation, Cloudflare/DNS provider setup |
| 02 | [Custom Domain Verification](sec-02-custom-domain-verification.md) | DNS TXT record verification, CNAME verification, automated validation, status polling |
| 03 | [Let's Encrypt SSL Automation](sec-03-lets-encrypt-ssl.md) | ACME protocol, automated certificate issuance, renewal hooks, wildcard certificates |
| 04 | [Reverse Proxy Configuration](sec-04-reverse-proxy-config.md) | Caddy/Traefik/NGINX configuration, TLS termination, request routing by domain |
| 05 | [Domain Mapping Storage](sec-05-domain-mapping-storage.md) | Domain-to-tenant mapping schema, caching strategy, lookup performance, TTL management |
| 06 | [Multi-Region Domain Routing](sec-06-multi-region-routing.md) | Geo-aware DNS routing, region-specific domains, latency-based routing, failover |
| 07 | [Custom Domain Health Checks](sec-07-domain-health-checks.md) | SSL certificate expiry monitoring, DNS resolution checks, domain connectivity probes |
| 08 | [Domain Migration Strategy](sec-08-domain-migration-strategy.md) | Moving between domains, 301 redirects, SEO preservation, cutover planning |

---

## Domain Resolution Flow

```
User → custom.voiceagent.com (or customer-domain.com)
        ↓
    DNS Resolution → A/AAAA or CNAME
        ↓
    Reverse Proxy (Caddy/Traefik)
        ↓
    Domain Lookup → Cache → DB
        ↓
    Tenant Context Extracted
        ↓
    Application Routes to Tenant Environment
```

---

## Learning Objectives

- Configure wildcard DNS for subdomain-based tenant routing
- Implement custom domain verification with DNS record validation
- Automate Let's Encrypt SSL certificate lifecycle
- Configure reverse proxy for multi-tenant domain routing
- Design domain-to-tenant mapping with caching
- Implement multi-region DNS-based routing
- Build custom domain health monitoring
- Plan domain migration with minimal downtime
