# Section 04: Real-Time CRM Data Injection

## Overview

Real-time CRM data injection fetches live data from the customer's CRM system during a call and injects it into the script template. This enables the AI agent to reference up-to-the-minute information — recent orders, open support tickets, account balances, or the customer's current subscription tier. The injection must happen with minimal latency (the contact is waiting on the line) and gracefully handle API failures, rate limits, and data inconsistencies.

The injection system maintains CRM connection configurations per tenant (API endpoints, authentication, field mappings), provides a caching layer to reduce redundant API calls, and implements circuit breakers to protect CRM APIs from excessive load. It supports both pull-based injection (script requests specific CRM fields) and push-based injection (CRM sends webhook updates during the call for specific triggers).

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Real-Time CRM Data Injection                    │
├─────────────────────────────────────────────────────────────┤
│  Call Initiation                                            │
│       │                                                     │
│       ▼                                                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  1. Identify CRM Fields Required by Script            │   │
│  │     Scan template for {{crm.*}} variables            │   │
│  │     Build field request list                          │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  2. Check Cache                                      │   │
│  │     Redis key: crm:{tenant}:{contactId}:{field}      │   │
│  │     TTL: 5 minutes (configurable)                    │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                    │
│              ┌──────────┴──────────┐                        │
│              ▼                     ▼                        │
│  ┌──────────────────┐  ┌──────────────────────┐            │
│  │ Cache Hit        │  │ Cache Miss           │            │
│  │ → Use cached     │  │ → Fetch from CRM     │            │
│  │   value          │  │   API                │            │
│  └──────────────────┘  └──────────┬───────────┘            │
│                                   │                        │
│                                   ▼                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  3. CRM API Call (with circuit breaker)               │   │
│  │     • Build CRM-specific request                      │   │
│  │     • Authenticate (OAuth2 token rotation)            │   │
│  │     • Execute with timeout (3 seconds)                │   │
│  │     • Parse response → extract fields                 │   │
│  │     • Cache response → return data                   │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  4. Template Rendering (with injected data)           │   │
│  │     "I see your last order was on March 15th..."     │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Design Decisions

- **Pre-fetch on call initiation:** All CRM variables required by the script are fetched in parallel when the call is initiated, before the AI agent starts speaking. This eliminates per-variable latency during the call. Trade-off: initial delay (500ms-3s) vs. no mid-call delays.

- **Configurable cache TTL per field type:** High-volatility fields (account balance) get short TTL (1-5 minutes), low-volatility fields (subscription tier) get longer TTL (1-24 hours). Trade-off: cache management complexity vs. data freshness.

- **Circuit breaker per CRM instance:** If a CRM API becomes slow or unresponsive, the circuit breaker trips and returns cached or default values. This prevents CRM issues from breaking calls. Trade-off: stale data during outages vs. call continuity.

- **Field-level fallback:** Each CRM field can have a fallback chain — if the CRM API fails, use cached data, then last-known value, then a configured default. Trade-off: fallback complexity vs. rendering reliability.

## Implementation Approach

