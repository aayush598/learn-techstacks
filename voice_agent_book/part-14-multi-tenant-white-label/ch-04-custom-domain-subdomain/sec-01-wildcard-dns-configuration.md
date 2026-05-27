# Section 01: Wildcard DNS Configuration

## Overview

Wildcard DNS is the foundation for subdomain-based multi-tenant routing, allowing each tenant to access the platform via `tenantname.voiceagent.com`. A wildcard DNS record (`*.voiceagent.com`) points all subdomains to the platform's load balancer, where the application extracts the tenant identifier from the subdomain and routes the request accordingly. This approach eliminates the need to create DNS records for each tenant individually.

Wildcard DNS configuration involves creating an A record (or CNAME) for `*.voiceagent.com` pointing to the platform's ingress IP or load balancer. The DNS provider must support wildcard records, which most modern providers do (Cloudflare, AWS Route53, Google Cloud DNS). DNS propagation typically takes 5-30 minutes for new records, though changes to existing records may propagate faster.

For production, use a CDN or reverse proxy (Cloudflare, Fastly) in front of the application to handle DNS resolution, DDoS protection, SSL termination, and caching. The CDN must support wildcard SSL certificates (either a wildcard cert for `*.voiceagent.com` or automated per-subdomain certs via Let's Encrypt).

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Audio    |--->| WebSocket|--->| Jitter   |--->| PLC      |--->| Player   |
| Producer |    | (WSS)    |    | Buffer   |    | (Packet  |    | (smooth  |
| (100ms   |    | (binary) |    | (adaptive|    |  Loss    |    |  output) |
|  chunks) |    |          |    |  60-200) |    |  Conceal)|    +----------+
+----------+    +----------+    +----------+    +----------+
```


## Design Decisions

**Decision 1: Wildcard A record vs individual CNAMEs.** Wildcard is simpler, cheaper, and faster for multi-tenant SaaS. Individual CNAMEs per tenant are needed only for custom domains (Ch 04, Sec 02).

**Decision 2: CDN in front of wildcard.** Always use a CDN (Cloudflare, Fastly) for wildcard DNS. The CDN provides DDoS protection, SSL termination, and caching that a bare DNS record would not.

**Decision 3: Root domain redirect.** Configure the root domain (voiceagent.com) to redirect to www.voiceagent.com or the marketing site. The wildcard should not match the root domain.

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **DNS Propagation:** Wildcard DNS changes can take 24-48 hours to fully propagate due to TTL caching. Set initial TTL low (60 seconds) when making changes, then increase to 300+ seconds once stable.
- **Wildcard SSL Certificate:** Ensure your SSL certificate covers `*.voiceagent.com`. Wildcard certificates from Let's Encrypt via DNS-01 challenge are free and auto-renewable.
- **Subdomain Collision Protection:** Reserve common subdomains (www, api, admin, app, mail, help, support, docs, status) to prevent tenants from registering them.
- **DNS Security:** Enable DNSSEC for your domain to prevent DNS spoofing. Configure CAA records to restrict which CAs can issue certificates for your domain.
- **Failover DNS:** Configure health checks on the wildcard record. If the primary load balancer fails, DNS failover should redirect traffic to a secondary region.
