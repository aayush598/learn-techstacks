# Section 05: Edge Case Fuzzing

## Overview

Edge case fuzzing tests the conversation engine's robustness by feeding it unexpected, malformed, or boundary-condition inputs. For the voice AI platform, fuzzing covers silence detection, noise interference, speech interruptions, non-speech audio, multiple intents in one utterance, and adversarial inputs designed to confuse the intent classifier.

Fuzzing is essential for building robust voice agents that handle real-world conditions gracefully. Unlike happy-path testing, fuzzing discovers failure modes that would otherwise only surface in production, such as the agent's behavior when faced with background noise, heavy accents, or users who talk over the agent.

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
class FuzzingEngine {
  private mutators: Mutator[] = [
    new SilenceMutator(),
    new NoiseMutator(),
    new InterruptionMutator(),
    new GibberishMutator(),
    new BoundaryMutator(),
  ];

  async fuzz(
    agent: AgentClient,
    flow: FlowDefinition,
    config: FuzzConfig
  ): Promise<FuzzResult> {
    const results: FuzzCase[] = [];
    const startTime = Date.now();

    while (Date.now() - startTime < config.duration) {
      // Select random mutator
      const mutator = faker.helpers.arrayElement(this.mutators);
      
      // Generate fuzzed input
      const baseUtterance = this.getBaseUtterance(flow);
      const fuzzed = mutator.mutate(baseUtterance);

      // Execute
      try {
        const response = await agent.processUtterance(fuzzed.input);
        results.push({
          input: fuzzed.input,
          type: fuzzed.type,
          response: response.text,
          status: 'completed',
          duration: response.latency,
          error: null,
        });
      } catch (error) {
        results.push({
          input: fuzzed.input,
          type: fuzzed.type,
          response: null,
          status: 'error',
          duration: 0,
          error: error.message,
        });
      }
    }

    return this.analyze(results, config);
  }

  private analyze(results: FuzzCase[], config: FuzzConfig): FuzzResult {
    const errors = results.filter(r => r.status === 'error');
    const crashes = errors.filter(e => e.error?.includes('crash'));
    const slowResponses = results.filter(r => r.duration > config.maxLatency);

    return {
      totalCases: results.length,
      errorCount: errors.length,
      crashCount: crashes.length,
      slowResponseCount: slowResponses.length,
      errorRate: errors.length / results.length,
      crashRate: crashes.length / results.length,
      errorDetails: errors.slice(0, 10), // Top 10 errors
      slowResponses: slowResponses.slice(0, 5),
      coverage: results.map(r => r.input.type),
    };
  }
}

// Example mutator: Interruption
class InterruptionMutator implements Mutator {
  mutate(input: Utterance): FuzzedInput {
    const interruption = faker.helpers.arrayElement([
      "Wait, that's not what I meant!",
      "No no no, listen to me!",
      "Actually, forget that.",
      "Hold on, let me start over.",
    ]);

    return {
      input: `${input.text}... ${interruption}`,
      type: 'interruption',
      meta: { interruptionPoint: input.text.length },
    };
  }
}
```

## Integration Points

- **Simulation Engine**: Fuzzing integrated into simulation workflow
- **CI Pipeline**: Fuzzing runs as a separate CI job with time budget
- **Issue Tracking**: Discovered issues auto-create tickets
- **Regression Suite**: Fuzzing-discovered bugs added to regression test suite
- **Coverage Integration**: Fuzzing coverage mapped to source code

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **Test Cost**: Fuzzing is computationally expensive; time-box execution
- **False Positives**: Some fuzz inputs are unrealistic; review before filing bugs
- **Safety Considerations**: Ensure fuzzing doesn't trigger unwanted side effects
- **Regression Corpus**: Maintain a curated set of fuzz inputs for regression testing
- **Coverage Analysis**: Use coverage data to identify untested code paths
