# Section 03: Email Preferences & Subscription

## Overview

Email preferences allow users to control which emails they receive, how often, and through which addresses. The preference center provides a unified interface for managing subscriptions across email categories (notifications, digests, marketing, billing). Unsubscribe management complies with CAN-SPAM and GDPR requirements.

## Implementation Approach

```typescript
interface EmailPreferences {
  userId: string;
  email: string;
  subscribed: boolean;
  categories: EmailCategoryPreferences;
  frequency: EmailFrequency;
  digestSchedule?: DigestSchedule;
  unsubscribedAt?: string;
  unsubscribeReason?: string;
}

interface EmailCategoryPreferences {
  notifications: { subscribed: boolean; frequency: 'immediate' | 'digest' | 'off' };
  billing: { subscribed: boolean; frequency: 'immediate' | 'off' };
  product: { subscribed: boolean; frequency: 'immediate' | 'weekly' | 'off' };
  marketing: { subscribed: boolean; frequency: 'weekly' | 'monthly' | 'off' };
  security: { subscribed: boolean; frequency: 'immediate' | 'off' };
}

class EmailPreferenceManager {
  async getPreferences(userId: string): Promise<EmailPreferences> {
    let prefs = await this.storage.findOne({ userId });
    if (!prefs) {
      prefs = this.getDefaults(userId);
      await this.storage.save(prefs);
    }
    return prefs;
  }

  async updatePreferences(userId: string, updates: Partial<EmailPreferences>): Promise<EmailPreferences> {
    const prefs = await this.getPreferences(userId);
    Object.assign(prefs, updates);
    await this.storage.update(prefs);
    await this.auditLogger.log({ event: 'email_prefs_updated', userId, changes: updates });
    return prefs;
  }

  async unsubscribe(userId: string, reason?: string): Promise<void> {
    const prefs = await this.getPreferences(userId);
    prefs.subscribed = false;
    prefs.unsubscribedAt = new Date().toISOString();
    prefs.unsubscribeReason = reason;
    await this.storage.update(prefs);
  }

  async unsubscribeFromCategory(userId: string, category: string): Promise<void> {
    const prefs = await this.getPreferences(userId);
    if (prefs.categories[category]) {
      prefs.categories[category].subscribed = false;
      await this.storage.update(prefs);
    }
  }

  async shouldSend(emailType: string, userId: string): Promise<boolean> {
    const prefs = await this.getPreferences(userId);
    if (!prefs.subscribed) return false;
    const category = prefs.categories[emailType];
    if (!category) return true; // unknown category defaults to allowed
    return category.subscribed && category.frequency !== 'off';
  }

  async processUnsubscribeLink(token: string): Promise<void> {
    const data = this.verifyUnsubscribeToken(token);
    await this.unsubscribe(data.userId, 'link_click');
  }

  generateUnsubscribeLink(userId: string, email: string): string {
    const token = this.signToken({ userId, email, action: 'unsubscribe' });
    return `${this.baseUrl}/email/unsubscribe?token=${token}`;
  }

  private getDefaults(userId: string): EmailPreferences {
    return {
      userId,
      email: '',
      subscribed: true,
      categories: {
        notifications: { subscribed: true, frequency: 'immediate' },
        billing: { subscribed: true, frequency: 'immediate' },
        product: { subscribed: true, frequency: 'weekly' },
        marketing: { subscribed: false, frequency: 'off' },
        security: { subscribed: true, frequency: 'immediate' },
      },
      frequency: 'immediate',
    };
  }
}
```

## Integration Points

- **Preference API**: REST endpoints for preference CRUD
- **Email Footer**: Unsubscribe link in every email
- **Preference Center UI**: User-facing settings page

## Production Considerations

- **Unsubscribe Compliance**: Process unsubscribe within 10 business days
- **Preference Caching**: Cache preferences to avoid DB lookup per email
- **Audit Trail**: Log all preference changes
