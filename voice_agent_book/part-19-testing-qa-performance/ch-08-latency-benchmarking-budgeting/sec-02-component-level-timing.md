# Section 02: Component-Level Timing

## Overview

Component-level timing breaks down the E2E latency into per-stage measurements. Each stage in the voice pipeline has its own timing characteristics and optimization opportunities. Understanding timing at this granularity enables targeted optimization efforts.

## Latency Budget

| Component | Target p50 | Target p95 | Notes |
|-----------|-----------|-----------|-------|
| VAD Detection | 20ms | 50ms | Voice activity detection |
| Audio Buffering | 30ms | 60ms | Network jitter buffer |
| STT Processing | 200ms | 400ms | Speech-to-text inference |
| Intent Classification | 50ms | 100ms | NLP intent matching |
| LLM Response | 500ms | 1000ms | Language model inference |
| TTS Generation | 150ms | 300ms | Text-to-speech synthesis |
| Audio Playback | 50ms | 100ms | Audio buffer to speaker |
| **Total** | **~1000ms** | **~2000ms** | |

## Implementation Approach

```typescript
interface StageTiming {
  stage: 'vad' | 'buffering' | 'stt' | 'intent' | 'llm' | 'tts' | 'playback';
  startTime: number;
  endTime: number;
  metadata?: Record<string, unknown>;
}

class ComponentTimer {
  private stages: StageTiming[] = [];

  start(stage: StageTiming['stage'], metadata?: Record<string, unknown>): void {
    this.stages.push({ stage, startTime: performance.now(), endTime: 0, metadata });
  }

  end(stage: StageTiming['stage']): void {
    const s = this.stages.find(s => s.stage === stage && s.endTime === 0);
    if (s) s.endTime = performance.now();
  }

  report(): ComponentTimingReport {
    return {
      stages: this.stages.map(s => ({
        stage: s.stage,
        duration: s.endTime - s.startTime,
        metadata: s.metadata,
      })),
      total: this.stages.reduce((sum, s) => sum + (s.endTime - s.startTime), 0),
    };
  }

  async measure<T>(stage: StageTiming['stage'], fn: () => Promise<T>): Promise<T> {
    this.start(stage);
    try { return await fn(); } finally { this.end(stage); }
  }
}

// Usage
const timer = new ComponentTimer();
const response = await timer.measure('stt', () => sttService.transcribe(audio));
```

## Integration Points

- **Prometheus Histograms**: Per-stage latency distributions
- **Grafana Dashboards**: Stage-by-stage latency breakdown
- **Alerting**: Individual stage budget violations trigger alerts

## Open-Source Tools

- **process.hrtime** (Node.js): High-resolution timing
- **performance.now()** (Web API): Browser/client timing
- **OpenTelemetry** (Apache 2.0): Span creation per stage

## Production Considerations

- **Measurement Overhead**: Minimize instrumentation in hot paths
- **Statistical Significance**: Single measurements are noisy; aggregate across calls
- **Correlation**: Correlate component timings with infrastructure metrics
