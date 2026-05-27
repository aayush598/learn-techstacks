# Section 08: Unified Calendar Adapter

## Overview

The unified calendar adapter provides a consistent interface across multiple calendar platforms (Google Calendar, Outlook Calendar, Calendly) behind a single abstraction. This enables the voice platform to work with any calendar system through the same API, simplifying scheduling logic and enabling multi-calendar workflows where availability is checked across multiple sources.

The unified adapter defines a common set of operations: availability checking (what slots are free), event management (create, read, update, delete), attendee management, conferencing, and webhooks/notifications. Each platform-specific adapter implements these operations using its system's API semantics. The unified layer handles cross-cutting concerns like authentication, rate limiting, error mapping, capability detection (which systems support which features), and result normalization (time formats, status codes, error messages).

## Architecture

```
                    Unified Calendar Adapter

   +----------------------------------------------------------+
   |           Unified Calendar Interface                      |
   |                                                          |
   |  findAvailableSlots() | createEvent() | updateEvent()    |
   |  getEvent() | cancelEvent() | getEventTypes()            |
   |  registerWebhook() | verifyWebhook()                     |
   +----------------------------------------------------------+
              |              |              |
              v              v              v
   +------------------+  +------------------+  +------------------+
   | Google Calendar  |  | Outlook          |  | Calendly         |
   | Adapter          |  | Calendar Adapter |  | Adapter          |
   +------------------+  +------------------+  +------------------+
              |              |              |
              v              v              v
   +----------------------------------------------------------+
   |           Cross-Cutting Services                         |
   |                                                          |
   |  Authentication | Rate Limiting | Error Mapping          |
   |  Caching        | Retry Logic   | Observability          |
   +----------------------------------------------------------+
```

## Design Decisions

- **Capability-based adapter selection with automatic fallback:** Each calendar adapter declares its capabilities (supportsConferencing, supportsAttendees, supportsRecurrence, supportsAvailabilityDetails). The platform selects the appropriate adapter based on capability requirements. If the primary adapter doesn't support a required capability, the system falls back to a secondary adapter or returns a clear error. Trade-off: capability checks add routing complexity but prevent runtime errors from unsupported operations.

- **Normalized time handling across calendar systems:** Different calendar systems use different time formats (Google uses RFC 3339, Outlook uses ISO 8601 with timezone, Calendly uses UTC with timezone field). The unified adapter normalizes all times to UTC and stores timezone separately. Availability slots and event times are always returned as UTC with timezone information. Trade-off: normalization overhead is minimal but eliminates a common source of bugs.

- **Write-operations idempotency via idempotency keys:** All write operations (create, update, cancel) accept an optional idempotency key. The adapter ensures that the same key within a 24-hour window produces only one effect. This enables safe retry of write operations after timeouts or network failures. Trade-off: requires storing idempotency keys in the adapter's state store.

## Implementation Approach

```
// Unified calendar interface
interface CalendarAdapter {
  readonly platform: string;
  readonly capabilities: CalendarCapabilities;

  initialize(config: CalendarConfig): Promise<void>;
  healthCheck(): Promise<HealthStatus>;

  // Availability
  findAvailableSlots(params: AvailabilityParams): Promise<AdapterResponse<TimeSlot[]>>;
  getBusyPeriods(params: BusyPeriodParams): Promise<AdapterResponse<BusyPeriod[]>>;

  // Event management
  createEvent(event: CalendarEventInput): Promise<AdapterResponse<CalendarEventResult>>;
  getEvent(eventId: string, calendarId: string): Promise<AdapterResponse<CalendarEventResult>>;
  updateEvent(eventId: string, calendarId: string, update: Partial<CalendarEventInput>): Promise<AdapterResponse<void>>;
  cancelEvent(eventId: string, calendarId: string, reason?: string): Promise<AdapterResponse<void>>;

  // Event types (for scheduling platforms like Calendly)
  getEventTypes?(userId: string): Promise<AdapterResponse<EventType[]>>;

  // Conferencing
  getConferencingInfo?(eventId: string, calendarId: string): Promise<AdapterResponse<ConferencingInfo>>;

  // Webhook management
  registerWebhook?(config: WebhookConfig): Promise<AdapterResponse<{ id: string }>>;
  unregisterWebhook?(webhookId: string): Promise<AdapterResponse<void>>;
  verifyWebhook?(payload: any, signature: string): boolean;
}

interface CalendarCapabilities {
  availability: boolean;           // Supports free/busy queries
  eventCRUD: boolean;              // Supports create/update/delete
  attendees: boolean;              // Supports attendee management
  conferencing: boolean;           // Supports video/audio conferencing
  recurrence: boolean;             // Supports recurring events
  eventTypes: boolean;             // Supports event type definitions
  webhooks: boolean;               // Supports push notifications
  multipleCalendars: boolean;      // Supports multiple calendars per user
  readOnly?: boolean;              // Calendar is read-only
}

// Normalized domain types
interface CalendarEventInput {
  summary: string;
  description?: string;
  startTime: string;           // ISO 8601 UTC
  endTime: string;             // ISO 8601 UTC
  timeZone?: string;
  attendees?: { email: string; name?: string; response?: 'accepted' | 'declined' | 'tentative' }[];
  conference?: { provider: 'google_meet' | 'teams' | 'zoom' | 'none' };
  recurrence?: string[];       // RRULE strings
  reminders?: { method: 'email' | 'popup'; minutes: number }[];
  idempotencyKey?: string;
}

interface CalendarEventResult {
  id: string;
  externalId: string;
  calendarId: string;
  summary: string;
  startTime: string;
  endTime: string;
  timeZone: string;
  status: 'confirmed' | 'tentative' | 'cancelled';
  hangoutLink?: string;
  conferenceData?: any;
  attendees?: { email: string; response: string }[];
  createdAt: string;
  updatedAt: string;
}

class CalendarAdapterFactory {
  private adapters = new Map<string, CalendarAdapter>();

  register(type: string, adapter: CalendarAdapter) {
    this.adapters.set(type, adapter);
  }

  getAdapter(type: string): CalendarAdapter {
    const adapter = this.adapters.get(type);
    if (!adapter) throw new Error(`Unsupported calendar type: ${type}`);
    return adapter;
  }

  async getBestAdapter(userConfig: CalendarConfig): Promise<CalendarAdapter> {
    const primary = this.getAdapter(userConfig.type);
    await primary.initialize(userConfig);
    return primary;
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **TypeScript** (Apache 2.0) | Language | Interface definitions |
| **Zod** (MIT) | Validation | Canonical model validation |
| **date-fns** (MIT) | Dates | Time zone handling |

## Production Considerations

**Scaling:** The unified adapter adds abstraction overhead. Profile adapter method performance to ensure < 10ms overhead above the platform API call. Cache adapter instances by integration configuration. For multi-calendar users, parallelize queries across adapters.

**Security:** Adapters must handle authentication credentials (OAuth tokens, API keys) securely. Never expose credentials through the unified interface. The unified adapter should not log sensitive fields (event details, attendee emails) in plain text.

**Monitoring:** Track adapter distribution by calendar type, per-operation latency by adapter, capability mismatch rate (attempting unsupported operations), and adapter initialization failures. Alert on adapter health check failures, initialization errors, and operations that fall back to fallback adapters.
