# Section 05: Booking Creation from Voice

## Overview

Booking creation from voice enables callers to schedule appointments, meetings, and events through natural conversation with the voice agent. The booking workflow follows a conversational flow: identify the intent ("I'd like to book an appointment"), determine the context (type of appointment, reason), check availability, present options, confirm the booking, create the event, and send confirmation. The system handles the full lifecycle including rescheduling, cancellation, and reminder management.

The booking creation service orchestrates multiple subsystems: natural language understanding (identifying date/time references, duration preferences, and event types), availability checking (querying calendar integrations), user preference management (preferred times, locations, meeting types), confirmation processing (voice confirmation, dual factor for high-stakes bookings), and post-booking actions (calendar event creation, confirmation messages, CRM updates). The service supports one-time bookings and recurring bookings (daily, weekly, monthly patterns).

## Architecture

```
                    Booking Creation Workflow

   Caller: "I'd like to book a consultation"
        |
        v
   +------------------+
   | Intent Recognition|
   | • Booking intent  |
   | • Event type      |
   | • Date/time ref   |
   | • Duration        |
   +------------------+
        |
        v
   +------------------+
   | Availability Check|
   | • Query calendars |
   | • Find slots      |
   | • Consider prefs  |
   +------------------+
        |
        v
   +------------------+
   | Slot Presentation |
   | Voice: "Available |
   | times: Tue 2pm,   |
   | Wed 10am, Thu 3pm"|
   +------------------+
        |
        v
   Caller selects slot
        |
        v
   +------------------+
   | Booking Creation  |
   | • Create event    |
   | • Send invite     |
   | • Update CRM      |
   | • Confirm to user |
   +------------------+
```

## Design Decisions

- **Conversational slot narrowing over listing all options:** Instead of listing all available slots (which overwhelms callers), the system uses conversational narrowing: "What day works best for you?" → "Morning or afternoon?" → "I have 10 AM or 2 PM on Tuesday." This reduces cognitive load and speeds up the booking process. The narrowing strategy is configurable — more options for power users, fewer for casual callers. Trade-off: narrowing requires more conversation turns but results in higher booking completion rates.

- **Implicit confirmation with explicit confirmation override:** For low-stakes bookings (15-min chat, standard appointments), the system uses implicit confirmation: "Great, I've booked your consultation for Tuesday at 2 PM. You'll receive a confirmation email." For high-stakes bookings (medical appointments, financial consultations), explicit confirmation is required: "To confirm, Tuesday at 2 PM with Dr. Smith. Say 'Yes' to confirm." Trade-off: explicit confirmation for all bookings would add friction; implicit-only risks misunderstandings for critical appointments.

- **Post-booking action chain with error handling:** After booking creation, a chain of actions executes: calendar event creation → email confirmation → CRM update → follow-up campaign enrollment. If any action fails (CRMs down, email delivery failure), the chain continues but the failure is logged and retried. The booking is considered successful once the calendar event is created. Trade-off: partial action failures require manual reconciliation but don't block the booking from completing.

## Implementation Approach

```
interface BookingRequest {
  contactId: string;
  tenantId: string;
  eventType: string;
  duration: number;
  preferredDateRange?: { start: string; end: string };
  preferredTimes?: string[];
  participants?: string[];
  notes?: string;
  userId: string;  // The person whose calendar is being booked
}

interface BookingResult {
  success: boolean;
  eventId?: string;
  eventSummary?: string;
  startTime?: string;
  endTime?: string;
  confirmationStatus: 'confirmed' | 'pending_approval' | 'failed';
  fallbackMessage?: string;
  postBookingStatus: {
    calendarCreated: boolean;
    emailSent: boolean;
    crmUpdated: boolean;
    failures: string[];
  };
}

class BookingCreationService {
  async createBooking(request: BookingRequest): Promise<BookingResult> {
    const calendarAdapter = this.getCalendarAdapter(request.userId);

    // Find available slots
    const slots = await calendarAdapter.findAvailableSlots({
      calendarId: request.userId,
      startDate: new Date(request.preferredDateRange?.start || Date.now()),
      endDate: new Date(request.preferredDateRange?.end || Date.now() + 7 * 86400000),
      durationMinutes: request.duration
    });

    if (slots.length === 0) {
      return {
        success: false,
        confirmationStatus: 'failed',
        fallbackMessage: 'No available slots in the requested time range.'
      };
    }

    // Select slot (first matching preference or best available)
    const selectedSlot = this.selectBestSlot(slots, request.preferredTimes);

    // Create event
    const eventResult = await calendarAdapter.createEvent({
      calendarId: request.userId,
      summary: `${request.eventType} - Voice booking`,
      description: request.notes || `Booked via voice agent\nContact: ${request.contactId}`,
      startTime: new Date(selectedSlot.start),
      endTime: new Date(selectedSlot.end),
      attendees: [request.userId, ...request.participants].map(id => ({ email: id }))
    });

    // Execute post-booking actions
    const postStatus = await this.executePostBookingActions(request, eventResult.data);

    return {
      success: true,
      eventId: eventResult.data.id,
      eventSummary: request.eventType,
      startTime: selectedSlot.start,
      endTime: selectedSlot.end,
      confirmationStatus: 'confirmed',
      postBookingStatus: postStatus
    };
  }

  private async executePostBookingActions(
    request: BookingRequest, event: { id: string; hangoutLink?: string }
  ): Promise<BookingResult['postBookingStatus']> {
    const status = {
      calendarCreated: true,
      emailSent: false,
      crmUpdated: false,
      failures: [] as string[]
    };

    try {
      await this.notificationService.sendConfirmation(request.contactId, event);
      status.emailSent = true;
    } catch (error) {
      status.failures.push(`email: ${error.message}`);
    }

    try {
      await this.crmService.logActivity(request.contactId, {
        type: 'appointment_scheduled',
        eventId: event.id,
        metadata: event
      });
      status.crmUpdated = true;
    } catch (error) {
      status.failures.push(`crm: ${error.message}`);
    }

    return status;
  }

  private selectBestSlot(slots: TimeSlot[], preferredTimes?: string[]): TimeSlot {
    if (!preferredTimes?.length) return slots[0];

    const preferred = preferredTimes.map(t => t.toLowerCase());
    const preferredSlot = slots.find(s => {
      const hour = new Date(s.start).getHours();
      return preferred.some(p => {
        if (p === 'morning') return hour >= 8 && hour < 12;
        if (p === 'afternoon') return hour >= 12 && hour < 17;
        if (p === 'evening') return hour >= 17 && hour < 20;
        return s.start.includes(p);
      });
    });
    return preferredSlot || slots[0];
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **BullMQ** (MIT) | Queue | Post-booking action queuing |
| **date-fns** (MIT) | Dates | Date/time manipulation |
| **Redis** (BSD) | Cache | Booking state caching |

## Production Considerations

**Scaling:** Booking creation is moderately resource-intensive (availability queries, event creation, post-booking chain). Process bookings asynchronously via a queue to ensure smooth handling during peak call volume. Cache availability results briefly to avoid redundant queries during the booking conversation (user says "show me the next day").

**Security:** Booking creation requires write access to calendars. Ensure the voice agent is authenticated with appropriate permissions. Implement booking limits per caller (prevent booking spam). Validate that requested booking times are not in the past. Log all booking actions for audit.

**Monitoring:** Track booking completion rate (% of booking intents that result in booked events), average booking conversation duration, slot selection distribution, post-booking action success rate, and booking cancellation/ reschedule rate. Alert on low booking completion rate (< 50% — may indicate issues with intent recognition or slot availability) and post-booking action failures.
