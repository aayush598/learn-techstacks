# Section 08: Monitoring & Observability Stack

## Observability Architecture

The platform implements the **three pillars of observability** — metrics, logs, and traces — using a fully open-source stack. Every component emits structured telemetry data that flows into a centralized observability pipeline.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      OBSERVABILITY STACK                               │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐     │
│  │                    TELEMETRY GENERATION                        │     │
│  │                                                                  │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │     │
│  │  │ Next.js  │  │  Micro   │  │  Media   │  │Databases │        │     │
│  │  │ App      │  │ Services │  │  Server  │  │ & Queues │        │     │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘        │     │
│  │       │              │              │              │             │     │
│  │  ┌────┴──────────────┴──────────────┴──────────────┴────────┐    │     │
│  │  │              OpenTelemetry Collector                     │    │     │
│  │  │  (OTLP receiver → processors → exporters)                │    │     │
│  │  └────┬──────────────────────┬──────────────────────┬───────┘    │     │
│  └───────┼──────────────────────┼──────────────────────┼────────────┘     │
│          │                      │                      │                 │
│  ┌───────┴──────────┐  ┌───────┴──────────┐  ┌───────┴──────────┐     │
│  │    Prometheus    │  │       Loki       │  │      Tempo       │     │
│  │    (Metrics)     │  │      (Logs)      │  │     (Traces)     │     │
│  │  ┌────────────┐  │  │  ┌────────────┐  │  │  ┌────────────┐  │     │
│  │  │ Metrics    │  │  │  │ Structured │  │  │  │ Distributed│  │     │
│  │  │ Collection │  │  │  │ Logs (JSON)│  │  │  │ Traces     │  │     │
│  │  │ Alerting   │  │  │  │ LogQL     │  │  │  │ Span       │  │     │
│  │  │ Recording  │  │  │  │ Retention │  │  │  │ Queries    │  │     │
│  │  │ Rules      │  │  │  │           │  │  │  │           │  │     │
│  │  └────────────┘  │  │  └────────────┘  │  │  └────────────┘  │     │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘     │
│          │                      │                      │                 │
│  ┌───────┴──────────────────────┴──────────────────────┴───────────┐     │
│  │                          Grafana                               │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │     │
│  │  │Dashboards│  │  Alerts  │  │ Explore  │  │  Incidents│       │     │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │     │
│  └─────────────────────────────────────────────────────────────────┘     │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐     │
│  │                  NOTIFICATIONS & INCIDENT MGMT                  │     │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │     │
│  │  │ PagerDuty│  │  Slack   │  │  Email   │  │  Webhook │        │     │
│  │  │ /Opsgenie│  │          │  │          │  │          │        │     │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │     │
│  └─────────────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────────┘
```

## Metrics (Prometheus)

Prometheus collects metrics from all services via pull-based scraping:

```typescript
// Application metrics definition
interface AppMetrics {
  // HTTP metrics
  'http_requests_total': Counter
  'http_request_duration_seconds': Histogram
  'http_requests_in_flight': Gauge

  // Call metrics
  'calls_total': Counter
  'calls_active': Gauge
  'calls_duration_seconds': Histogram
  'calls_by_status': Counter

  // Voice pipeline metrics
  'voice_pipeline_latency_ms': Histogram    // Per component
  'voice_stt_tokens_per_second': Gauge
  'voice_audio_jitter_ms': Gauge
  'voice_packet_loss_percent': Gauge

  // AI metrics
  'ai_llm_latency_ms': Histogram
  'ai_tokens_used_total': Counter
  'ai_tokens_per_call': Histogram
  'ai_model_calls_total': Counter

  // Business metrics
  'api_requests_by_tenant': Counter
  'api_requests_by_endpoint': Counter
  'active_tenants': Gauge
  'usage_minutes_total': Counter
}

// Prometheus metric registration
import prometheus from 'prom-client'

const callCounter = new prometheus.Counter({
  name: 'calls_total',
  help: 'Total number of calls',
  labelNames: ['tenant_id', 'status', 'agent_id']
})

