# Section 02: API Versioning Strategy

## Versioning Approach

The API uses **URL-based versioning** with the prefix `/api/v1/`, `/api/v2/`, etc. This provides clear visibility of API version in every request URL and enables simple routing at the gateway level.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    API VERSIONING STRATEGY                          │
│                                                                     │
│  Request Path          Version   Status        Notes                │
│  ────────────────────────────────────────────────────────────      │
│  /api/v1/agents        v1        Active        Current stable       │
│  /api/v1/calls         v1        Active                            │
│  /api/v2/agents        v2        Beta          New features         │
│  /api/v2/analytics     v2        Preview       Breaking changes    │
│  /api/v0/agents        v0        Deprecated    Sunset: 2026-06-30  │
│                        (Sunset header returned)                    │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              Gateway Version Routing                        │   │
│  │                                                              │   │
│  │  /api/v1/*  ───→  agent-service (stable)                    │   │
│  │  /api/v2/*  ───→  agent-service-v2 (canary)                 │   │
│  │  /api/v0/*  ───→  410 Gone (or routes to EOL handler)      │   │
│  │                                                              │   │
│  │  Header-based alternative (not used):                        │   │
│  │    Accept: application/vnd.voiceagent.v2+json                │   │
│  │    → Rejected for: poor visibility, caching complexity       │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Version Lifecycle

```typescript
interface ApiVersion {
  version: string;
  status: 'active' | 'beta' | 'deprecated' | 'sunset';
  releaseDate: string;
  deprecationDate?: string;
  sunsetDate?: string;
  changelog: string[];
  migrationGuide?: string; // URL to migration docs
}

const API_VERSIONS: ApiVersion[] = [
  {
    version: 'v1',
    status: 'active',
    releaseDate: '2025-01-15',
    changelog: ['Initial release', 'Agent CRUD', 'Call management'],
  },
  {
    version: 'v2',
    status: 'beta',
    releaseDate: '2026-03-01',
    changelog: [
      'BREAKING: Agent config schema restructured',
      'Added: Real-time analytics endpoint',
      'Added: Campaign management',
    ],
    migrationGuide: '/docs/api-migration-v1-to-v2',
  },
  {
    version: 'v0',
    status: 'sunset',
    releaseDate: '2024-06-01',
    deprecationDate: '2025-12-01',
    sunsetDate: '2026-06-30',
    changelog: ['Legacy beta API'],
    migrationGuide: '/docs/api-migration-v0-to-v1',
  },
];
```

## Deprecation Policy

```typescript
// Middleware that checks for deprecated versions
async function deprecationMiddleware(request: NextRequest): Promise<NextResponse | null> {
  const version = extractVersion(request.nextUrl.pathname);
  const versionInfo = API_VERSIONS.find(v => v.version === version);

  if (!versionInfo) {
    return formatError('unknown_version', `API version '${version}' does not exist`, 404);
  }

  const response = NextResponse.next();

  if (versionInfo.status === 'deprecated' && versionInfo.sunsetDate) {
    response.headers.set('Sunset', new Date(versionInfo.sunsetDate).toUTCString());
    response.headers.set('Deprecation', 'true');
    response.headers.set(
      'Link',
      `<${versionInfo.migrationGuide}>; rel="deprecation"; type="text/html"`
    );
    // Add warning header for deprecation
    response.headers.set(
      'Warning',
      `299 - "This API version is deprecated. Sunset: ${versionInfo.sunsetDate}. See: ${versionInfo.migrationGuide}"`
    );
  }

  if (versionInfo.status === 'sunset') {
    return formatError('api_sunset', `API version '${version}' is no longer supported`, 410, {
      sunsetDate: versionInfo.sunsetDate,
      migrationGuide: versionInfo.migrationGuide,
    });
  }

  return response;
}
```

## Migration Support

```typescript
// Request transformation for gradual migration
// When using header Accept-Version: v1, v2 endpoint is mapped to v1 schema
interface VersionTransform {
  fromVersion: string;
  toVersion: string;
  transformRequest: (body: unknown) => unknown;
  transformResponse: (body: unknown) => unknown;
}

const V1_TO_V2_TRANSFORM: VersionTransform = {
  fromVersion: 'v2',
  toVersion: 'v1',
  transformRequest: (body: AgentConfigV2): AgentConfigV1 => ({
    name: body.name,
    voice_id: body.voiceSettings.model,
    temperature: body.voiceSettings.temperature,
    prompt: body.behavior.systemPrompt,
    // ... field mappings
  }),
  transformResponse: (body: AgentConfigV1): AgentConfigV2 => ({
    name: body.name,
    voiceSettings: {
      model: body.voice_id,
      temperature: body.temperature,
    },
    behavior: {
      systemPrompt: body.prompt,
    },
  }),
};
```

## Sunset Headers

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SUNSET HEADER BEHAVIOR                           │
│                                                                     │
│  Phase 1: Deprecation (6 months before sunset)                     │
│  Response Headers:                                                  │
│    Sunset: Sat, 30 Jun 2026 00:00:00 GMT                           │
│    Deprecation: true                                                │
│    Warning: 299 - "This API version is deprecated. Sunset: ..."     │
│    Link: </docs/api-migration>; rel="deprecation"                   │
│                                                                     │
│  Phase 2: Sunset (after sunset date)                               │
│  Response:                                                          │
│    Status: 410 Gone                                                 │
│    Body: { "error": { "code": "api_sunset", ... } }                │
│    Link: </docs/api-migration>; rel="deprecation"                   │
│                                                                     │
│  Client Notification:                                               │
│    • Email sent 90 days before sunset                               │
│    • Email sent 30 days before sunset                               │
│    • Email sent on sunset date                                      │
│    • Dashboard banner for affected tenants                          │
└─────────────────────────────────────────────────────────────────────┘
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Version in URL vs header | URL prefix (`/api/v1/`) | Visible, cacheable, simpler routing, easier debugging |
| Deprecation period | 6 months minimum | Industry standard, gives clients adequate migration time |
| Sunset enforcement | 410 Gone after date | Clear signal, no silent failures |
| Migration transforms | Gateway-level field mapping | Clients upgrade independently, wire format compatibility |
| Backward compatibility | Additive changes only within major version | Avoid breaking existing clients |

## Integration Points

- **Ch 07 (API Gateway)** — Version routing implemented in gateway middleware
- **Ch 07 (Documentation)** — OpenAPI spec generated per version with deprecation annotations
- **Ch 03 (Database)** — Schema migrations versioned alongside API versions

## Production Considerations

- **Version Count**: Maximum 3 active versions (current stable, previous deprecated, next beta)
- **Migration Analytics**: Track API version usage per tenant to identify stragglers
- **Automated Testing**: CI runs integration tests against all active versions
- **Changelog Feed**: `/api/changelog` endpoint returns all releases with breaking change indicators
- **Client SDK**: Generated SDKs include version pinning and deprecation warnings
