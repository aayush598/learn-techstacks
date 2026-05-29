# Section 04: Delivery Logs & Monitoring

## Overview

Every webhook delivery attempt is logged with detailed metadata for monitoring and debugging. Delivery logs track status codes, latency, error messages, and retry history. Dashboards provide real-time visibility into delivery health, failure patterns, and endpoint performance.

## Architecture

```
Delivery Logging Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Delivery Attempt] → [Log Writer] → [Storage] → [Monitoring]
       │                   │              │            │
  Event details         Structured      PostgreSQL   Grafana
  Endpoint URL          log entry       + S3         dashboard
  Status code           (JSON)          archive      Alerts
  Latency                                  │
  Error message                      Logs retained
  Attempt number                        for 90 days
  Timestamp                              (hot storage)
                                       1 year (cold)

Dashboard Metrics:
  ┌──────────────────────────────────────────────────┐
  │ Webhook Delivery Health                           │
  │                                                    │
  │ Delivery Rate: 98.7% ▲ 2.3% this week              │
  │ Active Endpoints: 42  •  Failing: 3                │
  │                                                    │
  │ Latency (p50/p95/p99): 120ms / 450ms / 1200ms      │
  │                                                    │
  │ Failed by Status:                                   │
  │ 500: ████████ 65%  (server errors)                 │
  │ 408: ████ 20%   (timeout)                          │
  │ 429: ██ 10%    (rate limited)                      │
  │ 4xx: ██ 5%     (bad request)                       │
  │                                                    │
  │ [View Logs] [View Failed] [Retry All Failed]      │
  └──────────────────────────────────────────────────┘
```

## Design Decisions

- **Structured Logging**: JSON logs with consistent schema
- **Separate Index**: Logs stored in dedicated table for query performance
- **Retry History**: Array of all attempts per event
- **Log Archival**: Hot storage for 90 days, cold storage for 1 year

## Implementation Approach

```typescript
interface DeliveryLog {
  id: string;
  eventId: string;
  eventType: string;
  endpointId: string;
  endpointUrl: string;
  tenantId: string;
  status: 'success' | 'failed' | 'retrying';
  statusCode?: number;
  latencyMs: number;
  attemptNumber: number;
  maxRetries: number;
  errorMessage?: string;
  responseBody?: string;
  requestHeaders?: Record<string, string>;
  responseHeaders?: Record<string, string>;
  timestamp: Date;
}

class DeliveryLogger {
  async logAttempt(attempt: DeliveryAttemptData): Promise<void> {
    const log: DeliveryLog = {
      id: crypto.randomUUID(),
      eventId: attempt.event.id,
      eventType: attempt.event.type,
      endpointId: attempt.endpoint.id,
      endpointUrl: attempt.endpoint.url,
      tenantId: attempt.event.tenantId,
      status: attempt.status,
      statusCode: attempt.statusCode,
      latencyMs: attempt.durationMs,
      attemptNumber: attempt.attemptNumber,
      maxRetries: attempt.maxRetries,
      errorMessage: attempt.error?.message,
      responseBody: this.truncateBody(attempt.responseBody),
      requestHeaders: {
        'X-Webhook-ID': attempt.event.id,
        'X-Delivery-Attempt': String(attempt.attemptNumber),
      },
      responseHeaders: attempt.responseHeaders,
      timestamp: new Date(),
    };

    await Promise.all([
      this.insertLog(log),
      this.updateMetrics(log),
    ]);
  }

  private truncateBody(body?: string): string | undefined {
    if (!body) return undefined;
    return body.length > 1000 ? body.substring(0, 1000) + '...' : body;
  }

  private async updateMetrics(log: DeliveryLog): Promise<void> {
    const hour = new Date(log.timestamp).setMinutes(0, 0, 0);

    await this.db.upsert('webhook_metrics_hourly', {
      hour: new Date(hour),
      endpointId: log.endpointId,
    }, {
      $inc: {
        totalDeliveries: 1,
        successfulDeliveries: log.status === 'success' ? 1 : 0,
        failedDeliveries: log.status === 'failed' ? 1 : 0,
        totalLatencyMs: log.latencyMs,
      },
      $max: {
        maxLatencyMs: log.latencyMs,
      },
    });
  }

  async queryLogs(filters: LogQuery): Promise<{ logs: DeliveryLog[]; total: number }> {
    const query: any = {};

    if (filters.endpointId) query.endpointId = filters.endpointId;
    if (filters.eventType) query.eventType = filters.eventType;
    if (filters.status) query.status = filters.status;
    if (filters.statusCode) query.statusCode = filters.statusCode;
    if (filters.startDate || filters.endDate) {
      query.timestamp = {};
      if (filters.startDate) query.timestamp.$gte = new Date(filters.startDate);
      if (filters.endDate) query.timestamp.$lte = new Date(filters.endDate);
    }

    const [logs, total] = await Promise.all([
      this.db.find('webhook_delivery_logs', query, {
        sort: { timestamp: -1 },
        limit: filters.limit || 50,
        offset: filters.offset || 0,
      }),
      this.db.count('webhook_delivery_logs', query),
    ]);

    return { logs: logs as DeliveryLog[], total };
  }

  async getEndpointHealth(endpointId: string): Promise<EndpointHealth> {
    const last24h = new Date(Date.now() - 24 * 60 * 60 * 1000);

    const recentAttempts = await this.db.find('webhook_delivery_logs', {
      endpointId,
      timestamp: { $gte: last24h },
    });

    const total = recentAttempts.length;
    const successful = recentAttempts.filter(l => l.status === 'success').length;
    const failed = recentAttempts.filter(l => l.status === 'failed').length;
    const latencies = recentAttempts.filter(l => l.latencyMs != null).map(l => l.latencyMs);
    const sorted = [...latencies].sort((a, b) => a - b);

    return {
      endpointId,
      totalDeliveries: total,
      successRate: total > 0 ? successful / total : 0,
      failedCount: failed,
      averageLatencyMs: latencies.length > 0
        ? latencies.reduce((s, l) => s + l, 0) / latencies.length
        : 0,
      p95LatencyMs: sorted[Math.floor(sorted.length * 0.95)] || 0,
      recentErrors: recentAttempts
        .filter(l => l.status === 'failed')
        .slice(0, 5)
        .map(l => ({ time: l.timestamp, error: l.errorMessage, code: l.statusCode })),
    };
  }
}
```

## Integration Points

- **Grafana**: Real-time dashboards from PostgreSQL metrics
- **Alert System**: Health degradation triggers notifications
- **Developer Portal**: Endpoint-level delivery logs for users

## Production Considerations

- **Log Volume**: At scale, 1000+ logs/second — use batch inserts
- **Log Retention**: 90 days hot storage, 1 year cold archive
- **PII Redaction**: Strip sensitive data from logged payloads
- **Index Strategy**: Index on (endpointId, timestamp) for common queries

## Open-Source Tools

- **Pino**: Structured JSON logging
- **Grafana**: Delivery health dashboards
- **pg_partman**: PostgreSQL table partitioning for log retention
