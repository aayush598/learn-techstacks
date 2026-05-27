# Section 06: Status Update Synchronization

## Overview

Status update synchronization ensures that the voice platform and helpdesk system maintain consistent view of ticket states. When a ticket status changes in the helpdesk (e.g., opened → pending customer response → resolved), the platform can trigger appropriate actions (e.g., schedule a follow-up call for pending tickets). Conversely, when a voice interaction resolves a ticket, the platform updates the helpdesk system with the resolution details.

The synchronization engine monitors ticket status changes through webhooks (real-time) and polling (fallback). Status changes are evaluated against configurable rules: "When a ticket moves to Pending status with priority High, schedule a follow-up call within 2 hours." The rules engine supports conditional logic (AND/OR conditions on ticket fields), action selection (call, SMS, email, no action), and notification routing (specific agent, queue, or skill group). The engine also handles idempotent status updates — no duplicate actions for the same status change.

## Architecture

```
                    Status Update Synchronization

   Helpdesk Webhook → Status Change Event → Rules Engine → Action Trigger
                                                               |
                                                               v
   +------------------+    +------------------+    +------------------+
   | Event Ingestion  | -> | Rules Engine     | -> | Action Scheduler |
   | • Webhook        |    | • Condition eval  |    | • Call queue     |
   | • Polling        |    | • Action mapping  |    | • SMS queue      |
   | • API callback   |    | • Prioritization  |    | • Notification   |
   +------------------+    +------------------+    +------------------+
                                                               |
                                                               v
   +------------------+    +------------------+    +------------------+
   | Ticket Update    | <- | Sync Engine      | <- | Voice Platform   |
   | • Status change  |    | • Idempotency    |    | • Call result    |
   | • Work note add  |    | • Conflict detect|    | • Agent input    |
   | • Assignment     |    | • Audit logging  |    | • AI summary     |
   +------------------+    +------------------+    +------------------+
```

## Design Decisions

- **Webhook-first with polling fallback for status change detection:** Webhooks provide real-time status change notifications with minimal latency. However, webhooks can be missed (platform downtime, network issues). A polling fallback (every 5-15 minutes) reconciles any missed updates. This dual approach ensures no status changes are missed while maintaining real-time responsiveness. Trade-off: periodic polling adds unnecessary API calls when webhooks are working reliably.

- **Deduplication window with idempotency keys:** Status changes are deduplicated within a 5-minute window using a composite key of ticket ID + target status + source. This prevents multiple actions from the same event (duplicate webhooks, webhook + polling overlap). Idempotency keys on update API calls prevent duplicate status writes. Trade-off: deduplication may suppress legitimate rapid status changes (e.g., Pending → Open → Pending within minutes).

- **State machine with allowed transitions for ticket updates:** Not all status transitions are valid (e.g., you can't go from Open to Closed without passing through Resolved). The engine uses a configurable state machine that validates transitions before executing them. Invalid transitions are logged and flagged for manual review. Trade-off: strict transition validation may block legitimate updates in helpdesk systems with custom workflows.

## Implementation Approach

```
interface StatusChangeEvent {
  ticketId: string;
  helpdeskType: string;
  previousStatus: string;
  newStatus: string;
  changedFields: Record<string, any>;
  timestamp: number;
  source: 'webhook' | 'polling' | 'api';
}

interface SyncRule {
  id: string;
  name: string;
  enabled: boolean;
  conditions: {
    field: string;       // Ticket field to evaluate
    operator: 'eq' | 'neq' | 'in' | 'changed_to' | 'changed_from';
    value: any;
  }[];
  matchMode: 'all' | 'any';
  actions: {
    type: 'schedule_call' | 'send_sms' | 'send_email' | 'webhook' | 'update_ticket';
    config: Record<string, any>;
    priority: number;
  }[];
}

class StatusSyncEngine {
  async handleStatusChange(event: StatusChangeEvent): Promise<void> {
    const dedupKey = `${event.ticketId}:${event.newStatus}:${event.timestamp}`;
    const isDuplicate = await this.checkDuplicate(dedupKey);
    if (isDuplicate) return;

    const matchingRules = await this.evaluateRules(event);
    for (const rule of matchingRules) {
      await this.executeActions(rule.actions, event);
    }

    await this.recordProcessed(dedupKey);
  }

  async evaluateRules(event: StatusChangeEvent): Promise<SyncRule[]> {
    const rules = await this.getActiveRules(event.helpdeskType);
    return rules.filter(rule => {
      const results = rule.conditions.map(condition => {
        switch (condition.operator) {
          case 'changed_to':
            return event.newStatus === condition.value;
          case 'changed_from':
            return event.previousStatus === condition.value;
          case 'in':
            return (condition.value as any[]).includes(event.newStatus);
          default:
            return false;
        }
      });

      return rule.matchMode === 'all' ? results.every(Boolean) : results.some(Boolean);
    });
  }

  async executeActions(actions: SyncRule['actions'], event: StatusChangeEvent): Promise<void> {
    for (const action of actions) {
      switch (action.type) {
        case 'schedule_call':
          await this.callScheduler.scheduleFollowUp({
            ticketId: event.ticketId,
            priority: action.priority,
            ...action.config
          });
          break;
        case 'update_ticket':
          await this.updateTicketStatus(event.ticketId, event.helpdeskType, action.config);
          break;
      }
    }
  }

  async updateTicketStatus(
    ticketId: string, helpdeskType: string, update: { status: string; comment?: string }
  ): Promise<void> {
    const adapter = this.adapterRegistry.get(helpdeskType);
    if (update.comment) {
      await adapter.addComment(ticketId, { body: update.comment, isPublic: false });
    }
    // Status update logic varies by helpdesk
    await this.recordStatusUpdate(ticketId, update.status);
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **BullMQ** (MIT) | Queue | Action execution queue |
| **Redis** (BSD) | Data store | Deduplication and state |
| **Node.js** (MIT) | Runtime | Rules engine execution |

## Production Considerations

**Scaling:** Webhook processing must handle bursts (hundreds of simultaneous events during ticket reassignments). The ingestion pipeline should batch process events before rule evaluation. Use Redis streams for event buffering. Rules evaluation is compute-bound — cache compiled rules in memory.

**Security:** Webhook endpoints must be secured with HMAC signature verification. Ticket status synchronization should respect access controls — the integration should only update tickets it has permission to modify. Log all synchronization actions for audit.

**Monitoring:** Track webhook processing latency, rule evaluation time, actions triggered per event, deduplication rate, and sync conflicts (status update rejected by helpdesk). Alert on webhook delivery failures, rule evaluation errors, and actions that fail to execute.
