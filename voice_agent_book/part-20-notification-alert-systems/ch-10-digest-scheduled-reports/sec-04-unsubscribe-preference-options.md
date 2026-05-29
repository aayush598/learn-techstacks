# Section 04: Unsubscribe & Preference Options

## Overview

Users can unsubscribe from digests or adjust preferences through one-click links in digest emails, preference pages, and API endpoints. Granular controls allow pausing specific digest types, changing frequency, and adjusting content modules without fully unsubscribing.

## Architecture

```
Unsubscribe Flow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Digest Email] → [Unsubscribe Link] → [Preference Page] → [Updated]
      │                  │                      │               │
  One-click link      Tokenized URL          Full preference  Preferences
  at bottom of        Contains userId         editor with     saved, next
  digest              + signature             granular        digest affected
                      + action                controls

Unsubscribe Link Format:
  https://app.voiceagent.com/preferences/digests
    ?action=unsubscribe
    &user=abc123
    &token=hmac_signature

One-Click Actions:
  ┌──────────────────────────────────────────────────────┐
  │ Unsubscribe from all digests                          │
  │                                                       │
  │ [Unsubscribe from all]                                │
  │                                                       │
  │ Or adjust preferences:                                │
  │                                                       │
  │ ○ Change frequency to: [Weekly ▼]                     │
  │ ○ Pause for: [7 days ▼]                               │
  │ ○ Switch to: Summary only                             │
  │ ○ Manage all preferences →                            │
  │                                                       │
  │ © Voice Agent | [Preferences] [Privacy Policy]        │
  └──────────────────────────────────────────────────────┘

Preference Granularity:
  Full Unsubscribe → Pause → Frequency Change → Content Modules → Channel
```

## Design Decisions

- **One-Click Unsubscribe**: No login required for unsubscribe
- **Token-Based Auth**: HMAC-signed tokens prevent unauthorized changes
- **Granular Pause**: Support time-bound pauses (24h, 7d, 30d)
- **Re-subscribe Option**: Easy re-enable through preferences or link in pause confirmation

## Implementation Approach

