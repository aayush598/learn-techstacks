# Section 08: Compatibility & Breaking Changes

## Breaking Change Policy

Breaking changes follow a **strict policy** with minimum 6-month deprecation periods, feature flags for gradual rollout, and automated compatibility testing. All breaking changes are additive-first where possible.

```
┌─────────────────────────────────────────────────────────────────────┐
│              BREAKING CHANGE LIFECYCLE                              │
│                                                                     │
│  Phase 1: Announcement                                             │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │  • Publish RFC in developer portal                         │     │
│  │  • Tag with "breaking" in changelog                        │     │
│  │  • Email notification to all affected tenants              │     │
│  │  • Duration: 30 days for feedback                          │     │
│  └────────────────────────────────────────────────────────────┘     │
│                              │                                       │
│  Phase 2: Deprecation                                              │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │  • Old behavior still works                                │     │
│  │  • Warning headers on every response:                      │     │
│  │    Sunset: <date>                                          │     │
│  │    Deprecation: true                                       │     │
│  │  • Duration: Minimum 6 months                              │     │
│  │  • Dashboard banner for affected tenants                   │     │
│  └────────────────────────────────────────────────────────────┘     │
│                              │                                       │
│  Phase 3: Sunset                                                  │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │  • Old endpoints return 410 Gone                           │     │
│  │  • Error response includes migration guide link            │     │
│  │  • Last-chance email sent 30 days prior                   │     │
│  │  • Duration: Perpetual (410 persists)                      │     │
│  └────────────────────────────────────────────────────────────┘     │
│                              │                                       │
│  Phase 4: Removal                                                 │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │  • Code removal from codebase                              │     │
│  │  • Last-chance data export available for 30 days           │     │
│  │  • Route table cleaned up                                  │     │
│  └────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────┘
```

## Types of Breaking Changes

```typescript
// Categorized breaking changes with migration strategies
interface BreakingChange {
  category: 'field_removal' | 'field_rename' | 'field_type_change' | 'behavior_change' | 'auth_requirement' | 'rate_limit_reduction';
  description: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  migrationStrategy: 'additive' | 'coexist' | 'flag_gated' | 'version_bump';
  autoMigrate: boolean; // Can gateway auto-transform?
}

const BREAKING_CHANGE_CATALOG: Record<string, BreakingChange> = {
  field_rename: {
    category: 'field_rename',
    description: 'Renaming a field (e.g., voice → voiceModel)',
    severity: 'medium',
    migrationStrategy: 'additive',
    autoMigrate: true, // Accept both old and new names
  },
  field_removal: {
    category: 'field_removal',
    description: 'Removing a field entirely',
    severity: 'high',
    migrationStrategy: 'coexist', // Keep field but ignore, warn
    autoMigrate: false,
  },
  behavior_change: {
    category: 'behavior_change',
    description: 'Changing default value or business logic',
    severity: 'high',
    migrationStrategy: 'flag_gated', // Feature flag to opt-in
    autoMigrate: false,
  },
};
```

## Feature Flags for Gradual Rollout

```typescript
interface FeatureFlag {
  key: string;
  name: string;
  description: string;
  tenantIds: string[];     // Specific tenants with access
  percentage?: number;      // Percentage rollout (0-100)
  isEnabled: boolean;
  dependsOn?: string[];     // Required flags
  expiresAt?: Date;         // Auto-cleanup date
}

// Feature flag middleware
async function featureFlagMiddleware(request: NextRequest, ctx: GatewayContext): Promise<NextResponse | null> {
  const flag = FEATURE_FLAGS.get(request.nextUrl.pathname);
  if (!flag) return null; // No flag required

  if (!flag.isEnabled) {
    return formatError('feature_disabled', 'This feature is not yet available', 404);
  }

  // Check tenant-specific access
  if (flag.tenantIds.length > 0 && !flag.tenantIds.includes(ctx.tenantId)) {
    return formatError('feature_disabled', 'This feature is not enabled for your tenant', 404);
  }

  // Percentage-based rollout
  if (flag.percentage && flag.percentage < 100) {
    const hash = hashTenant(ctx.tenantId);
    if (hash > flag.percentage) {
      return formatError('feature_disabled', 'This feature is in phased rollout', 404);
    }
  }

  return null; // Feature enabled, proceed
}
```

