# Section 05: Blackout Dates & Holiday Calendar

## Overview

Blackout dates and holiday calendars define specific days when calling is prohibited or restricted. These include public holidays (when most people do not want to be called), industry-specific blackout periods (e.g., mortgage calls during refinancing blackouts), company-specific dates (corporate events, system maintenance), and special regulatory periods (election-related calling restrictions, disaster-related moratoriums).

The blackout system supports global blackout dates (applied to all campaigns for a tenant), campaign-specific blackout dates, and jurisdiction-specific holidays. It integrates with external holiday calendar APIs for automatic holiday detection and supports recurring blackout dates (e.g., "every year on December 25"). Blackout dates can be full-day (no calls at all) or partial-day (no calls during specific hours).

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
class BlackoutCalendar {
  constructor(holidayApi, prisma) {
    this.holidayApi = holidayApi;
    this.prisma = prisma;
    this.cache = new BlackoutCache();
  }

  async initialize(countryCodes) {
    // Pre-fetch holidays for all relevant countries
    for (const country of countryCodes) {
      const holidays = await this.holidayApi.getHolidays(country, new Date().getFullYear());
      await this.storeHolidays(country, holidays);
    }
  }

  async isBlackedOut(contact, campaign, date) {
    const cacheKey = `blackout:${contact.jurisdiction}:${this.toDateString(date)}`;
    const cached = await this.cache.get(cacheKey);
    if (cached !== null) return cached;

    // Check all blackout sources
    const checks = [
      this.checkPublicHolidays(contact.jurisdiction, date),
      this.checkGlobalBlackouts(date),
      this.checkCampaignBlackouts(campaign.id, date),
      this.checkIndustryBlackouts(campaign.type, contact.jurisdiction, date)
    ];

    const results = await Promise.all(checks);
    const blackout = results.find(r => r.isBlackout);

    const result = blackout || { isBlackout: false };
    
    // Cache for 1 hour
    await this.cache.setex(cacheKey, 3600, result);

    return result;
  }

  async checkPublicHolidays(jurisdiction, date) {
    const holiday = await this.prisma.holiday.findFirst({
      where: {
        jurisdiction: jurisdiction,
        date: {
          gte: this.startOfDay(date),
          lte: this.endOfDay(date)
        }
      }
    });

    if (holiday) {
      return {
        isBlackout: true,
        type: 'public_holiday',
        name: holiday.name,
        severity: holiday.severity, // 'full' | 'partial'
        partialEnd: holiday.partialEnd
      };
    }

    return { isBlackout: false };
  }

  async checkCampaignBlackouts(campaignId, date) {
    const blackout = await this.prisma.campaignBlackout.findFirst({
      where: {
        campaign_id: campaignId,
        date: {
          gte: this.startOfDay(date),
          lte: this.endOfDay(date)
        }
      }
    });

    return blackout
      ? { isBlackout: true, type: 'campaign_blackout', name: blackout.reason }
      : { isBlackout: false };
  }

  async getNextAvailableDate(contact, campaign, fromDate) {
    let checkDate = new Date(fromDate);
    const maxLookAhead = 30; // Don't look more than 30 days ahead

    for (let i = 0; i < maxLookAhead; i++) {
      const result = await this.isBlackedOut(contact, campaign, checkDate);
      if (!result.isBlackout) return checkDate;
      checkDate.setDate(checkDate.getDate() + 1);
    }

    return null; // No available date within look-ahead window
  }

  toDateString(date) {
    return date.toISOString().split('T')[0];
  }
}
```

## Integration Points

- **Calling Window Enforcement (sec-03):** Blackout check is integrated into calling window evaluation
- **Campaign Schedule (sec-01):** Schedule generation excludes blackout dates
- **Campaign Lifecycle (Ch 01):** Campaigns auto-pause when a blackout period begins and resume after
- **Timezone Resolver (sec-02):** Jurisdiction resolution for holiday lookup
- **Notification System:** Alerts operators about upcoming blackout periods
- **Analytics (Ch 09):** Blackout impact on campaign performance metrics

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Public holiday data changes — governments add/remove holidays, change dates. Refresh the holiday database annually
- Blackout periods may be regional within a country (e.g., provincial holidays in Canada, state holidays in India)
- Industry-specific blackouts require domain expertise — mortgage blackout periods vary by lender, not just regulation
- Disaster-related moratoriums (natural disasters, public health emergencies) may be declared at short notice — implement an emergency blackout API
- Blackout date lookup must be fast — integrate into the calling window cache rather than querying separately
- Display upcoming blackout dates prominently in the campaign management dashboard
- Test campaign behavior around year boundaries — a campaign that starts Dec 15 and runs for 30 days crosses multiple holiday periods
- Consider "white days" (dates/times when calling is especially effective) alongside blackout dates for scheduling optimization
- Provide an ICS/calendar export of blackout dates so operators can import them into their personal calendars
- Blackout override capability for emergency campaigns (e.g., public health alerts) with appropriate audit logging
