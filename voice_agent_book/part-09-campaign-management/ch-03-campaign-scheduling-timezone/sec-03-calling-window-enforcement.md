# Section 03: Calling Window Enforcement

## Overview

Calling window enforcement ensures that calls are only placed during legally and socially acceptable hours for each contact's location. Unlike campaign schedules (when the business wants to call), calling windows define when contacts can be called based on timezone-specific regulations and social norms. The enforcement layer intersects campaign schedules with contact-level calling windows to determine the actual allowable dialing times.

Calling windows are typically defined as configurable ranges (e.g., 9 AM - 8 PM for weekdays, 10 AM - 6 PM for Sundays) with variations by contact type (residential vs. business) and jurisdiction (state-specific regulations). The enforcement system must check calling windows at the moment of dialing, accounting for real-time changes like DST transitions and the contact's current location (if traveling).

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
class CallingWindowEnforcer {
  constructor(timezoneResolver, complianceConfig) {
    this.timezone = timezoneResolver;
    this.compliance = complianceConfig;
  }

  async getCallingWindow(contact, campaign, currentTime = new Date()) {
    const tzInfo = await this.timezone.resolve(contact);
    const contactTz = tzInfo.timezone;

    // Get all applicable windows
    const campaignWindows = this.getCampaignWindows(campaign, contactTz, currentTime);
    const contactTypeWindows = this.getContactTypeWindows(
      contact.type || 'residential',
      contactTz,
      currentTime
    );
    const complianceWindows = this.getComplianceWindows(
      contact.jurisdiction,
      contact.type,
      contactTz,
      currentTime
    );

    // Intersect all windows
    const intersection = this.intersectWindows([
      campaignWindows,
      contactTypeWindows,
      complianceWindows
    ]);

    return {
      canDial: intersection.some(w => this.isWithin(w, currentTime)),
      windows: intersection,
      nextWindowStart: intersection.length > 0 ? intersection[0].start : null,
      constraints: this.getActiveConstraints(campaign, contact)
    };
  }

  async canDialNow(contact, campaign) {
    const window = await this.getCallingWindow(contact, campaign);
    return window.canDial;
  }

  intersectWindows(windowSets) {
    if (windowSets.length === 0) return [];
    if (windowSets.length === 1) return windowSets[0];

    let result = windowSets[0];

    for (let i = 1; i < windowSets.length; i++) {
      result = this.intersectTwo(result, windowSets[i]);
      if (result.length === 0) return [];
    }

    return result;
  }

  intersectTwo(windowsA, windowsB) {
    const result = [];
    
    for (const a of windowsA) {
      for (const b of windowsB) {
        const start = new Date(Math.max(a.start.getTime(), b.start.getTime()));
        const end = new Date(Math.min(a.end.getTime(), b.end.getTime()));
        
        if (start < end) {
          result.push({ start, end });
        }
      }
    }

    return result.sort((a, b) => a.start - b.start);
  }

  getComplianceWindows(jurisdiction, contactType, timezone, date) {
    // Look up jurisdiction-specific calling hours
    const rules = this.compliance.getRules(jurisdiction, contactType);
    const dayOfWeek = date.toLocaleDateString('en-US', { weekday: 'long', timeZone: timezone });
    
    const windows = [];
    for (const rule of rules) {
      if (rule.days.includes(dayOfWeek)) {
        const start = this.createTimeInZone(date, rule.startHour, rule.startMin, timezone);
        const end = this.createTimeInZone(date, rule.endHour, rule.endMin, timezone);
        windows.push({ start, end, rule: rule.name });
      }
    }

    return windows;
  }

  createTimeInZone(date, hours, minutes, timezone) {
    const inZone = new Date(date.toLocaleString('en-US', { timeZone: timezone }));
    inZone.setHours(hours, minutes, 0, 0);
    return inZone;
  }
}
```

## Integration Points

- **Timezone Resolver (sec-02):** Provides contact timezone for window calculation
- **Campaign Schedule (sec-01):** Campaign window is the first constraint in the intersection
- **Compliance Engine (Ch 07):** Compliance calling hours are intersected with other windows
- **Dialing Engine (Ch 01):** Calls canDialNow before every dial attempt
- **Retry Engine (Ch 04):** Uses nextWindowStart for smarter retry scheduling
- **Analytics (Ch 09):** Tracks calls blocked by window enforcement for reporting

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Window evaluation must be sub-10ms since it runs before every dial attempt
- Cache window evaluation results per contact-campaign pair with a 5-minute TTL
- Intersection of three+ window sets can result in empty windows — detect and report to campaign operators
- Compliance windows should be updated automatically when regulations change — consider a regulation database API subscription
- Business vs. residential contact type affects calling windows — verify contact type during import
- Calling window violations should trigger an immediate campaign pause and alert
- "Next window" information should be exposed in the contact attempt history UI
- Batch window pre-calculation for retry queues can improve scheduling efficiency
- Test edge cases: contacts on ships (timezone changes frequently), contacts with no timezone, contacts in regions with extreme DST rules
- Provide a window visualization in the campaign configuration UI showing the effective calling hours
