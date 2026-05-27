# Developer Key Dashboard

## Overview

The developer dashboard provides a UI for managing API keys with masked key display, usage graphs, last-used timestamps, and quick actions for creating, revoking, and rotating keys.

## Dashboard Components

```typescript
interface KeyDashboardData {
  keys: KeyCardData[];
  totalCalls: number;
  activeKeys: number;
  expiringKeys: number;
  usageByDay: UsageDataPoint[];
}

interface KeyCardData {
  id: string;
  name: string;
  prefix: string;
  environment: 'live' | 'test';
  scopes: string[];
  createdAt: Date;
  expiresAt?: Date;
  lastUsedAt?: Date;
  status: 'active' | 'expired' | 'revoked';
  usage: { daily: number; monthly: number };
}
```

## API

```typescript
class DeveloperKeyController {
  async listKeys(req: Request, res: Response): Promise<void> {
    const keys = await this.apiKeyStore.findByUserId(req.user.id);
    const dashboardData: KeyDashboardData = {
      keys: keys.map(k => ({
        id: k.id,
        name: k.name,
        prefix: k.prefix,
        environment: k.environment,
        scopes: k.scopes,
        createdAt: k.createdAt,
        expiresAt: k.expiresAt,
        lastUsedAt: k.lastUsedAt,
        status: k.revokedAt ? 'revoked' : k.expiresAt && k.expiresAt < new Date() ? 'expired' : 'active',
        usage: { daily: 0, monthly: 0 },
      })),
      totalCalls: keys.reduce((sum, k) => sum + (k.usage?.monthly || 0), 0),
      activeKeys: keys.filter(k => !k.revokedAt).length,
      expiringKeys: keys.filter(k =>
        k.expiresAt && k.expiresAt > new Date() &&
        k.expiresAt < new Date(Date.now() + 14 * 86400000)
      ).length,
      usageByDay: [],
    };

    res.json(dashboardData);
  }

  async getUsageGraph(req: Request, res: Response): Promise<void> {
    const { keyId } = req.params;
    const usage = await this.usageService.getKeyUsage(keyId, 30);
    res.json({
      labels: usage.map(u => u.date),
      values: usage.map(u => u.count),
    });
  }
}
```

## UI Component

```typescript
function DeveloperKeyDashboard() {
  const { data, isLoading } = useQuery(['api-keys'], () => api.get('/developer/keys'));
  const [showCreate, setShowCreate] = useState(false);

  if (isLoading) return <Skeleton />;

  return (
    <div>
      <div className="stats-bar">
        <StatCard label="Active Keys" value={data.activeKeys} />
        <StatCard label="Total Calls (30d)" value={data.totalCalls.toLocaleString()} />
        <StatCard label="Expiring Soon" value={data.expiringKeys} warning={data.expiringKeys > 0} />
      </div>
      <div className="key-list">
        {data.keys.map(key => (
          <KeyCard key={key.id} keyData={key} />
        ))}
      </div>
      <UsageGraph data={data.usageByDay} />
      <Button onClick={() => setShowCreate(true)}>Create API Key</Button>
      {showCreate && <CreateKeyModal onClose={() => setShowCreate(false)} />}
    </div>
  );
}

function KeyCard({ keyData }: { keyData: KeyCardData }) {
  return (
    <div className="key-card">
      <div className="key-header">
        <span className="key-name">{keyData.name}</span>
        <span className={`badge ${keyData.environment}`}>{keyData.environment}</span>
        <span className={`badge ${keyData.status}`}>{keyData.status}</span>
      </div>
      <code className="key-prefix">{keyData.prefix}</code>
      <div className="key-meta">
        <span>Created: {formatDate(keyData.createdAt)}</span>
        {keyData.lastUsedAt && <span>Last used: {formatRelative(keyData.lastUsedAt)}</span>}
        {keyData.expiresAt && <span>Expires: {formatDate(keyData.expiresAt)}</span>}
      </div>
      <div className="key-scopes">
        {keyData.scopes.map(s => <span key={s} className="scope-tag">{s}</span>)}
      </div>
      <div className="key-actions">
        <Button variant="outline" onClick={() => rotateKey(keyData.id)}>Rotate</Button>
        <Button variant="danger" onClick={() => revokeKey(keyData.id)}>Revoke</Button>
      </div>
    </div>
  );
}
```

## Open-Source Tools

- **Recharts** (MIT) — Usage graph visualization
- **React Table** (MIT) — Key listing table

## Production Considerations

- Mask key values (show only last 4 characters)
- Provide one-click copy of full key at creation only
- Show key health indicators (usage vs quota, expiry status)
- Usage graph with daily breakdown for last 30/90 days
- Sort keys by last used, creation date, or expiry
- Confirm destructive actions (revoke, rotate) with modal
- Allow filtering by environment (live/test) and status
- Include quick scope editor for existing keys
