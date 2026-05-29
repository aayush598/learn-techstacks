# Section 05: Call Recording Consent Laws

## Overview of Consent Requirements

Call recording consent laws vary significantly by jurisdiction. In the US, 11 states require all-party (two-party) consent, while 39 states require one-party consent. Internationally, GDPR imposes additional requirements for recording EU residents.

```
US Consent Law Map
┌─────────────────────────────────────────────────────────────────────────┐
│ Two-Party Consent States (All parties must consent)                     │
│ ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────────────────┐  │
│ │ CA │ CT │ FL │ IL │ MD │ MA │ MT │ NH │ PA │ WA │ OR             │  │
│ └────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────────────────┘  │
│                                                                         │
│ One-Party Consent States (At least one party must consent)             │
│ All other states + DC                                                    │
│                                                                         │
│ Mixed Consent States (Varies by situation)                              │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────────┐    │
│ │ CA: All-party│ │ IL: All-party│ │ WA: All-party unless          │    │
│ │ but limited  │ │ but EBR      │ │ reasonable expectation       │    │
│ │ exceptions   │ │ exceptions   │ │ of privacy                   │    │
│ └──────────────┘ └──────────────┘ └──────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

## State-by-State Consent Requirements

### Two-Party Consent States (11)
**Requirements:** ALL parties to the conversation must be notified and consent to recording. **Implementation:** Verbal announcement + verbal or implied consent. **Best practice:** "This call may be recorded for quality assurance purposes. By continuing this call, you consent to recording."

**California:** Most restrictive. Penal Code 632 — all-party consent for confidential communications. Exception for business calls where parties have no reasonable expectation of privacy. **Florida:** All-party consent but with "commission of crime" exception. **Illinois:** Eavesdropping Act — all-party consent, strict interpretation. **Massachusetts:** Two-party consent, MGL c.272 §99. **Pennsylvania:** Wiretapping and Electronic Surveillance Control Act.

### One-Party Consent States (39 + DC)
**Requirements:** The recording party must consent. Other parties don't need to be notified. **However:** Still requires notification if call is used for "quality assurance" or "training" purposes (industry best practice). **Implementation:** Still announce recording — builds trust and reduces legal risk.

## Consent Announcement Requirements

**Verbal announcement at call start:** "This call may be recorded or monitored for quality assurance and training purposes." **Timing:** At the beginning of the call, before any substantive conversation. **Frequency:** Once per call (not per segment). **Recording of consent:** The announcement + response must be captured in the call recording.

## International Consent Requirements

### GDPR (EU)
**Requirements:** Explicit, informed, freely given, specific, revocable consent. **Consent must be:** (1) Given by a clear affirmative action, (2) Distinguishable from other matters, (3) Withdrawn as easily as given. **Recording purpose:** Must specify all purposes (quality assurance, training, compliance, dispute resolution).

### Canada (PIPEDA)
**Requirements:** Consent required for recording (implied for business purposes). **Best practice:** Announce recording and provide opt-out for non-service purposes.

### Australia
**Requirements:** One-party consent for recording (Telecommunications Interception Act). **Best practice:** Still announce for transparency.

## Consent Implementation Architecture

```typescript
interface ConsentRequirement {
  jurisdiction: string;
  requiredConsentType: 'one-party' | 'two-party' | 'all-party';
  announcement: string;
  requiresExplicit: boolean;
  requiresRecording: boolean;
  exceptions: ConsentException[];
}

class ConsentManager {
  private stateLookup: Map<string, ConsentRequirement>;
  private consentRecords: ConsentRecord[];
  
  async getConsentRequirements(phoneNumber: string): Promise<ConsentRequirement> {
    const state = await this.lookupState(phoneNumber);
    const country = await this.lookupCountry(phoneNumber);
    
    // Determine the most restrictive requirement
    const stateReq = this.stateLookup.get(state);
    const countryReq = this.getCountryRequirement(country);
    
    return this.mergeRequirements(stateReq, countryReq);
  }
  
  async handleCallRecordingConsent(call: CallContext): Promise<ConsentResult> {
    const req = await this.getConsentRequirements(call.toNumber);
    
    if (req.requiresExplicit) {
      // Play consent announcement and wait for response
      const announcement = req.announcement;
      const response = await call.playAndWaitForResponse(announcement, {
        timeout: 5000,
        expectedResponse: ['yes', 'sure', 'okay', 'i consent', 'go ahead', 'continue'],
      });
      
      const consentGiven = response.match || req.requiresExplicit === false;
      
      const record: ConsentRecord = {
        callId: call.id,
        phoneNumber: call.toNumber,
        jurisdiction: `${req.jurisdiction} (${state})`,
        consentGiven,
        consentMethod: 'verbal',
        announcement,
        responseText: response.transcript,
        recordingUrl: response.recordingUrl,
        timestamp: new Date(),
        expiresAt: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000), // 1 year
      };
      
      await this.storeConsent(record);
      
      return {
        canRecord: consentGiven,
        consentRecord: record,
        options: consentGiven ? {} : {
          canTranscribe: true, // can still transcribe without recording
          canAnalyze: true, // can do real-time analytics
          cannotStore: true, // cannot store recording
        },
      };
    }
    
    // One-party consent - announcement only
    await call.playAnnouncement(req.announcement);
    return { canRecord: true };
  }
  
  private async lookupState(phoneNumber: string): Promise<string> {
    // Use NPA-NXX lookup or carrier info
    // Fallback: area code-based approximate lookup
    const areaCode = phoneNumber.slice(2, 5);
    return this.areaCodeToState(areaCode);
  }
}
```

## Consent Recording & Storage

**Record keeping:** Store consent record with call recording metadata. **Retention:** Same as call recording retention (varies by jurisdiction: 1-7 years). **Audit:** Consent records must be producible in legal proceedings.

```typescript
interface ConsentRecord {
  callId: string;
  phoneNumber: string;
  jurisdiction: string;
  consentGiven: boolean;
  consentMethod: 'verbal' | 'digital' | 'written';
  announcement: string;
  responseText?: string;
  recordingUrl?: string;
  timestamp: Date;
  expiresAt?: Date;
  withdrawnAt?: Date;
  proofOfConsent: string; // URL to the consent portion of recording
}
```

## Best Practices for Call Recording

1. **Announce on every call** (even in one-party states) — transparency builds trust
2. **Record the consent announcement and response** — proves compliance
3. **Support opt-out** — if caller refuses, offer partial service (no recording but still can transcribe)
4. **Check jurisdiction per call** — caller's location determines consent requirement
5. **Time-check for state-specific rules** — some states have specific timing requirements
6. **Document consent retention policy** — align with regulatory requirements (1-7 years)
7. **International calls** — apply the most restrictive jurisdiction (GDPR-level consent)

## Penalties for Non-Compliance

| Violation | State | Penalty |
|-----------|-------|---------|
| Recording without consent (two-party state) | CA | $5,000 per violation + criminal |
| Recording without consent (two-party state) | FL | $10,000 per violation |
| Recording without consent (two-party state) | PA | $10,000 per violation + criminal |
| GDPR recording violation | EU | €20M or 4% of global revenue |
| PIPEDA recording violation | Canada | $100,000 per violation |

## Tools & Resources

- **Phone number lookup:** Twilio Lookup API, Telnyx Number Lookup, MaxMind GeoIP
- **State jurisdiction database:** NPA-NXX to state mapping (maintained monthly)
- **Consent recording:** Store consent segment as separate audio file
- **Legal counsel:** Telecommunications litigation specialist
- **Consent management:** Transcend, OneTrust
