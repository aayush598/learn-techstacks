# Section 02: Voice Agent Sandbox Playground

## Overview

The sandbox playground is a web-based interface where developers can interact with their voice agent in real time. It provides text input, audio recording, and simulated voice conversation, with live transcripts, debug output, and TTS preview. The playground is embedded in the developer portal and pre-configured with the developer's sandbox API key.

## Architecture

```
Sandbox Playground UI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────────┐
│ Sandbox Playground                                      │
│                                                          │
│ ┌─────────────┐  ┌─────────────────────────────────────┐│
│ │ Agent Config  │  │ Conversation Panel                  ││
│ │              │  │                                     ││
│ │ Voice: Emma  │  │ [Caller] Hi, I'd like to order...  ││
│ │ Language: en │  │ [Agent] I can help with that!       ││
│ │ TTS: Neural  │  │ [Caller] My address is...           ││
│ │              │  │ [Agent] Got it, shipping to...      ││
│ │ [Reset]      │  │                                     ││
│ └─────────────┘  │ [🎤 Record] [Send] [Step Through]   ││
│                   └─────────────────────────────────────┘│
│ ┌────────────────────────────────────────────────────────┐│
│ │ Debug Panel                                            ││
│ │                                                        ││
│ │ [NLU] Intent: place_order (confidence: 0.98)          ││
│ │ [NLU] Entities: {product: "laptop", quantity: 1}      ││
│ │ [Dialog] Current state: address_collection             ││
│ │ [Knowledge] Query: shipping policy → result found     ││
│ │ [Latency] STT: 120ms | NLU: 45ms | TTS: 200ms         ││
│ │                                                        ││
│ │ [Copy Transcript] [Download Audio] [Share Scenario]   ││
│ └────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

## Design Decisions

- **Text-First, Voice-Optional**: Default to text input; voice recording on demand
- **Live Debug Panel**: Real-time visibility into NLU, dialog, and latency
- **Session-Independent**: Each playground session is isolated from others
- **Config Presets**: Quick-switch between agent configurations

## Implementation Approach

```typescript
// Sandbox playground React component
interface SandboxConfig {
  agentId: string;
  voice: string;
  language: string;
  ttsEngine: 'neural' | 'standard';
}

function SandboxPlayground({ config }: { config: SandboxConfig }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [debugEvents, setDebugEvents] = useState<DebugEvent[]>([]);
  const [inputText, setInputText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [session, setSession] = useState<WebSocket | null>(null);

  useEffect(() => {
    const ws = new WebSocket(`wss://sandbox.voiceagent.com/v1/simulate?agent_id=${config.agentId}`);

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      switch (data.type) {
        case 'transcript':
          setMessages(prev => [...prev, {
            role: data.role,
            text: data.text,
            timestamp: data.timestamp,
          }]);
          break;
        case 'debug':
          setDebugEvents(prev => [...prev, {
            component: data.component,
            event: data.event,
            details: data.details,
            latencyMs: data.latency_ms,
          }]);
          break;
        case 'latency':
          setDebugEvents(prev => [...prev, {
            component: 'pipeline',
            event: 'latency_report',
            details: data.breakdown,
          }]);
          break;
      }
    };

    setSession(ws);
    return () => ws.close();
  }, [config.agentId]);

  async function sendMessage(text: string) {
    setIsProcessing(true);
    session?.send(JSON.stringify({
      type: 'input',
      text,
      mode: 'text',
      timestamp: Date.now(),
    }));
    setInputText('');
    setIsProcessing(false);
  }

  async function startVoiceRecording() {
    setIsRecording(true);
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const recorder = new RecordRTC(stream, { type: 'audio' });
    recorder.startRecording();

    // Send audio chunks via WebSocket
    recorder.onAudioProcess = (blob) => {
      session?.send(JSON.stringify({
        type: 'input',
        audio: blob,
        mode: 'audio',
        timestamp: Date.now(),
      }));
    };
  }

  return (
    <div className="sandbox-playground">
      <div className="playground-header">
        <ConfigSelector config={config} />
        <button onClick={() => setMessages([])}>Reset Session</button>
        <button onClick={() => setDebugEvents([])}>Clear Debug</button>
      </div>

      <div className="playground-body">
        <ConversationPanel messages={messages} />

        <div className="input-area">
          <button
            className={`record-btn ${isRecording ? 'recording' : ''}`}
            onClick={isRecording ? stopVoiceRecording : startVoiceRecording}
          >
            {isRecording ? '⏹ Stop' : '🎤 Record'}
          </button>
          <input
            type="text"
            value={inputText}
            onChange={e => setInputText(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && sendMessage(inputText)}
            placeholder="Type a message to simulate..."
            disabled={isProcessing}
          />
          <button onClick={() => sendMessage(inputText)} disabled={isProcessing || !inputText}>
            Send
          </button>
          <button onClick={stepForward}>Step Forward</button>
        </div>

        <DebugPanel events={debugEvents} />
      </div>
    </div>
  );
}

// Debug panel component
function DebugPanel({ events }: { events: DebugEvent[] }) {
  return (
    <div className="debug-panel">
      <h3>Debug Output</h3>
      <div className="debug-stream">
        {events.map((event, i) => (
          <div key={i} className={`debug-entry ${event.component}`}>
            <span className="debug-timestamp">
              {new Date(event.timestamp).toISOString().slice(11, 23)}
            </span>
            <span className="debug-component">[{event.component}]</span>
            <span className="debug-event">{event.event}</span>
            <span className="debug-details">{JSON.stringify(event.details)}</span>
            {event.latencyMs && (
              <span className="debug-latency">{event.latencyMs}ms</span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

// Latency visualization
function LatencyBreakdown({ breakdown }: { breakdown: LatencyBreakdown }) {
  const total = breakdown.stt + breakdown.nlu + breakdown.dialog + breakdown.knowledge + breakdown.tts;

  return (
    <div className="latency-breakdown">
      <div className="latency-bar">
        {Object.entries(breakdown).map(([stage, ms]) => (
          <div
            key={stage}
            className={`latency-segment ${stage}`}
            style={{ width: `${(ms / total) * 100}%` }}
            title={`${stage}: ${ms}ms`}
          />
        ))}
      </div>
      <div className="latency-legend">
        <span className="legend-item stt">STT {breakdown.stt}ms</span>
        <span className="legend-item nlu">NLU {breakdown.nlu}ms</span>
        <span className="legend-item dialog">Dialog {breakdown.dialog}ms</span>
        <span className="legend-item knowledge">Knowledge {breakdown.knowledge}ms</span>
        <span className="legend-item tts">TTS {breakdown.tts}ms</span>
      </div>
    </div>
  );
}
```

## Integration Points

- **Agent API**: WebSocket connection for real-time simulation
- **Developer Portal**: Embedded in dashboard for authenticated developers
- **Browser APIs**: WebRTC for audio recording, WebSocket for streaming

## Production Considerations

- **Session Limits**: Maximum 30-minute playground sessions
- **Rate Limits**: 10 requests per minute in sandbox mode
- **Audio Processing**: Client-side audio encoding before transmission
- **Session Persistence**: Playground state preserved on page reload

## Open-Source Tools

- **RecordRTC**: Browser audio recording library
- **WaveSurfer.js**: Audio waveform visualization
- **D3.js**: Latency breakdown visualization
