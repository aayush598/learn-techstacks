# Section 01: On-Call Rotation Management

## Overview

On-call rotation management defines schedules for assigning responders to shifts. Rotation types include daily, weekly, and custom schedules. The system handles shift handoffs, override management, and ensures coverage during gaps. Rotations integrate with calendar systems for visibility.

## Architecture

```
┌──────────────────────────────────────────────┐
│           On-Call Rotation Manager             │
│                                              │
│  ┌────────────┐  ┌────────────┐  ┌────────┐  │
│  │ Schedule    │  │ Rotation   │  │ Shift  │  │
│  │ Definition  │  │ Engine     │  │ Handoff│  │
│  │            │  │            │  │        │  │
│  │ Rotation   │──│ Assign     │──│ Handoff│  │
│  │ Types      │  │ Round-     │  │ Notify │  │
│  │ Days/Times │  │ Robin      │  │ Context│  │
│  │ Teams      │  │ Weighted   │  │ Transfer│  │
│  └────────────┘  └────────────┘  └────────┘  │
└──────────────────────────────────────────────┘
```

## Implementation Approach

```typescript
interface Rotation {
  id: string;
  name: string;
  teamId: string;
  type: 'daily' | 'weekly' | 'custom';
  members: RotationMember[];
  shiftDuration: number; // hours or days
  shiftStart: string; // cron expression
  timezone: string;
  handoffTime: number; // minutes before handoff
  overrides: RotationOverride[];
}

interface RotationMember {
  userId: string;
  weight: number; // for weighted rotation
  skills: string[];
  preferences: ShiftPreference[];
}

class RotationManager {
  async getCurrentOnCall(rotationId: string): Promise<OnCallEntry> {
    const rotation = await this.storage.get(rotationId);
    const schedule = await this.computeSchedule(rotation, new Date());
    return schedule.current;
  }

  async getOnCallSchedule(rotationId: string, period: TimeRange): Promise<OnCallSchedule> {
    const rotation = await this.storage.get(rotationId);
    const shifts: OnCallShift[] = [];

    let cursor = new Date(period.start);
    while (cursor < new Date(period.end)) {
      const shift = await this.computeShift(rotation, cursor);
      shifts.push(shift);
      cursor = this.advanceShift(rotation, cursor);
    }

    return { rotationId, shifts, period };
  }

  private async computeSchedule(rotation: Rotation, date: Date): Promise<OnCallSchedule> {
    const shift = await this.computeShift(rotation, date);
    const nextShift = await this.computeShift(rotation, this.advanceShift(rotation, date));
    return { current: shift, next: nextShift };
  }

  private async computeShift(rotation: Rotation, date: Date): Promise<OnCallShift> {
    // Check overrides
    const override = rotation.overrides.find(o =>
      date >= new Date(o.startDate) && date <= new Date(o.endDate)
    );
    if (override) {
      return { start: override.startDate, end: override.endDate, userId: override.userId, isOverride: true };
    }

    // Compute rotation
    const memberIndex = this.getMemberIndex(rotation, date);
    const member = rotation.members[memberIndex % rotation.members.length];
    const shiftStart = this.getShiftStart(rotation, date);
    const shiftEnd = this.getShiftEnd(rotation, shiftStart);

    return { start: shiftStart, end: shiftEnd, userId: member.userId, isOverride: false };
  }

  private getMemberIndex(rotation: Rotation, date: Date): number {
    const epoch = new Date('2024-01-01').getTime();
    const elapsed = date.getTime() - epoch;

    switch (rotation.type) {
      case 'daily':
        return Math.floor(elapsed / (24 * 3600 * 1000));
      case 'weekly':
        return Math.floor(elapsed / (7 * 24 * 3600 * 1000));
      case 'custom':
        return Math.floor(elapsed / (rotation.shiftDuration * 3600 * 1000));
    }
  }

  private getShiftEnd(rotation: Rotation, start: Date): Date {
    const durationMs = rotation.shiftDuration * (rotation.type === 'weekly' ? 7 : 1) * 3600 * 1000;
    return new Date(start.getTime() + durationMs);
  }

  private advanceShift(rotation: Rotation, current: Date): Date {
    return this.getShiftEnd(rotation, this.getShiftStart(rotation, current));
  }

  async createOverride(rotationId: string, override: RotationOverride): Promise<void> {
    const rotation = await this.storage.get(rotationId);
    rotation.overrides.push(override);
    await this.storage.update(rotation);
    await this.notifyOverride(rotation, override);
  }

  private async notifyOverride(rotation: Rotation, override: RotationOverride): Promise<void> {
    const overriddenUser = await this.getCurrentOnCall(rotation.id);
    await this.notificationService.send({
      userId: overriddenUser.userId,
      type: 'on_call_override',
      message: `Your on-call shift has been overridden for ${override.startDate} - ${override.endDate}`,
    });
  }
}
```

## Integration Points

- **Calendar Sync**: Export schedules to iCal/Google Calendar
- **Notification Service**: Shift reminders and handoff notifications
- **Team Service**: Team membership data

## Production Considerations

- **Coverage Gaps**: Alert when no one is scheduled
- **Fair Distribution**: Weighted rotation for experience levels
- **Override Audit**: Log all override changes
