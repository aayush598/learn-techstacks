# Chapter 02: Multi-Factor Authentication

> **Part:** 16 - User Management & Access Control

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [MFA Architecture Design](sec-01-mfa-architecture-design.md) | MFA factors (knowledge, possession, inherence), factor enrollment, challenge-response flow |
| 02 | [TOTP Implementation](sec-02-totp-implementation.md) | Time-based one-time passwords, shared secret generation, authenticator app integration, recovery |
| 03 | [SMS/Email OTP Delivery](sec-03-sms-email-otp.md) | OTP generation, delivery via SMS/email, rate limiting delivery, delivery cost optimization |
| 04 | [WebAuthn / FIDO2 Passkeys](sec-04-webauthn-fido2-passkeys.md) | Public key credential creation, authentication ceremony, platform vs roaming authenticators |
| 05 | [Backup Codes & Recovery](sec-05-backup-codes-recovery.md) | One-time backup code generation, secure storage, recovery workflow, code revocation |
| 06 | [MFA Enrollment Flow](sec-06-mfa-enrollment-flow.md) | Forced enrollment policy, step-up authentication, device trust, enrollment completion rate optimization |
| 07 | [Adaptive / Risk-Based MFA](sec-07-adaptive-risk-based-mfa.md) | Risk scoring factors (IP, device, location, behavior), step-up challenges, low-risk exemptions |
| 08 | [MFA Compliance Requirements](sec-08-mfa-compliance-requirements.md) | SOC 2 MFA requirements, HIPAA technical safeguards, PCI DSS MFA for admin access |

---

## MFA Verification Flow

```
Login Attempt (password correct)
    ↓
[Risk Assessment]
    ├── Low Risk → Skip MFA (device trust)
    └── High Risk → Require MFA
                       ↓
[MFA Challenge]
    ├── TOTP (Authenticator App)
    ├── SMS/Email OTP
    ├── Push Notification
    └── WebAuthn (Biometric/Security Key)
                       ↓
[Verify] → Success → Issue Token
              ↓
       Failure → Retry (max 3) → Lockout
```

---

## Learning Objectives

- Design MFA architecture supporting multiple factor types
- Implement TOTP with authenticator app integration
- Build SMS/Email OTP delivery with rate limiting
- Integrate WebAuthn/FIDO2 passkeys for biometric auth
- Create backup codes and account recovery workflow
- Design MFA enrollment flow with forced enrollment policies
- Implement adaptive risk-based MFA challenge decisions
- Meet MFA compliance requirements (SOC 2, HIPAA, PCI)
