# Section 07: Rescheduling & Cancellation

## Overview

Rescheduling and cancellation workflows enable callers to modify or cancel existing appointments through voice conversations. These workflows are more complex than initial booking because they involve two-party confirmation (the calendar owner and the customer both need to be notified and agree), time-dependent policies (cancellation windows, fees, minimum notice periods), and resource reallocation (releasing the original slot, finding a new one).

The rescheduling workflow follows: identify the existing booking → confirm identity (security check) → understand the change (new time or cancellation) → check policies (is the change within allowed window?) → execute the change in all connected systems → notify all affected parties → update CRM and analytics. The cancellation workflow is similar but simpler (no new slot needed). Both workflows support partial changes (reschedule just one occurrence of a recurring series) and full changes (reschedule/cancel all occurrences).

## Architecture

```
                    Rescheduling & Cancellation Workflow

   Caller: "I need to reschedule my appointment"
        |
        v
   +------------------+
   | Booking Lookup    |
   | • Find by contact |
   | • Find by date    |
   | • Verify identity |
   +------------------+
        |
        v
   +------------------+
   | Policy Check      |
   | • Notice period   |
   | • Cancellation fee|
   | • Reschedule limit|
   +------------------+
        |
        v
   +------------------+     +------------------+
   | Reschedule?      | Yes | Availability     |
   |                  |---->| Check            |
   +------------------+     +------------------+
        |                            |
       No                            v
        v                     +------------------+
   +------------------+      | New Booking      |
   | Cancellation     |      | Create + Notify  |
   | Process          |      +------------------+
   +------------------+              |
        |                            v
        v                     +------------------+
   +------------------+      | Release Old Slot |
   | Release Slot     |<-----|                  |
   +------------------+      +------------------+
        |
        v
   +------------------+
   | Notifications     |
   | • Confirmation    |
   | • Calendar update |
   | • Email/SMS       |
   +------------------+
```

## Design Decisions

- **Policy-driven rescheduling with configurable rules:** Rescheduling and cancellation policies are configurable per event type/campaign: minimum notice period (e.g., 24 hours before appointment), maximum reschedules (e.g., 2 per booking), cancellation restrictions (e.g., cannot cancel within 2 hours of start), and fee conditions (e.g., cancellation after notice period incurs fee). The policy engine evaluates all rules and determines whether the change is allowed. Trade-off: complex policies can lead to surprising outcomes for callers; clear communication of policies during booking is essential.

- **Voice-based identity verification for booking modifications:** Before allowing changes, the system verifies the caller's identity through one or more factors: phone number match (calling from registered number), date of birth verification, security question, or PIN confirmation. The verification level required depends on the sensitivity of the booking (medical appointments require higher verification than retail consultations). Trade-off: verification adds friction but prevents unauthorized changes to bookings.

- **Original slot preservation during rescheduling (two-phase commit):** When rescheduling, the original slot is temporarily held (marked "pending release") while the new slot is created. If the new slot creation fails, the original slot is restored, preventing loss of the appointment. Once the new slot is confirmed, the original slot is released (deleted or made available). This "two-phase commit" pattern prevents accidental double-booking or lost appointments. Trade-off: the hold period (typically 30-60 seconds) temporarily reduces available slots for other callers.

## Implementation Approach

