# Section 02: Resource Naming Conventions

## Overview

Consistent resource naming conventions make the API intuitive, predictable, and self-documenting. The Voice Agent API follows plural noun naming for collections, lowercase kebab-case for resource identifiers, and hierarchical paths for nested resources. Every URL corresponds to exactly one resource or collection, and path segments represent ownership relationships.

## Architecture

```
URL Structure Patterns
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Collection:     /v1/{resource}
Singleton:      /v1/{resource}/{id}
Sub-collection: /v1/{resource}/{id}/{sub-resource}
Action:         POST /v1/{resource}/{id}/{action}

Examples:
  GET  /v1/agents                    → List all agents
  POST /v1/agents                    → Create new agent
  GET  /v1/agents/ag_12345           → Get specific agent
  PATCH /v1/agents/ag_12345          → Update agent
  DELETE /v1/agents/ag_12345         → Delete agent
  GET  /v1/agents/ag_12345/calls     → List agent's calls
  POST /v1/calls/cl_67890/transfer   → Action on call
  POST /v1/agents/ag_12345/deploy    → Action on agent
```

## Design Decisions

- **Plural Nouns**: Always `/agents`, never `/agent` or `/getAgents` — collections are plural, singletons return one item
- **Hierarchical Nesting**: Resources that only exist within a parent use nested paths; globally addressable resources use flat paths
- **Action Verbs**: Non-CRUD operations use POST with a verb segment — `POST /agents/:id/deploy` not `POST /agents/:id?action=deploy`
- **Consistent ID Prefix**: Resource IDs include a type prefix (`ag_`, `cl_`, `cmp_`) for readability and type inference

## Implementation Approach

```typescript
// Route registration using Hono
import { Hono } from 'hono';

const app = new Hono();

// Collection routes
app.get('/v1/agents', agentsController.list);
app.post('/v1/agents', agentsController.create);

// Singleton routes
app.get('/v1/agents/:id', agentsController.get);
app.patch('/v1/agents/:id', agentsController.update);
app.delete('/v1/agents/:id', agentsController.delete);

// Sub-collection routes
app.get('/v1/agents/:id/calls', callsController.listByAgent);
app.post('/v1/agents/:id/calls', callsController.createForAgent);

// Action routes
app.post('/v1/agents/:id/deploy', agentsController.deploy);
app.post('/v1/agents/:id/test', agentsController.test);

// Naming validation utility
const RESOURCE_PREFIXES = {
  agent: 'ag',
  call: 'cl',
  campaign: 'cmp',
  transcript: 'trn',
  recording: 'rec',
  webhook: 'wh',
} as const;

function generateResourceId(type: keyof typeof RESOURCE_PREFIXES): string {
  const prefix = RESOURCE_PREFIXES[type];
  const random = crypto.randomBytes(16).toString('hex');
  return `${prefix}_${random}`;
}

function isValidResourceId(id: string): boolean {
  const prefixes = Object.values(RESOURCE_PREFIXES).join('|');
  return new RegExp(`^(${prefixes})_[a-f0-9]{32}$`).test(id);
}
```

## Integration Points

- **API Gateway Routing**: Path patterns map to backend services — `/v1/agents/*` → agent service
- **SDK Client Generation**: Consistent URL patterns enable automatic client generation from OpenAPI spec
- **API Versioning**: All paths start with `/v1/` — the version prefix is part of the URL structure

## Production Considerations

- **URL Length Limits**: Proxies and load balancers enforce max URL length (~8KB); deeply nested paths can hit limits
- **Caching Granularity**: Collection URLs are uncacheable by default; singleton URLs are cacheable with proper TTLs
- **Backward Compatibility**: Once published, URL structures are permanent — use query parameters for optional features, never change existing path semantics

## Open-Source Tools

- **Hono**: Route parameter extraction and validation middleware
- **OpenAPI 3.1**: Path patterns documented via URI templates in the spec
