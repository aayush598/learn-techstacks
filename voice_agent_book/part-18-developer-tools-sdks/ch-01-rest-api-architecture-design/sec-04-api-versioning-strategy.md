# Section 04: API Versioning Strategy

## Overview

The Voice Agent API uses URL-based versioning with a clear deprecation and sunset policy. Every request targets a versioned URL path (`/v1/agents`), and versions follow semantic versioning semantics — v1, v2, etc. A version is published with a minimum 12-month deprecation window, and deprecated versions receive security fixes but no new features. Clients receive sunset headers well in advance of version retirement.

## Architecture

```
Versioning Strategy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

URL-Based Versioning:
  /v1/agents    → Agent API version 1
  /v2/agents    → Agent API version 2 (breaking changes)

Version Lifecycle:
  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
  │ Preview  │───▶│ Current  │───▶│ Deprecated│───▶│ Sunset   │
  │ (beta)   │    │ (stable) │    │ (12mo)   │    │ (gone)   │
  └──────────┘    └──────────┘    └──────────┘    └──────────┘

Sunset Header Response:
  Deprecation: true
  Sunset: Sat, 01 Jun 2027 00:00:00 GMT
  Link: </v2/agents>; rel="successor-version"
```

## Design Decisions

- **URL Path Versioning**: Most explicit and cache-friendly; allows different versions to be routed to different backend services
- **Semantic Versioning at API Level**: `/v1/`, `/v2/` for major breaking changes; additive changes (new fields, new endpoints) are backward-compatible within a version
- **Minimum 12-Month Deprecation Window**: Published in deprecation policy; enforced through automated sunset header warnings
- **Parallel Operation**: Multiple API versions can run simultaneously, allowing gradual client migration

## Implementation Approach

```typescript
// Version router
interface ApiVersion {
  number: string;
  status: 'preview' | 'current' | 'deprecated' | 'sunset';
  sunsetDate?: Date;
  routes: Router;
}

class ApiVersionManager {
  private versions: Map<string, ApiVersion> = new Map();

  registerVersion(version: ApiVersion): void {
    this.versions.set(version.number, version);
  }

  createVersionedRouter(): Router {
    const mainRouter = new Hono();

    for (const [versionNumber, version] of this.versions) {
      const pathPrefix = `/v${versionNumber}`;
      const router = version.routes;

      // Add deprecation middleware for deprecated versions
      if (version.status === 'deprecated') {
        router.use('*', async (c, next) => {
          c.header('Deprecation', 'true');
          c.header('Sunset', version.sunsetDate?.toUTCString() || '');
          c.header('Link', `</v${this.getCurrentVersionNumber()}>; rel="successor-version"`);
          await next();
        });
      }

      mainRouter.route(pathPrefix, router);
    }

    return mainRouter;
  }

  private getCurrentVersionNumber(): string {
    const current = Array.from(this.versions.values())
      .find(v => v.status === 'current');
    return current?.number || '';
  }
}

// API version configuration
const v1Routes = new Hono()
  .get('/agents', agentsV1.list)
  .post('/agents', agentsV1.create)
  .get('/agents/:id', agentsV1.get);

const v2Routes = new Hono()
  .get('/agents', agentsV2.list)
  .post('/agents', agentsV2.create)
  .get('/agents/:id', agentsV2.get)
  .get('/agents/:id/analytics', agentsV2.getAnalytics);

const versionManager = new ApiVersionManager();
versionManager.registerVersion({
  number: '1',
  status: 'deprecated',
  sunsetDate: new Date('2027-06-01'),
  routes: v1Routes,
});
versionManager.registerVersion({
  number: '2',
  status: 'current',
  routes: v2Routes,
});

const app = versionManager.createVersionedRouter();
```

## Integration Points

- **SDK Version Pinning**: SDKs pin a specific API version; SDK upgrades correspond to API version migrations
- **Changelog Automation**: Breaking changes are documented in the API changelog; automated migration guides are generated
- **Internal Routing**: API gateway routes versioned paths to appropriate backend deployments (v1 → legacy service, v2 → new service)

## Production Considerations

- **Version Count Limit**: Maximum 3 active versions (current + 2 deprecated) to reduce maintenance burden
- **Backward-Compatible Additions**: New fields in responses are additive — clients must ignore unknown fields
- **Migration Testing**: Run integration tests against both old and new versions during transition periods
- **Monitoring**: Track version adoption rates through analytics; auto-notify teams with high deprecated-version usage

## Open-Source Tools

- **Hono**: Router namespacing for versioned route groups
- **OpenAPI Diff**: Automated breaking change detection between API spec versions
