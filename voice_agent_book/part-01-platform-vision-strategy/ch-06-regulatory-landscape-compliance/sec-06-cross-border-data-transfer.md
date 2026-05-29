# Section 06: Cross-Border Data Transfer

## Overview

Cross-border data transfer regulations determine how personal data can move between jurisdictions. For a voice AI platform, this affects where call recordings, transcripts, analytics data, and customer information are stored and processed.

```
Global Data Transfer Landscape
┌─────────────────────────────────────────────────────────────────────────┐
│ Data Transfer Corridors                                                 │
│                                                                         │
│  ┌─────────┐           ┌─────────┐           ┌─────────┐              │
│  │  EU     │◄─────────►│  US     │◄─────────►│  UK     │              │
│  │  GDPR   │   SCCs    │  No fed │   UK GDPR │         │              │
│  │         │   + DPF   │  privac.│   + SCCs  │         │              │
│  └─────────┘           └─────────┘           └─────────┘              │
│       │                      │                      │                   │
│       ▼                      ▼                      ▼                   │
│  ┌─────────┐           ┌─────────┐           ┌─────────┐              │
│  │  APAC   │           │  LATAM  │           │  Africa │              │
│  │  Various│           │  Various│           │  Various│              │
│  └─────────┘           └─────────┘           └─────────┘              │
└─────────────────────────────────────────────────────────────────────────┘
```

## EU-US Data Transfers

### History of EU-US Data Transfer Frameworks
**Safe Harbor (2000-2015):** Invalidated by Schrems I. **Privacy Shield (2016-2020):** Invalidated by Schrems II. **Data Privacy Framework (2023-present):** Current framework, faces legal challenge expected 2025-2026.

### Current Requirements
**Standard Contractual Clauses (SCCs):** Primary mechanism for EU-US transfers. Must be signed between data exporter (EU customer) and data importer (us). **Transfer Impact Assessment (TIA):** Required alongside SCCs. Assesses whether the importer's jurisdiction provides essentially equivalent protection. **Supplemental measures:** Technical measures (encryption, pseudonymization) to address risks identified in TIA.

## Data Residency Architecture

```typescript
interface DataResidencyConfig {
  defaultRegion: string;
  allowedRegions: string[];
  
  dataClassification: {
    callRecordings: {
      storageRegion: string;
      backupRegion: string;
      retentionDays: number;
    };
    transcripts: {
      storageRegion: string;
      processingRegion: string;
    };
    analytics: {
      aggregatedRegion: string;
      rawRegion: string;
    };
    customerProfiles: {
      storageRegion: string;
    };
  };
  
  dataTransfer: {
    mechanism: 'scc' | 'adequacy' | 'consent' | 'contractual_necessity';
    safeguards: ('encryption' | 'pseudonymization' | 'anonymization')[];
    tiaCompleted: boolean;
    lastTiaDate: Date;
  };
}

class DataResidencyManager {
  private configs: Map<string, DataResidencyConfig>;
  
  async routeData(data: VoiceData, customerRegion: string): Promise<RoutingDecision> {
    const config = this.configs.get(customerRegion);
    
    if (!config) {
      throw new Error(`No data residency config for region: ${customerRegion}`);
    }
    
    const classification = this.classifyData(data);
    const region = config.dataClassification[classification].storageRegion;
    
    // Check if cross-border transfer is needed
    if (region !== this.defaultRegion) {
      await this.validateTransfer(region, customerRegion, classification);
    }
    
    return {
      storageRegion: region,
      processingRegion: config.dataClassification[classification].processingRegion,
      allowed: true,
      retentionDays: config.dataClassification[classification].retentionDays,
    };
  }
  
  private async validateTransfer(
    targetRegion: string,
    customerRegion: string,
    classification: string
  ): Promise<void> {
    // Check adequacy decision
    if (this.adequacyDecisions.includes(targetRegion)) {
      return; // Adequacy decision covers this transfer
    }
    
    // Verify SCCs are in place
    if (!this.sccsInPlace[customerRegion]) {
      throw new TransferError(`SCCs not in place for ${customerRegion}`);
    }
    
    // Check TIA
    if (this.needsTIA(customerRegion, targetRegion, classification)) {
      const tia = await this.performTIA(customerRegion, targetRegion);
      if (!tia.favorable) {
        throw new TransferError(`TIA unfavorable for ${customerRegion} → ${targetRegion}`);
      }
    }
  }
}
```

