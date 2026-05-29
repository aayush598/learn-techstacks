# Section 04: Financial Services (PCI DSS)

## PCI DSS Overview

The Payment Card Industry Data Security Standard (PCI DSS) governs how organizations handle cardholder data. For voice AI platforms, PCI compliance is essential for any payment processing — voice payments, payment verification, or billing inquiries involving card data.

```
PCI DSS Compliance Domains
┌─────────────────────────────────────────────────────────────────────────┐
│ Build & Maintain     │ Protect           │ Maintain             │      │
│ Secure Network       │ Cardholder Data   │ Vulnerability Mgmt   │      │
├──────────────────────┼───────────────────┼──────────────────────┤      │
│ 1. Firewall          │ 3. Protect stored │ 5. Antivirus         │      │
│    configuration     │    cardholder     │    (if applicable)    │      │
│ 2. Secure configs    │    data           │ 6. Secure apps       │      │
│    (no defaults)      │ 4. Encrypt       │    & configurations  │      │
│                       │    transmission   │                       │      │
├──────────────────────┼───────────────────┼──────────────────────┤      │
│ Implement Strong     │ Regular           │ Maintain             │      │
│ Access Control       │ Monitoring        │ Info Security Policy │      │
├──────────────────────┼───────────────────┼──────────────────────┤      │
│ 7. Need-to-know      │ 10. Track &       │ 12. Policy           │      │
│    access            │    monitor all    │    program           │      │
│ 8. Unique IDs        │    access         │                       │      │
│ 9. Physical access   │ 11. Test security│                       │      │
│    controls          │    systems        │                       │      │
└─────────────────────────────────────────────────────────────────────────┘
```

## Cardholder Data in Voice AI

**What is cardholder data (CHD)?** Primary Account Number (PAN), cardholder name, expiration date, service code. **Sensitive Authentication Data (SAD):** Full magnetic stripe data, CVV2/CVC2, PINs. **Prohibition:** SAD cannot be stored after authorization (even encrypted). PAN must be encrypted at rest.

**Voice AI risk:** Callers may verbally provide credit card numbers, CVV codes, expiration dates. The voice platform must detect, mask, and never store full PAN or SAD.

## Scoping & SAQ Validation

**Our scope:** Service provider (we process, store, or transmit CHD on behalf of customers). **SAQ type:** SAQ D for Service Providers (most rigorous). **Validation:** Quarterly ASV scans, annual on-site assessment (ISA or QSA).

## PCI Technical Implementation

```typescript
interface PCIDSSConfig {
  scope: {
    chdEnv: string[]; // systems processing cardholder data
    connectedTo: string[]; // systems connected to CHD environment
    outOfScope: string[]; // systems verified out of scope
  };
  
  encryption: {
    dataAtRest: 'AES-256' | 'TDE';
    dataInTransit: 'TLS-1.3';
    keyManagement: 'HSM' | 'KMS' | 'vault';
    keyRotation: number; // days
  };
  
  tokenization: {
    provider: 'stripe' | 'braintree' | 'spreedly';
    panFormat: string; // first6last4 for display
    reversible: boolean;
  };
  
  segmentation: {
    chdNetwork: string; // isolated VLAN
    accessControls: 'firewall' | 'nac' | 'sg';
    monitoring: 'ids' | 'ips' | 'siem';
  };
  
  logging: {
    events: PCIAuditEvent[];
    retention: number; // 12 months minimum, 3 for accessible
    protection: 'immutable' | 'append-only';
  };
}

class PCIComplianceManager {
  private tokenVault: TokenVault;
  
  async processVoicePayment(callContext: CallContext): Promise<PaymentResult> {
    // Detect credit card pattern in real-time transcript
    const ccPattern = /\b(\d{4}[- ]?){3}\d{4}\b/;
    const transcript = callContext.currentTranscript;
    
    if (ccPattern.test(transcript)) {
      // Mute DTMF tones from recording
      await callContext.muteDTMFFromRecording();
      
      // Extract and tokenize
      const pan = await this.extractPAN(callContext.audioStream);
      const token = await this.tokenVault.tokenize(pan);
      
      // Never store raw PAN
      callContext.replaceTranscript('****');
      
      return { token, last4: pan.slice(-4), masked: `****${pan.slice(-4)}` };
    }
    
    return { error: 'No payment detected' };
  }
  
  async validatePCICompliance(): Promise<ValidationReport> {
    const checks = [
      this.checkFirewallRules(),
      this.checkEncryptionConfig(),
      this.checkAccessControls(),
      this.checkLogging(),
      this.checkVulnerabilityScans(),
      this.checkPenetrationTests(),
    ];
    
    return {
      passed: checks.every(c => c.passed),
      checks,
      lastValidation: new Date(),
      nextValidationDue: new Date(Date.now() + 90 * 24 * 60 * 60 * 1000),
    };
  }
}
```

