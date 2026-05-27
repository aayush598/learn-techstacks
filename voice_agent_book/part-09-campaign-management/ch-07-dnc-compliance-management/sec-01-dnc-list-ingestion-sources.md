# Section 01: DNC List Ingestion & Sources

## Overview

Do-Not-Call (DNC) list ingestion is the process of importing, maintaining, and synchronizing telephone numbers that must not be called. These lists come from multiple sources: national registries (US National DNC, Canada's CNID, UK's TPS), state-level registries, internal suppression lists (prior customers who opted out), third-party data providers, and industry-specific lists (litigators, bankruptcy records for collections). Each source has different formats, update frequencies, and legal requirements.

The ingestion pipeline must handle millions of numbers across multiple lists, de-duplicate across sources, track list provenance for compliance audit, and provide real-time lookup capabilities. Lists must be refreshed at regulatory-specified intervals — the US DNC must be refreshed every 31 days, while state lists may have different requirements. The system tracks list freshness and alerts when lists are due for refresh.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              DNC List Ingestion & Sources                    │
├─────────────────────────────────────────────────────────────┤
│  Source Types:                                              │
│                                                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────┐  │
│  │ National   │  │ State      │  │ Internal   │  │Third │  │
│  │ DNC        │  │ Registries │  │ Suppress   │  │Party │  │
│  └──────┬─────┘  └──────┬─────┘  └──────┬─────┘  └──┬───┘  │
│         │               │               │            │      │
│         ▼               ▼               ▼            ▼      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Ingestion Pipeline                                 │   │
│  │                                                      │   │
│  │  1. Download (FTP/API/Upload) → format detection    │   │
│  │  2. Parse + normalize (E.164 conversion)            │   │
│  │  3. Validate (checksum, format, dedup within list)  │   │
│  │  4. Merge into master DNC database                   │   │
│  │  5. Update Bloom filter for fast lookup              │   │
│  │  6. Log import summary (total, added, removed)       │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Master DNC Database                                 │   │
│  │                                                      │   │
│  │  phone (E.164) │ source │ imported_at │ expires_at  │   │
│  │  ──────────────┼────────┼─────────────┼─────────────│   │
│  │  +14155551234  │ US DNC │ 2025-01-01  │ 2025-02-01  │   │
│  │  +14155551235  │ FL DNC │ 2025-01-15  │ 2025-02-15  │   │
│  │  +14155551236  │ Inter. │ 2025-01-10  │ NULL        │   │
│  │  +14155551237  │ ThirdP │ 2025-01-20  │ 2025-05-20  │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Design Decisions

- **Unified DNC database with source attribution:** All DNC sources are consolidated into a single database with per-record source tracking. Different sources have different regulatory weight — a national DNC match is more significant than an internal suppression. Trade-off: database size vs. unified query performance.

- **Bloom filter for fast negative checks:** A Redis Bloom filter provides O(1) negative checks (definitely not on DNC). Only numbers that match the Bloom filter need a database confirmation. Trade-off: configurable false positive rate vs. memory usage.

- **Source expiration tracking:** Each DNC record has an expiration date based on the source's refresh requirements. Expired records are automatically purged or flagged for refresh. Trade-off: expiration management overhead vs. regulatory compliance.

- **Import delta tracking:** Each import logs the number of added, removed, and unchanged records. This provides auditability and allows rollback of specific imports if needed. Trade-off: audit log storage vs. import transparency.

## Implementation Approach

