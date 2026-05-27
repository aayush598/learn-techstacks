# Section 03: Concurrent Call Simulation

## Overview

Concurrent call simulation is the most critical load testing capability. Each concurrent call represents a real-time audio stream flowing through the voice pipeline (VAD → STT → LLM → TTS). Simulating hundreds of simultaneous calls stresses the media processing infrastructure, WebSocket connections, and AI service integrations.

## Design Decisions

- **Real Audio Streams**: Simulate actual WebSocket audio, not just HTTP requests
- **Call Duration Distribution**: Mix of short (<1min), medium (1-5min), and long (>5min) calls
- **Geographic Distribution**: Simulate calls from multiple regions
- **Random Inter-arrival Times**: Poisson process for realistic call arrival patterns

## Implementation Approach

```javascript
import { WebSocket } from 'k6/experimental/websockets';
import { Trend, Rate } from 'k6/metrics';

const callSetupTime = new Trend('call_setup_ms');
const callCompletionRate = new Rate('call_completed');

export function simulateCall(agentId, duration) {
  const startTime = Date.now();
  const setupRes = http.post(`${BASE_URL}/v1/calls`, JSON.stringify({
    agentId, phoneNumber: generatePhoneNumber(), maxDuration: duration,
  }));
  callSetupTime.add(Date.now() - startTime);
  if (setupRes.status !== 201) { callCompletionRate.add(false); return; }
  
  const callId = setupRes.json('callId');
  const ws = new WebSocket(`${WS_URL}/v1/calls/${callId}/stream`);
  
  let audioReceived = 0, errors = 0;
  ws.on('open', () => {
    const interval = setInterval(() => {
      if (audioReceived >= duration * 10) {
        clearInterval(interval);
        ws.send(JSON.stringify({ type: 'end_call' }));
        return;
      }
      ws.send(JSON.stringify({ type: 'audio', data: generateAudioChunk(), sequence: audioReceived++ }));
    }, 100);
  });
  ws.on('message', (data) => {
    const msg = JSON.parse(data);
    if (msg.type === 'error') errors++;
  });
  ws.on('close', () => callCompletionRate.add(errors === 0));
}

export default function () {
  const duration = [30, 60, 120, 300][Math.floor(Math.random() * 4)];
  simulateCall(__ENV.AGENT_ID || 'load-test-agent', duration);
  sleep(Math.random() * 10 + 1);
}
```

## Integration Points

- **Voice Pipeline**: Tests end-to-end audio processing
- **WebSocket Infrastructure**: Validates WebSocket scaling
- **Media Servers**: Tests media processing capacity

## Open-Source Tools

- **k6** (AGPL 3.0): WebSocket simulation
- **GStreamer** (LGPL-2.0): Audio generation
- **FFmpeg** (GPL-2.0): Audio file manipulation

## Production Considerations

- **Audio File Size**: Generated audio chunks must be realistic but not excessive
- **WebSocket Connections**: Each VU opens a WebSocket; manage file descriptor limits
