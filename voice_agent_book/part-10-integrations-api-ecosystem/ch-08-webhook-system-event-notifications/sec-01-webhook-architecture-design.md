# Section 01: Webhook Architecture Design

## Overview

The webhook architecture design establishes the foundational infrastructure for sending real-time event notifications from the voice agent platform to external systems. Webhooks provide a push-based integration pattern where the platform emits events (call completed, payment received, customer identified) and registered endpoints receive those events via HTTP POST requests. The architecture must support high throughput (thousands of events per second during peak calling hours), guaranteed at-least-once delivery, payload signing for security, and observability into delivery health.

The webhook system acts as the outbound complement to the inbound integration adapters. While adapters pull data from external APIs, webhooks push platform events to external systems. The architecture is event-driven: the platform's internal event bus (emitted by the call runtime, payment engine, and analytics pipeline) feeds into the webhook delivery engine, which fans out events to all registered endpoints matching the event type. The system supports both tenant-specific webhooks (per customer) and global webhooks (platform-wide integrations).

## Architecture

```
                   Webhook Architecture

   Event Sources → Event Bus → Webhook Engine → External Systems
                                    |
   +----------------------------------------------------------+
   |              Webhook Delivery Pipeline                   |
   |                                                          |
   |  +------------------+  +-------------------+            |
   |  | Event Router     |  | Delivery Queue     |            |
   |  | • Type matching  |  | • Event enrichment |            |
   |  | • Filter rules   |  | • Fan-out per      |            |
   |  | • Rate limiting  |  |   endpoint         |            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | HTTP Dispatcher  |  | Retry Engine       |            |
   |  | • POST delivery  |  | • Exponential      |            |
   |  | • Timeout (10s)  |  |   backoff          |            |
   |  | • Response       |  | • Max 5 retries    |            |
   |  |   validation     |  | • DLQ after failure|            |
   |  +------------------+  +-------------------+            |
   |  +------------------+  +-------------------+            |
   |  | Signature        |  | Monitoring        |             |
   |  | • HMAC-SHA256    |  | • Delivery stats   |            |
   |  | • Header injection|  | • Failure tracking|            |
   |  | • Idempotency key|  | • Alerting        |             |
   |  +------------------+  +-------------------+            |
   +----------------------------------------------------------+
```

## Design Decisions

- **At-least-once delivery with idempotency over exactly-once:** Webhook events may be delivered more than once due to network retries, worker restarts, or queue replays. Each event includes an idempotency key (event ID) in the HTTP header and the payload. Consumers use the idempotency key to deduplicate. At-least-once is simpler to implement than exactly-once (which requires distributed consensus) and is acceptable for most use cases when consumers deduplicate. Trade-off: idempotency requires consumer-side deduplication but provides reliable delivery without the complexity of two-phase commit.

- **Event envelope over raw payload delivery:** Each webhook delivery wraps the event payload in a standard envelope containing the event ID, event type, event version, timestamp, tenant ID, and idempotency key. The envelope provides consumers with metadata needed for processing without parsing the payload body. Payload schemas are versioned independently of the envelope. Trade-off: envelope wrapping increases payload size slightly but provides standard metadata that all consumers can rely on.

- **Dedicated delivery queue per endpoint over shared queue:** Each registered webhook endpoint has its own delivery queue (a Redis list or RabbitMQ queue). This isolates delivery failures — a slow or failing endpoint does not block delivery to other endpoints. Fan-out from the event bus to endpoint queues is done by the webhook router with bounded concurrency. Trade-off: per-endpoint queues increase infrastructure overhead (queue count = endpoint count) but provide failure isolation and independent delivery pacing.

## Implementation Approach

