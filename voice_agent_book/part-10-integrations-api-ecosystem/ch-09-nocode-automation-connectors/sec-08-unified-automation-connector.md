# Section 08: Unified Automation Connector

## Overview

The Unified Automation Connector provides a single, consistent interface for all no-code automation platforms (Zapier, Make, n8n, Workato) to interact with the voice agent platform. Instead of maintaining separate code paths for each platform, the unified connector provides a common API layer that each automation platform's adapter translates into its specific protocol. This reduces code duplication, ensures consistent behavior across platforms, and simplifies the addition of new automation platforms.

The unified connector defines a standard protocol for automation interactions: trigger registration (webhook subscription for push events and polling endpoint for pull events), action execution (validated input to operation to formatted output), search/lookup operations, and schema discovery. Each automation platform adapter implements a thin translation layer between the platform's SDK/API and the unified connector protocol. The connector also handles cross-cutting concerns: authentication translation, rate limit mapping, error code normalization, and response formatting.

## Architecture

```
              Unified Automation Connector

   Zapier → Zapier Adapter --+
   Make   → Make Adapter   --+
   n8n    → n8n Adapter    --+
   Workato→ Workato Adapter --+
                              |
                       Unified Connector API
                              |
   +----------------------------------------------------------+
   |           Unified Automation Connector                  |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | Schema Discovery |  | Trigger Registry  |            |
   |  | • List triggers  |  | • Webhook lifecycl|            |
   |  | • List actions   |  | • Polling cursor  |            |
   |  | • Input/output   |  | • Event filtering |            |
   |  |   schemas        |  +-------------------+            |
   |  +------------------+                                    |
   |  +------------------+  +-------------------+            |
   |  | Action Dispatcher|  | Response          |            |
   |  | • Auth mapping   |  | Formatter         |            |
   |  | • Rate limit     |  | • Platform-       |            |
   |  |   translation    |  |   specific shape  |            |
   |  | • Error mapping  |  | • Field mapping   |            |
   |  +------------------+  +-------------------+            |
   +----------------------------------------------------------+
```

## Design Decisions

- **Platform adapter layer over separate endpoints per platform:** Each automation platform has a thin adapter that translates between the platform's native format and the unified connector's standard protocol. The adapter handles: authentication format conversion (OAuth2 headers vs. API key headers), pagination style (cursor vs. offset), error code mapping (404 vs. resource_not_found), and response shaping. New platforms are added by writing a new adapter without modifying the unified connector core. Trade-off: adapter layer adds indirection but eliminates platform-specific code throughout the connector stack.

- **Schema-driven adapter auto-generation over manual adapter coding:** Platform adapters are partially auto-generated from the unified connector's schema registry. The registry defines triggers, actions, and their input/output schemas in a platform-agnostic YAML format. A code generator produces the platform-specific manifest files (Zapier's app definition JSON, Make's module JSON, n8n's node TypeScript, Workato's Ruby DSL). Manual customization is needed only for platform-specific features (Make's aggregators, Workato's lookup tables). Trade-off: code generation reduces manual effort by 70% but requires maintaining a code generator for each platform.

- **Unified audit trail across all platforms over per-platform logging:** All automation operations (trigger fires, action executions, search lookups) are logged to a unified audit trail regardless of which platform initiated them. The audit trail includes the platform identifier, the operation, the input parameters (masked for sensitive fields), the response status, and the duration. This provides a single pane of glass for monitoring all automation activity. Trade-off: unified logging requires normalizing platform-specific operation identifiers but provides comprehensive automation observability.

## Implementation Approach

