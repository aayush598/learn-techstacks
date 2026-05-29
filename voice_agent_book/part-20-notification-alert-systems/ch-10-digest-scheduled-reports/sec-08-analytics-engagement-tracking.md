# Section 08: Analytics & Engagement Tracking

## Overview

Digest analytics track open rates, click-through rates, and engagement patterns to measure digest effectiveness. Engagement scoring identifies which content types drive user action, and A/B testing optimizes digest content, timing, and formatting for maximum engagement.

## Architecture

```
Analytics Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Digest Sent] → [User Action] → [Event Tracking] → [Analytics DB] → [Dashboard]
       │               │                │                │               │
  Email sent       User opens       Track pixel      PostgreSQL      Engagement
  Slack posted     User clicks      (email open)     + Redis         metrics
  In-app shown     User converts    Webhook click     (real-time)     Content perf
                                    API event push                    A/B test results

Tracked Events:
  Event              Channel     Data Collected
  ────────────────────────────────────────────────────────
  digest.sent        all         digestId, channel, timestamp
  digest.open        email       digestId, userAgent, IP, timestamp
  digest.click       all         digestId, itemId, moduleId, timestamp
  digest.convert     all         digestId, itemId, action taken
  digest.unsubscribe email       digestId, reason, timestamp
  digest.bounce      email       digestId, bounce type, timestamp

Dashboard Metrics:
  ┌──────────────────────────────────────────────────────┐
  │ Digest Performance                                     │
  │                                                        │
  │ Delivery Rate:  99.2%     ▲ 0.5% from last week       │
  │ Open Rate:      42.3%     ▲ 2.1%                      │
  │ Click Rate:     12.7%     ▼ 0.8%                      │
  │ Unsubscribe:    0.8%      ▼ 0.2%                      │
  │                                                        │
  │ Top Performing Content:                                 │
  │   Critical Alerts       30.2% CTR  ▲ 5.2%              │
  │   Daily Stats           15.4% CTR  — 0.1%              │
  │   Warnings              8.9% CTR   ▼ 1.2%              │
  │                                                        │
  │ A/B Test: Subject Line                                 │
  │   A: "Your Daily Digest"    Open: 38%  ✓               │
  │   B: "🔴 2 alerts waiting"  Open: 45%  *WINNER*        │
  └──────────────────────────────────────────────────────┘
```

## Design Decisions

- **Tracking Pixel**: 1x1 transparent GIF for email open tracking
- **Link Wrapping**: All links go through tracking redirect service
- **Real-Time Dashboard**: Redis for real-time event counts
- **A/B Testing**: Randomized user assignment with statistical significance check

## Implementation Approach

