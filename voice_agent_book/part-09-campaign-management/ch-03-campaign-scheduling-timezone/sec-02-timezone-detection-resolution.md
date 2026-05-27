# Section 02: Timezone Detection & Resolution

## Overview

Determining a contact's timezone is critical for compliance and campaign effectiveness. Calling a contact outside their local waking hours is not just ineffective — it's illegal in many jurisdictions. Timezone detection must determine the most likely timezone for each contact using available data sources, handle ambiguous cases, and provide fallback strategies when timezone cannot be reliably determined.

The timezone resolver combines multiple signal sources: phone number area code and prefix mapping, IP geolocation (if available from web forms), user-provided or CRM timezone data, address-based timezone lookup, and behavioral patterns (historical call answer times). Each source produces a timezone with confidence, and the resolver selects the most reliable result.

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
class TimezoneResolver {
  constructor(providers, cache) {
    this.providers = providers; // Ordered by priority
    this.cache = cache;
    this.phoneDb = new NPANXXDatabase(); // Local or API-based
  }

  async resolve(contact) {
    const cacheKey = `tz:${contact.tenant_id}:${contact.id}`;
    
    // Check cache
    const cached = await this.cache.get(cacheKey);
    if (cached) return JSON.parse(cached);

    // Evaluate all available sources
    const sources = [];

    if (contact.crmTimezone) {
      sources.push({
        timezone: contact.crmTimezone,
        confidence: 0.95,
        source: 'crm'
      });
    }

    if (contact.phone) {
      const phoneTz = await this.resolveFromPhone(contact.phone);
      if (phoneTz) sources.push(phoneTz);
    }

    if (contact.address?.state) {
      const addressTz = this.resolveFromAddress(contact.address);
      if (addressTz) sources.push(addressTz);
    }

    // Select best source
    const best = sources.sort((a, b) => b.confidence - a.confidence)[0];
    
    const result = best || {
      timezone: contact.defaultTimezone || 'America/New_York',
      confidence: 0.1,
      source: 'default'
    };

    // Cache for 24 hours
    await this.cache.setex(cacheKey, 86400, JSON.stringify(result));

    return result;
  }

  async resolveFromPhone(phone) {
    // Extract NPA (area code) and NXX (exchange)
    const cleaned = phone.replace(/\D/g, '');
    const npa = cleaned.slice(0, 3);
    const nxx = cleaned.slice(3, 6);
    
    const mapping = await this.phoneDb.lookup(npa, nxx);
    
    if (mapping) {
      return {
        timezone: mapping.timezone,
        confidence: mapping.isLandline ? 0.9 : 0.7,
        source: 'phone_npa_nxx'
      };
    }

    // Fallback to area-code-only mapping
    const areaCode = await this.phoneDb.lookupByAreaCode(npa);
    return areaCode ? {
      timezone: areaCode.timezone,
      confidence: 0.5,
      source: 'phone_area_code'
    } : null;
  }

  resolveFromAddress(address) {
    const stateTimezoneMap = {
      'NY': 'America/New_York',
      'CA': 'America/Los_Angeles',
      'TX': 'America/Chicago',
      'FL': 'America/New_York',
      // ... full US state mapping
    };

    const tz = stateTimezoneMap[address.state];
    if (!tz) return null;

    // City-level refinement would provide better accuracy
    return {
      timezone: tz,
      confidence: 0.6,
      source: 'address_state'
    };
  }
}
```

## Integration Points

- **Phone Validation (sec-02, ch-07):** Phone number parsing provides NPA-NXX extraction
- **Contact Import (Ch 02):** Timezone resolution runs during import for batch processing
- **Dialing Engine (Ch 01):** Resolved timezone determines calling window enforcement
- **Campaign Schedule (sec-01):** Timezone-aware schedule evaluation
- **Compliance (Ch 07):** State-specific regulations depend on resolved location
- **Analytics (Ch 09):** Timezone distribution reporting for campaign planning

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Phone-to-timezone databases are commercially available (e.g., Twilio Lookup, TeloTrack) — budget for API costs
- Area code splits (new area codes splitting from existing ones) can cause inaccurate mappings — keep the database updated
- Mobile numbers cannot be reliably mapped to timezone via area code — consider alternative sources for mobile contacts
- VPN use can make IP geolocation unreliable — treat IP-based timezone with lower confidence
- Timezone caching TTL should account for contacts who move (rare but possible) — 24-48 hour cache is reasonable
- Batch timezone resolution for import should be throttled to avoid rate limits on lookup APIs
- Expose timezone resolution details in the contact detail UI for operator review and manual override
- Contacts in ambiguous timezone zones (state borders, territories) should be flagged for manual review
- Monitor timezone resolution coverage — target >95% of contacts with confidence >0.8
- Fallback to a safe calling window (10 AM - 4 PM ET) when timezone cannot be resolved with confidence
