# Section 01: US Regulatory Framework

## Overview of US Regulations

The US regulatory landscape for AI voice agents is complex and fragmented, with federal laws (TCPA, FCC regulations) overlapping with state-level laws (two-party consent, state privacy laws). Compliance is not optional — penalties range from $500 to $50,000+ per violation.

```
US Regulatory Landscape
┌─────────────────────────────────────────────────────────────────────────┐
│ Federal Regulations                                                     │
│ ┌────────────────────┐ ┌────────────────────┐ ┌────────────────────┐  │
│ │ TCPA              │ │ FCC Regulations    │ │ FTC Act Section 5  │  │
│ │ Telephone Consumer│ │ Do-Not-Call rules  │ │ Unfair/deceptive   │  │
│ │ Protection Act    │ │ Call abandonment   │ │ practices          │  │
│ │ Private right of  │ │ STIR/SHAKEN        │ │ AI disclosure      │  │
│ │ action            │ │                    │ │ guidelines         │  │
│ └────────────────────┘ └────────────────────┘ └────────────────────┘  │
├─────────────────────────────────────────────────────────────────────────┤
│ State-Level Regulations                                                 │
│ ┌────────────────────┐ ┌────────────────────┐ ┌────────────────────┐  │
│ │ Two-Party Consent  │ │ State Privacy Laws │ │ State TCPA        │  │
│ │ (11 states)        │ │ • CCPA (CA)        │ │ Supplements       │  │
│ │ All-party consent  │ │ • CPA (CO)         │ │ • FL, OK, RI      │  │
│ │ for recording      │ │ • CTDPA (CT)       │ │ have own laws     │  │
│ └────────────────────┘ └────────────────────┘ └────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

## TCPA (Telephone Consumer Protection Act)

**Scope:** Governs outbound calls, auto-dialers, prerecorded voices, and SMS messages. **Enforcement:** FCC + private right of action ($500-$1,500 per violation, statutory damages). **Class action risk:** TCPA class actions regularly settle for $5M-$50M+.

### Key Requirements for Voice AI
- **Express consent:** Prior written consent required for telemarketing calls using auto-dialer or prerecorded voice.
- **Opt-out mechanism:** Must provide opt-out at start of each call (press 1 to opt out, or verbal opt-out).
- **Call time restrictions:** 8:00 AM - 9:00 PM (local time of called party).
- **Identification:** Must identify caller name and purpose of call within first seconds.
- **Do-Not-Call:** Must scrub against DNC registry (national + state-specific + company-specific).
- **Record keeping:** Maintain consent records for 5+ years.

### TCPA Compliance Architecture

```typescript
interface TCPACompliance {
  consent: {
    type: 'prior_express_written' | 'prior_express_verbal' | 'established_business_relationship';
    obtainedAt: Date;
    method: 'web_form' | 'verbal_during_call' | 'written_signature';
    record: string; // URL to consent evidence
    scope: string; // what they consented to
  };
  
  callRestrictions: {
    timeZone: string;
    allowedStartHour: number; // 8
    allowedEndHour: number; // 21
    dayOfWeek: ('mon' | 'tue' | 'wed' | 'thu' | 'fri' | 'sat' | 'sun')[];
  };
  
  optOut: {
    mechanism: ('press_1' | 'verbal_i_opt_out' | 'text_stop');
    confirmationRequired: boolean;
    optOutRecord: string; // URL to recording of opt-out
  };
  
  dncScrubbing: {
    nationalRegistry: boolean;
    stateRegistries: string[];
    companyList: string[];
    scrubFrequency: 'realtime' | 'daily' | 'weekly';
    lastScrubDate: Date;
  };
}

function validateTCPABeforeCall(call: OutboundCall): TCPAValidation {
  const consent = getConsent(call.phoneNumber);
  const dncStatus = checkDNC(call.phoneNumber);
  const timeCheck = isWithinAllowedHours(call.scheduledAt, getTimeZone(call.phoneNumber));
  
  if (!consent || !consent.obtainedAt) {
    return { allowed: false, reason: 'No consent', blocking: true };
  }
  if (dncStatus.onNationalRegistry && !consent.type.includes('written')) {
    return { allowed: false, reason: 'DNC registered', blocking: true };
  }
  if (!timeCheck.allowed) {
    return { allowed: false, reason: `Outside hours: ${timeCheck.reason}`, blocking: true };
  }
  
  return { allowed: true };
}
```

## FCC Regulations

**STIR/SHAKEN:** Mandatory caller ID authentication (CSTP). Voice AI platforms must sign calls with A-level attestation. **Call abandonment:** <3% abandonment rate for predictive dialers. Must play a recorded message if abandoned. **AI disclosure:** FCC proposed rules requiring AI disclosure on calls (2024+). Likely to require "This call is from an AI voice agent" disclosure.

## State Consent Laws

### Two-Party Consent States (11)
California, Connecticut, Florida, Illinois, Maryland, Massachusetts, Montana, New Hampshire, Pennsylvania, Washington, Oregon.

**Requirement:** ALL parties must consent to call recording. **Implementation:** Verbal consent prompt at call start: "This call may be recorded for quality assurance purposes. Do you consent?" Must capture and store the consent. **One-party states:** Only the caller must consent (easier, but still notify).

### State Privacy Laws
- **CCPA (California):** Right to know, delete, opt out of sale of personal information.
- **CPA (Colorado):** Similar to CCPA with universal opt-out.
- **CTDPA (Connecticut):** Similar requirements.
- **Additional states:** VA, UT, IA, IN, TN, MT, OR, TX (growing list).

## Penalty Exposure

| Violation | Per Incident | Max Penalty | Risk for 10K calls |
|-----------|-------------|-------------|-------------------|
| TCPA (no consent) | $500 - $1,500 | No cap (class action) | $5M-$15M |
| TCPA (DNC violation) | $500 - $1,500 | No cap | $5M-$15M |
| Two-party consent | $5,000+ per state | Varies | $500K-$5M |
| STIR/SHAKEN violation | FCC enforcement | $10K/day | $100K+ |

## Implementation Requirements

- **Consent collection:** Capture verbal or digital consent before recording/outbound calls
- **DNC scrubbing:** Real-time DNC check before every outbound call
- **Time zone detection:** Accurate geo-lookup of phone numbers for call time compliance
- **State detection:** Identify caller's state to apply correct consent laws
- **Recording logs:** Immutable audit trail of consent + call recordings + opt-outs
- **Opt-out processing:** Immediate opt-out with confirmation, company-wide suppression

## Tools & Resources

- **DNC scrubbing:** DNC.com, CallerID, Gryphon Networks
- **Consent management:** Transcend, OneTrust
- **Time zone detection:** Twilio (carrier lookup), Telnyx, MaxMind
- **Call recording compliance:** Verified consent, audit logs
- **Legal counsel:** Telecommunications law specialist (Wiley Rein, Kelley Drye)
- **Compliance automation:** Vanta, Drata
