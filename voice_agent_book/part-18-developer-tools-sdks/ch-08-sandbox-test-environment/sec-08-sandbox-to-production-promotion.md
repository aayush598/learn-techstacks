# Section 08: Sandbox-to-Production Promotion

## Overview

The promotion workflow allows developers to export validated configurations from sandbox and import them into production. The system performs validation checks during promotion to catch misconfigurations, missing dependencies, and breaking changes. An environment diff shows what will change before promotion is executed.

## Architecture

```
Promotion Workflow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Sandbox Configuration] → [Export]
                              │
                         [Validation Checks]
                           ├── Agent config valid?
                           ├── Voice ID exists in production?
                           ├── Model available in production?
                           ├── Webhook endpoints reachable?
                           └── Parameters within limits?
                              │
                      [Environment Diff]
                        ├── agents: 2 added, 1 modified, 0 removed
                        ├── webhooks: 1 added
                        └── settings: 3 changed
                              │
                      [Production Import]
                        ├── Create/modify resources
                        ├── Map sandbox IDs → production IDs
                        └── Verification step
                              │
                      [Promotion Complete]

Export Format:
  {
    "version": "1.0",
    "exportedAt": "2025-06-01T10:00:00Z",
    "source": {
      "environment": "sandbox",
      "tenantId": "tenant_demo"
    },
    "resources": {
      "agents": [
        {
          "id": "ag_sandbox_123",
          "name": "Customer Support Bot",
          "voice": { "provider": "elevenlabs", "voiceId": "21m00Tcm4TlvDq8ikWAM" },
          "model": { "provider": "openai", "model": "gpt-4o" },
          "greeting": "Hello, how can I help?",
          "status": "active"
        }
      ],
      "webhooks": [...],
      "settings": { "timezone": "UTC", "language": "en" }
    }
  }
```

## Design Decisions

- **Export-Import Model**: Full configuration export from sandbox; validated import to production
- **ID Mapping**: Sandbox resource IDs differ from production; mapping table maintained
- **Validation Gate**: Promotion fails if validation checks fail; no forced promotion
- **Rollback Support**: Promotion creates a snapshot for rollback if issues arise

## Implementation Approach

```typescript
// Promotion service
interface PromotionExport {
  version: string;
  exportedAt: Date;
  source: { environment: string; tenantId: string };
  resources: {
    agents: AgentConfig[];
    webhooks: WebhookConfig[];
    settings: Record<string, unknown>;
  };
}

interface ValidationResult {
  passed: boolean;
  checks: ValidationCheck[];
  warnings: string[];
}

interface ValidationCheck {
  resource: string;
  check: string;
  passed: boolean;
  message?: string;
}

class PromotionService {
  async exportFromSandbox(tenantId: string): Promise<PromotionExport> {
    const [agents, webhooks, settings] = await Promise.all([
      this.sandboxDb.find('agents', { tenantId }),
      this.sandboxDb.find('webhooks', { tenantId }),
      this.sandboxDb.findOne('settings', { tenantId }),
    ]);

    return {
      version: '1.0',
      exportedAt: new Date(),
      source: { environment: 'sandbox', tenantId },
      resources: {
        agents: agents.map(this.stripSandboxOnlyFields),
        webhooks: webhooks.map(this.stripSandboxOnlyFields),
        settings: settings?.config || {},
      },
    };
  }

  async validate(exported: PromotionExport): Promise<ValidationResult> {
    const checks: ValidationCheck[] = [];

    // Validate agents
    for (const agent of exported.resources.agents) {
      checks.push({
        resource: `agent:${agent.name}`,
        check: 'Voice provider available in production',
        passed: await this.voiceService.isVoiceAvailable(agent.voice.provider, agent.voice.voiceId),
      });

      checks.push({
        resource: `agent:${agent.name}`,
        check: 'Model available in production',
        passed: await this.modelService.isModelAvailable(agent.model.provider, agent.model.model),
      });

      checks.push({
        resource: `agent:${agent.name}`,
        check: 'Greeting length within limits',
        passed: !agent.greeting || agent.greeting.length <= 1000,
      });
    }

    // Validate webhooks
    for (const webhook of exported.resources.webhooks) {
      checks.push({
        resource: `webhook:${webhook.url}`,
        check: 'Webhook endpoint is reachable',
        passed: await this.isEndpointReachable(webhook.url),
      });
    }

    const passed = checks.every(c => c.passed);
    return { passed, checks, warnings: [] };
  }

  async importToProduction(exported: PromotionExport, dryRun = false): Promise<PromotionResult> {
    if (!dryRun) {
      const validation = await this.validate(exported);
      if (!validation.passed) {
        throw new Error('Validation failed — cannot promote');
      }
    }

    const idMap = new Map<string, string>(); // sandbox ID → production ID
    const results: ResourceResult[] = [];

    // Import agents
    for (const agent of exported.resources.agents) {
      if (dryRun) {
        results.push({ type: 'agent', name: agent.name, action: 'create' });
        continue;
      }

      const created = await this.productionDb.insert('agents', {
        ...this.stripIds(agent),
        tenantId: this.productionTenantId,
        status: agent.status || 'draft',
      });

      idMap.set(agent.id, created.id);
      results.push({ type: 'agent', name: agent.name, action: 'created', id: created.id });
    }

    // Import webhooks with mapped agent IDs
    for (const webhook of exported.resources.webhooks) {
      if (dryRun) continue;

      if (webhook.agentId && idMap.has(webhook.agentId)) {
        webhook.agentId = idMap.get(webhook.agentId);
      }

      await this.productionDb.insert('webhooks', webhook);
    }

    return {
      success: true,
      idMap: Object.fromEntries(idMap),
      results,
      importedAt: new Date(),
    };
  }

  private stripSandboxOnlyFields<T extends Record<string, unknown>>(resource: T): T {
    const { id, tenantId, createdAt, updatedAt, ...rest } = resource;
    return rest as T;
  }

  async generateDiff(exported: PromotionExport): Promise<EnvironmentDiff> {
    const prodAgents = await this.productionDb.find('agents', { tenantId: this.productionTenantId });

    return {
      agents: {
        added: exported.resources.agents.filter(
          a => !prodAgents.some(p => p.name === a.name),
        ).length,
        modified: exported.resources.agents.filter(
          a => prodAgents.some(p => p.name === a.name),
        ).length,
        removed: 0, // Promotion never removes resources
      },
      webhooks: {
        added: exported.resources.webhooks.length,
        modified: 0,
      },
    };
  }
}
```

## Integration Points

- **Developer Portal**: Promotion UI with diff view and confirmation
- **CLI**: `voiceagent sandbox promote` command
- **CI/CD**: Automated promotion pipeline with approval gates

## Production Considerations

- **Promotion Freeze**: Block promotions during production deployments
- **Rollback Plan**: Each promotion saves a pre-promotion snapshot for rollback
- **Audit Trail**: All promotions logged with operator identity and approval
- **Testing After Promotion**: Automated smoke tests verify promoted configurations work in production

## Open-Source Tools

- **jsondiffpatch**: JSON diff visualization for environment comparison
- **Zod**: Schema validation for exported configurations
