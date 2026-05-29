# Section 03: Scheduling System

## Overview

Digests are generated and delivered on configurable schedules using cron expressions. The scheduling system handles timezone-aware delivery, frequency management, and ad-hoc digest triggers. Schedules are managed per-user with team-level defaults.

## Architecture

```
Scheduling Architecture
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Scheduler] → [Due Check] → [Generation] → [Delivery]
      │              │              │              │
  BullMQ        Every minute,    Check user      Send via
  repeatable     check for      preferences,     configured
  jobs per      due digests     generate         channels
  digest config                  content

Schedule Evaluation:
  Time: 08:00 AM ET
    
  User A (NY/ET):   08:00 → Generate → Deliver ✓
  User B (LA/PT):   05:00 → Not due yet → Skip
  User C (London):  13:00 → Due → Generate ✓

  Cron Expression Examples:
    Daily at 8 AM:    0 8 * * *
    Weekly Monday:    0 9 * * 1
    Hourly:           0 * * * *
    Custom:           0 8,17 * * *  (twice daily)

Ad-Hoc Triggers:
  - User clicks "Send Digest Now" in preferences
  - High-priority alert triggers immediate mini-digest
  - API endpoint for programmatic trigger
```

## Design Decisions

- **Cron-Based Scheduling**: Industry-standard, flexible, timezone-aware
- **Timezone Conversion**: Schedules stored in user timezone, converted to UTC
- **Ad-Hoc Triggers**: Bypass schedule for immediate delivery
- **Rate Limiting**: Prevent more than one digest per minimum interval

## Implementation Approach

```typescript
interface DigestSchedule {
  userId: string;
  tenantId: string;
  frequency: 'hourly' | 'daily' | 'weekly';
  cronExpression?: string;
  timezone: string;
  preferredTime: string; // HH:MM
  enabled: boolean;
  nextDelivery?: Date;
  lastDelivery?: Date;
  adHocAllowed: boolean;
  minIntervalMs: number; // Minimum time between digests
}

class DigestScheduler {
  private cronParser: typeof import('cron-parser');

  async createSchedule(preferences: DigestPreferences): Promise<DigestSchedule> {
    const cronExpression = this.frequencyToCron(preferences.frequency, preferences.preferredTime);
    const nextDelivery = this.computeNextDelivery(cronExpression, preferences.timezone);

    const schedule: DigestSchedule = {
      userId: preferences.userId,
      tenantId: preferences.tenantId,
      frequency: preferences.frequency,
      cronExpression,
      timezone: preferences.timezone,
      preferredTime: preferences.preferredTime,
      enabled: true,
      nextDelivery,
      adHocAllowed: true,
      minIntervalMs: 3600000, // 1 hour minimum
    };

    await this.store.create('digest_schedules', schedule);

    // Register cron job
    await this.registerCronJob(schedule);

    return schedule;
  }

  async checkDueDigests(): Promise<DigestSchedule[]> {
    const now = new Date();
    const dueSchedules = await this.store.find('digest_schedules', {
      enabled: true,
      nextDelivery: { $lte: now },
    });

    return dueSchedules;
  }

  async triggerDigest(userId: string, isAdHoc: boolean = false): Promise<void> {
    const schedule = await this.store.findOne('digest_schedules', { userId });
    if (!schedule) throw new Error('No schedule found');

    if (isAdHoc && !schedule.adHocAllowed) {
      throw new Error('Ad-hoc digests not allowed');
    }

    // Rate limit check
    if (schedule.lastDelivery) {
      const elapsed = Date.now() - schedule.lastDelivery.getTime();
      if (elapsed < schedule.minIntervalMs) {
        throw new Error(`Please wait ${Math.ceil((schedule.minIntervalMs - elapsed) / 60000)} minutes`);
      }
    }

    // Generate and deliver
    const digest = await this.digestGenerator.generate(this.getConfig(userId));
    await this.digestDeliverer.deliver(digest, this.getChannels(userId));

    // Update schedule
    const nextDelivery = this.computeNextDelivery(schedule.cronExpression!, schedule.timezone);
    await this.store.update('digest_schedules', { userId }, {
      lastDelivery: new Date(),
      nextDelivery,
    });
  }

  async changeFrequency(
    userId: string,
    newFrequency: 'hourly' | 'daily' | 'weekly',
    newTime?: string,
  ): Promise<void> {
    const schedule = await this.store.findOne('digest_schedules', { userId });
    if (!schedule) throw new Error('No schedule found');

    const preferredTime = newTime || schedule.preferredTime;
    const cronExpression = this.frequencyToCron(newFrequency, preferredTime);
    const nextDelivery = this.computeNextDelivery(cronExpression, schedule.timezone);

    // Remove old cron job
    await this.removeCronJob(schedule);

    // Update schedule
    await this.store.update('digest_schedules', { userId }, {
      frequency: newFrequency,
      preferredTime,
      cronExpression,
      nextDelivery,
    });

    // Register new cron job
    await this.registerCronJob({
      ...schedule,
      frequency: newFrequency,
      cronExpression,
      nextDelivery,
    });
  }

  private frequencyToCron(frequency: string, time: string): string {
    const [hour, minute] = time.split(':').map(Number);

    switch (frequency) {
      case 'hourly':
        return `${minute} * * * *`;
      case 'daily':
        return `${minute} ${hour} * * *`;
      case 'weekly':
        return `${minute} ${hour} * * 1`; // Monday
      default:
        return `${minute} ${hour} * * *`;
    }
  }

  private computeNextDelivery(cronExpression: string, timezone: string): Date {
    const interval = this.cronParser.parseExpression(cronExpression, { tz: timezone });
    return interval.next().toDate();
  }

  private async registerCronJob(schedule: DigestSchedule): Promise<void> {
    await this.jobQueue.add(
      'generate-digest',
      { userId: schedule.userId },
      {
        repeat: { cron: schedule.cronExpression!, tz: schedule.timezone },
        jobId: `digest-${schedule.userId}`,
        removeOnComplete: true,
      },
    );
  }

  private async removeCronJob(schedule: DigestSchedule): Promise<void> {
    const repeatableJobs = await this.jobQueue.getRepeatableJobs();
    const job = repeatableJobs.find(
      (j: any) => j.id === `digest-${schedule.userId}`
    );
    if (job) {
      await this.jobQueue.removeRepeatableByKey(job.key);
    }
  }

  async pauseSchedule(userId: string): Promise<void> {
    const schedule = await this.store.findOne('digest_schedules', { userId });
    if (schedule) {
      await this.store.update('digest_schedules', { userId }, { enabled: false });
      await this.removeCronJob(schedule);
    }
  }

  async resumeSchedule(userId: string): Promise<void> {
    const schedule = await this.store.findOne('digest_schedules', { userId });
    if (schedule) {
      await this.store.update('digest_schedules', { userId }, { enabled: true });
      await this.registerCronJob({ ...schedule, enabled: true, nextDelivery: undefined });
    }
  }
}
```

## Integration Points

- **BullMQ**: Cron job scheduling for digest generation
- **Timezone Database**: IANA timezone support for accurate delivery times
- **User Preferences**: Schedule configuration tied to preference settings

## Production Considerations

- **Timezone Changes**: Handle DST transitions gracefully
- **Skew Handling**: Recompute next delivery on server time changes
- **Missed Digest Recovery**: Queue missed digest on scheduler restart
- **Load Distribution**: Stagger digest generation to avoid thundering herd

## Open-Source Tools

- **cron-parser**: Cron expression parsing and next-computation
- **BullMQ**: Repeatable job scheduling
- **luxon**: Timezone-aware datetime handling
