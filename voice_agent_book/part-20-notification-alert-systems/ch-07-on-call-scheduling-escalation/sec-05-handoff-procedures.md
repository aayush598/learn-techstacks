# Section 05: Handoff Procedures

## Overview

Handoff procedures ensure smooth transitions between on-call shifts. The handoff workflow includes context transfer (active alerts, ongoing incidents, notes), notification to incoming and outgoing responders, and escalation of unacknowledged alerts if needed.

## Implementation Approach

```typescript
interface ShiftHandoff {
  id: string;
  scheduleId: string;
  fromUserId: string;
  toUserId: string;
  timestamp: string;
  context: ShiftContext;
  status: 'pending' | 'completed' | 'failed';
  notes?: string;
}

interface ShiftContext {
  activeAlerts: AlertSummary[];
  ongoingIncidents: IncidentSummary[];
  pendingActions: PendingAction[];
  knownIssues: string[];
  communicationChannels: string[];
}

class HandoffManager {
  async initiateHandoff(scheduleId: string): Promise<ShiftHandoff> {
    const schedule = await this.scheduleService.get(scheduleId);
    const fromUser = await this.onCallService.getCurrentOnCall(scheduleId);
    const toUser = await this.onCallService.getNextOnCall(scheduleId);

    const context = await this.collectContext(fromUser.userId);
    const handoff: ShiftHandoff = {
      id: generateId(),
      scheduleId,
      fromUserId: fromUser.userId,
      toUserId: toUser.userId,
      timestamp: new Date().toISOString(),
      context,
      status: 'pending',
    };

    await this.storage.save(handoff);
    await this.notifyHandoff(handoff);
    return handoff;
  }

  private async collectContext(userId: string): Promise<ShiftContext> {
    const [activeAlerts, ongoingIncidents, pendingActions] = await Promise.all([
      this.alertService.getActiveAlerts(userId),
      this.incidentService.getOngoingIncidents(userId),
      this.getPendingActions(userId),
    ]);

    return {
      activeAlerts: activeAlerts.map(a => ({
        id: a.id,
        title: a.title,
        severity: a.severity,
        status: a.status,
        age: Date.now() - new Date(a.createdAt).getTime(),
      })),
      ongoingIncidents: ongoingIncidents.map(i => ({
        id: i.id,
        title: i.title,
        status: i.status,
        lastActivity: i.updatedAt,
      })),
      pendingActions: pendingActions,
      knownIssues: [],
      communicationChannels: ['slack', 'phone'],
    };
  }

  private async notifyHandoff(handoff: ShiftHandoff): Promise<void> {
    // Notify outgoing
    await this.notificationService.send({
      userId: handoff.fromUserId,
      type: 'shift_handoff_outgoing',
      message: 'Your on-call shift is ending. Handoff context is available.',
      context: handoff.context,
    });

    // Notify incoming
    await this.notificationService.send({
      userId: handoff.toUserId,
      type: 'shift_handoff_incoming',
      message: 'You are now on-call. Review the handoff context for active items.',
      context: handoff.context,
    });

    // Post handoff summary to Slack
    await this.slackService.sendMessage({
      channel: scheduleId, // channel mapped to this schedule
      text: `🔄 *Shift Handoff*\nFrom: <@${handoff.fromUserId}>\nTo: <@${handoff.toUserId}>`,
      blocks: [
        {
          type: 'section',
          text: { type: 'mrkdwn', text: `*Active Alerts:* ${handoff.context.activeAlerts.length}\n*Ongoing Incidents:* ${handoff.context.ongoingIncidents.length}` },
        },
      ],
    });
  }

  async completeHandoff(handoffId: string, notes?: string): Promise<void> {
    const handoff = await this.storage.get(handoffId);
    handoff.status = 'completed';
    handoff.notes = notes;
    await this.storage.update(handoff);

    // Escalate any unacknowledged alerts from outgoing shift
    const unacknowledged = handoff.context.activeAlerts.filter(a => a.status === 'firing');
    for (const alert of unacknowledged) {
      await this.alertService.reassign(alert.id, handoff.toUserId);
    }
  }

  async getHandoffHistory(scheduleId: string, limit: number = 10): Promise<ShiftHandoff[]> {
    return this.storage.query(
      { scheduleId },
      { sort: { timestamp: -1 }, limit }
    );
  }

  private async getPendingActions(userId: string): Promise<PendingAction[]> {
    return this.actionStore.query({ assignee: userId, status: 'pending' });
  }
}
```

## Integration Points

- **On-Call Schedule**: Determines shift transitions
- **Alert Service**: Reassigns alerts on handoff
- **Slack Integration**: Posts handoff summaries

## Production Considerations

- **Context Freshness**: Capture context just before handoff
- **Failed Handoff**: Escalate if handoff fails
- **Handoff Reminders**: Remind outgoing to complete handoff notes
