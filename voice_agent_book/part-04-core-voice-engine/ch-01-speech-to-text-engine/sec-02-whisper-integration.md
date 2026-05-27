# Section 02: Whisper Integration

## Overview

OpenAI's Whisper is the gold standard for open-source STT, supporting 99 languages with near-commercial accuracy. The platform integrates Whisper in two modes: OpenAI Cloud API for simplicity and Whisper.cpp for self-hosted cost control and data privacy. Both share a unified provider interface.

Whisper models range from `tiny` (39M params, ~1GB) to `large-v3` (1.5B params, ~10GB). For real-time voice, `base` (74M) or `small` (244M) offer optimal accuracy-to-speed. Whisper.cpp adds GGML quantization (2-8 bit) and efficient C++ CPU inference.

## Architecture

```
Audio Stream ──▶ Audio Buffer ──▶ Whisper.cpp ──▶ Decoded Text
(16kHz PCM)     30s window       Inference        + Timestamps
                 2s overlap       Engine
                                      │
                          ┌───────────▼───────────┐
                          │ Model: tiny/base/small │
                          │ medium/large + quant   │
                          └───────────────────────┘
```

## Design Decisions

- **Self-Hosted > API for Volume**: At >100k mins/month, self-hosted saves ~60% ($0.002 vs $0.006/min). Trade-off: operational overhead.
- **q5_0 Quantization**: 2x speedup with <1% WER increase. q8_0 for near-lossless at 1.5x. 2-3 bit quant offers 4x but degrades accuracy 5-8%.
- **Sliding Window**: 30s segments with 2s overlap prevent boundary splits. Overlap deduplicated via timestamp comparison.
- **Instance Pool**: 1 Whisper instance per CPU core, managed via semaphore. Overflow requests queued.

## Implementation Approach

```typescript
class WhisperProvider implements STTProvider {
  private pool: WhisperInstance[];
  private semaphore: Semaphore;

  async *transcribe(stream: AudioStream): AsyncIterable<TranscriptChunk> {
    const buf = new RingBuffer(30 * 16000); // 30s at 16kHz
    for await (const frame of stream) {
      buf.push(frame);
      if (buf.duration >= 30) {
        const seg = buf.read(Math.max(0, buf.length - 2 * 16000));
        const release = await this.semaphore.acquire();
        try {
          const result = await this.getInstance().transcribe(seg);
          yield* this.dedup(result);
        } finally { release(); }
      }
    }
  }
}
```

## Integration Points

- **Model Registry**: Versioned S3 bucket. Downloaded at container start.
- **GPU Orchestration**: NVIDIA MPS for GPU sharing. Max 4 instances per T4.
- **Monitoring**: Track inference time, queue depth, memory. Alert at p99 >500ms.

## Open-Source Tools

- **Whisper.cpp** (MIT): ggerganov/whisper.cpp. CPU-optimized C++ inference.
- **faster-whisper** (MIT): CTranslate2-based. 4x faster than original Python Whisper.
- **whisperX** (BSD-2): Word timestamps + speaker diarization.

## Production Considerations

- **Cold Start**: Model load 2-8s. Pre-warm instances with keep-alive.
- **Memory**: tiny=0.5GB, base=1.2GB, small=2.5GB, medium=5GB, large=10GB.
- **Concurrency**: 8-core pod handles ~60 concurrent streams (p50:150ms per 30s window).
- **Auto-scaling**: Model load average >80% triggers scale-up.

## Additional Production Guidance

### GPU vs CPU Decision Matrix
| Scenario | Recommendation | Cost/hr | Throughput |
|----------|---------------|---------|------------|
| <50 concurrent | CPU (8 vCPU, q5_0) | ~$0.20 | 50 streams |
| 50-200 concurrent | GPU (T4, q8_0) | ~$0.35 | 200 streams |
| >200 concurrent | Multi-GPU (A10G) | ~$1.00 | 800 streams |

### Model Update Strategy
Whisper models improve with each release. Maintain a canary deployment where 5% of traffic uses the new model. Compare WER on a held-out test set of 1000 utterances. Promote when WER improves >1% relative.

### Security Considerations
- Models stored encrypted at rest (AES-256)
- Model files integrity-checked via SHA-256 before loading
- Audio data never persisted unless call recording enabled
- API keys for cloud Whisper rotated every 30 days

### Fallback Behavior
When Whisper.cpp fails to load the model (corrupt file, OOM), the system falls back to:
1. Deepgram API (cloud, pay-per-use)
2. Web Speech API (browser-native, limited accuracy)
3. Return error to caller with "I'm having trouble hearing you" message

