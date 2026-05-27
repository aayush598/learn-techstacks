# Section 04: Expected Path Validation

## Overview

Expected path validation compares the actual conversation path taken during simulation against the expected path defined in the flow. The validator checks that the agent correctly navigated through required states, handled transitions properly, and produced expected responses. Validation goes beyond simple path matching to include semantic response comparison, intent accuracy verification, and timing constraints.

Path validation is critical for detecting regressions in agent behavior. When a code change causes the agent to take a different conversational path, the validator catches it immediately and provides detailed diffs showing where the paths diverged.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Audio    |--->| WebSocket|--->| Jitter   |--->| PLC      |--->| Player   |
| Producer |    | (WSS)    |    | Buffer   |    | (Packet  |    | (smooth  |
| (100ms   |    | (binary) |    | (adaptive|    |  Loss    |    |  output) |
|  chunks) |    |          |    |  60-200) |    |  Conceal)|    +----------+
+----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```typescript
class PathValidator {
  validate(flow: FlowDefinition, actual: ConversationPath): ValidationResult {
    const expectedPath = this.getExpectedPath(flow);
    const issues: PathIssue[] = [];

    // 1. Extract state sequence
    const expectedStates = expectedPath.map(s => s.state);
    const actualStates = actual.turns.map(t => t.currentState);

    // 2. LCS-based diff
    const diff = this.computeDiff(expectedStates, actualStates);

    // 3. Analyze differences
    for (const change of diff) {
      switch (change.type) {
        case 'missing':
          issues.push({
            type: 'missing_node',
            expected: change.value,
            turn: change.index,
          });
          break;
        case 'extra':
          issues.push({
            type: 'extra_node',
            actual: change.value,
            turn: change.index,
          });
          break;
        case 'wrong_order':
          issues.push({
            type: 'wrong_order',
            expected: change.expected,
            actual: change.actual,
          });
          break;
      }
    }

    // 4. Validate responses
    for (let i = 0; i < actual.turns.length; i++) {
      const turn = actual.turns[i];
      const expectedResponse = expectedPath[i]?.response;
      
      if (expectedResponse) {
        const similarity = this.calculateSimilarity(
          turn.agentResponse,
          expectedResponse
        );
        if (similarity < this.config.responseThreshold) {
          issues.push({
            type: 'response_mismatch',
            turn: i,
            expected: expectedResponse,
            actual: turn.agentResponse,
            similarity,
          });
        }
      }
    }

    return {
      passed: issues.length === 0,
      issues,
      pathScore: this.calculatePathScore(expectedStates, actualStates),
      divergencePoint: this.findDivergence(expectedStates, actualStates),
    };
  }

  private computeDiff(expected: string[], actual: string[]): DiffChange[] {
    // Longest Common Subsequence algorithm
    const lcs = this.longestCommonSubsequence(expected, actual);
    
    const changes: DiffChange[] = [];
    let e = 0, a = 0, l = 0;
    
    while (e < expected.length || a < actual.length) {
      if (l < lcs.length && expected[e] === lcs[l] && actual[a] === lcs[l]) {
        e++; a++; l++; // Match
      } else if (l < lcs.length && expected[e] !== lcs[l]) {
        changes.push({ type: 'missing', value: expected[e], index: e });
        e++;
      } else if (l < lcs.length && actual[a] !== lcs[l]) {
        changes.push({ type: 'extra', value: actual[a], index: a });
        a++;
      } else {
        if (e < expected.length) {
          changes.push({ type: 'missing', value: expected[e], index: e });
          e++;
        }
        if (a < actual.length) {
          changes.push({ type: 'extra', value: actual[a], index: a });
          a++;
        }
      }
    }
    
    return changes;
  }
}
```

## Integration Points

- **Simulation Engine**: Validator called at end of each simulation
- **CI Pipeline**: Validation results determine pass/fail
- **Dashboard**: Validation trends displayed on quality dashboard
- **Agent Config**: Validation thresholds configurable per agent
- **Debugging**: Detailed path diffs for debugging agent behavior changes

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **Threshold Tuning**: Response similarity thresholds need tuning per use case
- **Expected Path Drift**: Update expected paths when flows intentionally change
- **Performance**: Path validation is fast; LCS runs in O(n*m) time
- **False Positives**: Lenient matching for responses that are semantically correct but textually different
- **Validation Caching**: Cache validation results for identical simulations
