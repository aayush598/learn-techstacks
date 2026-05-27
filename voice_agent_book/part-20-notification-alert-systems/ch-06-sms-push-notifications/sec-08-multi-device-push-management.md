# Section 08: Multi-Device Push Management

## Overview

Multi-device push management handles push notification delivery across multiple devices per user. Users may have a phone, tablet, laptop, and desktop all registered for push. The system manages device registration, cross-device synchronization, push quota limits, and device token refresh.

## Implementation Approach

```typescript
interface DeviceRegistration {
  id: string;
  userId: string;
  deviceType: 'phone' | 'tablet' | 'desktop' | 'laptop';
  platform: 'ios' | 'android' | 'web';
  pushToken: string;
  tokenExpiresAt?: string;
  isActive: boolean;
  lastSeen: string;
  createdAt: string;
}

class MultiDeviceManager {
  async registerDevice(userId: string, registration: DeviceRegistrationInput): Promise<DeviceRegistration> {
    // Invalidate old token if same device
    await this.deactivateToken(registration.pushToken);

    const device: DeviceRegistration = {
      id: generateId(),
      userId,
      ...registration,
      isActive: true,
      lastSeen: new Date().toISOString(),
      createdAt: new Date().toISOString(),
    };

    await this.storage.save(device);
    return device;
  }

  async sendToAllDevices(userId: string, payload: PushPayload): Promise<PushResult[]> {
    const devices = await this.storage.query({ userId, isActive: true });
    const results = await Promise.all(
      devices.map(device => this.sendToDevice(device, payload))
    );

    // Handle token refresh
    for (let i = 0; i < results.length; i++) {
      if (results[i].status === 'expired_token') {
        await this.deactivateDevice(devices[i].id);
      }
    }

    return results;
  }

  async sendToDevice(device: DeviceRegistration, payload: PushPayload): Promise<PushResult> {
    try {
      // Platform-specific push
      switch (device.platform) {
        case 'ios':
          return this.sendAPNS(device.pushToken, payload);
        case 'android':
          return this.sendFCM(device.pushToken, payload);
        case 'web':
          return this.sendWebPush(device.pushToken, payload);
      }
    } catch (error) {
      if (this.isTokenExpiredError(error as Error)) {
        return { deviceId: device.id, status: 'expired_token' };
      }
      return { deviceId: device.id, status: 'failed', error: (error as Error).message };
    }
  }

  async syncDeviceState(userId: string, state: DeviceSyncState): Promise<void> {
    const devices = await this.storage.query({ userId, isActive: true });

    for (const device of devices) {
      // Mark notifications as read on all devices
      if (state.readNotificationIds?.length) {
        await this.markReadOnDevice(device.id, state.readNotificationIds);
      }

      // Dismiss notifications on all devices
      if (state.dismissedNotificationIds?.length) {
        await this.dismissOnDevice(device.id, state.dismissedNotificationIds);
      }
    }

    // Cross-device sync via WebSocket
    await this.realtimeService.push(userId, {
      type: 'sync',
      state,
    });
  }

  private async deactivateToken(token: string): Promise<void> {
    await this.storage.updateMany(
      { pushToken: token, isActive: true },
      { isActive: false }
    );
  }

  private isTokenExpiredError(error: Error): boolean {
    const messages = ['Invalid token', 'BadDeviceToken', 'Unregistered', 'NotRegistered'];
    return messages.some(m => error.message.includes(m));
  }

  async cleanupExpiredTokens(): Promise<number> {
    const expired = await this.storage.query({
      tokenExpiresAt: { $lt: new Date().toISOString() },
      isActive: true,
    });

    for (const device of expired) {
      device.isActive = false;
      await this.storage.update(device);
    }

    return expired.length;
  }

  async getDeviceStats(userId: string): Promise<DeviceStats> {
    const devices = await this.storage.query({ userId, isActive: true });
    return {
      total: devices.length,
      byPlatform: {
        ios: devices.filter(d => d.platform === 'ios').length,
        android: devices.filter(d => d.platform === 'android').length,
        web: devices.filter(d => d.platform === 'web').length,
      },
      lastActive: Math.max(...devices.map(d => new Date(d.lastSeen).getTime())),
    };
  }
}
```

## Integration Points

- **APNS/FCM**: Apple and Google push notification services
- **Web Push**: Browser push via Web Push API
- **Real-Time Sync**: WebSocket for cross-device state sync

## Production Considerations

- **Token Refresh**: Apple/Google tokens expire; handle refresh flow
- **Device Limit**: Limit devices per user (e.g., 10)
- **Push Quotas**: Respect APNS/FCM rate limits per device
