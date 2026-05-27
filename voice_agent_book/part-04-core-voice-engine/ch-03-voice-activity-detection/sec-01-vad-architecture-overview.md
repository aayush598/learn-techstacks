# Section 01: VAD Architecture Overview

## Overview

Voice Activity Detection (VAD) determines when a human is speaking vs. when there is silence or background noise. It is the gatekeeper of the ASR pipeline: accurate VAD reduces STT costs by 40-60% (silence isn't transcribed) and improves user experience by preventing the agent from interrupting. The VAD system must detect speech onset within 50ms and speech offset within 300ms to feel natural.

The architecture supports dual VAD engines: Silero VAD (ML-based, high accuracy) as primary and WebRTC VAD (threshold-based, low latency) as fallback. Both run locally in the media server to avoid network round trips.

## Architecture

```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ Audio Frame  │──▶│ VAD Engine   │──▶│ State Machine│──▶│ Gate Control │
│ (10ms,       │   │ (Silero/     │   │ (silence/    │   │ (open/close  │
│  16kHz PCM)  │   │  WebRTC)     │   │  speech/     │   │  for ASR)    │
└──────────────┘   └──────┬───────┘   │  endpoint)   │   └──────────────┘
                          │            └──────────────┘
                   ┌──────▼───────┐
                   │ Sensitivity  │
                   │  Threshold   │
                   │  Config      │
                   │  (per tenant)│
                   └──────────────┘
```

## Design Decisions

- **Silero VAD as Primary**: Pre-trained ONNX model with 98% accuracy. Runs in ~5ms per 30ms frame on CPU. Significantly more accurate than WebRTC VAD in noisy environments.
- **WebRTC VAD as Fallback**: Lightweight (1ms per frame). Used when CPU load exceeds 80% or Silero model fails to load.
- **State Machine**: Three states: SPEECH, SILENCE, ENDPOINT. Transition thresholds configurable per tenant. Hangover time (continue SPEECH state after last speech frame) prevents choppy detection.
- **Lookahead**: Buffer 150ms of audio before VAD decision to improve onset detection. This adds 150ms latency but reduces front-end clipping by 90%.

## Implementation Approach

```typescript
enum VADState { SILENCE, SPEECH, ENDPOINT }

interface VADConfig {
  threshold: number;      // Silero threshold (0-1, default: 0.5)
  minSpeechDuration: number; // ms, prevent noise bursts as speech
  minSilenceDuration: number; // ms, endpoint detection
  hangoverFrames: number; // frames to stay in SPEECH after last speech
}

class VADProcessor {
  private silero: SileroVAD;
  private state: VADState = VADState.SILENCE;
  private speechFrames = 0;
  private silenceFrames = 0;

  process(frame: Float32Array): VADState {
    const isSpeech = this.silero.predict(frame) > this.config.threshold;

    switch (this.state) {
      case VADState.SILENCE:
        if (isSpeech) {
          this.speechFrames++;
          if (this.speechFrames * 10 > this.config.minSpeechDuration) {
            this.state = VADState.SPEECH;
          }
        } else {
          this.speechFrames = 0;
        }
        break;
      case VADState.SPEECH:
        if (!isSpeech) {
          this.silenceFrames++;
          if (this.silenceFrames > this.config.hangoverFrames) {
            this.state = VADState.ENDPOINT;
          }
        } else {
          this.silenceFrames = 0;
        }
        break;
    }

    return this.state;
  }
}
```

## Integration Points

- **STT (Ch 01)**: VAD gates audio to STT. Reduces cost by 40-60%.
- **Barge-In (Ch 06)**: VAD state used alongside STT interim results for interruption detection.
- **Audio Pipeline (Ch 04)**: VAD receives pre-processed audio frames.

## Open-Source Tools

- **Silero VAD** (MIT): Pre-trained ONNX model. 98% accuracy. GitHub: snakers4/silero-vad.
- **WebRTC VAD** (BSD): Part of WebRTC source code. 5x faster than Silero but less accurate.
- **ONNX Runtime** (MIT): Cross-platform inference for Silero model.

## Production Considerations

- **Performance**: Silero VAD: 5ms per 30ms frame on 1 vCPU. WebRTC VAD: 1ms per frame.
- **Threshold Tuning**: Default threshold 0.5 works for clean audio. Noisy environments may need 0.3-0.4.
- **Min Speech Duration**: 100ms prevents keyboard clicks from triggering VAD. Adjust per use case.
- **Monitoring**: Track VAD state transitions per minute. Abnormal transition frequency (>20/min) may indicate noisy audio.
