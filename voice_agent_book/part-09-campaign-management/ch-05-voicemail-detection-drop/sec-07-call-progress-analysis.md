# Section 07: Call Progress Analysis

## Overview

Call Progress Analysis (CPA) is the technology that detects and interprets telephony network signals during call setup and after answer. Unlike Answering Machine Detection (AMD), which classifies the answering party as human or machine, CPA detects network-level events: busy signals, ring-no-answer, SIT (Special Information Tones), fax/modem carrier tones, operator intercept messages, network congestion messages, and disconnected number recordings. CPA operates in the first 5-15 seconds of call establishment and provides the essential "what happened to this call" answer that drives dialer decision-making.

Modern CPA systems must handle hundreds of different tone patterns across global telecommunications networks. SIT tones vary by country and carrier — the US uses a three-tone sequence at specific frequencies (950Hz, 1400Hz, 1800Hz), while other countries may use different frequencies and patterns. Carrier-specific intercept messages add further complexity: "The number you have dialed is not in service" sounds different across carriers, regions, and languages. CPA systems use a combination of spectral analysis, tone detection, and ASR-transcribed message analysis to achieve >99% classification accuracy.

## Architecture

```
                      Call Progress Analysis Pipeline
                      
+---------+     +-----------+     +------------+     +-----------+
| Audio   |---->| Tone      |---->| State      |---->| Decision  |
| Stream  |     | Detector  |     | Machine    |     | Engine    |
+---------+     +-----------+     +------------+     +-----------+
     |               |                |                    |
     |    +----------+                |                    |
     |    | SIT Tone  |               |                    |
     |    | Matcher   |               |                    |
     |    | (950/1400 |               |                    |
     |    |  /1800Hz) |               |                    |
     |    +----------+                |                    |
     |               |                |                    |
     |    +----------+                |                    |
     |    | Busy Tone |               |                    |
     |    | Detector  |               |                    |
     |    | (cadence  |               |                    |
     |    |  match)   |               |                    |
     |    +----------+                |                    |
     |               |                |                    |
     |    +----------+                |                    |
     +----| ASR      |----------------+                    |
     |    | (message |                                     |
     |    |  detect) |                                     |
     |    +----------+                                     |
     |                                                     |
     +-----------------------------------------------------+
                              |
                              v
                    +------------------+
                    | Call Outcome:    |
                    | - Answered       |
                    | - Busy           |
                    | - No Answer      |
                    | - SIT/Disconnected|
                    | - Fax/Modem      |
                    | - Intercept      |
                    +------------------+
```

## Design Decisions

- **Tone detection before ASR:** Tone detection (SIT, busy, fax) is orders of magnitude faster and cheaper than ASR. CPA processes tones in the first 1-3 seconds and only falls back to ASR for ambiguous cases. Trade-off: tone detection may misclassify unusual patterns, but ASR latency (2-5 seconds) would slow down all calls.

- **Carrier-specific profile system:** Different carriers use different SIT tone frequencies, busy signal cadences, and intercept message patterns. A profile system maps carrier → detection parameters. Trade-off: requires ongoing maintenance as carriers change their networks, but significantly improves accuracy.

- **State machine with configurable transitions:** CPA uses a deterministic state machine with clear transitions: RINGING → CONNECTED → ANALYZING → CLASSIFIED. Each state has configurable timeouts. Trade-off: rigid state machine vs. flexibility, but predictability is essential for dialer coordination.

- **Confidence-based fallback to AMD:** When CPA cannot determine call outcome (confidence < 0.7), the system falls back to AMD analysis. Trade-off: additional processing time vs. improved classification accuracy.

## Implementation Approach

