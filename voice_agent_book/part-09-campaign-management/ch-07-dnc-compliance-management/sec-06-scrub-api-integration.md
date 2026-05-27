# Section 06: Scrub API Integration

## Overview

Scrub API Integration connects the campaign management system with third-party phone number scrubbing services that verify contact lists against Do-Not-Call registries, deceased person databases, litigation lists, and other regulatory data sources. While the in-house DNC engine handles the primary pre-dial check (Bloom filter + database lookup), scrub APIs provide an additional compliance layer by cross-referencing against external data sources that the system cannot maintain internally. These services include national DNC registries (FTC, CRTC, ICO), third-party compliance providers (DNC.com, Gryphon Networks, PossibleNOW), and industry-specific lists (litigation databases for collections, bankruptcy filings for financial services).

The scrubbing process can be batch-based (upload entire contact list, receive results asynchronously) or real-time (individual number lookup via API). Batch scrubbing is typically used during contact list import and periodic compliance recalibration, while real-time scrubbing is reserved for high-value or high-risk calls. The integration must handle multiple service providers, manage API rate limits, process results with configurable match sensitivity, and maintain provider rotation for reliability.

## Architecture

```
                   Scrub API Integration System

  +-----------+    +-----------+    +-----------+    +-----------+
  | Contact   |--->| Scrub     |--->| Provider  |--->| Provider  |
  | Import    |    | Scheduler |    | Router    |    | Adapters  |
  | (Ch 02)   |    |           |    |           |    |           |
  +-----------+    +-----------+    +-----------+    +-----------+
                        |                               |     |
                        v                               |     |
                  +-----------+    +-----------+    +----+  +----+
                  | Batch     |--->| Provider  |    | DNC |  | Dor |
                  | Queue     |    | Worker    |    | .com|  | En |
                  +-----------+    +-----------+    +-----+  +----+
                        |               |
                        v               v
                  +-----------+    +-----------+
                  | Result    |    | Anomaly   |
                  | Processor |    | Detector  |
                  +-----------+    +-----------+
                        |               |
                        v               v
                  +-----------------------------------+
                  |         Scrub Results Database     |
                  |                                   |
                  | contact_id | provider | matched  |
                  | -----------+----------+----------|
                  | cnt001     | dnc_com  | true     |
                  | cnt002     | possiblenow | false |
                  | cnt003     | ftc_dnc | true     |
                  +-----------------------------------+
                                |
                                v
                  +-----------------------------+
                  | Action Engine               |
                  |                             |
                  | matched true → auto-suppress|
                  | uncertain → flag for review |
                  | error → retry or alert      |
                  +-----------------------------+
```

## Design Decisions

- **Provider abstraction with adapter pattern:** Each scrub provider implements a common interface (upload → poll/result → parse). The system can switch providers, add new ones, or run multiple providers in parallel without changing core logic. Trade-off: adapter development overhead vs. vendor flexibility and redundancy.

- **Batch as primary, real-time as secondary:** Batch scrubbing is the default for cost efficiency (batch rates are 5-10x cheaper than real-time). Real-time scrubbing is only used for high-value calls or same-day list imports. Trade-off: batch processing adds latency (minutes to hours) vs. real-time API costs.

- **Multi-provider consensus for high-risk matches:** When a phone number matches a DNC record in one provider, the system cross-references with a second provider before auto-suppressing. Consensus matching reduces false positives from provider data errors. Trade-off: double API costs vs. reduced false suppression risk.

- **Result caching with TTL:** Scrub results are cached with provider-specific TTLs (typically 30 days to match FTC refresh requirements). Subsequent scrubs for the same number skip API calls if cache is valid. Trade-off: cache staleness risk vs. significant API cost reduction.

## Implementation Approach

