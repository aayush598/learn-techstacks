# Section 02: Schedule Definition & Calendar Integration

## Overview

Schedule definition allows creating and managing on-call schedules with CRUD operations. The system supports iCal export for calendar app integration, Google Calendar sync for automatic updates, and a team calendar view for visibility. Schedules define rotation periods, handoff times, and team assignments.

## Implementation Approach

```typescript
interface ScheduleDefinition {
  id: string;
  name: string;
  teamId: string;
  timezone: string;
  rotations: RotationConfig[];
  blackoutPeriods: TimeRange[];
  iCalUrl: string;
  googleCalendarId?: string;
}

interface RotationConfig {
  name: string;
  members: string[];
  type: 'daily' | 'weekly' | 'weekday' | 'weekend';
  startDate: string;
  shiftDuration: number;
  handoffTime: string; // HH:mm
}

class ScheduleManager {
  async createSchedule(definition: ScheduleDefinitionInput): Promise<ScheduleDefinition> {
    const schedule: ScheduleDefinition = {
      id: generateId(),
      ...definition,
      iCalUrl: this.generateICalUrl(definition),
      blackoutPeriods: definition.blackoutPeriods || [],
    };
    await this.storage.save(schedule);
    if (schedule.googleCalendarId) {
      await this.syncToGoogleCalendar(schedule);
    }
    return schedule;
  }

  async exportICal(scheduleId: string): Promise<string> {
    const schedule = await this.storage.get(scheduleId);
    const events = await this.computeEvents(schedule, { start: new Date(), end: new Date(Date.now() + 90 * 86400000) });

    let iCal = 'BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//OnCall//Schedule\n';
    for (const event of events) {
      iCal += 'BEGIN:VEVENT\n';
      iCal += `UID:${event.id}@oncall\n`;
      iCal += `DTSTART:${this.formatICalDate(event.start)}\n`;
      iCal += `DTEND:${this.formatICalDate(event.end)}\n`;
      iCal += `SUMMARY:On-Call: ${event.userName}\n`;
      iCal += `DESCRIPTION:On-call shift for ${schedule.name}\n`;
      iCal += `RRULE:FREQ=${this.getRRuleFreq(schedule)}\n`;
      iCal += 'END:VEVENT\n';
    }
    iCal += 'END:VCALENDAR';
    return iCal;
  }

  private generateICalUrl(schedule: ScheduleDefinition): string {
    const token = this.signToken({ scheduleId: schedule.id });
    return `${this.baseUrl}/api/schedules/${schedule.id}/ical?token=${token}`;
  }

  async syncToGoogleCalendar(schedule: ScheduleDefinition): Promise<void> {
    const events = await this.computeEvents(schedule, { start: new Date(), end: new Date(Date.now() + 30 * 86400000) });
    const calendar = await this.googleCalendarClient.getCalendar(schedule.googleCalendarId!);

    // Clear existing events and recreate
    await this.googleCalendarClient.clearCalendar(calendar.id);
    for (const event of events) {
      await this.googleCalendarClient.createEvent(calendar.id, {
        summary: `On-Call: ${event.userName}`,
        description: `On-call shift for ${schedule.name}`,
        start: { dateTime: event.start.toISOString(), timeZone: schedule.timezone },
        end: { dateTime: event.end.toISOString(), timeZone: schedule.timezone },
        reminders: { useDefault: true },
      });
    }
  }

  async getTeamCalendar(teamId: string, period: TimeRange): Promise<TeamCalendarView> {
    const schedules = await this.storage.query({ teamId });
    const allEvents: CalendarEvent[] = [];

    for (const schedule of schedules) {
      const events = await this.computeEvents(schedule, period);
      allEvents.push(...events.map(e => ({
        ...e,
        scheduleName: schedule.name,
        teamId,
      })));
    }

    return {
      teamId,
      period,
      events: allEvents.sort((a, b) => a.start.getTime() - b.start.getTime()),
    };
  }

  private async computeEvents(schedule: ScheduleDefinition, period: TimeRange): Promise<CalendarEvent[]> {
    const events: CalendarEvent[] = [];
    for (const rotation of schedule.rotations) {
      let cursor = new Date(Math.max(new Date(rotation.startDate).getTime(), new Date(period.start).getTime()));
      while (cursor < new Date(period.end)) {
        const memberIndex = this.getMemberIndex(rotation, cursor);
        const member = rotation.members[memberIndex % rotation.members.length];
        const shiftEnd = this.getShiftEnd(rotation, cursor);
        events.push({ id: generateId(), start: new Date(cursor), end: shiftEnd, userId: member, userName: member });
        cursor = shiftEnd;
      }
    }
    return events.filter(e => !this.isInBlackout(e, schedule.blackoutPeriods));
  }
}
```

## Integration Points

- **Google Calendar API**: Sync shifts to Google Calendar
- **iCal Export**: Subscribe in Apple/Outlook Calendar
- **Calendar View UI**: Team schedule visibility

## Production Considerations

- **Token Expiry**: Calendar sync tokens need refresh
- **Sync Limits**: Google Calendar API rate limits
- **Timezone Handling**: All times stored in UTC, displayed in user's timezone
