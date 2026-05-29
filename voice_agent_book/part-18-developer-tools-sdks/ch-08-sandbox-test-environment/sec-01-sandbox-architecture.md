# Section 01: Sandbox Architecture

## Overview

The sandbox environment provides an isolated, fully functional copy of the production API for development and testing. It mirrors production configuration but uses mock services for telephony and AI, separate databases, and dedicated API keys. Developers can test integrations, build new features, and validate configurations without affecting production data or incurring charges.

## Architecture

```
Sandbox Architecture
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Developer] → Sandbox Endpoint: api.sandbox.voiceagent.com
                   │
              [Sandbox Gateway]
                ├── Auth (sandbox-only keys: va_test_*)
                ├── Rate Limits (3x production limits)
                └── Request Logging (full capture)
                   │
              [Service Layer ─ All Mirrored]
                ├── Agent Service → Sandbox DB
                ├── Call Service  → Sandbox DB
                ├── Campaign Svc → Sandbox DB
                ├── Mock STT     → Simulated transcription
                ├── Mock AI      → Predefined responses
                ├── Mock TTS     → Short audio clips
                └── Test Phone   → Virtual numbers
                   │
              [Data Layer ─ Fully Isolated]
                ├── PostgreSQL (sandbox cluster)
                │   ├── No connection to production
                │   ├── Reset on demand
                │   └── Sample seed data
                └── Redis (sandbox instance)
                    ├── Rate limit counters
                    └── Idempotency store

Environment Comparison:
  Feature           Production      Sandbox
  ────────────────────────────────────────────
  Endpoint          api.voiceagent  api.sandbox.voiceagent
  API Key Prefix    va_live_        va_test_
  Telephony         Real PSTN/SIP   Virtual test numbers
  AI Responses      Real AI models  Predefined/mock
  Billing           Charged         Free
  Rate Limits       Standard        3x higher
  Data Retention    Permanent       7 days (or reset)
  SLA               99.9%           Best effort
```

## Design Decisions

- **Environment Mirroring**: Sandbox runs the same service code as production with different configuration
- **Mock AI Services**: Replace real AI calls with deterministic mock responses for predictable testing
- **Separate Infrastructure**: Completely isolated databases, queues, and caches — no cross-contamination risk
- **Full Request Logging**: Every sandbox request/response captured for debugging

## Implementation Approach

```typescript
// Environment configuration
interface EnvironmentConfig {
  name: 'production' | 'sandbox' | 'development';
  apiKeyPrefix: string;
  baseUrl: string;
  rateLimitMultiplier: number;
  mockServices: boolean;
  dataRetentionDays: number;
  enableBilling: boolean;
}

const ENVIRONMENTS: Record<string, EnvironmentConfig> = {
  production: {
    name: 'production',
    apiKeyPrefix: 'va_live_',
    baseUrl: 'https://api.voiceagent.com',
    rateLimitMultiplier: 1,
    mockServices: false,
    dataRetentionDays: 365,
    enableBilling: true,
  },
  sandbox: {
    name: 'sandbox',
    apiKeyPrefix: 'va_test_',
    baseUrl: 'https://api.sandbox.voiceagent.com',
    rateLimitMultiplier: 3,
    mockServices: true,
    dataRetentionDays: 7,
    enableBilling: false,
  },
};

// Sandbox-aware service factory
class ServiceFactory {
  create(config: EnvironmentConfig): ServiceContainer {
    const mockAiService = config.mockServices
      ? new MockAiService()
      : new RealAiService();

    const mockSttService = config.mockServices
      ? new MockSttService()
      : new RealSttService();

    return {
      agentService: new AgentService(this.getDb(config)),
      callService: new CallService(this.getDb(config), mockSttService, mockAiService),
      campaignService: new CampaignService(this.getDb(config)),
      billingService: config.enableBilling
        ? new RealBillingService()
        : new NoopBillingService(),
    };
  }

  private getDb(config: EnvironmentConfig): Database {
    const dbName = config.name === 'production' ? 'voiceagent_prod' : 'voiceagent_sandbox';
    return new Database({ dbName, host: config.name === 'production' ? 'prod-db' : 'sandbox-db' });
  }
}

// Sandbox reset capability
class SandboxManager {
  async reset(tenantId: string): Promise<void> {
    // Clear all tenant data
    await Promise.all([
      this.db.delete('agents', { tenantId }),
      this.db.delete('calls', { tenantId }),
      this.db.delete('campaigns', { tenantId }),
      this.db.delete('recordings', { tenantId }),
      this.redis.flushall(),
    ]);

    // Re-seed sample data
    await this.seedSampleData(tenantId);
  }

  private async seedSampleData(tenantId: string): Promise<void> {
    const sampleAgent = {
      id: generateId('ag'),
      tenantId,
      name: 'Sample Support Agent',
      status: 'active',
      voice: { provider: 'elevenlabs', voiceId: 'sample_voice' },
      model: { provider: 'openai', model: 'gpt-4o' },
    };

    await this.db.insert('agents', sampleAgent);
  }
}
```

## Integration Points

- **SDK**: Automatic environment detection from API key prefix
- **CLI**: `--environment sandbox` flag for sandbox operations
- **Developer Portal**: Sandbox toggle in dashboard; sandbox-specific API keys

## Production Considerations

- **Data Synchronization**: Sandbox configuration can be exported to production after validation
- **Resource Limits**: Sandbox has storage and request quotas to prevent abuse
- **Reset Cadence**: Automated weekly reset of sandbox data; manual reset available on demand
- **Feature Parity**: Sandbox must remain in sync with production — CI validates feature parity

## Open-Source Tools

- **Docker Compose**: Local sandbox environment for development
- **Testcontainers**: Programmatic environment setup for integration tests