```
interface WebhookEventEnvelope {
  id: string;                    // Unique event ID
  type: string;                  // e.g., "call.completed"
  version: number;               // Event schema version
  tenantId: string;
  timestamp: string;             // ISO 8601
  idempotencyKey: string;        // Same as event ID
  data: Record<string, any>;     // Event payload
}

interface WebhookEndpoint {
  id: string;
  tenantId: string;
  url: string;
  secret: string;                // HMAC signing secret
  eventTypes: string[];          // Subscribed event types
  filters?: WebhookFilter[];     // Optional payload filters
  status: 'active' | 'paused' | 'disabled';
  retryConfig: {
    maxRetries: number;
    backoffMs: number;
    timeoutMs: number;
  };
  headers?: Record<string, string>; // Custom headers
  createdAt: Date;
}

class WebhookEngine {
  private endpoints: Map<string, WebhookEndpoint>;
  private deliveryQueues: Map<string, Queue>;
  private eventBus: EventBus;

  async registerEndpoint(config: CreateEndpointRequest): Promise<WebhookEndpoint> {
    const endpoint: WebhookEndpoint = {
      id: generateId('wh'),
      tenantId: config.tenantId,
      url: config.url,
      secret: await generateSecret(),
      eventTypes: config.eventTypes,
      filters: config.filters,
      status: 'active',
      retryConfig: {
        maxRetries: config.maxRetries ?? 5,
        backoffMs: config.backoffMs ?? 1000,
        timeoutMs: config.timeoutMs ?? 10000,
      },
      headers: config.headers,
      createdAt: new Date(),
    };
    await this.db.webhookEndpoints.insert(endpoint);
    this.deliveryQueues.set(endpoint.id, this.createQueue(endpoint.id));
    return endpoint;
  }

  async emitEvent(eventType: string, data: Record<string, any>, tenantId: string): Promise<void> {
    const envelope: WebhookEventEnvelope = {
      id: generateId('evt'),
      type: eventType,
      version: this.getEventSchemaVersion(eventType),
      tenantId,
      timestamp: new Date().toISOString(),
      idempotencyKey: generateIdempotencyKey(),
      data,
    };

    // Find matching endpoints
    const matchingEndpoints = Array.from(this.endpoints.values())
      .filter(ep => ep.status === 'active')
      .filter(ep => ep.tenantId === tenantId || ep.eventTypes.includes('*'))
      .filter(ep => ep.eventTypes.some(et => matchEventType(et, eventType)))
      .filter(ep => !ep.filters || ep.filters.every(f => this.evaluateFilter(f, data)));

    // Enqueue to each endpoint's delivery queue
    await Promise.all(
      matchingEndpoints.map(ep =>
        this.deliveryQueues.get(ep.id)!.enqueue({
          envelope,
          endpointId: ep.id,
          attempt: 0,
        })
      )
    );

    logger.info(`Emitted ${eventType} to ${matchingEndpoints.length} endpoints`, {
      eventId: envelope.id,
      tenantId,
    });
  }

  async processDeliveryQueue(endpointId: string): Promise<void> {
    const endpoint = this.endpoints.get(endpointId);
    if (!endpoint) return;

    const queue = this.deliveryQueues.get(endpointId);
    if (!queue) return;

    const job = await queue.dequeue();
    if (!job) return;

    try {
      const payload = JSON.stringify(job.envelope);
      const signature = this.signPayload(payload, endpoint.secret);

      const response = await axios.post(endpoint.url, payload, {
        headers: {
          'Content-Type': 'application/json',
          'X-Webhook-Signature': signature,
          'X-Webhook-Id': job.envelope.id,
          'X-Webhook-Idempotency-Key': job.envelope.idempotencyKey,
          'X-Webhook-Timestamp': job.envelope.timestamp,
          'X-Webhook-Event-Type': job.envelope.type,
          ...endpoint.headers,
        },
        timeout: endpoint.retryConfig.timeoutMs,
        validateStatus: (status) => status < 500, // Accept 2xx, 3xx, 4xx as delivered
      });

      if (response.status >= 200 && response.status < 300) {
        logger.info(`Webhook delivered`, { eventId: job.envelope.id, endpointId, status: response.status });
        return;
      }

      // 4xx errors — consumer rejected; log and do not retry
      if (response.status >= 400 && response.status < 500) {
        logger.warn(`Webhook rejected (${response.status})`, { eventId: job.envelope.id, endpointId });
        await this.moveToDLQ(job, `Consumer rejected with ${response.status}`);
        return;
      }
    } catch (error) {
      // Network error or timeout — retry
      job.attempt++;
      if (job.attempt <= endpoint.retryConfig.maxRetries) {
        const delay = endpoint.retryConfig.backoffMs * Math.pow(2, job.attempt - 1);
        await queue.enqueue(job, { delay });
        logger.warn(`Webhook delivery failed, scheduled retry ${job.attempt}`, {
          eventId: job.envelope.id,
          endpointId,
          delay,
        });
      } else {
        await this.moveToDLQ(job, 'Max retries exceeded');
      }
    }
  }

  private signPayload(payload: string, secret: string): string {
    return crypto.createHmac('sha256', secret).update(payload).digest('hex');
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Bull/BullMQ (MIT) | Node.js | Delivery queues + retry |
| Axios (MIT) | HTTP | Webhook HTTP dispatch |
| Pino (MIT) | Logging | Event delivery audit logs |

## Production Considerations

**Scaling:** The webhook engine must handle burst events (e.g., campaign ends, 1000 calls complete simultaneously). Each endpoint queue is processed by a dedicated worker pool with configurable concurrency (default 5 concurrent deliveries per endpoint). Use a global concurrency limiter to prevent outbound HTTP from overwhelming the network. Queue length monitoring alerts on delivery backlog. Consider partitioning high-volume endpoints to separate worker processes.

**Security:** Every webhook payload is signed with an HMAC-SHA256 signature using the endpoint's secret key. Consumers verify the signature to confirm the payload originated from the platform and has not been tampered with. The webhook endpoint must be idempotent (same event ID processes once). Secrets must be encrypted at rest and never included in logs. Webhook URLs are validated against an allowlist to prevent SSRF attacks. Custom headers are sanitized to prevent header injection.

**Monitoring:** Track events emitted per second, delivery success rate, delivery latency (enqueue to delivery), retry distribution, DLQ depth, endpoint response code distribution, and endpoint health. Alert on delivery success rate below 95%, DLQ growth, endpoint failures (persistent 5xx), and delivery latency exceeding 30 seconds. Monitor webhook payload size distribution and alert if any payload exceeds 1MB.
