# Section 08: Schema Management and Evolution

## Overview

Schema management and evolution handles the lifecycle of event schemas in the analytics pipeline. As the platform evolves, new event types are added, existing events gain new fields, and occasionally fields are deprecated or removed. The schema management system ensures that all pipeline components (ingestion, stream processing, batch processing, data lake, data warehouse) remain consistent with the current schema while maintaining backward compatibility for historical data.

The schema registry is the central component, storing versioned JSON Schema and Avro schema definitions for every event type. All pipeline components reference the registry to validate, serialize, and deserialize events. Schema evolution follows strict backward compatibility rules: new schemas can add optional fields, add new enum values, and widen numeric types, but cannot remove or rename fields, make optional fields required, or change field types in incompatible ways.

## Architecture

```
   Schema Registry ← Producers → Events → Consumers
        |                              |
        v                              v
   Avro/JSON Schema               Data Lake Parquet
   Store                           Schema Evolution
```

## Design Decisions

- **Schema registry as a centralized service over embedded schemas:** The schema registry is a centralized service (with caching) that all pipeline components call to retrieve schemas. This ensures a single source of truth for event schemas. Producers fetch the latest schema before publishing; consumers cache schemas and invalidate on schema version change. The registry stores all schema versions, enabling evolution tracking and consumer migration planning. Trade-off: centralized registry is a single point of failure (mitigated by aggressive client caching) but provides consistent schema management across all components.

- **Avro for event bus serialization, Parquet for data lake, JSON Schema for validation over universal format:** Different layers use different schema formats optimized for their use case: Avro for Kafka event serialization (compact binary, schema embedded or referenced by ID), Parquet for data lake storage (columnar, compressed, schema evolution), and JSON Schema for the ingestion validation API (developer-friendly, runtime validation). The schema registry maintains all three representations for each event type. Trade-off: multi-format support requires schema format converters but uses each format optimally.

- **Forward compatibility required for consumer upgrades:** New schema versions must be forward-compatible — consumers running the old schema version must be able to read events written with the new schema version. This is achieved by following Avro's schema evolution rules: new fields must have defaults, field types can only be widened, and enum values can only be added. Breaking changes require a new major version and a migration period where both old and new schemas exist simultaneously. Trade-off: forward compatibility restricts schema evolution but enables independent upgrade of producers and consumers.

## Implementation Approach

