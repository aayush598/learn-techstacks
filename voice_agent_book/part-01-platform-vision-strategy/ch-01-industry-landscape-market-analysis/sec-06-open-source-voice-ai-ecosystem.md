# Section 06: Open-Source Voice AI Ecosystem

## Ecosystem Overview

The open-source voice AI ecosystem has matured significantly in the last 2-3 years. It now supports production-grade speech-to-text, text-to-speech, voice activity detection, and LLM orchestration. This creates a viable alternative to proprietary platforms for teams with engineering capability.

```
Open-Source Voice AI Stack
┌──────────────────────────────────────────────────────────────┐
│                     Application Layer                        │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │ LangChain   │  │ LlamaIndex   │  │ Haystack          │  │
│  │ Orchestrate │  │ RAG Pipeline │  │ Search/QA         │  │
│  └─────────────┘  └──────────────┘  └───────────────────┘  │
├──────────────────────────────────────────────────────────────┤
│                   AI/ML Model Layer                          │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │ Whisper     │  │ Coqui TTS    │  │ Silero VAD        │  │
│  │ STT         │  │ Voice Clone  │  │ Voice Detection   │  │
│  └─────────────┘  └──────────────┘  └───────────────────┘  │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │ Llama 3     │  │ Qdrant       │  │ Sentence-         │  │
│  │ LLM         │  │ Vector DB    │  │ Transformers      │  │
│  └─────────────┘  └──────────────┘  └───────────────────┘  │
├──────────────────────────────────────────────────────────────┤
│                 Communications Layer                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │ LiveKit     │  │ SIP.js       │  │ WebRTC            │  │
│  │ WebRTC Infra│  │ SIP Client   │  │ Transport Layer   │  │
│  └─────────────┘  └──────────────┘  └───────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

## Core Open-Source Components

### Speech-to-Text: Whisper
**License:** MIT. **Model sizes:** tiny (39M) to large (1.5B). **Accuracy:** 95.2% WER on LibriSpeech. **GPU requirement:** 1GB (tiny) to 10GB (large). **Alternatives:** DeepSpeech (Mozilla, Apache 2.0, older architecture), Coqui STT (BSD, needs more training data). **Production consideration:** Whisper large is the gold standard but requires GPU inference. Use tiny for real-time streaming with accuracy trade-off.

### Text-to-Speech: Coqui TTS
**License:** MIT + CPML. **Features:** Voice cloning (5 seconds of audio), 1400+ speaker models, multi-language. **Voice quality:** 4.2/5 MOS score (approaches human-level). **Alternatives:** Piper (fast, small footprint, Apache 2.0), Bark (Suno, MIT, highly expressive but slower), Silero TTS (MIT, reliable, 100+ languages). **Production consideration:** Coqui v2 with XTTS provides the best quality for voice cloning use cases.

### Voice Activity Detection: Silero VAD
**License:** MIT. **Accuracy:** 99%+ detection rate at 3% false positive. **Latency:** <50ms on CPU. **Model size:** 1.1MB. **Alternatives:** WebRTC VAD (BSD, lightweight, less accurate), rVAD (MIT, research-grade). **Production consideration:** Silero is the clear winner — fast, accurate, tiny footprint. Use in pre-roll and end-of-speech detection.

### LLM Orchestration: LangChain
**License:** MIT. **Community:** 200k+ GitHub stars, 5k+ contributors. **Features:** Chain composition, agent patterns, RAG support, tool calling. **Alternatives:** LlamaIndex (narrower focus on data indexing), Haystack (production pipeline focus). **Production consideration:** LangChain evolves rapidly — pin versions and expect breaking changes in minor versions.

## Cost Comparison: Open-Source vs Proprietary

```
Cost per 10,000 Call Minutes
┌───────────────────────────────────────────────────────────────────┐
│ Component        │ Open-Source     │ Proprietary     │ Savings    │
├───────────────────────────────────────────────────────────────────┤
│ STT              │ $8 (GPU cost)   │ $50 (Deepgram)  │ 84%        │
│ TTS              │ $4 (GPU cost)   │ $30 (ElevenLabs)│ 87%        │
│ LLM              │ $15 (self-host) │ $80 (OpenAI)    │ 81%        │
│ VAD              │ $0              │ $5              │ 100%       │
│ Communications   │ $0 (WebRTC)     │ $20 (Twilio)    │ 100%       │
├───────────────────────────────────────────────────────────────────┤
│ Total            │ $27             │ $185            │ 85%        │
└───────────────────────────────────────────────────────────────────┘
```

## Integration & API Design

```typescript
interface OpenSourceVoicePipeline {
  stt: {
    model: 'whisper-tiny' | 'whisper-base' | 'whisper-large';
    provider: 'local-gpu' | 'groq' | 'replicate';
    sampleRate: 16000;
    language: string;
    vad: 'silero' | 'webrtc' | 'none';
  };
  llm: {
    model: 'llama3-8b' | 'llama3-70b' | 'mistral-7b' | 'qwen-72b';
    provider: 'local' | 'together' | 'groq' | 'anyscale';
    temperature: number;
    maxTokens: number;
  };
  tts: {
    model: 'coqui-xtts' | 'piper' | 'bark';
    voice: string;
    speed: number;
    emotion: 'neutral' | 'happy' | 'sympathetic';
  };
  telephony: {
    provider: 'twilio' | 'telnyx' | 'signalwire' | 'plivo';
    protocol: 'sip' | 'webrtc' | 'pstn';
    codec: 'opus' | 'pcmu' | 'pcma';
  };
}

async function processCall(
  audioStream: ReadableStream,
  pipeline: OpenSourceVoicePipeline
): Promise<CallResult> {
  const vad = createSileroVAD();
  const segments = await vad.detectSegments(audioStream);
  
  const transcribed = await whisperSTT(segments, {
    model: pipeline.stt.model,
    language: pipeline.stt.language,
  });

  const response = await llm.invoke(transcribed, {
    model: pipeline.llm.model,
    temperature: pipeline.llm.temperature,
  });

  return synthesizeSpeech(response, pipeline.tts);
}
```

## Community Ecosystem

**GitHub activity:** 500+ voice AI repos with >100 stars. **Top repos:** Whisper (70k+ stars), Coqui TTS (35k+), Silero VAD (5k+). **Community channels:** Hugging Face (model hosting), Discord (developer chat), Reddit r/voicetechnology. **Maintenance risk:** Coqui (company closed in 2024, community fork active), Whisper (maintained by OpenAI), Llama (Meta, well-resourced).

## Build vs. Buy Decision Framework

**When to build (open-source):** You have ML engineering capability, want full control, have compliance requirements (HIPAA/hosted models), need customization, have scale >100k calls/month. **When to buy (proprietary):** You need quick time-to-market, lack ML engineering resources, have low-moderate call volume, don't need deep customization.

## Production Considerations

- GPU orchestration using Kubernetes with GPU node pools
- Model caching with Redis to avoid cold starts
- Graceful degradation if GPU OOM — fallback to smaller models
- Monitor model drift with periodic evaluation datasets
- A/B test model changes with traffic splitting
- Local model hosting saves 60-80% vs API costs at scale
- Build in model registry for version management and rollbacks
