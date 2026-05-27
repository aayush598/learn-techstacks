# Backup Codes & Recovery

## Overview

Backup codes provide a fallback authentication method when primary MFA factors are unavailable (lost phone, broken device, no network). These are single-use, pre-generated codes distributed during MFA enrollment that allow users to regain account access without support intervention.

## Backup Code Generation

```typescript
interface BackupCode {
  id: string;
  codeHash: string;         // SHA-256 hash of the code
  codePrefix: string;       // First 4 chars for identification
  userId: string;
  tenantId: string;
  usedAt?: Date;
  expiresAt?: Date;
  batchId: string;          // Links to enrollment batch
}

class BackupCodeGenerator {
  generateBatch(userId: string, count: number = 10): { codes: string[]; records: BackupCode[] } {
    const batchId = `batch_${randomBytes(8).toString('hex')}`;
    const codes: string[] = [];
    const records: BackupCode[] = [];

    for (let i = 0; i < count; i++) {
      const code = this.generateSingleCode();
      const codeHash = createHash('sha256').update(code).digest('hex');

      codes.push(code);
      records.push({
        id: `bc_${randomBytes(8).toString('hex')}`,
        codeHash,
        codePrefix: code.slice(0, 4),
        userId,
        tenantId: 'default',
        batchId,
        expiresAt: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000), // 1 year
      });
    }

    return { codes, records };
  }

  private generateSingleCode(): string {
    const bytes = randomBytes(6);
    const code = bytes.toString('hex').toUpperCase();
    return `${code.slice(0, 4)}-${code.slice(4, 8)}-${code.slice(8, 12)}`;
  }
}
```

## Recovery Workflow

```
[User] → Login → MFA Required → MFA Device Unavailable
    ↓
"Use Recovery Code"
    ↓
[System] → Prompt for backup code
    ↓
[User] → Enter backup code (XXXX-XXXX-XXXX)
    ↓
[System] → Hash input, compare against stored hashes
    ├── Match found, unused → Mark code as used
    │   ├── Issue session (with MFA trusted flag)
    │   └── Prompt to set up new MFA device
    └── No match or already used → Error + retry
        └── After 3 failures → Account lockout
```

## Recovery Code Verification

```typescript
class BackupCodeVerifier {
  async verify(userId: string, code: string): Promise<VerificationResult> {
    const normalizedCode = code.toUpperCase().replace(/\s/g, '');
    const codeHash = createHash('sha256').update(normalizedCode).digest('hex');

    const storedCode = await this.db.findOne('backup_codes', {
      userId,
      codeHash,
      usedAt: null,
    });

    if (!storedCode) {
      // Check if it was already used (to prevent reuse guessing)
      const usedCode = await this.db.findOne('backup_codes', {
        userId,
        codeHash,
        usedAt: { $ne: null },
      });

      if (usedCode) {
        return { success: false, reason: 'already_used' };
      }
      return { success: false, reason: 'invalid_code' };
    }

    if (storedCode.expiresAt && storedCode.expiresAt < new Date()) {
      return { success: false, reason: 'expired' };
    }

    await this.db.update('backup_codes', { id: storedCode.id }, {
      usedAt: new Date(),
    });

    // Invalidate all sessions for this user to force new MFA setup
    await this.sessionService.revokeAllUserSessions(userId);

    return { success: true, remainingCodes: await this.countRemaining(userId) };
  }

  async countRemaining(userId: string): Promise<int> {
    return this.db.count('backup_codes', { userId, usedAt: null });
  }

  async hasRemainingCodes(userId: string): Promise<boolean> {
    const count = await this.countRemaining(userId);
    return count > 0;
  }
}
```

## Regenerate Backup Codes

```typescript
interface BackupCodeRegenerationResult {
  newCodes: string[];
  invalidatedCodes: number;
  previousBatchId: string;
}

class BackupCodeManager {
  async regenerate(userId: string): Promise<BackupCodeRegenerationResult> {
    // Get current batch info
    const currentBatch = await this.db.findOne('backup_codes', {
      userId,
      usedAt: null,
    });
    const previousBatchId = currentBatch?.batchId;

    // Invalidate all remaining unused codes
    await this.db.update('backup_codes', {
      userId,
      usedAt: null,
    }, {
      expiredAt: new Date(), // Mark as expired
    });

    // Generate new batch
    const { codes, records } = new BackupCodeGenerator().generateBatch(userId);

    await this.db.insertBatch('backup_codes', records);

    return {
      newCodes: codes,
      invalidatedCodes: records.length,
      previousBatchId,
    };
  }
}
```

## Secure Storage Requirements

Backup codes must be stored as hashes, never in plaintext:

```typescript
const BACKUP_CODES_TABLE = `
  CREATE TABLE backup_codes (
    id VARCHAR(64) PRIMARY KEY,
    code_hash VARCHAR(64) NOT NULL,
    code_prefix VARCHAR(4) NOT NULL,
    user_id VARCHAR(64) NOT NULL,
    tenant_id VARCHAR(64) NOT NULL,
    batch_id VARCHAR(64) NOT NULL,
    used_at TIMESTAMP NULL,
    expires_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_batch_id (batch_id),
    INDEX idx_code_hash (code_hash)
  )
`;
```

## Open-Source Tools

- **otplib** — Backup code generation alongside TOTP
- **speakeasy** — Recovery code generation utilities

## Production Considerations

- Display codes only once: require user to confirm they've saved them before dismissing the dialog
- Recommend password managers for backup code storage (not plaintext files)
- Allow printing as PDF for offline storage
- Send SMS notification when backup codes are used (potential account compromise indicator)
- Regenerate codes whenever new MFA devices are enrolled
- Limit to 3 batch regenerations per year to prevent abuse
- Support recovery via support ticket (with identity verification) as last resort
