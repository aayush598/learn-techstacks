# Section 05: Reminder & Notification Campaigns

## Overview

Reminder and notification campaigns deliver time-sensitive information to contacts — appointment reminders, payment due notifications, shipping updates, and event reminders. These campaigns are characterized by strict timing requirements, high volume, and relatively simple interaction flows. The AI agent typically plays a brief notification, confirms receipt, and may offer simple menu options (confirm, reschedule, cancel).

The critical requirement for reminder campaigns is delivery within precise time windows. An appointment reminder that arrives too early is forgotten; one that arrives too late is useless. The system must support scheduled delivery with configurable lead times, timezone-aware delivery windows, and confirmation tracking. Integration with calendar systems and appointment management platforms is essential for bidirectional updates.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Audio    |--->| WebSocket|--->| Jitter   |--->| PLC      |--->| Player   |
| Producer |    | (WSS)    |    | Buffer   |    | (Packet  |    | (smooth  |
| (100ms   |    | (binary) |    | (adaptive|    |  Loss    |    |  output) |
|  chunks) |    |          |    |  60-200) |    |  Conceal)|    +----------+
+----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```
class ReminderCampaign {
  constructor(scheduler, deliveryEngine) {
    this.scheduler = scheduler;
    this.delivery = deliveryEngine;
    this.channelManager = new MultiChannelManager();
  }

  async scheduleReminders(contacts, reminderConfig) {
    for (const contact of contacts) {
      const deliveryTime = this.calculateOptimalTime(
        reminderConfig.leadTime,
        contact.timezone,
        reminderConfig.preferredWindows
      );

      await this.scheduler.schedule({
        jobType: 'deliver_reminder',
        contactId: contact.id,
        channel: this.determinePrimaryChannel(contact),
        scheduledAt: deliveryTime,
        reminderType: reminderConfig.type,
        payload: reminderConfig.payload
      });
    }
  }

  async deliverReminder(job) {
    const channels = this.channelManager.getChannelPriority(job.contact);
    
    for (const channel of channels) {
      const result = await channel.send(job.payload);
      
      if (result.confirmed) {
        await this.recordDelivery(job, channel.type, 'confirmed');
        await this.updateExternalSystem(job, result);
        return { status: 'confirmed', channel: channel.type };
      }
      
      if (result.isVoicemail) {
        await this.recordDelivery(job, channel.type, 'voicemail');
        continue; // Try next channel for confirmation
      }
    }
    
    await this.recordDelivery(job, null, 'failed');
    return { status: 'failed' };
  }

  calculateOptimalTime(leadTime, timezone, preferredWindows) {
    const eventTime = new Date(leadTime.referenceTime);
    const adjustedTime = new Date(eventTime.getTime() - leadTime.ms);
    // Clamp to preferred calling windows for the contact's timezone
    return this.clampToWindow(adjustedTime, timezone, preferredWindows);
  }
}
```

## Integration Points

- **Calendar Integration (Part 10, Ch 04):** Appointment data source and rescheduling updates
- **Scheduling Engine (Ch 03):** Timezone resolution and delivery window enforcement
- **Multi-Channel Communication:** SMS gateway and email service for fallback delivery
- **CRM System (Part 10, Ch 02):** Event/reminder status updates
- **Payment Gateway (Part 10, Ch 06):** Payment reminder links and payment confirmation
- **Analytics (Ch 09):** Reminder delivery rate and confirmation rate tracking

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Reminder delivery is time-sensitive — the scheduler must have millisecond precision for near-term reminders
- Implement idempotency keys to prevent duplicate reminder delivery from retries
- Reminder confirmation rates should be monitored — a sudden drop may indicate carrier or contact list issues
- Multi-touch reminder series should respect a global contact frequency cap (e.g., max 3 calls per day)
- Payment reminders must avoid creating urgency that triggers customer complaints — include clear opt-out instructions
- Appointment reminder confirmations should trigger waitlist and slot management updates in real-time
- Holiday and blackout date checking is critical — never deliver reminders on prohibited dates
- Track reminder fatigue — contacts who repeatedly confirm and no-show should trigger a review
