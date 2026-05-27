# Section 02: Real-Time DNC Check Engine

## Overview

The real-time DNC check engine validates every outbound call attempt against all applicable Do-Not-Call lists before the call is placed. This check happens in the critical dialing path — it must be both comprehensive (checking all applicable sources) and extremely fast (under 10ms) to avoid delaying the dialing pipeline. The engine checks national, state, internal, and campaign-specific DNC lists for each contact's phone number before allowing the call to proceed.

The check engine uses a multi-layer architecture: an in-memory Bloom filter for rapid negative checks, a Redis cache for recently checked numbers, and a database query for confirmation. It supports batch checking for list scrubbing and per-contact exceptions based on consent or established business relationship. Every check result is logged with the timestamp, lists checked, and match result for compliance audit.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Real-Time DNC Check Engine                      │
├─────────────────────────────────────────────────────────────┤
│  Dial Request for: +14155551234                              │
│       │                                                     │
│       ▼                                                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Layer 1: Redis Cache (sub-millisecond)               │   │
│  │  Key: dnc:check:{phone}                              │   │
│  │  If cached result exists and TTL valid → return      │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │ Cache miss                        │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Layer 2: Bloom Filter (O(1), ~1ms)                  │   │
│  │  If NOT in Bloom → definitely not on DNC → return    │   │
│  │  If IN Bloom → possible match → check database       │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │ Bloom says "maybe"                │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Layer 3: Database Query (indexed, ~5ms)             │   │
│  │  SELECT * FROM dnc_entries                           │   │
│  │  WHERE phone = '+14155551234'                         │   │
│  │    AND (expires_at IS NULL OR expires_at > NOW())    │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                    │
│              ┌──────────┴──────────┐                        │
│              ▼                     ▼                        │
│  ┌──────────────────┐  ┌──────────────────────┐            │
│  │ DNC Match Found  │  │ No DNC Match        │            │
│  │ → Check exception │  │ → Allow dial        │            │
│  │   (consent/EBR)  │  │ → Cache result      │            │
│  └──────┬───────────┘  └──────────────────────┘            │
│         │                                                    │
│  ┌──────▼───────────┐                                       │
│  │ Has Exception?    │                                       │
│  │ Yes → allow       │                                       │
│  │ No → block dial   │                                       │
│  └──────────────────┘                                       │
└─────────────────────────────────────────────────────────────┘
```

## Design Decisions

- **Bloom filter for scalability:** A Bloom filter with 1% false positive rate can represent 10M numbers in ~12MB of memory. This allows the common case (number not on DNC) to be resolved without a database query. Trade-off: configurable false positives vs. memory usage.

- **Result caching with short TTL:** Recent DNC check results are cached in Redis for 5 minutes. This handles repeated checks of the same number in rapid succession (e.g., retry attempts). Trade-off: cache TTL vs. DNC list freshness.

- **Exception checking after DNC match:** If a number is on a DNC list, the engine checks for exceptions (prior express consent, established business relationship, transactional context). Exceptions are tracked per contact with source and timestamp. Trade-off: exception checking complexity vs. permissible calling flexibility.

- **Per-source DNC resolution:** The engine checks all applicable sources and returns the most restrictive result. A number on both the national DNC and a campaign-specific list gets the combined restriction. Trade-off: multi-source checking cost vs. comprehensive compliance.

## Implementation Approach

```
class RealTimeDncChecker {
  constructor(bloomFilter, cache, db, exceptionService) {
    this.bloom = bloomFilter;
    this.cache = cache;
    this.db = db;
    this.exceptions = exceptionService;
    this.cacheTTL = 300; // 5 minutes
  }

  async check(phone, tenantId, campaignId) {
    const normalizedPhone = this.normalizePhone(phone);
    
    // Layer 1: Cache
    const cached = await this.checkCache(normalizedPhone, tenantId);
    if (cached !== null) {
      return this.applyExceptionOverride(cached, tenantId, normalizedPhone);
    }

    // Layer 2: Bloom filter
    const bloomKey = `dnc:bloom:${tenantId}`;
    const inBloom = await this.bloom.exists(bloomKey, normalizedPhone);
    
    if (!inBloom) {
      // Definitely not on DNC
      const result = { blocked: false, source: null, checkedAt: new Date() };
      await this.cacheResult(normalizedPhone, tenantId, result);
      return result;
    }

    // Layer 3: Database check (Bloom had potential match)
    const dncEntries = await this.queryDncDatabase(normalizedPhone, tenantId);
    
    if (dncEntries.length === 0) {
      // Bloom false positive
      const result = { blocked: false, source: null, checkedAt: new Date() };
      await this.cacheResult(normalizedPhone, tenantId, result);
      return result;
    }

    // DNC match found — check for exceptions
    const exception = await this.exceptions.getActiveException(
      tenantId, 
      normalizedPhone,
      campaignId
    );

    if (exception) {
      // Exception overrides DNC
      const result = {
        blocked: false,
        source: dncEntries[0].source,
        exceptionApplied: true,
        exceptionType: exception.type,
        checkedAt: new Date()
      };
      await this.cacheResult(normalizedPhone, tenantId, result);
      return result;
    }

    // Blocked by DNC
    const result = {
      blocked: true,
      source: dncEntries[0].source,
      matchedOn: dncEntries.map(e => e.source),
      blockedBy: dncEntries[0].source,
      checkedAt: new Date()
    };

    await this.cacheResult(normalizedPhone, tenantId, result);
    return result;
  }

