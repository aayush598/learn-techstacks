# Section 02: Template Variables & Data Sources

## Overview

Template variables are the dynamic elements that make each call unique and personalized. They draw data from multiple sources — contact fields, campaign configuration, CRM records, computed values, and external API responses. The variable system resolves values at render time, handling missing data with fallbacks, formatting for natural speech, and ensuring data freshness through configurable caching strategies.

The data source architecture provides a unified interface for accessing variables from disparate systems. Each data source implements a resolver interface that handles fetching, caching, and error handling. The system supports hierarchical variable paths (e.g., `contact.address.city`) and computed variables (e.g., `{{daysSinceLastContact}}`) that derive from other data. Variable sources are ordered by priority, with higher-priority sources overriding lower ones.

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
class VariableResolver {
  constructor(sourceRegistry, cache) {
    this.sources = sourceRegistry;
    this.cache = cache;
    this.computedRegistry = new Map();
  }

  async resolve(variablePath, context, options = {}) {
    const cacheKey = `var:${variablePath}:${context.callSid}`;
    
    // Check per-call cache
    if (!options.bypassCache) {
      const cached = this.cache.get(cacheKey);
      if (cached) return cached;
    }

    // Parse variable path
    const { source, field } = this.parsePath(variablePath);

    // Resolve from appropriate source
    const sourceResolver = this.sources.get(source);
    if (!sourceResolver) {
      return options.fallback || this.createFallback(variablePath);
    }

    try {
      const value = await sourceResolver.resolve(field, context);
      const formatted = this.formatForSpeech(value, options.format);
      
      this.cache.set(cacheKey, formatted, this.getCacheTTL(source));
      return formatted;
    } catch (error) {
      // Fallback on error
      return options.fallback || this.createFallback(variablePath, error);
    }
  }

  parsePath(path) {
    const parts = path.split('.');
    return {
      source: parts[0], // e.g., "contact", "crm", "campaign"
      field: parts.slice(1).join('.'), // e.g., "address.city"
    };
  }

  formatForSpeech(value, format) {
    if (value === null || value === undefined) return '';

    switch (typeof value) {
      case 'number':
        if (format === 'currency') return this.numberToWords(Math.round(value));
        if (format === 'ordinal') return this.toOrdinal(value);
        return this.numberToWords(value);
      case 'object':
        if (value instanceof Date) return this.formatDate(value, format);
        return JSON.stringify(value);
      default:
        return String(value);
    }
  }

  numberToWords(num) {
    // Convert numbers to natural speech
    // 1234 → "one thousand two hundred thirty-four"
    // For voice, this is more natural than "one two three four"
    if (num < 0 || num > 999999) return String(num);
    // ... (implementation uses ones/tens/hundreds/thousands tables)
    return this.convertNumber(num);
  }

  formatDate(date, format) {
    if (format === 'relative') {
      const diff = Date.now() - date.getTime();
      const days = Math.floor(diff / 86400000);
      if (days === 0) return 'today';
      if (days === 1) return 'yesterday';
      if (days < 30) return `${days} days ago`;
    }
    
    return date.toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }

  getCacheTTL(source) {
    const ttls = {
      contact: 86400, // 24 hours
      campaign: 86400, // 24 hours
      crm: 300, // 5 minutes
      computed: 0, // No cache — recompute on every call
      call: 0 // Immutable for call duration
    };
    return ttls[source] || 60;
  }
}

// Contact Data Source
class ContactDataSource {
  constructor(contactService) {
    this.contacts = contactService;
  }

  async resolve(field, context) {
    const contact = await this.contacts.getById(context.contactId);
    return this.getValueByPath(contact, field);
  }
}

// CRM Data Source (with real-time fetching)
class CrmDataSource {
  constructor(crmAdapter, cache) {
    this.crm = crmAdapter;
    this.cache = cache;
  }

  async resolve(field, context) {
    // Try cache first
    const cacheKey = `crm:${context.contact.crmId}:${field}`;
    const cached = await this.cache.get(cacheKey);
    if (cached) return cached;

    // Fetch from CRM
    const crmData = await this.crm.getContactData(context.contact.crmId);
    
    // Cache the entire response, then extract field
    await this.cache.set(
      `crm:${context.contact.crmId}`,
      crmData,
      300 // 5 minute TTL
    );

    return this.getValueByPath(crmData, field);
  }
}

// Computed Variables
class ComputedVariableRegistry {
  constructor() {
    this.computations = new Map();
    this.registerDefaults();
  }

  register(name, computation) {
    this.computations.set(name, computation);
  }

  async compute(name, context) {
    const computation = this.computations.get(name);
    if (!computation) return null;
    return computation(context);
  }

  registerDefaults() {
    this.register('daysSinceLastContact', async (ctx) => {
      if (!ctx.contact.lastContactedAt) return 'never';
      const diff = Date.now() - new Date(ctx.contact.lastContactedAt).getTime();
      return Math.floor(diff / 86400000);
    });

    this.register('accountAge', async (ctx) => {
      if (!ctx.contact.createdAt) return 'unknown';
      const diff = Date.now() - new Date(ctx.contact.createdAt).getTime();
      const months = Math.floor(diff / (30 * 86400000));
      return months < 12 ? `${months} months` : `${Math.floor(months / 12)} years`;
    });

    this.register('nextPaymentDate', async (ctx) => {
      if (!ctx.contact.lastPaymentDate) return null;
      const last = new Date(ctx.contact.lastPaymentDate);
      last.setMonth(last.getMonth() + 1);
      return last;
    });

    this.register('lifetimeValue', async (ctx) => {
      if (!ctx.crm?.totalPayments) return null;
      return ctx.crm.totalPayments;
    });
  }
}
```

## Integration Points

- **Template Engine (sec-01):** Consumes resolved variable values during rendering
- **Contact Service (Ch 02):** Provides contact field data
- **CRM Integration (Part 10, Ch 02):** Real-time CRM data fetching
- **Campaign Config (Ch 01):** Provides static campaign-level variables
- **Computed Variable Registry:** Derives values from other sources
- **Cache Layer (Redis):** Variable value caching with configurable TTL

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- CRM data fetching adds latency — target <100ms for CRM variable resolution, with fallback if slower
- Cache invalidation is critical — when CRM data changes, cached variables should reflect the update within TTL
- Circular computed variable references should be detected and prevented during registration
- Variable resolution failures should not crash the call — always provide a configured fallback
- Log variable resolution failures with full context for debugging (but avoid logging PII in logs)
- Deep path resolution (e.g., `contact.preferences.communication.language`) should handle null intermediate objects
- Variable resolution should be observable — each resolution should have timing and source tracking for debugging
- Consider pre-fetching known required variables when the call is initiated, rather than lazy resolution
- Custom field type definitions (date, number, boolean, text) help with proper formatting
- Sensitive data (credit cards, SSNs) should never be available as template variables — enforce at the data source level