const httpDuration = new prometheus.Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration in seconds',
  labelNames: ['method', 'route', 'status'],
  buckets: [0.01, 0.05, 0.1, 0.2, 0.5, 1, 2, 5]
})

const activeCalls = new prometheus.Gauge({
  name: 'calls_active',
  help: 'Currently active calls',
  labelNames: ['tenant_id']
})

// In middleware
export function metricsMiddleware(req: NextRequest, res: NextResponse) {
  const end = httpDuration.startTimer()
  res.on('finish', () => {
    end({ method: req.method, route: req.nextUrl.pathname, status: res.status })
    if (req.nextUrl.pathname.startsWith('/api/v1/calls')) {
      callCounter.inc({ tenant_id: req.headers.get('x-tenant-id'), status: res.status.toString() })
    }
  })
}
```

## Structured Logging (Pino + Loki)

All services emit structured JSON logs that are collected by Loki:

```typescript
// Pino logger setup
import pino from 'pino'
import { LokiTransport } from 'winston-loki'
// Using pino-loki transport
import pinoLoki from 'pino-loki'

const logger = pino({
  level: process.env.LOG_LEVEL ?? 'info',
  formatters: {
    level: (label) => ({ level: label }),
    bindings: (bindings) => ({
      pid: bindings.pid,
      host: bindings.hostname,
      service: process.env.SERVICE_NAME ?? 'unknown'
    })
  },
  serializers: {
    err: pino.stdSerializers.err,
    req: pino.stdSerializers.req,
    res: pino.stdSerializers.res
  },
  transport: {
    target: 'pino-loki',
    options: {
      host: process.env.LOKI_URL ?? 'http://loki:3100',
      labels: { 
        service: process.env.SERVICE_NAME,
        environment: process.env.NODE_ENV
      }
    }
  }
})

// Structured log example
logger.info({
  event: 'call.started',
  callId: '550e8400-e29b-41d4-a716-446655440000',
  tenantId: 'tenant_abc123',
  agentId: 'agent_456',
  from: '+14155551234',
  to: '+14155555678',
  direction: 'inbound',
  duration: 0
}, 'Call started')

// Error logging
try {
  await processCall(callId)
} catch (err) {
  logger.error({
    err,
    callId,
    event: 'call.processing_error',
    context: { component: 'voice-pipeline', stage: 'stt' }
  }, 'Failed to process call')
}
```

## Distributed Tracing (OpenTelemetry)

OpenTelemetry provides end-to-end tracing across services:

```typescript
// OpenTelemetry setup
import { NodeSDK } from '@opentelemetry/sdk-node'
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http'
import { BatchSpanProcessor } from '@opentelemetry/sdk-trace-base'
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node'
import { Resource } from '@opentelemetry/resources'
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions'

const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: process.env.SERVICE_NAME,
    [SemanticResourceAttributes.SERVICE_VERSION]: process.env.APP_VERSION
  }),
  spanProcessor: new BatchSpanProcessor(new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT ?? 'http://tempo:4318/v1/traces'
  })),
  instrumentations: [getNodeAutoInstrumentations()]
})

sdk.start()

// Manual tracing in application code
import { trace, Span } from '@opentelemetry/api'

const tracer = trace.getTracer('voice-pipeline')

