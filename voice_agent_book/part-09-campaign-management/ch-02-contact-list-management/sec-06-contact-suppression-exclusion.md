# Section 06: Contact Suppression & Exclusion

## Overview

Contact suppression prevents specific contacts from being called, ensuring compliance with opt-out requests, protecting against repeat calling of bounced or invalid numbers, and respecting contact preferences. The suppression system must support multiple suppression list types — global Do-Not-Call (DNC), campaign-specific exclusion lists, industry-specific suppression (e.g., bankruptcy for collections), and temporary suppression for contacts who recently opted out.

Suppression is different from DNC compliance: DNC covers regulatory required lists, while suppression covers business-driven exclusions (e.g., contacts who asked to be contacted via email only, competitors, or known invalid numbers). The suppression check must happen in real-time before every dial attempt, as suppression lists can change between retry attempts. The system must also support suppression list imports, management UI, and audit logging.

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
class SuppressionEngine {
  constructor(redis, prisma) {
    this.redis = redis;
    this.prisma = prisma;
    this.cache = new SuppressionCache(redis);
  }

  async isSuppressed(contact, campaign, tenantContext) {
    // Check in-memory cache first (sub-millisecond)
    const cacheKey = `suppress:${tenantContext.tenantId}:${contact.id}`;
    const cached = await this.redis.get(cacheKey);
    if (cached !== null) return JSON.parse(cached);

    // Multi-layer check
    const checks = [
      this.checkTemporarySuppression(contact.id, tenantContext),
      this.checkGlobalDnc(contact.phone, tenantContext),
      this.checkCampaignExclusion(contact.id, campaign.id),
      this.checkIndustryRegulation(contact, campaign),
      this.checkChannelPreference(contact, 'voice')
    ];

    const results = await Promise.all(checks);
    const suppressed = results.find(r => r.suppressed);

    // Cache result for 5 seconds
    await this.redis.setex(cacheKey, 5, JSON.stringify(suppressed || null));

    return suppressed;
  }

  async checkGlobalDnc(phone, tenantContext) {
    // Bloom filter check for O(1) performance
    const inBloom = await this.redis.bf.exists(
      `dnc:bloom:${tenantContext.tenantId}`,
      phone
    );
    
    if (!inBloom) return { suppressed: false };

    // Confirm in database (Bloom filter may have false positives)
    const dncEntry = await this.prisma.dncEntry.findUnique({
      where: {
        tenant_phone: {
          tenant_id: tenantContext.tenantId,
          phone
        }
      }
    });

    return dncEntry
      ? { suppressed: true, reason: 'global_dnc', source: dncEntry.source }
      : { suppressed: false };
  }

  async addToSuppression(contact, reason, expiry, actor) {
    const entry = await this.prisma.suppressionEntry.create({
      data: {
        tenant_id: contact.tenant_id,
        contact_id: contact.id,
        phone: contact.phone,
        reason,
        source: actor,
        expires_at: expiry,
        created_at: new Date()
      }
    });

    // Invalidate cache
    await this.redis.del(`suppress:${contact.tenant_id}:${contact.id}`);

    return entry;
  }
}

class SuppressionCache {
  constructor(redis) {
    this.redis = redis;
  }

  async warmCache(tenantId) {
    // Preload active suppressions into Redis for fast lookups
    const suppressions = await prisma.suppressionEntry.findMany({
      where: {
        tenant_id: tenantId,
        OR: [
          { expires_at: null },
          { expires_at: { gt: new Date() } }
        ]
      }
    });

    const pipeline = this.redis.pipeline();
    for (const s of suppressions) {
      const key = `suppress:${tenantId}:${s.contact_id}`;
      pipeline.setex(key, 300, JSON.stringify(s));
    }
    await pipeline.exec();
  }
}
```

## Integration Points

- **Dialing Engine (Ch 01):** Calls suppression check before every dial attempt
- **DNC Service (Ch 07):** Regulatory DNC lists feed into the global suppression layer
- **Contact Service:** Opt-out actions create suppression entries
- **Campaign Service:** Campaign-specific exclusion lists are managed per campaign
- **Compliance Reporting (Ch 07):** Suppression activity is included in compliance reports
- **Analytics (Ch 09):** Suppression rate tracking and trend analysis

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Suppression check must complete in under 50ms to avoid delaying the dialing pipeline
- Use Redis cache with a short TTL (5 seconds) to balance freshness with performance
- Temporary suppression cleanup should run as a scheduled job every 15 minutes
- Suppression list import can be large (millions of records) — use the same bulk import pipeline as contact lists
- Implement a "suppression test" UI tool where operators can check if a specific number would be suppressed
- Suppression should persist across campaign lifecycles — a contact suppressed in one campaign should remain suppressed across all
- Consider "soft" suppression for marketing preference changes vs. "hard" suppression for opt-out
- Export suppression lists for regulatory submission and external verification
- Monitor suppression rate — an unexpected spike may indicate a data issue or compliance event
- Suppression reason should be exposed in call attempt history for transparency
