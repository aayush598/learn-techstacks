# Section 06: Request/Response Transformation

## Overview

Request/response transformation handles the mapping between the platform's internal domain data model and the external API's data format. Every external system has its own data model, field naming conventions, data types, nesting structures, and serialization formats (JSON, XML, form-encoded). The transformation layer provides bidirectional mapping between these divergent representations, enabling the platform to work with a consistent internal data model while connecting to diverse external APIs.

Transformations cover field-level mappings (firstName → FirstName), type coercions (string dates → Date objects, number strings → integers), structural transformations (flatten nested objects, expand flat objects into nested), value transformations (gender codes: "M"/"F" → "male"/"female"), computed fields (fullName = firstName + lastName), conditional mappings (field A is mapped if present, otherwise field B), and default values for missing fields. Transformations are defined declaratively as mapping schemas rather than imperatively as code, enabling non-developers to configure integrations.

## Architecture

```
                  Request/Response Transformation Pipeline

   Request (Platform → External API)              Response (External API → Platform)
   ==========================================     ==========================================
   +------------------+                         +------------------+
   | Platform Object  |                         | API Response     |
   | {                |                         | {                |
   |   firstName,     |                         |   FirstName,     |
   |   lastName,      |                         |   LastName,      |
   |   email,         |                         |   Email,         |
   |   phone          |                         |   Phone_Number   |
   | }                |                         | }                |
   +------------------+                         +------------------+
          |                                               |
          v                                               v
   +------------------+                         +------------------+
   | Transformation   |                         | Transformation   |
   | Pipeline         |                         | Pipeline         |
   | 1. Field mapping |                         | 1. Field mapping |
   | 2. Type coercion |                         | 2. Type coercion |
   | 3. Value transform|                         | 3. Value transform|
   | 4. Default apply |                         | 4. Validation    |
   | 5. Serialize     |                         | 5. Parse         |
   +------------------+                         +------------------+
          |                                               |
          v                                               v
   +------------------+                         +------------------+
   | API Request      |                         | Platform Object  |
   | {                |                         | {                |
   |   FirstName,     |                         |   firstName,     |
   |   LastName,      |                         |   lastName,      |
   |   Email,         |                         |   email,         |
   |   Phone_Number   |                         |   phone          |
   | }                |                         | }                |
   +------------------+                         +------------------+
```

## Design Decisions

- **Declarative mapping schemas over imperative transformation code:** Transformations are defined as JSON/YAML mapping schemas that specify field-to-field mappings, type conversions, and value transformations. The framework interprets these schemas at runtime to execute transformations. This enables integration configuration without code changes and supports visual mapping tools. Trade-off: declarative mapping has limitations for complex conditional or computed transformations that require custom code extensions.

- **Schema-driven validation on both request and response paths:** Outgoing requests are validated against the API's expected schema before sending (catching mapping errors early). Incoming responses are validated against the expected response schema before processing (catching API changes or unexpected data). Validation uses JSON Schema or TypeScript interfaces at compile time and Zod at runtime. Trade-off: dual validation increases processing time per request by 1-5ms but catches errors at the earliest possible point.

- **Transformation versioning with backward compatibility:** Mapping schemas are versioned alongside adapter versions. When an API changes its data model, a new mapping version is created while the old version continues to work for existing configurations. The framework selects the appropriate mapping version based on the integration configuration. Trade-off: maintaining multiple mapping versions increases storage and complexity but enables safe upgrades.

## Implementation Approach

```
interface FieldMapping {
  sourceField: string;
  targetField: string;
  type: 'direct' | 'coerce' | 'transform' | 'computed' | 'conditional';
  sourceType?: 'string' | 'number' | 'boolean' | 'date' | 'object' | 'array';
  targetType?: 'string' | 'number' | 'boolean' | 'date' | 'object' | 'array';
  defaultValue?: any;
  transform?: (value: any, context: TransformContext) => any;
  condition?: (context: TransformContext) => boolean;
}

interface MappingSchema {
  name: string;
  version: number;
  direction: 'request' | 'response';
  fieldMappings: FieldMapping[];
  validation?: Record<string, any>;  // JSON Schema validation rules
}

class TransformationEngine {
  async transform<T>(input: T, schema: MappingSchema, context: TransformContext): Promise<any> {
    const output = {};
    for (const mapping of schema.fieldMappings) {
      if (mapping.condition && !mapping.condition(context)) continue;

      const value = this.resolveValue(input, mapping, context);
      if (value === undefined && mapping.defaultValue !== undefined) {
        output[mapping.targetField] = mapping.defaultValue;
      } else if (value !== undefined) {
        output[mapping.targetField] = value;
      }
    }
    return output;
  }

  private resolveValue(input: any, mapping: FieldMapping, context: TransformContext): any {
    const raw = this.getNestedValue(input, mapping.sourceField);

    switch (mapping.type) {
      case 'direct':
        return raw;
      case 'coerce':
        return this.coerceType(raw, mapping.sourceType, mapping.targetType);
      case 'transform':
        return mapping.transform(raw, context);
      case 'computed':
        return mapping.transform(input, context);  // Full object access
      case 'conditional':
        return mapping.condition(context) ? raw : undefined;
      default:
        return raw;
    }
  }

  private coerceType(value: any, fromType: string, toType: string): any {
    if (fromType === 'string' && toType === 'number') return Number(value);
    if (fromType === 'string' && toType === 'date') return new Date(value);
    if (fromType === 'number' && toType === 'string') return String(value);
    return value;
  }

  private getNestedValue(obj: any, path: string): any {
    return path.split('.').reduce((current, key) => current?.[key], obj);
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Zod** (MIT) | Validation | Schema validation |
| **jsonata** (MIT) | Transformation | JSON query and transformation |
| **jmespath** (MIT) | Query | JSON query language |
| **lodash** (MIT) | Utilities | Object manipulation |

## Production Considerations

**Scaling:** Transformation is CPU-bound and scales with request volume. Pre-compile mapping schemas into optimized transformation functions at adapter initialization time rather than interpreting schemas on each request. Cache compiled transformations in memory. For large payloads (1000+ fields), use streaming transforms to avoid memory pressure.

**Security:** Validate all transformed data before sending to external APIs to prevent injection attacks (no raw string concatenation in GraphQL queries or SOAP XML). Sanitize input from external APIs to prevent data injection into the platform. Never log raw transformed payloads that may contain PII or sensitive data.

**Monitoring:** Track transformation success rate, average transformation time per request, schema validation failure rate, and field mapping coverage (% of fields successfully mapped). Alert on transformation failures > 1% (may indicate API schema change) and validation failures > 5% (may indicate mapping configuration error).
