# Section 07: Documentation & Discovery

## API Documentation Architecture

API documentation is auto-generated from route definitions and Zod schemas using **OpenAPI 3.1**. The spec is served via **Scalar** (modern API client) with **Swagger UI** as fallback. SDK generation creates typed clients for popular languages.

```
┌─────────────────────────────────────────────────────────────────────┐
│              API DOCUMENTATION & DISCOVERY                          │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │               DOCUMENTATION GENERATION                       │   │
│  │                                                              │   │
│  │  Route Definitions ──→ OpenAPI Generator ←── Zod Schemas    │   │
│  │       (route.ts)              │               (validators)   │   │
│  │                               │                              │   │
│  │                               ▼                              │   │
│  │                    ┌──────────────────────┐                  │   │
│  │                    │  openapi.json (3.1)  │                  │   │
│  │                    └──────────────────────┘                  │   │
│  │                      │         │          │                  │   │
│  │                      ▼         ▼          ▼                  │   │
│  │               ┌────────┐ ┌────────┐ ┌──────────┐           │   │
│  │               │ Scalar │ │Swagger │ │ SDK Gen  │           │   │
│  │               │UI (pref)│ │UI (fall│ │(openapi- │           │   │
│  │               │        │ │ back)  │ │ typescript│           │   │
│  │               └────────┘ └────────┘ └──────────┘           │   │
│  │                                                              │   │
│  │  Generated SDKs:                                             │   │
│  │    • TypeScript (openapi-typescript)                         │   │
│  │    • Python (openapi-python-client)                          │   │
│  │    • Go (oapi-codegen)                                      │   │
│  │    • Postman Collection (postman-to-openapi)                │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │               DISCOVERY ENDPOINTS                            │   │
│  │                                                              │   │
│  │  GET  /api/openapi.json        → Full OpenAPI spec          │   │
│  │  GET  /api/docs                → Scalar UI                  │   │
│  │  GET  /api/swagger             → Swagger UI (fallback)      │   │
│  │  GET  /api/health              → Health check               │   │
│  │  GET  /api/versions            → Available API versions     │   │
│  │  GET  /api/changelog           → Recent changes             │   │
│  │  GET  /api/sdks/{language}.zip → Generated SDK download     │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## OpenAPI Generation

```typescript
// Route metadata used for spec generation
interface RouteMetadata {
  method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  path: string;
  version: string;
  summary: string;
  description: string;
  tags: string[];
  auth: 'required' | 'optional' | 'none';
  scopes?: string[];
  requestSchema?: z.ZodSchema;
  responseSchema?: z.ZodSchema;
  rateLimit?: { tier: string; limit: number };
  deprecated?: boolean;
  deprecationDate?: string;
  sunsetDate?: string;
}

// Decorator-based route metadata
function apiRoute(meta: RouteMetadata) {
  return (target: Function) => {
    ROUTE_REGISTRY.push(meta);
  };
}

// Usage
@apiRoute({
  method: 'POST',
  path: '/api/v1/agents',
  summary: 'Create a new agent',
  description: 'Creates a voice agent configuration with the specified settings.',
  tags: ['Agents'],
  auth: 'required',
  scopes: ['agents:write'],
  requestSchema: CreateAgentSchema,
  responseSchema: AgentResponseSchema,
  rateLimit: { tier: 'standard', limit: 30 },
})
export async function POST(request: NextRequest) { ... }
```

## Scalar UI Integration

```typescript
// Scalar API reference — modern, interactive API docs
// Configured via next/dynamic to avoid bundle bloat

import dynamic from 'next/dynamic';

const ApiReference = dynamic(
  () => import('@scalar/nextjs-api-reference'),
  { ssr: false }
);

