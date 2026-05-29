# Section 03: Voice Processing Pipeline

## Pipeline Architecture

The voice processing pipeline is the **core audio pathway** that transforms raw audio from phone calls or WebRTC streams into text, processes it through an AI engine, and generates spoken responses. This is the most latency-sensitive component of the entire system.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         VOICE PROCESSING PIPELINE                       │
│                                                                         │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐       │
│  │  Audio   │     │  Voice   │     │   STT    │     │   AI     │       │
│  │  Source  │────▶│  Activity│────▶│(Speech to│────▶│Orchestr. │       │
│  │          │     │  Detect  │     │  Text)   │     │  Engine  │       │
│  └──────────┘     └──────────┘     └──────────┘     └────┬─────┘       │
│       │                                                    │            │
│       │ Voice Activity Detection                           │            │
│       │ - Silero VAD                                       │            │
│       │ - Noise suppression                                │            │
│       │ - Endpoint detection                               │            │
│       │                                                    │            │
│  ┌────┴──────┐                                             │            │
│  │   Audio   │     ┌──────────┐     ┌──────────┐           │            │
│  │  Mixer    │◀────│   TTS    │◀────│ Response │◀──────────┘            │
│  │           │     │(Text to  │     │  Formatter│                        │
│  │           │     │  Speech) │     │           │                        │
│  └──────────┘     └──────────┘     └──────────┘                         │
│       │                                                                  │
│       ▼                                                                  │
│  ┌──────────┐     ┌──────────┐                                          │
│  │  Output  │     │Recording │                                          │
│  │  Stream  │     │  Store   │                                          │
│  │(WebRTC)  │     │ (MinIO)  │                                          │
│  └──────────┘     └──────────┘                                          │
└─────────────────────────────────────────────────────────────────────────┘

Audio Flow Timeline:
Time ────────────────────────────────────────────────────────────────►
User:  "Hello, I need help with my order"
       │───────VAD────────►│───────STT─────────►│
       │                                        │
       │              "Hello, I need help with my order"
       │                                        │
       │                              ┌─────────┴─────────┐
       │                              │  AI Processing...  │
       │                              │  ~200-500ms       │
       │                              └─────────┬─────────┘
       │                                        │
       │    "I'd be happy to help you with your order!"
       │◄────────TTS────────────│◄──────────────┘
       │◄──────Audio Out────────│
```

## Component Details

### 1. Audio Source
Audio enters the pipeline from one of two paths:
- **WebRTC**: Browser or mobile app sends Opus-encoded audio via WebRTC peer connection to the media server
- **SIP/PSTN**: Traditional phone calls arrive via SIP trunking, transcoded to Opus by the media server

```
interface AudioSource {
  type: 'webrtc' | 'sip' | 'file'
  codec: 'opus' | 'pcmu' | 'pcma' | 'g722'
  sampleRate: 8000 | 16000 | 48000
  channels: 1 | 2
  sourceId: string         // Call ID or stream ID
  metadata: Record<string, unknown>
}
```

### 2. Voice Activity Detection (VAD)
VAD determines when someone is speaking. We use **Silero VAD**, a pre-trained PyTorch model that provides state-of-the-art voice detection with minimal latency.

```typescript
interface VADConfig {
  model: 'silero_v4'
  threshold: number          // 0.0-1.0, default 0.5
  minSpeechDurationMs: number // 100ms
  minSilenceDurationMs: number // 500ms — end of utterance
  windowSizeMs: number       // 30ms processing window
  sampleRate: 16000
}

interface VADEvent {
  type: 'speech_start' | 'speech_end' | 'silence'
  timestamp: number
  energy: number
  duration: number
}
```

### 3. Speech-to-Text (STT)
We use **OpenAI Whisper** (large-v3) for transcription, with optimizations:

```typescript
interface STTConfig {
  model: 'whisper-large-v3'
  language: 'en' | 'es' | 'fr' | 'de' | 'ja' | 'zh' | 'auto'
  beamSize: number           // 5 for accuracy, 1 for speed
  wordTimestamps: boolean    // Enable word-level timing
  vadFilter: boolean         // Use VAD results for silence trimming
  computeType: 'float16' | 'int8'  // Quantization for speed
}

