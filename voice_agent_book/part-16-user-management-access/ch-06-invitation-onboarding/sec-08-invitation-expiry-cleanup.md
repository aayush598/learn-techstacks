# Invitation Expiry & Cleanup

## Overview

Invitation tokens must expire after a configurable period. Cleanup processes handle expired tokens, re-invitation flows, stale invitation reporting, and automatic revocation when user roles change.

## Expiry & Cleanup Service

```typescript
class InvitationCleanupService {
  async cleanupExpiredTokens(): Promise<CleanupResult> {
    const expired = await this.db.find('invitation_tokens', {
      expiresAt: { $lt: new Date() },
      usedCount: 0,
      revokedAt: null,
    });

    let revoked = 0;
    for (const token of expired) {
      if (token.payload.maxUses > 1 && token.usedCount > 0) {
        // Partially used tokens - keep but mark as expired
        continue;
      }
      await this.db.update('invitation_tokens', { id: token.id }, {
        revokedAt: new Date(),
        revokeReason: 'expired',
      });
      revoked++;
    }

    return { totalProcessed: expired.length, revoked, skipped: expired.length - revoked };
  }

  async revokeOnRoleChange(userId: string, oldRoleId: string): Promise<void> {
    // Revoke pending invitations for this user with old role
    await this.db.update('invitation_tokens', {
      'payload.roleId': oldRoleId,
      usedCount: 0,
      revokedAt: null,
    }, {
      revokedAt: new Date(),
      revokeReason: 'role_changed',
    });
  }

  async reInvite(inviteId: string, invitedBy: string): Promise<string> {
    const original = await this.db.findOne('invitation_tokens', { id: inviteId });
    if (!original) throw new Error('Original invitation not found');

    // Revoke original
    await this.db.update('invitation_tokens', { id: inviteId }, {
      revokedAt: new Date(),
      revokeReason: 'reinvited',
    });

    // Create new invitation with updated expiry
    return this.invitationService.generateToken({
      ...original.payload,
      expiresAt: new Date(Date.now() + 7 * 86400000),
      maxUses: 1,
    });
  }
}
```

## Stale Invitation Reports

```
Invitations Report
├── Active (12): 10 unopened, 2 opened (pending registration)
├── Expired (5): Awaiting cleanup or re-invite
├── Revoked (3): Manually cancelled
└── Accepted (145): Successfully registered
```

## Open-Source Tools

- **node-cron** (MIT) — Scheduler for cleanup jobs
- **BullMQ** (MIT) — Queue for re-invitation flows

## Production Considerations

- Run cleanup daily at midnight
- Send admin weekly report of stale invitations (>30 days)
- Re-invitation resets all use counters
- Max 3 re-invitations per original invite
- Notify admin when invite link is clicked after expiry
- Allow bulk re-invite from admin panel