## Global Data Residency Map

| Region | Data Center Options | Regulations | Transfer Mechanism |
|--------|-------------------|-------------|-------------------|
| US (Primary) | AWS us-east-1, us-west-2 | CCPA, state laws | N/A (origin) |
| EU (Required for EU) | AWS eu-west-1, eu-central-1 | GDPR | SCCs + TIA (incoming) |
| UK | AWS eu-west-2 | UK GDPR | UK SCCs |
| Canada | AWS ca-central-1 | PIPEDA | Adequacy decision |
| Australia | AWS ap-southeast-2 | Privacy Act | SCCs |
| Japan | AWS ap-northeast-1 | APPI | Adequacy decision |
| Brazil | AWS sa-east-1 | LGPD | SCCs |
| India | AWS ap-south-1 | DPDP Act 2023 | SCCs |

## Implementation Strategy

**Phase 1 (Year 1):** Single US region. EU customers sign SCCs. Data transfer via SCCs + encryption. **Phase 2 (Year 2):** EU region (Frankfurt/Ireland). Data residency controls for EU customers. **Phase 3 (Year 3):** Multi-region (US + EU + APAC). Customer-selectable data residency.

## Data Transfer Safeguards

### Technical Safeguards
- **Encryption at rest:** AES-256 with customer-managed keys (where possible)
- **Encryption in transit:** TLS 1.3 between all regions
- **Pseudonymization:** Replace direct identifiers with pseudonyms for cross-border analytics
- **Anonymization:** Aggregate data before cross-border transfer (irreversible)

### Organizational Safeguards
- **SCCs:** Signed with every non-EU customer processing EU data
- **DPA:** Data Processing Agreement with each customer
- **TIA:** Transfer Impact Assessment completed annually
- **Data mapping:** Automated data flow mapping

## Schrems II Compliance Checklist

- [ ] SCCs signed with all EU customers transferring data to US
- [ ] TIA completed for EU-US transfers
- [ ] Supplemental measures implemented (encryption, pseudonymization)
- [ ] Data processed in EU for EU customers (Phase 2)
- [ ] Sub-processor list maintained with transfer mechanisms
- [ ] Data Protection Officer appointed
- [ ] Breach notification procedure includes cross-border considerations

## DPF (Data Privacy Framework) Certification

**Status:** Certified (or in process). **Coverage:** EU-US and (separate) Swiss-US transfers. **Limitations:** Not fully tested in court (expected challenge 2025-2026). **Recommendation:** Use DPF + SCCs as backup.

## Monitoring & Compliance

```typescript
class CrossBorderMonitor {
  async auditDataFlows(): Promise<DataFlowReport> {
    // Track all data transfer events
    const transfers = await this.queryTransferLogs(last90Days);
    
    const violations = transfers.filter(t => {
      const config = this.residencyConfigs.get(t.customerRegion);
      return t.targetRegion !== config?.allowedRegions[t.classification];
    });
    
    return {
      totalTransfers: transfers.length,
      compliantTransfers: transfers.length - violations.length,
      violations: violations.map(v => ({
        customerId: v.customerId,
        dataType: v.classification,
        from: v.sourceRegion,
        to: v.targetRegion,
        timestamp: v.timestamp,
        severity: 'high',
      })),
      recommendations: violations.length > 0 
        ? ['Review data routing rules', 'Update data residency configs']
        : [],
    };
  }
}
```

## Tools & Resources

- **Data mapping:** OneTrust, Securiti, Transcend
- **SCC management:** Ironclad, Evisort, DocuSign
- **TIA templates:** IAPP, OneTrust
- **DPF certification:** Privacy Framework website (privacyshield.gov)
- **DPO services:** DataGuard, OneTrust DPO
- **Legal counsel:** International data privacy law firm (Baker McKenzie, Covington)
