# Section 01: TTS Architecture Overview

## Overview

The Text-to-Speech (TTS) engine converts LLM-generated text responses into natural-sounding audio streams for playback to callers. The architecture must support sub-100ms first-byte latency, multiple voice profiles, emotion-aware prosody, and streaming playback. It is the final stage in the voice AI pipeline and directly impacts caller satisfaction.

The TTS pipeline has five stages: (1) SSML parsing and validation, (2) voice selection based on agent configuration and language, (3) text synthesis via Coqui TTS (self-hosted) or Piper TTS (edge), (4) emotion modulation to match conversation sentiment, and (5) streaming audio output with buffer management.

## Architecture

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│  Text In     │──▶│  SSML Parser │──▶│  Voice       │──▶│  Synthesizer │──▶│  Audio Out   │
│  (from LLM)  │   │  (validate/  │   │  Selector    │   │  (Coqui/     │   │  (streaming  │
│              │   │   transform) │   │  (lang/gender│   │   Piper)     │   │   playback)  │
└──────────────┘   └──────────────┘   │   /style)    │   └──────┬───────┘   └──────────────┘
                                       └──────────────┘          │
                                                           ┌──────▼───────┐
                                                           │  Emotion     │
                                                           │  Controller  │
                                                           │  (prosody    │
                                                           │   modulation)│
                                                           └──────────────┘
```

## Design Decisions

- **Dual-Provider Strategy**: Coqui TTS for primary synthesis with high-quality voices; Piper TTS for low-latency edge deployment (<50ms first byte). Fallback: browser Web Speech API.
- **Streaming Synthesis**: Begin playback as soon as first audio chunk is available. Target first-byte latency: <100ms. Use progressive chunking with 200ms audio chunks.
- **SSML Pipeline**: All text passes through SSML parser even without SSML tags. This normalizes numbers, dates, and abbreviations before synthesis.
- **Voice Pre-warming**: Keep 2 most-used voices pre-loaded in memory. Load new voices asynchronously. Cache synthesized audio for repeated phrases.

## Implementation Approach

```typescript
interface TTSProvider {
  synthesize(text: string, voice: string, opts?: TTSOptions): ReadableStream<AudioChunk>;
  getVoices(): Promise<Voice[]>;
}

interface TTSOptions {
  emotion?: 'neutral' | 'happy' | 'sympathetic' | 'urgent';
  rate?: number;  // 0.5 - 2.0
  pitch?: number; // -10 to +10 semitones
  ssml?: boolean;
}

class TTSEngine {
  async *speak(text: string, config: AgentTTSConfig): AsyncIterable<AudioChunk> {
    const processed = await this.preprocessText(text);
    const voice = this.selectVoice(config);
    const provider = this.getProvider(config.deployment);

    for await (const chunk of provider.synthesize(processed, voice, {
      emotion: await this.detectEmotion(text)
    })) {
      yield this.applyGain(chunk, config.volume);
    }
  }
}
```

## Integration Points

- **LLM (P5 Ch 01)**: Receives text responses. Can inject SSML tags for emphasis.
- **Emotion System (P5 Ch 04)**: Sentiment output modulates TTS prosody.
- **Streaming (P4 Ch 07)**: Audio chunks delivered via WebSocket to browser/SIP endpoint.

## Open-Source Tools

- **Coqui TTS** (MIT): High-quality neural TTS with voice cloning. 30+ languages.
- **Piper TTS** (MIT): Ultra-fast inference. Under 50ms first byte on Raspberry Pi.
- **eSpeak-NG** (GPL): Lightweight fallback TTS.

## Production Considerations

- **Latency**: Coqui TTS first byte: ~150ms GPU, ~300ms CPU. Piper: ~30ms CPU.
- **Caching**: Cache common phrases in Redis (greetings, hold music prompts). Hit rate: ~20%.
- **Voice Licensing**: Verify licensing for commercial use. Coqui TTS is MIT. Some voices may have restrictions.
- **Storage**: Generated audio not stored by default. Enable recording per tenant for quality monitoring.

## Additional Production Guidance

### Voice Selection Strategy
```typescript
interface VoiceSelector {
  selectVoice(config: AgentConfig, context: CallContext): string {
    // Priority: 1. Explicit config  2. Language match  3. Gender preference  4. Default
    if (config.voiceId) return config.voiceId;
    const langVoices = this.voiceDB.query({ language: context.language });
    if (config.gender) return langVoices.find(v => v.gender === config.gender);
    return langVoices[0]; // most popular voice
  }
}
```

### Quality Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| First-byte latency | <100ms | Time from text to first audio chunk |
| MOS score | >4.0 | ITU-T P.862 on 100-sample test set |
| Voice consistency | >95% | Same voice across entire call |
| Emotion accuracy | >85% | Human-rater agreement on emotion delivery |

### Caching Strategy
- **Static phrases**: Greetings, hold messages, "please hold" - cache indefinitely
- **Dynamic phrases**: Cache with TTL 300s (frequent patterns)
- **Cache key**: hash(text + voice_id + emotion + rate)
- **Storage**: Redis with LRU eviction, max 500MB
- **Hit rate target**: >20% for static, >5% for dynamic

### High Availability
- Dual TTS providers (Coqui + Piper) with automatic failover
- Health check: synthesize test phrase every 30s
- If Coqui fails 3x in 60s, switch to Piper for all requests
- Re-check Coqui health every 60s

