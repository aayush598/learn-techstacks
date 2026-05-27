# Section 07: Connection Management and Security

## Overview

Connection management handles the lifecycle of automation connector connections — API key generation and rotation, OAuth2 authorization flows, scope management, connection health monitoring, and revocation. When a user connects their voice agent account to Zapier, Make, n8n, or Workato, the connection management system authenticates the connection, establishes the appropriate auth mechanism, and maintains the connection throughout its lifecycle.

The security model ensures that each automation connection is authenticated, authorized with the minimum required permissions, and monitored for suspicious activity. Connections can be scoped to specific resources (e.g., read-only access to call data, or full access to messaging) and can be revoked at any time from the platform dashboard. The system also handles credential rotation — both proactive (the platform rotates API keys on a schedule) and reactive (a user revokes and re-creates a compromised connection).

## Architecture

```
             Connection Management & Security

   User Dashboard ←→ Connection Manager ←→ Automation Platform
                          |
   +----------------------------------------------------------+
   |              Connection Lifecycle                        |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | Create           |  | Authenticate      |            |
   |  | Connection       |  | • OAuth2 flow     |            |
   |  | • Choose platform|  | • API key validation|          |
   |  | • Select scopes  |  | • Test connection  |            |
   |  | • Label/name     |  +-------------------+            |
   |  +------------------+                                    |
   |  +------------------+  +-------------------+            |
   |  | Monitor          |  | Rotate            |             |
   |  | • Health checks  |  | • Scheduled key   |            |
   |  | • Usage tracking |  |   rotation        |            |
   |  | • Anomaly detect |  | • Emergency revoke|            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Revoke           |  | Audit Log         |             |
   |  | • User-initiated |  | • Creation        |            |
   |  | • Admin-initiated|  | • Scope changes   |            |
   |  | • Auto (expired) |  | • Rotation events |            |
   |  | • Security event |  | • Revocation      |            |
   |  +------------------+  +-------------------+            |
   +----------------------------------------------------------+
```

## Design Decisions

- **API key with granular scopes over single master key:** Each automation connection gets a unique API key with scoped permissions (e.g., `messages:write`, `calls:read`, `contacts:*`). This limits blast radius — a compromised Zapier key can only send messages, not delete call recordings. API keys are generated with a prefix identifying the connection type (e.g., `zap_`, `make_`, `n8n_`, `wrk_`) for easy identification in logs. Trade-off: granular scoping adds complexity to the permission model but provides effective security isolation between different automation use cases.

- **OAuth2 for third-party platforms, API key for self-hosted:** Zapier, Make, and Workato use OAuth2 with authorization code flow — the user is redirected to the platform, authenticates, and grants permission. n8n (self-hosted) uses API keys since there's no browser redirect flow. The connection manager supports both mechanisms with a unified connection record. OAuth2 includes refresh token rotation — each refresh returns a new refresh token, invalidating the previous one. Trade-off: maintaining both OAuth2 and API key auth doubles the authentication code surface but supports both cloud and self-hosted automation platforms.

- **Connection health monitoring with automated alerts:** Each connection is health-checked periodically (every 5 minutes for active connections) by calling the platform's `/health` endpoint with the connection's credentials. Failed health checks trigger: (1) email notification to the connection owner, (2) connection status change to "degraded", (3) automated retry every 15 minutes for 2 hours, (4) after 2 hours, status changes to "disconnected". Trade-off: health checking consumes API quota and adds load but provides early warning of connection issues before automation workflows fail.

## Implementation Approach

