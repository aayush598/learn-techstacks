# SMS/Email OTP Delivery

## Overview

OTP delivery via SMS and email provides a possession-factor verification channel using the user's registered phone number or email. While less secure than TOTP or WebAuthn, SMS/email OTP remains widely adopted due to its simplicity and universal device compatibility.

## OTP Generation & Storage

```typescript
interface OtpRecord {
  id: string;
  factorType: 'sms' | 'email';
  target: string;             // Phone number or email address
  codeHash: string;           // SHA-256 hash of OTP
  userId: string;
  tenantId: string;
  expiresAt: Date;
  attemptsRemaining: number;
  status: 'pending' | 'verified' | 'expired' | 'failed';
}

class OtpService {
  private generateOtp(length: number = 6): string {
    const digits = '0123456789';
    let otp = '';
    const bytes = randomBytes(length);
    for (let i = 0; i < length; i++) {
      otp += digits[bytes[i] % 10];
    }
    return otp;
  }

  async createAndSendOtp(
    userId: string,
    target: string,
    type: 'sms' | 'email'
  ): Promise<{ otpId: string; maskedTarget: string }> {
    // Rate limit check
    const recentCount = await this.getRecentOtpCount(userId, 5 * 60 * 1000);
    if (recentCount >= 5) {
      throw new OtpRateLimitError('Too many OTP requests. Please wait.');
    }

    const otp = this.generateOtp();
    const codeHash = createHash('sha256').update(otp).digest('hex');
    const expiresAt = new Date(Date.now() + 10 * 60 * 1000); // 10 minutes

    const record: OtpRecord = {
      id: `otp_${randomBytes(8).toString('hex')}`,
      factorType: type,
      target,
      codeHash,
      userId,
      tenantId: 'default',
      expiresAt,
      attemptsRemaining: 3,
      status: 'pending',
    };

    await this.db.insert('otp_records', record);
    await this.deliverOtp(type, target, otp, userId);

    return {
      otpId: record.id,
      maskedTarget: this.maskTarget(target, type),
    };
  }

  private maskTarget(target: string, type: 'sms' | 'email'): string {
    if (type === 'sms') {
      return target.replace(/(\d{3})\d{4}(\d{2})/, '$1****$2');
    }
    const [local, domain] = target.split('@');
    return `${local.slice(0, 2)}***@${domain}`;
  }
}
```

## SMS Delivery

```
[OTP Service] → [SMS Provider] → [Carrier Network] → [User Phone]
     │               │                    │
     │── Send OTP ──→│                    │
     │               │── Route to carrier │
     │               │                    │── Deliver SMS
     │               │───── Delivered ────│
     │←── Delivery Status ───────────────│
```

### Twilio SMS Integration

```typescript
import twilio from 'twilio';

interface SmsProvider {
  send(phoneNumber: string, message: string): Promise<DeliveryResult>;
}

class TwilioSmsProvider implements SmsProvider {
  private client: twilio.Twilio;

  constructor(accountSid: string, authToken: string) {
    this.client = twilio(accountSid, authToken);
  }

  async send(phoneNumber: string, message: string): Promise<DeliveryResult> {
    try {
      const result = await this.client.messages.create({
        body: message,
        to: phoneNumber,
        from: process.env.TWILIO_PHONE_NUMBER,
      });

      return {
        success: true,
        providerMessageId: result.sid,
        status: result.status,
        cost: result.price ? parseFloat(result.price) : 0,
      };
    } catch (error) {
      return { success: false, error: String(error) };
    }
  }
}
```

## Email Delivery

```
[OTP Service] → [Email Provider] → [SMTP/Mail API] → [User Inbox]
     │               │                    │
     │── Send OTP ──→│                    │
     │               │── SMTP Submission  │
     │               │                    │── Deliver to Inbox
     │               │───── Delivered ────│
     │←── Delivery Status ───────────────│
```

### Resend Email Integration

```typescript
import { Resend } from 'resend';

class ResendEmailProvider implements EmailProvider {
  private client: Resend;

  constructor(apiKey: string) {
    this.client = new Resend(apiKey);
  }

  async sendOtp(email: string, otp: string): Promise<DeliveryResult> {
    const html = `
      <div style="font-family: sans-serif; max-width: 480px;">
        <h2>Your Verification Code</h2>
        <div style="font-size: 32px; letter-spacing: 8px; text-align: center;
                    padding: 20px; background: #f5f5f5; border-radius: 8px;">
          ${otp}
        </div>
        <p style="color: #666;">This code expires in 10 minutes.</p>
        <p style="color: #666; font-size: 12px;">
          If you didn't request this code, ignore this email.
        </p>
      </div>
    `;

    const result = await this.client.emails.send({
      from: 'VoiceAgent <noreply@voiceagent.com>',
      to: email,
      subject: 'Your Verification Code',
      html,
    });

    return {
      success: true,
      providerMessageId: result.id,
      status: 'sent',
    };
  }
}
```

## Verification Flow

```typescript
class OtpVerifier {
  async verifyOtp(otpId: string, userCode: string): Promise<OtpVerificationResult> {
    const record = await this.db.findOne('otp_records', { id: otpId });
    if (!record) return { verified: false, reason: 'not_found' };
    if (record.status !== 'pending') return { verified: false, reason: 'already_used' };
    if (record.expiresAt < new Date()) return { verified: false, reason: 'expired' };

    const inputHash = createHash('sha256').update(userCode).digest('hex');
    if (inputHash !== record.codeHash) {
      record.attemptsRemaining--;
      if (record.attemptsRemaining <= 0) {
        await this.db.update('otp_records', { id: otpId }, { status: 'failed' });
        return { verified: false, reason: 'too_many_attempts' };
      }
      await this.db.update('otp_records', { id: otpId }, {
        attemptsRemaining: record.attemptsRemaining,
      });
      return { verified: false, reason: 'incorrect', attemptsRemaining: record.attemptsRemaining };
    }

    await this.db.update('otp_records', { id: otpId }, { status: 'verified' });
    return { verified: true };
  }
}
```

## Cost Optimization

```typescript
interface OtpCostOptimizer {
  async deliver(userId: string, target: string, type: 'sms' | 'email'): Promise<void> {
    // Prefer email over SMS (SMS costs $0.0079/message vs email ~$0.0001)
    if (type === 'sms' && userHasEmailMfaEnabled(userId)) {
      // Offer email as free alternative
      await this.offerAlternative(target);
    }

    // Batch SMS sending during off-peak hours for non-urgent OTPs
    if (this.isWithinOffPeakWindow() && !this.isUrgent(userId)) {
      await this.enqueueBatchSms(userId, target);
    } else {
      await this.sendImmediate(userId, target, type);
    }
  }
}
```

## Open-Source Tools

- **Twilio** (Commercial) — SMS/Voice delivery
- **Resend** (MIT) — Email delivery via API
- **nodemailer** (MIT) — SMTP email sending
- **bullmq** (MIT) — Queue for delivery retries

## Production Considerations

- Store OTP hashes (SHA-256) never plaintext codes
- Enforce strict rate limiting: max 5 OTP requests per user per 5 minutes, max 3 verification attempts per OTP
- Use short OTP expiry (5-10 minutes) and one-time use enforcement
- Implement delivery status callbacks for SMS to detect failed deliveries
- Mask contact info in logs and responses (e.g., +1***4567, a***@example.com)
- Include geographic rate limiting to prevent SMS toll fraud (Wangiri attacks)
- Set up separate sender pool for transactional vs promotional SMS
- Monitor delivery costs and set per-tenant budget caps
