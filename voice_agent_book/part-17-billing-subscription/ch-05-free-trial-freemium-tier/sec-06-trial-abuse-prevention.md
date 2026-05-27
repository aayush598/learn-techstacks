# Section 06: Trial Abuse Prevention

## Email Domain Blocking

Free trials attract abuse from users who create multiple accounts to exploit free resources. Email domain blocking prevents disposable email addresses and known abuse domains from creating trials.

```typescript
interface AbuseDetectionRule {
  type: 'domain_block' | 'email_pattern' | 'ip_range' | 'card_fingerprint' | 'device_fingerprint';
  action: 'block' | 'flag' | 'require_approval';
  parameters: Record<string, any>;
  priority: number;
}

class AbuseDetectionService {
  private readonly BLOCKED_DOMAINS = [
    'tempmail.com', 'mailinator.com', 'guerrillamail.com',
    '10minutemail.com', 'throwaway.email', 'yopmail.com',
    'sharklasers.com', 'trashmail.com', 'temp-mail.org',
    // ... maintained as a configurable blocklist
  ];

  private readonly SUSPICIOUS_PATTERNS = [
    /^test/i,
    /^temp/i,
    /^abc\d+@/i,
    /\+\w+@/, // Gmail plus addressing
  ];

  async check(tenant: Tenant): Promise<AbuseCheckResult> {
    const checks = await Promise.all([
      this.checkEmailDomain(tenant.email),
      this.checkEmailPattern(tenant.email),
      this.checkIpReputation(tenant.signupIp),
      this.checkExistingAccounts(tenant),
      this.checkDeviceFingerprint(tenant.fingerprint),
    ]);

    const suspicious = checks.filter(c => c.suspicious);
    const blocked = checks.find(c => c.action === 'block');

    if (blocked) {
      return {
        isSuspicious: true,
        action: 'block',
        reason: blocked.reason,
        checks: checks,
      };
    }

    if (suspicious.length > 0) {
      return {
        isSuspicious: true,
        action: 'flag',
        reason: `Flagged by ${suspicious.length} check(s)`,
        checks: checks,
      };
    }

    return {
      isSuspicious: false,
      action: 'allow',
      checks: checks,
    };
  }

  private async checkEmailDomain(email: string): Promise<CheckResult> {
    const domain = email.split('@')[1]?.toLowerCase();
    const isBlocked = this.BLOCKED_DOMAINS.includes(domain);

    return {
      type: 'domain_block',
      suspicious: isBlocked,
      action: isBlocked ? 'block' : 'allow',
      reason: isBlocked ? `Blocked domain: ${domain}` : undefined,
    };
  }

  private async checkEmailPattern(email: string): Promise<CheckResult> {
    const matchesPattern = this.SUSPICIOUS_PATTERNS.some(p => p.test(email));
    return {
      type: 'email_pattern',
      suspicious: matchesPattern,
      action: matchesPattern ? 'flag' : 'allow',
      reason: matchesPattern ? 'Suspicious email pattern' : undefined,
    };
  }

  private async checkIpReputation(ip: string): Promise<CheckResult> {
    // Check against known VPN/proxy IP ranges
    // Use IP geolocation data
    const isVpn = await this.ipReputationService.isVpn(ip);
    const isDatacenter = await this.ipReputationService.isDatacenterIp(ip);

    return {
      type: 'ip_range',
      suspicious: isVpn || isDatacenter,
      action: isVpn ? 'require_approval' : isDatacenter ? 'flag' : 'allow',
      reason: isVpn ? 'VPN IP detected' : isDatacenter ? 'Datacenter IP' : undefined,
    };
  }

  private async checkExistingAccounts(tenant: Tenant): Promise<CheckResult> {
    // Check if this email/phone has been used before
    const existingByEmail = await this.db.tenants.countDocuments({
      email: tenant.email,
    });

    const existingByPhone = tenant.phone
      ? await this.db.tenants.countDocuments({ phone: tenant.phone })
      : 0;

    const hasExisting = existingByEmail > 0 || existingByPhone > 0;

    return {
      type: 'existing_account',
      suspicious: hasExisting,
      action: hasExisting ? 'block' : 'allow',
      reason: hasExisting ? 'Account already exists' : undefined,
    };
  }
}
```

## Credit Card Uniqueness

For trials that require a payment method, credit card fingerprinting prevents users from starting multiple trials with different cards from the same bank account.

