# Section 05: Domain Mapping Storage

## Overview

Domain mapping storage maintains the relationship between custom domains, subdomains, and their owning tenants. This mapping is queried on every HTTP request to determine which tenant's environment should handle the request. Fast, reliable domain resolution is critical—every millisecond of DNS resolution and domain lookup latency directly impacts page load time and API response time.

The domain mapping system has two components: a database of record (PostgreSQL) for authoritative storage, and a cache layer (Redis) for sub-millisecond lookups. The database stores domain-to-tenant mappings with verification status, SSL certificate metadata, and timestamps. Redis caches active domain mappings with appropriate TTLs, invalidated when domain status changes.

For a voice agent platform supporting white-label and enterprise customers, the domain mapping must handle multiple domains per tenant, domain aliases, wildcard subdomains, redirect rules (www → non-www, HTTP → HTTPS), and domain-specific configuration overrides.

## Architecture

```
Domain Lookup Flow

[HTTP Request] → Host Header: "voiceagent.acmecorp.com"
    │
    ▼
[Reverse Proxy]
    │
    ├── Query Redis: domain:voiceagent.acmecorp.com
    │   ├── HIT → Return tenant_id → Route request
    │   └── MISS → Query PostgreSQL
    │               ├── FOUND → Cache in Redis (TTL: 300s)
    │               │           → Return tenant_id → Route request
    │               └── NOT FOUND → Return 404 / Default route
    │
    ▼
[Application] → X-Tenant-ID header set by proxy
```

## Design Decisions

**Decision 1: Redis as primary lookup cache.** Redis provides sub-millisecond lookups essential for high-throughput request routing. Use Redis hashes for efficient storage and expiration.

**Decision 2: Separate table for domain mappings.** Don't embed domain in the tenants table. Domains have their own lifecycle (verification, SSL, expiry) and a tenant may have multiple domains.

**Decision 3: Domain normalization on insert.** Store normalized (lowercase, no www prefix, IDN-encoded) domains. This prevents duplicate entries for "Example.com", "example.com", and "www.example.com".

## Implementation Approach

