# Section 03: Calendly API Integration

## Overview

Calendly API integration connects the voice platform with Calendly's scheduling platform, enabling automated meeting booking through voice conversations. Calendly is optimized for one-click scheduling — users share their availability link, invitees pick a time, and the meeting is automatically added to the host's calendar. The Calendly API provides access to event types (scheduling configurations), scheduled events, invitees, availability, and webhook notifications.

The Calendly adapter differs from direct calendar integrations (Google, Outlook) because Calendly manages its own availability logic, timezone handling, and calendar synchronization. Instead of checking a calendar directly, the adapter works with Calendly's scheduling engine: it lists available event types for a user, retrieves available time slots for a specific event type, and creates a scheduled event through the API. Calendly handles all downstream calendar integration, confirmation emails, reminders, and cancellations.

## Architecture

```
                    Calendly Integration Architecture

   Voice Agent → Schedule Intent → Calendly Adapter → Calendly REST API
        |
        v
   +------------------+
   | Calendly Adapter  |
   | • Event types     |
   | • Availability    |
   | • Schedule event  |
   | • Cancel/Reschedule|
   +------------------+
        |
        v
   +------------------+
   | Calendly API v2   |
   | (REST)            |
   +------------------+
        |
        v
   +------------------+
   | Calendly Webhooks |
   | (Event creation   |
   |  notifications)   |
   +------------------+
```

## Design Decisions

- **Event type discovery for context-appropriate scheduling:** The adapter retrieves the user's active event types (15-min chat, 30-min sales call, 60-min demo) and presents them to the voice agent. The agent can determine which event type is appropriate based on the conversation context. This is more flexible than hardcoding a single event type. Trade-off: users with many event types may need voice-guided narrowing ("What type of meeting?").

- **Availability slot retrieval with duration matching:** The adapter fetches available slots for a specific event type within a date range. Slots are returned as ISO datetime ranges that respect the event type's duration, buffer time, and minimum notice period. The voice agent presents the options to the caller. Trade-off: Calendly availability retrieval may return many slots; the adapter should limit results to the most relevant (e.g., next 5 available slots).

- **Webhook integration for event lifecycle tracking:** Calendly webhooks notify the platform when events are created, cancelled, or rescheduled. The platform uses these to update internal state (marking scheduled calls, updating contact records) and to trigger follow-up actions (send reminder, update CRM). Webhooks use Calendly's HMAC signature for verification. Trade-off: webhook processing requires maintaining an event-to-contact mapping to correlate Calendly events with voice platform contacts.

## Implementation Approach

```
class CalendlyAdapter extends BaseAdapter {
  private baseUrl = 'https://api.calendly.com/v2';
  private userUri: string;

  async initialize(config: CalendlyConfig) {
    await super.initialize(config);
    // Resolve user URI
    const userResponse = await this.execute({
      method: 'GET', url: `${this.baseUrl}/users/me`
    });
    this.userUri = userResponse.data.resource.uri;
  }

  async getEventTypes(): Promise<AdapterResponse<EventType[]>> {
    const response = await this.execute({
      method: 'GET', url: `${this.baseUrl}/event_types`,
      params: { user: this.userUri, active: true }
    });

    return {
      success: true,
      data: response.data.collection.map(et => ({
        uri: et.uri,
        name: et.name,
        duration: et.duration,
        description: et.description,
        slug: et.slug,
        active: et.active,
        schedulingUrl: et.scheduling_url
      }))
    };
  }

  async getAvailableSlots(params: {
    eventTypeUri: string;
    startDate: string;
    endDate: string;
    maxResults?: number;
  }): Promise<AdapterResponse<TimeSlot[]>> {
    const response = await this.execute({
      method: 'GET', url: `${this.baseUrl}/event_type_available_times`,
      params: {
        event_type: params.eventTypeUri,
        start_time: params.startDate,
        end_time: params.endDate,
        max_results: params.maxResults || 10
      }
    });

    return {
      success: true,
      data: response.data.collection.map(slot => ({
        start: slot.start_time,
        end: slot.end_time,
        status: slot.status
      }))
    };
  }

  async scheduleEvent(event: {
    eventTypeUri: string;
    inviteeEmail: string;
    inviteeName: string;
    startTime: string;
    timezone?: string;
    guestEmails?: string[];
    customQuestions?: { question: string; answer: string }[];
  }): Promise<AdapterResponse<{ uri: string; eventUri: string }>> {
    const schedulingPayload = {
      event_type: event.eventTypeUri,
      start_time: event.startTime,
      invitee: {
        name: event.inviteeName,
        email: event.inviteeEmail,
        timezone: event.timezone || 'UTC',
        questions_and_answers: event.customQuestions?.map(q => ({
          question: q.question, answer: q.answer
        }))
      },
      guests: event.guestEmails?.map(email => ({ email })) || []
    };

    const response = await this.execute({
      method: 'POST', url: `${this.baseUrl}/scheduling_links`,
      data: schedulingPayload
    });

    return {
      success: true,
      data: {
        uri: response.data.resource.uri,
        eventUri: response.data.resource.event
      }
    };
  }

  async cancelEvent(eventUri: string, reason?: string): Promise<AdapterResponse<void>> {
    await this.execute({
      method: 'POST', url: `${eventUri}/cancellation`,
      data: { reason: reason || 'Cancelled by voice agent' }
    });
    return { success: true, data: undefined };
  }

  async verifyWebhook(signature: string, body: string): Promise<boolean> {
    const hmac = crypto.createHmac('sha256', this.config.webhookSecret);
    hmac.update(body);
    return hmac.digest('base64') === signature;
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Axios** (MIT) | HTTP client | REST API communication |
| **node-cron** (MIT) | Node.js | Webhook health check |

## Production Considerations

**Scaling:** Calendly API rate limits are 500 requests/minute per user token. Cache event type lists (infrequently changed) for 1 hour. Availability queries are time-sensitive and should not be cached beyond 30 seconds. Use webhook event buffering to handle burst notifications.

**Security:** Calendly uses Personal Access Tokens (PAT) for API authentication, scoped to a specific Calendly user. Tokens are stored encrypted. Webhook verification using HMAC-SHA256 signatures prevents spoofed notifications. OAuth 2.0 is available for marketplace apps.

**Monitoring:** Track scheduling requests per minute, availability query latency, event type changes (detect deletions or deactivations), webhook delivery success rate. Alert on scheduling failures (test with a mock booking), webhook verification failures, and API token expiry approaching.
