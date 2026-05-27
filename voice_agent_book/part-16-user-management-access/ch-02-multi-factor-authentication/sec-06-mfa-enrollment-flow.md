# MFA Enrollment Flow

## Overview

MFA enrollment guides users through setting up their first (or additional) authentication factor. The enrollment flow must balance security requirements with user experience to maximize adoption rates while meeting compliance mandates.

## Enrollment Flow Architecture

```
┌─────────────┐     ┌─────────────────┐     ┌────────────────┐
│  User       │     │  Enrollment     │     │  Factor        │
│  Settings   │────→│  Service        │────→│  Provisioner   │
└─────────────┘     └─────────────────┘     └────────────────┘
                           │                        │
                    ┌──────▼──────┐         ┌───────▼───────┐
                    │  Policy     │         │  Factor       │
                    │  Engine     │         │  Store        │
                    └──────┬──────┘         └───────────────┘
                           │
                    ┌──────▼──────┐
                    │  Compliance │
                    │  Checker    │
                    └─────────────┘
```

## Enrollment Policy Configuration

```typescript
interface MfaEnrollmentPolicy {
  tenantId: string;
  enabled: boolean;
  enforced: boolean;                       // Force MFA for all users
  gracePeriodDays: number;                 // Days before enforcement kicks in
  minimumFactors: number;                  // Minimum factors required (default 1)
  allowedFactorTypes: MfaFactorType[];     // Which factors users can enroll
  bypassRoles: string[];                   // Roles exempt from MFA
  exemptUserIds: string[];                 // Individual user exemptions
  requireForRoles: string[];               // Roles that MUST have MFA
  rememberDeviceDays: number;              // Trust device duration
}

interface MfaEnrollmentState {
  userId: string;
  enrollmentStatus: 'not_started' | 'in_progress' | 'completed' | 'exempt';
  enrolledFactors: string[];
  enrolledAt?: Date;
  lastFactorUsedAt?: Date;
  gracePeriodEnds?: Date;
  deviceTrustTokens: DeviceTrust[];
}
```

## Forced Enrollment

```typescript
class MfaEnforcementService {
  async checkEnforcement(userId: string): Promise<EnforcementResult> {
    const user = await this.userService.getUser(userId);
    const policy = await this.getTenantPolicy(user.tenantId);

    if (!policy.enabled) {
      return { requiresMfa: false, reason: 'mfa_disabled' };
    }

    if (policy.bypassRoles.includes(user.primaryRole)) {
      return { requiresMfa: false, reason: 'role_exempt' };
    }

    if (policy.exemptUserIds.includes(userId)) {
      return { requiresMfa: false, reason: 'user_exempt' };
    }

    const state = await this.getEnrollmentState(userId);

    if (state.enrollmentStatus === 'completed') {
      return { requiresMfa: false, reason: 'already_enrolled' };
    }

    // Check if user is in a required role
    const isRequiredRole = policy.requireForRoles.some(role =>
      user.roles.includes(role)
    );

    if (isRequiredRole && state.enrollmentStatus === 'not_started') {
      return {
        requiresMfa: true,
        reason: 'role_requires_mfa',
        gracePeriodEnds: null,
        blocking: true,
      };
    }

    // Check grace period
    if (state.enrollmentStatus === 'not_started' && policy.gracePeriodDays > 0) {
      const userCreatedAt = user.createdAt;
      const graceEnd = new Date(userCreatedAt.getTime() + policy.gracePeriodDays * 86400000);

      if (new Date() > graceEnd) {
        return {
          requiresMfa: true,
          reason: 'grace_period_expired',
          gracePeriodEnds: graceEnd,
          blocking: true,
        };
      }

      return {
        requiresMfa: true,
        reason: 'in_grace_period',
        gracePeriodEnds: graceEnd,
        blocking: false, // Warn but don't block
      };
    }

    return { requiresMfa: false, reason: 'not_enforced' };
  }
}
```

## Step-Up Authentication

When accessing sensitive operations (API key management, billing, settings), require fresh MFA even if the user has an active session:

```typescript
interface StepUpAuthService {
  async requireStepUp(userId: string, requiredLevel: SecurityLevel): Promise<boolean> {
    const session = await this.sessionService.getCurrentSession(userId);

    // Check if MFA was verified recently (within step-up window)
    if (session.mfaVerified && session.mfaVerifiedAt) {
      const windowMinutes = this.getStepUpWindow(requiredLevel);
      const elapsed = (Date.now() - session.mfaVerifiedAt.getTime()) / 60000;
      if (elapsed < windowMinutes) {
        return true; // Recent MFA verification satisfies
      }
    }

    return false; // Step-up MFA required
  }

  private getStepUpWindow(level: SecurityLevel): number {
    switch (level) {
      case 'standard': return 60;   // 1 hour
      case 'sensitive': return 15;  // 15 minutes
      case 'critical': return 0;    // Always require fresh MFA
    }
  }
}
```

## Device Trust

```typescript
interface DeviceTrust {
  deviceFingerprint: string;
  trustedAt: Date;
  expiresAt: Date;
  userAgent: string;
  lastIpAddress: string;
}

class DeviceTrustService {
  private readonly TRUST_DURATION_DAYS = 30;

  async trustDevice(userId: string, fingerprint: string, userAgent: string, ip: string): Promise<void> {
    const trust: DeviceTrust = {
      deviceFingerprint: fingerprint,
      trustedAt: new Date(),
      expiresAt: new Date(Date.now() + this.TRUST_DURATION_DAYS * 86400000),
      userAgent,
      lastIpAddress: ip,
    };

    await this.db.upsert('device_trust', {
      userId,
      deviceFingerprint: fingerprint,
    }, trust);
  }

  async isDeviceTrusted(userId: string, fingerprint: string): Promise<boolean> {
    const trust = await this.db.findOne('device_trust', {
      userId,
      deviceFingerprint: fingerprint,
    });

    if (!trust) return false;
    if (trust.expiresAt < new Date()) {
      await this.db.delete('device_trust', { id: trust.id });
      return false;
    }

    return true;
  }
}
```

## Enrollment Dashboard

```
MFA Status: ● Protected
Factors Enrolled:
  ├── TOTP (Google Authenticator) — Last used 2 days ago
  └── Backup Codes (10 remaining)

Available Factors to Add:
  ├── + SMS/Email OTP
  ├── + Security Key (WebAuthn)
  └── + Push Notification (Mobile App)

Security Score: 85/100
```

## Open-Source Tools

- **Auth.js** — Session management integration
- **ioredis** — Challenge/state storage

## Production Considerations

- Track enrollment funnel metrics: started → completed → verified
- Send reminder emails for users in grace period (at 7 days, 3 days, 1 day, and day of expiry)
- Provide dedicated support flow for users who lose all MFA access
- Enforce minimum one TOTP or WebAuthn factor (not just SMS, which is less secure)
- Allow MFA bypass for 24 hours after enrollment in case of setup errors
- Log all enrollment events with device info and IP for security audit