```typescript
interface UnsubscribeToken {
  userId: string;
  action: 'unsubscribe' | 'pause' | 'frequency_change';
  expiresAt: Date;
  signature: string;
  metadata?: {
    pauseDuration?: number; // hours
    newFrequency?: 'hourly' | 'daily' | 'weekly';
  };
}

class UnsubscribeService {
  private secret: string;

  generateToken(
    userId: string,
    action: UnsubscribeToken['action'],
    metadata?: UnsubscribeToken['metadata'],
  ): string {
    const payload = {
      userId,
      action,
      expiresAt: Date.now() + 7 * 24 * 3600000, // 7 days
      metadata,
    };

    const signature = crypto
      .createHmac('sha256', this.secret)
      .update(JSON.stringify(payload))
      .digest('hex');

    const token = Buffer.from(JSON.stringify({ ...payload, signature })).toString('base64url');
    return token;
  }

  verifyToken(token: string): UnsubscribeToken {
    try {
      const decoded = JSON.parse(Buffer.from(token, 'base64url').toString());
      const { signature, ...payload } = decoded;

      const expectedSig = crypto
        .createHmac('sha256', this.secret)
        .update(JSON.stringify(payload))
        .digest('hex');

      if (signature !== expectedSig) {
        throw new Error('Invalid token signature');
      }

      if (Date.now() > payload.expiresAt) {
        throw new Error('Token expired');
      }

      return { ...payload, signature };
    } catch (error) {
      throw new Error(`Invalid unsubscribe token: ${error.message}`);
    }
  }

  async handleOneClickAction(token: string): Promise<{ message: string; success: boolean }> {
    const decoded = this.verifyToken(token);

    switch (decoded.action) {
      case 'unsubscribe':
        await this.unsubscribeAll(decoded.userId);
        return { message: 'Unsubscribed from all digests', success: true };

      case 'pause':
        const duration = decoded.metadata?.pauseDuration || 168; // default 7 days
        await this.pauseDigests(decoded.userId, duration);
        return {
          message: `Digests paused for ${duration} hours. You can resume anytime.`,
          success: true,
        };

      case 'frequency_change':
        const frequency = decoded.metadata?.newFrequency || 'weekly';
        await this.changeFrequency(decoded.userId, frequency);
        return {
          message: `Digest frequency changed to ${frequency}`,
          success: true,
        };

      default:
        return { message: 'Unknown action', success: false };
    }
  }

  private async unsubscribeAll(userId: string): Promise<void> {
    await this.scheduler.pauseSchedule(userId);
    await this.preferences.update(userId, {
      digestEnabled: false,
      modules: [],
    });
    await this.trackUnsubscribe(userId, 'all');
  }

  private async pauseDigests(userId: string, durationHours: number): Promise<void> {
    const pauseUntil = new Date(Date.now() + durationHours * 3600000);

    await this.preferences.update(userId, {
      digestPaused: true,
      digestPauseUntil: pauseUntil,
    });

    await this.scheduler.pauseSchedule(userId);

    // Schedule automatic resume
    await this.jobQueue.add(
      'resume-digest',
      { userId },
      { delay: durationHours * 3600000, jobId: `resume-digest-${userId}` },
    );
  }

  async resumeDigests(userId: string): Promise<void> {
    await this.preferences.update(userId, {
      digestPaused: false,
      digestPauseUntil: null,
    });
    await this.scheduler.resumeSchedule(userId);
  }

  private async changeFrequency(
    userId: string,
    newFrequency: 'hourly' | 'daily' | 'weekly',
  ): Promise<void> {
    await this.scheduler.changeFrequency(userId, newFrequency);
  }

  async getUnsubscribeLink(
    userId: string,
    action: UnsubscribeToken['action'],
    metadata?: UnsubscribeToken['metadata'],
  ): Promise<string> {
    const token = this.generateToken(userId, action, metadata);
    return `https://app.voiceagent.com/preferences/digests/unsubscribe?token=${token}`;
  }

  private async trackUnsubscribe(userId: string, type: string): Promise<void> {
    await this.db.insert('digest_unsubscribe_events', {
      userId, type, timestamp: new Date(),
    });
  }
}

// Preference management service
class DigestPreferenceService {
  async getPreferences(userId: string): Promise<DigestPreferences> {
    const prefs = await this.store.findOne('digest_preferences', { userId });
    return prefs || this.getDefaults(userId);
  }

  async updatePreferences(userId: string, updates: Partial<DigestPreferences>): Promise<void> {
    await this.store.upsert('digest_preferences', { userId }, updates);
  }

  private getDefaults(userId: string): DigestPreferences {
    return {
      userId,
      tenantId: '',
      frequency: 'daily',
      preferredTime: '09:00',
      timezone: 'UTC',
      modules: [
        { moduleId: 'critical_alerts', enabled: true, order: 1, mode: 'always' },
        { moduleId: 'warnings', enabled: true, order: 2, mode: 'smart' },
        { moduleId: 'stats', enabled: true, order: 3, mode: 'smart' },
      ],
      channelPreferences: [
        { channel: 'email', enabled: true, digestFormat: 'full' },
        { channel: 'in_app', enabled: true, digestFormat: 'summary' },
      ],
      smartSelection: true,
      maxItemsPerModule: 20,
    };
  }
}
```

## Integration Points

- **Email Service**: Unsubscribe links generated for each digest
- **Preference API**: Full preference CRUD for dashboard
- **Analytics**: Track unsubscribe reasons for product improvement

## Production Considerations

- **Unsubscribe Rate Monitoring**: Alert on sudden increase in unsubscribes
- **Token Expiry**: 7-day token expiration for security
- **GDPR Compliance**: Unsubscribe = stop all digests + delete preference data
- **Resume Reminders**: Email reminder 24 hours before pause expires

## Open-Source Tools

- **Node.js crypto**: HMAC token generation and verification
- **BullMQ**: Delayed job for automatic digest resume