  async batchCheck(phones, tenantId, campaignId) {
    const results = {};
    const batchSize = 100;

    for (let i = 0; i < phones.length; i += batchSize) {
      const batch = phones.slice(i, i + batchSize);
      const batchResults = await Promise.all(
        batch.map(phone => this.check(phone, tenantId, campaignId))
      );
      
      batch.forEach((phone, idx) => {
        results[phone] = batchResults[idx];
      });
    }

    return results;
  }

  async queryDncDatabase(phone, tenantId) {
    // Check all DNC sources (cached query)
    return this.db.$queryRaw`
      SELECT source, expires_at, metadata
      FROM dnc_entries
      WHERE phone = ${phone}
        AND tenant_id = ${tenantId}
        AND (expires_at IS NULL OR expires_at > NOW())
      ORDER BY 
        CASE source
          WHEN 'national_dnc' THEN 1
          WHEN 'state_dnc' THEN 2
          WHEN 'internal' THEN 3
          ELSE 4
        END
      LIMIT 5
    `;
  }

  async checkCache(phone, tenantId) {
    const key = `dnc:result:${tenantId}:${phone}`;
    const cached = await this.cache.get(key);
    if (cached) {
      return JSON.parse(cached);
    }
    return null;
  }

  async cacheResult(phone, tenantId, result) {
    const key = `dnc:result:${tenantId}:${phone}`;
    await this.cache.setex(key, this.cacheTTL, JSON.stringify(result));
  }

  async applyExceptionOverride(result, tenantId, phone) {
    if (result.blocked) {
      // Re-check exception in case one was added since cache
      const exception = await this.exceptions.getActiveException(tenantId, phone);
      if (exception) {
        return {
          ...result,
          blocked: false,
          exceptionApplied: true,
          exceptionType: exception.type
        };
      }
    }
    return result;
  }

  async handleOptOut(phone, tenantId, source, campaignId) {
    // Immediately add to suppression DNC list
    await this.db.dncEntry.create({
      data: {
        phone: this.normalizePhone(phone),
        tenant_id: tenantId,
        source: 'internal_opt_out',
        metadata: {
          campaignId,
          optOutTime: new Date().toISOString(),
          channel: 'voice'
        },
        expires_at: null // Never expires
      }
    });

    // Invalidate cache
    await this.cache.del(`dnc:result:${tenantId}:${phone}`);
    
    // Update Bloom filter
    const bloomKey = `dnc:bloom:${tenantId}`;
    await this.bloom.add(bloomKey, phone);
  }

  normalizePhone(phone) {
    const cleaned = phone.replace(/\D/g, '');
    if (cleaned.length === 10) return `+1${cleaned}`;
    if (cleaned.length === 11 && cleaned.startsWith('1')) return `+${cleaned}`;
    return `+${cleaned}`;
  }
}
```

## Integration Points

- **Dialing Engine (Ch 01):** Calls check before every dial attempt
- **DNC Ingestion (sec-01):** Populates the DNC database and Bloom filter
- **Exception/Consent Service (sec-05):** Provides exception overrides for DNC matches
- **Opt-Out Handling (sec-05):** Triggers immediate DNC addition on opt-out
- **Contact Import (Ch 02):** Batch DNC check during import
- **Compliance Audit (sec-07):** DNC check logging for audit trail
- **Campaign Configuration (Ch 01):** Campaign-specific DNC list associations

## Open-Source Tools

- **Redis + RedisBloom:** Bloom filter setup and fast lookups
- **PostgreSQL:** DNC database with GIN indexes on phone number
- **BullMQ:** Async DNC cache warming for high-volume campaigns
- **Prometheus:** DNC check latency and hit rate monitoring
- **libphonenumber:** Phone normalization

## Production Considerations

- DNC check latency target: <10ms total for the multi-layer check
- Bloom filter false positive rate should be monitored — if it exceeds 2%, the filter needs resizing
- Cache TTL balances freshness vs. performance — 5 minutes is a good default but should be configurable
- Exception checking after a DNC match should be fast (<5ms) since it's in the hot path
- Opt-out must be IMMEDIATE — the Bloom filter and cache must be updated synchronously before the call flow continues
- Batch DNC checking for list import should use a separate, lower-priority queue to avoid impacting real-time checks
- DNC check results should be logged with source attribution for all blocked calls
- Monitor DNC match rate — a sudden increase may indicate a list import issue or a data quality problem
- International DNC lists require country-specific Bloom filters — avoid mixing US and UK numbers in the same filter
- The Bloom filter should be persisted to disk for recovery — Redis RDB/AOF should include bloom filter keys
