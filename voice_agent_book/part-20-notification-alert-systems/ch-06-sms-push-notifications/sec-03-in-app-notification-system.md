# Section 03: In-App Notification System

## Overview

The in-app notification system delivers notifications within the application UI. Notifications appear in a notification center panel with real-time updates via WebSocket. Features include read/unread state, notification grouping, action buttons, and a badge counter.

## Implementation Approach

```typescript
interface InAppNotification {
  id: string;
  userId: string;
  type: string;
  title: string;
  body: string;
  data: Record<string, unknown>;
  read: boolean;
  readAt?: string;
  archived: boolean;
  createdAt: string;
  expiresAt?: string;
  actions: NotificationAction[];
  group?: string;
  priority: 'low' | 'normal' | 'high';
}

class InAppNotificationService {
  async create(notification: InAppNotificationInput): Promise<InAppNotification> {
    const notif: InAppNotification = {
      id: generateId(),
      ...notification,
      read: false,
      archived: false,
      createdAt: new Date().toISOString(),
    };

    await this.storage.save(notif);
    await this.realtimeService.push(notification.userId, {
      type: 'notification',
      action: 'created',
      notification: notif,
    });

    return notif;
  }

  async markRead(notificationId: string, userId: string): Promise<void> {
    await this.storage.update(notificationId, { read: true, readAt: new Date().toISOString() });
    await this.updateBadge(userId);
  }

  async markAllRead(userId: string): Promise<void> {
    await this.storage.updateMany({ userId, read: false }, { read: true, readAt: new Date().toISOString() });
    await this.updateBadge(userId);
  }

  async archive(notificationId: string, userId: string): Promise<void> {
    await this.storage.update(notificationId, { archived: true });
  }

  async list(userId: string, options?: NotificationListOptions): Promise<PaginatedResult<InAppNotification>> {
    const query: Query = { userId, archived: false };
    if (options?.unreadOnly) query.read = false;
    if (options?.types) query.type = { $in: options.types };

    return this.storage.paginate(query, {
      sort: { createdAt: -1 },
      limit: options?.limit || 50,
      offset: options?.offset || 0,
    });
  }

  async getUnreadCount(userId: string): Promise<number> {
    return this.storage.count({ userId, read: false, archived: false });
  }

  private async updateBadge(userId: string): Promise<void> {
    const count = await this.getUnreadCount(userId);
    await this.realtimeService.push(userId, {
      type: 'badge',
      count,
    });
  }

  // Cleanup expired notifications
  async cleanupExpired(): Promise<void> {
    await this.storage.deleteMany({
      expiresAt: { $lt: new Date().toISOString() },
      read: true,
    });
  }
}

// React hook for consuming notifications
function useNotifications() {
  const [notifications, setNotifications] = useState<InAppNotification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    const ws = new WebSocket('/ws/notifications');
    ws.onmessage = event => {
      const data = JSON.parse(event.data);
      if (data.type === 'notification' && data.action === 'created') {
        setNotifications(prev => [data.notification, ...prev]);
        setUnreadCount(c => c + 1);
      } else if (data.type === 'badge') {
        setUnreadCount(data.count);
      }
    };
    return () => ws.close();
  }, []);
}
```

## Integration Points

- **WebSocket Server**: Real-time push to connected clients
- **Notification API**: REST endpoints for notification CRUD
- **UI Components**: Notification center, badge, toast

## Production Considerations

- **Storage Limits**: Limit notifications per user (e.g., 500)
- **WebSocket Scaling**: Use Redis adapter for multi-instance WebSocket
- **Offline Support**: Store notifications server-side for offline users