async function processAudioChunk(chunk: AudioChunk): Promise<STTResult> {
  return tracer.startActiveSpan('voice.stt.process', async (span: Span) => {
    span.setAttribute('chunk.size', chunk.byteLength)
    span.setAttribute('chunk.duration_ms', chunk.durationMs)

    try {
      const result = await sttModel.transcribe(chunk)
      span.setAttribute('stt.text_length', result.text.length)
      span.setAttribute('stt.confidence', result.confidence)
      span.setAttribute('stt.latency_ms', result.latencyMs)
      span.setStatus({ code: SpanStatusCode.OK })
      return result
    } catch (err) {
      span.setStatus({ 
        code: SpanStatusCode.ERROR, 
        message: (err as Error).message 
      })
      throw err
    } finally {
      span.end()
    }
  })
}
```

## Dashboards (Grafana)

Key dashboards for operational visibility:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      CALL OPERATIONS DASHBOARD                         │
├─────────────────────────────────────────────────────────────────────────┤
│  Active Calls: 42   |   Avg Duration: 4m32s   |   Success Rate: 95.2%  │
│  STT Latency: 287ms  |   AI Latency: 412ms     |   TTS Latency: 186ms  │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────┐  ┌─────────────────────────────────────┐  │
│  │   Active Calls (24h)    │  │   Call Duration Distribution       │  │
│  │   [line chart]          │  │   [histogram]                      │  │
│  └─────────────────────────┘  └─────────────────────────────────────┘  │
│  ┌─────────────────────────┐  ┌─────────────────────────────────────┐  │
│  │   Pipeline Latency      │  │   Error Rate by Service            │  │
│  │   [stacked area]        │  │   [bar chart]                      │  │
│  └─────────────────────────┘  └─────────────────────────────────────┘  │
│  ┌─────────────────────────┐  ┌─────────────────────────────────────┐  │
│  │   Top Agents by Calls   │  │   Cost per Call                    │  │
│  │   [table]               │  │   [scatter plot]                   │  │
│  └─────────────────────────┘  └─────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

## Alerting Rules

```yaml
# Prometheus alerting rules
groups:
  - name: voice-platform
    rules:
      - alert: HighCallFailureRate
        expr: rate(calls_total{status="failed"}[5m]) / rate(calls_total[5m]) > 0.05
        for: 5m
        annotations:
          summary: "Call failure rate is above 5%"
          description: "Current failure rate: {{ $value | humanizePercentage }}"

      - alert: HighPipelineLatency
        expr: histogram_quantile(0.95, rate(voice_pipeline_latency_ms_bucket[5m])) > 2000
        for: 2m
        annotations:
          summary: "Voice pipeline P95 latency exceeds 2 seconds"
          description: "Current P95 latency: {{ $value }}ms"

      - alert: NoMediaServersAvailable
        expr: up{job="media-server"} == 0
        for: 30s
        annotations:
          summary: "No media servers are available"
          description: "All media server instances are down"

      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.01
        for: 5m
        annotations:
          summary: "API error rate above 1%"
          description: "Service {{ $labels.service }} has {{ $value | humanizePercentage }} error rate"

      - alert: DiskSpaceLow
        expr: node_filesystem_avail_bytes{mountpoint="/data"} / node_filesystem_size_bytes{mountpoint="/data"} < 0.1
        for: 5m
        annotations:
          summary: "Disk space below 10% on data volume"
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Metrics | Prometheus + Grafana | Open-source, Kubernetes-native, extensive ecosystem |
| Logging | Pino → Loki | Structured JSON logs, low overhead, Grafana integration |
| Tracing | OpenTelemetry → Tempo | Vendor-neutral, distributed context propagation |
| Alerting | Grafana Alerts | Unified alert management, silence routing, notification channels |
| Health Checks | Kubernetes probes + custom | Both platform-level and application-level health |

## Integration Points

- **Part 23 (DevOps/CI-CD)** — Observability stack deployed alongside application
- **Part 24 (Scaling)** — Metrics drive auto-scaling decisions
- **Part 19 (Testing)** — Traces help debug test failures in CI
- **Part 25 (Production Launch)** — Dashboards used for launch monitoring

## Production Considerations

- **Retention Policy**: Metrics: 30 days (raw), 12 months (aggregated); Logs: 7 days (all), 30 days (errors); Traces: 14 days
- **Storage Costs**: Monitor Prometheus TSDB size, Loki log volume, Tempo trace volume. Set retention limits.
- **Sampling**: Head-based sampling for traces (10% for normal, 100% for errors)
- **Cardinality Limits**: Prevent metric label cardinality explosion — review before deploying new metrics
- **SLO Tracking**: Track service-level objectives (uptime, latency, error rate) as Prometheus recording rules
- **On-Call Rotation**: Integrate with PagerDuty/Opsgenie for critical alerts, Slack for warnings
