# Section 01: Digest Generation Engine

## Overview

The digest generation engine aggregates notifications, alerts, and reports into personalized digests delivered on a schedule. Content is selected based on user preferences, relevance scoring, and time sensitivity. The engine supports multiple formats and channels.

## Architecture

```
Digest Generation Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Content Sources] → [Aggregator] → [Templating] → [Delivery]
       │                  │              │              │
  Alerts from past    Group by        Apply user     Multi-channel
  N hours             category        template       send: email,
  Unread notificationsSeverity        Branding       in-app, Slack
  System updates      Prioritize      Personalize    SMS summary
  Custom reports      Deduplicate     Format (HTML/
                                       plain/Markdown)

Digest Content Modules:
  ┌──────────────────────────────────────────────────┐
  │ Your Daily Digest — Tue, June 10                  │
  │                                                    │
  │ 🔴 Critical Alerts (2):                            │
  │   • Call error rate exceeded threshold (12 min ago)│
  │   • API latency p99 > 500ms (25 min ago)           │
  │                                                    │
  │ 🟡 Warnings (5):                                   │
  │   • Agent response timeout on support flow         │
  │   • STT accuracy below 95% on Spanish calls        │
  │   • 3 more warnings...                             │
  │                                                    │
  │ 📊 Stats at a Glance:                              │
  │   Calls handled: 1,234  ▲ 12% from yesterday       │
  │   Avg duration: 3m 42s  ▼ 5s                       │
  │   Satisfaction: 94.2%   ▲ 0.3%                     │
  │                                                    │
  │ [View in Dashboard] [Manage Preferences]           │
  └──────────────────────────────────────────────────┘
```

## Design Decisions

- **Content Modules**: Pluggable content modules for flexible composition
- **Priority Ordering**: Critical items first, followed by warnings, then stats
- **Deduplication**: Merge repeated alerts into single digest entry
- **Personalization**: User preferences control module selection and ordering

## Implementation Approach

