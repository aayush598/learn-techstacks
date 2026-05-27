# Section 05: Attempt History Tracking

## Overview

Attempt history tracking records every call made to each contact during a campaign, creating a complete audit trail of all outbound activities. Each attempt record captures the timestamp, outcome, duration, agent used (AI or human), route details (carrier, SIP trunk), and any notes or dispositions. This history is essential for compliance verification, retry logic, analytics, and providing operators with complete context on each contact's calling journey.

The attempt history system must support high-volume writes (potentially thousands per second during peak dialing), efficient queries for individual contact history, and aggregations for analytics. History records should be immutable — once written, they are never modified. Corrections are handled via "correction records" that reference the original attempt and provide updated information with an audit trail.

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
class AttemptHistoryService {
  constructor(writeBuffer, prisma, archiveStorage) {
    this.buffer = writeBuffer;
    this.prisma = prisma;
    this.archive = archiveStorage;
  }

  async recordAttempt(attempt) {
    const record = {
      ...attempt,
      id: attempt.id || crypto.randomUUID(),
      created_at: new Date()
    };

    // Write to buffer for batch flush
    await this.buffer.push('attempts', record);

    // If a previous record needs correction
    if (attempt.correctsId) {
      await this.buffer.push('attempt_corrections', {
        original_id: attempt.correctsId,
        correction_id: record.id,
        correction_reason: attempt.correctionReason,
        corrected_at: new Date()
      });
    }

    return record.id;
  }

  async getContactAttempts(contactId, campaignId, options = {}) {
    const cacheKey = `attempts:${campaignId}:${contactId}`;
    
    // Check cache for recent attempts
    const cached = await this.getFromCache(cacheKey);
    if (cached && !options.forceRefresh) {
      return this.applyCorrections(cached);
    }

    // Query from database
    const attempts = await this.prisma.callAttempt.findMany({
      where: {
        contact_id: contactId,
        campaign_id: campaignId,
        ...this.buildDateFilter(options.dateRange)
      },
      orderBy: { timestamp: 'desc' },
      take: options.limit || 50
    });

    // Cache for 1 minute
    await this.cacheAttempts(cacheKey, attempts, 60);

    return this.applyCorrections(attempts);
  }

  async getCampaignAttemptSummary(campaignId, dateRange) {
    // Use materialized view for performance at scale
    const summary = await this.prisma.$queryRaw`
      SELECT 
        outcome,
        COUNT(*) as count,
        AVG(duration_ms) as avg_duration,
        COUNT(DISTINCT contact_id) as unique_contacts
      FROM call_attempts
      WHERE campaign_id = ${campaignId}
        AND timestamp BETWEEN ${dateRange.start} AND ${dateRange.end}
      GROUP BY outcome
    `;

    return summary;
  }

  async batchFlush() {
    // Called by scheduler every 5 seconds
    const batch = await this.buffer.pop('attempts', 1000);
    if (batch.length === 0) return;

    // Bulk insert with conflict handling
    await this.prisma.$executeRaw`
      INSERT INTO call_attempts (
        id, tenant_id, campaign_id, contact_id, 
        attempt_number, timestamp, outcome, duration_ms,
        disposition, ai_agent_id, carrier_info, notes
      ) VALUES ${this.formatBatchValues(batch)}
      ON CONFLICT (id) DO NOTHING
    `;

    return batch.length;
  }

  async archiveOldRecords(retentionDays = 365) {
    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - retentionDays);

    // Move to archive storage
    const oldRecords = await this.prisma.callAttempt.findMany({
      where: { timestamp: { lt: cutoff } },
      take: 10000 // Batch size
    });

    if (oldRecords.length > 0) {
      await this.archive.store('call_attempts', oldRecords);
      await this.prisma.callAttempt.deleteMany({
        where: { id: { in: oldRecords.map(r => r.id) } }
      });
    }
  }

  applyCorrections(attempts) {
    // Replace corrected records with their corrections
    const correctedIds = new Set(
      attempts.filter(a => a.correction_of)
        .map(a => a.correction_of)
    );
    
    return attempts
      .filter(a => !correctedIds.has(a.id) || a.correction_of)
      .sort((a, b) => b.timestamp - a.timestamp);
  }

  buildDateFilter(dateRange) {
    if (!dateRange) return {};
    return {
      timestamp: {
        gte: dateRange.start,
        lte: dateRange.end
      }
    };
  }
}
```

## Integration Points

- **Dialing Engine (Ch 01):** Records attempt after each call completes
- **Telephony Layer (Part 07):** Provides call metadata (duration, status, carrier info)
- **AI Agent (Part 06):** Provides disposition and notes
- **Retry Engine (sec-02 to sec-04):** Reads attempt history for retry logic
- **Analytics (Ch 09, Part 11):** Aggregates attempt data for reporting
- **Compliance Audit (Ch 07):** Attempt history serves as compliance evidence
- **UI:** Contact history timeline displayed in agent and campaign management interfaces

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Attempt history grows rapidly — a campaign making 100,000 calls/day generates 3M records/month. Plan storage and query performance accordingly.
- Write buffer provides resilience — if the database is temporarily unavailable, attempts accumulate in Redis and flush when the DB recovers.
- Index strategy: indexes on (tenant_id, campaign_id, contact_id), (tenant_id, campaign_id, timestamp), and (tenant_id, timestamp) for common query patterns.
- Partitioning by month enables efficient data lifecycle management — older partitions can be compressed or moved to cheaper storage.
- Attempt history must be included in backup and disaster recovery planning — it's often a compliance requirement.
- API exposure should paginate attempts and limit maximum history returned (e.g., 100 most recent).
- Correction records should include the reason and author for full audit traceability.
- Real-time attempt feed via WebSocket enables live monitoring dashboards (Part 11, Ch 02).
- Data retention policies vary by regulation (TCPA: 2 years, HIPAA: 6 years, GDPR: duration of processing) — support configurable retention.
- Export attempt history for external compliance audits in standard formats (CSV, JSON).
