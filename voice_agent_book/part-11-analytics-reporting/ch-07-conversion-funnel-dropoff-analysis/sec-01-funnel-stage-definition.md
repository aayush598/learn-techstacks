# Section 01: Funnel Stage Definition

## Overview

Funnel stage definition establishes the structured path that callers follow from initial contact through successful resolution. Each stage represents a distinct phase in the customer journey: Contact → IVR Handling → Queue → Agent Assignment → Conversation → Resolution → Post-Call Survey. Funnel analysis measures how many callers successfully transition from each stage to the next, identifying where callers drop off and why.

The funnel is fully configurable per tenant — an ecommerce support funnel might have stages like "Product Inquiry → Pricing → Purchase Decision" while a technical support funnel might be "Issue Reported → Diagnosis → Solution Proposed → Issue Resolved." Each stage has a definition (entry criteria, exit criteria, stage type), an optional time limit (e.g., "must reach resolution within 10 minutes"), and success criteria (what constitutes a successful transition to the next stage). Stage definitions are stored as configuration in PostgreSQL and cached in Redis.

## Architecture

```
           Funnel Stage Definition System

   Tenant Admin UI (Stage Configurator)
        |
   PostgreSQL (funnel_stages table)
        |
   Redis Cache (stage definitions)
        |
   Funnel Engine (reads stages)
        |
   ClickHouse (funnel events)
        |
   Funnel Analytics Dashboard
```

## Design Decisions

- **Configurable stages with no-code editor over hardcoded stages:** Contact centers have different definitions of "success" and different customer journeys. The no-code stage editor allows operations managers to define stages, set entry/exit criteria, and configure success thresholds without developer involvement. Stages can reference platform events (call.ivr_completed, call.queued, call.answered, call.transferred, call.completed) or custom events sent via the platform API. Trade-off: configurable stages increase the surface area for misconfiguration — stage definitions are validated before saving.

- **Stage tree (branched funnels) over linear pipeline:** Not all callers follow the same path. Some may go directly to an agent (if the IVR identifies them as VIP), some may use self-service, and some may be transferred between departments. The funnel supports branching: a caller at "IVR" may go to "Self-Service" or "Queue" depending on their choice. Each branch has its own funnel metrics. Trade-off: tree-structured funnels are more complex to visualize and analyze than linear funnels; the dashboard shows both the tree view and the "main path" linear view.

- **Event-based stage transitions over time-based stage detection:** Stage transitions are determined by platform events (e.g., `call.ivr.completed` event indicates the caller finished the IVR stage), not by time intervals or sentiment heuristics. This provides precise, deterministic stage boundaries. If a custom event is needed for a stage not covered by standard events, the tenant can emit events via the webhook API. Trade-off: event-based transitions require the voice platform to emit the correct events at the correct times; missing or misordered events can corrupt funnel data.

## Implementation Approach

