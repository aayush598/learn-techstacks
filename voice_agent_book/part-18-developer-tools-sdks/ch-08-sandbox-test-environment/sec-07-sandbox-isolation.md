# Section 07: Sandbox Isolation

## Overview

Sandbox environments are fully isolated from each other and from production. Each tenant's sandbox has separate database schemas, separate caches, and no cross-tenant data access. Isolation prevents development activity from affecting other tenants and ensures production data is never exposed in development environments.

## Architecture

```
Isolation Layers
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tenant-Level Isolation:
  ┌─────────────────────────────────────────────┐
  │              Sandbox Cluster                  │
  │                                               │
  │  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
  │  │ Tenant A │  │ Tenant B │  │ Tenant C │   │
  │  │ Sandbox  │  │ Sandbox  │  │ Sandbox  │   │
  │  │          │  │          │  │          │   │
  │  │ DB_A     │  │ DB_B     │  │ DB_C     │   │
  │  │ Cache_A  │  │ Cache_B  │  │ Cache_C  │   │
  │  │ Files_A  │  │ Files_B  │  │ Files_C  │   │
  │  └──────────┘  └──────────┘  └──────────┘   │
  └─────────────────────────────────────────────┘

Production vs Sandbox:
  [Production Cluster]     [Sandbox Cluster]
  ├── prod-db-1            ├── sandbox-db-1
  ├── prod-redis           ├── sandbox-redis
  ├── prod-storage         ├── sandbox-storage
  └── prod-telephony       └── mock-telephony

No Cross-Contamination:
  - Different database schemas (prod_*, sbx_*)
  - Different Redis namespaces
  - Different file storage buckets
  - Separate Kafka topics
  - No shared queues
  - API keys scoped to environment

Reset Capability:
  [Full Reset]:
    - Drop tenant database
  - Recreate with seed data
  - Clear Redis cache
  - Delete file storage
  - Reset rate limit counters
  - Regenerate test numbers

  [Partial Reset]:
    - Delete all calls and recordings
  - Reset conversation logs
  - Keep agent configurations
```

## Design Decisions

- **Separate Database Schemas**: Logical isolation without separate infrastructure — cost-effective
- **Tenant-Specific API Keys**: API keys include environment prefix (va_test_); keys validated against tenant
- **Database Namespacing**: All tables include tenant_id column; queries filtered by tenant
- **Full Reset Available**: Complete data wipe available on demand for testing fresh state

## Implementation Approach

```typescript
// Isolation middleware
class IsolationMiddleware {
  async enforce(c: Context, next: Next): Promise<void> {
    const authContext: AuthContext = c.get('authContext');
    const isSandbox = this.isSandboxKey(authContext);

    c.set('environment', isSandbox ? 'sandbox' : 'production');
    c.set('database', this.getDatabase(isSandbox));
    c.set('cache', this.getCacheNamespace(authContext.tenantId, isSandbox));

    await next();

    // Verify no cross-tenant data in response
    this.verifyResponseIsolation(c, authContext.tenantId);
  }

  private isSandboxKey(authContext: AuthContext): boolean {
    return authContext.keyId?.startsWith('va_test_') ?? false;
  }

  private getDatabase(isSandbox: boolean): Database {
    return isSandbox ? sandboxDb : productionDb;
  }

  private getCacheNamespace(tenantId: string, isSandbox: boolean): string {
    const prefix = isSandbox ? 'sbx' : 'prd';
    return `${prefix}:${tenantId}`;
  }

  private verifyResponseIsolation(c: Context, tenantId: string): void {
    // In development, verify response only contains tenant's data
    const responseBody = c.get('responseBody');
    if (Array.isArray(responseBody?.data)) {
      for (const item of responseBody.data) {
        if (item.tenantId && item.tenantId !== tenantId) {
          console.error('CRITICAL: Cross-tenant data leak detected!');
          // Trigger alert
        }
      }
    }
  }
}

// Sandbox reset service
class SandboxResetService {
  async resetTenant(tenantId: string, type: 'full' | 'partial'): Promise<void> {
    const db = sandboxDb.schema(tenantId);

    if (type === 'full') {
      // Drop and recreate all tables for tenant
      await db.dropTables();
      await db.createTables();
      await this.seedSampleData(tenantId);
    } else {
      // Partial reset — keep configs, reset data
      await db.delete('calls', { tenantId });
      await db.delete('recordings', { tenantId });
      await db.delete('conversation_logs', { tenantId });
    }

    // Clear cache
    await sandboxRedis.del(`sbx:${tenantId}:*`);

    // Delete file storage
    await sandboxStorage.deletePrefix(`tenants/${tenantId}`);

    // Reset rate limit counters
    await sandboxRedis.del(`ratelimit:sbx:${tenantId}:*`);
  }

  private async seedSampleData(tenantId: string): Promise<void> {
    const sampleAgent = {
      id: generateId('ag'),
      tenantId,
      name: 'Sample Agent',
      status: 'draft',
      voice: { provider: 'elevenlabs', voiceId: 'sample' },
      model: { provider: 'openai', model: 'gpt-4o' },
      createdAt: new Date(),
    };

    await sandboxDb.insert('agents', sampleAgent);
  }
}

// API key validation — scoped to sandbox
function validateSandboxKey(key: string): { tenantId: string; isValid: boolean } {
  if (!key.startsWith('va_test_')) {
    return { tenantId: '', isValid: false };
  }

  // Lookup key in sandbox-only key store
  const keyRecord = sandboxKeyStore.get(key);
  return {
    tenantId: keyRecord?.tenantId || '',
    isValid: !!keyRecord,
  };
}
```

## Integration Points

- **API Gateway**: Routes requests to appropriate service based on environment prefix
- **Database Proxy**: Query middleware adds tenant_id filter automatically
- **Migration Pipeline**: Schema changes applied to both production and sandbox databases

## Production Considerations

- **Cross-Environment Access**: Production data should never be accessible from sandbox API keys
- **Data Export Controls**: Sandbox data export limited to prevent mass data extraction
- **Reset Audit**: All reset operations logged with actor identity and timestamp
- **Network Isolation**: Sandbox services run in separate VPC/subnets from production

## Open-Source Tools

- **PostgreSQL Row-Level Security**: Database-level tenant isolation
- **Redis Namespacing**: Key prefix-based isolation