## Voice Payment Compliance

### DTMF Masking
When callers enter credit card digits via keypad, DTMF tones must be masked in recordings. **Implementation:** Capture DTMF but replace with flat tone in recording. Store only tokenized representation.

### Verbal Card Processing
When callers verbally provide card info: (1) Real-time STT detects credit card pattern, (2) Pause recording, (3) Process payment via tokenization service, (4) Resume recording with masked transcript, (5) Store only token + last 4 digits.

### Recording & Storage
- Full PAN must never appear in stored transcripts
- Recording segments containing cardholder data must be redacted or deleted
- Token mapping must be stored separately (logically or physically isolated)
- Key management: HSM or equivalent with dual control

## PCI Requirements Checklist for Voice AI

| Requirement | Voice AI Specific | Implementation |
|-------------|------------------|----------------|
| 2.1 - Change defaults | Secure default configs | Hardened AMI, secure defaults |
| 3.4 - Render PAN unreadable | PAN masking + tokenization | Tokenization service |
| 3.5 - Protect keys | HSM-based key management | AWS CloudHSM or Vault |
| 4.1 - Encrypt transmission | TLS 1.3 for all APIs | mTLS for internal services |
| 6.6 - Public-facing app security | WAF + regular scanning | AWS WAF, Cloudflare WAF |
| 7.1 - Need-to-know access | RBAC + PCI scope | Policy-as-code (OPA) |
| 8.3 - MFA | MFA for admin access | TOTP + SSO |
| 10.2 - Audit trails | Immutable audit logs | Append-only database |
| 10.7 - Retain audit history | 12-month retention | S3 Glacier + Athena |
| 11.2 - Run ASV scans | Quarterly ASV | AWS Inspector + external ASV |
| 11.3 - Penetration testing | Annual pen test | HackerOne + external pentest |
| 12.8 - Service providers | Due diligence on sub-processors | Third-party risk management |

## PCI Compliance Timeline

**Month 1-3:** Scope determination, network segmentation design. **Month 4-6:** Tokenization implementation, encryption deployment, logging infrastructure. **Month 7-9:** ASV scanning setup, penetration testing, remediation. **Month 10-12:** SAQ completion, QSA assessment, ROC submission (if required). **Ongoing:** Quarterly ASV scans, annual pen test, continuous monitoring.

## Tokenization vs. Encryption

| Approach | Security | Complexity | Scope Impact | Recommendation |
|----------|----------|------------|--------------|----------------|
| Full encryption | High | Medium | Still in scope | Good but complex |
| Tokenization | Very high | Medium | Reduces scope | Best for voice payments |
| Point-to-point encryption | High | High | Reduces scope | Hardware dependent |
| Third-party token (Stripe) | Very high | Low | Eliminates storage scope | Recommended for MVP |

## Open Source PCI Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| OpenSCAP | Security compliance scanning | CIS benchmarks |
| Wazuh | SIEM + IDS | Audit log monitoring |
| OPA (Open Policy Agent) | Access control policy | PCI access enforcement |
| Vault (HashiCorp) | Key management | Encryption key lifecycle |
| ModSecurity | WAF | Open-source web firewall |
| Lynis | Security auditing | Linux security assessment |

## Competitive PCI Comparison

| Feature | Us | Twilio | Stripe | Braintree |
|---------|-----|--------|--------|-----------|
| PCI DSS Level 1 | Year 2 goal | ✅ | ✅ | ✅ |
| Tokenization | ✅ (Stripe) | ✅ | Native | Native |
| DTMF masking | ✅ (planned) | ✅ | N/A | N/A |
| Voice payment support | ✅ (planned) | ⬜ | N/A | N/A |
| SAQ D service provider | Year 2 goal | ✅ | ✅ | ✅ |

## Tools & Resources

- **PCI compliance consultants:** SecurityMetrics, ControlCase, Coalfire
- **ASV scanning:** Trustwave, SecurityMetrics, ControlCase
- **Penetration testing:** NCC Group, Bishop Fox, Cure53
- **Tokenization:** Stripe (easiest), Basis Theory, Spreedly
- **HSM:** AWS CloudHSM, Azure Dedicated HSM, HashiCorp Vault
- **QSA assessment:** Qualified Security Assessor (list on PCI Council website)
