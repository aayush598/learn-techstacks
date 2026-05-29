# Section 06: API Changelog & Versioning

## Overview

The API changelog documents all changes to the API — new endpoints, deprecated features, breaking changes, and bug fixes. The changelog is auto-generated from git commits and OpenAPI spec diffs. Migration guides detail steps for upgrading between versions.

## Architecture

```
Changelog Generation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Git Commits] → [Conventional Commits Parser] → [Changelog Entries]
[OpenAPI Spec] → [Spec Diff] → [Breaking Change Detection]
                      │
                 [Changelog.md]
                      │
                 [Developer Portal]
                      │
              ┌───────┴───────┐
              │               │
       [Versioned List]  [RSS Feed]
              │
     ┌────────┴────────┐
     │                  │
  v2.1.0 (current)   v2.0.0
     │                  │
  + New analytics    + Breaking: Agent
    endpoints          create request
  + Deprecated         changed
    v1 agents          + Migration guide
    create             for v1→v2

Changelog Format:
  # Changelog

  ## [2.1.0] - 2025-06-01

  ### Added
  - New `analytics` endpoints for call metrics
  - Support for custom voice parameters
  - Pagination cursor in list responses

  ### Deprecated
  - `POST /v1/agents` — use `POST /v2/agents`
  - Field `voice.provider` string — use enum

  ## [2.0.0] - 2025-05-01

  ### ⚠️ Breaking Changes
  - Agent creation request schema changed
  - Pagination now uses cursor, not offset
  - Rate limit headers renamed

  ### Migration Guide
  See [v1 → v2 Migration Guide](/docs/migration/v1-to-v2)
```

## Design Decisions

- **Conventional Commits**: Changelog auto-generated from commit messages
- **OpenAPI Diff**: Breaking changes detected by comparing OpenAPI specs
- **Deprecation Policy**: Features deprecated for minimum 6 months before removal
- **Migration Guides**: Written for each breaking change; linked from changelog entries

## Implementation Approach

```typescript
// Changelog generator
interface ChangelogEntry {
  version: string;
  date: Date;
  sections: {
    added?: string[];
    changed?: string[];
    deprecated?: string[];
    removed?: string[];
    fixed?: string[];
    security?: string[];
  };
  migrationGuide?: string;
}

class ChangelogGenerator {
  async generate(fromVersion: string, toVersion: string): Promise<ChangelogEntry> {
    const commits = await this.getCommitsSince(fromVersion);
    const oldSpec = await this.getSpec(fromVersion);
    const newSpec = await this.getSpec(toVersion);
    const breakingChanges = this.detectBreakingChanges(oldSpec, newSpec);

    return {
      version: toVersion,
      date: new Date(),
      sections: {
        added: this.filterByType(commits, 'feat'),
        changed: this.filterByType(commits, 'change'),
        deprecated: this.filterByType(commits, 'deprecate'),
        fixed: this.filterByType(commits, 'fix'),
        security: this.filterByType(commits, 'security'),
        removed: [...breakingChanges.removed, ...this.filterByType(commits, 'remove')],
      },
      migrationGuide: breakingChanges.hasBreakingChanges
        ? `/docs/migration/v${fromVersion}-to-v${toVersion}`
        : undefined,
    };
  }

  private detectBreakingChanges(oldSpec: Spec, newSpec: Spec): BreakingChanges {
    const changes: BreakingChanges = {
      hasBreakingChanges: false,
      removed: [],
      changed: [],
    };

    // Check for removed paths
    for (const path of Object.keys(oldSpec.paths)) {
      if (!newSpec.paths[path]) {
        changes.removed.push(`Removed endpoint: ${path}`);
        changes.hasBreakingChanges = true;
      }
    }

    // Check for changed request schemas
    for (const [path, pathItem] of Object.entries(newSpec.paths)) {
      for (const [method, operation] of Object.entries(pathItem)) {
        const oldOp = oldSpec.paths[path]?.[method];
        if (!oldOp) continue;

        // Check for required parameter changes
        const oldRequired = this.getRequiredParams(oldOp);
        const newRequired = this.getRequiredParams(operation);
        const added = newRequired.filter(p => !oldRequired.includes(p));

        if (added.length > 0) {
          changes.changed.push(`New required parameter in ${method.toUpperCase()} ${path}: ${added.join(', ')}`);
          changes.hasBreakingChanges = true;
        }
      }
    }

    return changes;
  }

  private filterByType(commits: Commit[], type: string): string[] {
    return commits
      .filter(c => c.type === type)
      .map(c => `- ${c.description}`);
  }
}

// Version deprecation notices
function getVersionStatus(version: string): 'current' | 'deprecated' | 'sunset' {
  const versions = {
    'v1': { sunset: new Date('2026-06-01'), status: 'deprecated' as const },
    'v2': { sunset: new Date('2027-06-01'), status: 'current' as const },
  };

  return versions[version]?.status || 'deprecated';
}

// Migration guide generator
class MigrationGuideGenerator {
  generateV1ToV2(): string {
    return `
# Migrating from v1 to v2

## Breaking Changes

### 1. Agent Creation Request

**v1 (old):**
\`\`\`json
POST /v1/agents
{
  "name": "Agent",
  "voice_provider": "elevenlabs",
  "voice_id": "abc123"
}
\`\`\`

**v2 (new):**
\`\`\`json
POST /v2/agents
{
  "name": "Agent",
  "voice": {
    "provider": "elevenlabs",
    "voiceId": "abc123"
  }
}
\`\`\`

### 2. Pagination

Cursor-based pagination replaces offset-based.

**v1:** \`?offset=20&limit=20\`
**v2:** \`?cursor=abc123&limit=20\`

### 3. Rate Limit Headers

Headers renamed for consistency.

| v1 | v2 |
|---|---|
| X-Rate-Limit | X-RateLimit-Limit |
| X-Rate-Remaining | X-RateLimit-Remaining |

## Timeline
- v1 current until June 2026
- v1 deprecation warnings started May 2025
- v1 sunset: June 2026
    `;
  }
}
```

## Integration Points

- **Developer Portal**: Changelog page with version filter and RSS feed
- **CI/CD**: Changelog auto-generated on release; posted to changelog page
- **API Response Headers**: `Sunset` header on deprecated endpoints

## Production Considerations

- **Deprecation Communication**: Email notification 6 months before breaking changes
- **Migration Support**: Dedicated migration support for enterprise customers
- **Legacy Version Availability**: Deprecated versions available for 12 months after deprecation
- **API Version Analytics**: Track version adoption to understand migration progress

## Open-Source Tools

- **git-cliff**: Changelog generation from conventional commits
- **openapi-diff**: Breaking change detection in OpenAPI specs
- **Keep a Changelog**: Changelog format standard
