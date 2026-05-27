# Section 03: Event Schema and Versioning

## Overview

Event schema and versioning management defines the structure, evolution, and lifecycle of webhook event payloads in the voice agent platform. Every event type (call.completed, payment.succeeded, agent.status_changed) has an associated JSON Schema that describes the payload structure, field types, required fields, and validation rules. Schema versioning enables the platform to evolve event payloads over time without breaking existing consumers.

The schema management system covers the complete event lifecycle: schema definition and registration, version creation (major/minor/patch), backward compatibility validation, consumer endpoint registration against specific schema versions, schema deprecation, and eventual retirement. The system provides a schema registry that consumers can query to discover available event types and their schemas, and a schema validator that ensures all emitted events conform to their registered schema before delivery.

## Architecture

```
                 Event Schema & Versioning

   Schema Registry ← Schema Validator → Webhook Engine → Consumers
                        |
   +----------------------------------------------------------+
   |              Schema Management System                    |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | Schema Registry  |  | Version Manager   |            |
   |  | • Event types    |  | • Major releases   |            |
   |  | • JSON Schema    |  | • Minor additions  |            |
   |  | • Changelog      |  | • Patch fixes      |            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Compatibility    |  | Consumer Registry |             |
   |  | • Backward check |  | • Endpoint →      |            |
   |  | • Breaking       |  |   schema versions |            |
   |  |   detection      |  | • Migrate status  |            |
   |  | • Migration guide|  | • Sunset tracking  |            |
   |  +------------------+  +-------------------+            |
   +----------------------------------------------------------+
```

## Design Decisions

- **JSON Schema Draft 2020-12 over Protobuf/Thrift:** JSON Schema is self-describing (schema documents are JSON), widely supported across programming languages, and can validate payloads at runtime. While Protobuf offers smaller payloads and stronger typing, JSON Schema provides better developer experience for webhook consumers (they can read the schema directly and use it to generate client code). Trade-off: JSON Schema payloads are larger than binary formats but provide human-readable documentation and wider tooling support.

- **Semantic versioning with backward-compatible minor bumps:** Event schemas follow semver: major version for breaking changes (field removal, type changes), minor version for backward-compatible additions (new optional fields, new enum values), patch for fixes (schema documentation, constraints tightening). The schema registry rejects schemas that violate backward compatibility rules (e.g., removing a required field is a breaking change only permitted in major versions). Trade-off: semver adds version management overhead but provides clear consumer migration expectations.

- **Consumer-pinned version resolution over automatic upgrade:** Each webhook endpoint registers the specific schema version(s) it supports. The webhook engine delivers events using the schema version the consumer registered for. If no version is specified, the latest major version is used. This allows consumers to upgrade on their schedule — they receive events in their chosen version format until they explicitly migrate. Trade-off: pinning requires consumers to explicitly update their registration when migrating but prevents unexpected breaking changes from disrupting production consumers.

## Implementation Approach

