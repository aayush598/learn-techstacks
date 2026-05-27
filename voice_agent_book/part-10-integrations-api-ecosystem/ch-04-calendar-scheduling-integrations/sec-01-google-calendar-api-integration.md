# Section 01: Google Calendar API Integration

## Overview

Google Calendar API integration enables the voice platform to check availability, create appointments, and manage calendar events through voice conversations. The integration uses Google's REST API and client libraries to access calendar resources, manage events, handle attendees, and process notifications. Voice agents can check a user's calendar availability, schedule meetings, reschedule existing appointments, cancel events, and send calendar invites — all through natural language conversation.

The Google Calendar adapter must handle OAuth 2.0 authentication (with Google's unique consent flow), multiple calendar scopes (primary, secondary, shared calendars), event recurrence (daily, weekly, monthly patterns), attendee management (add/remove, check responses), conference creation (Google Meet links), and reminders (email and popup). The adapter also handles Google's quota limits (per-project, per-user, per-minute) and supports push notifications through the Google Watch API for real-time calendar changes.

## Architecture

```
                    Google Calendar Integration Architecture

   Voice Agent → Schedule Intent → Calendar Adapter → Google Calendar API
        |
        v
   +------------------+
   | Calendar Adapter  |
   | • Availability    |
   | • Event CRUD      |
   | • Attendees       |
   | • Conferencing    |
   +------------------+
        |
        v
   +------------------+
   | OAuth 2.0 Flow   |
   | (Google Identity)|
   +------------------+
        |
        v
   +------------------+
   | Google Calendar   |
   | REST API (v3)     |
   +------------------+
```

## Design Decisions

- **Or-availability (list of available slots) over yes/no availability checks:** Instead of asking "Is 3 PM free?" the adapter returns a list of available time slots within a requested window. This enables the voice agent to offer choices: "The nearest available slots are tomorrow at 10 AM, 2 PM, or 4 PM." Or-availability requires querying the calendar for busy periods and computing available gaps. Trade-off: computing available slots requires fetching all events in the window, which is more API-intensive than a single time check.

- **Conference creation with Google Meet links:** Events created through the platform automatically include Google Meet video conferencing links. The link is generated at event creation and included in the event description and invite emails. This provides a seamless virtual meeting experience without requiring users to create conferencing separately. Trade-off: Google Meet generation adds latency to event creation (~1-2 seconds) and requires additional API scopes.

- **Push notification channel via Google Watch API:** The adapter registers a push notification channel for calendar changes. Google sends HTTP POST requests to the platform's webhook endpoint when events are created, updated, or deleted. This enables real-time calendar syncing without polling. The channel must be renewed every 24 hours (Google's expiration limit). Trade-off: push notifications require a publicly accessible webhook endpoint and periodic channel renewal.

## Implementation Approach

```
class GoogleCalendarAdapter extends BaseAdapter {
  private calendar: any;  // Google Calendar API client

  async initialize(config: GoogleCalendarConfig) {
    const auth = new google.auth.OAuth2(config.clientId, config.clientSecret, config.redirectUri);
    auth.setCredentials({ refresh_token: config.refreshToken });
    this.calendar = google.calendar({ version: 'v3', auth });
  }

  async findAvailableSlots(params: {
    calendarId: string;
    startDate: Date;
    endDate: Date;
    durationMinutes: number;
    workingHours?: { start: string; end: string };
  }): Promise<AdapterResponse<TimeSlot[]>> {
    // Fetch busy periods
    const busyResponse = await this.calendar.freebusy.query({
      requestBody: {
        timeMin: params.startDate.toISOString(),
        timeMax: params.endDate.toISOString(),
        items: [{ id: params.calendarId }]
      }
    });

    const busyPeriods = busyResponse.data.calendars[params.calendarId].busy || [];
    const slots = this.computeAvailableSlots(
      params.startDate, params.endDate,
      params.durationMinutes, busyPeriods,
      params.workingHours
    );

    return { success: true, data: slots };
  }

  async createEvent(event: {
    calendarId: string; summary: string; description?: string;
    startTime: Date; endTime: Date;
    attendees?: { email: string }[];
    addConference?: boolean;
  }): Promise<AdapterResponse<{ id: string; hangoutLink?: string }>> {
    const calendarEvent = {
      summary: event.summary,
      description: event.description || '',
      start: { dateTime: event.startTime.toISOString(), timeZone: 'UTC' },
      end: { dateTime: event.endTime.toISOString(), timeZone: 'UTC' },
      attendees: event.attendees,
      conferenceData: event.addConference ? {
        createRequest: { requestId: uuid.v4(), conferenceSolutionKey: { type: 'hangoutsMeet' } }
      } : undefined,
      reminders: { useDefault: true }
    };

    const response = await this.calendar.events.insert({
      calendarId: event.calendarId,
      requestBody: calendarEvent,
      conferenceDataVersion: event.addConference ? 1 : 0
    });

    return {
      success: true,
      data: {
        id: response.data.id,
        hangoutLink: response.data.hangoutLink
      }
    };
  }

  async rescheduleEvent(eventId: string, calendarId: string, newStart: Date, newEnd: Date): Promise<AdapterResponse<void>> {
    await this.calendar.events.patch({
      calendarId,
      eventId,
      requestBody: {
        start: { dateTime: newStart.toISOString(), timeZone: 'UTC' },
        end: { dateTime: newEnd.toISOString(), timeZone: 'UTC' }
      }
    });
    return { success: true, data: undefined };
  }

  private computeAvailableSlots(
    start: Date, end: Date, duration: number, busyPeriods: any[], workingHours?: { start: string; end: string }
  ): TimeSlot[] {
    const slots: TimeSlot[] = [];
    const msInMinute = 60000;
    let cursor = new Date(start);

    while (cursor < end) {
      const slotEnd = new Date(cursor.getTime() + duration * msInMinute);
      if (slotEnd > end) break;

      const isBusy = busyPeriods.some(bp => {
        const busyStart = new Date(bp.start);
        const busyEnd = new Date(bp.end);
        return cursor < busyEnd && slotEnd > busyStart;
      });

      if (!isBusy) {
        slots.push({ start: cursor.toISOString(), end: slotEnd.toISOString() });
      }
      cursor = new Date(cursor.getTime() + 30 * msInMinute); // 30-min increments
    }
    return slots;
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **googleapis** (Apache 2.0) | Node.js | Google API client library |
| **OAuth.js** (MIT) | Node.js | OAuth2 flow handling |
| **node-cron** (MIT) | Node.js | Watch channel renewal |

## Production Considerations

**Scaling:** Google Calendar API quota varies by project (typically 1,000,000 queries/day, 60 queries/user/minute). Implement a per-user rate limiter. Cache calendar availability for short durations (30-60 seconds) since calendar data doesn't change rapidly. Use batch requests for multiple calendar operations.

**Security:** OAuth 2.0 tokens require user consent with specific scopes (https://www.googleapis.com/auth/calendar for read/write, https://www.googleapis.com/auth/calendar.events for event management). Request minimal scopes. Store refresh tokens encrypted. Implement token expiry monitoring.

**Monitoring:** Track API call volume by endpoint, availability check latency, event creation rate, watch channel health (renewal success rate), and quota utilization. Alert on watch channel renewal failures, quota approaching limits, and event creation error rate exceeding 5%.