```typescript
interface DigestConfig {
  userId: string;
  tenantId: string;
  frequency: 'hourly' | 'daily' | 'weekly';
  channels: ('email' | 'in_app' | 'slack' | 'sms')[];
  modules: DigestModule[];
  timezone: string;
  preferredTime?: string; // HH:MM format for delivery
}

interface DigestModule {
  id: string;
  type: 'critical_alerts' | 'warnings' | 'stats' | 'reports' | 'custom';
  enabled: boolean;
  order: number;
  config?: Record<string, unknown>;
}

interface Digest {
  id: string;
  userId: string;
  tenantId: string;
  generatedAt: Date;
  period: { start: Date; end: Date };
  modules: DigestModuleContent[];
  metadata: {
    totalItems: number;
    criticalCount: number;
    warningCount: number;
    template: string;
  };
}

interface DigestModuleContent {
  moduleId: string;
  title: string;
  priority: 'critical' | 'warning' | 'info';
  items: DigestItem[];
}

interface DigestItem {
  id: string;
  title: string;
  description?: string;
  severity: string;
  timestamp: Date;
  link?: string;
  metadata?: Record<string, unknown>;
}

class DigestGenerator {
  async generate(config: DigestConfig): Promise<Digest> {
    const period = this.computePeriod(config.frequency);

    const moduleContents = await Promise.all(
      config.modules
        .filter(m => m.enabled)
        .sort((a, b) => a.order - b.order)
        .map(module => this.generateModule(module, config, period))
    );

    const allItems = moduleContents.flatMap(m => m.items);

    return {
      id: crypto.randomUUID(),
      userId: config.userId,
      tenantId: config.tenantId,
      generatedAt: new Date(),
      period,
      modules: moduleContents,
      metadata: {
        totalItems: allItems.length,
        criticalCount: allItems.filter(i => i.severity === 'critical').length,
        warningCount: allItems.filter(i => i.severity === 'warning').length,
        template: 'default',
      },
    };
  }

  private async generateModule(
    module: DigestModule,
    config: DigestConfig,
    period: { start: Date; end: Date },
  ): Promise<DigestModuleContent> {
    switch (module.type) {
      case 'critical_alerts':
        return this.generateCriticalAlerts(config, period);
      case 'warnings':
        return this.generateWarnings(config, period);
      case 'stats':
        return this.generateStats(config, period);
      case 'reports':
        return this.generateReports(config, period, module.config);
      default:
        return { moduleId: module.id, title: 'Unknown', priority: 'info', items: [] };
    }
  }

  private async generateCriticalAlerts(
    config: DigestConfig,
    period: { start: Date; end: Date },
  ): Promise<DigestModuleContent> {
    const alerts = await this.alertService.getAlerts(config.tenantId, {
      severity: 'critical',
      startDate: period.start,
      endDate: period.end,
      status: 'fired',
    });

    return {
      moduleId: 'critical_alerts',
      title: `Critical Alerts (${alerts.length})`,
      priority: 'critical',
      items: alerts.slice(0, 10).map(a => ({
        id: a.id,
        title: a.title,
        description: a.description,
        severity: 'critical',
        timestamp: a.createdAt,
        link: `/alerts/${a.id}`,
        metadata: { metric: a.metric, value: a.value },
      })),
    };
  }

  private async generateStats(
    config: DigestConfig,
    period: { start: Date; end: Date },
  ): Promise<DigestModuleContent> {
    const stats = await this.statsService.getStats(config.tenantId, period);

    return {
      moduleId: 'stats',
      title: 'Stats at a Glance',
      priority: 'info',
      items: [
        {
          id: 'calls',
          title: `Calls handled: ${stats.calls} ${this.formatTrend(stats.callTrend)}`,
          severity: 'info',
          timestamp: new Date(),
        },
        {
          id: 'duration',
          title: `Avg duration: ${stats.avgDuration} ${this.formatTrend(stats.durationTrend)}`,
          severity: 'info',
          timestamp: new Date(),
        },
        {
          id: 'satisfaction',
          title: `Satisfaction: ${stats.satisfaction}% ${this.formatTrend(stats.satisfactionTrend)}`,
          severity: 'info',
          timestamp: new Date(),
        },
      ],
    };
  }

  private formatTrend(trend: number): string {
    if (trend > 0) return `▲ ${Math.abs(trend)}%`;
    if (trend < 0) return `▼ ${Math.abs(trend)}%`;
    return '—';
  }

  private computePeriod(frequency: string): { start: Date; end: Date } {
    const end = new Date();
    const start = new Date();

    switch (frequency) {
      case 'hourly':
        start.setHours(start.getHours() - 1);
        break;
      case 'daily':
        start.setDate(start.getDate() - 1);
        break;
      case 'weekly':
        start.setDate(start.getDate() - 7);
        break;
    }

    return { start, end };
  }

  async prioritizeItems(items: DigestItem[]): Promise<DigestItem[]> {
    const severityOrder = { critical: 0, warning: 1, info: 2 };
    return items.sort((a, b) => {
      const sevDiff = severityOrder[a.severity] - severityOrder[b.severity];
      if (sevDiff !== 0) return sevDiff;
      return b.timestamp.getTime() - a.timestamp.getTime();
    });
  }
}
```

## Integration Points

- **Alert Service**: Sources for critical alerts and warnings
- **Analytics Service**: Statistics and metrics for digest stats module
- **Delivery Service**: Sends generated digest via configured channels

## Production Considerations

- **Generation Window**: Digests generated in off-peak hours for scheduled delivery
- **Content Limits**: Maximum 50 items per digest to prevent overload
- **Partial Failure**: One failed module doesn't prevent digest generation
- **Cache**: Frequently accessed stats cached for performance

## Open-Source Tools

- **Handlebars**: Template engine for digest rendering
- **BullMQ**: Scheduled job queue for digest generation