```
interface RescheduleRequest {
  bookingId: string;
  contactId: string;
  newStartTime?: string;    // For reschedule
  newEndTime?: string;
  reason?: string;
  action: 'reschedule' | 'cancel';
  cancellationScope?: 'this_occurrence' | 'future_occurrences' | 'all';
}

interface RescheduleResult {
  success: boolean;
  originalEventHandled: boolean;
  newEventCreated?: boolean;
  notificationsSent: string[];
  policyMessages: string[];   // Any policy-based messages (fees, limits)
  status: 'completed' | 'partial' | 'denied';
}

class ReschedulingService {
  async processReschedule(request: RescheduleRequest): Promise<RescheduleResult> {
    const originalBooking = await this.bookingStore.findById(request.bookingId);
    if (!originalBooking) {
      return { success: false, status: 'denied', notificationsSent: [], policyMessages: ['Booking not found'] };
    }

    // Policy check
    const policyResult = await this.policyEngine.evaluate(request.action, originalBooking);
    if (!policyResult.allowed) {
      return { success: false, status: 'denied', notificationsSent: [], policyMessages: policyResult.messages };
    }

    if (request.action === 'reschedule') {
      return this.handleReschedule(request, originalBooking, policyResult);
    }
    return this.handleCancellation(request, originalBooking, policyResult);
  }

  private async handleReschedule(
    request: RescheduleRequest, booking: any, policy: PolicyResult
  ): Promise<RescheduleResult> {
    // Phase 1: Hold original slot, create new booking
    await this.bookingStore.markPendingRelease(booking.id);

    try {
      const calendarAdapter = this.getCalendarAdapter(booking.userId);
      const newEvent = await calendarAdapter.createEvent({
        calendarId: booking.userId,
        summary: booking.summary,
        startTime: new Date(request.newStartTime),
        endTime: new Date(request.newEndTime),
        attendees: booking.attendees
      });

      // Phase 2: Release original slot
      await calendarAdapter.cancelEvent(booking.externalId, booking.userId);

      // Update platform state
      await this.bookingStore.update(booking.id, {
        externalId: newEvent.data.id,
        startTime: request.newStartTime,
        endTime: request.newEndTime,
        status: 'rescheduled'
      });

      // Notifications
      const sent = await this.sendChangeNotifications(booking, {
        type: 'rescheduled',
        newTime: { start: request.newStartTime, end: request.newEndTime }
      });

      return { success: true, originalEventHandled: true, newEventCreated: true, notificationsSent: sent, policyMessages: policy.messages, status: 'completed' };
    } catch (error) {
      // Rollback: restore original slot
      await this.bookingStore.unmarkPendingRelease(booking.id);
      return { success: false, originalEventHandled: false, notificationsSent: [], policyMessages: [`Reschedule failed: ${error.message}`], status: 'partial' };
    }
  }

  private async handleCancellation(
    request: RescheduleRequest, booking: any, policy: PolicyResult
  ): Promise<RescheduleResult> {
    const calendarAdapter = this.getCalendarAdapter(booking.userId);

    if (request.cancellationScope === 'this_occurrence' && booking.recurringEventId) {
      // Cancel single occurrence of recurring event
      await calendarAdapter.cancelOccurrence(booking.externalId, booking.userId, booking.startTime);
    } else {
      // Cancel entire event (or all future occurrences)
      await calendarAdapter.cancelEvent(booking.externalId, booking.userId);
    }

    await this.bookingStore.update(booking.id, { status: 'cancelled' });

    const sent = await this.sendChangeNotifications(booking, { type: 'cancelled', reason: request.reason });

    return { success: true, originalEventHandled: true, notificationsSent: sent, policyMessages: policy.messages, status: 'completed' };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **BullMQ** (MIT) | Queue | Async notification processing |
| **Redis** (BSD) | Cache | Pending release state |
| **PostgreSQL** (PostgreSQL) | Data store | Booking state |

## Production Considerations

**Scaling:** Two-phase commit for rescheduling can lead to contention if many reschedules happen simultaneously. Use Redis locks per booking ID to serialize operations. The hold period should have a TTL — if the process crashes mid-reschedule, the hold expires and the slot becomes available again.

**Security:** Identity verification for booking changes is critical. Implement rate limiting on verification attempts (prevent brute force). Log all booking changes with caller identity, timestamp, and verification method. Support admin override for legitimate exception cases (with audit trail).

**Monitoring:** Track reschedule rate (% of bookings that are rescheduled), cancellation rate, reschedule success rate, policy denial rate (indicates policy issues), identity verification failure rate, and rollback rate (two-phase commit failures). Alert on high rollback rates (> 5%), unexpected cancellation patterns (possible system issue), and identity verification failures.