## Backward Compatibility Patterns

```typescript
// Pattern 1: Accept both old and new field names
interface AgentCreateV2 {
  name: string;
  voiceModel?: string;  // New name
  voice?: string;       // Old name (accepted, mapped)
}

function normalizeAgentInput(input: AgentCreateV2): NormalizedAgent {
  return {
    name: input.name,
    voiceModel: input.voiceModel ?? input.voice, // Prefer new, fallback to old
  };
}

// Pattern 2: Default preservation
// New defaults only apply to new resources; existing resources keep their values
function migrateDefaults(config: AgentConfig): AgentConfig {
  if (config.createdAt < new Date('2026-03-01')) {
    return config; // Preserve original behavior
  }
  return { ...config, temperature: config.temperature ?? 0.7 };
}

// Pattern 3: Sunset header on deprecated endpoints
async function deprecatedEndpoint(request: NextRequest): Promise<NextResponse> {
  const response = NextResponse.json({ ... });
  response.headers.set('Sunset', 'Sun, 30 Jun 2026 00:00:00 GMT');
  response.headers.set('Deprecation', 'true');
  response.headers.set('Link', '</docs/migration-v2>; rel="deprecation"');
  return response;
}
```

## Migration Guides

```typescript
// Structured migration guide data
interface MigrationGuide {
  fromVersion: string;
  toVersion: string;
  summary: string;
  breakingChanges: {
    what: string;
    why: string;
    impact: string;
    before: string; // Code example
    after: string;  // Code example
  }[];
  timeline: {
    deprecationDate: string;
    sunsetDate: string;
  };
  codemod?: string; // Automated migration script URL
}

// Example: v1 → v2 migration guide
const V1_TO_V2_GUIDE: MigrationGuide = {
  fromVersion: 'v1',
  toVersion: 'v2',
  summary: 'Agent configuration schema restructured for clarity and extensibility.',
  breakingChanges: [
    {
      what: 'Voice and temperature moved to voiceSettings object',
      why: 'Consolidate voice-related configuration',
      impact: 'Requests using flat voice/temperature fields will be rejected',
      before: `{ "voice": "alloy", "temperature": 0.7 }`,
      after: `{ "voiceSettings": { "model": "alloy", "temperature": 0.7 } }`,
    },
  ],
  timeline: {
    deprecationDate: '2026-03-01',
    sunsetDate: '2026-09-01',
  },
};
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Deprecation period | 6 months minimum | Industry standard, gives adequate migration time |
| Migration strategy | Additive changes first | Old and new coexist, clients migrate at their pace |
| Feature flags | In-house flag system | No external dependency, integrated with gateway |
| Sunset enforcement | 410 Gone | Clear signal, prevents silent breakage |
| Automated migration | Codemod scripts | Reduce manual effort for common migrations |

## Integration Points

- **Ch 07 (API Versioning)** — Breaking changes trigger new API version
- **Ch 07 (Documentation)** — Migration guides linked from sunset headers
- **Ch 10 (Security)** — Feature flags scoped to tenant authorization

## Production Considerations

- **Migration Analytics**: Track old-version API calls per tenant to identify migration stragglers
- **Automated Testing**: CI runs integration tests against all active versions with both old and new payloads
- **Client Notification**: Email + dashboard banner at T-90, T-30, T-7, and T-0 days
- **Codemod Validation**: Codemod scripts tested on real API traffic replay before release
- **Rate Limit During Migration**: Deprecated endpoints get stricter rate limits to encourage migration
