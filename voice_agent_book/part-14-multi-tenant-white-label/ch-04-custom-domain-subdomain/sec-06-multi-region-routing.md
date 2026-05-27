# Section 06: Multi-Region Domain Routing

## Overview

Multi-region domain routing directs user traffic to the geographically closest or most appropriate data center region. For a globally distributed voice agent platform, latency to the nearest region directly impacts the quality of real-time voice conversations. Multi-region routing ensures that a tenant's users and voice agents connect to the region with the lowest latency, improving call quality and user experience.

The routing strategy uses DNS-based global load balancing (GSLB) with health-checked endpoints in each region. When a user resolves a custom domain or subdomain, the DNS responds with the IP address of the nearest healthy region. Application-level routing within regions is handled by the reverse proxy. For advanced scenarios, latency-based routing (AWS Route53 latency records) directs traffic to the region with the lowest current latency.

For a voice agent platform, multi-region routing must also account for data residency requirements (Part 15, Ch 10). A tenant may require their data to stay within a specific region (EU for GDPR). In this case, routing must always direct that tenant's traffic to the EU region, regardless of geographic proximity.

## Architecture

```
Global DNS Routing

┌─────────────┐
│  User in    │
│  London, UK │
└──────┬──────┘
       │
       ▼
┌──────────────────────┐
│ Google DNS / ISP DNS  │
└──────┬───────────────┘
       │
       ▼
┌─────────────────────────────────────────────┐
│ Route53 Latency-Based / Geo-DNS              │
│                                              │
│  voiceagent.acmecorp.com →                   │
│    eu-west-1: 12ms (selected)                │
│    us-east-1: 78ms                           │
│    ap-southeast-1: 250ms                     │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌──────────────────────────────┐
│ eu-west-1 (Frankfurt)        │
│                              │
│ ┌──────────────────────────┐ │
│ │ CDN / WAF / Reverse Proxy│ │
│ └──────────┬───────────────┘ │
│            ▼                 │
│ ┌──────────────────────────┐ │
│ │ Application Services     │ │
│ │ Tenant data in EU region │ │
│ └──────────────────────────┘ │
└──────────────────────────────┘
```

## Design Decisions

**Decision 1: DNS-based routing for simplicity and reliability.** DNS routing doesn't require changes to application code. It operates at the infrastructure level and is supported by all DNS providers.

**Decision 2: Latency-based routing as default, geo-based for compliance.** Use latency records for performance optimization. Override with geo-based records for tenants with data residency requirements.

**Decision 3: Tenant-level region preference stored in tenant config.** Each tenant has a `preferred_region` setting. The DNS routing layer checks this setting and directs traffic accordingly.

## Implementation Approach

