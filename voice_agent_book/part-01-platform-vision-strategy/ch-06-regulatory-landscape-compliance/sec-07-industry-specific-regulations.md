# Section 07: Industry-Specific Regulations

## Overview

Beyond general privacy and telephony laws, several industries have additional regulations that impact voice AI platform requirements. Understanding these is essential for vertical market strategy.

```
Industry-Specific Regulations Map
┌─────────────────────────────────────────────────────────────────────────┐
│ Healthcare     │  HIPAA/HITECH, state health privacy, FDA (if clinical)  │
├─────────────────────────────────────────────────────────────────────────┤
│ Financial      │  FINRA, SEC, GLBA, FCRA, ECOA, BSA/AML, state banking  │
├─────────────────────────────────────────────────────────────────────────┤
│ Debt           │  FDCPA, state collection laws, TCPA overlay             │
│ Collection     │                                                        │
├─────────────────────────────────────────────────────────────────────────┤
│ Education      │  FERPA, PPRA, state education privacy                   │
├─────────────────────────────────────────────────────────────────────────┤
│ Insurance      │  State insurance dept regulations, NAIC model laws     │
├─────────────────────────────────────────────────────────────────────────┤
│ Government     │  FedRAMP, StateRAMP, DFARS (defense), ITAR             │
└─────────────────────────────────────────────────────────────────────────┘
```

## FINRA (Financial Industry Regulatory Authority)

**Applies to:** Broker-dealers, financial advisors, securities firms. **Scope:** Record keeping of all communications related to business (including voice calls). **FINRA Rule 17a-4:** Requires retention of communications for 3-6 years, with specific storage formats (WORM — Write Once Read Many).

**Voice AI requirements:**
- All call recordings must be retained in WORM format (no modification, no deletion)
- Record retention: 3 years (broker-dealers), 6 years (exchanges)
- Immediate production for regulatory request (72 hours)
- Supervision: Firms must supervise communications (AI monitoring of advisor-client calls)
- Off-channel communication prohibition: All business communications must occur on approved channels

**Implementation:**
- WORM-compliant storage (S3 Object Lock, Write Once Read Many)
- Automated call archiving with immutability policies
- Supervision dashboard: AI-powered compliance monitoring of advisor calls
- Communication channel detection: Flag if business communication happens off-platform

## SEC (Securities and Exchange Commission)

**Regulations:** SEC Rule 17a-4 (record keeping), Regulation Best Interest (Reg BI), Marketing Rule (Rule 206(4)-1). **Record keeping:** Similar to FINRA — all business communications retained. **Reg BI:** Advisors must act in client's best interest — AI agents must be configured to comply (no unsuitable recommendations).

## FDCPA (Fair Debt Collection Practices Act)

**Applies to:** Debt collectors (third-party and first-party). **Scope:** Governs how debt collectors communicate with consumers. **Key requirements:**

- **Call time:** 8 AM - 9 PM (local time of consumer)
- **Call frequency:** Cannot call repeatedly or continuously (no definition, but best practice: <3 calls/day)
- **Identification:** Must identify as debt collector
- **Dispute rights:** Must inform consumer of dispute rights (within 5 days of initial communication)
- **Harassment:** No harassing, oppressive, or abusive conduct
- **Third-party disclosure:** Cannot disclose debt to third parties (including leaving voicemails with third parties)
- **Cease and desist:** Must stop collection upon written request

**Voice AI considerations:**
- Agent script must include debt collector identification
- Voicemail detection — cannot leave messages that disclose debt
- Frequency monitoring — track call attempts per consumer
- Consent for outbound calls (TCPA overlay)
- Right-party verification before discussing debt
- Cease and desist management — immediate flagging and suppression

## FERPA (Family Educational Rights and Privacy Act)

**Applies to:** Educational institutions receiving federal funding. **Scope:** Student education records. **Voice AI intersection:** Call recording of student communications (admissions, advising, financial aid). **Requirement:** Written consent for disclosure of education records. **Exception:** School official with legitimate educational interest.

