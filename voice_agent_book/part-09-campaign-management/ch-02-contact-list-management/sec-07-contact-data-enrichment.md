# Section 07: Contact Data Enrichment

## Overview

Contact data enrichment enhances imported contacts with additional information from third-party sources, improving campaign effectiveness through better targeting, personalization, and contact quality. Enrichment adds missing data points (e.g., demographic information), validates existing data (e.g., phone number verification), and appends valuable attributes (e.g., income level, homeowner status, purchase intent scores).

The enrichment pipeline operates as an optional post-processing step after contact import. Contacts flow through enrichment providers that add or update fields. The system supports a provider abstraction layer, allowing multiple enrichment sources to be configured per tenant. Enrichment can happen in real-time for small batches or as a background job for large imports. Cost management is critical since most enrichment providers charge per record or per lookup.

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
class EnrichmentOrchestrator {
  constructor(providers, costManager, contactService) {
    this.providers = providers; // Ordered provider chain
    this.costManager = costManager;
    this.contacts = contactService;
  }

  async enrichContact(contactId, tenantContext) {
    const contact = await this.contacts.getById(contactId);
    const budget = await this.costManager.getBudget(tenantContext);

    let enrichedData = { ...contact };

    for (const provider of this.providers) {
      if (!provider.isEligible(contact)) continue;

      const cost = provider.estimateCost(contact);
      if (!this.costManager.canSpend(tenantContext, cost)) {
        await this.costManager.logSkip(provider.name, 'budget_exceeded');
        continue;
      }

      try {
        const result = await provider.enrich(contact);
        
        this.costManager.recordSpend(tenantContext, provider.name, cost);

        enrichedData = this.mergeEnrichment(
          enrichedData,
          result.data,
          provider.name,
          result.confidence
        );
      } catch (error) {
        await this.costManager.logError(provider.name, error);
        // Continue with next provider on failure
      }
    }

    return enrichedData;
  }

  async batchEnrich(contactIds, tenantContext) {
    const batchSize = 100;
    const results = [];

    for (let i = 0; i < contactIds.length; i += batchSize) {
      const batch = contactIds.slice(i, i + batchSize);
      const enriched = await Promise.all(
        batch.map(id => this.enrichContact(id, tenantContext))
      );
      results.push(...enriched);
    }

    return results;
  }

  mergeEnrichment(contact, newData, providerName, confidence) {
    const merged = { ...contact };

    for (const [field, value] of Object.entries(newData)) {
      if (value !== null && value !== undefined) {
        merged[field] = value;
        merged[`${field}_source`] = providerName;
        merged[`${field}_confidence`] = confidence;
      }
    }

    return merged;
  }
}

class PhoneValidationProvider {
  async enrich(contact) {
    const response = await axios.post('https://api.example.com/phone/validate', {
      phone: contact.phone,
      countryCode: contact.country || 'US'
    });

    return {
      data: {
        phoneType: response.data.line_type, // mobile, landline, voip
        isActive: response.data.status === 'active',
        carrier: response.data.carrier,
        countryCode: response.data.country_code,
        timezone: response.data.timezone,
        isPrepaid: response.data.is_prepaid
      },
      confidence: response.data.quality_score
    };
  }

  estimateCost() {
    return { credits: 1, currency: 'USD', amount: 0.005 };
  }

  isEligible(contact) {
    return !!contact.phone;
  }
}
```

## Integration Points

- **Contact Import Pipeline (sec-01, sec-02):** Enrichment runs as post-import processing step
- **Campaign Engine (Ch 01):** Enriched fields are available for personalization and segmentation
- **Cost Management/Billing (Part 17):** Enrichment costs tracked per tenant for billing
- **Analytics (Ch 09):** Enrichment coverage rate and campaign lift measurement
- **Personalization (Ch 06):** Enriched data feeds dynamic script personalization

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Enrichment adds per-contact cost — track ROI by measuring campaign lift from enriched vs. non-enriched contacts
- Cache enrichment results aggressively — enriched data rarely changes and redundant lookups waste money
- Set per-tenant enrichment budgets and alert when approaching limits
- Some enrichment providers have rate limits — implement token bucket throttling per provider
- Enrichment confidence scores should be exposed in the UI so users can make informed decisions
- Privacy regulations (GDPR, CCPA) may restrict what enrichment is permissible — check jurisdiction before enriching
- Provide an enrichment preview feature showing what data would be appended before committing
- Enrichment failure should not block the import pipeline — enrichments are best-effort enhancements
- Carrier and timezone enrichment is particularly valuable for campaign scheduling optimization
- Consider a "data freshness" score that decays over time — re-enrich contacts with stale enrichment data
