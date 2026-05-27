# Section 08: State-Specific Regulation Handling

## Overview

State-specific regulation handling manages the complex web of telemarketing laws that vary across US states and international jurisdictions. While the federal TCPA provides a baseline for telemarketing regulation, many states have enacted additional requirements: some mandate stricter calling hours, others require state-specific DNC lists, and several impose consent requirements beyond the TCPA minimum. For example, California requires calls to numbers on the state's DNC list even if the caller has an existing business relationship, Florida restricts calls to numbers on its no-solicitation list, and Oklahoma prohibits automated calls entirely unless the caller has express written consent.

The challenge is maintaining a compliance rules engine that can evaluate every call attempt against all applicable state regulations simultaneously. A contact in California may be called from a campaign based in Texas, through a phone number with a Florida area code — each jurisdiction's rules may apply. The rules engine must resolve conflicting requirements (e.g., one state permits calls until 9 PM, another until 8 PM) by applying the strictest applicable rule. The system must also handle international regulations for cross-border campaigns, including Canada's CRTC rules, the UK's ICO regulations, and EU's GDPR e-privacy directive.

## Architecture

```
                State-Specific Regulation Engine

  +------------------+     +------------------+
  | Campaign Config  |     | Contact Profile  |
  | (target states,  |     | (state, timezone,|
  |  consent type)   |     |  area code,      |
  +--------+---------+     |  consent record) |
           |               +--------+---------+
           |                        |
           v                        v
  +---------------------------------------------------+
  |            Regulation Rules Engine                  |
  |                                                    |
  |  Rule Evaluator:                                   |
  |  For each applicable jurisdiction:                  |
  |    1. Load regulation rules for state/jurisdiction |
  |    2. Evaluate: calling hours, consent, DNC,       |
  |       recording consent, auto-dialer restrictions  |
  |    3. Apply strictest rule across all jurisdictions|
  |    4. Return compliance result + applicable rules   |
  +---------------------------------------------------+
           |               |               |
           v               v               v
  +-----------+    +-----------+    +-----------+
  | State DNC |    | Calling   |    | Recording |
  | Rules     |    | Hours     |    | Consent   |
  +-----------+    +-----------+    +-----------+
  | - State DNC   | - Time      | - One-party  |
  |   list check  |   windows   |   consent    |
  | - EBR         | - Day of    | - Two-party  |
  |   exemptions  |   week      |   consent    |
  | - Content     |   rules     | - Notification|
  |   restrictions| - Holiday   |   requirements|
  +-----------+    |   rules    | +-----------+
                   +-----------+
  
  +---------------------------------------------------+
  |          Jurisdiction Resolver                      |
  |                                                    |
  |  Determines which jurisdictions apply to a call:   |
  |  1. Contact's billing address state                |
  |  2. Contact's phone number area code state         |
  |  3. Campaign's originating state                   |
  |  4. Campaign's target states configuration         |
  |  5. Always apply: CA, FL, OK (strictest states)   |
  +---------------------------------------------------+
```

## Design Decisions

- **Rules-as-configuration, not hard-coded:** State regulations are defined in configuration files (YAML/JSON), not in application code. New regulations or regulation changes can be deployed without code changes or system downtime. Trade-off: configuration complexity vs. deployment agility and regulatory responsiveness.

- **Strictest-rule-wins conflict resolution:** When multiple jurisdictions apply to a call, the system applies the most restrictive rule for each dimension (hours, consent, DNC, recording). This ensures compliance with the strictest applicable law. Trade-off: may be over-restrictive for some calls vs. guaranteed compliance across all jurisdictions.

- **Jurisdiction-specific DNC list management:** State DNC lists are maintained separately from the federal DNC list with independent refresh schedules. Each state list has its own rules about exemptions (existing business relationship, prior consent, etc.). Trade-off: multiple list management overhead vs. state-specific compliance accuracy.

- **Geolocation-based jurisdiction inference:** When contact location is unknown, the system infers jurisdiction from the phone number's area code and NPA-NXX prefix. This is less reliable than billing address but provides defensible good-faith effort for jurisdiction determination. Trade-off: inference accuracy (~80-90%) vs. more invasive address collection requirements.

## Implementation Approach