export function GET() {
  const spec = generateOpenApiSpec(ROUTE_REGISTRY);
  return ApiReference({
    spec,
    configuration: {
      theme: 'purple',
      showSidebar: true,
      hideDownloadButton: false,
      searchHotkey: 'k',
      servers: [
        { url: 'https://api.voiceagent.dev', description: 'Production' },
        { url: 'https://staging.api.voiceagent.dev', description: 'Staging' },
      ],
    },
  });
}
```

## SDK Generation

```typescript
// CI workflow for SDK generation
// .github/workflows/sdk-generation.yml
// Triggers on API spec change

interface GeneratedSDK {
  language: 'typescript' | 'python' | 'go' | 'rust';
  generator: string;
  outputPath: string;
}

const SDK_GENERATORS: GeneratedSDK[] = [
  { language: 'typescript', generator: 'openapi-typescript', outputPath: 'sdks/typescript' },
  { language: 'python', generator: 'openapi-python-client', outputPath: 'sdks/python' },
  { language: 'go', generator: 'oapi-codegen', outputPath: 'sdks/go' },
];

// Generated TypeScript client example
// SDK endpoint: /sdks/typescript/voice-agent-client.ts
export class VoiceAgentClient {
  private baseUrl: string;
  private apiKey: string;

  constructor(config: { baseUrl: string; apiKey: string }) {
    this.baseUrl = config.baseUrl;
    this.apiKey = config.apiKey;
  }

  async createAgent(data: CreateAgentRequest): Promise<Agent> {
    const response = await fetch(`${this.baseUrl}/api/v1/agents`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`,
      },
      body: JSON.stringify(data),
    });
    return response.json();
  }

  async listAgents(params?: PaginationParams): Promise<PaginatedResponse<Agent>> {
    const query = new URLSearchParams(params as Record<string, string>);
    const response = await fetch(`${this.baseUrl}/api/v1/agents?${query}`, {
      headers: { 'Authorization': `Bearer ${this.apiKey}` },
    });
    return response.json();
  }
}
```

## API Changelog

```typescript
interface ChangelogEntry {
  date: string;
  version: string;
  type: 'added' | 'changed' | 'deprecated' | 'removed' | 'fixed' | 'security';
  description: string;
  affectedEndpoints?: string[];
  migrationNotes?: string;
}

const API_CHANGELOG: ChangelogEntry[] = [
  {
    date: '2026-03-15',
    version: 'v2',
    type: 'added',
    description: 'Campaign management endpoints (CRUD + scheduling)',
    affectedEndpoints: ['POST /api/v2/campaigns', 'GET /api/v2/campaigns'],
  },
  {
    date: '2026-02-01',
    version: 'v2',
    type: 'changed',
    description: 'Agent configuration schema restructured — voice and temperature moved to voiceSettings object',
    affectedEndpoints: ['POST /api/v2/agents', 'PUT /api/v2/agents/:id'],
    migrationNotes: 'See migration guide: /docs/api-migration-v1-to-v2',
  },
];
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Spec format | OpenAPI 3.1 | JSON Schema 2020-12 support, broader ecosystem |
| Documentation UI | Scalar (primary) + Swagger UI (fallback) | Modern UX, code examples, dark mode |
| SDK generation | CI-generated per commit | Always up-to-date with spec |
| Spec serving | Static JSON at `/api/openapi.json` | Cacheable, no runtime generation |
| Change tracking | CHANGELOG.md + API endpoint | Dual channel: developer portal + API discovery |

## Integration Points

- **Ch 07 (API Gateway)** — Route registry feeds spec generator
- **Ch 06 (Frontend)** — Generated TypeScript SDK used in dashboard
- **Ch 10 (Security)** — Auth requirements documented per endpoint in spec

## Production Considerations

- **Spec Size**: Full OpenAPI spec ~500KB; served with brotli compression (~80KB)
- **Versioning**: Each API version has its own spec file (`openapi-v1.json`, `openapi-v2.json`)
- **Authentication**: Spec itself is public; live API testing requires API key in Scalar UI
- **SDK Publishing**: TypeScript SDK published to npm, Python SDK to PyPI, Go SDK as GitHub release
- **Preview Deployments**: PR deployments include staging docs with preview API spec
