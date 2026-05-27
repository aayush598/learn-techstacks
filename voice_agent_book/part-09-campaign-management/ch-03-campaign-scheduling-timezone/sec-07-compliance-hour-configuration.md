# Section 07: Compliance Hour Configuration

## Overview

Compliance hour configuration manages the legal time-of-day restrictions on outbound calling that vary by jurisdiction, contact type, and industry. In the US, the TCPA restricts calls to residential lines to 8 AM - 9 PM in the contact's local timezone. However, this varies by state — some states have narrower windows (e.g., Florida restricts to 8 AM - 8 PM). International regulations add further complexity, with the EU's GDPR and ePrivacy Directive, Canada's CRTC rules, and individual country telemarketing laws.

The compliance hours system must support a dynamic rules engine where regulations can be defined, updated, and enforced without code changes. The rules must account for contact type (residential, business, mobile), industry (financial services, healthcare, debt collection), consent status (prior express consent, established business relationship), and jurisdiction (state, province, country). Each rule defines permissible calling windows, applicable days, and exceptions.

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
class ComplianceHourEngine {
  constructor(ruleRepository) {
    this.rules = ruleRepository;
  }

  async getComplianceWindows(contact, campaign) {
    const jurisdiction = await this.resolveJurisdiction(contact);
    const rules = await this.rules.getRulesForJurisdiction(jurisdiction);
    
    // Filter to applicable rules
    const applicable = rules.filter(rule => 
      this.isRuleApplicable(rule, contact, campaign)
    );

    if (applicable.length === 0) {
      return { windows: [], restrictions: [] };
    }

    // Apply most restrictive rule
    const strictest = this.findStrictestRule(applicable);
    
    // Check for exceptions
    const hasException = await this.checkExceptions(contact, campaign, strictest);

    if (hasException && strictest.exceptionWindows) {
      return {
        windows: strictest.exceptionWindows,
        restrictions: [strictest.ruleId],
        exceptionApplied: true
      };
    }

    return {
      windows: strictest.windows,
      restrictions: [strictest.ruleId],
      exceptionApplied: false
    };
  }

  async isCompliant(contact, campaign, currentTime) {
    const result = await this.getComplianceWindows(contact, campaign);
    
    return result.windows.some(w => {
      const localTime = this.toContactTimezone(currentTime, contact.timezone);
      return localTime >= w.start && localTime < w.end;
    });
  }

  findStrictestRule(rules) {
    return rules.reduce((strictest, rule) => {
      // Calculate total weekly calling hours for comparison
      const strictHours = this.totalWeeklyHours(rule.windows);
      const currentHours = this.totalWeeklyHours(strictest.windows);
      
      return strictHours < currentHours ? rule : strictest;
    });
  }

  async checkExceptions(contact, campaign, rule) {
    if (!rule.exceptions || rule.exceptions.length === 0) return false;

    for (const exception of rule.exceptions) {
      switch (exception.type) {
        case 'prior_consent':
          return await this.consentService.hasPriorConsent(contact.id);
        case 'ebr':
          return await this.ebrService.hasEstablishedBusinessRelationship(contact.id);
        case 'transactional':
          return this.isTransactionalCall(campaign.type);
        case 'business':
          return contact.type === 'business';
      }
    }

    return false;
  }

  async resolveJurisdiction(contact) {
    // Resolve hierarchical jurisdiction
    const country = contact.country || 'US';
    const state = contact.state || '';
    const localArea = contact.areaCode || '';

    return {
      country: country,
      state: state ? `${country}-${state}` : undefined,
      local: localArea ? `${country}-${state}-${localArea}` : undefined,
      primary: state ? `${country}-${state}` : country
    };
  }

  totalWeeklyHours(windows) {
    return windows.reduce((total, w) => {
      const hoursPerDay = (w.end.hour - w.start.hour) + 
        (w.end.minute - w.start.minute) / 60;
      return total + (hoursPerDay * (w.days?.length || 7));
    }, 0);
  }
}

// Rule definition example
const tcpaResidentialRule = {
  ruleId: 'tcpa_residential_v2',
  jurisdiction: ['US_ALL'],
  contactTypes: ['residential'],
  effectiveDate: '2024-01-01',
  windows: [
    { days: ['mon','tue','wed','thu','fri','sat'], 
      start: { hour: 8, minute: 0 }, 
      end: { hour: 21, minute: 0 } },
    { days: ['sun'], 
      start: { hour: 8, minute: 0 }, 
      end: { hour: 17, minute: 0 } }
  ],
  exceptions: [
    { type: 'prior_consent', exceptionWindows: [
      { days: ['mon','tue','wed','thu','fri','sat','sun'],
        start: { hour: 8, minute: 0 },
        end: { hour: 21, minute: 0 } }
    ]},
    { type: 'ebr' },
    { type: 'transactional' }
  ]
};
```

## Integration Points

- **Calling Window Enforcement (sec-03):** Compliance windows are intersected with calling windows
- **Timezone-Aware Dialing Engine (sec-06):** Compliance check integrated into dialing decision
- **Consent Service (Ch 07):** Exception checking (prior consent, EBR)
- **Campaign Configuration UI:** Admin interface for rule management
- **Compliance Audit (Ch 07):** Compliance check logging for audit trail
- **Analytics (Ch 09):** Compliance-related call blocking tracking

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Compliance rules change frequently — build a rule update workflow with staging, review, and activation
- Rule versioning is essential for audit — campaigns must be evaluated against rules in effect at call time, not current rules
- Most-restrictive-wins approach may be overly conservative — consider "stricter of applicable" rather than strictest of all
- Exception tracking must be rigorous — if a call relied on an "established business relationship" exception, the EBR evidence must be recorded
- Compliance hour configuration should be part of the initial tenant onboarding, not an afterthought
- International tenants need jurisdiction-specific rules — provide a rule library that covers major jurisdictions
- Monitor compliance rule violations separately from other metrics for management reporting
- Test compliance rules with automated tests that verify correct behavior for each jurisdiction
- Provide a compliance check preview tool in the UI — "Test if call to this contact would be compliant right now"
- Regulation changes often include grandfathering periods — support effective-date-based rule activation
