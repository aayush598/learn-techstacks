# Part 15: Security, Compliance & Governance

> **Duration:** Security Phase (Ongoing, begins Week 4)  
> **Goal:** Build a security-first platform with enterprise compliance (GDPR, HIPAA, SOC 2, PCI DSS), encryption, and governance.

---

## Chapters Overview

| # | Chapter | Description |
|---|---------|-------------|
| 01 | [Security Architecture & Threat Model](ch-01-security-architecture-threat-model/README.md) | Zero-trust architecture, threat modeling (STRIDE), attack surface analysis, security controls mapping |
| 02 | [Encryption Strategy (At Rest & In Transit)](ch-02-encryption-strategy/README.md) | TLS 1.3, AES-256 encryption, envelope encryption, key management (HashiCorp Vault), encryption at application layer |
| 03 | [GDPR Compliance Toolkit](ch-03-gdpr-compliance-toolkit/README.md) | Data mapping, consent management, right to erasure, data portability, DPA, breach notification |
| 04 | [HIPAA Compliance for Healthcare](ch-04-hipaa-compliance-healthcare/README.md) | BAAs, PHI identification, access controls, audit controls, integrity controls, transmission security |
| 05 | [SOC 2 Type II Readiness](ch-05-soc2-readiness/README.md) | Trust services criteria, control activities, evidence collection, auditor preparation, continuous monitoring |
| 06 | [PCI DSS & Payment Security](ch-06-pci-dss-payment-security/README.md) | Cardholder data protection, SAQ validation, tokenization, voice payment PCI compliance |
| 07 | [TCPA & Outbound Calling Compliance](ch-07-tcpa-outbound-calling-compliance/README.md) | Prior express consent, revocation tracking, calling hours, DNC list management, call recording consent |
| 08 | [Role-Based Access Control (RBAC)](ch-08-role-based-access-control/README.md) | Role hierarchy, permission model, resource-level permissions, policy evaluation, custom roles |
| 09 | [Audit Logging & Forensics](ch-09-audit-logging-forensics/README.md) | Immutable audit trail, event correlation, user action tracking, system event logging, SIEM integration |
| 10 | [Data Residency & Sovereignty](ch-10-data-residency-sovereignty/README.md) | Regional data storage (US/EU/APAC), data classification, cross-border transfer, Schrems II compliance |

---

## Compliance Matrix

| Requirement | GDPR | HIPAA | SOC 2 | PCI DSS | TCPA |
|-------------|------|-------|-------|---------|------|
| Encryption | ✅ | ✅ | ✅ | ✅ | — |
| Access Control | ✅ | ✅ | ✅ | ✅ | — |
| Audit Logs | ✅ | ✅ | ✅ | ✅ | ✅ |
| Data Deletion | ✅ | ✅ | — | — | — |
| Consent | ✅ | ✅ | — | — | ✅ |
| Breach Notification | ✅ | ✅ | — | ✅ | — |

---

## Key Open-Source Tools

- **HashiCorp Vault** (MPL 2.0) — Secrets & encryption management
- **Let's Encrypt** (Mozilla) — TLS certificates
- **OpenSSL** (Apache 2.0) — Cryptography
- **presidio** (MIT) — PII detection (Microsoft)
- **Wazuh** (GPL 2.0) — SIEM & security monitoring
- **OAuth.js** (MIT) — Auth & session management

---

## Learning Objectives

- Design a zero-trust security architecture for a multi-tenant SaaS
- Implement encryption at rest and in transit with key management
- Build GDPR compliance tools for data subject requests
- Configure HIPAA-compliant mode for healthcare use cases
- Prepare for SOC 2 Type II audit with continuous controls
- Implement PCI DSS compliant voice payment processing
- Ensure TCPA compliance for outbound calling campaigns
- Build a granular RBAC system with custom roles
- Create immutable audit logging with SIEM integration
- Implement data residency controls for global operations
