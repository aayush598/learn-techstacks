# Section 03: Deepgram API Integration

## Overview

Deepgram provides a cloud-based STT API with the Nova-2 model, offering industry-leading accuracy (8% word error rate on LibriSpeech) and real-time streaming capabilities. The API supports WebSocket streaming, custom vocabulary, language detection, and punctuation. For the AI voice agent platform, Deepgram serves as the primary cloud STT provider with automatic failover to Whisper.cpp.

Nova-2 is optimized for conversational speech, with particular strength in handling overlapping speech, filled pauses ("um", "uh"), and diverse accents. The API provides word-level timestamps, confidence scores, and speaker diarization out of the box.

## Architecture

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Client SDK  │───▶│  WebSocket   │───▶│  Deepgram    │───▶│  Results     │
│  (Node.js)   │    │  Connection  │    │  Nova-2 API  │    │  Callback    │
│              │    │  wss://...   │    │  (Cloud)     │    │  (streaming) │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
       │                    │                   │                   │
       │ Send audio chunks  │  Keepalive ping   │  Interim + final  │
       │ every 100ms        │  every 5s         │  transcript JSON  │
       ▼                    ▼                   ▼                   ▼
  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
  │  Audio       │    │  Connection  │    │  Model       │    │  Post-       │
  │  Buffer      │───▶│  Pool        │───▶│  Config      │───▶│  Process    │
  │  400ms       │    │  5 conns     │    │  language/   │    │  (punct/     │
  │              │    │  + fallback  │    │  vocab/...   │    │  format)     │
  └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

## Design Decisions

- **WebSocket for Streaming**: REST endpoints are used only for pre-recorded audio. All real-time interactions use WebSocket for sub-300ms end-to-end latency. The WebSocket connection is established before the first audio frame arrives (pre-connection) to eliminate setup latency.
- **Connection Pool**: Maintain a pool of 5 pre-established WebSocket connections per pod to handle concurrent transcription requests. Each connection can handle one transcription session at a time. Pool pressure triggers new connection creation.
- **Keepalive Strategy**: Send a keepalive message every 5 seconds to prevent idle timeout (Deepgram's timeout is 10s). Failure to receive a pong response triggers connection recycling.
- **Interim Results Policy**: Interim results are delivered every 300-500ms during speech. The final result is marked with `is_final: true`. The system uses final results for LLM consumption and interim results for display/barge-in detection.

## Implementation Approach

```typescript
import { createClient, LiveClient } from '@deepgram/sdk';

interface DeepgramConfig {
  apiKey: string;
  model: 'nova-2' | 'nova-2-general';
  language: string;
  interimResults: boolean;
  punctuation: boolean;
  utteranceSplit: boolean;
  endpointing: number; // ms of silence to trigger endpoint
  encoding: 'linear16';
  sampleRate: 16000;
}

class DeepgramProvider implements STTProvider {
  private pool: LiveClient[] = [];
  private config: DeepgramConfig;

  async *transcribe(audio: AudioStream): AsyncIterable<TranscriptChunk> {
    const conn = await this.acquireConnection();
    const resultStream = conn.stream();
    const audioProducer = this.sendAudio(conn, audio);

    for await (const msg of resultStream) {
      if (msg.type === 'Results') {
        yield {
          text: msg.channel.alternatives[0].transcript,
          isFinal: msg.is_final,
          confidence: msg.channel.alternatives[0].confidence,
          words: msg.channel.alternatives[0].words,
          startTime: msg.start,
          endTime: msg.duration,
        };
      }
    }
  }

  private async sendAudio(conn: LiveClient, audio: AudioStream): Promise<void> {
    for await (const frame of audio) {
      conn.send(frame.toBuffer());
    }
    conn.finish();
  }

  private async acquireConnection(): Promise<LiveClient> {
    return this.pool.pop() ?? this.createConnection();
  }
}
```

## Integration Points

- **API Key Management**: Deepgram API keys stored in HashiCorp Vault with automatic rotation. Keys are scoped per tenant for usage tracking.
- **Usage-Based Cost Attribution**: Each transcription request is tagged with tenant ID, call ID, and model type for cost allocation.
- **Fallback Chain**: Deepgram → Whisper.cpp → Web Speech API. Failure detection based on HTTP 4xx/5xx, WebSocket close codes, and latency >2x p50.

## Open-Source Tools

- **@deepgram/sdk** (MIT): Official Node.js SDK with TypeScript types.
- **deepgram-cli** (MIT): CLI tool for testing and debugging.

## Production Considerations

- **Rate Limits**: Deepgram has tiered rate limits (Starter: 10 concurrent, Pro: 100+, Enterprise: custom). Monitor `X-RateLimit-Remaining` headers.
- **Latency**: Nova-2 average streaming latency is ~300ms p50. Setup pre-connection to avoid WebSocket handshake overhead.
- **Cost**: ~$0.004 per minute for Nova-2. Reserved capacity discounts available at 1M+ minutes/month.
- **Data Residency**: Deepgram offers GCP, AWS, and Azure regions. Choose region matching tenant data residency requirements for GDPR/HIPAA.
- **Error Handling**: WebSocket disconnect triggers immediate reconnection. Unprocessed audio buffered during reconnect (max 2s buffer to avoid memory pressure).