```
enum CallState {
  IDLE,
  RINGING,
  CONNECTED,
  ANALYZING,
  CLASSIFIED,
  TIMEOUT,
  ERROR
}

enum CallOutcome {
  ANSWERED_HUMAN,
  ANSWERED_MACHINE,
  BUSY,
  NO_ANSWER,
  SIT_DISCONNECTED,
  FAX_MODEM,
  OPERATOR_INTERCEPT,
  NETWORK_CONGESTION,
  UNKNOWN
}

class CallProgressAnalyzer {
  constructor(carrierProfiles, amdEngine) {
    this.carrierProfiles = carrierProfiles;
    this.amdEngine = amdEngine;
    this.toneDetector = new ToneDetector();
    this.stateMachine = new StateMachine(CallState.IDLE);
    this.timeoutConfig = {
      ringTimeout: 30000,    // 30s max ringing
      analysisTimeout: 10000, // 10s for CPA analysis
      answerStabilityMs: 500  // 500ms stability check
    };
  }

  async analyzeCall(audioStream, callMetadata) {
    const carrier = callMetadata.carrier || 'default';
    const profile = this.carrierProfiles[carrier];

    this.stateMachine.transition(CallState.RINGING);

    // Phase 1: Ring-state analysis
    const ringResult = await this.analyzeRingPhase(audioStream, profile);

    if (ringResult.outcome === CallState.NO_ANSWER) {
      return { outcome: CallOutcome.NO_ANSWER, confidence: 0.95 };
    }

    if (ringResult.outcome === CallState.BUSY) {
      return { outcome: CallOutcome.BUSY, confidence: 0.95 };
    }

    // Phase 2: Post-connect analysis
    this.stateMachine.transition(CallState.CONNECTED);

    // Wait for audio stability
    await this.waitForStableAudio(audioStream);

    this.stateMachine.transition(CallState.ANALYZING);

    // Phase 3: Parallel detection
    const [toneResult, asrResult] = await Promise.all([
      this.analyzeTones(audioStream, profile),
      this.transcribeAudio(audioStream)
    ]);

    // Phase 4: Classify outcome
    const outcome = this.classifyOutcome(toneResult, asrResult, profile);

    this.stateMachine.transition(CallState.CLASSIFIED);

    // Phase 5: Confidence check — fallback to AMD if low
    if (outcome.confidence < 0.7 && outcome.outcome === CallOutcome.UNKNOWN) {
      const amdResult = await this.amdEngine.analyzeAudio(
        audioStream.getBuffer(),
        carrier
      );

      outcome.confidence = Math.max(outcome.confidence, amdResult.confidence * 0.8);
      outcome.outcome = this.mapAmdToOutcome(amdResult);
      outcome.amdFallbackUsed = true;
    }

    return outcome;
  }

  analyzeRingPhase(audioStream, profile) {
    // Monitor for ring-back tone pattern
    // Busy signal: fast cadence (0.5s on, 0.5s off)
    // Ring: slow cadence (2s on, 4s off)
    // SIT: three ascending tones then silence

    const ringPatterns = {
      busy: { cadence: { onMs: 500, offMs: 500 }, tolerance: 100 },
      ringback: { cadence: { onMs: 2000, offMs: 4000 }, tolerance: 500 },
      sitTone: { frequencies: [950, 1400, 1800], durationMs: 330, tolerance: 20 }
    };

    const ringBuffer = [];
    let totalSilenceMs = 0;
    let lastActivity = Date.now();

    while (this.stateMachine.current === CallState.RINGING) {
      const chunk = await audioStream.readChunk();
      const energy = this.computeEnergy(chunk);

      ringBuffer.push({
        energy,
        timestamp: Date.now(),
        spectrum: this.computeSpectrum(chunk)
      });

      // Check for SIT tones during ringing
      const sitMatch = this.detectSitTone(ringBuffer, ringPatterns.sitTone);
      if (sitMatch) {
        return {
          outcome: CallState.SIT_DETECTED,
          pattern: 'sit_tone',
          confidence: 0.98
        };
      }

      // Check for busy signal cadence
      const busyMatch = this.detectCadence(ringBuffer, ringPatterns.busy);
      if (busyMatch) {
        return {
          outcome: CallState.BUSY,
          pattern: 'busy_signal',
          confidence: 0.95
        };
      }

      // Check for ring timeout
      if (Date.now() - lastActivity > this.timeoutConfig.ringTimeout) {
        return {
          outcome: CallState.NO_ANSWER,
          pattern: 'timeout',
          confidence: 0.9
        };
      }

      // Detect answer (energy spike and sustained audio)
      if (energy > profile.answerThreshold && this.isSustainedAudio(audioStream)) {
        return {
          outcome: CallState.CONNECTED,
          pattern: 'answer',
          confidence: 0.8
        };
      }
    }
  }

  analyzeTones(audioStream, profile) {
    const toneResults = [];

    // SIT tone detection
    const sitResult = this.toneDetector.detectSit(
      audioStream,
      profile.sitFrequencies || [950, 1400, 1800]
    );

    // Fax/Modem carrier detection (CNG tone at 1100Hz)
    const faxResult = this.toneDetector.detectContinuousTone(
      audioStream,
      { frequency: 1100, durationMs: 500 }
    );

    // Busy tone detection (post-connect — some carriers connect before playing busy)
    const busyResult = this.toneDetector.detectBusyCadence(
      audioStream,
      profile.busyCadence
    );

    // Silence detection (disconnected line)
    const silenceResult = this.detectSilenceSequence(audioStream, {
      minSilenceMs: 5000,
      maxSpeechMs: 200
    });

    return {
      sitTone: sitResult,
      faxDetected: faxResult,
      busyTone: busyResult,
      disconnectedSilence: silenceResult,
      timestamp: Date.now()
    };
  }

  async transcribeAudio(audioStream) {
    // Use ASR to transcribe intercept messages
    const audioBuffer = audioStream.getBuffer();
    const transcription = await this.asrService.transcribe(audioBuffer, {
      model: 'nova-2',
      language: 'en',
      sampleRate: 8000
    });

    // Match against known intercept patterns
    const interceptPatterns = [
      /(not in service|disconnected|no longer in service)/i,
      /(has been changed|is not available|does not accept)/i,
      /(cannot be completed as dialed|incorrect number)/i,
      /(please hang up|try your call again|try again later)/i,
      /(this is a recording|operator|telephone company)/i
    ];

    return {
      text: transcription.text,
      confidence: transcription.confidence,
      interceptMatch: this.matchInterceptPatterns(
        transcription.text,
        interceptPatterns
      ),
      durationMs: audioBuffer.length / 8 // 8kHz sample rate
    };
  }

  classifyOutcome(toneResult, asrResult, profile) {
    // Weighted ensemble classification
    let outcomes = [];
    let weights = [];

    // Tone-based outcomes have high weight
    if (toneResult.sitTone.detected) {
      outcomes.push({
        outcome: CallOutcome.SIT_DISCONNECTED,
        subType: this.classifySitType(toneResult.sitTone)
      });
      weights.push(0.95);
    }

    if (toneResult.faxDetected) {
      outcomes.push({ outcome: CallOutcome.FAX_MODEM });
      weights.push(0.95);
    }

    if (toneResult.busyTone.detected) {
      outcomes.push({ outcome: CallOutcome.BUSY });
      weights.push(0.9);
    }

    // ASR-based outcomes
    if (asrResult.interceptMatch.matched) {
      outcomes.push({ outcome: CallOutcome.OPERATOR_INTERCEPT });
      weights.push(0.85);
    }

    // No clear signal — check for silence
    if (toneResult.disconnectedSilence.detected) {
      outcomes.push({ outcome: CallOutcome.SIT_DISCONNECTED });
      weights.push(0.7);
    }

    // Default to unknown
    if (outcomes.length === 0) {
      outcomes.push({ outcome: CallOutcome.UNKNOWN });
      weights.push(0.0);
    }

    // Pick highest weighted outcome
    const maxIdx = weights.indexOf(Math.max(...weights));

    return {
      outcome: outcomes[maxIdx].outcome,
      confidence: weights[maxIdx],
      subType: outcomes[maxIdx].subType,
      evidence: { tones: toneResult, asr: asrResult },
      classificationTimeMs: 0
    };
  }

  classifySitType(sitResult) {
    // SIT tone sequences indicate specific conditions:
    // 950+1400+1800: Vacant circuit / disconnected
    // 1400+1800+950: Reorder / congestion
    // 1800+950+1400: No circuit / temporary failure

    const freqSeq = sitResult.frequencies.join('+');
    const sitTypes = {
      '950+1400+1800': 'vacant_circuit',
      '1400+1800+950': 'reorder_congestion',
      '1800+950+1400': 'no_circuit',
      '950+1400+950': 'intercept'
    };

    return sitTypes[freqSeq] || 'unknown';
  }

  detectSitTone(buffer, pattern) {
    // Sliding window FFT to detect SIT tone sequence
    if (buffer.length < 3) return null;

    const toneSequence = [];

    for (const chunk of buffer) {
      const dominantFreq = this.findDominantFrequency(
        chunk.spectrum,
        pattern.tolerance
      );

      if (dominantFreq) {
        toneSequence.push(dominantFreq);
      }
    }

    // Check if toneSequence matches the expected pattern
    if (toneSequence.length >= 3) {
      const match = pattern.frequencies.every((freq, i) =>
        Math.abs(toneSequence[i] - freq) < pattern.tolerance
      );

      if (match) {
        return {
          detected: true,
          frequencies: toneSequence.slice(0, 3),
          confidence: 0.98
        };
      }
    }

    return { detected: false };
  }

  isSustainedAudio(audioStream) {
    // Check that audio energy stays above threshold for stability period
    const samples = [];
    const checkDurationMs = this.timeoutConfig.answerStabilityMs;
    const numSamples = Math.floor(checkDurationMs / 100); // 100ms chunks

    for (let i = 0; i < numSamples; i++) {
      const chunk = audioStream.readChunk();
      samples.push(this.computeEnergy(chunk) > this.energyThreshold);
    }

    // At least 80% of samples must have energy
    return samples.filter(Boolean).length / samples.length >= 0.8;
  }

  computeEnergy(audioChunk) {
    return audioChunk.reduce(
      (sum, sample) => sum + sample * sample, 0
    ) / audioChunk.length;
  }

  computeSpectrum(audioChunk) {
    const N = audioChunk.length;
    const spectrum = new Float32Array(N / 2);

    for (let k = 0; k < N / 2; k++) {
      let real = 0;
      let imag = 0;
      for (let n = 0; n < N; n++) {
        const angle = (2 * Math.PI * k * n) / N;
        real += audioChunk[n] * Math.cos(angle);
        imag -= audioChunk[n] * Math.sin(angle);
      }
      spectrum[k] = Math.sqrt(real * real + imag * imag);
    }

    return spectrum;
  }

  findDominantFrequency(spectrum, tolerance) {
    const sampleRate = 8000;
    const N = spectrum.length * 2;
    let maxMagnitude = 0;
    let dominantFreq = 0;

    for (let i = 0; i < spectrum.length; i++) {
      const freq = (i * sampleRate) / N;
      if (spectrum[i] > maxMagnitude) {
        maxMagnitude = spectrum[i];
        dominantFreq = freq;
      }
    }

    return maxMagnitude > this.magnitudeThreshold ? Math.round(dominantFreq) : null;
  }
}
```

