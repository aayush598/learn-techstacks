# Section 01: Simulation Engine Architecture

## Overview

The Conversation Simulation Engine is a custom testing framework that generates realistic voice conversations to validate agent behavior. It simulates caller utterances, processes them through the voice pipeline (VAD → STT → LLM → TTS), and compares the actual conversation against expected paths. This enables automated testing of agent responses, intent recognition, knowledge base retrieval, and conversation flow adherence.

The engine is built as a standalone service that interacts with the platform's core voice pipeline through the same API surface as real calls. It uses a state machine to model conversation flows, template-based and LLM-generated utterances for input variety, and configurable evaluation criteria to validate outcomes.

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
class SimulationEngine {
  private flows: Map<string, FlowDefinition> = new Map();
  private generator: UtteranceGenerator;
  private validator: PathValidator;

  constructor(
    private voicePipeline: VoicePipelineClient,
    private config: EngineConfig
  ) {
    this.generator = new UtteranceGenerator(config);
    this.validator = new PathValidator(config);
  }

  async simulate(flowName: string, options: SimulationOptions): Promise<SimulationResult> {
    const flow = this.flows.get(flowName);
    if (!flow) throw new Error(`Flow not found: ${flowName}`);

    const context = new ConversationContext(flow.initial);
    const transcript: ConversationTurn[] = [];

    while (!context.isComplete()) {
      // Generate utterance based on current state
      const utterance = this.generator.generate(
        flow.states[context.currentState],
        options
      );

      // Process through voice pipeline
      const response = await this.voicePipeline.processUtterance(utterance, {
        agentId: options.agentId,
        sessionId: options.sessionId,
      });

      // Record turn
      transcript.push({
        utterance,
        response: response.text,
        intent: response.intent,
        latency: response.latency,
      });

      // Advance state
      const transition = flow.states[context.currentState].on[response.intent];
      if (transition) {
        context.advance(transition);
      } else {
        context.advance('__fallback__');
      }
    }

    return {
      transcript,
      path: context.path,
      metrics: this.calculateMetrics(transcript),
      passed: this.validator.validatePath(flow, context.path),
    };
  }
}
```

## Integration Points

- **Voice Pipeline**: Engine calls the same STT/LLM/TTS APIs as real calls
- **Agent Configuration**: Simulations use actual agent configurations
- **Knowledge Base**: Tests validate KB retrieval during conversations
- **CI Pipeline**: Simulations run on every agent configuration change
- **Analytics**: Simulation results feed into quality dashboards

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **Simulation Cost**: LLM-generated utterances incur API costs; cache results
- **Execution Time**: Complex simulations take time; run asynchronously
- **Determinism**: Seeded randomness ensures reproducible results
- **Resource Cleanup**: Active simulations consume pipeline resources; enforce timeouts
- **Result Storage**: Store simulation results for trend analysis and debugging