```
interface StateRegulation {
  stateCode: string;
  name: string;
  callingHours: {
    default: { start: string; end: string; timezone: string };
    weekdays?: { start: string; end: string };
    saturday?: { start: string; end: string };
    sunday?: { start: string; end: string };
    holidays?: Array<{ month: number; day: number }>;
  };
  dncRules: {
    hasStateDnc: boolean;
    ebrExemption: boolean;     // Existing business relationship exemption
    consentExemption: boolean;  // Prior written consent exemption
    internalDncRequired: boolean;
    refreshIntervalDays: number;
  };
  consentRequirements: {
    type: 'express_written' | 'express_verbal' | 'implied' | 'ebr';
    recordingConsent: 'one_party' | 'two_party' | 'all_party';
    consentValidDays: number | null;
    withdrawalMethod: 'any_reasonable' | 'specific_channel';
  };
  autoDialerRestrictions: {
    prohibited: boolean;
    exemptions: string[];
  };
  contentRestrictions: {
    requireDoNotCallOption: boolean;
    requireBusinessName: boolean;
    requireCallbackNumber: boolean;
    restrictedContent: string[];
  };
  additionalNotes: string;
}

class StateRegulationEngine {
  constructor() {
    this.regulations = new Map();
  }

  async loadRegulations() {
    // Load from configuration files
    const regulationFiles = await this.loadConfigFiles('regulations/*.yaml');
    for (const file of regulationFiles) {
      const reg = yaml.parse(file.content);
      this.regulations.set(reg.stateCode, reg);
    }
  }

  async evaluateCompliance(contact, campaign) {
    // 1. Determine applicable jurisdictions
    const jurisdictions = this.resolveJurisdictions(contact, campaign);

    // 2. Load regulations for each jurisdiction
    const applicableRegs = jurisdictions
      .map(j => this.regulations.get(j))
      .filter(Boolean);

    // 3. Evaluate each dimension with strictest-rule-wins
    const results = {
      callingHours: this.evaluateCallingHours(applicableRegs),
      dncCompliance: this.evaluateDncRules(applicableRegs, contact, campaign),
      consentCompliance: this.evaluateConsentRules(applicableRegs, contact),
      recordingConsent: this.evaluateRecordingConsent(applicableRegs),
      autoDialer: this.evaluateAutoDialerRules(applicableRegs, campaign),
      contentCompliance: this.evaluateContentRules(applicableRegs, campaign),
      applicableJurisdictions: jurisdictions,
      appliedRegulations: applicableRegs.map(r => r.stateCode),
      strictestRules: {},
      canProceed: true
    };

    // 4. Determine if call can proceed
    results.canProceed = Object.values(results).every(
      r => r === true || r.compliant === true
    );

    return results;
  }

  resolveJurisdictions(contact, campaign) {
    const jurisdictions = new Set();

    // Contact's billing address state (most reliable)
    if (contact.billingState) {
      jurisdictions.add(contact.billingState);
    }

    // Contact's phone number area code state
    const areaCodeState = this.areaCodeToState(
      contact.phone?.substring(2, 5)
    );
    if (areaCodeState && areaCodeState !== contact.billingState) {
      jurisdictions.add(areaCodeState);
    }

    // Campaign's target states
    if (campaign.targetStates) {
      campaign.targetStates.forEach(s => jurisdictions.add(s));
    }

    // Campaign originating state
    if (campaign.originatingState) {
      jurisdictions.add(campaign.originatingState);
    }

    // Always add strictest states if there's uncertainty
    // Some states accept jurisdiction over calls to their residents
    const strictStates = this.getStrictStates();
    strictStates.forEach(s => {
      if (this.isCallSubjectToState(contact, s)) {
        jurisdictions.add(s);
      }
    });

    return Array.from(jurisdictions);
  }

  evaluateCallingHours(regulations) {
    const now = new Date();
    const dayOfWeek = now.getDay(); // 0 = Sunday
    const currentMinutes = now.getHours() * 60 + now.getMinutes();

    // Start with strictest possible (no calling hours)
    let strictest = {
      compliant: false,
      applicableWindow: null,
      appliedState: null
    };
    let earliestStart = 0;
    let latestEnd = 1440;

    for (const reg of regulations) {
      let windowStart: number;
      let windowEnd: number;

      if (reg.callingHours[this.getDayKey(dayOfWeek)]) {
        const hours = reg.callingHours[this.getDayKey(dayOfWeek)];
        windowStart = this.parseTime(hours.start);
        windowEnd = this.parseTime(hours.end);
      } else {
        windowStart = this.parseTime(reg.callingHours.default.start);
        windowEnd = this.parseTime(reg.callingHours.default.end);
      }

      // Check holiday restrictions
      if (this.isHoliday(now, reg.callingHours.holidays)) {
        return {
          compliant: false,
          reason: 'Calling prohibited on holiday',
          appliedState: reg.stateCode,
          holidayName: this.getHolidayName(now)
        };
      }

      // Strictest = latest start, earliest end
      earliestStart = Math.max(earliestStart, windowStart);
      latestEnd = Math.min(latestEnd, windowEnd);
    }

    const compliant = currentMinutes >= earliestStart && currentMinutes <= latestEnd;

    return {
      compliant,
      currentTime: `${now.getHours()}:${now.getMinutes().toString().padStart(2, '0')}`,
      permittedWindow: `${this.formatTime(earliestStart)} - ${this.formatTime(latestEnd)}`,
      appliedStates: regulations.map(r => r.stateCode),
      timezone: 'ET' // All calling hours are in recipient's timezone
    };
  }

  evaluateDncRules(regulations, contact, campaign) {
    const dncResults = [];

    for (const reg of regulations) {
      // Check state-specific DNC list
      if (reg.dncRules.hasStateDnc) {
        const onStateDnc = this.stateDncService.checkNumber(
          contact.phone,
          reg.stateCode
        );

        if (onStateDnc) {
          // Check if any exemption applies
          const ebrExempt = reg.dncRules.ebrExemption && 
            this.hasExistingBusinessRelationship(contact, campaign);
          const consentExempt = reg.dncRules.consentExemption &&
            contact.hasExplicitConsent;

          if (!ebrExempt && !consentExempt) {
            dncResults.push({
              compliant: false,
              state: reg.stateCode,
              reason: `Number on ${reg.stateCode} DNC list`,
              exemptions: { ebrExempt, consentExempt }
            });
          }
        }
      }
    }

    return {
      compliant: dncResults.length === 0,
      violations: dncResults,
      details: dncResults.length > 0 
        ? dncResults.map(r => r.reason).join('; ')
        : 'No DNC violations detected'
    };
  }

  evaluateConsentRules(regulations, contact) {
    const consentIssues = [];

    for (const reg of regulations) {
      const requiredType = reg.consentRequirements.type;

      switch (requiredType) {
        case 'express_written':
          if (contact.consentType !== 'explicit_written') {
            consentIssues.push({
              state: reg.stateCode,
              required: 'express_written_consent',
              current: contact.consentType || 'none'
            });
          }
          break;

        case 'express_verbal':
          if (!['explicit_written', 'explicit_verbal'].includes(contact.consentType)) {
            consentIssues.push({
              state: reg.stateCode,
              required: 'express_consent',
              current: contact.consentType || 'none'
            });
          }
          break;

        case 'ebr':
          // EBR exemption requires active business relationship
          if (!this.hasExistingBusinessRelationship(contact) && 
              !['explicit_written', 'explicit_verbal', 'explicit_electronic'].includes(contact.consentType)) {
            consentIssues.push({
              state: reg.stateCode,
              required: 'ebr_or_consent',
              current: 'neither'
            });
          }
          break;
      }

      // Check consent expiration
      if (reg.consentRequirements.consentValidDays && contact.consentDate) {
        const daysSinceConsent = Math.floor(
          (Date.now() - new Date(contact.consentDate).getTime()) / 86400000
        );
        if (daysSinceConsent > reg.consentRequirements.consentValidDays) {
          consentIssues.push({
            state: reg.stateCode,
            required: `consent_within_${reg.consentRequirements.consentValidDays}_days`,
            current: `${daysSinceConsent}_days_since_consent`
          });
        }
      }
    }

    return {
      compliant: consentIssues.length === 0,
      issues: consentIssues,
      details: consentIssues.length > 0
        ? consentIssues.map(i => `${i.state}: ${i.required}`).join('; ')
        : 'Consent requirements satisfied'
    };
  }

  evaluateRecordingConsent(regulations) {
    // Determine if call recording requires one-party or two-party consent
    let strictestType = 'one_party';

    for (const reg of regulations) {
      const current = this.partyConsentRank(reg.consentRequirements.recordingConsent);
      const strictest = this.partyConsentRank(strictestType);

      if (current > strictest) {
        strictestType = reg.consentRequirements.recordingConsent;
      }
    }

    return {
      compliant: true,
      requirement: strictestType,
      explanation: strictestType === 'two_party'
        ? 'Two-party consent required — all participants must consent to recording'
        : 'One-party consent sufficient — only one participant needs to consent'
    };
  }

  evaluateAutoDialerRules(regulations, campaign) {
    const issues = [];

    for (const reg of regulations) {
      if (reg.autoDialerRestrictions.prohibited) {
        const isExempt = reg.autoDialerRestrictions.exemptions.some(
          e => campaign.type === e
        );

        if (!isExempt && campaign.usesAutoDialer) {
          issues.push({
            state: reg.stateCode,
            reason: 'Auto-dialer prohibited',
            campaignType: campaign.type
          });
        }
      }
    }

    return {
      compliant: issues.length === 0,
      issues,
      details: issues.length > 0
        ? issues.map(i => `${i.state}: ${i.reason}`).join('; ')
        : 'Auto-dialer restrictions satisfied'
    };
  }

  evaluateContentRules(regulations, campaign) {
    const issues = [];

    for (const reg of regulations) {
      // Check if campaign complies with content requirements
      if (reg.contentRestrictions.requireDoNotCallOption &&
          !campaign.hasDoNotCallOption) {
        issues.push({
          state: reg.stateCode,
          requirement: 'Must provide do-not-call option'
        });
      }

      if (reg.contentRestrictions.requireBusinessName &&
          !campaign.includesBusinessName) {
        issues.push({
          state: reg.stateCode,
          requirement: 'Must disclose business name'
        });
      }

      if (reg.contentRestrictions.requireCallbackNumber &&
          !campaign.includesCallbackNumber) {
        issues.push({
          state: reg.stateCode,
          requirement: 'Must provide callback number'
        });
      }

      // Check restricted content
      const campaignContent = campaign.script?.toLowerCase() || '';
      for (const restricted of reg.contentRestrictions.restrictedContent) {
        if (campaignContent.includes(restricted.toLowerCase())) {
          issues.push({
            state: reg.stateCode,
            requirement: `Content contains restricted term: "${restricted}"`
          });
        }
      }
    }

    return {
      compliant: issues.length === 0,
      issues,
      details: issues.length > 0
        ? issues.map(i => `${i.state}: ${i.requirement}`).join('; ')
        : 'Content requirements satisfied'
    };
  }

  getStrictStates() {
    // States with telemarketing regulations stricter than TCPA baseline
    return ['CA', 'FL', 'OK', 'AR', 'IN', 'KY', 'MS', 'MO', 'MT', 'NE', 'NH', 'OH', 'PA', 'SD', 'TN', 'TX', 'WI', 'WY'];
  }

  isCallSubjectToState(contact, stateCode) {
    // Determine if a call is subject to a state's regulations
    // States assert jurisdiction over calls to residents, regardless of where caller is
    if (contact.billingState === stateCode) return true;
    if (this.areaCodeToState(contact.phone?.substring(2, 5)) === stateCode) return true;

    // For states with broad jurisdiction assertions (e.g., CA, FL)
    const broadJurisdictionStates = ['CA', 'FL'];
    if (broadJurisdictionStates.includes(stateCode)) {
      // Assume call could be subject if phone could be in that state
      return true;
    }

    return false;
  }

  areaCodeToState(areaCode) {
    const areaCodeMap = {
      '201': 'NJ', '202': 'DC', '203': 'CT', '205': 'AL', '206': 'WA',
      '207': 'ME', '208': 'ID', '209': 'CA', '210': 'TX', '212': 'NY',
      '213': 'CA', '214': 'TX', '215': 'PA', '216': 'OH', '217': 'IL',
      '218': 'MN', '219': 'IN', '220': 'OH', '224': 'IL', '225': 'LA',
      '228': 'MS', '229': 'GA', '231': 'MI', '234': 'OH', '239': 'FL',
      '240': 'MD', '248': 'MI', '251': 'AL', '252': 'NC', '253': 'WA',
      '254': 'TX', '256': 'AL', '260': 'IN', '262': 'WI', '267': 'PA',
      '269': 'MI', '270': 'KY', '272': 'PA', '276': 'VA', '281': 'TX',
      '301': 'MD', '302': 'DE', '303': 'CO', '304': 'WV', '305': 'FL',
      '307': 'WY', '308': 'NE', '309': 'IL', '310': 'CA', '312': 'IL',
      '313': 'MI', '314': 'MO', '315': 'NY', '316': 'KS', '317': 'IN',
      '318': 'LA', '319': 'IA', '320': 'MN', '321': 'FL', '323': 'CA',
      '325': 'TX', '330': 'OH', '331': 'IL', '334': 'AL', '336': 'NC',
      '337': 'LA', '339': 'MA', '346': 'TX', '347': 'NY', '351': 'MA',
      '352': 'FL', '360': 'WA', '361': 'TX', '364': 'KY', '380': 'OH',
      '385': 'UT', '386': 'FL', '401': 'RI', '402': 'NE', '404': 'GA',
      '405': 'OK', '406': 'MT', '407': 'FL', '408': 'CA', '409': 'TX',
      '410': 'MD', '412': 'PA', '413': 'MA', '414': 'WI', '415': 'CA',
      '417': 'MO', '419': 'OH', '423': 'TN', '424': 'CA', '425': 'WA',
      '430': 'TX', '432': 'TX', '434': 'VA', '435': 'UT', '440': 'OH',
      '442': 'CA', '443': 'MD', '458': 'OR', '469': 'TX', '470': 'GA',
      '475': 'CT', '478': 'GA', '479': 'AR', '480': 'AZ', '484': 'PA',
      '501': 'AR', '502': 'KY', '503': 'OR', '504': 'LA', '505': 'NM',
      '507': 'MN', '508': 'MA', '509': 'WA', '510': 'CA', '512': 'TX',
      '513': 'OH', '515': 'IA', '516': 'NY', '517': 'MI', '518': 'NY',
      '520': 'AZ', '530': 'CA', '531': 'NE', '534': 'WI', '539': 'OK',
      '540': 'VA', '541': 'OR', '551': 'NJ', '559': 'CA', '561': 'FL',
      '562': 'CA', '563': 'IA', '567': 'OH', '570': 'PA', '571': 'VA',
      '573': 'MO', '574': 'IN', '575': 'NM', '580': 'OK', '585': 'NY',
      '586': 'MI', '601': 'MS', '602': 'AZ', '603': 'NH', '605': 'SD',
      '606': 'KY', '607': 'NY', '608': 'WI', '609': 'NJ', '610': 'PA',
      '612': 'MN', '614': 'OH', '615': 'TN', '616': 'MI', '617': 'MA',
      '618': 'IL', '619': 'CA', '620': 'KS', '623': 'AZ', '626': 'CA',
      '628': 'CA', '629': 'TN', '630': 'IL', '631': 'NY', '636': 'MO',
      '640': 'NJ', '641': 'IA', '646': 'NY', '650': 'CA', '651': 'MN',
      '657': 'CA', '660': 'MO', '661': 'CA', '662': 'MS', '667': 'MD',
      '669': 'CA', '678': 'GA', '680': 'NY', '681': 'WV', '682': 'TX',
      '701': 'ND', '702': 'NV', '703': 'VA', '704': 'NC', '706': 'GA',
      '707': 'CA', '708': 'IL', '712': 'IA', '713': 'TX', '714': 'CA',
      '715': 'WI', '716': 'NY', '717': 'PA', '718': 'NY', '719': 'CO',
      '720': 'CO', '724': 'PA', '725': 'NV', '727': 'FL', '731': 'TN',
      '732': 'NJ', '734': 'MI', '737': 'TX', '740': 'OH', '747': 'CA',
      '754': 'FL', '757': 'VA', '760': 'CA', '762': 'GA', '763': 'MN',
      '765': 'IN', '769': 'MS', '770': 'GA', '772': 'FL', '773': 'IL',
      '774': 'MA', '775': 'NV', '779': 'IL', '781': 'MA', '785': 'KS',
      '786': 'FL', '801': 'UT', '802': 'VT', '803': 'SC', '804': 'VA',
      '805': 'CA', '806': 'TX', '808': 'HI', '810': 'MI', '812': 'IN',
      '813': 'FL', '814': 'PA', '815': 'IL', '816': 'MO', '817': 'TX',
      '818': 'CA', '828': 'NC', '830': 'TX', '831': 'CA', '832': 'TX',
      '843': 'SC', '845': 'NY', '847': 'IL', '848': 'NJ', '850': 'FL',
      '854': 'SC', '856': 'NJ', '857': 'MA', '858': 'CA', '859': 'KY',
      '860': 'CT', '862': 'NJ', '863': 'FL', '864': 'SC', '865': 'TN',
      '870': 'AR', '872': 'IL', '878': 'PA', '901': 'TN', '903': 'TX',
      '904': 'FL', '906': 'MI', '907': 'AK', '908': 'NJ', '909': 'CA',
      '910': 'NC', '912': 'GA', '913': 'KS', '914': 'NY', '915': 'TX',
      '916': 'CA', '917': 'NY', '918': 'OK', '919': 'NC', '920': 'WI',
      '925': 'CA', '928': 'AZ', '929': 'NY', '930': 'IN', '931': 'TN',
      '934': 'NY', '936': 'TX', '937': 'OH', '938': 'AL', '940': 'TX',
      '941': 'FL', '947': 'MI', '949': 'CA', '951': 'CA', '952': 'MN',
      '954': 'FL', '956': 'TX', '959': 'CT', '970': 'CO', '971': 'OR',
      '972': 'TX', '973': 'NJ', '978': 'MA', '979': 'TX', '980': 'NC',
      '984': 'NC', '985': 'LA', '986': 'ID', '989': 'MI'
    };
    return areaCodeMap[areaCode] || null;
  }

  parseTime(timeStr) {
    const [hours, minutes] = timeStr.split(':').map(Number);
    return hours * 60 + minutes;
  }

  formatTime(minutes) {
    const h = Math.floor(minutes / 60);
    const m = minutes % 60;
    const period = h >= 12 ? 'PM' : 'AM';
    const displayH = h > 12 ? h - 12 : (h === 0 ? 12 : h);
    return `${displayH}:${m.toString().padStart(2, '0')} ${period}`;
  }

  getDayKey(dayIndex) {
    const days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'];
    return days[dayIndex];
  }

  isHoliday(date, holidays) {
    if (!holidays) return false;
    return holidays.some(h => h.month === date.getMonth() + 1 && h.day === date.getDate());
  }

  partyConsentRank(type) {
    const ranks = { 'one_party': 1, 'two_party': 2, 'all_party': 3 };
    return ranks[type] || 1;
  }
}
```

