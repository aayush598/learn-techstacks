# Section 06: Calendar Event Synchronization

## Overview

Calendar event synchronization maintains bidirectional consistency between the voice platform's internal scheduling state and connected calendar systems. When events are created, updated, or cancelled through any channel (voice, web, API, or directly in the calendar), the synchronization service ensures all systems reflect the current state. This is critical for maintaining accurate availability — if an event is cancelled in Google Calendar but the platform doesn't know, the platform might offer that slot to another caller, leading to double-booking.

The sync engine handles conflict detection (two bookings for the same slot), change propagation (updating all connected services when an event changes), reconciliation (resolving differences between calendar and platform state), and tombstone management (tracking deleted events to prevent re-creation). The engine supports partial sync (only recent changes) and full re-sync on demand. It also handles edge cases: events created by other systems (non-voice events appearing in the calendar), tentative vs. confirmed events, and recurring event exceptions.

## Architecture

```
                    Calendar Event Synchronization

   +------------------+     +------------------+     +------------------+
   | Google Calendar  |     | Outlook Calendar |     | Other Sources    |
   | Changes          |     | Changes          |     | (API, web)       |
   +------------------+     +------------------+     +------------------+
           |                       |                       |
           v                       v                       v
   +----------------------------------------------------------+
   |              Event Synchronization Engine                 |
   |                                                          |
   |  Change Detection → Conflict Check → Apply → Notify     |
   |                                                          |
   |  1. Detect changes (webhook or polling)                  |
   |  2. Compare with platform state                          |
   |  3. Detect conflicts (same slot, 2 different events)     |
   |  4. Apply changes respecting write permissions           |
   |  5. Notify connected services of updates                 |
   +----------------------------------------------------------+
           |                       |                       |
           v                       v                       v
   +------------------+     +------------------+     +------------------+
   | Platform State   |     | CRM Event Log    |     | Notification     |
   | (Event Store)    |     | (Activity Record) |    | (Reminders)     |
   +------------------+     +------------------+     +------------------+
```

## Design Decisions

- **Webhook-first with polling reconciliation:** Calendar platforms provide push notifications for event changes (Google Watch API, Microsoft Graph subscriptions). The sync engine processes these in real-time. A periodic reconciliation job (every 30-60 minutes) performs a full diff between calendar state and platform state to catch missed notifications. Trade-off: reconciliation adds API load but provides a safety net against missed notifications.

- **Platform as source of truth for voice-created events, calendar-authoritative for others:** Events created through the voice platform are "owned" by the platform — changes in connected calendars are detected but the platform state takes precedence for these events (other systems should not modify voice-created events). For events created in the calendar directly, the calendar is authoritative. This split model prevents the platform from overwriting user-made changes while protecting voice bookings. Trade-off: the ownership model requires tracking which events were created by which system.

- **Tombstone-based deletion tracking:** When events are deleted, the platform creates a "tombstone" record (event ID, deletion timestamp) rather than immediately removing the event from the database. Tombstones prevent the event from being re-created by sync cycles. They are garbage-collected after 30 days. This provides a grace period for recovery if an event was accidentally deleted. Trade-off: tombstones require additional storage and cleanup processes.

## Implementation Approach

