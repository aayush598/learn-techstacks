# Section 01: AMD Technology Overview

## Overview

Answering Machine Detection (AMD) is the technology that determines whether a telephone call has been answered by a human or an answering machine/voicemail system. This distinction is critical for outbound campaigns — if an answering machine is detected, the system can either disconnect (to avoid leaving a message) or play a pre-recorded voicemail message. If a human answers, the call should be immediately connected to a live agent or AI agent.

AMD technology has evolved from simple heuristic approaches (silence detection, tone analysis) to sophisticated machine learning models that analyze audio features in real-time. Modern AMD systems process the first 2-5 seconds of audio after the call is answered, extracting acoustic features, detecting speech patterns, and classifying the answer type with high accuracy. The challenge is balancing accuracy against speed — the classification must happen quickly enough to avoid awkward silences with human answers.

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
class AmdEngine {
  constructor(modelService, carrierProfiles) {
    this.modelService = modelService;
    this.carrierProfiles = carrierProfiles;
    this.audioBuffer = new AudioBuffer();
    this.decisionThresholds = {
      human: 0.8, // >= 0.8 → definitely human
      machine: 0.7, // >= 0.7 → definitely machine
      uncertain: 0.4 // < 0.4 → need more audio or heuristic
    };
  }

  async analyzeAudio(audioChunk, carrier) {
    this.audioBuffer.addChunk(audioChunk);
    
    // Need minimum 2 seconds of audio
    if (this.audioBuffer.durationMs < 2000) {
      return { status: 'buffering', progress: this.audioBuffer.durationMs / 5000 };
    }

    // Pre-process
    const processed = this.preprocess(this.audioBuffer.getAudio());

    // Extract features
    const features = this.extractFeatures(processed);

    // ML model classification
    const mlResult = await this.modelService.classify(
      features,
      carrier
    );

    // Heuristic classification as fallback
    const heuristicResult = this.heuristicClassify(features);

    // Ensemble decision
    const decision = this.ensembleDecision(mlResult, heuristicResult, carrier);

    return decision;
  }

  extractFeatures(audioData) {
    return {
      mfcc: this.computeMFCC(audioData),
      zeroCrossingRate: this.computeZeroCrossingRate(audioData),
      spectralCentroid: this.computeSpectralCentroid(audioData),
      energyEnvelope: this.computeEnergyEnvelope(audioData),
      silencePattern: this.detectSilencePatterns(audioData),
      durationMs: audioData.length / 16, // 16kHz sample rate
      maxAmplitude: Math.max(...audioData.map(Math.abs)),
      avgAmplitude: audioData.reduce((sum, v) => sum + Math.abs(v), 0) / audioData.length
    };
  }

  heuristicClassify(features) {
    let humanScore = 0;
    let machineScore = 0;

    // Silence gap analysis
    // Voicemail greetings typically have: greeting → silence → beep
    const gaps = features.silencePattern;
    if (gaps.length >= 2) {
      const longGap = gaps.some(g => g.duration > 500 && g.duration < 2000);
      if (longGap) machineScore += 0.3;
    }

    // Duration of initial speech
    // Human greetings are typically shorter ("Hello?")
    // Machine greetings are longer ("Hello, you've reached...")
    const initialSpeechDuration = features.silencePattern[0]?.speechDuration || 0;
    if (initialSpeechDuration > 2000) machineScore += 0.2;
    else if (initialSpeechDuration < 500) humanScore += 0.2;

    // Tone detection (voicemail beep)
    if (this.detectBeepTone(features.spectralCentroid)) {
      machineScore += 0.4;
    }

    // Energy pattern
    // Human speech has more variable energy
    const energyVariance = this.computeVariance(features.energyEnvelope);
    if (energyVariance > 0.3) humanScore += 0.2;
    else machineScore += 0.2;

    const totalScore = humanScore + machineScore;
    return {
      isHuman: totalScore > 0 ? humanScore / totalScore : 0.5,
      confidence: Math.max(humanScore, machineScore),
      features: { humanScore, machineScore }
    };
  }

  ensembleDecision(mlResult, heuristicResult, carrier) {
    const carrierProfile = this.carrierProfiles[carrier] || this.carrierProfiles.default;
    
    // Weight combination: ML 70%, Heuristic 30%
    const humanProbability = 
      mlResult.humanProbability * 0.7 + 
      heuristicResult.isHuman * 0.3;

    const confidence = 
      mlResult.confidence * 0.7 + 
      heuristicResult.confidence * 0.3;

    let classification;
    if (humanProbability >= this.decisionThresholds.human) {
      classification = 'human';
    } else if (humanProbability <= (1 - this.decisionThresholds.machine)) {
      classification = 'machine';
    } else {
      classification = 'uncertain';
    }

    return {
      classification,
      humanProbability,
      confidence,
      mlResult,
      heuristicResult,
      carrierApplied: carrier,
      processingTimeMs: this.audioBuffer.durationMs
    };
  }

  computeMFCC(audioData) {
    // MFCC computation (simplified)
    // Real implementation would use FFT, mel filterbank, DCT
    const frameSize = 1024;
    const numCoefficients = 13;
    const mfccs = [];

    for (let i = 0; i < audioData.length - frameSize; i += frameSize / 2) {
      const frame = audioData.slice(i, i + frameSize);
      const windowed = this.applyHammingWindow(frame);
      const spectrum = this.fft(windowed);
      const melSpectrum = this.applyMelFilterbank(spectrum);
      const mfcc = this.dct(melSpectrum).slice(0, numCoefficients);
      mfccs.push(mfcc);
    }

    return mfccs;
  }
}
```

## Integration Points

- **Dialing Engine (Ch 01):** AMD classification determines call routing (agent vs. voicemail)
- **Voicemail Drop (sec-03):** Machine classification triggers voicemail drop flow
- **Call Progress Analysis (sec-07):** AMD works alongside CPA for comprehensive call state detection
- **Carrier Telephony (Part 07):** Carrier information feeds carrier-specific calibration
- **Campaign Configuration (Ch 01):** AMD sensitivity configured per campaign
- **Analytics (Ch 09):** AMD performance metrics (accuracy by carrier)

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- AMD accuracy target: >95% correct classification, <2% false humans (classifying human as machine)
- Processing must complete within 2-3 seconds of answer to avoid awkward silence with human callers
- Carrier-specific calibration is essential — a model trained on Verizon may perform poorly on T-Mobile
- False positives (hanging up on humans) are much more damaging than false negatives (missing voicemail)
- International carriers have different voicemail patterns — greetings, beep tones, and timing vary
- AMD performance should be monitored by carrier and region, with automatic profile switching
- Noise reduction pre-processing significantly improves accuracy for calls in noisy environments
- Consider multi-language AMD — voicemail greetings in different languages have different acoustic properties
- AMD confidence below threshold should route to a human agent or AI agent with disclaimer
- Log AMD decisions with audio samples for model improvement and quality assurance
