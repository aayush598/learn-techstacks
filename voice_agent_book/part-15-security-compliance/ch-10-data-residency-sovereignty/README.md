# Chapter 10: Data Residency & Sovereignty

> **Part:** 15 - Security, Compliance & Governance

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Data Residency Requirements](sec-01-data-residency-requirements.md) | Regulatory data localization laws (GDPR, LGPD, PIPL), industry-specific requirements, contractual obligations |
| 02 | [Region Selection Strategy](sec-02-region-selection-strategy.md) | Cloud provider region selection, latency considerations, compliance coverage, region availability |
| 03 | [Data Classification & Labeling](sec-03-data-classification-labeling.md) | Data sensitivity levels, automated classification rules, labeling taxonomy, metadata tagging |
| 04 | [Cross-Region Data Flow](sec-04-cross-region-data-flow.md) | Region-to-region data transfer controls, data flow approval, transfer logging, transfer encryption |
| 05 | [Region-Specific Encryption](sec-05-region-specific-encryption.md) | Per-region KMS keys, region-locked encryption, customer-managed keys per region |
| 06 | [Data Residency API](sec-06-data-residency-api.md) | Region selection at tenant onboarding, data location query API, residency verification endpoints |
| 07 | [Multi-Region Deployment](sec-07-multi-region-deployment.md) | Active-active vs active-passive multi-region, data sync across regions, region failover |
| 08 | [Compliance Automation](sec-08-compliance-automation.md) | Automated compliance checks, policy-as-code for residency, region restriction enforcement, compliance reporting |

---

## Data Residency Zones

```
EU Zone (Frankfurt)
  ├── Customer Data (Call recordings, transcripts)
  ├── User Data (PII, account info)
  └── Logs (Audit, operational)

US Zone (Virginia)
  ├── Customer Data
  ├── User Data
  └── Logs

APAC Zone (Singapore/Tokyo)
  ├── Customer Data
  ├── User Data
  └── Logs

Global Zone (US - shared)
  ├── Application Configuration
  ├── Feature Flags
  └── Analytics Aggregates
```

---

## Learning Objectives

- Understand data residency requirements across jurisdictions
- Select cloud provider regions for compliance coverage
- Implement data classification and automated labeling
- Control cross-region data flows with audit trail
- Configure region-specific encryption with per-region keys
- Build data residency API for tenant region selection
- Design multi-region deployment architecture
- Automate compliance enforcement with policy-as-code
