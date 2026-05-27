# Section 04: Digest Email System

## Overview

The digest email system aggregates multiple notification events into scheduled email summaries. Digests are configurable as daily or weekly summaries, with content selected based on user preferences and event importance. The system handles content ranking, scheduling, and multi-channel delivery.

## Implementation Approach

```typescript
interface DigestConfig {
  id: string;
  userId: string;
  frequency: 'daily' | 'weekly' | 'custom';
  schedule: CronExpression;
  timezone: string;
  categories: string[];
  maxItems: number;
  includeSummary: boolean;
}

interface DigestContent {
  id: string;
  userId: string;
  period: TimeRange;
  items: DigestItem[];
  summary: DigestSummary;
  generatedAt: string;
}

class DigestGenerator {
  async generate(userId: string, config: DigestConfig): Promise<DigestContent> {
    const events = await this.collectEvents(userId, config);
    const ranked = this.rankItems(events);
    const truncated = ranked.slice(0, config.maxItems);
    const summary = this.createSummary(truncated, config);

    return {
      id: generateId(),
      userId,
      period: { start: this.getPeriodStart(config), end: new Date().toISOString() },
      items: truncated,
      summary,
      generatedAt: new Date().toISOString(),
    };
  }

  private async collectEvents(userId: string, config: DigestConfig): Promise<NotificationEvent[]> {
    const periodStart = this.getPeriodStart(config);
    return this.eventStore.query({
      userId,
      categories: { $in: config.categories },
      createdAt: { $gte: periodStart },
      read: false,
    });
  }

  private rankItems(events: NotificationEvent[]): DigestItem[] {
    return events.map(e => ({
      ...e,
      score: this.computeImportance(e),
    })).sort((a, b) => b.score - a.score);
  }

  private computeImportance(event: NotificationEvent): number {
    let score = 0;
    const severityScores = { critical: 100, major: 50, minor: 20, warning: 5 };
    score += severityScores[event.severity] || 0;
    if (event.requiresAction) score += 30;
    if (event.isUrgent) score += 20;
    return score;
  }

  private createSummary(items: DigestItem[], config: DigestConfig): DigestSummary {
    return {
      totalItems: items.length,
      byCategory: this.groupBy(items, 'category'),
      bySeverity: this.groupBy(items, 'severity'),
      requiresAction: items.filter(i => i.requiresAction).length,
      period: config.frequency,
    };
  }

  private getPeriodStart(config: DigestConfig): string {
    const now = new Date();
    switch (config.frequency) {
      case 'daily':
        now.setDate(now.getDate() - 1);
        break;
      case 'weekly':
        now.setDate(now.getDate() - 7);
        break;
    }
    return now.toISOString();
  }
}

class DigestScheduler {
  async scheduleDigest(userId: string, config: DigestConfig): Promise<void> {
    const job = {
      name: `digest:${userId}`,
      data: { userId, configId: config.id },
      repeat: { pattern: config.schedule },
      opts: { jobId: `digest:${userId}:${config.id}` },
    };
    await this.queue.add(job);
  }

  async processDigestJob(job: Job): Promise<void> {
    const { userId, configId } = job.data;
    const config = await this.digestConfigStore.get(configId);
    const content = await this.digestGenerator.generate(userId, config);
    await this.renderAndSend(userId, config, content);
  }
}
```

## Integration Points

- **Notification Store**: Collect events for digest
- **Email Queue**: Send digest via transactional email
- **Scheduler**: BullMQ repeatable jobs for digest scheduling

## Production Considerations

- **Generation Time**: Pre-generate digests before delivery time
- **Empty Digests**: Skip sending if no events to report
- **Timezone Handling**: Deliver based on user's timezone
