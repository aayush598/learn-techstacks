# Section 02: k6 Test Scripts & Configuration

## Overview

k6 is the primary load testing tool for the voice AI platform. Test scripts are version-controlled alongside application code, enabling load testing as code. Scripts model the complete call lifecycle: initiating calls, maintaining WebSocket connections during active calls, sending audio data, and terminating calls. Custom metrics capture platform-specific behaviors like STT latency, LLM response time, and call completion rate.

## Design Decisions

- **Test as Code**: Load test scripts in git alongside application code
- **Custom Metrics**: Platform-specific metrics beyond HTTP timings
- **Scenario-Based Testing**: Different test scenarios for different load profiles
- **Parameterized Configuration**: Environment-specific settings via environment variables
- **CI Integration**: k6 runs as a CI job with JUnit output

## Implementation Approach

```javascript
import { Trend, Rate } from 'k6/metrics';

const sttLatency = new Trend('stt_latency_ms');
const llmLatency = new Trend('llm_latency_ms');
const ttsLatency = new Trend('tts_latency_ms');
const callSuccess = new Rate('call_success_rate');

export const options = {
  scenarios: {
    ramp_up: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 50 },
        { duration: '5m', target: 50 },
        { duration: '2m', target: 100 },
        { duration: '5m', target: 100 },
        { duration: '2m', target: 0 },
      ],
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<500'],
    stt_latency_ms: ['p(95)<300'],
    llm_latency_ms: ['p(95)<800'],
    call_success_rate: ['rate>0.99'],
  },
};

export default function () {
  const callId = initiateCall();
  if (!callId) return;
  const ws = new WebSocket(`wss://api.example.com/v1/calls/${callId}/stream`);
  ws.on('open', () => {
    for (let i = 0; i < 10; i++) {
      ws.send(JSON.stringify({ type: 'audio', data: generateAudioChunk(), timestamp: Date.now() }));
      sleep(0.5);
    }
  });
  ws.on('message', (data) => {
    const msg = JSON.parse(data);
    if (msg.type === 'stt_result') sttLatency.add(msg.latency);
    if (msg.type === 'agent_response') llmLatency.add(msg.llm_latency);
  });
}
```

## Integration Points

- **CI Pipeline**: Automated load test execution
- **Grafana Dashboard**: Real-time metric visualization
- **Slack Alerts**: Threshold breach notifications

## Open-Source Tools

- **k6** (AGPL 3.0): Load testing
- **xk6-output-prometheus** (AGPL 3.0): Prometheus output
- **k6-reporter** (MIT): HTML report generation

## Production Considerations

- **Test Data**: Generate realistic but safe test data
- **Result Storage**: Store historical results for trend analysis