```typescript
interface DigestEvent {
  id: string;
  digestId: string;
  userId: string;
  tenantId: string;
  type: 'sent' | 'open' | 'click' | 'convert' | 'unsubscribe' | 'bounce';
  channel: string;
  metadata?: {
    itemId?: string;
    moduleId?: string;
    userAgent?: string;
    ipAddress?: string;
    conversionAction?: string;
    bounceType?: string;
  };
  timestamp: Date;
}

interface EngagementMetrics {
  digestId: string;
  sentCount: number;
  openCount: number;
  clickCount: number;
  convertCount: number;
  unsubscribeCount: number;
  bounceCount: number;
  openRate: number;
  clickRate: number;
  conversionRate: number;
  unsubscribeRate: number;
}

interface EngagementScore {
  userId: string;
  overallScore: number;
  moduleScores: Record<string, number>;
  preferredChannel: string;
  preferredTime: string;
  lastEngaged: Date;
}

class DigestAnalytics {
  private redis: Redis;

  async trackEvent(event: Omit<DigestEvent, 'id' | 'timestamp'>): Promise<void> {
    const fullEvent: DigestEvent = {
      ...event,
      id: crypto.randomUUID(),
      timestamp: new Date(),
    };

    // Store in PostgreSQL for persistence
    await this.db.insert('digest_events', fullEvent);

    // Update real-time counters in Redis
    const hour = new Date().setMinutes(0, 0, 0);
    await this.redis.pipeline()
      .incr(`digest:${fullEvent.digestId}:${fullEvent.type}`)
      .incr(`digest:${fullEvent.digestId}:channel:${fullEvent.channel}:${fullEvent.type}`)
      .incr(`digest:metrics:hourly:${hour}:${fullEvent.type}`)
      .exec();

    // If click, attribute to specific module
    if (fullEvent.type === 'click' && fullEvent.metadata?.moduleId) {
      await this.redis.incr(
        `digest:${fullEvent.digestId}:module:${fullEvent.metadata.moduleId}:clicks`
      );
    }
  }

  async getMetrics(digestId: string): Promise<EngagementMetrics> {
    const [sent, open, click, convert, unsubscribe, bounce] = await Promise.all([
      this.db.count('digest_events', { digestId, type: 'sent' }),
      this.db.count('digest_events', { digestId, type: 'open' }),
      this.db.count('digest_events', { digestId, type: 'click' }),
      this.db.count('digest_events', { digestId, type: 'convert' }),
      this.db.count('digest_events', { digestId, type: 'unsubscribe' }),
      this.db.count('digest_events', { digestId, type: 'bounce' }),
    ]);

    return {
      digestId, sentCount: sent, openCount: open, clickCount: click,
      convertCount: convert, unsubscribeCount: unsubscribe, bounceCount: bounce,
      openRate: sent > 0 ? open / sent : 0,
      clickRate: sent > 0 ? click / sent : 0,
      conversionRate: sent > 0 ? convert / sent : 0,
      unsubscribeRate: sent > 0 ? unsubscribe / sent : 0,
    };
  }

  async getModulePerformance(digestId: string): Promise<ModulePerformance[]> {
    const clicks = await this.db.find('digest_events', {
      digestId, type: 'click',
      'metadata.moduleId': { $exists: true },
    });

    const moduleClicks = new Map<string, number>();
    for (const click of clicks) {
      const moduleId = click.metadata.moduleId;
      moduleClicks.set(moduleId, (moduleClicks.get(moduleId) || 0) + 1);
    }

    const totalClicks = clicks.length;

    return Array.from(moduleClicks.entries()).map(([moduleId, count]) => ({
      moduleId,
      clickCount: count,
      clickShare: totalClicks > 0 ? count / totalClicks : 0,
    }));
  }

  async computeEngagementScore(userId: string): Promise<EngagementScore> {
    const recentEvents = await this.db.find('digest_events', {
      userId,
      timestamp: { $gte: daysAgo(30) },
    });

    const sentCount = recentEvents.filter(e => e.type === 'sent').length;
    const openCount = recentEvents.filter(e => e.type === 'open').length;
    const clickCount = recentEvents.filter(e => e.type === 'click').length;

    const moduleScores: Record<string, number> = {};
    const moduleClicks = recentEvents
      .filter(e => e.type === 'click' && e.metadata?.moduleId)
      .reduce((acc, e) => {
        const moduleId = e.metadata!.moduleId!;
        acc[moduleId] = (acc[moduleId] || 0) + 1;
        return acc;
      }, {} as Record<string, number>);

    for (const [moduleId, clicks] of Object.entries(moduleClicks)) {
      moduleScores[moduleId] = sentCount > 0 ? clicks / sentCount : 0;
    }

    return {
      userId,
      overallScore: sentCount > 0 ? (openCount * 0.3 + clickCount * 0.7) / sentCount : 0,
      moduleScores,
      preferredChannel: this.determinePreferredChannel(recentEvents),
      preferredTime: this.determinePreferredTime(recentEvents),
      lastEngaged: recentEvents
        .filter(e => ['open', 'click'].includes(e.type))
        .sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime())[0]?.timestamp || new Date(0),
    };
  }

  private determinePreferredChannel(events: DigestEvent[]): string {
    const channelEngagement = new Map<string, { opens: number; clicks: number }>();

    for (const event of events) {
      if (!['open', 'click'].includes(event.type)) continue;
      const current = channelEngagement.get(event.channel) || { opens: 0, clicks: 0 };
      if (event.type === 'open') current.opens++;
      if (event.type === 'click') current.clicks++;
      channelEngagement.set(event.channel, current);
    }

    let bestChannel = 'email';
    let bestScore = 0;

    for (const [channel, stats] of channelEngagement) {
      const score = stats.opens * 0.4 + stats.clicks * 0.6;
      if (score > bestScore) {
        bestScore = score;
        bestChannel = channel;
      }
    }

    return bestChannel;
  }

  private determinePreferredTime(events: DigestEvent[]): string {
    const hourCounts = new Array(24).fill(0);
    for (const event of events) {
      if (!['open', 'click'].includes(event.type)) continue;
      hourCounts[new Date(event.timestamp).getHours()]++;
    }

    const maxHour = hourCounts.indexOf(Math.max(...hourCounts));
    return `${maxHour.toString().padStart(2, '0')}:00`;
  }
}

// A/B Testing
interface ABTestConfig {
  id: string;
  name: string;
  variable: 'subject_line' | 'content_layout' | 'sending_time' | 'channel';
  variants: ABVariant[];
  trafficSplit: number[]; // e.g., [50, 50]
  minSampleSize: number;
  durationDays: number;
  metric: 'open_rate' | 'click_rate' | 'conversion_rate';
}

interface ABVariant {
  id: string;
  name: string;
  config: Record<string, unknown>;
}

class DigestABTest {
  async assignVariant(userId: string, testId: string): Promise<string> {
    // Consistent assignment based on userId hash
    const hash = crypto.createHash('md5').update(`${userId}:${testId}`).digest('hex');
    const bucket = parseInt(hash.substring(0, 8), 16) % 100;

    const test = await this.getTest(testId);
    let cumulative = 0;

    for (let i = 0; i < test.variants.length; i++) {
      cumulative += test.trafficSplit[i];
      if (bucket < cumulative) {
        return test.variants[i].id;
      }
    }

    return test.variants[0].id;
  }

  async evaluateTest(testId: string): Promise<ABTestResult> {
    const test = await this.getTest(testId);
    const results: Array<{ variantId: string; metric: number; sampleSize: number }> = [];

    for (const variant of test.variants) {
      const events = await this.db.find('digest_events', {
        'metadata.abTestId': testId,
        'metadata.variantId': variant.id,
      });

      const sent = events.filter(e => e.type === 'sent').length;
      const metricEvents = events.filter(e => e.type === test.metric.replace('_rate', ''));

      results.push({
        variantId: variant.id,
        metric: sent > 0 ? metricEvents.length / sent : 0,
        sampleSize: sent,
      });
    }

    // Determine winner
    const sorted = [...results].sort((a, b) => b.metric - a.metric);
    const winner = sorted[0];
    const isSignificant = this.isStatisticallySignificant(results, test);

    return {
      testId: test.id,
      testName: test.name,
      results,
      winner: isSignificant ? winner.variantId : null,
      isSignificant,
      confidence: isSignificant ? 0.95 : 0,
      recommendedAction: isSignificant
        ? `Roll out variant ${winner.variantId} to all users`
        : 'Continue test — insufficient data',
    };
  }

  private isStatisticallySignificant(
    results: Array<{ metric: number; sampleSize: number }>,
    test: ABTestConfig,
  ): boolean {
    // Simplified chi-squared test
    const total = results.reduce((s, r) => s + r.sampleSize, 0);
    if (total < test.minSampleSize) return false;

    const best = results[0];
    const rest = results.slice(1);
    return rest.every(r => Math.abs(best.metric - r.metric) > 0.02);
  }
}
```

## Integration Points

- **Analytics Dashboard**: Grafana or custom dashboard for digest metrics
- **Engagement Service**: User engagement scores influence content selection
- **A/B Test Framework**: Test results feed into digest optimization

## Production Considerations

- **Privacy**: Tracking opt-out option, anonymize IP addresses
- **Data Volume**: Digest events can reach millions per day — batch processing
- **Attribution Window**: Click attributed to digest within 24 hours of send
- **Statistical Rigor**: A/B tests require minimum 1000 users per variant for significance

## Open-Source Tools

- **Redis**: Real-time event counting and aggregation
- **PostgreSQL**: Persistent event storage with partitioning
- **Grafana**: Engagement metrics dashboard
- **simple-statistics**: Statistical significance testing
