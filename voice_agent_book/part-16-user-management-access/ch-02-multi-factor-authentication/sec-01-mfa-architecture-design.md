# MFA Architecture Design

## Overview

Multi-factor authentication (MFA) adds a second verification layer beyond passwords, significantly reducing account compromise risk. The architecture must support multiple factor types (TOTP, SMS OTP, email OTP, WebAuthn, backup codes), enrollment workflows, and adaptive challenge policies.

## Factor Classification

```
Authentication Factors
├── Knowledge (something you know)
│   ├── Password
│   └── Security questions
├── Possession (something you have)
│   ├── TOTP (Authenticator app)
│   ├── SMS/Email OTP
│   ├── Hardware security key (FIDO2)
│   └── Push notification to phone
└── Inherence (something you are)
    ├── Fingerprint
    ├── Face recognition
    └── Voice biometric
```

## MFA System Architecture

```
[User] → Login → Password OK?
               ├── No → Return error
               └── Yes → MFA Required?
                           ├── No → Issue session
                           └── Yes → MFA Challenge Selection
                                       ├── TOTP
                                       ├── SMS/Email OTP
                                       ├── WebAuthn
                                       └── Backup Code
                                           └── Verify → Success → Issue session
                                                         └── Failure → Retry (max N) → Lockout
```

## Architecture Components

```typescript
interface MfaFactor {
  id: string;
  type: MfaFactorType;
  userId: string;
  tenantId: string;
  enabled: boolean;
  createdAt: Date;
  lastUsedAt?: Date;
  metadata: Record<string, unknown>;
}

type MfaFactorType =
  | 'totp'
  | 'sms_otp'
  | 'email_otp'
  | 'webauthn'
  | 'backup_code'
  | 'push_notification';

interface MfaChallenge {
  id: string;
  factorId: string;
  userId: string;
  type: MfaFactorType;
  state: 'pending' | 'verified' | 'expired' | 'failed';
  expiresAt: Date;
  attemptsRemaining: number;
  metadata: Record<string, unknown>;
}

interface MfaVerificationResult {
  verified: boolean;
  factorId: string;
  type: MfaFactorType;
  attemptsRemaining?: number;
  locked?: boolean;
}
```

## Challenge-Response Flow

```typescript
class MfaChallengeService {
  async createChallenge(userId: string, factorType: MfaFactorType): Promise<MfaChallenge> {
    const factor = await this.factorStore.findActiveFactor(userId, factorType);
    if (!factor) throw new Error('MFA factor not found or not enabled');

    let challenge: MfaChallenge;

    switch (factorType) {
      case 'totp':
        challenge = await this.createTotpChallenge(factor);
        break;
      case 'sms_otp':
        challenge = await this.createOtpChallenge(factor, 'sms');
        break;
      case 'email_otp':
        challenge = await this.createOtpChallenge(factor, 'email');
        break;
      case 'webauthn':
        challenge = await this.createWebAuthnChallenge(factor);
        break;
      case 'backup_code':
        challenge = await this.createBackupCodeChallenge(factor);
        break;
    }

    await this.challengeStore.save(challenge);
    return challenge;
  }

  async verifyChallenge(
    challengeId: string,
    response: string
  ): Promise<MfaVerificationResult> {
    const challenge = await this.challengeStore.findById(challengeId);
    if (!challenge) {
      return { verified: false, factorId: '', type: 'totp', attemptsRemaining: 0 };
    }

    if (challenge.state !== 'pending' || challenge.expiresAt < new Date()) {
      return { verified: false, factorId: challenge.factorId, type: challenge.type };
    }

    const factor = await this.factorStore.findById(challenge.factorId);
    const verified = await this.verifyResponse(factor!, challenge, response);

    if (verified) {
      await this.challengeStore.update(challengeId, { state: 'verified' });
      await this.factorStore.updateLastUsed(challenge.factorId);
      return { verified: true, factorId: challenge.factorId, type: challenge.type };
    }

    challenge.attemptsRemaining--;
    if (challenge.attemptsRemaining <= 0) {
      await this.challengeStore.update(challengeId, { state: 'failed' });
      return { verified: false, factorId: challenge.factorId, type: challenge.type, locked: true };
    }

    await this.challengeStore.update(challengeId, { attemptsRemaining: challenge.attemptsRemaining });
    return {
      verified: false,
      factorId: challenge.factorId,
      type: challenge.type,
      attemptsRemaining: challenge.attemptsRemaining,
    };
  }
}
```

## Factor Enrollment Flow

```
[User] → Settings → Security → Enable MFA
    ↓
[Select Factor Type]
    ├── TOTP: Scan QR code → Verify code
    ├── SMS: Verify phone → Send test code
    ├── Email: Verify email → Send test code
    ├── WebAuthn: Register device → Biometric prompt
    └── Backup codes: Generate → Download → Verify one
    ↓
[Factor Activated]
    ├── Generate recovery codes (if first factor)
    └── Update user MFA status
```

## Open-Source Tools

- **otplib** — TOTP and HOTP implementation
- **speakeasy** — One-time password generation
- **SimpleWebAuthn** — WebAuthn/FIDO2 browser library
- **node-2fa** — Two-factor authentication utilities

## Production Considerations

- Rate-limit MFA challenge creation per user (max 5 per minute)
- Lock account after 5 consecutive failed MFA attempts
- Provide session token that skips MFA for trusted devices (30-day trust)
- Store challenge timeouts in Redis with automatic expiry
- Audit log all MFA events (enrollment, verification attempts, failures)
- Allow bypass for test/sandbox accounts in non-production environments only
