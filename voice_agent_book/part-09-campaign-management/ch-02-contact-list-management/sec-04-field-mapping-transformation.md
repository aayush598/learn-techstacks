# Section 04: Field Mapping & Transformation

## Overview

Field mapping bridges the gap between source data formats and the system's internal contact schema. When users import contacts from CSV files, CRMs, or APIs, the source column names rarely match the system's field names. The mapping system provides auto-detection of source-to-target field correspondences, a UI for manual override, and transformation rules for data normalization (date formatting, phone number standardization, case conversion, etc.).

A robust field mapping system reduces import friction dramatically. Instead of requiring users to reformat their data before import, the system handles common variations automatically. The mapper supports default values for missing fields, concatenation of multiple source fields into one target field, and custom transformation functions for complex conversions.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Audio    |--->| WebSocket|--->| Jitter   |--->| PLC      |--->| Player   |
| Producer |    | (WSS)    |    | Buffer   |    | (Packet  |    | (smooth  |
| (100ms   |    | (binary) |    | (adaptive|    |  Loss    |    |  output) |
|  chunks) |    |          |    |  60-200) |    |  Conceal)|    +----------+
+----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```
class FieldMapper {
  constructor(systemFields, aliasDictionary) {
    this.systemFields = systemFields;
    this.aliases = aliasDictionary;
    this.transformer = new TransformationEngine();
  }

  autoMap(sourceColumns) {
    const mappings = {};

    for (const sourceCol of sourceColumns) {
      const normalized = sourceCol.toLowerCase().replace(/[\s_-]/g, '');
      
      // Check direct match
      const directMatch = this.systemFields.find(
        f => f.name.toLowerCase() === normalized
      );
      if (directMatch) {
        mappings[sourceCol] = { field: directMatch.name, confidence: 1.0 };
        continue;
      }

      // Check alias dictionary
      const aliasMatch = this.aliases[normalized];
      if (aliasMatch) {
        mappings[sourceCol] = { field: aliasMatch, confidence: 0.95 };
        continue;
      }

      // Fuzzy match
      const fuzzyMatches = this.systemFields
        .map(f => ({
          field: f.name,
          score: this.stringSimilarity(normalized, f.name.toLowerCase())
        }))
        .filter(m => m.score > 0.6)
        .sort((a, b) => b.score - a.score);

      if (fuzzyMatches.length > 0) {
        mappings[sourceCol] = {
          field: fuzzyMatches[0].field,
          confidence: fuzzyMatches[0].score
        };
      }
    }

    return mappings;
  }

  async applyTransformations(contact, mappedFields, transformations) {
    const result = {};

    for (const [targetField, sourceCol] of Object.entries(mappedFields)) {
      let value = contact[sourceCol];
      
      const transform = transformations[targetField];
      if (transform) {
        value = await this.transformer.apply(value, transform, contact);
      }

      result[targetField] = value;
    }

    return result;
  }
}

class TransformationEngine {
  registry = {
    'phone_e164': (v) => this.toE164(v),
    'date_iso': (v) => new Date(v).toISOString(),
    'uppercase': (v) => v?.toUpperCase(),
    'lowercase': (v) => v?.toLowerCase(),
    'trim': (v) => v?.trim(),
    'concat': (v, config, row) => {
      const parts = config.fields.map(f => row[f] || '');
      return parts.join(config.separator || ' ');
    },
    'default': (v, config) => v || config.defaultValue,
    'custom': async (v, config, row) => {
      // Sandboxed JavaScript function execution
      return this.executeSandboxed(config.fn, { value: v, row });
    }
  };

  async apply(value, transformConfig, row) {
    const fn = this.registry[transformConfig.type];
    if (!fn) throw new Error(`Unknown transform: ${transformConfig.type}`);
    return fn(value, transformConfig, row);
  }
}
```

## Integration Points

- **CSV Import Pipeline (sec-01):** Field mapping runs after header detection, before validation
- **API Import (sec-02):** API import uses the same mapping logic but typically skips auto-mapping
- **CRM Integration (Part 10, Ch 02):** CRM field mapping uses the same system field definitions
- **Contact Service:** Mapped fields populate the contact record
- **UI Component:** Drag-and-drop mapping interface in the campaign configuration screen

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Auto-mapping confidence below 0.8 should require user confirmation before import proceeds
- Store per-tenant mapping history in PostgreSQL for personalized auto-mapping improvement
- Custom transformation functions must be sandboxed to prevent server-side code injection
- Mapping errors should be reported clearly — "Could not map 'ph' to any known field"
- Preview first 20 rows with applied mappings before full import commit
- Support template-based mappings — save and reuse common mapping configurations
- Test mappings with a small sample before processing the full import
- Log mapping decisions for debugging and user support
- Internationalization — field names and mapping UI should be localized for non-English users
- Provide a reset-to-defaults option for mapping when auto-detection is incorrect