```
class DncIngestionService {
  constructor(storage, bloomFilter, dncDb) {
    this.storage = storage; // File storage for downloaded lists
    this.bloom = bloomFilter; // Redis Bloom filter
    this.db = dncDb;
  }

  async importSource(sourceType, options = {}) {
    // Get source configuration
    const sourceConfig = this.getSourceConfig(sourceType);
    
    // Download the list
    const file = await this.downloadSource(sourceConfig, options);
    
    // Parse and normalize
    const records = await this.parseFile(file, sourceConfig.format);
    
    // Normalize phone numbers to E.164
    const normalized = records.map(r => ({
      ...r,
      phone: this.normalizePhone(r.phone, sourceConfig.countryCode)
    }));

    // Validate numbers
    const valid = normalized.filter(r => r.phone);
    
    // Batch import
    const result = await this.batchImport(valid, sourceType, sourceConfig);
    
    // Update Bloom filter
    await this.rebuildBloomFilter();
    
    // Log import record
    await this.logImport(sourceType, result);
    
    return result;
  }

  async batchImport(records, sourceType, config) {
    const BATCH_SIZE = 10000;
    let added = 0;
    let duplicates = 0;
    let errors = 0;

    for (let i = 0; i < records.length; i += BATCH_SIZE) {
      const batch = records.slice(i, i + BATCH_SIZE);
      
      // Upsert with conflict handling
      const result = await this.db.$executeRaw`
        INSERT INTO dnc_entries (phone, source, imported_at, expires_at, metadata)
        VALUES ${this.formatBatchValues(batch, sourceType, config)}
        ON CONFLICT (phone, source) 
        DO UPDATE SET 
          imported_at = NOW(),
          expires_at = ${config.refreshIntervalDays} ? NOW() + INTERVAL '${config.refreshIntervalDays} days' : NULL,
          metadata = EXCLUDED.metadata
      `;
    }

    // Remove entries where the source list no longer contains the number
    if (config.pruneMissing) {
      await this.pruneMissingNumbers(records, sourceType);
    }

    return {
      totalProcessed: records.length,
      added,
      duplicates,
      errors,
      source: sourceType
    };
  }

  async refreshAllSources() {
    const sources = this.getAllSourceConfigs();
    const results = [];

    for (const source of sources) {
      if (this.isRefreshDue(source)) {
        const result = await this.importSource(source.type);
        results.push(result);
        source.lastRefreshed = new Date();
      }
    }

    return results;
  }

  isRefreshDue(source) {
    if (!source.lastRefreshed) return true;
    
    const daysSinceRefresh = Math.floor(
      (Date.now() - source.lastRefreshed.getTime()) / 86400000
    );
    
    return daysSinceRefresh >= source.refreshIntervalDays;
  }

  async rebuildBloomFilter() {
    // Rebuild Bloom filter from scratch (done after import)
    const redisKey = 'dnc:bloom';
    await this.bloom.reserve(redisKey, 0.01, 10000000); // 1% false positive, 10M expected
    
    // Stream all active DNC numbers and add to filter
    const cursor = this.db.$queryRawUnsafe(
      'SELECT phone FROM dnc_entries WHERE expires_at IS NULL OR expires_at > NOW()'
    );
    
    for await (const row of cursor) {
      await this.bloom.add(redisKey, row.phone);
    }
  }

  normalizePhone(phone, defaultCountry) {
    // Use libphonenumber for robust normalization
    const parsed = phoneUtil.parse(phone, defaultCountry);
    if (!phoneUtil.isValidNumber(parsed)) return null;
    return phoneUtil.format(parsed, PhoneNumberFormat.E164);
  }

  // Source configurations
  getSourceConfig(type) {
    const sources = {
      'us_dnc': {
        type: 'us_dnc',
        name: 'US National Do Not Call Registry',
        url: 'https://www.donotcall.gov/downloads/',
        format: 'csv',
        countryCode: 'US',
        refreshIntervalDays: 31, // Required by FTC
        lastRefreshed: null,
        pruneMissing: true // Remove numbers no longer on list
      },
      'internal_suppression': {
        type: 'internal_suppression',
        format: 'api',
        refreshIntervalDays: 1,
        pruneMissing: false // Never remove internal suppressions
      },
      'state_dnc': {
        type: 'state_dnc',
        format: 'csv',
        refreshIntervalDays: 31,
        pruneMissing: true
      }
    };

    return sources[type] || sources['internal_suppression'];
  }
}

interface DncSourceConfig {
  type: string;
  name: string;
  format: 'csv' | 'api' | 'ftp';
  refreshIntervalDays: number;
  lastRefreshed: Date | null;
  pruneMissing: boolean;
  countryCode?: string;
  url?: string;
}
```

## Integration Points

- **Real-Time DNC Check (sec-02):** Consumes the DNC database and Bloom filter for pre-dial checks
- **Contact Import (Ch 02):** DNC check during import prevents adding DNC-listed contacts
- **Campaign Dialing (Ch 01):** Pre-dial DNC check prevents calling DNC numbers
- **Compliance Audit (Ch 07, sec-07):** DNC list refresh history for regulatory audit
- **Internal Opt-Out:** Contact opt-outs trigger immediate addition to DNC database
- **Analytics (Ch 09):** DNC match rate tracking for list quality assessment

## Open-Source Tools

- **libphonenumber (Google):** Phone number parsing and E.164 normalization
- **Redis + RedisBloom:** Bloom filter module for DNC lookups
- **BullMQ:** Scheduled refresh job queue for DNC list updates
- **PostgreSQL:** DNC entry database with indexes on (phone, source)
- **csv-parse / papaparse:** CSV parsing for downloaded DNC lists
- **basic-ftp / axios:** FTP and HTTP download for DNC list retrieval

## Production Considerations

- US National DNC list contains ~250M numbers — ensure the database and Bloom filter can handle this scale
- DNC list refresh is time-sensitive — the FTC requires monthly updates; schedule refreshes automatically
- Different DNC sources have different formats, delimiters, and encodings — make the parser robust
- Source attribution is critical for compliance — must be able to prove which DNC list was checked
- DNC lookups must be extremely fast (<10ms) since they're in the dialing hot path
- Bloom filter false positives mean a small percentage of non-DNC numbers get checked against the database
- Internal suppression list entries are permanent — never expire unless explicitly removed
- Third-party DNC lists may have usage restrictions — track per-list API usage for billing
- Audit log for all DNC imports (who imported, when, how many records) is a compliance requirement
- DNC list errors (bad format, download failure) should trigger immediate alerts to compliance team
