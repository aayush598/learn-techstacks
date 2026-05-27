# Section 02: Metering Data Model

## Usage Records Schema

The usage record schema captures every dimension of a billable event. Each record is immutable once written, and the schema must support flexible meter definitions, multiple unit types, and rich metadata for auditing and debugging.

```typescript
interface UsageRecord {
  id: string;
  idempotencyKey: string;
  tenantId: string;
  subscriptionId?: string;
  meterId: string;
  eventType: string;

  // Quantities
  quantity: number;
  unit: 'minutes' | 'seconds' | 'characters' | 'requests' | 'bytes' | 'count';

  // Timing
  eventTimestamp: string;    // When the usage occurred
  ingestedAt: string;        // When we received the event
  billingPeriodStart?: string;
  billingPeriodEnd?: string;

  // Attribution
  source: string;            // Which service emitted this
  userId?: string;
  agentId?: string;
  callId?: string;

  // Audit
  metadata: Record<string, string>;
  checksum: string;          // For data integrity verification
}

interface MeterDefinition {
  id: string;
  name: string;
  description: string;
  aggregationType: 'sum' | 'max' | 'unique_count' | 'rate';
  unit: string;
  billingModel: 'included' | 'metered' | 'prepaid';
  resetPeriod: 'hourly' | 'daily' | 'monthly' | 'yearly' | 'never';
  tiers?: MeterTier[];
}

interface MeterTier {
  upTo: number;
  rate: number;
  label: string;
}
```

## Meter Definition

Meters are the fundamental unit of billing. Each meter tracks a specific type of consumption. Meters can be standalone (e.g., monthly_minutes) or composite (e.g., total_processing_time = transcription + TTS).

```
Meter Catalog:
┌──────────────────────────────────────────────────────────────────┐
│ Meter ID            │ Type    │ Unit    │ Aggregation │ Reset   │
├──────────────────────┼─────────┼─────────┼─────────────┼─────────┤
│ monthly_minutes     │ core    │ minutes │ sum         │ monthly │
│ transcription_hours │ core    │ hours   │ sum         │ monthly │
│ tts_characters      │ core    │ chars   │ sum         │ monthly │
│ storage_gb_months   │ core    │ GB-month│ max         │ monthly │
│ api_requests        │ core    │ reqs    │ sum         │ daily   │
│ active_agents       │ core    │ agents  │ max         │ monthly │
│ voice_clones        │ addon   │ clones  │ max         │ monthly │
│ concurrent_calls    │ limit   │ calls   │ max         │ hourly  │
└──────────────────────────────────────────────────────────────────┘
```

## Aggregation Dimensions

Usage can be aggregated across multiple dimensions for analysis and billing. The primary dimensions are time (billing period), tenant, meter, source, and agent.

```typescript
interface AggregationDimension {
  name: string;
  type: 'tenant' | 'time' | 'meter' | 'source' | 'agent' | 'region';
  granularity: 'raw' | 'hourly' | 'daily' | 'monthly';
  materialized: boolean; // Pre-computed in rollup tables
}

const aggregationDimensions = [
  { name: 'tenant_id', type: 'tenant', granularity: 'raw', materialized: true },
  { name: 'billing_period', type: 'time', granularity: 'monthly', materialized: true },
  { name: 'meter', type: 'meter', granularity: 'raw', materialized: true },
  { name: 'source', type: 'source', granularity: 'daily', materialized: false },
  { name: 'agent_id', type: 'agent', granularity: 'daily', materialized: false },
];
```

Pre-aggregated rollups are stored in ClickHouse for analytical queries. The raw events are stored in PostgreSQL for audit and reconciliation. The billing engine queries pre-aggregated rollups for invoice generation, while the real-time counters use Redis.

## Unit Types

Different meters measure different unit types. Each unit type has its own conversion rules and pricing implications.

- **Minutes**: Voice call duration. Rounded to nearest second, aggregated to minutes for billing.
- **Characters**: TTS output. Billed per 1,000 characters (CPM model).
- **Requests**: API calls. Billed per 1,000 requests.
- **Storage**: Monthly GB. Measured as daily peak, billed as maximum during the period.
- **Seats**: Active agents or team members. Maximum concurrent during period.

```typescript
interface UnitConfig {
  type: string;
  displayName: string;
  billingUnit: string;        // Unit shown on invoice
  conversionFactor: number;   // Raw → billing unit
  rounding: 'nearest' | 'ceil' | 'floor';
  precision: number;          // Decimal places
}

const unitConfigs: Record<string, UnitConfig> = {
  minutes: {
    type: 'minutes',
    displayName: 'Minutes',
    billingUnit: 'minute',
    conversionFactor: 1,      // Seconds → divide by 60
    rounding: 'ceil',
    precision: 2,
  },
  tts_characters: {
    type: 'characters',
    displayName: 'Characters',
    billingUnit: '1K characters',
    conversionFactor: 1000,
    rounding: 'ceil',
    precision: 1,
  },
};
```

## Data Model for Aggregated Usage

For performance, aggregated usage is stored in materialized views that summarize raw events by tenant, meter, and billing period.

```typescript
interface AggregatedUsage {
  tenantId: string;
  meterId: string;
  billingPeriod: string;     // '2025-06'
  total: number;
  unit: string;
  lastUpdated: string;
  breakdown?: Record<string, number>; // Per-source or per-agent
}
```

## Open-Source Tools

- **ClickHouse** (Apache 2.0) — Columnar analytics database for usage aggregation
- **PostgreSQL** (PostgreSQL) — Relational storage for usage records
- **Redis** (BSD-3) — Real-time counter storage
- **TimescaleDB** (Apache 2.0 / TS License) — Time-series optimized PostgreSQL

TimescaleDB is a strong option for usage data because it provides automatic partitioning by time, continuous aggregates, and retention policies — all within PostgreSQL compatibility.

## Integration Points

The metering data model is consumed by the billing engine for Stripe usage record submission, the analytics service for usage dashboards, the quota enforcement system for real-time controls, and the reconciliation service for Stripe vs internal comparison.

## Production Considerations

- Partition usage tables by month for query performance
- Implement data retention policies (raw: 12 months, aggregated: 7 years)
- Use write-audit pattern — append-only with immutable records
- Monitor usage record ingestion rate and volume growth
- Plan for usage data volume growth (SaaS usage data grows with customer base)

## Open-Source First Philosophy

The entire metering data stack is open-source: PostgreSQL/TimescaleDB for transactional storage, ClickHouse for analytical queries, and Redis for real-time counters. This replaces proprietary data warehouses (Snowflake, BigQuery) and specialized metering SaaS products (Stripe Metering, Metronome) with a self-hosted, auditable, and cost-effective alternative.
