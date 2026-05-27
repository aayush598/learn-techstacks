# TOTP Implementation

## Overview

Time-based One-Time Passwords (TOTP) provide a software-based possession factor using shared secrets and time synchronization. Users generate codes via authenticator apps (Google Authenticator, Authy, 1Password) without requiring network connectivity.

## TOTP Algorithm

```
Secret (base32 encoded)
    │
    ├── HMAC-SHA1(secret, time_counter)
    │
    ▼
Truncate to 31 bits
    │
    ▼
Generate 6-8 digit code
    │
    ▼
Compare with user-provided code (constant-time)
```

## Secret Generation & Storage

```typescript
import { authenticator } from 'otplib';
import { createHash, randomBytes } from 'crypto';

interface TotpConfig {
  issuer: string;           // Company name displayed in authenticator app
  algorithm: 'sha1' | 'sha256' | 'sha512';
  digits: number;           // 6 or 8
  step: number;             // Time step in seconds (default 30)
  window: number;           // Verification window (default 1 = +/- 30s)
}

interface TotpSecret {
  base32: string;           // Shared secret in base32
  hex: string;              // Hex-encoded secret for verification
  ascii: string;            // ASCII representation
  otpauthUrl: string;       // Key URI for QR code generation
}

function generateTotpSecret(userId: string, tenantId: string): TotpSecret {
  const secret = authenticator.generateSecret(32); // 32 bytes = 256 bits

  const otpauthUrl = authenticator.keyuri(
    `${tenantId}:${userId}`,
    'VoiceAgent',
    secret
  );

  return {
    base32: secret,
    hex: Buffer.from(secret, 'base32').toString('hex'),
    ascii: Buffer.from(secret, 'base32').toString('ascii'),
    otpauthUrl,
  };
}
```

## QR Code Rendering

```typescript
import QRCode from 'qrcode';

async function renderTotpQrCode(otpauthUrl: string): Promise<string> {
  // Generate QR as data URL for in-app display
  const qrDataUrl = await QRCode.toDataURL(otpauthUrl, {
    width: 300,
    margin: 2,
    color: { dark: '#000', light: '#FFF' },
  });
  return qrDataUrl;
}
```

## Verification Logic

```typescript
class TotpVerifier {
  constructor(private config: TotpConfig) {
    authenticator.options = {
      algorithm: this.config.algorithm,
      digits: this.config.digits,
      step: this.config.step,
      window: this.config.window,
    };
  }

  verify(token: string, secret: string): boolean {
    try {
      return authenticator.check(token, secret);
    } catch {
      return false;
    }
  }

  verifyWithWindow(token: string, secret: string, windowSize: number): boolean {
    try {
      return authenticator.check(token, secret, windowSize);
    } catch {
      return false;
    }
  }

  generate(secret: string): string {
    return authenticator.generate(secret);
  }

  getRemainingSeconds(): number {
    return authenticator.timeRemaining();
  }

  getTimeUsed(): number {
    return authenticator.timeUsed();
  }
}
```

## Storing TOTP Secrets Securely

```typescript
interface StoredTotpFactor {
  id: string;
  userId: string;
  tenantId: string;
  encryptedSecret: string;   // AES-256-GCM encrypted
  encryptionIv: string;      // Initialization vector
  encryptionTag: string;     // Auth tag for GCM
  label: string;             // User-friendly device name
  createdAt: Date;
  lastVerifiedAt?: Date;
  enabled: boolean;
}

class TotpFactorStore {
  private encryptionKey: Buffer;

  constructor(key: string) {
    this.encryptionKey = Buffer.from(key, 'hex');
  }

  async storeFactor(userId: string, tenantId: string, secret: TotpSecret): Promise<StoredTotpFactor> {
    const iv = randomBytes(16);
    const cipher = crypto.createCipheriv('aes-256-gcm', this.encryptionKey, iv);
    let encrypted = cipher.update(secret.hex, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    const tag = cipher.getAuthTag();

    const factor: StoredTotpFactor = {
      id: `totp_${randomBytes(8).toString('hex')}`,
      userId,
      tenantId,
      encryptedSecret: encrypted,
      encryptionIv: iv.toString('hex'),
      encryptionTag: tag.toString('hex'),
      label: 'Default Authenticator App',
      createdAt: new Date(),
      enabled: true,
    };

    await this.db.insert('mfa_totp_factors', factor);
    return factor;
  }

  async getDecryptedSecret(factorId: string): Promise<string> {
    const factor = await this.db.findOne('mfa_totp_factors', { id: factorId });
    if (!factor) throw new Error('TOTP factor not found');

    const decipher = crypto.createDecipheriv(
      'aes-256-gcm',
      this.encryptionKey,
      Buffer.from(factor.encryptionIv, 'hex')
    );
    decipher.setAuthTag(Buffer.from(factor.encryptionTag, 'hex'));
    let decrypted = decipher.update(factor.encryptedSecret, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    return decrypted;
  }
}
```

## Backup Codes on TOTP Enrollment

When a user first enables TOTP, generate a set of one-time backup codes:

```typescript
function generateBackupCodes(count: number = 10): string[] {
  const codes: string[] = [];
  for (let i = 0; i < count; i++) {
    const code = randomBytes(6).toString('hex').toUpperCase();
    const formatted = `${code.slice(0, 4)}-${code.slice(4, 8)}-${code.slice(8, 12)}`;
    codes.push(formatted);
  }
  return codes;
}
```

## Open-Source Tools

- **otplib** (MIT) — Complete TOTP/HOTP implementation
- **qrcode** (MIT) — QR code generation for authenticator app setup
- **speakeasy** (MIT) — One-time password utilities

## Production Considerations

- Store shared secrets encrypted at rest using AES-256-GCM with a key management service
- Allow users to label multiple authenticator devices for convenience
- Display TOTP enrollment as a QR code that can be scanned or a plain text secret for manual entry
- Set a maximum of 5 TOTP factors per user to limit attack surface
- Detect clock drift by allowing a configurable verification window (default +/- 1 step)
- Warn users when time sync is off by checking current token vs expected token range
- Never log TOTP secrets or codes even in error scenarios
