# Section 03: Voicemail Drop Strategy

## Overview

Voicemail drop is the process of playing a pre-recorded message when a call is answered by voicemail rather than by a human. Unlike traditional telemarketing where the agent leaves a voicemail manually, automated voicemail drop detects the voicemail greeting, waits for the beep, and plays a targeted message — all without human involvement. The strategy must precisely time the message delivery to avoid cutting off the greeting or playing over the beep.

A well-executed voicemail drop increases contact rates by delivering the campaign message even when the contact is unavailable. Studies show that voicemail messages from automated systems can achieve 20-40% callback rates when well-crafted. The strategy must handle different voicemail greeting formats (standard, extended absence, full mailbox), different beep patterns, and the possibility that the greeting never ends (some systems have very long greetings).

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Audio    |--->| WebSocket|--->| Jitter   |--->| PLC      |--->| Player   |
| Producer |    | (WSS)    |    | Buffer   |    | (Packet  |    | (smooth  |
| (100ms   |    | (binary) |    | (adaptive|    |  Loss    |    |  output) |
|  chunks) |    |          |    |  60-200) |    |  Conceal)|    +----------+
+----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```
class VoicemailDropEngine {
  constructor(audioPlayer, dtmfDetector) {
    this.audioPlayer = audioPlayer;
    this.dtmf = dtmfDetector;
    this.config = {
      postBeepDelay: 300, // ms to wait after beep
      minGreetingDuration: 1000, // ms minimum greeting before beep search
      beepFrequencies: [440, 480, 520, 620, 950, 1000],
      listenAfterMessage: 3000, // ms to wait for DTMF after message
    };
  }

  async executeVoicemailDrop(callSid, message, amdResult) {
    // Phase 1: Wait for greeting to complete and detect beep
    const beepResult = await this.waitForBeep(callSid, amdResult);
    
    if (!beepResult.beepDetected) {
      // Fallback: if no beep detected within timeout, play message anyway
      await this.audioPlayer.play(callSid, message.audioRef);
      return { outcome: 'no_beep_fallback', messagePlayed: true };
    }

    // Phase 2: Small pause after beep for natural spacing
    await this.sleep(this.config.postBeepDelay);

    // Phase 3: Play the message
    const playResult = await this.audioPlayer.play(callSid, message.audioRef);

    if (!playResult.completed) {
      return { outcome: 'interrupted', messagePlayed: false, reason: playResult.reason };
    }

    // Phase 4: Optional - listen for DTMF response
    if (message.interactive) {
      const dtmfResult = await this.listenForDTMF(callSid, this.config.listenAfterMessage);
      
      if (dtmfResult.digit) {
        return {
          outcome: 'dtmf_received',
          dtmf: dtmfResult.digit,
          messagePlayed: true,
          action: this.resolveDTMFAction(dtmfResult.digit, message)
        };
      }
    }

    return { outcome: 'completed', messagePlayed: true };
  }

  async waitForBeep(callSid, amdResult) {
    return new Promise((resolve) => {
      let audioBuffer = [];
      const startTime = Date.now();
      const timeout = 10000; // Max 10 seconds to wait for beep
      
      // Subscribe to audio stream
      const subscription = this.subscribeAudio(callSid, (chunk) => {
        audioBuffer.push(chunk);
        const audioData = this.concatenateAudio(audioBuffer);

        // Check if we have enough audio
        if (this.getDuration(audioData) < this.config.minGreetingDuration) {
          return;
        }

        // Analyze for beep tone
        const beepCheck = this.detectBeepTone(audioData);
        
        if (beepCheck.detected) {
          subscription.unsubscribe();
          resolve({
            beepDetected: true,
            beepTimestamp: beepCheck.timestamp,
            greetingDuration: this.getDuration(audioData) - beepCheck.timestamp,
            confidence: beepCheck.confidence
          });
        }
      });

      // Timeout
      setTimeout(() => {
        subscription.unsubscribe();
        resolve({
          beepDetected: false,
          greetingDuration: this.getDuration(audioBuffer),
          reason: 'timeout'
        });
      }, timeout);
    });
  }

  detectBeepTone(audioData) {
    // FFT-based beep detection
    const fftSize = 2048;
    const spectrum = this.fft(audioData, fftSize);
    
    // Look for energy at known beep frequencies
    for (let i = 0; i < spectrum.length; i++) {
      const frequency = (i * this.sampleRate) / fftSize;
      
      if (this.config.beepFrequencies.some(f => Math.abs(frequency - f) < 20)) {
        const magnitude = Math.abs(spectrum[i]);
        const avgMagnitude = spectrum.reduce((s, v) => s + Math.abs(v), 0) / spectrum.length;
        
        if (magnitude > avgMagnitude * 3) {
          // Check duration of the tone
          const toneDuration = this.measureToneDuration(audioData, frequency);
          if (toneDuration > 100 && toneDuration < 800) { // Beeps are typically 200-500ms
            return {
              detected: true,
              frequency,
              timestamp: this.estimateBeepStart(audioData, frequency),
              confidence: Math.min(1.0, magnitude / (avgMagnitude * 5))
            };
          }
        }
      }
    }

    return { detected: false };
  }

  async listenForDTMF(callSid, durationMs) {
    return new Promise((resolve) => {
      const subscription = this.dtmf.subscribe(callSid, (digit) => {
        subscription.unsubscribe();
        resolve({ digit, timestamp: Date.now() });
      });

      setTimeout(() => {
        subscription.unsubscribe();
        resolve({ digit: null, reason: 'timeout' });
      }, durationMs);
    });
  }
}
```

## Integration Points

- **AMD Engine (sec-01, sec-02):** Provides the machine classification that triggers voicemail drop
- **Audio Player:** Plays pre-recorded messages via the telephony provider's media API
- **DTMF Detector:** Captures touch-tone responses for interactive voicemail
- **Message Library (sec-04):** Stores and manages pre-recorded messages
- **Call Progress Analysis (sec-07):** Monitors call state during voicemail playback
- **Campaign Analytics (Ch 09):** Tracks voicemail drop rates, callback rates, message effectiveness
- **AI Agent (Part 06):** Optionally, the AI agent can handle post-voicemail interactions

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Beep detection is critical — missing the beep means the message plays over the greeting; a false beep means the message cuts off the greeting
- Voicemail greetings vary internationally — French greetings are typically longer; Japanese voicemail has different beep characteristics
- Some voicemail systems have no beep (especially mobile voicemail in some countries) — implement a no-beep fallback
- Voicemail message length should be 15-20 seconds for optimal callback rates
- Interactive voicemail (press 1 to connect) adds compliance considerations — must include opt-out option
- Monitor voicemail drop success rate — a sudden drop may indicate carrier changes or AMD degradation
- A/B test voicemail messages — different openings, lengths, and CTAs produce different callback rates
- Voicemail messages must include the business name and purpose per TCPA requirements
- Consider "voicemail as a service" — some providers offer specialized voicemail drop APIs
- Message playback should be monitored for abrupt disconnections — the system should detect if the call is dropped during playback