## Integration Points

- **Campaign Dialing (Ch 01):** Pre-dial regulation check before call placement
- **DNC Engine (sec-02):** State DNC list integration with federal DNC checks
- **Consent Tracking (sec-05):** State-specific consent requirements for verification
- **Call Scheduling (Ch 03):** State-specific calling hours for time-of-day optimization
- **Call Recording (Part 12):** State-specific recording consent requirements
- **Campaign Config (Ch 01):** Per-campaign state targeting configuration
- **Compliance Reporting (sec-07):** State compliance metrics for regulatory filing
- **Analytics (Ch 09):** State-level compliance rate tracking and risk assessment

## Open-Source Tools

- **js-yaml / js-toml:** Regulation configuration file parsing
- **node-geocoder:** Geolocation for area code to state mapping
- **PostgreSQL:** Regulation rules database with state index
- **Redis:** Cached regulation evaluation results for high-volume calls
- **BullMQ:** Scheduled state DNC list refresh jobs
- **node-cron:** Calling hours compliance scheduler
- **Prometheus:** State compliance rate metrics and regulatory risk scoring
- **Winston:** Regulation evaluation audit logging for compliance

## Production Considerations

- State regulations change frequently — monitor legislative updates and deploy configuration updates promptly
- New state regulations can go into effect with as little as 30 days notice — maintain rapid deployment capability
- Area-code-to-state mapping is ~90% accurate — supplement with billing address or IP geolocation
- Conflict resolution (strictest rule wins) may block calls unnecessarily — provide override with legal counsel approval
- State DNC lists require separate subscription and refresh schedules — budget for multiple list subscription costs
- International regulations add significant complexity — consider region-specific compliance modules
- Regulation configuration changes must be version-controlled and audited by compliance team
- Pre-call regulation evaluation must complete in <10ms — cache evaluated results where possible
- Some states (e.g., CA, FL) assert broad jurisdiction — assume their rules apply to most consumer calls
- Regulation changes should have staged rollout with canary testing before full deployment
- Compliance dashboards should show state-level violation rates for targeted risk management
- Consider a compliance rule simulation mode for testing new regulations against historical call data
- Regulation configuration should be human-readable — compliance teams may need to review and approve changes
- Maintain a regulatory change log with effective dates for audit purposes
- State-specific exemptions (e.g., nonprofit calls, political calls, surveys) must be configurable per campaign
