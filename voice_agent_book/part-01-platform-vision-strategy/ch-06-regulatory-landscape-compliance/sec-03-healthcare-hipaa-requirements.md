# Section 03: Healthcare (HIPAA) Requirements

## HIPAA Overview

The Health Insurance Portability and Accountability Act (HIPAA) governs the use and disclosure of Protected Health Information (PHI) by covered entities (healthcare providers, insurers) and their business associates. HIPAA compliance is mandatory for any voice AI platform handling healthcare data.

```
HIPAA Compliance Architecture
┌─────────────────────────────────────────────────────────────────────────┐
│                      HIPAA Security Rule                               │
├─────────────────────────────────────────────────────────────────────────┤
│ Administrative Safeguards   Physical Safeguards    Technical Safeguards │
│ ┌─────────────────────┐   ┌──────────────────┐   ┌─────────────────┐  │
│ │ Security             │   │ Facility access  │   │ Access control  │  │
│ │ management process   │   │ controls          │   │ (unique user ID)│  │
│ │ Security personnel   │   │ Workstation      │   │ Emergency access│  │
│ │ Info access mgmt    │   │ security         │   │ Auto logoff     │  │
│ │ Workforce training   │   │ Device/device    │   │ Encryption      │  │
│ │ Contingency plan     │   │ controls         │   │ Integrity       │  │
│ │ Evaluation           │   │                  │   │ Authentic.      │  │
│ └─────────────────────┘   └──────────────────┘   └─────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

## PHI in Voice AI Context

**What is PHI in voice calls?** Patient name, date of birth, phone number, medical record number, health history, prescription details, appointment information, insurance ID, any voice recording (considered PHI identifier), any medical information discussed.

**Processing PHI means:** Transcribing medical calls (STT), generating responses with medical context (LLM), storing recordings and transcripts (storage), analyzing sentiment and intent (analytics).

## BAA Requirements

A Business Associate Agreement (BAA) is required between our platform and each healthcare customer. The BAA must include:

- Permitted uses and disclosure of PHI
- Prohibition on unauthorized use
- Sub-contractor (sub-processor) obligations
- Breach notification (60-day requirement)
- Access, amendment, and accounting of disclosures
- Return or destruction of PHI at termination
- Audit rights for covered entity

## HIPAA Technical Safeguards

```typescript
interface HIPAAConfig {
  accessControl: {
    uniqueUserId: boolean;
    emergencyAccess: boolean;
    autoLogoff: number; // seconds of inactivity
    encryptionAndDecryption: boolean;
  };
  
  auditControls: {
    hardwareSoftware: boolean;
    auditLogRetention: number; // 6 years minimum
    reviewedRecords: AuditEvent[];
  };
  
  integrityControls: {
    mechanism: 'checksums' | 'digital_signatures' | 'hashing';
    verificationFrequency: 'realtime' | 'daily' | 'weekly';
  };
  
  transmissionSecurity: {
    integrityControls: boolean;
    encryptionInTransit: 'TLS-1.2' | 'TLS-1.3';
  };
  
  contingencyPlan: {
    dataBackup: boolean;
    disasterRecovery: boolean;
    emergencyMode: boolean;
    testingFrequency: 'quarterly' | 'semi-annual' | 'annual';
  };
}

