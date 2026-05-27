# Section 01: STT Architecture Overview

## Overview

The Speech-to-Text (STT) engine is the voice entry point for the AI agent pipeline. It converts raw audio streams into structured text for NLU and LLM processing. The architecture must deliver real-time streaming transcription with under 200ms end-to-end latency while maintaining high accuracy across diverse languages, accents, and acoustic environments.

A production-grade STT pipeline has five stages: audio capture and pre-processing, Voice Activity Detection (VAD) gating to filter silence, audio codec normalization to 16kHz mono PCM, ASR inference via configurable providers (Whisper, Deepgram, Google), and text post-processing for punctuation, capitalization, and formatting. Each stage is independently scalable and hot-swappable.

## Architecture

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Audio In    │   │  VAD Gate    │   │  Audio Codec │   │  ASR Engine  │   │Post-Processor │
│ (WebRTC/SIP) │──▶│ (Silero/     │──▶│ (Resample to │──▶│ (Whisper/    │──▶│ (Punct/Cap/   │
│ 48kHz stereo │   │  WebRTC VAD) │   │  16kHz mono) │   │  Deepgram)   │   │  Filter)      │
└──────────────┘   └──────────────┘   └──────────────┘   └──────┬───────┘   └──────┬───────┘
                                                                │                   │
                                                                ▼                   ▼
                                                         ┌──────────────┐   ┌──────────────┐
                                                         │  Provider    │   │  Formatted   │
                                                         │  Abstraction │──▶│  Text Out    │
                                                         │  Layer       │   │  + Metadata  │
                                                         └──────────────┘   └──────────────┘
```

## Design Decisions

- **Provider Abstraction Layer**: All STT providers implement a common `STTProvider` interface. This decouples the pipeline from any single vendor and enables seamless failover. The abstraction adds ~3ms overhead per request but eliminates vendor lock-in.
- **VAD Gating**: Audio is only sent to ASR when speech is detected, reducing costs by 40-60%. VAD miss rate must be <1%, requiring careful threshold tuning.
- **Streaming First**: Prioritizes WebSocket streaming over batch for real-time. Interim results every 200-500ms enable barge-in detection and live transcripts.
- **Audio Normalization**: All input normalized to 16kHz/16-bit/mono PCM via high-quality Kaiser-window resampling (64 taps) for consistent ASR quality.

## Implementation Approach

```typescript
interface STTProvider {
  transcribe(audio: ReadableStream<AudioFrame>, opts?: STTOptions): AsyncIterable<TranscriptChunk>;
  transcribeFile(file: Buffer, opts?: STTOptions): Promise<FinalTranscript>;
}

class STTEngine {
  private providers: Map<string, STTProvider>;
  private vad: VADProcessor;

  async *transcribe(audio: AudioStream): AsyncIterable<TranscriptChunk> {
    for await (const segment of this.vad.filter(audio)) {
      const norm = await normalizeAudio(segment, 16000);
      try {
        yield* this.providers.get('primary')!.transcribe(norm);
      } catch (err) {
        yield* this.providers.get('fallback')!.transcribe(norm);
      }
    }
  }
}
```

## Integration Points

- **VAD (Ch 03)**: Gates audio before STT; aggressive VAD causes "first word eaten" issues.
- **Audio Pipeline (Ch 04)**: Normalization runs before STT; corrupt frames must be caught.
- **Barge-In (Ch 06)**: Interim STT results drive interruption detection; low-confidence results suppressed.
- **LLM Context (P5 Ch 02)**: Final STT appended to conversation memory; word timestamps enable TTS sync.

## Open-Source Tools

- **Whisper.cpp** (MIT): C++ Whisper with GGML quantization. 35k+ GitHub stars.
- **Deepgram SDK** (MIT): Nova-2 model with <300ms streaming latency.
- **Vosk** (Apache 2.0): Offline STT for air-gapped deployments.
- **SoX**: Audio sample rate conversion and format normalization.

## Production Considerations

- **Latency**: STT ≤200ms of 500ms budget. p50 <150ms, p99 <350ms.
- **Cost**: Self-hosted Whisper.cpp ~$0.002/min vs Deepgram ~$0.004/min. Hybrid saves 40-60%.
- **GPU**: Whisper.cpp runs CPU-only (q5_0: ~5GB RAM). For >100 concurrent streams, use T4 GPU.
- **Error Handling**: Exponential backoff (100/250/500ms) then failover. Track error rates per provider.
- **Model Mgmt**: Versioned S3 storage. Pre-warm during startup. A/B test model versions.
