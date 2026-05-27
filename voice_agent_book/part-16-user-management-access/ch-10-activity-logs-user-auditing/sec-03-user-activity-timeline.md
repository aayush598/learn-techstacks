# User Activity Timeline

## Overview

The user activity timeline displays a chronological feed of actions performed by or involving a specific user. It supports search, filtering by action type, and grouping of related events.

## Timeline Service

```typescript
interface ActivityTimelineQuery {
  userId: string;
  startDate?: Date;
  endDate?: Date;
  actions?: string[];
  limit?: number;
  cursor?: string;
}

class ActivityTimelineService {
  async getTimeline(query: ActivityTimelineQuery): Promise<PaginatedResult<ActivityEvent>> {
    const filters: any = {
      $or: [
        { 'actor.id': query.userId },
        { 'target.id': query.userId },
      ],
    };

    if (query.startDate) filters.timestamp = { $gte: query.startDate };
    if (query.endDate) filters.timestamp = { ...filters.timestamp, $lte: query.endDate };
    if (query.actions) filters.action = { $in: query.actions };

    const events = await this.db.find('activity_logs', filters, {
      sort: { timestamp: -1 },
      limit: query.limit || 50,
    });

    return {
      data: this.groupRelatedEvents(events),
      cursor: events.length === (query.limit || 50) ? events[events.length - 1].id : null,
    };
  }

  private groupRelatedEvents(events: ActivityEvent[]): ActivityGroup[] {
    const groups: ActivityGroup[] = [];
    const correlationMap = new Map<string, ActivityEvent[]>();

    for (const event of events) {
      if (event.context.correlationId) {
        const existing = correlationMap.get(event.context.correlationId) || [];
        existing.push(event);
        correlationMap.set(event.context.correlationId, existing);
      } else {
        groups.push({ primary: event, related: [] });
      }
    }

    for (const [_, related] of correlationMap) {
      if (related.length > 0) {
        groups.push({ primary: related[0], related: related.slice(1) });
      }
    }

    return groups.sort((a, b) => b.primary.timestamp.getTime() - a.primary.timestamp.getTime());
  }
}
```

## Timeline UI

```
Activity Timeline for Alice Johnson
┌─────────────────────────────────────────────────────┐
│  Today                                              │
├─────────────────────────────────────────────────────┤
│  2:30 PM  Campaign "Q3 Launch" created             │
│  1:15 PM  Agent configuration updated              │
│  11:00 AM Login from new device (Chrome on MacOS)   │
├─────────────────────────────────────────────────────┤
│  Yesterday                                           │
├─────────────────────────────────────────────────────┤
│  4:20 PM  Password changed                          │
│  2:00 PM  Call history exported (45 records)        │
│                     ╰─ Exported by admin@company.com │
│  10:30 AM Role changed: Agent → Senior Agent        │
└─────────────────────────────────────────────────────┘
```

## Open-Source Tools

- **React Infinite Scroll** (MIT) — Cursor-based pagination
- **date-fns** (MIT) — Date formatting

## Production Considerations

- Cache recent activity (last 24h) in Redis
- Use cursor-based pagination for performance
- Group related events by correlation ID
- Allow filtering by action type, date range, and actor
- Highlight security-relevant events (login, password change)
- Max 200 events per page
- Data available for 90 days in hot storage
