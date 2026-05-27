# Chapter 06: PCI DSS Payment Security

> **Part:** 15 - Security, Compliance & Governance

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [PCI DSS Scope Definition](sec-01-pci-dss-scope-definition.md) | Cardholder data environment, scope reduction, segmentation, CDE boundary documentation |
| 02 | [Card Data Flow Mapping](sec-02-card-data-flow-mapping.md) | Data flow diagrams, touch points, storage locations, transmission paths, third-party handoffs |
| 03 | [Tokenization & Vaulting](sec-03-tokenization-vaulting.md) | PCI-listed tokenization, vault architecture, detokenization controls, token format preservation |
| 04 | [SAQ Selection & Compliance](sec-04-saq-selection-compliance.md) | SAQ A through D eligibility, merchant level determination, compliance validation |
| 05 | [Secure Payment Integration](sec-05-secure-payment-integration.md) | Stripe Elements, iframe-based collection, direct post, 3D Secure, SCA compliance |
| 06 | [PCI-Compliant Voice Payments](sec-06-pci-compliant-voice-payments.md) | DTMF capture, IVR payment flows, PCI-compliant recording pausing, key masking |
| 07 | [Quarterly ASV Scanning](sec-07-asv-scanning.md) | Approved scanning vendor, external vulnerability scans, passing criteria, scan remediation |
| 08 | [PCI Training & Awareness](sec-08-pci-training-awareness.md) | Annual security training, role-specific training, phishing awareness, attestation tracking |

---

## PCI DSS 4.0 Requirements

| Requirement | Description | Key Implementation |
|-------------|-------------|-------------------|
| 1 | Install firewall configuration | Network segmentation, CDE isolation |
| 2 | Secure configuration | Hardened images, default password removal |
| 3 | Protect stored cardholder data | Tokenization, encryption, truncation |
| 4 | Encrypt transmission | TLS 1.2+, strong ciphers |
| 5 | Protect against malware | Antivirus, EDR, file integrity monitoring |
| 6 | Secure systems/applications | Patch management, secure coding |
| 7 | Restrict access | Need-to-know, role-based access |
| 8 | Identify and authenticate | MFA, unique IDs, password policies |
| 9 | Restrict physical access | Data center controls, device security |
| 10 | Monitor and test networks | Audit logging, intrusion detection |
| 11 | Test security | ASV scanning, penetration testing |
| 12 | Information security policy | Policies, risk assessment, training |
