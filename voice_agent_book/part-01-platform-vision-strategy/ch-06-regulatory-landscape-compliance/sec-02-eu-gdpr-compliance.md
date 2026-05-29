# Section 02: EU & GDPR Compliance

## GDPR Overview

The General Data Protection Regulation (GDPR) is the EU's comprehensive data privacy framework. It applies to any organization processing personal data of EU residents, regardless of where the organization is based. Non-compliance penalties: up to €20M or 4% of global annual revenue.

```
GDPR Compliance Framework for Voice AI
┌─────────────────────────────────────────────────────────────────────────┐
│ Data Processing Principles                                              │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────────┐  │
│ │ Lawfulness   │ │ Purpose      │ │ Data         │ │ Accuracy       │  │
│ │ Fairness     │ │ Limitation   │ │ Minimization │ │                │  │
│ │ Transparency │ │              │ │              │ │                │  │
│ └──────────────┘ └──────────────┘ └──────────────┘ └────────────────┘  │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────────┐  │
│ │ Storage      │ │ Integrity    │ │ Accountability│ │Data Subject   │  │
│ │ Limitation   │ │ & Confidenti.│ │              │ │ Rights         │  │
│ └──────────────┘ └──────────────┘ └──────────────┘ └────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

## GDPR Applicability to Voice AI

**Controllers:** The business using voice AI (determines purposes and means). **Processors:** Our platform process personal data on behalf of controllers. **Personal data:** Call recordings, transcripts, voice fingerprints, phone numbers, names, any information that identifies a natural person.

### Lawful Basis for Processing
- **Consent:** Explicit, informed, freely given, revocable. Recorded consent must be demonstrable.
- **Legitimate interest:** Can be used for service delivery calls but NOT for marketing calls.
- **Contractual necessity:** Processing necessary for contract fulfillment.

**Recommendation:** Default to consent for call recording + legitimate interest for service delivery.

## Data Subject Rights

| Right | Implementation in Voice AI | Response Timeline |
|-------|---------------------------|-------------------|
| Right to be informed | Privacy notice at data collection point | At collection |
| Right of access | API endpoint to export all personal data | 30 days |
| Right to rectification | Update phone number, name, preferences | 30 days |
| Right to erasure | Delete call recordings, transcripts, profile | 30 days (immediate for automated) |
| Right to restrict processing | Flag account to stop all processing | 30 days |
| Right to data portability | Export transcripts + recordings in standard format | 30 days |
| Right to object | Stop processing for direct marketing | Immediate |

## GDPR Technical Implementation

```typescript
interface GDPRCompliance {
  dataInventory: {
    personalDataCategories: string[];
    processingPurposes: string[];
    storageLocations: string[];
    retentionPeriods: Record<string, number>; // days per data category
  };
  
  dataSubjectRights: {
    sarEndpoint: string;
    erasureEndpoint: string;
    portabilityEndpoint: string;
    maxResponseDays: number;
    automatedDeletionEnabled: boolean;
  };
  
  consentManagement: {
    captureMethod: 'digital' | 'verbal' | 'written';
    consentRecord: string; // audio recording or digital signature
    consentExpiry: number; // days
    withdrawMechanism: string;
  };
  
  dataProcessing: {
    dpaSigned: boolean;
    subProcessors: SubProcessor[];
    dataTransferMechanism: string; // SCCs, DPF, etc.
    processingRecord: ProcessingRecord[];
  };
}

async function handleDataSubjectRequest(
  request: DataSubjectRequest
): Promise<GDPRResponse> {
  verifyIdentity(request.tenantId, request.phoneNumber, request.verificationMethod);
  
  switch (request.type) {
    case 'access':
      return exportPersonalData(request);
    case 'erasure':
      return deletePersonalData(request);
    case 'portability':
      return exportData(request, 'json');
    case 'restrict':
      return restrictProcessing(request);
  }
}

async function deletePersonalData(request: ErasureRequest): Promise<DeletionResult> {
  const deletions = await Promise.all([
    deleteCallRecordings(request.phoneNumber),
    deleteTranscripts(request.phoneNumber),
    deleteVoiceFingerprint(request.phoneNumber),
    deleteConsentRecords(request.phoneNumber),
    anonymizeAnalytics(request.phoneNumber),
  ]);
  
  return {
    tenantId: request.tenantId,
    deletedCategories: deletions.filter(d => d.success).map(d => d.category),
    failedCategories: deletions.filter(d => !d.success).map(d => ({ category: d.category, reason: d.error })),
    deletionCertificate: generateCertificate(deletions),
  };
}
```

## Data Protection Agreement (DPA)

**Required with:** All customers processing EU personal data. **Contents:** Scope of processing, data categories, data subject rights, sub-processor list, data transfer mechanism, security measures, breach notification, audit rights, deletion/return terms.

## Cross-Border Data Transfer

**Schrems II ruling (2020):** Invalidated Privacy Shield. **Current mechanism:** Standard Contractual Clauses (SCCs) + Transfer Impact Assessment (TIA). **Data Privacy Framework (2023):** New EU-US transfer framework (not yet fully tested in court). **Recommendation:** Use SCCs + TIA for all EU-US transfers. Monitor DPF developments.

## Sub-Processor Management

All sub-processors must be listed, with contractual GDPR obligations. **Current sub-processors:** AWS (EU regions), Stripe, Twilio, SendGrid, PostHog (EU cloud). **Process:** Quarterly sub-processor review, 30-day notice before adding new sub-processor (customer can object).

## Data Breach Notification

**72-hour notification** to supervisory authority (DPC, ICO, etc.) for breaches involving personal data. **Notification to data subjects** if breach poses high risk to their rights and freedoms. **Process:** Internal detection → containment → assessment → notification.

## GDPR Compliance Timeline

**Month 1-2:** DPO appointment, data mapping, DPA template creation. **Month 3-4:** Consent mechanism implementation, data subject rights APIs. **Month 5-6:** Cross-border transfer analysis, SCCs implemented. **Month 7-8:** Privacy-by-design review, data minimization audit. **Month 9-12:** DPIA completion, external audit.

## Penalties & Fines

| Violation Type | Maximum Fine | Examples |
|---------------|-------------|----------|
| Core privacy principles | €20M or 4% of global revenue | Amazon: €746M (2021) |
| Data subject rights | €20M or 4% of global revenue | |
| Consent requirements | €20M or 4% of global revenue | |
| Breach notification | €10M or 2% of global revenue | Meta: various fines |
| Records/cooperation | €10M or 2% of global revenue | |

## Tools & Resources

- **DPO:** Internal or outsourced (OneTrust DPO, DataGuard)
- **Data mapping:** OneTrust, Securiti, Transcend
- **Consent management:** Transcend, Cookiebot, Usercentrics
- **DPA management:** Ironclad, Evisort
- **Breach notification:** Automated workflow (PagerDuty → legal → regulator)
- **GDPR compliance audit:** External DPO + law firm (Fieldfisher, Bird & Bird)
