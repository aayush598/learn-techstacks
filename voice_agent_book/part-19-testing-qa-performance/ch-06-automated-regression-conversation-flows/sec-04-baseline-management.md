# Section 04: Baseline Management

## Overview

Baseline management maintains the reference data that regression tests compare against. Each agent version has an associated baseline containing snapshots of expected conversation behavior. Baselines evolve as agents are improved, but changes must be intentional and reviewed. The baseline management system provides version control, review workflows, and automated updates for approved changes.

Baselines are stored as version-controlled files alongside agent configurations, enabling full traceability of when and why expected behavior changed. The system supports multiple baselines per agent (e.g., different languages or use cases) and can compare across baseline versions for trend analysis.

## Design Decisions

- **React Flow over Custom**: Battle-tested node/edge rendering. Saves 6+ months custom development.
- **Local-First State**: Zustand + debounced saves (2s). Instant UI response without waiting for API.
- **Function-as-Edge**: Edges carry conditions and transforms. Flow evaluates conditions at each step.
## Implementation Approach

```typescript
class BaselineManager {
  async create(agentId: string, version: string): Promise<Baseline> {
    const snapshot = await this.snapshotManager.capture(agentId);
    const baseline: Baseline = {
      id: `${agentId}/${version}`,
      agentId,
      version,
      createdAt: new Date(),
      snapshots: [snapshot],
      status: 'active',
    };
    await this.store(baseline);
    return baseline;
  }

  async update(baselineId: string, changes: BaselineChange[]): Promise<Baseline> {
    const baseline = await this.load(baselineId);
    
    // Apply approved changes
    for (const change of changes) {
      if (change.type === 'replace_snapshot') {
        const idx = baseline.snapshots.findIndex(s => s.id === change.snapshotId);
        if (idx >= 0) {
          baseline.snapshots[idx] = change.newSnapshot;
        }
      }
    }
    
    baseline.updatedAt = new Date();
    baseline.version = incrementVersion(baseline.version);
    
    await this.store(baseline);
    return baseline;
  }

  async compare(baselineA: string, baselineB: string): Promise<BaselineDiff> {
    const a = await this.load(baselineA);
    const b = await this.load(baselineB);
    return this.diffEngine.compare(a, b);
  }

  async proposeUpdate(agentId: string, currentVersion: string): Promise<BaselineProposal> {
    const currentBaseline = await this.load(`${agentId}/${currentVersion}`);
    const newSnapshots = await this.snapshotManager.capture(agentId);
    
    const diffs = await this.diffEngine.compare(currentBaseline, {
      snapshots: [newSnapshots],
    });
    
    return {
      agentId,
      fromVersion: currentVersion,
      toVersion: currentVersion, // Will be set on approval
      changes: diffs,
      proposedAt: new Date(),
      status: 'pending',
    };
  }
}
```

## Integration Points

- **Agent Versioning**: Baselines tied to agent version numbers
- **CI Pipeline**: Baselines created/updated during CI
- **Review System**: Baseline changes flow through code review
- **Regression Engine**: Baselines consumed for regression testing
- **Change Log**: Baseline changes logged for audit

## Open-Source Tools

- **React Flow** (MIT): Node-based UI
- **Zustand** (MIT): State management
- **Immer** (MIT): Immutable updates
## Production Considerations

- **Storage Size**: Full snapshots for every version grow large; use incremental baselines
- **Review Bottleneck**: Too many baseline change proposals overwhelm reviewers
- **Automation Trust**: Build confidence in automated proposals over time
- **Baseline Drift**: Regular audits ensure baselines reflect actual desired behavior
- **Migration**: When conversation design changes significantly, create new baseline branch
