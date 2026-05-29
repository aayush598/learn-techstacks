# Section 08: API Documentation Standards

## Overview

API documentation is generated automatically from OpenAPI 3.1 specification files, which are themselves generated from Zod schemas and route definitions. Every endpoint includes operation IDs, request/response examples, and error documentation. Documentation is versioned alongside the API, and consumers can browse interactive docs through Swagger UI or Scalar.

## Architecture

```
Documentation Generation Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Zod Schemas] ──→ [Zod-to-OpenAPI] ──→ [OpenAPI 3.1 Spec]
[Route Defs]  ──→ [Metadata Parser] ─┘        │
[Comments]    ──→ [Description Extractor]──┘   │
                                                ↓
                                    [Spec Validation]
                                                │
                          ┌─────────────────────┼─────────────────────┐
                          ↓                     ↓                     ↓
                    [Swagger UI]          [Scalar Docs]        [TypeScript Types]
                    Interactive Docs      Beautiful Docs       SDK Type Generation

OpenAPI Spec Structure:
  openapi: 3.1.0
  info:
    title: Voice Agent API
    version: "2.0.0"
  paths:
    /v1/agents:
      get:
        operationId: listAgents
        summary: List all agents
        parameters:
          - name: cursor
            in: query
            schema: { type: string }
          - name: limit
            in: query
            schema: { type: integer, minimum: 1, maximum: 100 }
        responses:
          200:
            description: List of agents
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/AgentListResponse'
```

## Design Decisions

- **Code-First Spec Generation**: Specs are generated from code (Zod schemas), not written by hand — reduces drift
- **Operation ID Convention**: `{resource}{Action}` camelCase — `listAgents`, `createAgent`, `getAgent`
- **Response Examples**: Every response schema includes a realistic example generated from test data
- **Changelog as Code**: API changes are tracked in a CHANGELOG.md file with version entries and migration notes

## Implementation Approach

```typescript
// OpenAPI generation from Zod schemas
import { OpenAPIRegistry, OpenApiGeneratorV3 } from '@asteasolutions/zod-to-openapi';
import { z } from 'zod';

const registry = new OpenAPIRegistry();

// Register schemas
const AgentSchema = z.object({
  id: z.string().openapi({ description: 'Unique agent identifier' }),
  name: z.string().openapi({ example: 'Customer Support Bot' }),
  status: z.enum(['draft', 'active', 'paused']),
  createdAt: z.string().datetime(),
});

const ListAgentsResponse = z.object({
  data: z.array(AgentSchema),
  pagination: z.object({
    cursor: z.string().nullable(),
    hasMore: z.boolean(),
  }),
});

// Register routes with metadata
registry.registerPath({
  method: 'get',
  path: '/v1/agents',
  operationId: 'listAgents',
  summary: 'List all voice agents',
  description: 'Returns a paginated list of agents belonging to the authenticated tenant.',
  tags: ['Agents'],
  parameters: [
    { name: 'cursor', in: 'query', schema: { type: 'string' } },
    { name: 'limit', in: 'query', schema: { type: 'integer', minimum: 1, maximum: 100 } },
    { name: 'status', in: 'query', schema: { type: 'string', enum: ['active', 'paused', 'draft'] } },
  ],
  responses: {
    200: {
      description: 'Paginated list of agents',
      content: { 'application/json': { schema: ListAgentsResponse } },
    },
    429: { description: 'Rate limit exceeded' },
  },
});

// Generate spec
const generator = new OpenApiGeneratorV3(registry.definitions);
const spec = generator.generateDocument({
  openapi: '3.1.0',
  info: {
    title: 'Voice Agent API',
    version: '2.0.0',
    description: 'REST API for managing AI voice agents, calls, and campaigns.',
  },
  servers: [
    { url: 'https://api.voiceagent.com', description: 'Production' },
    { url: 'https://api.sandbox.voiceagent.com', description: 'Sandbox' },
  ],
  security: [{ bearerAuth: [] }],
});

// Spec validation
import SwaggerParser from '@apidevtools/swagger-parser';
await SwaggerParser.validate(spec);
```

## Integration Points

- **SDK Code Generation**: OpenAPI spec feeds `openapi-typescript` and `openapi-python-client` for SDK generation
- **Documentation Portal**: Spec is consumed by Scalar or Swagger UI for interactive documentation
- **API Changelog**: Breaking changes in the spec trigger automated changelog entries

## Production Considerations

- **Spec Drift Detection**: CI pipeline validates that published spec matches generated spec
- **Security Schemas**: Document authentication methods in the security section — bearerAuth, apiKey
- **Rate Limit Documentation**: Document rate limit headers and error responses in the spec
- **Deprecated Endpoints**: Use `deprecated: true` in the spec to indicate deprecated paths

## Open-Source Tools

- **Zod-to-OpenAPI**: Automatic OpenAPI generation from Zod schemas
- **Scalar**: Beautiful, customizable API documentation UI
- **Swagger UI**: Interactive API explorer with try-it-out functionality
- **@apidevtools/swagger-parser**: Spec validation and dereferencing
