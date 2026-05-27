# Section 04: Real-Time Streaming STT

## Overview

Real-time streaming STT is the backbone of conversational AI voice agents. Unlike batch transcription, streaming STT must deliver partial results as audio is being captured, with tightly bounded latency. This enables natural conversation flow - the system can display live captions, detect interruptions, and prepare LLM responses before the user finishes speaking.

The streaming architecture uses WebSocket connections to deliver audio chunks (typically 20-100ms of audio per frame) and receive incremental transcription results. The system must handle network jitter, varying audio chunk sizes, and graceful degradation when the connection is interrupted.

## Architecture

```
┌──────┐  audio chunks  ┌──────────┐  WebSocket   ┌──────────┐  interim   ┌──────────┐
│ User │───────────────▶│  Audio   │─────────────▶│  STT     │──────────▶│  Result  │
│ Mic  │  every 80ms    │  Buffer  │  wss://...   │  Cloud   │  results   │  Handler │
└──────┘                │  400ms   │              │  API     │  every     │          │
                        └──────────┘              └──────────┘  300-500ms │  ┌───────▼───────┐
                                                                          │  │ Barge-In      │
                                                                          │  │ Detection     │
                                                                          │  └───────────────┘
                                                                          │  ┌───────▼───────┐
                                                                          │  │ Transcript   │
                                                                          │  │ Display       │
                                                                          │  └───────────────┘
```

## Design Decisions

- **Chunk Size**: 80ms audio chunks (1280 samples at 16kHz) balance network overhead vs latency. Smaller chunks increase WebSocket frame overhead; larger chunks increase latency.
- **Interim Result Suppression**: Low-confidence interim results (<0.6 confidence) are suppressed to avoid flickering in displays and false barge-in triggers. Only final results are sent to the LLM.
- **Utterance Segmentation**: The API uses endpoint detection (silence threshold: 500ms) to segment speech into utterances. Each utterance triggers a final result. This prevents the LLM from receiving partial thoughts.
- **Backpressure Management**: If the STT API is slower than real-time, audio frames are buffered (max 2s) and then dropped oldest-first. A warning metric is emitted when buffer exceeds 1s.

## Implementation Approach

```typescript
import WebSocket from 'ws';

interface StreamingConfig {
  url: string;
  apiKey: string;
  sampleRate: number;
  channels: number;
  encoding: 'linear16' | 'mulaw';
  interimResults: boolean;
  endpointing: number;
}

class StreamingSTT {
  private ws: WebSocket;
  private config: StreamingConfig;
  private buffer: AudioFrame[] = [];
  private readonly MAX_BUFFER_MS = 2000;

  async connect(): Promise<void> {
    this.ws = new WebSocket(this.config.url, {
      headers: { Authorization: `Token ${this.config.apiKey}` }
    });

    // Send streaming config as first message
    this.ws.send(JSON.stringify({
      type: 'Configure',
      ...this.config
    }));
  }

  async sendAudio(frame: AudioFrame): Promise<void> {
    this.buffer.push(frame);
    const bufferMs = this.getBufferDuration();

    if (bufferMs > this.MAX_BUFFER_MS) {
      const excess = Math.ceil((bufferMs - this.MAX_BUFFER_MS) / 80);
      this.buffer.splice(0, excess);
      console.warn('STT buffer overflow, dropping', excess, 'frames');
    }

    this.ws.send(frame.toBuffer());
  }

  async *results(): AsyncIterable<TranscriptChunk> {
    for await (const msg of this.ws) {
      const parsed = JSON.parse(msg.toString());
      if (parsed.type === 'Results') {
        yield {
          text: parsed.channel.alternatives[0].transcript,
          isFinal: parsed.is_final,
          confidence: parsed.channel.alternatives[0].confidence,
        };
      }
    }
  }

  async disconnect(): Promise<void> {
    this.ws.close(1000, 'Session complete');
  }

  private getBufferDuration(): number {
    return this.buffer.reduce((sum, f) => sum + f.durationMs, 0);
  }
}
```

## Integration Points

- **Turn Detection**: Streaming STT's endpoint detection marks utterance boundaries. The turn management system uses these to determine when the user has finished speaking.
- **Barge-In (P4 Ch 06)**: Interim results with high confidence (>0.8) that contain directive phrases ("stop", "wait", "actually...") trigger barge-in.
- **Memory Buffer (P5 Ch 02)**: Final utterances are appended to conversation memory. The buffer maintains last 3 utterances for context continuity.

## Open-Source Tools

- **ws** (MIT): Lightweight WebSocket client/server for Node.js.
- **@deepgram/sdk** (MIT): Streaming client with reconnect logic.

## Production Considerations

- **Reconnection**: Implement exponential backoff (100ms, 250ms, 500ms, 1s) for WebSocket reconnection. Buffer audio during reconnect (max 2s). Missed audio beyond 2s triggers full utterance restart.
- **Network Jitter**: Client-side timestamp each audio frame. Server uses timestamps to reconstruct correct ordering if frames arrive out of order.
- **Monitoring**: Track WebSocket message latency (p50/p99), reconnect count, buffer overflow events, and interim-to-final ratio. Alert on reconnect count >5/min.
- **Scaling**: Each WebSocket connection consumes ~1MB memory. Plan pod memory accordingly. 1000 concurrent streams require ~1GB for connections alone.
