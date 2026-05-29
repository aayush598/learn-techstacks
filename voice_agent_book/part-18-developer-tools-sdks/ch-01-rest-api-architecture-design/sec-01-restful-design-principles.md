# Section 01: RESTful Design Principles

## Overview

RESTful design principles form the foundation of the Voice Agent API. Resources are modeled as nouns — agents, calls, campaigns, transcripts — each accessible via deterministic URL paths. Operations on these resources are expressed through standard HTTP methods: GET for retrieval, POST for creation, PATCH for partial updates, and DELETE for removal. Statelessness ensures each request contains all context needed for processing, enabling horizontal scaling and cacheability.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                RESTful API Design Model                   │
├─────────────┬─────────────┬──────────────┬───────────────┤
│  Resource   │   GET       │   POST       │   PATCH/DELETE │
├─────────────┼─────────────┼──────────────┼───────────────┤
│ /agents     │ List agents │ Create agent │ N/A           │
│ /agents/:id │ Get agent   │ N/A          │ Update/Delete │
│ /calls      │ List calls  │ Create call  │ N/A           │
│ /campaigns  │ List cmpgns │ Create cmpgn │ Update/Delete │
└─────────────┴─────────────┴──────────────┴───────────────┘

Request Flow:
[Client] → HTTP Request (Method + Headers + Body)
              ↓
         [API Gateway] → Rate Limit Check → Auth Check
              ↓
         [Router] → URL → Resource + Action Resolution
              ↓
         [Controller] → Business Logic → Data Access
              ↓
         [Response] → Status Code + Headers + Body
```

## Design Decisions

- **Resource-Oriented**: Every URL maps to a resource or collection; actions are expressed as POST to a verb sub-resource (e.g., POST /agents/:id/deploy)
- **Statelessness**: Session state lives client-side; every request carries auth credentials and idempotency keys
- **HATEOAS**: Responses include links for discoverability — rel=next for pagination, rel=self for resource
- **Uniform Interface**: Consistent patterns across all endpoints — same pagination, same error format, same filtering syntax

## Implementation Approach

```typescript
// Core resource pattern
interface ApiResource {
  id: string;
  tenantId: string;
  createdAt: string;   // ISO 8601
  updatedAt: string;   // ISO 8601
}

interface Agent extends ApiResource {
  name: string;
  status: 'draft' | 'active' | 'paused' | 'archived';
  voice: VoiceConfig;
  model: ModelConfig;
  greeting?: string;
}

interface ListResponse<T> {
  data: T[];
  pagination: {
    cursor: string | null;
    hasMore: boolean;
    total?: number;
  };
}

// Controller pattern
class AgentsController {
  constructor(
    private readonly agentService: AgentService,
    private readonly paginationService: PaginationService,
  ) {}

  async list(req: Request, res: Response): Promise<void> {
    const { cursor, limit, status, query } = this.parseQuery(req.query);
    const filters = { status, query };
    const result = await this.agentService.list(filters, { cursor, limit });
    res.json({
      data: result.items,
      pagination: {
        cursor: result.nextCursor,
        hasMore: result.hasMore,
      },
    });
  }

  private parseQuery(query: Record<string, string>) {
    return {
      cursor: query.cursor,
      limit: Math.min(parseInt(query.limit || '20'), 100),
      status: query.status,
      query: query.query,
    };
  }
}
```

## Integration Points

- **API Gateway**: Routes requests based on URL prefix (/v1/agents, /v1/calls)
- **Auth Middleware**: Validates token and extracts tenant context before controller
- **Rate Limiter**: Enforces limits per API key per endpoint group before routing
- **Validation Layer**: Zod schemas validate request body and query parameters

## Production Considerations

- **Statelessness Enables Scale**: Any server can handle any request; no server-affinity needed
- **HTTP Caching**: GET responses carry ETag and Cache-Control headers; clients can cache safely
- **Method Safety**: GET/HEAD/OPTIONS are safe (no side effects); PUT/PATCH/DELETE are idempotent
- **Content Negotiation**: Accept header selects response format (application/json); Content-Type for request

## Open-Source Tools

- **Hono**: Lightweight, fast router for Node.js/Deno/Bun — ideal for REST APIs with Zod integration
- **tRPC**: End-to-end typesafe APIs if migrating from REST to RPC pattern
- **OpenAPI**: Specification-driven development with automatic documentation generation
