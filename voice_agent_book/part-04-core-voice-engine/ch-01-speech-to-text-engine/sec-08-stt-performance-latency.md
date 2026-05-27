# Section 08: STT Performance & Latency

## Overview

STT latency directly impacts the naturalness of voice conversations. The total interaction budget for an AI voice agent is ~500ms: STT (200ms), LLM reasoning (200ms), TTS (100ms). Any STT latency beyond 200ms creates an awkward pause that users perceive as "the agent is thinking too long."

This section covers techniques to achieve sub-200ms STT latency: model quantization, edge inference, connection pooling, audio preprocessing optimization, and adaptive model selection based on network conditions.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Latency Budget Breakdown                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Audio capture: 20ms  VAD: 10ms  Codec: 5ms  STT: 200ms    │
│  ├────────────────────┼─────────┼──────────┼─────────────┤ │
│  │  Audio Pipeline    │  VAD    │  Normaliz│  ASR Model   │ │
│  │  (20ms buffering)  │  (10ms) │  (5ms)   │  (150-200ms) │ │
│  └────────────────────┴─────────┴──────────┴─────────────┘ │
│                                                             │
│  Total: ~235ms (under 500ms budget)                         │
└─────────────────────────────────────────────────────────────┘
```

## Design Decisions

- **Model Quantization**: q5_0 quantization reduces Whisper inference time by 50% with <1% accuracy loss. For edge deployment, q4_0 offers 3x speedup with 2% WER increase.
- **GPU Acceleration**: NVIDIA T4 GPU reduces Whisper inference from 300ms to 80ms per 30s window. Use CUDA MPS for concurrent model sharing.
- **Connection Pooling**: Pre-establish WebSocket connections to STT APIs. Average handshake time: 150ms. Pool eliminates this per-call overhead.
- **Adaptive Model Selection**: Monitor CPU/GPU utilization and queue depth. If latency >200ms for 3 consecutive calls, switch to smaller model (small → base).

## Implementation Approach

```typescript
interface STTLatencyMonitor {
  measure(): Promise<STTLatencyReport>;
  shouldDowngrade(): boolean;
}

class AdaptiveSTT {
  private currentModel: string = 'small';
  private latencyHistory: number[] = [];

  async selectModel(): Promise<string> {
    const avgLatency = this.getAverageLatency();
    if (avgLatency > 200 && this.currentModel !== 'base') {
      this.currentModel = 'base';
      console.log('Downgrading to base model due to latency');
    } else if (avgLatency < 100 && this.currentModel !== 'medium') {
      this.currentModel = 'medium';
      console.log('Upgrading to medium model (latency headroom)');
    }
    return this.currentModel;
  }

  private getAverageLatency(): number {
    return this.latencyHistory.slice(-10).reduce((a, b) => a + b, 0) / 10;
  }
}
```

## Integration Points

- **Auto-scaling**: STT latency >200ms triggers pod scale-up. Use custom HPA metric `stt_latency_p99`.
- **Quality Monitoring (P4 Ch 10)**: Track STT latency as a key quality metric. Alert if p99 exceeds 350ms.

## Open-Source Tools

- **Whisper.cpp Quantization**: Multiple quantization levels (q2_k to q8_0).
- **TensorRT** (NVIDIA): GPU inference optimization for Whisper.
- **ONNX Runtime**: Cross-platform inference optimization.

## Production Considerations

- **Benchmarking**: Establish baseline latency per model/quantization: tiny=80ms, base=120ms, small=200ms, medium=400ms, large=800ms (CPU).
- **Batching**: For post-call batch transcription, batch size 8 achieves 4x throughput vs single inference.
- **Instance Sizing**: t3.large (2 vCPU) handles 30 concurrent streams with base model. g4dn.xlarge (T4 GPU) handles 200 concurrent streams.
- **Cold Start Mitigation**: Warm instances with 5 pre-loaded models. Use "keep-warm" Lambda function to prevent scaling to zero.

## Additional Production Guidance

### End-to-End Latency Budget Breakdown
```
Component         Budget    p50 Actual    p99 Actual    Optimization
----------------------------------------------------------------------
Audio capture     20ms      15ms          25ms          -
VAD processing    10ms      5ms           15ms          Silero ONNX
Audio normalize   5ms       3ms           8ms           Kaiser window
STT inference     200ms     150ms         350ms         q5_0 quantized
Post-processing   15ms      10ms          25ms          BERT-tiny
Network RTT       50ms      20ms          100ms         Edge deployment
----------------------------------------------------------------------
Total             300ms     203ms         523ms         -
```

### Adaptive Model Selection Algorithm
```typescript
class AdaptiveModelSelector {
  select(): ModelType {
    const load = this.systemMonitor.getCpuLoad();
    const latency = this.latencyTracker.p99();
    
    if (load > 80 || latency > 300) return 'tiny';
    if (load > 60 || latency > 200) return 'base';
    if (latency < 100) return 'medium'; // upgrade if headroom
    return 'small';
  }
}
```

### Auto-scaling Rules
| Metric | Threshold | Action | Cooldown |
|--------|-----------|--------|----------|
| STT latency p99 | >350ms for 2min | Scale up +1 pod | 5min |
| Queue depth | >100 for 1min | Scale up +2 pods | 3min |
| CPU utilization | >80% for 3min | Scale up +1 pod | 5min |
| All metrics normal | <50% for 10min | Scale down -1 pod | 10min |

### Cost Optimization Strategies
- Spot instances for GPU workers (save 60-70%)
- Reserved capacity for baseline (save 30% vs on-demand)
- Model caching: keep 5 most-used models loaded
- Batch post-call transcription with larger models on spot