```
interface EventSchema {
  eventType: string;
  version: string;              // "1.2.0"
  description: string;
  schema: JSONSchema;           // Draft 2020-12 schema
  deprecated?: boolean;
  deprecationMessage?: string;
  sunsetDate?: string;
  changelog: ChangelogEntry[];
}

interface SchemaCompatibilityResult {
  compatible: boolean;
  breakingChanges: string[];
  newOptionalFields: string[];
  warnings: string[];
}

class SchemaRegistry {
  private schemas = new Map<string, EventSchema[]>();

  async registerSchema(eventType: string, schema: EventSchema): Promise<void> {
    const existing = this.schemas.get(eventType) || [];
    const latest = existing[existing.length - 1];

    if (latest) {
      const compatibility = this.checkCompatibility(latest, schema);
      if (!compatibility.compatible) {
        throw new Error(
          `Schema incompatible: ${compatibility.breakingChanges.join(', ')}`
        );
      }
    }

    existing.push(schema);
    this.schemas.set(eventType, existing);
    await this.db.eventSchemas.insert(schema);
    logger.info(`Schema registered: ${eventType}@${schema.version}`);
  }

  getSchema(eventType: string, version?: string): EventSchema | undefined {
    const existing = this.schemas.get(eventType);
    if (!existing || existing.length === 0) return undefined;

    if (version) {
      return existing.find(s => s.version === version);
    }

    // Return latest non-deprecated
    const active = existing.filter(s => !s.deprecated);
    return active[active.length - 1];
  }

  getLatestMajorVersion(eventType: string, majorVersion: number): EventSchema | undefined {
    const existing = this.schemas.get(eventType);
    if (!existing) return undefined;
    const majorVersions = existing.filter(s => s.version.startsWith(`${majorVersion}.`));
    return majorVersions[majorVersions.length - 1];
  }

  async validateEvent(eventType: string, payload: Record<string, any>): Promise<ValidationResult> {
    const schema = this.getSchema(eventType);
    if (!schema) {
      return { valid: false, errors: [`Unknown event type: ${eventType}`] };
    }

    const validator = new AJV({ draft: '2020-12' });
    const valid = validator.validate(schema.schema, payload);

    if (!valid) {
      return { valid: false, errors: validator.errors?.map(e => `${e.instancePath} ${e.message}`) || [] };
    }

    return { valid: true, errors: [] };
  }

  checkCompatibility(oldSchema: EventSchema, newSchema: EventSchema): SchemaCompatibilityResult {
    const breakingChanges: string[] = [];
    const newOptionalFields: string[] = [];
    const warnings: string[] = [];

    const oldProps = this.flattenProperties(oldSchema.schema);
    const newProps = this.flattenProperties(newSchema.schema);

    for (const [path, prop] of Object.entries(oldProps)) {
      const newProp = newProps[path];

      if (!newProp) {
        breakingChanges.push(`Removed field: ${path}`);
        continue;
      }

      // Check type change
      if (prop.type !== newProp.type && prop.type !== undefined) {
        breakingChanges.push(`Type changed for ${path}: ${prop.type} → ${newProp.type}`);
      }

      // Check required → not required (backward-compatible relaxation)
      // Not required → required is breaking
      if (!prop.required && newProp.required) {
        breakingChanges.push(`Field ${path} became required`);
      }

      // Enum values removed
      if (prop.enum && newProp.enum) {
        const removed = prop.enum.filter((v: string) => !newProp.enum!.includes(v));
        if (removed.length > 0) {
          breakingChanges.push(`Enum values removed from ${path}: ${removed.join(', ')}`);
        }
      }
    }

    // New fields — check if they are optional (minor) or required (breaking)
    for (const [path, prop] of Object.entries(newProps)) {
      if (!oldProps[path]) {
        if (prop.required) {
          breakingChanges.push(`New required field: ${path}`);
        } else {
          newOptionalFields.push(path);
        }
      }
    }

    // Minor version: only new optional fields
    // Major version: breaking changes allowed
    const isMajor = !breakingChanges.length || newSchema.version.split('.')[0] !== oldSchema.version.split('.')[0];

    if (breakingChanges.length > 0 && !isMajor) {
      warnings.push(`Breaking changes should result in a major version bump`);
    }

    return {
      compatible: breakingChanges.length === 0 || isMajor,
      breakingChanges,
      newOptionalFields,
      warnings,
    };
  }

  async deprecateSchema(eventType: string, version: string, sunsetDate: Date): Promise<void> {
    const schema = this.getSchema(eventType, version);
    if (!schema) throw new Error(`Schema ${eventType}@${version} not found`);

    schema.deprecated = true;
    schema.deprecationMessage = `Deprecated in favor of ${this.getLatestMajorVersion(eventType, parseInt(version.split('.')[0]) + 1)?.version}`;
    schema.sunsetDate = sunsetDate.toISOString();

    await this.db.eventSchemas.update(schema);
    await this.notifyConsumers(eventType, version, schema);
  }
}

// Example: call.completed event schema v1.0.0
const callCompletedSchemaV1: EventSchema = {
  eventType: 'call.completed',
  version: '1.0.0',
  description: 'Emitted when a voice call is completed',
  schema: {
    $schema: 'https://json-schema.org/draft/2020-12/schema',
    type: 'object',
    required: ['callSid', 'duration', 'status', 'completedAt'],
    properties: {
      callSid: { type: 'string', description: 'Unique call identifier' },
      duration: { type: 'integer', minimum: 0, description: 'Call duration in seconds' },
      status: { type: 'string', enum: ['completed', 'failed', 'busy', 'no-answer', 'canceled'] },
      completedAt: { type: 'string', format: 'date-time' },
      customerPhone: { type: 'string', pattern: '^\\+[1-9]\\d{1,14}$' },
      agentId: { type: 'string' },
      recordingUrl: { type: 'string', format: 'uri' },
      metadata: { type: 'object' },
    },
  },
  changelog: [{ version: '1.0.0', date: '2026-01-15', description: 'Initial release' }],
};
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| AJV (MIT) | Node.js | JSON Schema validation |
| JSONSchema built-ins (MIT) | Node.js | Schema manipulation |
| Semver (ISC) | Node.js | Version comparison |

## Production Considerations

**Scaling:** Schema registration is a rare operation (events per schema lifecycle: weeks to months). Schema validation is per-event — ensure AJV compilation results are cached (compile once per schema, reuse for all events of that type). The schema registry should be read-optimized with in-memory cache and database fallback. Schema changes trigger consumer notifications — batch notifications to avoid email/SMS API rate limits.

**Security:** Event schemas can reveal platform data models — control write access to schema registration (admin only). Validate that schemas do not contain executable code (JSON Schema `$comment` and `examples` fields should be sanitized). Consumer registration should verify the requested schema version exists and is not deprecated (prevent consumers from unknowingly registering against a deprecated version).

**Monitoring:** Track schema versions in use across all endpoints, deprecation timeline adherence (schemas deprecated on schedule), validation failure rate (events that fail schema validation before delivery), and consumer migration progress. Alert on high schema validation failure rates (indicates a platform bug or schema drift) and consumers still on deprecated versions near the sunset date.