```typescript
class CardFingerprintService {
  async checkCardFingerprint(
    paymentMethodId: string
  ): Promise<CheckResult> {
    const paymentMethod = await stripe.paymentMethods.retrieve(paymentMethodId);
    const fingerprint = paymentMethod.card?.fingerprint;

    if (!fingerprint) {
      return { type: 'card_fingerprint', suspicious: false, action: 'allow' };
    }

    // Check if this card has been used for a trial before
    const previousTrials = await this.db.trials.countDocuments({
      cardFingerprint: fingerprint,
      createdAt: {
        $gte: new Date(Date.now() - 180 * 86400000).toISOString(), // 6 months
      },
    });

    const isDuplicate = previousTrials > 0;

    return {
      type: 'card_fingerprint',
      suspicious: isDuplicate,
      action: isDuplicate ? 'block' : 'allow',
      reason: isDuplicate ? 'Card has been used for previous trial' : undefined,
    };
  }
}
```

## Phone Verification

Phone verification adds a layer of identity verification for high-risk signups. Users receive an SMS with a verification code that must be entered to activate the trial.

```typescript
class PhoneVerificationService {
  async initiateVerification(phone: string): Promise<string> {
    const code = Math.floor(100000 + Math.random() * 900000).toString();

    await this.smsService.send({
      to: phone,
      message: `Your Voice Agent Platform verification code: ${code}`,
    });

    // Store verification code with 5-minute expiry
    const key = `phone_verify:${phone}`;
    await this.redis.setex(key, 300, JSON.stringify({
      code,
      attempts: 0,
      createdAt: Date.now(),
    }));

    return code.slice(0, 2) + '****'; // Masked for display
  }

  async verifyCode(phone: string, code: string): Promise<boolean> {
    const key = `phone_verify:${phone}`;
    const data = await this.redis.get(key);

    if (!data) return false;

    const record = JSON.parse(data);
    record.attempts++;

    if (record.attempts > 5) {
      await this.redis.del(key);
      return false;
    }

    await this.redis.setex(key, 300, JSON.stringify(record));

    if (record.code === code) {
      await this.redis.del(key);
      return true;
    }

    return false;
  }
}
```

## IP/Device Fingerprinting

Browser fingerprinting collects device characteristics (screen resolution, browser plugins, timezone, fonts) to identify devices used for previous trials.

```typescript
interface DeviceFingerprint {
  userAgent: string;
  screenResolution: string;
  timezone: string;
  language: string;
  platform: string;
  canvasFingerprint: string;
  webglFingerprint: string;
  fonts: string[];
  plugins: string[];
}

class DeviceFingerprintService {
  async checkFingerprint(
    fingerprint: DeviceFingerprint
  ): Promise<CheckResult> {
    // Hash the fingerprint for storage
    const hash = this.hashFingerprint(fingerprint);

    // Check if this device was used for a trial before
    const previousUse = await this.db.deviceFingerprints.findOne({
      hash,
      lastSeen: {
        $gte: new Date(Date.now() - 90 * 86400000).toISOString(),
      },
    });

    if (previousUse) {
      // Update last seen
      await this.db.deviceFingerprints.updateOne(
        { hash },
        { $set: { lastSeen: new Date().toISOString(), count: previousUse.count + 1 } }
      );

      return {
        type: 'device_fingerprint',
        suspicious: previousUse.count >= 3,
        action: previousUse.count >= 3 ? 'block' : 'flag',
        reason: previousUse.count >= 3
          ? 'Device used for multiple trials'
          : 'Device seen before',
      };
    }

    // Store new fingerprint
    await this.db.deviceFingerprints.create({
      hash,
      firstSeen: new Date().toISOString(),
      lastSeen: new Date().toISOString(),
      count: 1,
    });

    return { type: 'device_fingerprint', suspicious: false, action: 'allow' };
  }

  private hashFingerprint(fp: DeviceFingerprint): string {
    const normalized = `${fp.userAgent}|${fp.screenResolution}|${fp.timezone}|${fp.canvasFingerprint}|${fp.webglFingerprint}`;
    return crypto.createHash('sha256').update(normalized).digest('hex');
  }
}
```

## Open-Source Tools

- **Stripe API** — Card fingerprinting through PaymentMethod
- **Redis** — Phone verification code storage with TTL
- **PostgreSQL** — Device fingerprints and abuse records
- **FingerprintJS** (MIT) — Browser fingerprinting library
- **BullMQ** — Schedule abuse rule updates

## Integration Points

Abuse prevention connects to the authentication service (signup flow), the trial eligibility service (Section 1), and the notification service (alert on suspicious signups).

## Production Considerations

- Review abuse detection logs weekly for false positives
- Maintain blocklist as a configuration file in the repository
- Implement manual review queue for flagged signups
- Update abuse rules based on observed attack patterns
- Balance security with conversion (overly strict rules hurt legitimate users)

## Open-Source First Philosophy

FingerprintJS (MIT) provides device fingerprinting without proprietary tracking services. Redis handles verification code storage. PostgreSQL stores abuse detection data. This all-open-source abuse prevention stack avoids costly fraud detection services while providing effective protection against trial abuse.
