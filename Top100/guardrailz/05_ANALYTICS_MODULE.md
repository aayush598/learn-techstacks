# Analytics Module

The analytics module implements a simple **Event Sourcing / CQRS** pattern for tracking guardrail executions, usage, and performance metrics.

---

## Architecture

```
analytics/
├── domain/
│   ├── analytics-event.ts       # AnalyticsEvent interface
│   ├── analytics-dimensions.ts  # AnalyticsDimensions
│   ├── analytics-metrics.ts     # AnalyticsMetrics
│   ├── analytics-query.ts       # AnalyticsQuery
│   └── analytics-read-model.ts  # AnalyticsReadModel (dashboard response)
├── events/
│   ├── guardrail-executed.event.ts  # GUARDRAIL_EXECUTED_EVENT
│   ├── profile-used.event.ts        # PROFILE_USED_EVENT
│   └── rate-limit-hit.event.ts      # RATE_LIMIT_HIT_EVENT
├── ingestion/
│   └── analytics-ingestor.ts    # Event ingestion
├── mappers/
│   └── analytics.mapper.ts      # Row → Domain mapper
├── queries/
│   ├── usage.query.ts           # Usage stats query
│   └── guardrail-performance.query.ts  # Performance query
├── repository/
│   ├── analytics-row.ts         # DB row type
│   └── analytics.repository.ts  # Insert event
├── service/
│   ├── analytics.service.ts     # Write-side service
│   └── analytics-query.service.ts # Read-side service
├── utils/
│   └── type-guards.ts           # Event type guards
└── index.ts                     # Exports
```

---

## Domain Events

Three event types are defined:

### 1. Guardrail Executed Event
```typescript
export const GUARDRAIL_EXECUTED_EVENT = 'guardrail.executed';

export interface GuardrailExecutedPayload {
  guardrailName: string;
  passed: boolean;
  severity: string;
  executionTimeMs: number;
}
```
Tracks every guardrail execution.

### 2. Profile Used Event
```typescript
export const PROFILE_USED_EVENT = 'profile.used';

export interface ProfileUsedPayload {
  profileName: string;
  validationType: 'input' | 'output' | 'tool';
}
```
Tracks which profiles are being used.

### 3. Rate Limit Hit Event
```typescript
export const RATE_LIMIT_HIT_EVENT = 'rate_limit.hit';

export interface RateLimitHitPayload {
  limitType: 'minute' | 'day';
  current: number;
  max: number;
}
```
Tracks rate limit violations.

---

## Ingestion Pipeline

```typescript
class AnalyticsIngestor {
  async ingest<TPayload>(eventType: string, event: IngestEventInput<TPayload>) {
    // 1. Create AnalyticsEvent with UUID, timestamp
    // 2. Insert via AnalyticsRepository into analytics_events table
  }
}
```

The `AnalyticsService` wraps the ingestor with specific track methods:
```typescript
class AnalyticsService {
  async trackGuardrailExecution(params: {
    userId: string;
    apiKeyId?: string;
    profileId?: string;
    payload: GuardrailExecutedPayload;
  })
}
```

---

## Read Model

```typescript
interface AnalyticsReadModel {
  overview: AnalyticsOverview;     // totals, pass/fail, avg time, success rate
  hourlyDistribution: HourlyDistribution[];  // hourly breakdown
  guardrailStats: GuardrailStat[];  // per-guardrail stats
  profileStats: ProfileStat[];      // per-profile stats
  topErrors: string[];              // most common errors
}
```

The `AnalyticsQueryService.getDashboardAnalytics()` currently computes a simplified version with only the overview (hourly, guardrailStats, profileStats, topErrors are empty arrays).

---

## Queries

Two query functions:
1. `getUsageStats(query: AnalyticsQuery)`: Fetches events by userId + date range
2. `getGuardrailPerformance(userId: string)`: Fetches guardrail.executed events

---

## Type Guards
```typescript
export function isGuardrailExecutedEvent(
  event: AnalyticsEvent<unknown>
): event is AnalyticsEvent<GuardrailExecutedPayload> {
  return event.eventType === GUARDRAIL_EXECUTED_EVENT;
}
```

Used to filter events by type.

---

## Enhancements for Analytics

1. **Full CQRS separation**: Separate read/write databases
2. **Real-time analytics**: WebSocket-based streaming
3. **Time-series optimization**: Use TimescaleDB or similar for time-based queries
4. **Pre-aggregation**: Materialized views for common queries
5. **Alerting**: Threshold-based alerts for anomaly detection
6. **Export functionality**: CSV/JSON export of analytics data
7. **Custom dashboards**: User-configurable dashboard widgets
8. **Cost analytics**: Track estimated cost per guardrail execution
9. **Retention policies**: Event data lifecycle management
10. **Anomaly detection**: ML-based detection of unusual guardrail behavior patterns
