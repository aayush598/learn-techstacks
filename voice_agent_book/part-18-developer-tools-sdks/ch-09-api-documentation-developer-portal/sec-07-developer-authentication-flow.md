# Section 07: Developer Authentication Flow

## Overview

The developer portal includes API key management — generation, revocation, and usage monitoring. Developers can create sandbox and production keys, assign scopes, and monitor key usage. Security best practices are highlighted throughout the key management UI.

## Architecture

```
Key Management UI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Developer Portal → Settings → API Keys

┌──────────────────────────────────────────────────────┐
│ API Keys                                              │
│                                                        │
│ [Create API Key]                                       │
│                                                        │
│ Name: My Development Key                                │
│ Environment: ● Sandbox  ○ Production                   │
│ Scopes:                                                 │
│   ☑ agents:read    ☑ agents:write                      │
│   ☑ calls:read     ☐ calls:write                       │
│   ☐ campaigns:*    ☐ analytics:read                    │
│                                                        │
│ [Create Key]                                            │
│                                                        │
│ ┌────────────────────────────────────────────────────┐ │
│ │ Key Created! Copy this now — you won't see it again │ │
│ │                                                     │ │
│ │ va_test_EXAMPLE_KEY_DO_NOT_USE_IN_PROD  │ │
│ │                                                     │ │
│ │ [Copy] [Download as .env]                           │ │
│ └────────────────────────────────────────────────────┘ │
│                                                        │
│ Your Keys:                                              │
│ ┌────────────────────────────────────────────────────┐ │
│ │ Name            │ Key ID   │ Scopes    │ Created   │ │
│ ├────────────────────────────────────────────────────┤ │
│ │ Development     │ key_abc   │ agents:r/w │ Jun 1    │ │
│ │ CI Pipeline     │ key_def   │ agents:r   │ May 15   │ │
│ │ [Revoke] [Edit] │           │            │          │ │
│ └────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────┘

Usage Analytics:
  Key: My Development Key
  Last Used: 2 minutes ago
  Requests Today: 1,234
  Rate Limit Hits: 5
  Top Endpoints: /v2/agents (67%), /v2/calls (33%)
```

## Design Decisions

- **One-Time Display**: Key shown once after creation; never accessible again
- **Scope Selection**: Granular permission selection at key creation
- **Key Naming**: Required friendly name for identification
- **Usage Analytics**: Per-key usage metrics for monitoring and security

## Implementation Approach

```typescript
// API key management API (backend)
interface ApiKeyRecord {
  id: string;
  name: string;
  tenantId: string;
  environment: 'sandbox' | 'production';
  scopes: string[];
  keyPrefix: string; // First 8 chars for identification
  hash: string; // bcrypt hash
  lastUsedAt?: Date;
  createdAt: Date;
  revokedAt?: Date;
}

class ApiKeyManagementService {
  async createKey(
    tenantId: string,
    name: string,
    environment: 'sandbox' | 'production',
    scopes: string[],
  ): Promise<{ key: string; keyId: string }> {
    const keyService = new ApiKeyService();
    const generated = await keyService.generateKey(environment);

    await this.db.insert('api_keys', {
      id: generated.keyId,
      name,
      tenantId,
      environment,
      scopes,
      keyPrefix: generated.rawKey.slice(0, 12) + '...',
      hash: generated.hash,
      createdAt: new Date(),
    });

    return { key: generated.rawKey, keyId: generated.keyId };
  }

  async revokeKey(keyId: string, tenantId: string): Promise<void> {
    await this.db.update('api_keys', { id: keyId, tenantId }, {
      revokedAt: new Date(),
    });

    // Invalidate cache
    await this.redis.del(`apikey:${keyId}`);
  }

  async getKeyUsage(keyId: string, period: '24h' | '7d' | '30d'): Promise<KeyUsage> {
    const since = this.getPeriodStart(period);
    const logs = await this.analyticsDb.find('api_requests', {
      keyId,
      timestamp: { $gte: since },
    });

    return {
      totalRequests: logs.length,
      uniqueEndpoints: [...new Set(logs.map(l => l.path))],
      topEndpoints: this.getTopEndpoints(logs),
      rateLimitHits: logs.filter(l => l.status === 429).length,
      errorRate: logs.filter(l => l.status >= 500).length / logs.length * 100,
      lastUsed: logs.length > 0 ? logs[logs.length - 1].timestamp : null,
    };
  }

  private getTopEndpoints(logs: ApiRequestLog[]): Array<{ path: string; count: number }> {
    const counts = new Map<string, number>();
    for (const log of logs) {
      counts.set(log.path, (counts.get(log.path) || 0) + 1);
    }
    return Array.from(counts.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([path, count]) => ({ path, count }));
  }
}

// Frontend API key creation form
function ApiKeyCreateForm() {
  const [name, setName] = useState('');
  const [environment, setEnvironment] = useState<'sandbox' | 'production'>('sandbox');
  const [scopes, setScopes] = useState<Record<string, boolean>>({
    'agents:read': true,
    'agents:write': false,
    'calls:read': true,
    'calls:write': false,
    'campaigns:read': false,
    'campaigns:write': false,
  });

  const [createdKey, setCreatedKey] = useState<string | null>(null);

  async function handleCreate() {
    const response = await fetch('/api/v1/developer/api-keys', {
      method: 'POST',
      body: JSON.stringify({
        name,
        environment,
        scopes: Object.entries(scopes)
          .filter(([, v]) => v)
          .map(([k]) => k),
      }),
    });

    const { key, keyId } = await response.json();
    setCreatedKey(key);
  }

  if (createdKey) {
    return (
      <div className="key-created">
        <div className="alert alert-warning">
          <strong>Copy this key now!</strong> You won't be able to see it again.
        </div>
        <div className="key-display">
          <code>{createdKey}</code>
        </div>
        <div className="key-actions">
          <button onClick={() => navigator.clipboard.writeText(createdKey)}>
            Copy to Clipboard
          </button>
          <button onClick={() => downloadEnvFile(createdKey)}>
            Download .env
          </button>
        </div>
      </div>
    );
  }

  return (
    <form onSubmit={handleCreate}>
      <label>Key Name:</label>
      <input value={name} onChange={e => setName(e.target.value)} required />

      <label>Environment:</label>
      <select value={environment} onChange={e => setEnvironment(e.target.value)}>
        <option value="sandbox">Sandbox (for development)</option>
        <option value="production">Production (live traffic)</option>
      </select>

      <label>Scopes:</label>
      {Object.entries(scopes).map(([scope, enabled]) => (
        <label key={scope}>
          <input
            type="checkbox"
            checked={enabled}
            onChange={() => setScopes(prev => ({ ...prev, [scope]: !prev[scope] }))}
          />
          {scope}
        </label>
      ))}

      <button type="submit">Create API Key</button>
    </form>
  );
}
```

## Integration Points

- **Auth Service**: Key validation in API gateway
- **Usage Analytics**: Tracking per-key request metrics
- **Security Alerts**: Unusual key usage triggers alerts

## Production Considerations

- **Key Display Security**: Only show key once; use modal with copy button
- **Revocation Propagation**: Key revocation takes effect within 60 seconds via cache TTL
- **Scope Change Impact**: Changing scopes on existing keys may break integrations; warn user
- **Key Limit**: Maximum 10 API keys per tenant to prevent sprawl

## Open-Source Tools

- **bcrypt**: Key hashing for storage
- **clipboard.js**: Copy-to-clipboard utility
