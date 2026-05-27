# Section 02: Microsoft Outlook Calendar Integration

## Overview

Microsoft Outlook Calendar integration connects the voice platform with Microsoft 365 calendar through the Microsoft Graph API. The integration enables checking availability, scheduling meetings, managing events, and processing calendar sharing across Exchange Online and Outlook desktop users. The Graph API provides a unified endpoint for calendars, events, mail, and contacts within the Microsoft 365 ecosystem.

The Outlook Calendar adapter handles Microsoft's unique calendar characteristics: the concept of "master" recurring events with individual "exception" instances, the distinction between "organizer" and "attendee" roles, Online Meeting creation (Teams meetings with join URLs), rich email notifications through Exchange transport, and calendar sharing/delegation permissions. The adapter uses Microsoft's delegated authentication (acting on behalf of a user) and supports both work/school accounts (Azure AD) and personal Microsoft accounts.

## Architecture

```
                    Microsoft Outlook Calendar Integration

   Voice Agent → Schedule Intent → Graph API Adapter → Microsoft Graph API
        |
        v
   +------------------+
   | Graph API Adapter |
   | • Calendar read   |
   | • Event CRUD      |
   | • Online meetings |
   | • Notifications   |
   +------------------+
        |
        v
   +------------------+
   | Microsoft Auth    |
   | (Azure AD OAuth2) |
   +------------------+
        |
        v
   +------------------+
   | Microsoft Graph   |
   | API (v1.0)        |
   +------------------+
```

## Design Decisions

- **Graph API v1.0 over Exchange Web Services (EWS):** Microsoft Graph is the modern API for Microsoft 365 data, replacing EWS and Azure AD Graph. Graph API provides consistent REST endpoints, OAuth 2.0 authentication, JSON responses, and SDK support. EWS is deprecated for new integrations. Graph API is rate-limited per app and per user, requiring careful quota management. Trade-off: some advanced Exchange features (mailbox forwarding rules, resource mailbox configuration) are only available in EWS.

- **Teams meeting integration for online conferencing:** Events created through the platform can include Microsoft Teams online meeting links. The `onlineMeetingProvider` property is set to "teamsForBusiness" and the event includes the join URL, conference ID, and dial-in phone number. This provides enterprise users with familiar meeting experiences. Trade-off: Teams meeting creation adds latency and requires the user to have a Teams license.

- **Subscription-based change notifications over polling:** Microsoft Graph supports webhook subscriptions (change notifications) for calendar events. The platform registers subscriptions for each user's calendar and receives push notifications when events change. Subscriptions expire after a configurable period (max 3 days for high-frequency, 30 days for low-frequency). Trade-off: subscription renewal must be managed proactively to avoid notification gaps.

## Implementation Approach

```
class OutlookCalendarAdapter extends BaseAdapter {
  private graphClient: any;

  async initialize(config: OutlookCalendarConfig) {
    const authProvider = new MicrosoftAuthProvider(config);
    this.graphClient = MicrosoftGraph.Client.initWithMiddleware({
      authProvider: authProvider
    });
  }

  async findAvailableSlots(params: {
    userId: string;
    startDate: string;  // ISO string
    endDate: string;
    durationMinutes: number;
    timeZone?: string;
  }): Promise<AdapterResponse<TimeSlot[]>> {
    const response = await this.graphClient
      .api(`/users/${params.userId}/calendar/getSchedule`)
      .post({
        schedules: [params.userId],
        startTime: { dateTime: params.startDate, timeZone: params.timeZone || 'UTC' },
        endTime: { dateTime: params.endDate, timeZone: params.timeZone || 'UTC' },
        availabilityViewInterval: params.durationMinutes
      });

    const schedule = response.value?.[0];
    const slots = this.parseAvailabilityView(
      schedule.availabilityView, params.startDate, params.endDate, params.durationMinutes
    );

    return { success: true, data: slots };
  }

  async createEvent(event: {
    userId: string; subject: string; body?: string;
    start: { dateTime: string; timeZone: string };
    end: { dateTime: string; timeZone: string };
    attendees?: { emailAddress: { address: string; name: string }; type?: string }[];
    isOnlineMeeting?: boolean;
  }): Promise<AdapterResponse<{ id: string; onlineMeetingUrl?: string }>> {
    const graphEvent = {
      subject: event.subject,
      body: { contentType: 'text', content: event.body || '' },
      start: event.start,
      end: event.end,
      attendees: event.attendees?.map(a => ({
        emailAddress: a.emailAddress,
        type: a.type || 'required'
      })),
      isOnlineMeeting: event.isOnlineMeeting || false,
      onlineMeetingProvider: event.isOnlineMeeting ? 'teamsForBusiness' : undefined
    };

    const response = await this.graphClient
      .api(`/users/${event.userId}/events`)
      .post(graphEvent);

    return {
      success: true,
      data: {
        id: response.id,
        onlineMeetingUrl: response.onlineMeeting?.joinUrl
      }
    };
  }

  async cancelEvent(eventId: string, userId: string, message?: string): Promise<AdapterResponse<void>> {
    await this.graphClient
      .api(`/users/${userId}/events/${eventId}/cancel`)
      .post({ comment: message || 'Cancelled via voice agent' });
    return { success: true, data: undefined };
  }

  private parseAvailabilityView(
    view: string, startDate: string, endDate: string, intervalMinutes: number
  ): TimeSlot[] {
    const slots: TimeSlot[] = [];
    const start = new Date(startDate);
    const intervalMs = intervalMinutes * 60 * 1000;

    for (let i = 0; i < view.length; i++) {
      const slotStart = new Date(start.getTime() + i * intervalMs);
      if (view[i] === '0') {  // '0' = free
        slots.push({
          start: slotStart.toISOString(),
          end: new Date(slotStart.getTime() + intervalMs).toISOString()
        });
      }
    }
    return slots;
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Microsoft Graph SDK** (MIT) | Node.js | Graph API client |
| **@azure/identity** (MIT) | Node.js | Azure AD authentication |
| **node-cron** (MIT) | Node.js | Subscription renewal cron |

## Production Considerations

**Scaling:** Graph API throttling is per-app-per-user (typically 10,000 requests per 10 minutes per user per app). Implement user-level token bucket rate limiting. Cache availability results for 30-60 seconds. Use batch requests (Graph API supports `/batch` endpoint for grouping requests).

**Security:** Microsoft Graph requires Azure AD app registration with specific delegated permissions (Calendars.Read, Calendars.ReadWrite). Use the principle of least privilege — request only the permissions needed. Implement admin consent workflow for tenant-wide access. Store refresh tokens securely.

**Monitoring:** Track Graph API request volume, rate limit hits, subscription health (expiry and renewal status), event creation/ cancellation rates, and availability query latency. Alert on subscription renewal failures (critical — missed notifications), rate limit exceeding 80%, and authentication failures.