```typescript
interface DomainMapping {
  id: string;
  tenantId: string;
  domain: string;        // Normalized domain
  originalDomain: string; // As entered by user
  type: 'primary' | 'alias' | 'wildcard';
  status: 'pending' | 'active' | 'suspended' | 'expired';
  verificationToken: string;
  verifiedAt?: Date;
  sslCertArn?: string;
  sslExpiresAt?: Date;
  config?: {
    redirectWww: boolean;
    forceHttps: boolean;
    corsOrigins?: string[];
    customHeaders?: Record<string, string>;
  };
  createdAt: Date;
  updatedAt: Date;
}

class DomainMappingService {
  constructor(
    private pool: Pool,
    private redis: Redis,
    private eventBus: EventBus
  ) {}

  async resolveDomain(host: string): Promise<DomainResolution | null> {
    const normalized = this.normalizeDomain(host);

    // 1. Check Redis cache
    const cached = await this.redis.hgetall(`domain:${normalized}`);
    if (cached && cached.tenant_id) {
      return {
        tenantId: cached.tenant_id,
        config: cached.config ? JSON.parse(cached.config) : {},
      };
    }

    // 2. Check PostgreSQL
    const result = await this.pool.query(`
      SELECT tenant_id, config FROM custom_domains 
      WHERE domain = $1 AND status = 'active'
    `, [normalized]);

    if (result.rows.length > 0) {
      const mapping = result.rows[0];
      
      // 3. Cache in Redis
      await this.redis.hset(`domain:${normalized}`, {
        tenant_id: mapping.tenant_id,
        config: JSON.stringify(mapping.config || {}),
      });
      await this.redis.expire(`domain:${normalized}`, 300); // 5 min TTL

      return {
        tenantId: mapping.tenant_id,
        config: mapping.config || {},
      };
    }

    // 4. Check wildcard: *.customdomain.com
    const wildcardResult = await this.pool.query(`
      SELECT tenant_id, config FROM custom_domains 
      WHERE domain = $1 AND type = 'wildcard' AND status = 'active'
    `, [`*.${this.getDomainRoot(normalized)}`]);

    if (wildcardResult.rows.length > 0) {
      const mapping = wildcardResult.rows[0];
      const wildcardKey = `wildcard:${this.getDomainRoot(normalized)}`;
      
      await this.redis.hset(wildcardKey, {
        tenant_id: mapping.tenant_id,
        config: JSON.stringify(mapping.config || {}),
      });
      await this.redis.expire(wildcardKey, 300);

      return { tenantId: mapping.tenant_id, config: mapping.config || {} };
    }

    // 5. Not found
    return null;
  }

  async addDomainMapping(mapping: DomainMapping): Promise<void> {
    const normalized = this.normalizeDomain(mapping.domain);

    await this.pool.query(`
      INSERT INTO custom_domains (
        id, tenant_id, domain, original_domain, type, status,
        verification_token, config, created_at, updated_at
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, NOW(), NOW())
    `, [
      mapping.id, mapping.tenantId, normalized, mapping.originalDomain,
      mapping.type, mapping.status, mapping.verificationToken,
      JSON.stringify(mapping.config || {}),
    ]);

    // Invalidate cache for this domain
    await this.redis.del(`domain:${normalized}`);
    await this.redis.del(`wildcard:${this.getDomainRoot(normalized)}`);
  }

  async updateDomainStatus(
    domainId: string, 
    status: DomainMapping['status']
  ): Promise<void> {
    const result = await this.pool.query(`
      UPDATE custom_domains SET status = $1, updated_at = NOW()
      WHERE id = $2 RETURNING domain
    `, [status, domainId]);

    if (result.rows.length > 0) {
      // Invalidate cache
      const domain = result.rows[0].domain;
      await this.redis.del(`domain:${domain}`);
      
      // Notify proxy to update routing
      await this.eventBus.publish('domain.status_changed', {
        domain,
        status,
        timestamp: new Date(),
      });
    }
  }

  async getTenantDomains(tenantId: string): Promise<DomainMapping[]> {
    const result = await this.pool.query(
      'SELECT * FROM custom_domains WHERE tenant_id = $1 ORDER BY created_at DESC',
      [tenantId]
    );
    return result.rows;
  }

  async bulkCacheWarm(): Promise<number> {
    const activeDomains = await this.pool.query(`
      SELECT domain, tenant_id, config 
      FROM custom_domains 
      WHERE status = 'active'
    `);

    let cached = 0;
    for (const row of activeDomains.rows) {
      await this.redis.hset(`domain:${row.domain}`, {
        tenant_id: row.tenant_id,
        config: JSON.stringify(row.config || {}),
      });
      await this.redis.expire(`domain:${row.domain}`, 300);
      cached++;
    }

    return cached;
  }

  private normalizeDomain(host: string): string {
    // Remove port, lowercase, IDN encode
    let domain = host.split(':')[0].toLowerCase().trim();
    
    // Remove www. prefix for normalization
    domain = domain.replace(/^www\./, '');
    
    return domain;
  }

  private getDomainRoot(domain: string): string {
    // Extract root domain (example.com from sub.example.com)
    const parts = domain.split('.');
    if (parts.length >= 2) {
      return parts.slice(-2).join('.');
    }
    return domain;
  }
}
```

## Integration Points

- **Reverse Proxy (Sec 04):** The primary consumer of domain mapping data
- **Domain Verification (Sec 02):** Adds mappings when verification completes
- **DNS Configuration:** Domain mapping drives DNS record creation
- **Tenant Dashboard:** UI for managing domains
- **Analytics:** Domain resolution latency metrics

## Open-Source Tools

- **Redis** — Sub-millisecond key-value cache for domain lookups
- **node-ioredis** — Redis client with cluster and sentinel support
- **public-suffix-list** — Extract registrable domain names
- **punycode.js** — IDN encoding/decoding for internationalized domains
- **pg-cache** — Redis-backed PostgreSQL query cache

## Production Considerations

- **Cache Invalidation:** Domain status changes (verified, suspended, expired) must immediately invalidate the cache. Use Redis pub/sub or a cache version key for batch invalidation.
- **Cache Warm-up:** On deployment, warm the domain cache by loading all active domains into Redis. This prevents a cold-cache stampede where every first request hits PostgreSQL.
- **Domain Squatting Protection:** Prevent multiple tenants from verifying the same domain. Once a domain is verified, it's locked to that tenant. Domain transfer requires both parties' approval.
- **TTL Strategy:** Short TTL (5 minutes) for domain lookups balances cache freshness with database load. Set a shorter TTL during high-change periods (domain verification batches).
- **Wildcard Performance:** Wildcard domain lookups (`*.example.com`) require an extra database query. Consider pre-loading common wildcard domains into memory or a separate Redis set.
- **Purge on Tenant Deletion:** When a tenant is deleted, remove all domain mappings and invalidate caches. This prevents domain reuse by unauthorized parties.
- **Monitoring:** Track domain resolution latency (p50/p95/p99), cache hit rate, and cache size. Alert on cache hit rate dropping below 99%.