## GLBA (Gramm-Leach-Bliley Act)

**Applies to:** Financial institutions. **Scope:** Non-public personal information (NPI). **Requirements:** Privacy notice, opt-out for sharing with non-affiliates, safeguard rule (information security program). **Voice AI:** Must protect NPI in call recordings, must provide privacy notice, must allow opt-out.

## State-Specific Financial Regulations

| State | Regulation | Impact on Voice AI |
|-------|-----------|-------------------|
| California | California Financial Information Privacy Act | Additional opt-out requirements |
| New York | NYDFS Cybersecurity Regulation (23 NYCRR 500) | Multi-factor auth, annual certification, CISO |
| Texas | Texas Security Breach Notification | Enhanced data protection requirements |
| Vermont | Vt. Stat. tit. 9 § 2480e | Financial privacy opt-out |

## Regulatory Data Model

```typescript
interface IndustryRegulation {
  industry: string;
  regulation: string;
  jurisdiction: string;
  requirements: RegulationRequirement[];
  penalties: Penalty[];
}

interface RegulationRequirement {
  id: string;
  description: string;
  implementation: string;
  evidenceRequired: string;
  auditFrequency: 'quarterly' | 'annual' | 'ongoing';
}

function checkIndustryRequirements(
  customerIndustry: string,
  customerState: string
): ComplianceChecklist {
  const regulations = industryRegulations.filter(r => 
    r.industry === customerIndustry &&
    (r.jurisdiction === 'federal' || r.jurisdiction === customerState)
  );
  
  const requirements = regulations.flatMap(r => r.requirements);
  
  return {
    total: requirements.length,
    met: requirements.filter(r => isImplemented(r.id)).length,
    missing: requirements.filter(r => !isImplemented(r.id)).map(r => ({
      requirement: r.description,
      implementation: r.implementation,
      priority: getPriority(r),
      effort: estimateEffort(r),
    })),
    complianceScore: requirements.filter(r => isImplemented(r.id)).length / requirements.length,
  };
}
```

## Compliance Certification Roadmap

| Industry | Cert/Regulation | Timeline | Investment | Revenue Impact |
|----------|----------------|----------|------------|----------------|
| General | SOC 2 Type II | M4-9 | $50K | Enables all enterprise |
| Healthcare | HIPAA | M9-18 | $100K | Opens $2.8B healthcare TAM |
| Finance | PCI DSS Level 1 | M12-18 | $80K | Opens $1.8B finance TAM |
| Finance | FINRA compliance | M18-24 | $60K | Opens broker-dealer market |
| Government | FedRAMP | M24-36 | $200K+ | Opens $500M govt TAM |
| Education | FERPA | M6-12 | $20K | Opens education vertical |
| Insurance | State-specific | M18-24 | $40K | Opens insurance vertical |

## Industry-Specific Compliance Tools

| Industry | Tool | Purpose |
|----------|------|---------|
| Finance | Smarsh, Global Relay | FINRA-compliant archiving |
| Debt | DCI, Simplicity | FDCPA compliance management |
| All | Vanta, Drata | Compliance automation |
| Government | FedRAMP Marketplace | FedRAMP authorized services |
| All | OneTrust | Regulation mapping |
| Finance | AbacusNext, ComplianceMax | FINRA supervision |

## Tools & Resources

- **Regulatory monitoring:** ComplySci, Fenergo
- **Industry compliance consulting:** PwC, Deloitte, EY
- **Legal counsel:** Industry-specific (financial services: Morgan Lewis; healthcare: Epstein Becker Green)
- **FDCPA-specific:** DCI Consulting, Compliance Solutions
- **FINRA supervision:** Smarsh, Global Relay, Theta Lake
- **FERPA guidance:** Department of Education (FERPA@ed.gov)