```
type ConnectionPlatform = 'zapier' | 'make' | 'n8n' | 'workato';
type AuthType = 'oauth2' | 'api_key';
type ConnectionStatus = 'active' | 'degraded' | 'disconnected' | 'revoked';

interface AutomationConnection {
  id: string;
  tenantId: string;
  platform: ConnectionPlatform;
  authType: AuthType;
  status: ConnectionStatus;
  label: string;
  scopes: string[];
  apiKeyHash?: string;      // bcrypt hash of API key
  oauth2Tokens?: {
    accessToken: string;    // encrypted
    refreshToken: string;   // encrypted
    expiresAt: Date;
    scope: string;
  };
  createdAt: Date;
  lastUsedAt?: Date;
  lastHealthCheckAt?: Date;
  healthCheckStatus?: 'ok' | 'failed';
  metadata: Record<string, string>;
}

class ConnectionManager {
  private db: Database;
  private encryption: EncryptionService;

  async createConnection(params: {
    tenantId: string;
    platform: ConnectionPlatform;
    authType: AuthType;
    label: string;
    scopes: string[];
  }): Promise<{ connection: AutomationConnection; credential?: string }> {
    const connection: AutomationConnection = {
      id: generateId('conn'),
      tenantId: params.tenantId,
      platform: params.platform,
      authType: params.authType,
      status: 'active',
      label: params.label,
      scopes: params.scopes,
      createdAt: new Date(),
      metadata: {},
    };

    let credential: string | undefined;

    if (params.authType === 'api_key') {
      const apiKey = this.generateAPIKey(params.platform);
      connection.apiKeyHash = await bcrypt.hash(apiKey, 12);
      credential = apiKey; // Return to user only once
    }

    await this.db.automationConnections.insert(connection);

    if (credential) {
      // Schedule health check
      await this.scheduleHealthCheck(connection.id, 0);
    }

    await this.auditLog('connection.created', { connectionId: connection.id, platform: params.platform, scopes: params.scopes });
    return { connection, credential };
  }

  async validateAndGetConnection(apiKey: string): Promise<AutomationConnection | null> {
    // Extract prefix to identify platform
    const prefix = apiKey.split('_')[0];
    const platform = this.platformFromPrefix(prefix);
    if (!platform) return null;

    const connections = await this.db.automationConnections.find({ platform, status: 'active' });
    for (const conn of connections) {
      if (conn.apiKeyHash && await bcrypt.compare(apiKey, conn.apiKeyHash)) {
        await this.db.automationConnections.update(conn.id, { lastUsedAt: new Date() });
        return conn;
      }
    }
    return null;
  }

  async rotateAPIKey(connectionId: string): Promise<string> {
    const conn = await this.db.automationConnections.find(connectionId);
    if (!conn || !conn.apiKeyHash) throw new Error('Connection not found or not API key based');

    const newKey = this.generateAPIKey(conn.platform);
    conn.apiKeyHash = await bcrypt.hash(newKey, 12);
    conn.lastHealthCheckAt = undefined;
    conn.healthCheckStatus = undefined;

    await this.db.automationConnections.update(connectionId, conn);
    await this.auditLog('connection.key_rotated', { connectionId });

    return newKey;
  }

  async revokeConnection(connectionId: string, reason: string): Promise<void> {
    const conn = await this.db.automationConnections.find(connectionId);
    if (!conn) throw new Error('Connection not found');

    conn.status = 'revoked';
    await this.db.automationConnections.update(connectionId, conn);

    // Notify automation platform if possible (Zapier/Make/Workato support webhook unsubscribe)
    await this.notifyPlatformRevocation(conn);

    await this.auditLog('connection.revoked', { connectionId, reason });
    await this.notifyUser(conn.tenantId, `Connection "${conn.label}" was revoked. Reason: ${reason}`);
  }

  async healthCheck(connectionId: string): Promise<void> {
    const conn = await this.db.automationConnections.find(connectionId);
    if (!conn || conn.status === 'revoked') return;

    try {
      const apiKey = ''; // Retrieve decrypted key
      const response = await axios.get('https://api.voiceagent.com/v1/health', {
        headers: { 'Authorization': `Bearer ${apiKey}` },
        timeout: 5000,
      });

      conn.healthCheckStatus = 'ok';
      conn.lastHealthCheckAt = new Date();
      if (conn.status === 'degraded') conn.status = 'active';
    } catch {
      conn.healthCheckStatus = 'failed';
      conn.lastHealthCheckAt = new Date();

      if (conn.status === 'active') {
        conn.status = 'degraded';
        await this.notifyUser(conn.tenantId, `Connection "${conn.label}" is experiencing issues. Please check your API key.`);
      } else if (conn.status === 'degraded') {
        // Check if > 2 hours since first failure
        const firstFailure = await this.getFirstFailureTime(connectionId);
        if (firstFailure && Date.now() - firstFailure.getTime() > 7200000) {
          conn.status = 'disconnected';
          await this.notifyUser(conn.tenantId, `Connection "${conn.label}" has been disconnected due to persistent failures.`);
        }
      }
    }

    await this.db.automationConnections.update(connectionId, conn);
  }

  private generateAPIKey(platform: ConnectionPlatform): string {
    const prefix = this.platformPrefixMap[platform];
    const random = crypto.randomBytes(32).toString('hex');
    return `${prefix}_${random}`;
  }

  private platformPrefixMap: Record<ConnectionPlatform, string> = {
    zapier: 'zap',
    make: 'make',
    n8n: 'n8n',
    workato: 'wrk',
  };

  private platformFromPrefix(prefix: string): ConnectionPlatform | null {
    const map: Record<string, ConnectionPlatform> = { zap: 'zapier', make: 'make', n8n: 'n8n', wrk: 'workato' };
    return map[prefix] || null;
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| bcrypt (MIT) | Node.js | API key hashing |
| @node-rs/argon2 (MIT) | Node.js | Password hashing alternative |
| nanoid (MIT) | IDs | Connection ID generation |

## Production Considerations

**Scaling:** Each automation connection requires periodic health checks. For 10,000 active connections, the health check system makes 120,000 API calls per day (every 5 minutes). Use a dedicated worker pool for health checks with configurable concurrency. OAuth2 token refresh also creates load — batch token refreshes to avoid simultaneous refresh storms. API key hashing (bcrypt cost 12) is slow — consider using argon2 for better performance or cache hashed keys in memory.

**Security:** API keys are returned to the user only at creation time. Store only the bcrypt hash in the database. Support key fingerprinting (first 8 characters of the hash) for identifying keys in logs without exposing the full hash. OAuth2 tokens are encrypted at rest using envelope encryption (AES-256-GCM with a key encryption key stored in a HSM or cloud KMS). Implement connection usage anomaly detection — alert on connections suddenly making requests from unusual IP ranges or at unusual times.

**Monitoring:** Track active connections per platform, connection creation/revocation rates, health check pass/fail rates, connection degradation time, average connection lifetime, and OAuth2 token expiry events. Alert on connection failure rates exceeding 10%, sudden revocation spikes (possible security incident), expired OAuth tokens not being refreshed, and connections with no activity for 90+ days (consider auto-archiving).