```
class SchemaRegistryService {
  private schemas: Map<string, SchemaEntry[]>;
  private cache: Map<string, SchemaEntry>;
  private avroParser: AvroParser;

  async registerSchema(eventType: string, schema: SchemaDefinition): Promise<SchemaEntry> {
    const existing = await this.db.schemas.find({ eventType }).sort({ version: -1 }).limit(1).toArray();
    const latestVersion = existing[0]?.version || '0.0.0';

    // Validate compatibility
    if (existing[0]) {
      const compatResult = await this.checkCompatibility(existing[0].schema, schema);
      if (!compatResult.compatible) {
        throw new SchemaError(`Schema incompatible: ${compatResult.reasons.join(', ')}`);
      }
    }

    const newVersion = this.bumpVersion(latestVersion, schema.changeType);
    const entry: SchemaEntry = {
      eventType,
      version: newVersion,
      schema,
      avroSchema: this.convertToAvro(schema),
      parquetSchema: this.convertToParquet(schema),
      createdAt: new Date(),
      status: 'active',
    };

    await this.db.schemas.insert(entry);
    this.cache.delete(eventType); // Invalidate cache

    logger.info('Schema registered', { eventType, version: newVersion });
    return entry;
  }

  async getSchema(eventType: string, version?: string): Promise<SchemaEntry> {
    const cacheKey = `${eventType}:${version || 'latest'}`;
    const cached = this.cache.get(cacheKey);
    if (cached) return cached;

    const entry = version
      ? await this.db.schemas.findOne({ eventType, version })
      : await this.db.schemas.findOne({ eventType, status: 'active' }).sort({ version: -1 });

    if (!entry) throw new SchemaError(`Schema not found: ${eventType}@${version || 'latest'}`);

    this.cache.set(cacheKey, entry);
    return entry;
  }

  async checkCompatibility(oldSchema: any, newSchema: any): Promise<CompatibilityResult> {
    const reasons: string[] = [];

    // Compare required fields
    const oldRequired = new Set(oldSchema.required || []);
    const newRequired = new Set(newSchema.required || []);
    const removedRequired = [...oldRequired].filter(f => !newRequired.has(f));
    if (removedRequired.length > 0) {
      reasons.push(`Required fields removed: ${removedRequired.join(', ')}`);
    }

    const newAddedRequired = [...newRequired].filter(f => !oldRequired.has(f));
    if (newAddedRequired.length > 0) {
      reasons.push(`New required fields added: ${newAddedRequired.join(', ')}`);
    }

    // Compare field properties
    const oldProps = this.indexProperties(oldSchema.properties || {});
    const newProps = this.indexProperties(newSchema.properties || {});

    for (const [fieldName, oldProp] of Object.entries(oldProps)) {
      const newProp = newProps[fieldName];
      if (!newProp) {
        reasons.push(`Field removed: ${fieldName}`);
        continue;
      }

      // Type change check (widening allowed: int32 → int64, float → double)
      if (oldProp.type !== newProp.type) {
        if (!this.isTypeWidening(oldProp.type, newProp.type)) {
          reasons.push(`Field type changed incompatibly: ${fieldName} ${oldProp.type} → ${newProp.type}`);
        }
      }

      // Enum value removal
      if (oldProp.enum && newProp.enum) {
        const removedValues = oldProp.enum.filter((v: string) => !newProp.enum.includes(v));
        if (removedValues.length > 0) {
          reasons.push(`Enum values removed from ${fieldName}: ${removedValues.join(', ')}`);
        }
      }
    }

    return {
      compatible: reasons.length === 0,
      reasons,
      changeType: reasons.length > 0 ? 'major' :
        newAddedRequired.length > 0 ? 'minor' : 'patch',
    };
  }

  private convertToAvro(jsonSchema: any): any {
    // JSON Schema to Avro schema conversion
    const avroSchema: any = {
      type: 'record',
      name: this.toAvroName(jsonSchema.title || 'Event'),
      namespace: 'com.voiceagent.events',
      fields: [],
    };

    for (const [name, prop] of Object.entries(jsonSchema.properties || {})) {
      const field: any = {
        name,
        type: this.jsonSchemaTypeToAvro(prop, jsonSchema.required?.includes(name)),
      };
      if (prop.description) field.doc = prop.description;
      avroSchema.fields.push(field);
    }

    return avroSchema;
  }

  private jsonSchemaTypeToAvro(prop: any, required: boolean): any {
    const typeMap: Record<string, string> = {
      string: 'string',
      integer: 'long',
      number: 'double',
      boolean: 'boolean',
      object: 'record',
      array: { type: 'array', items: this.jsonSchemaTypeToAvro(prop.items || {}, true) },
    };

    const avroType = typeMap[prop.type] || 'string';
    return required ? avroType : ['null', avroType];
  }

  // Request schema version for a specific consumer
  async pinConsumerSchema(consumerId: string, eventType: string, version: string): Promise<void> {
    await this.db.consumerSchemaPins.insert({
      consumerId,
      eventType,
      version,
      pinnedAt: new Date(),
    });
  }

  async getConsumerSchema(consumerId: string, eventType: string): Promise<SchemaEntry> {
    const pin = await this.db.consumerSchemaPins.findOne({ consumerId, eventType });
    if (pin) return this.getSchema(eventType, pin.version);
    return this.getSchema(eventType); // Latest
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Confluent Schema Registry (Confluent) | Server | Avro schema registry |
| Apicurio (Apache 2.0) | Server | Schema registry alternative |
| AVSC (MIT) | Node.js | Avro schema manipulation |

## Production Considerations

**Scaling:** Schema registry operations are low-frequency (schema registrations: daily/weekly, schema reads: per-event). Cache aggressively at the consumer side — schemas rarely change. Schema registry should be highly available (at least 2 replicas) and maintain an audit log of all schema changes. Database-backed storage with in-memory cache provides adequate performance (schema reads are sub-millisecond from cache).

**Security:** Schema registry write access should be restricted to service accounts (not end users). Validate schema definitions for security concerns (no $ref external URLs, no executable fields). Schema registry public read access exposes platform data models — consider authenticated read access for production deployments.

**Monitoring:** Track schema registration rate, schema version count per event type, consumer schema pin distribution (which versions consumers are using), deprecated schema usage, and schema validation errors at ingestion. Alert on breaking schema registration attempts (catch configuration errors early), consumers still using deprecated schemas near sunset dates, and schema fetch failures.
