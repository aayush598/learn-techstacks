# Section 01: End-to-End Latency Measurement

## Overview

End-to-end latency measurement captures the total time from when a user speaks to when they hear the agent's response. This round-trip includes audio capture, VAD detection, STT processing, LLM inference, TTS generation, and audio playback. Accurate measurement requires timestamp correlation across all pipeline stages and clock synchronization between distributed services.

## Architecture

```
Latency Breakdown:
User Speaks → [Audio Capture → VAD → STT → LLM → TTS → Audio Playback]
                 50ms       20ms   200ms  500ms   150ms     50ms
                 
Total E2E Latency: ~970ms (p50), ~1500ms (p95)
Budget: 1200ms (p95)
```

## Design Decisions

- **Distributed Tracing**: Correlation IDs link spans across services
- **Clock Synchronization**: NTP-synchronized clocks across all servers
- **Timestamp Origin**: Use TAI (International Atomic Time) for precision
- **Per-Stage Instrumentation**: Each pipeline stage emits timing metrics
- **End-to-End Probes**: Synthetic calls measure real user experience

## Implementation Approach

```typescript
class LatencyTracker {
  private spans: Map<string, Span[]> = new Map();

  startSpan(traceId: string, stage: string): void {
    if (!this.spans.has(traceId)) this.spans.set(traceId, []);
    this.spans.get(traceId)!.push({ stage, startTime: this.now(), endTime: 0 });
  }

  endSpan(traceId: string, stage: string): void {
    const spans = this.spans.get(traceId);
    const span = spans?.find(s => s.stage === stage && s.endTime === 0);
    if (span) span.endTime = this.now();
  }

  getLatencyBreakdown(traceId: string): StageLatency[] {
    return (this.spans.get(traceId) || []).map(s => ({
      stage: s.stage,
      duration: s.endTime - s.startTime,
    }));
  }

  getE2ELatency(traceId: string): number {
    const spans = this.spans.get(traceId) || [];
    if (spans.length === 0) return 0;
    const firstStart = Math.min(...spans.map(s => s.startTime));
    const lastEnd = Math.max(...spans.map(s => s.endTime));
    return lastEnd - firstStart;
  }

  private now(): number {
    return performance.now(); // High-resolution timestamp
  }
}
```

## Integration Points

- **OpenTelemetry**: Traces exported to Tempo/Jaeger
- **Prometheus**: Latency metrics aggregated
- **Grafana Dashboards**: Real-time latency visualization

## Open-Source Tools

- **OpenTelemetry** (Apache 2.0): Distributed tracing
- **Jaeger** (Apache 2.0): Trace visualization
- **Grafana Tempo** (AGPL 3.0): Trace storage
- **NTP** (Public Domain): Clock synchronization

## Production Considerations

- **Clock Skew**: Even small clock differences cause inaccurate measurements
- **Sampling**: 100% tracing at scale is expensive; use adaptive sampling
- **Measurement Overhead**: Instrumentation adds latency; minimize in hot paths
