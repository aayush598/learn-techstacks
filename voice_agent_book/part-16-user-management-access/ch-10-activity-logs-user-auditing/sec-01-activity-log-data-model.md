# Activity Log Data Model

## Overview

The activity log data model defines the schema for recording user actions with the actor/action/target pattern, supporting comprehensive audit trails, correlation IDs for linking related events, and flexible metadata fields.

## Event Schema

```typescript
interface ActivityEvent {
  id: string;
  timestamp: Date;
  actor: {
    id: string;
    type: 'user' | 'system' | 'api_key' | 'webhook';
    email?: string;
    ipAddress?: string;
    userAgent?: string;
  };
  action: string;               // e.g., "campaign.created"
  target: {
    id: string;
    type: string;               // e.g., "campaign", "agent"
    name?: string;
    parentId?: string;
  };
  changes?: {
    before: Record<string, unknown> | null;
    after: Record<string, unknown> | null;
  };
  context: {
    tenantId: string;
    sessionId?: string;
    requestId?: string;
    correlationId?: string;
    source: 'app' | 'api' | 'admin' | 'system' | 'scim';
  };
  severity: 'info' | 'warning' | 'error' | 'critical';
  metadata?: Record<string, unknown>;
}
```

## Database Schema

```sql
CREATE TABLE activity_logs (
  id VARCHAR(64) PRIMARY KEY,
  timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actor_id VARCHAR(64) NOT NULL,
  actor_type VARCHAR(32) NOT NULL,
  actor_email VARCHAR(255),
  actor_ip VARCHAR(45),
  actor_user_agent TEXT,
  action VARCHAR(128) NOT NULL,
  target_id VARCHAR(64),
  target_type VARCHAR(64),
  target_name VARCHAR(255),
  target_parent_id VARCHAR(64),
  changes_before JSON,
  changes_after JSON,
  tenant_id VARCHAR(64) NOT NULL,
  session_id VARCHAR(64),
  request_id VARCHAR(64),
  correlation_id VARCHAR(64),
  source VARCHAR(32) NOT NULL DEFAULT 'app',
  severity VARCHAR(16) NOT NULL DEFAULT 'info',
  metadata JSON,
  INDEX idx_tenant_timestamp (tenant_id, timestamp DESC),
  INDEX idx_actor (actor_id, timestamp DESC),
  INDEX idx_action (action, timestamp DESC),
  INDEX idx_target (target_type, target_id),
  INDEX idx_correlation (correlation_id)
);
```

## Open-Source Tools

- **Elasticsearch** — Document storage for log analytics
- **TimescaleDB** — Time-series optimized PostgreSQL
- **ClickHouse** (Apache 2.0) — Columnar analytics storage

## Production Considerations

- Index by tenant + timestamp for common query patterns
- Use correlation IDs to trace related events across services
- Compress changes before/after JSON for storage efficiency
- Partition by time (monthly) for query performance
- Retain raw events for 90 days, aggregates for 13 months
- Never log sensitive data (passwords, tokens, PII) in metadata
- Include request ID for cross-service tracing