```
interface ScrubProvider {
  name: string;
  supportsBatch: boolean;
  supportsRealTime: boolean;
  
  uploadList(contacts: Contact[]): Promise<BatchJob>;
  checkStatus(jobId: string): Promise<BatchStatus>;
  getResults(jobId: string): Promise<ScrubResult[]>;
  checkNumber(phone: string): Promise<ScrubResult>;
}

interface ScrubResult {
  phone: string;
  matched: boolean;
  matchedOn: string[];  // List names (DNC, deceased, litigation)
  confidence: number;
  matchType: 'exact' | 'partial' | 'household';
  provider: string;
  checkedAt: Date;
  expiresAt?: Date;
  rawResponse: Record<string, any>;
}

class ScrubApiService {
  constructor(providers, cache, db) {
    this.providers = new Map(providers.map(p => [p.name, p]));
    this.cache = cache;
    this.db = db;
    this.config = {
      defaultProvider: 'dnc_com',
      consensusProvider: 'possiblenow',
      batchChunkSize: 5000,
      maxRetries: 3,
      resultCacheTtlDays: 30
    };
  }

  async scrubBatchContacts(contacts, options = {}) {
    const {
      provider = this.config.defaultProvider,
      consensusCheck = true,
      autoSuppress = true
    } = options;

    const scrubProvider = this.providers.get(provider);

    // 1. Filter out recently scrubbed contacts
    const toScrub = await this.filterCached(contacts);

    if (toScrub.length === 0) {
      return { contacts, allCached: true };
    }

    // 2. Chunk and upload
    const chunks = this.chunkArray(toScrub, this.config.batchChunkSize);
    const batchJobs = [];

    for (const chunk of chunks) {
      const job = await scrubProvider.uploadList(chunk);
      batchJobs.push(job);
    }

    // 3. Poll for results
    const batchResults = await this.pollBatchResults(batchJobs, scrubProvider);

    // 4. Process results
    const processed = await this.processResults(
      batchResults,
      provider,
      consensusCheck
    );

    // 5. Cache results
    await this.cacheResults(processed);

    // 6. Auto-suppress matched contacts
    if (autoSuppress) {
      await this.suppressMatched(processed);
    }

    return {
      totalScrubbed: toScrub.length,
      totalMatched: processed.filter(r => r.matched).length,
      totalErrors: processed.filter(r => r.error).length,
      provider,
      results: processed
    };
  }

  async scrubSingleNumber(phone, options = {}) {
    const {
      provider = this.config.defaultProvider,
      forceRefresh = false
    } = options;

    // Check cache first
    if (!forceRefresh) {
      const cached = await this.cache.get(`scrub:${phone}`);
      if (cached) return JSON.parse(cached);
    }

    // Check in-memory DNC first (fast path)
    const dncStatus = await this.dncService.checkNumber(phone);
    if (dncStatus.isDnc) {
      return {
        phone,
        matched: true,
        matchedOn: ['internal_dnc'],
        confidence: 1.0,
        matchType: 'exact',
        provider: 'internal',
        checkedAt: new Date(),
        expiresAt: null
      };
    }

    // Real-time API check
    const scrubProvider = this.providers.get(provider);
    const result = await scrubProvider.checkNumber(phone);

    // Consensus check for matches
    if (result.matched && options.consensusCheck) {
      const consensusResult = await this.checkConsensus(phone, result);
      result.consensus = consensusResult;
    }

    // Cache result
    await this.cache.set(
      `scrub:${phone}`,
      JSON.stringify(result),
      'EX',
      86400 * this.config.resultCacheTtlDays
    );

    return result;
  }

  async pollBatchResults(jobs, provider, timeout = 300000) {
    const startTime = Date.now();
    const completed = [];

    while (completed.length < jobs.length && (Date.now() - startTime) < timeout) {
      const pending = jobs.filter(j => !completed.find(c => c.jobId === j.jobId));

      for (const job of pending) {
        const status = await provider.checkStatus(job.jobId);

        if (status.state === 'completed') {
          const results = await provider.getResults(job.jobId);
          completed.push({
            jobId: job.jobId,
            chunk: job.chunk,
            results,
            error: null
          });
        } else if (status.state === 'error') {
          completed.push({
            jobId: job.jobId,
            chunk: job.chunk,
            results: [],
            error: status.error
          });
        }
      }

      if (completed.length < jobs.length) {
        await this.sleep(5000); // 5s polling interval
      }
    }

    return completed;
  }

  async processResults(batchResults, provider, consensusCheck) {
    const allResults = [];

    for (const batch of batchResults) {
      if (batch.error) {
        // Retry logic for failed batches
        for (const contact of batch.chunk) {
          allResults.push({
            phone: contact.phone,
            matched: false,
            matchedOn: [],
            confidence: 0,
            matchType: 'none',
            provider,
            checkedAt: new Date(),
            error: batch.error,
            retry: true
          });
        }
        continue;
      }

      for (const result of batch.results) {
        const processed = {
          phone: result.phone,
          matched: result.matched,
          matchedOn: result.matchedOn || [],
          confidence: result.confidence || (result.matched ? 0.9 : 0.1),
          matchType: result.matchType || 'exact',
          provider,
          checkedAt: new Date(),
          expiresAt: this.computeExpiry(result)
        };

        // Consensus check for positive matches
        if (processed.matched && consensusCheck && processed.confidence < 0.95) {
          processed.consensus = await this.checkConsensus(
            processed.phone,
            processed
          );
        }

        allResults.push(processed);
      }
    }

    return allResults;
  }

  async checkConsensus(phone, initialResult) {
    // Run against a second provider to verify match
    const consensusProvider = this.providers.get(this.config.consensusProvider);

    if (!consensusProvider) {
      return { verified: false, reason: 'No consensus provider available' };
    }

    try {
      const consensusResult = await consensusProvider.checkNumber(phone);

      return {
        verified: consensusResult.matched === initialResult.matched,
        verifiedWith: this.config.consensusProvider,
        initialResult,
        consensusResult,
        confidence: consensusResult.matched === initialResult.matched ? 0.99 : 0.5
      };
    } catch (error) {
      return {
        verified: false,
        reason: `Consensus check failed: ${error.message}`,
        verifiedWith: this.config.consensusProvider,
        error: error.message
      };
    }
  }

  async suppressMatched(results) {
    const matched = results.filter(r => r.matched);

    for (const result of matched) {
      await this.dncService.addToSuppression({
        phoneNumber: result.phone,
        reason: `scrub_api_match:${result.provider}`,
        source: `scrub_api:${result.provider}:${result.matchedOn.join(',')}`,
        expiresAt: result.expiresAt,
        metadata: {
          provider: result.provider,
          matchType: result.matchType,
          confidence: result.confidence,
          matchedOn: result.matchedOn,
          consensus: result.consensus
        }
      });
    }
  }

  async filterCached(contacts) {
    const toScrub = [];

    for (const contact of contacts) {
      const cached = await this.cache.get(`scrub:${contact.phone}`);

      if (cached) {
        const parsed = JSON.parse(cached);
        const expiresAt = parsed.expiresAt ? new Date(parsed.expiresAt) : null;

        if (expiresAt && expiresAt > new Date()) {
          contact._scrubResult = parsed;
          continue; // Cache valid
        }
      }

      toScrub.push(contact);
    }

    return toScrub;
  }

  async cacheResults(results) {
    const pipeline = this.cache.pipeline();

    for (const result of results) {
      const ttl = this.computeCacheTtl(result);
      pipeline.set(
        `scrub:${result.phone}`,
        JSON.stringify(result),
        'EX',
        ttl
      );
    }

    await pipeline.exec();
  }

  computeExpiry(providerResult) {
    // Provider results have different validity periods
    // DNC list match: expires per FTC 31-day refresh
    // Deceased match: permanent
    // Litigation match: typically 1 year
    if (providerResult.matchedOn?.includes('deceased')) return null;
    if (providerResult.matchedOn?.includes('dnc')) {
      return this.addDays(31);
    }
    return this.addDays(90);
  }

  computeCacheTtl(result) {
    if (!result.expiresAt) return 365 * 86400; // 1 year for permanent results
    const daysRemaining = Math.ceil(
      (new Date(result.expiresAt).getTime() - Date.now()) / 86400000
    );
    return Math.max(daysRemaining, 1) * 86400;
  }
}

// Provider Adapter Example
class DncComProviderAdapter implements ScrubProvider {
  name = 'dnc_com';
  supportsBatch = true;
  supportsRealTime = true;

  constructor(apiClient) {
    this.client = apiClient;
    this.baseUrl = 'https://api.dnc.com/v2';
  }

  async uploadList(contacts) {
    const payload = {
      contacts: contacts.map(c => ({
        phone: c.phone,
        firstName: c.firstName,
        lastName: c.lastName,
        zipCode: c.zipCode
      })),
      options: {
        matchType: 'exact_and_household',
        includeLists: ['dnc', 'deceased', 'litigation']
      }
    };

    const response = await this.client.post(
      `${this.baseUrl}/scrub/batch`,
      payload
    );

    return { jobId: response.data.jobId, chunk: contacts };
  }

  async checkStatus(jobId) {
    const response = await this.client.get(
      `${this.baseUrl}/scrub/batch/${jobId}/status`
    );
    return response.data;
  }

  async getResults(jobId) {
    const response = await this.client.get(
      `${this.baseUrl}/scrub/batch/${jobId}/results`
    );
    return response.data.results;
  }

  async checkNumber(phone) {
    const response = await this.client.get(
      `${this.baseUrl}/scrub/single/${phone}`
    );
    return response.data;
  }
}
```