interface STTResult {
  text: string
  segments: Array<{
    start: number
    end: number
    text: string
    confidence: number
    words: Array<{
      word: string
      start: number
      end: number
      probability: number
    }>
  }>
  language: string
  duration: number
}
```

**Optimization Strategies:**
- **Streaming mode**: Process audio in 5-second chunks with overlap
- **GPU acceleration**: Run on NVIDIA T4 or A10G GPUs
- **Quantization**: INT8 quantization reduces latency by 40% with minimal accuracy loss
- **Batched inference**: Combine multiple streams on a single GPU

### 4. AI Orchestration Engine
The AI engine receives transcribed text and determines the response:

```typescript
interface AIRequest {
  text: string
  conversationId: string
  agentId: string
  context: {
    previousTurns: Array<{ role: 'user' | 'assistant', text: string }>
    agentConfig: AgentConfig
    knowledgeBase: Array<KnowledgeDoc>
    callData: CallMetadata
  }
}

interface AIResponse {
  text: string
  actions?: Array<{
    type: 'transfer' | 'end_call' | 'schedule_callback' | 'send_email'
    params: Record<string, unknown>
  }>
  emotions?: 'neutral' | 'empathetic' | 'urgent'
  metadata: {
    tokensUsed: number
    latencyMs: number
    model: string
  }
}
```

### 5. Text-to-Speech (TTS)
Generated text is converted to speech using **Coqui TTS** or a cloud provider:

```typescript
interface TTSConfig {
  engine: 'coqui-tts' | 'elevenlabs' | 'azure'
  voice: string              // Voice ID
  speed: number              // 0.5-2.0
  pitch: number              // -20 to +20 semitones
  emotion: 'neutral' | 'happy' | 'calm' | 'urgent'
  sampleRate: 24000
  format: 'wav' | 'mp3' | 'opus'
}
```

### 6. Audio Mixer & Output
The audio mixer combines TTS output with any hold music, beeps, or announcements. It also handles:
- **Barge-in**: If the user interrupts, the mixer attenuates TTS output
- **Comfort noise**: Generate background noise to avoid dead air
- **Volume normalization**: Consistent output levels across calls

## Design Decisions and Trade-offs

| Decision | Choice | Trade-off |
|----------|--------|-----------|
| STT Engine | Whisper large-v3 vs Deepgram | Whisper is self-hosted (privacy), Deepgram has lower latency |
| TTS Engine | Coqui TTS vs ElevenLabs | Coqui is free/open-source, ElevenLabs sounds more natural |
| VAD | Silero VAD vs WebRTC VAD | Silero is more accurate, WebRTC is lighter |
| Media Server | Janus vs Mediasoup | Janus has more features (recording, SIP), Mediasoup is more performant |
| Audio Codec | Opus vs PCM | Opus has better compression, PCM has lower latency |
| Streaming vs Chunked | Streaming for real-time, chunked for archival | Streaming adds complexity, chunked is simpler |

## Integration Points

- **Part 04 (Core Voice Engine)** — This section introduces the pipeline; Part 04 implements it
- **Part 05 (AI Conversation)** — AI Orchestration Engine consumes STT output
- **Part 07 (Telephony)** — SIP/PSTN integration feeds audio into this pipeline
- **Part 12 (Recording)** — Recordings are captured from the media server

## Production Considerations

- **Latency Budget**: Total pipeline latency must be under 800ms for natural conversation
  - VAD: <20ms
  - STT: <300ms (streaming)
  - AI: <300ms (with streaming response)
  - TTS: <200ms (streaming)
- **GPU Allocation**: Each GPU handles 10-15 concurrent streams
- **Fallback Strategy**: If STT fails, fall back to a cloud provider (Deepgram/Google STT)
- **Monitoring**: Track per-component latency, audio quality scores, error rates
- **Scaling**: Auto-scale voice service pods based on active call count and queue depth
- **Recording**: All audio is recorded to MinIO for compliance and quality assurance