## Integration Points

- **Dialing Engine (Ch 01):** CPA outcomes drive call disposition and retry logic
- **AMD Engine (sec-01, sec-02):** Fallback path when CPA confidence is low
- **Retry Logic (Ch 04):** SIT tone outcomes trigger "do not retry" decisions; busy triggers retry with backoff
- **Campaign Scheduling (Ch 03):** Ring-no-answer outcomes affect time-of-day optimization
- **Voicemail Drop (sec-03):** CPA confirmation of answer before voicemail message playback
- **Carrier Telephony (Part 07):** Carrier-specific CPA profiles for tone detection parameters
- **Analytics (Ch 09):** CPA accuracy rates by carrier, region, and call outcome

## Open-Source Tools

- **fft.js / DSP.js:** FFT computation for spectral analysis and tone detection
- **SpeexDSP:** Audio pre-processing (noise reduction, echo cancellation) for cleaner CPA
- **librosa (Python):** Reference implementation for audio feature extraction algorithms
- **Deepgram / Whisper Nova:** ASR for intercept message transcription
- **node-pcm / speaker:** Raw audio stream processing utilities
- **Porter-Stemmer:** Text pattern matching for intercept message classification

## Production Considerations

- CPA must complete within 3-5 seconds of answer to avoid delaying the caller experience
- SIT tone frequencies vary by country — maintain a global carrier frequency database
- VoIP carriers may inject or modify telephony signals — CPA must account for carrier-specific behavior
- Some carriers play intercept messages after connection, requiring both tone and ASR analysis
- False positive SIT detection (classifying human answer as SIT) is extremely damaging — tune thresholds conservatively
- CPA accuracy monitoring by carrier is essential — carrier network changes can break tone detection
- International calls have different ring cadences, busy signals, and intercept patterns
- Fax/modem detection prevents costly misdials and protects fax server resources
- Operator intercept detection feeds DNC compliance — repeated intercepts indicate disconnected/high-risk numbers
- Log raw audio samples for CPA failures to enable post-mortem analysis and model improvement
- CPA timeouts (30s ring, 10s analysis) prevent stuck calls from consuming dialer resources
- Consider running CPA and AMD in parallel for the fastest possible classification
- Carrier profile updates should be deployed via configuration, not code changes, for rapid response to network changes