## Integration Points

- **Contact Import (Ch 02):** Batch scrubbing during list import prevents adding DNC-listed contacts
- **Real-Time DNC Check (sec-02):** Scrub API results feed into the in-memory DNC database
- **Campaign Dialing (Ch 01):** Pre-dial scrub check for high-risk campaigns (financial services, healthcare)
- **Compliance Reporting (sec-07):** Scrub history and provider coverage for regulatory audit
- **Consent Tracking (sec-05):** Consent records override scrub matches (consented numbers can be called despite DNC)
- **Analytics (Ch 09):** Scrub match rate by provider, list quality scoring, false positive tracking

## Open-Source Tools

- **BullMQ:** Batch scrub job queue with progress tracking and retry logic
- **Redis:** Scrub result cache for fast lookup and TTL management
- **PostgreSQL:** Scrub result persistence and historical tracking
- **axios / node-fetch:** HTTP client for scrub provider API calls
- **csv-parse / papaparse:** Contact list parsing for batch upload
- **Winston / Pino:** Scrub API integration logging for audit trail
- **Prometheus:** Scrub API call metrics, latency, error rate tracking

## Production Considerations

- Scrub API calls have cost implications — batch processing at $0.001-0.005 per number adds up at scale
- API rate limits vary by provider — implement token bucket rate limiting with provider backpressure
- Provider downtime requires automatic failover — maintain at least 2 active providers at all times
- Scrub results have expiration dates — implement proactive re-scrubbing before result expiration
- Match sensitivity must be configurable per campaign — high-risk campaigns use stricter matching
- False positives from scrub APIs can suppress legitimate contacts — implement manual review queue
- Provider SLAs should specify uptime and maximum batch processing time
- Scrub audit trail must include provider response data for regulatory defense
- Webhook-based result delivery is preferred over polling for batch jobs
- International number scrubbing requires providers with global DNC coverage
- Deceased-person scrubbing is mandatory for certain industries (collections, healthcare)
- Household-level matching (same household as DNC-listed number) may be restricted by state regulations
- Scrub API responses should be normalized across providers to a common schema
- Cost allocation tracks scrub spend per campaign for client billing and ROI analysis