```typescript
interface FunnelStage {
  id: string;
  tenantId: string;
  funnelId: string;
  name: string;
  description: string;
  order: number;
  parentStageId?: string;         // for branching
  stageType: 'entry' | 'process' | 'decision' | 'exit';
  entryEvent: string;              // event that starts this stage
  exitEvent: string;               // event that ends this stage
  successCriteria: {
    type: 'event_reached' | 'time_limit' | 'custom';
    eventName?: string;
    timeLimitSeconds?: number;
    customQuery?: string;
  };
  failureConditions: Array<{
    event: string;
    label: string;
    severity: 'drop_off' | 'abandon' | 'error';
  }>;
  isEnabled: boolean;
  createdAt: number;
  updatedAt: number;
}

interface FunnelDefinition {
  id: string;
  tenantId: string;
  name: string;
  description: string;
  stages: FunnelStage[];
  defaultTimeLimitSeconds: number;
  createdAt: number;
}

class FunnelStageService {
  private pg: PostgresClient;
  private redis: Redis;

  async getFunnel(funnelId: string, tenantId: string): Promise<FunnelDefinition | null> {
    const cacheKey = `funnel:${tenantId}:${funnelId}`;
    const cached = await this.redis.get(cacheKey);
    if (cached) return JSON.parse(cached);

    const stages = await this.pg.query(`
      SELECT * FROM funnel_stages
      WHERE funnel_id = $1 AND tenant_id = $2 AND is_enabled = true
      ORDER BY "order" ASC
    `, [funnelId, tenantId]);

    if (stages.rows.length === 0) return null;

    const funnel = {
      id: funnelId,
      tenantId,
      name: stages.rows[0].funnel_name,
      description: stages.rows[0].funnel_description,
      stages: stages.rows.map(r => ({
        id: r.id,
        tenantId: r.tenant_id,
        funnelId: r.funnel_id,
        name: r.name,
        description: r.description,
        order: r.order,
        parentStageId: r.parent_stage_id,
        stageType: r.stage_type,
        entryEvent: r.entry_event,
        exitEvent: r.exit_event,
        successCriteria: r.success_criteria,
        failureConditions: r.failure_conditions,
        isEnabled: r.is_enabled,
        createdAt: r.created_at.getTime(),
        updatedAt: r.updated_at.getTime(),
      })),
      defaultTimeLimitSeconds: stages.rows[0].default_time_limit_seconds ?? 600,
    };

    await this.redis.setex(cacheKey, 3600, JSON.stringify(funnel));
    return funnel;
  }

  async saveFunnel(funnel: FunnelDefinition): Promise<void> {
    const client = await this.pg.beginTransaction();

    try {
      // Delete existing stages
      await client.query(
        'DELETE FROM funnel_stages WHERE funnel_id = $1 AND tenant_id = $2',
        [funnel.id, funnel.tenantId]
      );

      // Insert stages
      for (let i = 0; i < funnel.stages.length; i++) {
        const stage = funnel.stages[i];
        await client.query(`
          INSERT INTO funnel_stages
          (id, tenant_id, funnel_id, name, description, "order",
           parent_stage_id, stage_type, entry_event, exit_event,
           success_criteria, failure_conditions, is_enabled,
           funnel_name, funnel_description, default_time_limit_seconds)
          VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)
        `, [
          stage.id, funnel.tenantId, funnel.id, stage.name, stage.description, stage.order,
          stage.parentStageId, stage.stageType, stage.entryEvent, stage.exitEvent,
          JSON.stringify(stage.successCriteria), JSON.stringify(stage.failureConditions),
          stage.isEnabled, funnel.name, funnel.description, funnel.defaultTimeLimitSeconds,
        ]);
      }

      await client.commit();
      await this.redis.del(`funnel:${funnel.tenantId}:${funnel.id}`);
    } catch (err) {
      await client.rollback();
      throw err;
    }
  }

  async validateFunnel(funnel: FunnelDefinition): Promise<string[]> {
    const errors: string[] = [];

    // Check stage order is valid
    const orders = funnel.stages.map(s => s.order);
    if (new Set(orders).size !== orders.length) {
      errors.push('Duplicate stage order values');
    }

    // Check at least one entry and one exit stage
    const entryStages = funnel.stages.filter(s => s.stageType === 'entry');
    const exitStages = funnel.stages.filter(s => s.stageType === 'exit');
    if (entryStages.length === 0) errors.push('At least one entry stage required');
    if (exitStages.length === 0) errors.push('At least one exit stage required');

    // Check parent stages exist
    for (const stage of funnel.stages) {
      if (stage.parentStageId) {
        const parent = funnel.stages.find(s => s.id === stage.parentStageId);
        if (!parent) errors.push(`Parent stage ${stage.parentStageId} not found for stage ${stage.id}`);
      }
    }

    return errors;
  }
}

// Stage configuration UI (simplified)
const FunnelStageEditor: React.FC<{
  funnel: FunnelDefinition;
  onSave: (funnel: FunnelDefinition) => void;
}> = ({ funnel, onSave }) => {
  const [stages, setStages] = useState(funnel.stages);

  const addStage = () => {
    setStages([...stages, {
      id: `stage_${Date.now()}`,
      tenantId: funnel.tenantId,
      funnelId: funnel.id,
      name: '',
      description: '',
      order: stages.length + 1,
      stageType: 'process',
      entryEvent: '',
      exitEvent: '',
      successCriteria: { type: 'event_reached' },
      failureConditions: [],
      isEnabled: true,
      createdAt: Date.now(),
      updatedAt: Date.now(),
    }]);
  };

  return (
    <div className="funnel-editor">
      <StageList
        stages={stages}
        onReorder={(fromIndex, toIndex) => { /* reorder logic */ }}
        onUpdate={(index, stage) => {
          const updated = [...stages];
          updated[index] = stage;
          setStages(updated);
        }}
      />
      <Button onClick={addStage}>Add Stage</Button>
      <Button onClick={() => onSave({ ...funnel, stages })}>Save Funnel</Button>
    </div>
  );
};
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| PostgreSQL (PostgreSQL) | Server | Stage definition storage |
| Redis (RSAL) | Server | Stage definition cache |
| react-beautiful-dnd (Apache 2.0) | Client | Drag-and-drop stage reordering |
| React Hook Form (MIT) | Client | Stage configuration form |

## Production Considerations

**Scaling:** Funnel definitions are small (< 10 KB) and infrequently modified. PostgreSQL handles millions of funnel records. Redis caches with 1-hour TTL ensure fast dashboard loads. Stage definitions are fetched once per dashboard session and cached on the client.

**Security:** Funnel definitions are tenant-scoped — the `getFunnel` query filters by tenantId. Only administrators and supervisors with the `analytics:configure` permission can create or modify funnels. Stage events reference platform event names — validation ensures tenants cannot reference events they don't have permission to use.

**Monitoring:** Track the number of funnel definitions per tenant, stage validation errors, and funnel modification frequency. Alert if a tenant's funnel has validation errors (broken parent references, no exit stage). Monitor the cache hit rate for funnel definitions — if below 90%, increase cache TTL.
