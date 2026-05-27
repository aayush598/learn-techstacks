# Section 03: Diff Detection & Analysis

## Overview

Diff detection identifies meaningful changes between conversation simulation results. Unlike simple text comparison, conversation diffing must understand semantic equivalence: two different phrasings that mean the same thing should not be flagged as a difference. The diff engine combines textual, semantic, and structural analysis to identify genuine regressions.

The detection pipeline processes conversation transcripts through multiple comparison stages: structural (path changes), semantic (meaning changes), textual (response wording), and metric (performance changes). Each stage produces a diff report that feeds into the regression classification system.

## Design Decisions

- **React Flow over Custom**: Battle-tested node/edge rendering. Saves 6+ months custom development.
- **Local-First State**: Zustand + debounced saves (2s). Instant UI response without waiting for API.
- **Function-as-Edge**: Edges carry conditions and transforms. Flow evaluates conditions at each step.
## Implementation Approach

```typescript
class ConversationDiffEngine {
  async compare(baseline: SimulationResult, current: SimulationResult): Promise<DiffReport> {
    const diffs: Diff[] = [];

    // 1. Path diff (structural)
    const pathDiff = this.comparePaths(baseline.path, current.path);
    if (pathDiff.hasChanges) {
      diffs.push({
        type: 'path',
        severity: 'high',
        description: `Conversation path changed`,
        details: pathDiff,
      });
    }

    // 2. Turn-by-turn comparison
    for (let i = 0; i < Math.max(baseline.transcript.length, current.transcript.length); i++) {
      const baseTurn = baseline.transcript[i];
      const currTurn = current.transcript[i];

      if (!baseTurn && currTurn) {
        diffs.push({ type: 'extra_turn', severity: 'medium', turn: i, ... });
        continue;
      }
      if (baseTurn && !currTurn) {
        diffs.push({ type: 'missing_turn', severity: 'medium', turn: i, ... });
        continue;
      }

      // 3. Intent comparison
      if (baseTurn.intent !== currTurn.intent) {
        diffs.push({
          type: 'intent_changed',
          severity: this.intentChangeSeverity(baseTurn.intent, currTurn.intent),
          turn: i,
          from: baseTurn.intent,
          to: currTurn.intent,
        });
      }

      // 4. Semantic response comparison
      const semanticSimilarity = await this.semanticSimilarity(
        baseTurn.response,
        currTurn.response
      );
      if (semanticSimilarity < this.config.semanticThreshold) {
        diffs.push({
          type: 'response_changed',
          severity: 'medium',
          turn: i,
          similarity: semanticSimilarity,
        });
      }

      // 5. Confidence comparison
      if (Math.abs(baseTurn.confidence - currTurn.confidence) > 0.1) {
        diffs.push({
          type: 'confidence_changed',
          severity: 'low',
          turn: i,
          from: baseTurn.confidence,
          to: currTurn.confidence,
        });
      }
    }

    return {
      hasRegressions: diffs.some(d => d.severity === 'high'),
      diffs: this.prioritizeDiffs(diffs),
      summary: {
        total: diffs.length,
        high: diffs.filter(d => d.severity === 'high').length,
        medium: diffs.filter(d => d.severity === 'medium').length,
        low: diffs.filter(d => d.severity === 'low').length,
      },
    };
  }

  private async semanticSimilarity(a: string, b: string): Promise<number> {
    // Use sentence transformer embeddings
    const embeddingA = await this.embeddingModel.embed(a);
    const embeddingB = await this.embeddingModel.embed(b);
    return this.cosineSimilarity(embeddingA, embeddingB);
  }
}
```

## Integration Points

- **Baseline Manager**: Consumes baseline data for comparison
- **Alert System**: High-severity diffs trigger alerts
- **PR Review**: Diffs presented in PR for developer review
- **Dashboard**: Diff trends tracked over time
- **Bisect Tool**: Diffs linked to specific commits

## Open-Source Tools

- **React Flow** (MIT): Node-based UI
- **Zustand** (MIT): State management
- **Immer** (MIT): Immutable updates
## Production Considerations

- **Embedding Cost**: Semantic comparison requires model inference; batch for efficiency
- **Threshold Tuning**: Semantic thresholds need tuning per domain
- **False Positives**: Some valid changes flagged as diffs; review process needed
- **Performance**: Diff computation is CPU-intensive; parallelize across workers
