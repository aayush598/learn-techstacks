# Concurrent Session Limits

## Overview

Concurrent session limits restrict how many simultaneous sessions a user can have. This prevents credential sharing, limits exposure from compromised devices, and helps comply with licensing constraints.

## Limit Configuration

```typescript
interface ConcurrentSessionConfig {
  maxSessionsPerUser: number;
  maxSessionsPerDeviceType: Record<string, number>; // { mobile: 1, desktop: 3 }
  enforcement: 'block_new' | 'terminate_oldest' | 'terminate_excess';
  exemptRoles: string[];
  notifyOnLimit: boolean;
}

const CONCURRENT_SESSION_CONFIG: ConcurrentSessionConfig = {
  maxSessionsPerUser: 5,
  maxSessionsPerDeviceType: { mobile: 2, desktop: 3, api: 10 },
  enforcement: 'terminate_oldest',
  exemptRoles: ['admin'],
  notifyOnLimit: true,
};
```

## Enforcement

```typescript
class ConcurrentSessionEnforcer {
  async enforce(userId: string, newDeviceType: string): Promise<void> {
    const user = await this.userService.getUser(userId);
    if (!user) return;

    const config = await this.getTenantConfig(user.tenantId);
    if (config.exemptRoles?.some(r => user.roles.includes(r))) return;

    let sessions = await this.sessionStore.getUserSessions(userId);

    // Filter by device type if configured
    if (config.maxSessionsPerDeviceType[newDeviceType]) {
      const deviceSessions = sessions.filter(s => s.metadata.deviceType === newDeviceType);
      const maxForDevice = config.maxSessionsPerDeviceType[newDeviceType];

      if (deviceSessions.length >= maxForDevice) {
        switch (config.enforcement) {
          case 'terminate_oldest':
            const oldest = deviceSessions.sort((a, b) => a.createdAt.getTime() - b.createdAt.getTime())[0];
            await this.sessionStore.delete(oldest.id);
            await this.notifyTerminated(oldest, userId);
            break;
          case 'block_new':
            throw new ConcurrentSessionError(`Maximum ${maxForDevice} ${newDeviceType} sessions allowed`);
        }
      }
    }

    // Global limit
    if (sessions.length >= config.maxSessionsPerUser) {
      switch (config.enforcement) {
        case 'terminate_oldest':
          sessions.sort((a, b) => a.createdAt.getTime() - b.createdAt.getTime());
          const toRemove = sessions.slice(0, sessions.length - config.maxSessionsPerUser + 1);
          for (const s of toRemove) {
            await this.sessionStore.delete(s.id);
            await this.notifyTerminated(s, userId);
          }
          break;
        case 'terminate_excess':
          const excess = sessions.slice(config.maxSessionsPerUser - 1);
          for (const s of excess) {
            await this.sessionStore.delete(s.id);
            await this.notifyTerminated(s, userId);
          }
          break;
        case 'block_new':
          throw new ConcurrentSessionError(`Maximum ${config.maxSessionsPerUser} sessions reached`);
      }
    }
  }

  private async notifyTerminated(session: Session, userId: string): Promise<void> {
    if (!config.notifyOnLimit) return;

    await this.notificationService.notify({
      type: 'session_terminated',
      userId,
      data: {
        reason: 'concurrent_limit',
        terminatedAt: session.lastActivity,
        deviceType: session.metadata.deviceType,
        ipAddress: session.ipAddress,
      },
    });
  }
}
```

## Dashboard

```
Active Sessions (3/5)
├── Current Session ● Active now
│   Chrome on MacOS · IP: 203.0.113.1
│
├── Mobile App ● Last active: 2 hours ago
│   VoiceAgent iOS · IP: 198.51.100.1
│   [Terminate]
│
└── API Key ● Last active: 5 minutes ago
    SDK Session · IP: 192.0.2.1
    [Terminate]
```

## Open-Source Tools

- **ioredis** (MIT) — Session counting with Redis sets

## Production Considerations

- Default limit: 5 sessions per user, configurable per tenant (1-20)
- API key sessions should count toward limit or have separate pool
- Always allow emergency admin override to terminate any session
- Notify user via email when session is terminated due to limit
- Show remaining session count in user settings
- Monitor concurrent session violations as security metric
- Support device-type-aware limits (mobile vs desktop vs API)