```
interface CalendarEvent {
  id: string;
  platformId?: string;
  calendarId: string;
  externalId: string;        // Calendar system's event ID
  source: 'voice_platform' | 'google_calendar' | 'outlook_calendar' | 'calendly';
  summary: string;
  startTime: number;
  endTime: number;
  status: 'confirmed' | 'tentative' | 'cancelled';
  attendees: string[];
  createdBy: string;
  etag: string;              // For change detection
  lastModified: number;
  metadata: Record<string, any>;
}

class CalendarEventSyncEngine {
  async processCalendarChange(change: {
    externalId: string; calendarId: string; source: string; action: 'created' | 'updated' | 'deleted';
  }): Promise<void> {
    const existing = await this.eventStore.findByExternalId(change.externalId, change.source);

    switch (change.action) {
      case 'created':
        if (!existing) {
          const event = await this.fetchEventDetails(change);
          if (!this.isDuplicate(event)) {
            await this.eventStore.create(this.toPlatformEvent(event));
            await this.notifyConnectedServices(event, 'created');
          }
        }
        break;

      case 'updated':
        if (existing && existing.source !== 'voice_platform') {
          // Calendar is authoritative for non-platform events
          const updatedEvent = await this.fetchEventDetails(change);
          if (this.hasConflict(existing, updatedEvent)) {
            await this.resolveConflict(existing, updatedEvent);
          } else {
            await this.eventStore.update(existing.id, updatedEvent);
            await this.notifyConnectedServices(updatedEvent, 'updated');
          }
        }
        break;

      case 'deleted':
        if (existing) {
          await this.eventStore.softDelete(existing.id);
          await this.notifyConnectedServices(existing, 'deleted');
        }
        break;
    }
  }

  async reconcile(calendarId: string, source: string): Promise<SyncResult> {
    const calendarEvents = await this.fetchAllCalendarEvents(calendarId, source);
    const platformEvents = await this.eventStore.findByCalendar(calendarId, source);

    const calendarMap = new Map(calendarEvents.map(e => [e.externalId, e]));
    const platformMap = new Map(platformEvents.map(e => [e.externalId, e]));

    const stats = { created: 0, updated: 0, deleted: 0, conflicts: 0 };

    // Process events in calendar but not in platform
    for (const [externalId, calEvent] of calendarMap) {
      if (!platformMap.has(externalId)) {
        await this.eventStore.create(this.toPlatformEvent(calEvent));
        stats.created++;
      } else if (this.hasChanged(calEvent, platformMap.get(externalId))) {
        await this.eventStore.update(platformMap.get(externalId).id, calEvent);
        stats.updated++;
      }
    }

    // Process events in platform but not in calendar
    for (const [externalId, platEvent] of platformMap) {
      if (!calendarMap.has(externalId) && platEvent.source === source) {
        // Only delete if calendar is the authoritative source
        if (platEvent.source !== 'voice_platform') {
          await this.eventStore.softDelete(platEvent.id);
          stats.deleted++;
        }
      }
    }

    return stats;
  }

  private hasConflict(existing: CalendarEvent, updated: any): boolean {
    // Check if two different events occupy overlapping time slots for the same user
    const timeChanged = existing.startTime !== new Date(updated.startTime).getTime() ||
                        existing.endTime !== new Date(updated.endTime).getTime();
    if (!timeChanged) return false;

    const overlapping = await this.eventStore.findOverlapping(
      existing.calendarId,
      new Date(updated.startTime).getTime(),
      new Date(updated.endTime).getTime(),
      existing.id
    );
    return overlapping.length > 0;
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **BullMQ** (MIT) | Queue | Sync job processing |
| **Redis** (BSD) | Cache | Change tracking state |
| **PostgreSQL** (PostgreSQL) | Data store | Event storage |

## Production Considerations

**Scaling:** Recurring full reconciliation is expensive — schedule during off-peak hours. Use incremental sync (only changes since last sync) for routine operations. Partition event storage by tenant and calendar ID for query performance. Implement backpressure on webhook processing to handle burst notification traffic.

**Security:** Event synchronization must respect calendar permissions — the integration can only access calendars the user has granted access to. Event data may contain sensitive information (meeting titles, attendee lists) — encrypt at rest and in transit. Do not sync events to tenants that the user hasn't authorized.

**Monitoring:** Track sync latency (time between calendar change and platform update), reconciliation duration and record counts, conflict rate (should be low, < 0.1%), webhook delivery reliability, and tombstone accumulation rate. Alert on sync lag exceeding 15 minutes, reconciliation failures, and conflict rate exceeding 1%.
