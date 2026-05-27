# Section 06: Simulation Data Collection

## Overview

Simulation data collection captures detailed telemetry from each conversation simulation run, enabling analysis of agent behavior, performance metrics, and quality trends. Collected data includes full conversation transcripts, per-turn latency measurements, intent classification confidence scores, path traversal information, and error details.

This data feeds into analytics dashboards that track simulation pass rates, latency trends, common failure modes, and agent behavior changes over time. The data pipeline processes simulation results in real-time and stores them for historical analysis.

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
class SimulationDataCollector {
  constructor(
    private db: PrismaClient,
    private storage: ObjectStorage,
    private metrics: MetricsClient
  ) {}

  async recordSimulation(simulation: SimulationResult): Promise<void> {
    // Store simulation record
    await this.db.simulation.create({
      data: {
        id: simulation.id,
        flowName: simulation.flowName,
        agentId: simulation.agentId,
        status: simulation.passed ? 'passed' : 'failed',
        duration: simulation.duration,
        turnCount: simulation.transcript.length,
        startedAt: simulation.startedAt,
        completedAt: simulation.completedAt,
      },
    });

    // Store transcript
    await this.storage.put(
      `simulations/${simulation.id}/transcript.json`,
      JSON.stringify(simulation.transcript, null, 2)
    );

    // Store per-turn metrics
    for (const turn of simulation.transcript) {
      await this.emitTurnMetric(simulation.id, turn);
    }

    // Update aggregated metrics
    await this.metrics.increment('simulation.total', 1);
    if (simulation.passed) {
      await this.metrics.increment('simulation.passed', 1);
    } else {
      await this.metrics.increment('simulation.failed', 1);
    }

    // Record latency distribution
    const latencies = simulation.transcript.map(t => t.latency);
    await this.metrics.histogram('simulation.latency', latencies);
  }

  private async emitTurnMetric(
    simulationId: string,
    turn: ConversationTurn
  ): Promise<void> {
    await this.metrics.gauge('turn.latency', turn.latency, {
      simulationId,
      intent: turn.intent,
      state: turn.currentState,
    });

    await this.metrics.gauge('turn.confidence', turn.confidence, {
      simulationId,
      intent: turn.intent,
    });
  }

  async querySimulations(query: SimulationQuery): Promise<SimulationSummary[]> {
    return this.db.simulation.findMany({
      where: {
        flowName: query.flowName,
        agentId: query.agentId,
        createdAt: {
          gte: query.dateFrom,
          lte: query.dateTo,
        },
      },
      orderBy: { createdAt: 'desc' },
      take: query.limit || 100,
    });
  }
}
```

## Integration Points

- **Analytics Dashboard**: Simulation metrics displayed on quality dashboard
- **CI Pipeline**: Results reported in CI output and PR comments
- **Alert System**: Failed simulation rate triggers alerts
- **Transcript Viewer**: Web UI for browsing simulation transcripts
- **Export API**: Simulation data exportable via API for external analysis

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **Storage Growth**: Simulation data grows quickly; implement lifecycle policies
- **Query Performance**: Index simulation queries by flow name, agent ID, and date
- **Cost Management**: Object storage costs for audio files; compress aggressively
- **Data Privacy**: Simulation transcripts may contain test PII; handle accordingly
- **Retention Compliance**: Data retention must comply with customer agreements