```
// Platform adapter interface
interface AutomationPlatformAdapter {
  readonly platform: string;
  readonly supportedAuthTypes: AuthType[];

  // Schema discovery
  getConnectorManifest(): Promise<ConnectorManifest>;

  // Trigger lifecycle
  registerTrigger(endpoint: WebhookEndpoint): Promise<TriggerRegistration>;
  unregisterTrigger(registration: TriggerRegistration): Promise<void>;

  // Action execution
  formatActionRequest(action: string, params: any): Promise<FormattedRequest>;
  formatActionResponse(action: string, response: any, raw?: any): Promise<any>;

  // Error mapping
  mapError(platformError: any): UnifiedError;
}

// Unified connector core
class UnifiedAutomationConnector {
  private adapters = new Map<string, AutomationPlatformAdapter>();

  registerAdapter(adapter: AutomationPlatformAdapter) {
    this.adapters.set(adapter.platform, adapter);
  }

  async handleTriggerRegistration(params: {
    platform: string;
    tenantId: string;
    eventType: string;
    targetUrl: string;
    filters?: Record<string, any>;
  }): Promise<TriggerRegistration> {
    const adapter = this.adapters.get(params.platform);
    if (!adapter) throw new Error(`Unsupported platform: ${params.platform}`);

    const endpoint = await this.webhookEngine.registerEndpoint({
      tenantId: params.tenantId,
      url: params.targetUrl,
      eventTypes: [params.eventType],
      filters: params.filters,
      secret: await generateSecret(),
    });

    return adapter.registerTrigger(endpoint);
  }

  async handleActionExecution(params: {
    platform: string;
    action: string;
    input: Record<string, any>;
    auth: AuthContext;
  }): Promise<any> {
    const adapter = this.adapters.get(params.platform);
    if (!adapter) throw new Error(`Unsupported platform: ${params.platform}`);

    const formatted = await adapter.formatActionRequest(params.action, params.input);
    const result = await this.executeCoreAction(params.action, formatted.body, params.auth);
    const response = await adapter.formatActionResponse(params.action, result, params.input);

    await this.auditLog({
      platform: params.platform,
      action: params.action,
      input: maskSensitiveFields(params.input),
      status: result.success ? 'success' : 'failure',
      duration: result.durationMs,
    });

    return response;
  }

  async getConnectorManifest(platform: string): Promise<ConnectorManifest> {
    const adapter = this.adapters.get(platform);
    if (!adapter) throw new Error(`Unsupported platform: ${platform}`);
    return adapter.getConnectorManifest();
  }
}

// Platform adapter example: Zapier
class ZapierAdapter implements AutomationPlatformAdapter {
  readonly platform = 'zapier';
  readonly supportedAuthTypes: AuthType[] = ['oauth2'];

  async getConnectorManifest(): Promise<ConnectorManifest> {
    const triggers = await this.schemaRegistry.getTriggers();
    const actions = await this.schemaRegistry.getActions();

    return {
      platform: 'zapier',
      authentication: { type: 'oauth2', scopes: ['default'] },
      triggers: triggers.map(t => ({
        key: t.name,
        noun: t.label,
        display: { label: t.label, description: t.description },
        operation: {
          inputFields: t.inputSchema.properties.map((p: any) => ({
            key: p.name, label: p.label, type: p.type,
            required: p.required, helpText: p.description,
          })),
          performSubscribe: { url: '/api/v1/connector/webhooks', method: 'POST' },
          performUnsubscribe: { url: '/api/v1/connector/webhooks/{{id}}', method: 'DELETE' },
          sample: t.sample,
          outputFields: t.outputSchema.properties.map((p: any) => ({
            key: p.name, label: p.label, type: p.type,
          })),
        },
      })),
      actions: actions.map(a => ({
        key: a.name,
        noun: a.label,
        display: { label: a.label, description: a.description },
        operation: {
          inputFields: a.inputSchema.properties.map((p: any) => ({
            key: p.name, label: p.label, type: p.type, required: p.required,
          })),
          perform: { url: `/api/v1/connector/actions/${a.name}`, method: 'POST' },
          sample: a.sample,
        },
      })),
    };
  }

  async registerTrigger(endpoint: WebhookEndpoint): Promise<TriggerRegistration> {
    return { id: endpoint.id, url: endpoint.url, platform: 'zapier' };
  }

  async unregisterTrigger(registration: TriggerRegistration): Promise<void> {
    await this.webhookEngine.unregisterEndpoint(registration.id);
  }

  async formatActionRequest(action: string, params: any): Promise<FormattedRequest> {
    return { method: 'POST', path: `/actions/${action}`, body: params };
  }

  async formatActionResponse(action: string, response: any, raw?: any): Promise<any> {
    return Array.isArray(response) ? response : [response];
  }

  mapError(platformError: any): UnifiedError {
    return {
      code: platformError.code || 'UNKNOWN',
      message: platformError.message || 'An error occurred',
      statusCode: platformError.statusCode || 500,
    };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Zod (MIT) | Validation | Unified schema definitions |
| Mustache (MIT) | Templates | Code generation templates |
| Pino (MIT) | Logging | Unified audit logging |

## Production Considerations

**Scaling:** The unified connector is a centralized component — all automation platform interactions pass through it. Ensure it is horizontally scalable (stateless design with shared state in Redis). Cache connector manifests aggressively (refreshed on schema registry changes via webhook). The connector API should respond within 100ms for schema discovery calls and within 30s for action execution (matching the most restrictive automation platform timeout).

**Security:** The unified connector authenticates requests from platform adapters using the adapter's API key or OAuth token. The connector itself is a privileged component — it has access to all platform operations. Ensure the connector runs with the minimum necessary permissions. All action input parameters are logged with PII masking. The connector manifest API is public (required for platform editor UIs) but should rate-limit anonymous requests.

**Monitoring:** Track unified connector metrics: adapter requests per second by platform, action execution latency by action type, trigger registration rate, manifest fetch rate, error rate by adapter and error code, and adapter health status. Alert on adapter failure (one platform's adapter down), connector response time degradation, and error rate spikes from any adapter. Monitor platform-specific API deprecation notices and plan adapter updates accordingly.
