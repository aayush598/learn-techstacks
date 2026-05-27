# Adaptive / Risk-Based MFA

## Overview

Adaptive MFA (risk-based authentication) dynamically adjusts authentication requirements based on contextual risk factors. Low-risk scenarios skip MFA entirely while high-risk scenarios require additional verification, balancing security with user convenience.

## Risk Scoring Factors

```
┌─────────────────────────────────────────────────────┐
│                 Risk Assessment Engine               │
├─────────────────────────────────────────────────────┤
│  Input Signals                                       │
│  ├── IP Reputation (known proxy/VPN, blacklist)      │
│  ├── Geolocation (distance from last login)          │
│  ├── Device Fingerprint (known/unknown device)       │
│  ├── Browser/User Agent (known pattern)              │
│  ├── Time of Day (business hours vs 3 AM)            │
│  ├── Login Velocity (multiple attempts)              │
│  ├── Resource Sensitivity (admin vs view-only)       │
│  └── Behavioral Pattern (typing speed, mouse moves)  │
├─────────────────────────────────────────────────────┤
│  Scoring                                             │
│  └── Weighted sum → Risk Score (0-100)              │
├─────────────────────────────────────────────────────┤
│  Action                                              │
│  ├── 0-30: Low Risk → No MFA                         │
│  ├── 31-60: Medium Risk → TOTP/SMS OTP              │
│  ├── 61-85: High Risk → WebAuthn + OTP              │
│  └── 86-100: Critical → Block + Alert Admin          │
└─────────────────────────────────────────────────────┘
```

## Risk Scoring Implementation

```typescript
interface RiskFactor {
  name: string;
  weight: number;
  score: number; // 0-100
}

interface RiskAssessment {
  score: number;
  level: 'low' | 'medium' | 'high' | 'critical';
  factors: RiskFactor[];
  recommendation: MfaAction;
}

type MfaAction = 'skip' | 'totp' | 'otp' | 'webauthn' | 'totp_and_otp' | 'block';

class RiskAssessmentEngine {
  async assess(request: AuthRequest): Promise<RiskAssessment> {
    const factors: RiskFactor[] = await Promise.all([
      this.assessIpReputation(request.ip),
      this.assessGeolocation(request.userId, request.ip),
      this.assessDeviceFingerprint(request.userId, request.deviceFingerprint),
      this.assessLoginVelocity(request.userId),
      this.assessTimeOfDay(),
      this.assessResourceSensitivity(request.resource),
    ]);

    const weightedScore = factors.reduce((sum, f) => sum + f.score * f.weight, 0);
    const totalWeight = factors.reduce((sum, f) => sum + f.weight, 0);
    const finalScore = Math.min(100, Math.round(weightedScore / totalWeight));

    return {
      score: finalScore,
      level: this.categorizeScore(finalScore),
      factors,
      recommendation: this.getMfaAction(finalScore),
    };
  }

  private async assessIpReputation(ip: string): Promise<RiskFactor> {
    const isProxy = await this.ipReputationService.isProxy(ip);
    const isKnown = await this.ipReputationService.isKnownGood(ip);
    const score = isProxy ? 90 : isKnown ? 10 : 40;
    return { name: 'ip_reputation', weight: 0.25, score };
  }

  private async assessGeolocation(userId: string, ip: string): Promise<RiskFactor> {
    const currentLocation = await this.geoService.lookup(ip);
    const lastLogin = await this.getLastLoginLocation(userId);

    if (!lastLogin) return { name: 'geolocation', weight: 0.15, score: 20 };

    const distance = this.calculateDistance(currentLocation, lastLogin);
    const timeSince = Date.now() - lastLogin.timestamp.getTime();

    // Impossible travel detection
    if (distance > 500 && timeSince < 3600000) {
      return { name: 'geolocation', weight: 0.15, score: 95 };
    }

    const score = Math.min(80, Math.round(distance / 100));
    return { name: 'geolocation', weight: 0.15, score };
  }

  private async assessDeviceFingerprint(userId: string, fingerprint: string): Promise<RiskFactor> {
    const isKnown = await this.deviceTrustService.isDeviceTrusted(userId, fingerprint);

    if (isKnown) {
      return { name: 'device_fingerprint', weight: 0.20, score: 5 };
    }

    const hasOtherDevices = await this.hasOtherTrustedDevices(userId);
    const score = hasOtherDevices ? 40 : 70;
    return { name: 'device_fingerprint', weight: 0.20, score };
  }

  private async assessLoginVelocity(userId: string): Promise<RiskFactor> {
    const recentAttempts = await this.getRecentLoginAttempts(userId, 300000); // 5 min

    if (recentAttempts.length > 20) {
      return { name: 'login_velocity', weight: 0.15, score: 100 };
    }
    if (recentAttempts.length > 10) {
      return { name: 'login_velocity', weight: 0.15, score: 70 };
    }
    if (recentAttempts.length > 5) {
      return { name: 'login_velocity', weight: 0.15, score: 40 };
    }

    return { name: 'login_velocity', weight: 0.15, score: 5 };
  }

  private categorizeScore(score: number): 'low' | 'medium' | 'high' | 'critical' {
    if (score <= 30) return 'low';
    if (score <= 60) return 'medium';
    if (score <= 85) return 'high';
    return 'critical';
  }

  private getMfaAction(score: number): MfaAction {
    if (score <= 30) return 'skip';
    if (score <= 60) return 'totp';
    if (score <= 75) return 'otp';
    if (score <= 85) return 'webauthn';
    return 'block';
  }
}
```