```
class CrmDataInjector {
  constructor(crmAdapter, cache, circuitBreaker) {
    this.adapter = crmAdapter;
    this.cache = cache;
    this.circuitBreaker = circuitBreaker;
  }

  async preFetchRequiredFields(template, context) {
    // Scan template for CRM variable references
    const requiredFields = this.extractCrmFields(template);
    if (requiredFields.length === 0) return {};

    const fields = {};
    const misses = [];

    // Check cache for each field
    for (const field of requiredFields) {
      const cacheKey = this.buildCacheKey(context, field);
      const cached = await this.cache.get(cacheKey);
      
      if (cached !== null && cached !== undefined) {
        fields[field] = JSON.parse(cached);
      } else {
        misses.push(field);
      }
    }

    // Fetch missing fields from CRM
    if (misses.length > 0) {
      const crmData = await this.fetchFromCrm(
        context.tenantId,
        context.contact.crmId,
        misses,
        context
      );

      // Cache and store results
      for (const [field, value] of Object.entries(crmData)) {
        const cacheKey = this.buildCacheKey(context, field);
        await this.cache.setex(
          cacheKey,
          this.getFieldCacheTTL(field),
          JSON.stringify(value)
        );
        fields[field] = value;
      }
    }

    return fields;
  }

  async fetchFromCrm(tenantId, crmContactId, fields, context) {
    const crmConfig = await this.getCrmConfig(tenantId);
    
    // Check circuit breaker
    if (this.circuitBreaker.isOpen(tenantId)) {
      return this.getFallbackValues(fields, context);
    }

    try {
      const response = await this.adapter.fetchContactData(
        crmConfig,
        crmContactId,
        fields,
        { timeout: 3000 } // 3 second timeout
      );

      // Record success for circuit breaker
      this.circuitBreaker.recordSuccess(tenantId);

      return response;
    } catch (error) {
      this.circuitBreaker.recordFailure(tenantId);
      
      // Log error and return fallbacks
      console.error(`CRM fetch failed for tenant ${tenantId}:`, error.message);
      return this.getFallbackValues(fields, context);
    }
  }

  extractCrmFields(templateAst) {
    const fields = new Set();
    
    const traverse = (node) => {
      if (node.type === 'variable' && node.source === 'crm') {
        fields.add(node.field);
      }
      if (node.children) {
        node.children.forEach(traverse);
      }
      if (node.trueBranch) node.trueBranch.forEach(traverse);
      if (node.falseBranch) node.falseBranch.forEach(traverse);
    };

    traverse(templateAst);
    return [...fields];
  }

  async getCrmConfig(tenantId) {
    const config = await this.cache.get(`crm:config:${tenantId}`);
    if (config) return JSON.parse(config);

    // Fetch from database
    const dbConfig = await this.prisma.crmConfig.findUnique({
      where: { tenant_id: tenantId }
    });

    await this.cache.setex(
      `crm:config:${tenantId}`,
      3600, // 1 hour cache
      JSON.stringify(dbConfig)
    );

    return dbConfig;
  }

  getFieldCacheTTL(field) {
    const ttls = {
      'accountBalance': 60, // 1 minute
      'lastOrderDate': 300, // 5 minutes
      'lastOrderTotal': 300,
      'subscriptionTier': 86400, // 24 hours
      'supportTickets': 60,
      'lifetimeValue': 86400
    };
    return ttls[field] || 300;
  }

  getFallbackValues(fields, context) {
    const fallbacks = {};
    
    // Try to get last known values from cache
    for (const field of fields) {
      fallbacks[field] = context.contact[field] || null;
    }

    return fallbacks;
  }

  buildCacheKey(context, field) {
    return `crm:${context.tenantId}:${context.contact.crmId}:${field}`;
  }
}

// CRM Adapter Interface (implemented per CRM type)
class CrmAdapter {
  async fetchContactData(config, crmContactId, fields, options) {
    throw new Error('Implement in CRM-specific adapter');
  }
}

// Salesforce implementation
class SalesforceAdapter extends CrmAdapter {
  async fetchContactData(config, salesforceContactId, fields) {
    const connection = await this.getConnection(config);
    
    const query = `
      SELECT ${fields.join(', ')}
      FROM Contact
      WHERE Id = '${salesforceContactId}'
    `;
    
    const result = await connection.query(query);
    return result.records[0];
  }
}

// HubSpot implementation
class HubSpotAdapter extends CrmAdapter {
  async fetchContactData(config, hubspotContactId, fields) {
    const properties = fields.map(f => ({
      propertyName: this.fieldMapping[f] || f
    }));

    const response = await axios.get(
      `https://api.hubapi.com/crm/v3/objects/contacts/${hubspotContactId}`,
      {
        headers: { Authorization: `Bearer ${config.accessToken}` },
        params: { properties: properties.map(p => p.propertyName).join(',') }
      }
    );

    return response.data.properties;
  }
}
```

## Integration Points

- **Template Engine (sec-01):** Consumes CRM-injected data during rendering
- **CRM Integration Layer (Part 10, Ch 02):** Adapter implementations for specific CRMs
- **Cache Layer (Redis):** Caches CRM responses with field-specific TTL
- **Circuit Breaker System:** Protects CRM APIs from overload
- **Call Context:** Passes tenant ID, contact CRM ID through call lifecycle
- **Analytics (Ch 09):** CRM injection latency, cache hit rate, fallback usage

## Open-Source Tools

- **Redis:** CRM data cache with per-field TTL
- **Opossum (Circuit Breaker):** Node.js circuit breaker for CRM API calls
- **Axios / SuperAgent:** HTTP client for CRM API requests with timeout support
- **Bottleneck:** Rate limiter for CRM API calls to respect API limits
- **Zod:** Response validation to catch CRM API data format changes

## Production Considerations

- CRM API latency is the biggest risk — set aggressive timeouts (3 seconds) and have fallbacks ready
- Cache hit rate target: >90% for commonly accessed fields (account balance, subscription tier)
- OAuth2 token refresh must be handled transparently — expired tokens should refresh without failing the call
- CRM API rate limits vary widely — HubSpot allows 100 req/10s, Salesforce 1500 req/hour per org
- Circuit breaker should trip after 5 consecutive failures and retry after 30 seconds
- Field mapping (CRM field names → system field names) should be configurable per tenant
- Pre-fetching all fields in parallel keeps total CRM latency to the slowest single field, not the sum
- Log CRM injection failures with context (tenant, field, error) for proactive monitoring
- Test CRM injection with real CRM sandboxes, not just mock responses
- Consider partial injection — if 3 of 5 fields fail, use the 3 successful fields and fallbacks for the other 2
