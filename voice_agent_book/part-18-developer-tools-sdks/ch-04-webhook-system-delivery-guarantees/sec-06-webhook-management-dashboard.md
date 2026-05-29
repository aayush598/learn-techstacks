# Section 06: Webhook Management Dashboard

## Overview

The webhook management dashboard allows developers to configure endpoints, view delivery logs, inspect retry history, and test webhook delivery. It provides visibility into the webhook delivery pipeline — success rates, latency percentiles, and failure reasons — enabling operators to diagnose and resolve delivery issues.

## Architecture

```
Dashboard Structure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Webhook Management Dashboard
├── Endpoints
│   ├── List all endpoints
│   ├── Create/Edit endpoint
│   │   ├── URL
│   │   ├── Secret (auto-generated)
│   │   ├── Event types to subscribe
│   │   ├── Rate limit config
│   │   └── Retry config
│   └── Test endpoint
│       ├── Send test event
│       └── View delivery result
├── Delivery Logs
│   ├── Real-time delivery stream
│   ├── Search by event/endpoint
│   ├── Status filter (success/failed/pending)
│   └── Detail view per delivery
│       ├── Request/response headers
│       ├── Request/response body
│       ├── Latency breakdown
│       └── Retry timeline
├── Dead Letter Queue
│   ├── List failed events
│   ├── Inspect payload
│   ├── Replay individual/bulk
│   └── Discard
└── Analytics
    ├── Success rate (24h/7d/30d)
    ├── Latency p50/p95/p99
    ├── Event type breakdown
    └── Failure reasons pie chart
```

## Design Decisions

- **Real-Time Delivery Feed**: Server-Sent Events stream deliveries as they happen — no page refresh needed
- **Search-Enabled Logs**: Full-text search across event IDs, endpoint URLs, and error messages
- **Request/Response Capture**: Full HTTP request and response stored for debugging (headers, body, timing)
- **Analytics Dashboard**: Aggregate metrics for health monitoring and trend analysis

## Implementation Approach

```typescript
// Dashboard API endpoints
interface WebhookDashboardRouter {
  // Endpoints CRUD
  'GET    /webhooks/endpoints': ListEndpointsResponse;
  'POST   /webhooks/endpoints': CreateEndpointRequest;
  'GET    /webhooks/endpoints/:id': EndpointDetail;
  'PATCH  /webhooks/endpoints/:id': UpdateEndpointRequest;
  'DELETE /webhooks/endpoints/:id': void;
  'POST   /webhooks/endpoints/:id/test': TestDeliveryResponse;

  // Delivery logs
  'GET    /webhooks/deliveries': PaginatedDeliveries;
  'GET    /webhooks/deliveries/:id': DeliveryDetail;
  'GET    /webhooks/deliveries/stream': EventStream<DeliveryEvent>;

  // Dead letter queue
  'GET    /webhooks/dlq': DeadLetterList;
  'GET    /webhooks/dlq/:id': DeadLetterDetail;
  'POST   /webhooks/dlq/:id/replay': void;
  'POST   /webhooks/dlq/bulk-replay': void;
  'POST   /webhooks/dlq/:id/discard': void;

  // Analytics
  'GET    /webhooks/analytics/summary': AnalyticsSummary;
  'GET    /webhooks/analytics/events-by-type': EventTypeBreakdown;
  'GET    /webhooks/analytics/failure-reasons': FailureReasonBreakdown;
}

// Delivery log service
interface DeliveryLog {
  id: string;
  eventId: string;
  eventType: string;
  endpointId: string;
  endpointUrl: string;
  status: 'success' | 'failed' | 'pending' | 'retrying';
  attempt: number;
  requestHeaders: Record<string, string>;
  requestBody: string;
  responseStatus?: number;
  responseHeaders?: Record<string, string>;
  responseBody?: string;
  latencyMs?: number;
  error?: string;
  createdAt: Date;
}

class WebhookDashboardService {
  constructor(
    private db: Database,
    private deliveryLogs: DeliveryLogRepository,
  ) {}

  async getDeliveryDetail(deliveryId: string): Promise<DeliveryDetail> {
    const log = await this.deliveryLogs.findById(deliveryId);
    if (!log) throw new NotFoundError('Delivery log', deliveryId);

    // Get retry chain
    const siblings = await this.deliveryLogs.findByEventId(log.eventId);

    return {
      ...log,
      retryTimeline: siblings.map(s => ({
        attempt: s.attempt,
        timestamp: s.createdAt,
        status: s.status,
        latencyMs: s.latencyMs,
      })),
    };
  }

  async getAnalyticsSummary(endpointId: string, period: '24h' | '7d' | '30d'): Promise<AnalyticsSummary> {
    const since = this.getPeriodStart(period);
    const logs = await this.deliveryLogs.findByEndpointSince(endpointId, since);

    const total = logs.length;
    const success = logs.filter(l => l.status === 'success').length;
    const latencies = logs.filter(l => l.latencyMs != null).map(l => l.latencyMs!);

    return {
      total,
      success,
      failed: total - success,
      successRate: total > 0 ? (success / total) * 100 : 100,
      latency: {
        p50: this.percentile(latencies, 50),
        p95: this.percentile(latencies, 95),
        p99: this.percentile(latencies, 99),
      },
      period,
    };
  }

  async testEndpoint(endpointId: string): Promise<TestDeliveryResponse> {
    const endpoint = await this.getEndpoint(endpointId);

    // Generate test event
    const testEvent = {
      type: 'webhook.test',
      version: 1,
      id: `test_${crypto.randomUUID()}`,
      timestamp: new Date().toISOString(),
      topic: 'webhook',
      data: { message: 'This is a test webhook delivery' },
    };

    // Attempt delivery
    const startTime = Date.now();
    try {
      const response = await fetch(endpoint.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-VoiceAgent-Signature': 'test_skip_verification',
          'X-VoiceAgent-Timestamp': Math.floor(Date.now() / 1000).toString(),
          'X-VoiceAgent-Event-Id': testEvent.id,
          'X-VoiceAgent-Delivery-Attempt': '1',
        },
        body: JSON.stringify(testEvent),
      });

      return {
        success: response.ok,
        statusCode: response.status,
        latencyMs: Date.now() - startTime,
        responseBody: await response.text(),
        eventId: testEvent.id,
      };
    } catch (error) {
      return {
        success: false,
        statusCode: 0,
        latencyMs: Date.now() - startTime,
        error: (error as Error).message,
        eventId: testEvent.id,
      };
    }
  }
}
```

## Integration Points

- **Developer Portal**: Webhook management as part of developer dashboard
- **Event Stream**: Real-time delivery updates via WebSocket or SSE
- **Analytics Pipeline**: Delivery metrics fed into monitoring dashboards

## Production Considerations

- **Log Retention**: Delivery logs retained for 30 days; aggregated analytics retained for 1 year
- **Rate Limits on Dashboard**: Dashboard API rate-limited to prevent excessive queries
- **Export Capability**: Download delivery logs as CSV or JSON for external analysis
- **Multi-Tenant Isolation**: Dashboard scoped to authenticated tenant — no cross-tenant visibility

## Open-Source Tools

- **React Admin**: Build dashboard UI with pre-built components
- **Chart.js / Recharts**: Analytics visualization for success rates and latency
