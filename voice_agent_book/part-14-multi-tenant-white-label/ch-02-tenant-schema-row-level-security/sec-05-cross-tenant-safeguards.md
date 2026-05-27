# Section 05: Cross-Tenant Query Safeguards

## Overview

Cross-tenant data leakage is the most critical security risk in multi-tenant SaaS applications. While RLS provides database-level protection, it must be complemented by application-layer safeguards, monitoring, and detective controls. Defense-in-depth means that even if RLS is misconfigured, an application bug bypasses tenant filtering, or a SQL injection vulnerability is exploited, additional layers of protection prevent or detect cross-tenant data access.

Cross-tenant query safeguards span multiple layers: query interceptors that validate tenant_id in all queries, SQL linters that catch missing tenant filters, penetration testing automation, anomaly detection on query patterns, and immutable audit logs that record all data access. For a voice agent platform handling sensitive call recordings and transcripts, cross-tenant safeguards are both a security requirement and a compliance necessity (SOC 2, HIPAA, GDPR all require demonstrated data isolation).

The most common cross-tenant vulnerability is not a direct query without tenant_id filter, but a more subtle bug: using the wrong tenant context (e.g., processing a webhook that doesn't include tenant context), caching that serves one tenant's data to another, or batch jobs that iterate over all tenants but skip context initialization for some operations.

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

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```typescript
// 1. Query Interceptor
class QueryInterceptor {
  private blockedQueries: RegExp[] = [
    /SELECT.*FROM\s+(calls|transcripts|agents)\s+WHERE\s+(?!.*tenant_id)/i,
    /UPDATE\s+(calls|transcripts|agents)\s+SET(?!.*WHERE.*tenant_id)/i,
    /DELETE\s+FROM\s+(calls|transcripts|agents)(?!.*WHERE.*tenant_id)/i,
  ];

  intercept(query: string, params: any[]): void {
    const context = getTenantContext();
    
    // 1. Check that tenant context exists
    if (!context?.tenantId) {
      throw new TenantContextError('No tenant context available');
    }

    // 2. Check for cross-tenant patterns
    if (this.detectCrossTenantQuery(query, params, context.tenantId)) {
      this.alertService.send({
        type: 'cross_tenant_query_detected',
        severity: 'critical',
        query,
        params,
        context,
      });
      throw new CrossTenantQueryError('Query detected as potential cross-tenant access');
    }

    // 3. Auto-inject tenant_id if missing (for ORM-generated queries)
    if (this.shouldInjectTenantId(query)) {
      query = this.injectTenantFilter(query, context.tenantId);
    }

    return { query, params };
  }

  private detectCrossTenantQuery(query: string, params: any[], currentTenant: string): boolean {
    // Detect if query explicitly references a different tenant_id
    const tenantRefMatch = query.match(/tenant_id\s*=\s*['"]?([^'"]+)['"]?/);
    if (tenantRefMatch && tenantRefMatch[1] !== currentTenant) {
      return true;
    }
    
    // Detect missing tenant filter on critical tables
    for (const pattern of this.blockedQueries) {
      if (pattern.test(query)) {
        return true;
      }
    }
    
    return false;
  }

  private shouldInjectTenantId(query: string): boolean {
    const tenantTables = ['calls', 'transcripts', 'agents', 'campaigns', 'recordings'];
    return tenantTables.some(table => 
      query.includes(`FROM ${table}`) || query.includes(`JOIN ${table}`)
    ) && !query.includes('tenant_id');
  }

  private injectTenantFilter(query: string, tenantId: string): string {
    // Add AND tenant_id = '...' to WHERE clause
    const whereIndex = query.toUpperCase().indexOf('WHERE');
    if (whereIndex === -1) {
      return query.replace(
        /(FROM\s+\w+)(?!.*WHERE)/i,
        `$1 WHERE tenant_id = '${tenantId}'`
      );
    }
    return query.replace(
      /(WHERE[^GROUP|ORDER|LIMIT]*)(?=\s*(GROUP|ORDER|LIMIT|;|$))/i,
      `$1 AND tenant_id = '${tenantId}'`
    );
  }
}

// 2. Database proxy with automatic tenant injection
class TenantAwareDBProxy {
  private interceptor: QueryInterceptor;

  async query(query: string, params?: any[]): Promise<QueryResult> {
    const { query: safeQuery, params: safeParams } = this.interceptor.intercept(query, params);
    return this.pool.query(safeQuery, safeParams);
  }
}

// 3. Tenant-aware cache service
class TenantAwareCache {
  constructor(private redis: Redis) {}

  private tenantKey(key: string): string {
    const tenantId = getTenantId();
    return `tenant:${tenantId}:${key}`;
  }

  async get<T>(key: string): Promise<T | null> {
    return this.redis.get(this.tenantKey(key));
  }

  async set(key: string, value: any, ttl?: number): Promise<void> {
    if (ttl) {
      await this.redis.setex(this.tenantKey(key), ttl, JSON.stringify(value));
    } else {
      await this.redis.set(this.tenantKey(key), JSON.stringify(value));
    }
  }

  async del(key: string): Promise<void> {
    await this.redis.del(this.tenantKey(key));
  }
}

// 4. Automated penetration test
class CrossTenantPenTest {
  async runTest(): Promise<PenTestResult> {
    const results: TestResult[] = [];

    // Test 1: Direct query without tenant filter
    results.push(await this.testQuery(
      'SELECT * FROM calls LIMIT 1',
      'Should fail: no tenant filter'
    ));

    // Test 2: Query with wrong tenant_id
    results.push(await this.testQuery(
      `SELECT * FROM calls WHERE tenant_id = '${this.otherTenantId}' LIMIT 1`,
      'Should return empty: RLS blocks cross-tenant'
    ));

    // Test 3: SQL injection attempt
    results.push(await this.testQuery(
      `SELECT * FROM calls WHERE tenant_id = '${this.myTenantId}' OR '1'='1'`,
      'Should fail: query interceptor blocks'
    ));

    // Test 4: Cross-tenant via JOIN
    results.push(await this.testQuery(
      `SELECT * FROM calls c JOIN transcripts t ON c.id = t.call_id WHERE t.tenant_id = '${this.otherTenantId}'`,
      'Should fail: RLS on both tables'
    ));

    // Test 5: Cache poisoning
    const cacheResult = await this.testCachePoisoning();
    results.push(cacheResult);

    return {
      timestamp: new Date().toISOString(),
      passed: results.filter(r => r.passed).length,
      failed: results.filter(r => !r.passed).length,
      results,
    };
  }
}
```

## Integration Points

- **CI/CD Pipeline:** Cross-tenant pen tests run on every deployment
- **Audit Logging:** All cross-tenant violation attempts are logged immutably
- **Alerting:** Real-time alerts for confirmed cross-tenant access attempts
- **ORM Layer:** Prisma/TypeORM middleware that enforces tenant filtering
- **API Gateway:** WAF rules that detect and block cross-tenant access patterns

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **False Positives:** Cross-tenant detection must handle legitimate cross-tenant operations (admin analytics, reseller visibility). Maintain an allowlist for approved cross-tenant queries.
- **Performance Impact:** Query interception adds latency (typically <1ms). Use sampling for detection in production—test every query in staging, sample in production.
- **Incident Response:** When cross-tenant access is detected, immediately invalidate the session, log full details, and notify security team. Have a documented incident response procedure for confirmed data breaches.
- **Pen Test Cadence:** Run cross-tenant penetration tests daily. New code deploys should not ship without passing cross-tenant isolation tests.
- **Compliance Evidence:** Cross-tenant safeguard logs serve as evidence for SOC 2, HIPAA, and GDPR audits. Ensure logs are immutable and have appropriate retention.
- **ORM-Level Filtering:** For teams using Prisma or TypeORM, implement global middleware that appends tenant_id to every query. This is the first line of defense.
- **Third-Party Code:** Carefully audit any third-party libraries or integrations for cross-tenant vulnerabilities. A compromised integration could bypass application-level safeguards.