## Challenge Selection Based on Risk

```typescript
class AdaptiveMfaService {
  async determineRequiredFactors(userId: string, assessment: RiskAssessment): Promise<MfaRequirement> {
    const enrolledFactors = await this.mfaService.getEnrolledFactors(userId);

    switch (assessment.recommendation) {
      case 'skip':
        return { required: false, factors: [] };

      case 'totp':
        if (enrolledFactors.includes('totp')) {
          return { required: true, factors: ['totp'], stepUp: false };
        }
        return { required: true, factors: ['sms_otp', 'email_otp'], stepUp: false };

      case 'webauthn':
        if (enrolledFactors.includes('webauthn')) {
          return { required: true, factors: ['webauthn'], stepUp: false };
        }
        return this.determineRequiredFactors(userId, { ...assessment, recommendation: 'totp' });

      case 'block':
        await this.alertService.sendSecurityAlert(userId, assessment);
        return { required: true, factors: [], block: true };
    }
  }
}
```

## Feedback Loop

```typescript
class RiskFeedbackService {
  async recordUserFeedback(userId: string, sessionId: string, wasBlocked: boolean, userReportedFraud: boolean): Promise<void> {
    const riskAssessment = await this.getStoredAssessment(sessionId);
    if (!riskAssessment) return;

    // Adjust factor weights based on outcomes
    if (userReportedFraud && riskAssessment.score < 50) {
      // Underscored - need to increase weight on certain factors
      await this.adjustFactorWeights(riskAssessment.factors, 'increase');
    }

    if (!wasBlocked && userReportedFraud) {
      // False negative - model needs adjustment
      await this.recordFalseNegative(riskAssessment);
    }

    if (wasBlocked && !userReportedFraud) {
      // False positive - model too aggressive
      await this.recordFalsePositive(riskAssessment);
    }
  }
}
```

## Open-Source Tools

- **maxmind** (IP geolocation database)
- **geoip-lite** (Lightweight GeoIP lookup)
- **express-rate-limit** (Login velocity tracking)

## Production Considerations

- Record all risk assessments for audit and model improvement
- Monitor false positive rate (users blocked but legitimate) and false negative rate (fraud allowed through)
- Provide dashboard for security team to review risk decisions
- Allow tenants to configure their own risk thresholds
- A/B test different risk models to optimize security vs convenience
- Cache IP reputation lookups to reduce latency
- Ensure GDPR compliance: obtaining consent for device fingerprinting and behavioral analysis
