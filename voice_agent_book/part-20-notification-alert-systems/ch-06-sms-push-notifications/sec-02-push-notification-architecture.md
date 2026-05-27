# Section 02: Push Notification Architecture

## Overview

Push notifications deliver messages to user devices via Web Push API (browsers) and platform push services (mobile). The system manages push subscriptions, generates VAPID keys for authentication, and handles message delivery with payload encryption.

## Implementation Approach

```typescript
interface PushSubscription {
  id: string;
  userId: string;
  endpoint: string;
  keys: {
    p256dh: string;
    auth: string;
  };
  deviceInfo: DeviceInfo;
  createdAt: string;
  expiresAt?: string;
}

interface PushPayload {
  title: string;
  body: string;
  icon?: string;
  badge?: string;
  data?: Record<string, unknown>;
  tag?: string;
  actions?: PushAction[];
  requireInteraction?: boolean;
  silent?: boolean;
  urgency?: 'low' | 'normal' | 'high';
}

class PushNotificationService {
  private vapidKeys: VAPIDKeys;

  async sendToUser(userId: string, payload: PushPayload): Promise<PushResult[]> {
    const subscriptions = await this.subscriptionStore.query({ userId, active: true });
    return Promise.all(subscriptions.map(sub => this.sendToSubscription(sub, payload)));
  }

  async sendToSubscription(subscription: PushSubscription, payload: PushPayload): Promise<PushResult> {
    try {
      const response = await webpush.sendNotification(
        {
          endpoint: subscription.endpoint,
          keys: {
            p256dh: subscription.keys.p256dh,
            auth: subscription.keys.auth,
          },
        },
        JSON.stringify(payload),
        {
          vapidDetails: {
            subject: 'mailto:notifications@example.com',
            publicKey: this.vapidKeys.public,
            privateKey: this.vapidKeys.private,
          },
          TTL: 86400, // 24 hours
          urgency: payload.urgency || 'normal',
        }
      );

      return { subscriptionId: subscription.id, status: 'sent', statusCode: response.statusCode };
    } catch (error) {
      if (error.statusCode === 410) {
        // Subscription expired or invalid
        await this.subscriptionStore.deactivate(subscription.id);
        return { subscriptionId: subscription.id, status: 'expired' };
      }
      return { subscriptionId: subscription.id, status: 'failed', error: error.message };
    }
  }

  async registerSubscription(userId: string, subscription: PushSubscriptionInput): Promise<PushSubscription> {
    const existing = await this.subscriptionStore.findOne({ endpoint: subscription.endpoint });
    if (existing) {
      await this.subscriptionStore.reactivate(existing.id);
      return existing;
    }

    const newSub: PushSubscription = {
      id: generateId(),
      userId,
      endpoint: subscription.endpoint,
      keys: subscription.keys,
      deviceInfo: subscription.deviceInfo,
      createdAt: new Date().toISOString(),
    };

    await this.subscriptionStore.save(newSub);
    return newSub;
  }

  async unsubscribe(endpoint: string): Promise<void> {
    await this.subscriptionStore.deactivateByEndpoint(endpoint);
  }

  static generateVAPIDKeys(): VAPIDKeys {
    const vapid = require('web-push').generateVAPIDKeys();
    return { public: vapid.publicKey, private: vapid.privateKey };
  }
}

// Service worker registration code (client-side)
navigator.serviceWorker.register('/sw.js');
navigator.serviceWorker.ready.then(registration => {
  registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: urlBase64ToUint8Array(publicKey),
  }).then(subscription => {
    fetch('/api/push/subscribe', {
      method: 'POST',
      body: JSON.stringify(subscription),
      headers: { 'Content-Type': 'application/json' },
    });
  });
});
```

## Integration Points

- **Service Worker**: Client-side push handling
- **Subscription API**: REST endpoints for CRUD subscriptions
- **VAPID Keys**: Generated once and shared across instances

## Production Considerations

- **Subscription Expiry**: Handle expired subscriptions gracefully
- **Payload Size**: Keep payload under 4KB (browser limit)
- **Permission**: Request push permission at appropriate time