```typescript
interface TenantRegionConfig {
  tenantId: string;
  preferredRegion?: string;   // For data residency
  allowedRegions: string[];   // Compliant regions
  routingPolicy: 'latency' | 'geo' | 'failover';
}

class MultiRegionRouter {
  private dnsProvider: DnsProvider;
  private healthChecker: HealthChecker;
  private regions: RegionConfig[];

  async configureTenantRouting(tenantId: string): Promise<void> {
    const tenant = await this.getTenantRegionConfig(tenantId);
    const domains = await this.getTenantDomains(tenantId);

    for (const domain of domains) {
      const routingConfig = this.buildRoutingConfig(tenant, domain);
      
      // Configure DNS records for each region
      for (const region of this.regions) {
        if (tenant.allowedRegions.includes(region.id)) {
          await this.dnsProvider.upsertRecord({
            zoneId: this.getHostedZoneId(domain.domain),
            name: domain.domain,
            type: 'A',
            setIdentifier: region.id,
            value: region.loadBalancerIp,
            routing: this.getRoutingPolicy(tenant.routingPolicy),
            healthCheckId: region.healthCheckId,
          });
        }
      }
    }
  }

  private buildRoutingConfig(
    tenant: TenantRegionConfig, 
    domain: DomainMapping
  ): RoutingConfig {
    // If tenant has a preferred region, route all traffic there
    if (tenant.preferredRegion) {
      return {
        type: 'latency',
        regions: [tenant.preferredRegion],
        fallback: tenant.allowedRegions.filter(r => r !== tenant.preferredRegion),
      };
    }

    // Default: route to lowest-latency region within allowed list
    return {
      type: 'latency',
      regions: tenant.allowedRegions,
      fallback: tenant.allowedRegions,
    };
  }

  private getRoutingPolicy(type: string): string {
    switch (type) {
      case 'geo': return 'geoproximity';
      case 'failover': return 'failover';
      default: return 'latency';
    }
  }

  async getNearestHealthyRegion(tenantId: string, userLatency: Map<string, number>): Promise<string> {
    const config = await this.getTenantRegionConfig(tenantId);
    const healthyRegions = await this.healthChecker.getHealthyRegions();
    
    // Filter to allowed and healthy
    const candidates = config.allowedRegions
      .filter(r => healthyRegions.includes(r) && userLatency.has(r));

    if (candidates.length === 0) {
      // Fallback to any healthy region
      return healthyRegions[0];
    }

    // Return region with lowest latency
    candidates.sort((a, b) => userLatency.get(a)! - userLatency.get(b)!);
    return candidates[0];
  }

  async handleRegionFailover(tenantId: string, failedRegion: string): Promise<void> {
    const tenant = await this.getTenantRegionConfig(tenantId);
    const healthRegion = tenant.allowedRegions.find(r => r !== failedRegion);
    
    if (!healthRegion) {
      await this.alertService.send({
        type: 'no_healthy_region',
        tenantId,
        severity: 'critical',
      });
      return;
    }

    // Update DNS to route to healthy region
    // Route53 health checks will automatically failover
    // But we also trigger explicit update for faster recovery
    await this.configureTenantRouting(tenantId);

    // Log failover event
    await this.auditService.log('region.failover', {
      tenantId,
      from: failedRegion,
      to: healthRegion,
      timestamp: new Date(),
    });
  }

  async measureLatency(tenantId: string): Promise<Map<string, number>> {
    const regions = this.regions.map(r => r.id);
    const measurement = new Map<string, number>();

    // Deploy latency measurement endpoints in each region
    const startTime = Date.now();
    const promises = regions.map(async (region) => {
      const response = await fetch(`https://${region}.health.voiceagent.com/ping`, {
        timeout: 5000,
        method: 'HEAD',
      });
      return { region, latency: Date.now() - startTime };
    });

    const results = await Promise.race([
      Promise.allSettled(promises),
      new Promise(resolve => setTimeout(resolve, 5000)),
    ]);

    if (Array.isArray(results)) {
      for (const result of results) {
        if (result.status === 'fulfilled') {
          measurement.set(result.value.region, result.value.latency);
        }
      }
    }

    return measurement;
  }
}

// Route53 configuration example
// AWS CDK / Terraform for infrastructure-as-code
const route53Config = {
  hostedZoneId: "ZONE123",
  recordName: "voiceagent.acmecorp.com",
  type: "A",
  routingPolicy: "latency",
  records: [
    {
      region: "eu-west-1",
      value: "203.0.113.10",  // EU load balancer
      healthCheck: "hc-eu",
      setIdentifier: "eu-west-1",
    },
    {
      region: "us-east-1",
      value: "203.0.113.20",  // US load balancer
      healthCheck: "hc-us",
      setIdentifier: "us-east-1",
    },
  ],
  failover: "PRIMARY",  // Active-active with health check failover
};
```

## Integration Points

- **Data Residency (Part 15 Ch 10):** Tenant region preferences drive routing decisions
- **Reverse Proxy (Sec 04):** Region-specific proxy instances
- **Health Checking:** Region health determines routing eligibility
- **Tenant Dashboard:** Users can see their assigned region
- **Compliance (Part 15):** Geo-routing enforces data localization

## Open-Source Tools

- **AWS Route53** — Global DNS with latency, geo, and failover routing
- **Google Cloud DNS** — Geo-routing with health checks
- **Azure Traffic Manager** — DNS-based traffic routing
- **OctoDNS** — Infrastructure-as-code for multi-provider DNS
- **DnsControl** — DNS configuration management tool

## Production Considerations

- **DNS TTL and Failover:** DNS-based routing has inherent failover latency (TTL-dependent). For faster failover, use anycast IP (Cloudflare, Fastly) which routes at the network level independent of DNS TTL.
- **Cross-Region Data Sync:** When routing to the nearest region, ensure the user's data is available there. Use cross-region database replication and global object storage.
- **Session Persistence:** A user may switch regions during a session if DNS changes or if they move geographically. WebSocket connections are particularly sensitive to region changes—maintain sticky sessions.
- **Health Check Granularity:** Health checks should verify not just server availability but also application health (API response, database connectivity, third-party service availability).
- **Cost Implications:** Multi-region deployment doubles/triples infrastructure costs. Only deploy to regions where you have sufficient traffic or compliance requirements.
- **Compliance Override:** Tenants with data residency requirements must always be routed to their designated region, even if latency is higher. Implement hard enforcement at the proxy level.
- **Monitoring:** Track per-region traffic distribution, latency, error rates, and failover events. Set up dashboards showing global traffic patterns.
