# Section 01: SDK Architecture Design

## Overview

The TypeScript/JavaScript SDK provides a fluent, typed interface for interacting with the Voice Agent API. The architecture follows a modular pattern with tree-shakable exports, a client class pattern for configuration, and a plugin system for extensibility. Every module is independently importable, enabling consumers to import only what they use.

## Architecture

```
SDK Module Structure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@voiceagent/sdk/
├── index.ts                    → Public exports (barrel)
├── client/
│   ├── voice-agent.ts          → Main client class
│   ├── config.ts               → Client configuration
│   └── errors.ts               → Error classes
├── resources/
│   ├── agents.ts               → Agent resource client
│   ├── calls.ts                → Call resource client
│   ├── campaigns.ts            → Campaign resource client
│   ├── analytics.ts            → Analytics resource client
│   └── webhooks.ts             → Webhook resource client
├── streaming/
│   ├── websocket.ts            → WebSocket transport
│   ├── sse.ts                  → SSE transport
│   └── events.ts               → Event subscription
├── webhooks/
│   ├── verify.ts               → Signature verification
│   └── parser.ts               → Event parsing
├── types/
│   ├── agents.ts               → Agent type definitions
│   ├── calls.ts                → Call type definitions
│   ├── common.ts               → Shared types
│   └── events.ts               → Event type definitions
└── utils/
    ├── retry.ts                → Retry with backoff
    ├── pagination.ts           → Pagination helpers
    ├── backoff.ts              → Exponential backoff
    └── version.ts              → SDK version

Tree-Shakable Exports:
  import { VoiceAgent } from '@voiceagent/sdk';           // Full client
  import { AgentsResource } from '@voiceagent/sdk/resources';  // Just agents
  import { verifyWebhook } from '@voiceagent/sdk/webhooks';    // Just webhook verify
  import type { Agent } from '@voiceagent/sdk/types';           // Just types
```

## Design Decisions

- **ESM-Only**: No CommonJS support — enables tree-shaking and modern bundler optimization
- **Modular Resources**: Each API resource is a separate class instantiated by the client; allows tree-shaking
- **Plugin Architecture**: Middleware-like plugin system for logging, retry, auth injection
- **Zero Runtime Dependencies**: Only dev dependencies for types — runtime uses native fetch and WebSocket

## Implementation Approach

```typescript
// Main client class
interface VoiceAgentConfig {
  apiKey: string;
  environment?: 'production' | 'sandbox' | 'development';
  baseUrl?: string;
  timeout?: number;
  retry?: RetryConfig;
  plugins?: Plugin[];
}

class VoiceAgent {
  private config: Required<VoiceAgentConfig>;
  private httpClient: HttpClient;
  private pluginPipeline: PluginPipeline;

  readonly agents: AgentsResource;
  readonly calls: CallsResource;
  readonly campaigns: CampaignsResource;
  readonly analytics: AnalyticsResource;
  readonly webhooks: WebhookHelpers;

  constructor(config: VoiceAgentConfig) {
    this.config = {
      apiKey: config.apiKey,
      environment: config.environment || 'production',
      baseUrl: config.baseUrl || this.getDefaultBaseUrl(config.environment || 'production'),
      timeout: config.timeout || 30_000,
      retry: config.retry || { maxRetries: 3, baseDelay: 1000 },
      plugins: config.plugins || [],
    };

    this.httpClient = new HttpClient(this.config);
    this.pluginPipeline = new PluginPipeline(this.config.plugins);

    // Initialize resource clients
    this.agents = new AgentsResource(this.httpClient, this.pluginPipeline);
    this.calls = new CallsResource(this.httpClient, this.pluginPipeline);
    this.campaigns = new CampaignsResource(this.httpClient, this.pluginPipeline);
    this.analytics = new AnalyticsResource(this.httpClient, this.pluginPipeline);
    this.webhooks = new WebhookHelpers();
  }

  private getDefaultBaseUrl(environment: string): string {
    const urls: Record<string, string> = {
      production: 'https://api.voiceagent.com',
      sandbox: 'https://api.sandbox.voiceagent.com',
      development: 'http://localhost:3000',
    };
    return urls[environment] || urls.production;
  }
}

// Plugin system
interface Plugin {
  name: string;
  request?: (req: RequestInit) => RequestInit | Promise<RequestInit>;
  response?: (res: Response, req: RequestInit) => Response | Promise<Response>;
  error?: (error: Error) => void;
}

class PluginPipeline {
  constructor(private plugins: Plugin[]) {}

  async applyRequest(req: RequestInit): Promise<RequestInit> {
    let modified = { ...req };
    for (const plugin of this.plugins) {
      if (plugin.request) {
        modified = await plugin.request(modified);
      }
    }
    return modified;
  }

  async applyResponse(res: Response, req: RequestInit): Promise<Response> {
    let modified = res;
    for (const plugin of this.plugins) {
      if (plugin.response) {
        modified = await plugin.response(modified, req);
      }
    }
    return modified;
  }
}

// Example plugin: logging
const loggingPlugin: Plugin = {
  name: 'logger',
  request: async (req) => {
    console.debug(`[VoiceAgent] ${req.method} ${req.url}`);
    return req;
  },
  response: async (res) => {
    console.debug(`[VoiceAgent] ${res.status} ${res.url}`);
    return res;
  },
};

// Tree-shakable resource client
class AgentsResource {
  constructor(
    private http: HttpClient,
    private plugins: PluginPipeline,
  ) {}

  async list(params?: {
    cursor?: string;
    limit?: number;
    status?: string;
  }): Promise<ListResponse<Agent>> {
    return this.http.get('/v1/agents', { params });
  }

  async get(id: string): Promise<Agent> {
    return this.http.get(`/v1/agents/${id}`);
  }

  async create(data: CreateAgentRequest): Promise<Agent> {
    return this.http.post('/v1/agents', { body: data });
  }

  async update(id: string, data: Partial<UpdateAgentRequest>): Promise<Agent> {
    return this.http.patch(`/v1/agents/${id}`, { body: data });
  }

  async delete(id: string): Promise<void> {
    return this.http.delete(`/v1/agents/${id}`);
  }

  async deploy(id: string): Promise<DeployResult> {
    return this.http.post(`/v1/agents/${id}/deploy`);
  }
}

// Usage
const client = new VoiceAgent({
  apiKey: 'va_live_abc123',
  plugins: [loggingPlugin],
});

const agents = await client.agents.list({ status: 'active' });
```

## Integration Points

- **OpenAPI Codegen**: Resource types and method signatures generated from OpenAPI spec
- **Plugin Ecosystem**: OpenTelemetry, rate limit handling, custom auth providers
- **Package Registry**: Published to npm as `@voiceagent/sdk`

## Production Considerations

- **Bundle Size Budget**: Core SDK < 10KB gzipped; each resource module < 3KB gzipped
- **Version Compatibility**: SDK version pinned in package.json; semver for API compatibility
- **Runtime Support**: Node.js 18+, modern browsers (last 2 versions)
- **Deprecation Warnings**: SDK methods emit deprecation warnings in console when using deprecated API features

## Open-Source Tools

- **openapi-typescript**: Type generation from OpenAPI spec
- **tsup**: TypeScript bundler for ESM output
