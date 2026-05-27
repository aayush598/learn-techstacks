# Section 06: On-Call Preferences

## Overview

On-call preferences allow team members to customize their on-call schedule. Preferences include personal schedule constraints, blackout dates, vacation handling, and rotation swaps. The system respects preferences while ensuring coverage.

## Implementation Approach

```typescript
interface OnCallPreferences {
  userId: string;
  maxShiftsPerMonth: number;
  preferredDays: DayOfWeek[];
  preferredShifts: TimeOfDay[];
  blackoutDates: DateRange[];
  vacations: Vacation[];
  swapRequests: SwapRequest[];
  unavailableDays: DayOfWeek[];
  minGapBetweenShifts: number; // hours
}

interface Vacation {
  id: string;
  startDate: string;
  endDate: string;
  type: 'vacation' | 'sick' | 'personal';
  status: 'pending' | 'approved' | 'rejected';
  backupUserId?: string;
}

interface SwapRequest {
  id: string;
  fromUserId: string;
  toUserId: string;
  shiftDate: string;
  reason: string;
  status: 'pending' | 'approved' | 'rejected' | 'expired';
  expiresAt: string;
}

class OnCallPreferencesManager {
  async updatePreferences(userId: string, preferences: Partial<OnCallPreferences>): Promise<OnCallPreferences> {
    const existing = await this.getPreferences(userId);
    Object.assign(existing, preferences);
    await this.storage.update(existing);
    return existing;
  }

  async setBlackoutDate(userId: string, dateRange: DateRange): Promise<void> {
    const prefs = await this.getPreferences(userId);
    prefs.blackoutDates.push(dateRange);
    await this.storage.update(prefs);
    await this.ensureCoverage(dateRange);
  }

  async requestVacation(userId: string, vacation: VacationInput): Promise<Vacation> {
    const vac: Vacation = {
      id: generateId(),
      ...vacation,
      status: 'pending',
    };

    await this.vacationStore.save(vac);

    // Find backup
    const backup = await this.findBackup(userId, vacation);
    if (backup) {
      vac.backupUserId = backup;
      await this.notifyBackup(vac);
    }

    // Notify team lead
    await this.notificationService.send({
      userId: await this.getTeamLead(userId),
      type: 'vacation_request',
      message: `${userId} requests vacation from ${vacation.startDate} to ${vacation.endDate}`,
    });

    return vac;
  }

  async approveVacation(vacationId: string, approverUserId: string): Promise<void> {
    const vacation = await this.vacationStore.get(vacationId);
    vacation.status = 'approved';
    await this.vacationStore.update(vacation);

    // Update schedule
    await this.scheduleService.addBlackout(vacation.backupUserId!, vacation.startDate, vacation.endDate);
    await this.notificationService.send({
      userId: vacation.userId,
      type: 'vacation_approved',
      message: 'Your vacation request has been approved.',
    });
  }

  async requestSwap(fromUserId: string, toUserId: string, shiftDate: string): Promise<SwapRequest> {
    const request: SwapRequest = {
      id: generateId(),
      fromUserId,
      toUserId,
      shiftDate,
      reason: '',
      status: 'pending',
      expiresAt: new Date(Date.now() + 7 * 86400000).toISOString(),
    };

    await this.swapStore.save(request);
    await this.notificationService.send({
      userId: toUserId,
      type: 'swap_request',
      message: `${fromUserId} requests to swap on-call shift on ${shiftDate}`,
      actions: [
        { label: 'Accept', actionId: 'accept_swap', value: request.id },
        { label: 'Decline', actionId: 'decline_swap', value: request.id },
      ],
    });

    return request;
  }

  async approveSwap(swapId: string, toUserId: string): Promise<void> {
    const request = await this.swapStore.get(swapId);
    if (request.toUserId !== toUserId) throw new Error('Unauthorized');
    if (new Date(request.expiresAt) < new Date()) {
      request.status = 'expired';
      await this.swapStore.update(request);
      throw new Error('Swap request expired');
    }

    request.status = 'approved';
    await this.swapStore.update(request);

    // Update schedule
    await this.scheduleService.swapShifts(request.fromUserId, request.toUserId, request.shiftDate);

    await this.notificationService.send({
      userId: request.fromUserId,
      type: 'swap_approved',
      message: `${toUserId} accepted your shift swap for ${request.shiftDate}`,
    });
  }

  private async findBackup(userId: string, vacation: VacationInput): Promise<string | null> {
    const team = await this.teamService.getTeamByMember(userId);
    const available = team.members.filter(m => m !== userId);

    for (const member of available) {
      const prefs = await this.getPreferences(member);
      const conflicts = prefs.blackoutDates.some(b =>
        new Date(vacation.startDate) <= new Date(b.endDate) &&
        new Date(vacation.endDate) >= new Date(b.startDate)
      );
      if (!conflicts) return member;
    }
    return null;
  }

  private async ensureCoverage(dateRange: DateRange): Promise<void> {
    const affectedSchedules = await this.scheduleService.getSchedulesForRange(dateRange);
    for (const schedule of affectedSchedules) {
      const coverage = await this.onCallService.getCoverage(schedule.id, dateRange);
      if (!coverage.covered) {
        await this.findCoverage(schedule.id, dateRange);
      }
    }
  }
}
```

## Integration Points

- **Team Service**: Team membership for backup finding
- **Schedule Service**: Schedule modification for swaps/vacations
- **Notification Service**: Preference change notifications

## Production Considerations

- **Minimum Coverage**: Ensure minimum coverage at all times
- **Fair Distribution**: Track shift frequency across team
- **Preference Conflicts**: Alert on scheduling conflicts
