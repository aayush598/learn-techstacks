# Section 06: Automated Rollout Strategies

## Overview

Automated rollout strategies define how winning test variants are gradually deployed to production traffic. Rather than a sudden "switch flip" from control to winner (which risks exposing all traffic to an underperforming variant if the test results were misleading), automated rollout uses progressive traffic ramping that increases the winning variant's allocation over time while monitoring for degradation. This approach provides a safety net — if the winner performs differently at 100% traffic than it did during the test (due to novelty effects, seasonality, or interaction effects), the rollout can be paused or rolled back.

The rollout system implements canary deployment patterns adapted for campaign traffic. The winning variant starts at a small allocation (e.g., 10% of contacts) while the control gets 90%. Over a configured period (hours to days), the winner's allocation increases through predefined stages (25%, 50%, 75%, 100%) with mandatory monitoring checkpoints at each stage. At any checkpoint, if key metrics degrade beyond acceptable thresholds, the rollout is automatically paused and the allocation reverts to the previous safe stage or fully back to control.

## Architecture

```
                  Automated Rollout Flow

   Winner Declared (Provisional)
        |
        v
   +----------------------------------------------------+
   |         Rollout Planning Engine                     |
   |                                                    |
   |  - Define ramp stages (10%, 25%, 50%, 75%, 100%)   |
   |  - Set stage duration (e.g., 2 hours each)         |
   |  - Configure metric monitoring thresholds           |
   |  - Define rollback criteria                         |
   |  - Schedule rollout start                           |
   +----------------------------------------------------+
        |
        v
   +----------------------------------------------------+
   |         Rollout Execution Engine                    |
   |                                                    |
   |  Stage 1: 10% winner, 90% control                  |
   |    → Monitor metrics for stage duration             |
   |    → Check thresholds: OK? → proceed to Stage 2     |
   |    → Thresholds breached? → pause & rollback        |
   |                                                    |
   |  Stage 2: 25% winner, 75% control                  |
   |    → Monitor metrics for stage duration             |
   |    → ...continue through all stages...              |
   |                                                    |
   |  Final: 100% winner, 0% control                    |
   |    → Winner confirmed → update default config      |
   +----------------------------------------------------+
        |
        v
   +----------------------------------------------------+
   |         Rollback & Recovery                         |
   |                                                    |
   |  Automatic rollback triggers:                       |
   |  - Primary metric drops below pre-rollout baseline  |
   |  - Secondary metric exceeds warning threshold       |
   |  - Error rate increases significantly               |
   |                                                    |
   |  Manual rollback: one-click revert to control       |
   |  • Allocations revert instantly                     |
   |  • Rollback reason logged                           |
   |  • Original test data preserved for analysis        |
   +----------------------------------------------------+
```

## Design Decisions

- **Progressive ramping with time-based stages over metric-based stages:** Rollout stages are defined by time duration (e.g., 2 hours per stage) rather than metric achievement. This provides predictable rollout timing and prevents indefinite pauses if metrics fluctuate within normal range. Metric thresholds at each stage are used for go/no-go decisions, not for determining stage duration. Trade-off: time-based stages may move too quickly through stages that need more data, or too slowly through stages that are clearly safe.

- **Automated rollback with manual restart:** If monitoring thresholds are breached, rollout automatically reverts to the previous safe stage (or fully to control). However, restarting the rollout requires manual intervention after root cause analysis. This prevents automatic restart into the same failure condition. The system logs all monitoring data before and during the breach to support RCA. Trade-off: manual restart can cause delays if the failure was a transient anomaly rather than a genuine winner problem.

- **Canary-by-segment for multi-tenant rollouts:** For multi-tenant SaaS, the rollout happens tenant-by-tenant rather than traffic-percentage. Initially, the winning variant is enabled for a small number of low-value, technically sophisticated tenants. After validation, it expands to more tenants in waves. Segment-based rollout provides stronger validation because it tests across different usage patterns and contact profiles. Trade-off: tenant-based rollout takes longer to reach full deployment and requires tenant segmentation logic.

## Implementation Approach

```
interface RolloutPlan {
  testId: string;
  winnerVariantId: string;
  controlVariantId: string;
  stages: { allocation: number; duration: number }[];
  monitoring: {
    metrics: string[];
    thresholds: { metric: string; maxDecline: number }[];
    evaluationInterval: number;  // How often to check thresholds (ms)
  };
  rollback: {
    autoRollbackEnabled: boolean;
    rollbackToStage: number;  // Stage to roll back to, 0 = full control
  };
  status: 'pending' | 'running' | 'completed' | 'rolled_back' | 'paused';
  currentStage: number;
}

class AutomatedRolloutService {
  async executeRollout(plan: RolloutPlan) {
    for (let i = 0; i < plan.stages.length; i++) {
      const stage = plan.stages[i];
      plan.currentStage = i;
      await this.setAllocation(plan.winnerVariantId, stage.allocation);

      // Monitor for stage duration
      const stageStart = Date.now();
      while (Date.now() - stageStart < stage.duration) {
        await this.sleep(plan.monitoring.evaluationInterval);
        const metrics = await this.getCurrentMetrics(plan);
        if (this.shouldRollback(metrics, plan)) {
          await this.executeRollback(plan);
          return { status: 'rolled_back', rolledBackAtStage: i };
        }
      }
    }
    plan.status = 'completed';
    await this.finalizeRollout(plan);
    return { status: 'completed' };
  }

  private shouldRollback(metrics: Record<string, number>, plan: RolloutPlan): boolean {
    if (!plan.rollback.autoRollbackEnabled) return false;
    return plan.monitoring.thresholds.some(t => {
      const currentValue = metrics[t.metric];
      const baselineValue = metrics[`${t.metric}_baseline`];
      const decline = baselineValue > 0 ? (baselineValue - currentValue) / baselineValue : 0;
      return decline > t.maxDecline;
    });
  }

  private async executeRollback(plan: RolloutPlan) {
    const previousStageAllocation = plan.currentStage > 0
      ? plan.stages[plan.currentStage - 1].allocation
      : 0;
    await this.setAllocation(plan.winnerVariantId, previousStageAllocation);
    plan.status = 'rolled_back';
    await this.recordRollback(plan);
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **BullMQ** (MIT) | Queue | Rollout stage scheduling |
| **Redis** (BSD) | Data store | Allocation state management |
| **Prometheus** (Apache 2.0) | Monitoring | Metric collection for rollback checks |
| **Grafana** (AGPLv3) | Dashboards | Rollout monitoring dashboard |

## Production Considerations

**Scaling:** Rollout allocation changes must propagate to all dialer instances within seconds. Use Redis pub/sub to broadcast allocation changes to all instances. Each instance independently enforces the allocation ratio using deterministic hashing (same contact always gets same variant). For multi-tenant rollouts, maintain per-tenant allocation overrides in Redis with a fallback to the default allocation.

**Security:** Rollout control endpoints must be protected with elevated access — only senior campaign managers or automated systems should trigger rollouts. Rollback capabilities should be available even if the rollout automation fails (manual override). Audit all rollout actions, including automatic rollbacks, with reason codes and metric snapshots.

**Monitoring:** Build a dedicated rollout monitoring dashboard showing current stage, allocation ratio, key metrics vs. baselines, rollback threshold status, and expected completion time. Alert on any automatic rollback (this is a significant event that requires investigation), stage duration exceeding estimate (may indicate infrastructure issues), and allocation state inconsistency (different instances showing different allocations).
