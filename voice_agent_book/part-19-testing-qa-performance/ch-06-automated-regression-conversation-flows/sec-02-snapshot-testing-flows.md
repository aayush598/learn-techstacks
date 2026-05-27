# Section 02: Snapshot Testing for Flows

## Overview

Snapshot testing for conversation flows captures the complete state of a conversation at each turn, storing it as a version-controlled snapshot. These snapshots serve as the ground truth for what correct agent behavior looks like. When agent code changes, new snapshots are compared against stored baselines to detect behavioral differences.

Flow snapshots include the utterance, agent response, detected intent, confidence score, conversation state, and timing information. The snapshot format is designed to be human-readable for review while supporting automated comparison.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Canvas   |--->| Node     |--->| Edge     |--->| Validator|--->| Serializ |
| (React   |    | Registry |    | Router   |    | (cycle   |    | ation    |
|  Flow)   |    | (types)  |    | (condit) |    |  detect) |    | (JSON)   |
+----------+    +----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **React Flow over Custom**: Battle-tested node/edge rendering. Saves 6+ months custom development.
- **Local-First State**: Zustand + debounced saves (2s). Instant UI response without waiting for API.
- **Function-as-Edge**: Edges carry conditions and transforms. Flow evaluates conditions at each step.
## Implementation Approach

```typescript
class FlowSnapshotManager {
  async capture(conversation: ConversationResult): Promise<FlowSnapshot> {
    return {
      flow: conversation.flowName,
      agentVersion: conversation.agentVersion,
      timestamp: new Date().toISOString(),
      turns: conversation.transcript.map((turn, i) => ({
        turn: i + 1,
        utterance: turn.utterance,
        response: turn.response,
        intent: turn.intent,
        confidence: turn.confidence,
        state: turn.state,
        latencyMs: turn.latency,
      })),
      path: conversation.path,
      metrics: {
        totalDuration: conversation.duration,
        avgLatency: this.average(conversation.transcript.map(t => t.latency)),
        avgConfidence: this.average(conversation.transcript.map(t => t.confidence)),
        turnCount: conversation.transcript.length,
      },
    };
  }

  async store(snapshot: FlowSnapshot): Promise<string> {
    const id = `${snapshot.flow}/${snapshot.agentVersion}/${Date.now()}`;
    await this.storage.put(`snapshots/${id}.json`, JSON.stringify(snapshot));
    return id;
  }

  async compare(baseline: FlowSnapshot, current: FlowSnapshot): Promise<SnapshotDiff> {
    const diffs: TurnDiff[] = [];
    
    for (let i = 0; i < Math.max(baseline.turns.length, current.turns.length); i++) {
      const base = baseline.turns[i];
      const curr = current.turns[i];
      
      if (!base || !curr) {
        diffs.push({ type: 'length_change', turn: i, ... });
        continue;
      }
      
      if (base.intent !== curr.intent) {
        diffs.push({ type: 'intent_change', turn: i, from: base.intent, to: curr.intent });
      }
      
      if (this.responseSimilarity(base.response, curr.response) < 0.8) {
        diffs.push({ type: 'response_change', turn: i, from: base.response, to: curr.response });
      }
    }
    
    return { diffs, hasChanges: diffs.length > 0 };
  }
}
```

## Integration Points

- **Regression Engine**: Snapshots consumed by regression comparison engine
- **CI Pipeline**: Snapshots generated and compared in CI
- **Review Workflow**: Snapshot diffs presented for human review
- **Changelog**: Snapshot changes documented in agent changelogs
- **Debugging**: Historical snapshots available for debugging

## Open-Source Tools

- **React Flow** (MIT): Node-based UI
- **Zustand** (MIT): State management
- **Immer** (MIT): Immutable updates
## Production Considerations

- **Storage Growth**: Snapshot storage grows with each agent version; archive old versions
- **Comparison Cost**: Full snapshot comparison is expensive; use checksums for quick diff
- **Human Review Bottleneck**: Too many snapshot changes overwhelm reviewers; auto-approve trivial changes
- **Snapshot Drift**: Baselines must be updated when intentional changes are made
