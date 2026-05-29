# Section 02: OpenAPI/Swagger Generation

## Overview

The OpenAPI 3.1 specification is auto-generated from code using Zod-to-OpenAPI conversion. The spec serves as the single source of truth for API types, SDK generation, and documentation. Spec validation runs in CI to ensure correctness and detect breaking changes.

## Architecture

```
Spec Generation Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Zod Schemas] ──→ [zod-to-openapi] ──→ [OpenAPI 3.1 YAML]
[Route Defs]  ──→ [Path Registration] ─┘        │
[Examples]    ──→ [Example Injection]           │
                                                 │
                                          [Spec Validation]
                                            ├── Schema valid?
                                            ├── Operations unique?
                                            ├── Examples match schema?
                                            └── Breaking changes detected?
                                                 │
                                          [Output]
                                            ├── openapi.yaml (development)
                                            ├── openapi.json (consumption)
                                            └── diff.yaml (breaking changes)

Spec Structure:
  openapi: 3.1.0
  info:
    title: Voice Agent API
    description: REST and WebSocket API for managing voice agents
    version: 2.1.0
    contact:
      name: Developer Support
      email: dev@voiceagent.com
  servers:
    - url: https://api.voiceagent.com/v2
      description: Production
    - url: https://api.sandbox.voiceagent.com/v2
      description: Sandbox
  security:
    - bearerAuth: []
  paths:
    /agents:
      get:
        operationId: listAgents
        summary: List all agents
        tags: [Agents]
        parameters:
          - $ref: '#/components/parameters/PaginationCursor'
          - $ref: '#/components/parameters/PaginationLimit'
        responses:
          200:
            description: Paginated agent list
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/AgentListResponse'
```

## Design Decisions

- **Code-First Generation**: Spec generated from Zod schemas — never hand-written
- **Zod-to-OpenAPI Over Swagger Annotations**: No code annotations required; types and docs from same source
- **Spec Validation**: CI validates spec against OpenAPI 3.1 schema
- **Breaking Change Detection**: compare URLs and schemas against previous version

## Implementation Approach

```typescript
import { OpenAPIRegistry, OpenApiGeneratorV3 } from '@asteasolutions/zod-to-openapi';
import { z } from 'zod';

// Create registry
const registry = new OpenAPIRegistry();

// Register schemas with metadata
const AgentSchema = z.object({
  id: z.string().openapi({ description: 'Unique agent identifier', example: 'ag_abc123' }),
  name: z.string().openapi({ description: 'Agent display name', example: 'Customer Support Bot' }),
  status: z.enum(['draft', 'active', 'paused', 'archived']).openapi({ description: 'Current agent status' }),
  voice: z.object({
    provider: z.enum(['elevenlabs', 'azure', 'google', 'amazon']),
    voiceId: z.string(),
    speed: z.number().min(0.5).max(2.0).default(1.0),
  }).openapi({ description: 'Voice configuration' }),
  model: z.object({
    provider: z.enum(['openai', 'anthropic', 'google']),
    model: z.string(),
    temperature: z.number().min(0).max(2).default(0.7),
    maxTokens: z.number().int().min(1).max(16384).default(4096),
  }).openapi({ description: 'AI model configuration' }),
  createdAt: z.string().datetime().openapi({ description: 'ISO 8601 creation timestamp' }),
  updatedAt: z.string().datetime().openapi({ description: 'ISO 8601 last update timestamp' }),
});

const CreateAgentRequestSchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().max(500).optional(),
  voice: z.object({
    provider: z.enum(['elevenlabs', 'azure', 'google', 'amazon']),
    voiceId: z.string(),
    speed: z.number().min(0.5).max(2.0).optional().default(1.0),
  }),
  model: z.object({
    provider: z.enum(['openai', 'anthropic', 'google']),
    model: z.string(),
    temperature: z.number().min(0).max(2).optional().default(0.7),
    maxTokens: z.number().int().min(1).max(16384).optional().default(4096),
  }),
  greeting: z.string().max(1000).optional(),
  timezone: z.string().optional().default('UTC'),
});

// Register components
registry.registerComponent('schemas', 'Agent', AgentSchema);
registry.registerComponent('schemas', 'CreateAgentRequest', CreateAgentRequestSchema);
registry.registerComponent('securitySchemes', 'bearerAuth', {
  type: 'http',
  scheme: 'bearer',
  bearerFormat: 'JWT',
  description: 'JWT token or API key',
});

// Register paths
registry.registerPath({
  method: 'get',
  path: '/v2/agents',
  operationId: 'listAgents',
  summary: 'List all agents',
  tags: ['Agents'],
  parameters: [
    { name: 'cursor', in: 'query', schema: { type: 'string' } },
    { name: 'limit', in: 'query', schema: { type: 'integer', minimum: 1, maximum: 100, default: 20 } },
    { name: 'status', in: 'query', schema: { type: 'string', enum: ['active', 'paused', 'draft'] } },
  ],
  responses: {
    200: {
      description: 'Paginated list of agents',
      content: { 'application/json': { schema: z.object({
        data: z.array(AgentSchema),
        pagination: z.object({ cursor: z.string().nullable(), hasMore: z.boolean() }),
      }) } },
    },
  },
});

// Generate spec
function generateSpec(): Record<string, unknown> {
  const generator = new OpenApiGeneratorV3(registry.definitions);
  return generator.generateDocument({
    openapi: '3.1.0',
    info: {
      title: 'Voice Agent API',
      version: '2.1.0',
      description: 'REST API for managing AI voice agents, calls, and campaigns.',
    },
    servers: [
      { url: 'https://api.voiceagent.com/v2', description: 'Production' },
      { url: 'https://api.sandbox.voiceagent.com/v2', description: 'Sandbox' },
    ],
  });
}

// Validate spec
async function validateSpec(spec: Record<string, unknown>): Promise<void> {
  const SwaggerParser = await import('@apidevtools/swagger-parser');
  await SwaggerParser.validate(spec as never);
}
```

## Integration Points

- **Scalar/Swagger UI**: Spec consumed by documentation UI
- **SDK Generation**: openapi-typescript consumes spec for type generation
- **API Changelog**: Spec diff generates changelog entries

## Production Considerations

- **Spec Size**: Large specs can be slow to parse; split into multiple files with $ref
- **Versioning**: Each API version has its own spec file
- **Deprecated Endpoints**: Marked with `deprecated: true` in spec
- **Spec Hosting**: Spec served at standard URL `/openapi.json` for tool discovery

## Open-Source Tools

- **zod-to-openapi**: Zod schema to OpenAPI conversion
- **@apidevtools/swagger-parser**: Spec validation and dereferencing
- **Scalar**: OpenAPI documentation UI
