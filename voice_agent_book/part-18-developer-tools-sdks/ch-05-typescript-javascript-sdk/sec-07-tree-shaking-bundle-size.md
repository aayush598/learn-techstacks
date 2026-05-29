# Section 07: Tree-Shaking & Bundle Size

## Overview

The SDK is designed for optimal tree-shaking — modern bundlers eliminate unused exports, reducing bundle size for consumers. Every module is independently importable, side-effect-free, and ES module only. Bundle size budgets are enforced in CI to prevent regression.

## Architecture

```
Tree-Shaking Strategy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Import Patterns (Optimal vs Suboptimal):

  ❌ Bad — imports everything:
  import { VoiceAgent } from '@voiceagent/sdk';
  → Bundler must include ALL modules (agents, calls, campaigns, analytics, webhooks, streaming, utils)

  ✅ Good — imports only what's needed:
  import { VoiceAgent } from '@voiceagent/sdk';
  → If only agents is used, bundler strips unused resources

  ✅ Best — direct module imports:
  import { AgentsResource } from '@voiceagent/sdk/resources';
  import type { Agent } from '@voiceagent/sdk/types';
  → Bundle only includes agents resource and type definitions

Bundle Size Budget:
  Module                          Size (gzipped)
  ──────────────────────────────────────────────
  Core (VoiceAgent client)        5 KB
  Agents resource                 1.5 KB
  Calls resource                  1.5 KB
  Campaigns resource              1.5 KB
  Analytics resource              1 KB
  WebSocket streaming             3 KB
  Webhook verification            2 KB
  Types only                      0.5 KB
  ────────────────────────────────
  Full SDK                        12 KB
```

## Design Decisions

- **ESM-Only**: No CommonJS — tree-shaking requires static import/export analysis
- **Side-Effect-Free**: All modules have `"sideEffects": false` in package.json
- **Module Isolation**: Each resource module is independent with no circular dependencies
- **Type-Only Exports**: Type definitions in separate files; no runtime code for types

## Implementation Approach

```typescript
// package.json — side effects declaration
{
  "name": "@voiceagent/sdk",
  "version": "1.0.0",
  "type": "module",
  "sideEffects": false,
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.mjs"
    },
    "./resources": {
      "types": "./dist/resources/index.d.ts",
      "import": "./dist/resources/index.mjs"
    },
    "./resources/agents": {
      "types": "./dist/resources/agents.d.ts",
      "import": "./dist/resources/agents.mjs"
    },
    "./resources/calls": {
      "types": "./dist/resources/calls.d.ts",
      "import": "./dist/resources/calls.mjs"
    },
    "./streaming": {
      "types": "./dist/streaming/index.d.ts",
      "import": "./dist/streaming/index.mjs"
    },
    "./webhooks": {
      "types": "./dist/webhooks/index.d.ts",
      "import": "./dist/webhooks/index.mjs"
    },
    "./types": {
      "types": "./dist/types/index.d.ts",
      "import": "./dist/types/index.mjs"
    },
    "./types/agents": {
      "types": "./dist/types/agents.d.ts"
    }
  }
}

// Barrel exports — minimal, no re-exports from unused modules
// dist/index.mjs
export { VoiceAgent } from './client/voice-agent.mjs';
export { AgentsResource } from './resources/agents.mjs';
export { CallsResource } from './resources/calls.mjs';
export { CampaignsResource } from './resources/campaigns.mjs';

// NOT re-exported from barrel (import from subpath instead):
// Webhooks, Streaming — not part of core bundle

// Module isolation — no internal cross-references
// resources/agents.mjs
import { HttpClient } from '../client/http-client.mjs';
import { AgentsResource } from './agents.mjs';

// Only depends on HttpClient — no references to CallsResource or other resources

// Dynamic imports for heavy features
class VoiceAgent {
  async getWebhookHelpers(): Promise<WebhookHelpers> {
    // Webhook verification is heavy — import on demand
    const { WebhookHelpers } = await import('@voiceagent/sdk/webhooks');
    return new WebhookHelpers();
  }

  async getStreamingClient(): Promise<StreamingClient> {
    // Streaming is heavy — import on demand
    const { StreamingClient } = await import('@voiceagent/sdk/streaming');
    return new StreamingClient(this.config);
  }
}
```

## Integration Points

- **Bundler Detection**: package.json `exports` field guides bundlers to correct entry points
- **CI Bundle Analysis**: Use `size-limit` or `bundlesize` to enforce bundle size budgets
- **Import Maps**: Support import maps for CDN usage

## Production Considerations

- **Size-Limit Configuration**: CI fails if bundle size exceeds budget
- **Dependency Audit**: All dependencies must be tree-shakable; no side-effect imports
- **Regular Audits**: Run bundle analysis monthly to detect size regressions
- **Version Tags**: SDK version included in bundle for debugging; stripped in production builds

## Open-Source Tools

- **tsup**: Build ESM outputs with tree-shaking
- **size-limit**: Bundle size budget enforcement in CI
- **bundlephobia**: Bundle size analysis and comparison
