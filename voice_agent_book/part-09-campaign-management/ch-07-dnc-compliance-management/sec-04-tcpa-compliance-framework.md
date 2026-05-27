# Section 04: TCPA Compliance Framework

## Overview

The Telephone Consumer Protection Act (TCPA) is the primary US federal law governing outbound telemarketing calls. TCPA compliance is one of the highest-risk areas for voice agent SaaS platforms — violations carry statutory damages of $500-$1,500 per call, and class action lawsuits can result in multi-million dollar settlements. The TCPA compliance framework must be baked into every layer of the campaign management system, not bolted on as an afterthought.

Key TCPA requirements include: prior express written consent for autodialed or prerecorded calls to mobile numbers, time-of-day restrictions (8 AM - 9 PM in the consumer's local time), do-not-call list compliance, caller ID transmission, opt-out mechanisms, and recordkeeping. The framework enforces these requirements through configurable rules, automated checks before every call, and comprehensive audit logging.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              TCPA Compliance Framework                       │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐   │
│  │  TCPA Requirements Check (pre-dial)                  │   │
│  │                                                      │   │
│  │  1. Consent Verification                            │   │
│  │     Written consent on file?                         │   │
│  │     Consent method recorded? (web, IVR, paper)       │   │
│  │     Consent timestamp < 18 months?                   │   │
│  │                                                      │   │
│  │  2. Calling Time Compliance                         │   │
│  │     Current time in contact's timezone               │   │
│  │     Weekday: 8 AM - 9 PM                            │   │
│  │     Weekend: 10 AM - 6 PM (stricter)                │   │
│  │                                                      │   │
│  │  3. DNC List Compliance                             │   │
│  │     National DNC checked within 31 days             │   │
│  │     Internal DNC checked                            │   │
│  │     EBR exception documented if claimed             │   │
│  │                                                      │   │
│  │  4. Caller ID Compliance                            │   │
│  │     Valid originating phone number                  │   │
│  │     Number not blocked or spoofed                   │   │
│  │     CNAM (caller name) displayed                    │   │
│  │                                                      │   │
│  │  5. Recording Consent                               │   │
│  │     One-party or two-party state check              │   │
│  │     Consent recorded if required                    │   │
│  │                                                      │   │
│  │  6. Opt-Out Mechanism                               │   │
│  │     "Press 2 to opt out" available                  │   │
│  │     Opt-out processed immediately                   │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Compliance Check Result                             │   │
│  │  PASS: Allow call [ ]  FAIL: Block call [✗]         │   │
│  │  Violations detected: ["consent_expired"]            │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Design Decisions

- **Layered compliance enforcement:** Compliance is enforced at multiple levels — system configuration (blocking non-compliant campaign types), campaign setup (validating configuration against regulations), pre-dial checks (per-call verification), and post-call audit (detecting violations in completed calls). Trade-off: multi-layer overhead vs. defense-in-depth compliance.

- **Strictest-jurisdiction enforcement:** When a call spans multiple jurisdictions (federal, state, local), the strictest applicable rule is enforced. This over-restricts some calls but ensures compliance across all applicable regulations. Trade-off: reduced calling opportunities vs. risk elimination.

- **Consent evidence storage:** Every call relies on a specific consent record that is captured and stored with full provenance (when, how, what was consented to). If a call is challenged, the consent record is the primary defense. Trade-off: storage and management overhead vs. legal protection.

- **Automated compliance updates:** TCPA regulations change (FCC rulings, court decisions, state laws). The compliance framework supports live updates to rules without system downtime. Trade-off: update mechanism complexity vs. regulatory agility.

## Implementation Approach

```
class TcpaComplianceEngine {
  constructor(consentService, dncService, timeEnforcer, recordingService) {
    this.consent = consentService;
    this.dnc = dncService;
    this.time = timeEnforcer;
    this.recording = recordingService;
  }

  async preCallCheck(contact, campaign) {
    startTime = Date.now();
    const violations = [];

    // 1. Consent check
    const consentCheck = await this.checkConsent(contact, campaign);
    if (!consentCheck.passed) {
      violations.push({
        requirement: 'consent',
        severity: 'critical',
        details: consentCheck.reason,
        action: 'block_call'
      });
    }

    // 2. Time-of-day check
    const timeCheck = await this.time.isWithinTcpaWindow(contact);
    if (!timeCheck.compliant) {
      violations.push({
        requirement: 'calling_time',
        severity: 'critical',
        details: `Outside TCPA calling window. Current time: ${timeCheck.currentLocalTime}`,
        action: 'block_call'
      });
    }

    // 3. DNC check
    const dncCheck = await this.dnc.check(contact.phone, contact.tenantId, campaign.id);
    if (dncCheck.blocked) {
      violations.push({
        requirement: 'dnc',
        severity: 'critical',
        details: `Number on ${dncCheck.source} DNC list`,
        action: 'block_call'
      });
    }

    // 4. Caller ID check
    if (!this.isValidCallerId(campaign.callerId)) {
      violations.push({
        requirement: 'caller_id',
        severity: 'high',
        details: 'Invalid or unregistered caller ID',
        action: 'block_call'
      });
    }

    // 5. Recording consent check
    if (this.requiresConsent(contact.jurisdiction)) {
      const hasConsent = await this.recording.hasConsent(contact.id);
      if (!hasConsent) {
        violations.push({
          requirement: 'recording_consent',
          severity: 'high',
          details: `Two-party consent state (${contact.jurisdiction}) — consent required`,
          action: 'block_recording'
        });
      }
    }

    // 6. Opt-out mechanism check
    if (!this.hasOptOutMechanism(campaign)) {
      violations.push({
        requirement: 'opt_out',
        severity: 'high',
        details: 'Campaign must provide opt-out mechanism (e.g., "Press 2")',
        action: 'block_call'
      });
    }

    // Log compliance check
    await this.logCheck({
      contactId: contact.id,
      campaignId: campaign.id,
      passed: violations.filter(v => v.action === 'block_call').length === 0,
      violations,
      checkDurationMs: Date.now() - startTime,
      timestamp: new Date()
    });

    return {
      passed: violations.filter(v => v.action === 'block_call').length === 0,
      violations,
      warnings: violations.filter(v => v.action === 'block_recording')
    };
  }

  async checkConsent(contact, campaign) {
    // Determine required consent level based on campaign type and jurisdiction
    const consentLevel = this.getRequiredConsentLevel(campaign);
    
    const consent = await this.consent.getLatestConsent(
      contact.id,
      'telemarketing',
      campaign.brandId
    );

    if (!consent) {
      return {
        passed: false,
        reason: `No ${consentLevel} consent on file for telemarketing calls`
      };
    }

    // Check consent validity
    if (consent.expiresAt && new Date(consent.expiresAt) < new Date()) {
      return {
        passed: false,
        reason: `Consent expired on ${consent.expiresAt}`
      };
    }

    // Check consent covers this type of contact
    if (consent.scope === 'email' || consent.channel !== 'voice') {
      return {
        passed: false,
        reason: 'Consent does not cover voice calls'
      };
    }

    return { passed: true, consent };
  }

  getRequiredConsentLevel(campaign) {
    // TCPA requires "prior express written consent" for autodialed/prerecorded calls
    // to mobile phones. "Prior express consent" is needed for non-autodialed calls.
    if (campaign.usesAutoDialer || campaign.usesPrerecorded) {
      return 'prior_express_written_consent';
    }
    return 'prior_express_consent';
  }

  requiresConsent(jurisdiction) {
    const twoPartyStates = [
      'US-CA', 'US-CT', 'US-FL', 'US-IL', 'US-MD', 'US-MA',
      'US-MT', 'US-NH', 'US-PA', 'US-WA'
    ];
    return twoPartyStates.includes(jurisdiction);
  }

  isValidCallerId(phoneNumber) {
    // Must be a valid, non-premium number (not 900, etc.)
    const cleaned = phoneNumber.replace(/\D/g, '');
    if (cleaned.length < 10) return false;
    const areaCode = cleaned.slice(0, 3);
    // Check against known invalid area codes
    const invalidPrefixes = ['900', '976', '555']; // Premium rate numbers
    return !invalidPrefixes.includes(areaCode);
  }

  hasOptOutMechanism(campaign) {
    // Campaign must provide clear opt-out mechanism
    return campaign.script.includes('opt-out') || 
           campaign.script.includes('don\'t call') ||
           campaign.script.includes('press') ||
           campaign.hasOptOutDtmf;
  }

  async logCheck(check) {
    // Immutable compliance check log
    await this.db.tcpaCheck.create({
      data: {
        ...check,
        violations: JSON.stringify(check.violations)
      }
    });
  }

  async generateComplianceReport(tenantId, dateRange) {
    const checks = await this.db.tcpaCheck.findMany({
      where: {
        tenant_id: tenantId,
        timestamp: { gte: dateRange.start, lte: dateRange.end }
      }
    });

    return {
      totalChecks: checks.length,
      passedChecks: checks.filter(c => c.passed).length,
      blockedCalls: checks.filter(c => !c.passed).length,
      violationsByType: this.aggregateViolations(checks),
      complianceRate: checks.filter(c => c.passed).length / checks.length
    };
  }
}
```

## Integration Points

- **Consent Service (sec-05):** Provides consent records for pre-call verification
- **DNC Engine (sec-02):** DNC compliance check
- **Calling Window Enforcer (Ch 03, sec-03):** TCPA time window enforcement
- **Recording Service (Part 12):** Recording consent management
- **Campaign Config (Ch 01):** TCPA-relevant campaign settings (auto-dialer, prerecorded)
- **Compliance Audit (sec-07):** TCPA check logging for regulatory submission
- **Analytics (Ch 09):** TCPA compliance rate trending

## Open-Source Tools

- **PostgreSQL:** Immutable compliance check logs with timestamp indexes
- **Redis:** Consent cache for fast pre-call checks
- **BullMQ:** Compliance report generation queue
- **ECharts:** Compliance rate visualization in dashboards
- **Zod:** Compliance check schema validation

## Production Considerations

- TCPA compliance should never be overridable — even if an operator explicitly allows a call, the system should enforce compliance
- Compliance check logs are the primary defense in TCPA litigation — they must be immutable and backed up
- Statutory damages of $500-$1,500 per violation mean a single campaign making 10,000 non-compliant calls could face $15M in damages
- Regular compliance audits (monthly) should verify that the system's TCPA enforcement is working correctly
- TCPA rules evolve through FCC rulings and court decisions — the rule engine must support hot updates
- Two-party consent states require affirmative recording consent — a violation can result in wiretapping charges, not just TCPA fines
- Caller ID spoofing is illegal under the Truth in Caller ID Act — ensure caller ID is legitimate and authorized
- Test compliance edge cases (timezone boundaries, DST transitions, partial-day blackouts) to ensure no gaps
- Provide a TCPA compliance dashboard for legal and compliance teams to monitor violation rates
- Train operations staff on TCPA requirements — system enforcement alone is not sufficient for safe operation