function validateHIPAAConfig(config: HIPAAConfig): ValidationResult {
  const failures = [];
  
  if (!config.accessControl.uniqueUserId) {
    failures.push({ control: 'Access Control', finding: 'Unique user identification required' });
  }
  if (!config.accessControl.autoLogoff || config.accessControl.autoLogoff > 900) {
    failures.push({ control: 'Access Control', finding: 'Auto-logoff must be ≤ 15 minutes' });
  }
  if (!config.auditControls.auditLogRetention || config.auditControls.auditLogRetention < 2190) {
    failures.push({ control: 'Audit Controls', finding: 'Audit logs must be retained 6+ years' });
  }
  if (config.transmissionSecurity.encryptionInTransit !== 'TLS-1.3') {
    failures.push({ control: 'Transmission', finding: 'TLS 1.3 required for PHI in transit' });
  }
  
  return {
    compliant: failures.length === 0,
    failures,
    recommendations: generateRemediations(failures),
  };
}
```

## HIPAA Compliance Requirements for Voice AI Platform

| Requirement | Implementation | Audit Evidence |
|-------------|---------------|----------------|
| Access control | Unique user IDs, role-based access, auto-logoff (15 min) | User access matrix, system config |
| Audit controls | Detailed audit trail of PHI access | Audit logs, review reports |
| Integrity controls | PHI checksum validation, version tracking | Integrity verification reports |
| Transmission security | TLS 1.3 for all PHI in transit | TLS config, certificate mgmt |
| Encryption at rest | AES-256 for stored PHI | Encryption config, key management |
| Authentication | Strong passwords, MFA, SSO | Authentication policy |
| Device/Media controls | Secure disposal, data re-use, accountability | Disposal procedures, tracking |
| Disaster recovery | Backup, DR plan, testing every 6 months | DR test results |
| Emergency access | Break-glass procedure for PHI access | Emergency access logs |
| Automatic logoff | 15-minute inactivity timeout | System configuration |

## PHI De-Identification

For analytics and model training, PHI must be de-identified. **Expert determination:** Statistical expert certifies re-identification risk is very small. **Safe harbor:** Remove 18 identifiers (name, geographic subdivisions, dates, phone, fax, email, SSN, MRN, health plan numbers, account numbers, certificate numbers, vehicle identifiers, device identifiers, URLs, IP addresses, biometric identifiers, photos, any other unique identifiers).

## Breach Notification

**Breach definition:** Unauthorized acquisition, access, use, or disclosure of PHI. **Risk assessment:** 4-factor test (nature of data, unauthorized person, actual acquisition, risk mitigation). **Notification timeline:** 60 days to affected individuals, HHS, and media (if 500+ affected). **Our process:** Incident detection → forensic investigation → legal assessment → notification.

## HIPAA Compliance Timeline

**Month 1:** HIPAA readiness assessment, gap analysis. **Month 2-3:** BAA template, policies and procedures, workforce training. **Month 4-6:** Technical safeguards implementation, audit controls, encryption. **Month 7-9:** Penetration testing, risk assessment, remediation. **Month 9-12:** External audit, HIPAA certification, BAA execution with first healthcare customers.

## Open Source HIPAA Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| AWS HIPAA Eligible Services | Infrastructure | All services used must be HIPAA eligible |
| OpenSSL | Encryption | TLS implementation |
| HashiCorp Vault | Key management | PHI encryption keys |
| Wazuh | SIEM/Security monitoring | Audit log analysis |
| OPA (Open Policy Agent) | Access control | Policy-as-code for PHI access |
| CertManager | Certificate management | TLS certificate lifecycle |

## Competitive HIPAA Comparison

| Factor | Us | Retell AI | Twilio | Google CCAI | Amazon Connect |
|--------|-----|-----------|--------|-------------|----------------|
| HIPAA compliant | Year 2 goal | ✅ | ✅ | ✅ | ✅ |
| BAA included | Enterprise tier | Enterprise | ✅ | ✅ | ✅ |
| PHI audit logs | ✅ (planned) | ✅ | ✅ | ✅ | ✅ |
| Self-hosted HIPAA | ✅ (planned) | Limited | ❌ | ❌ | ❌ |
| PHI de-identification | ✅ (planned) | ❌ | ❌ | ❌ | ❌ |
| Breach notification | Automated | Manual | Manual | Manual | Manual |

## Tools & Resources

- **HIPAA compliance automation:** Vanta, Drata, Thoropass
- **HIPAA risk assessment:** RiskWatch, ComplianceForge
- **Penetration testing:** HackerOne, Bugcrowd, AWS Pen Test
- **HIPAA attorney:** Healthcare law specialist (Epstein Becker Green, McDermott Will & Emery)
- **Training:** HIPAA training for all employees (annual)
- **BAA management:** Ironclad, Evisort
