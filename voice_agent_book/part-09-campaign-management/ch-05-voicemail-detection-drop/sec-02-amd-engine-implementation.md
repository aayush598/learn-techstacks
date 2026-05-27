# Section 02: AMD Engine Implementation

## Overview

The AMD engine is the runtime component that processes audio streams in real-time during outbound calls, detects whether the answerer is human or machine, and triggers appropriate actions. Unlike the research-oriented AMD models discussed in the overview, the engine implementation focuses on production concerns: low-latency processing, streaming audio handling, graceful degradation, and integration with the broader calling pipeline.

The engine operates as a middleware between the telephony layer and the call routing system. It receives raw audio chunks as they arrive from the telephony provider, buffers them, processes them through the AMD pipeline, and produces a classification decision. The engine must handle varied audio quality, network jitter, different codecs, and edge cases like calls answered by children, very brief answers, or calls that drop immediately after answer.

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
class AmdEngineRuntime {
  constructor(config) {
    this.inferencePool = new InferenceWorkerPool(config.poolSize);
    this.carrierProfiles = {};
    this.config = config;
    this.activeDetections = new Map(); // callSid → detection context
  }

  async onCallAnswered(callSid, carrier) {
    const context = new DetectionContext(callSid, carrier, this.config);
    this.activeDetections.set(callSid, context);
    
    return {
      detectionId: context.id,
      status: 'monitoring'
    };
  }

  async onAudioChunk(callSid, chunk) {
    const context = this.activeDetections.get(callSid);
    if (!context) throw new Error(`No active detection for ${callSid}`);

    // Add chunk to buffer
    context.buffer.addChunk(chunk);

    // Check if we have enough audio
    if (context.buffer.durationMs < this.config.minAudioMs) {
      return { status: 'buffering', progress: context.buffer.progress };
    }

    // Pre-process
    const processed = this.preProcessAudio(context.buffer.flush());

    // Run ensemble classification
    const decision = await this.runEnsemble(processed, context.carrier);

    context.addDecision(decision);

    // If confident enough or max duration reached, finalize
    if (decision.confidence >= this.config.decisionThreshold || 
        context.buffer.totalDurationMs >= this.config.maxAudioMs) {
      return this.finalizeDetection(context, decision);
    }

    return { status: 'analyzing', decision: decision.classification, confidence: decision.confidence };
  }

  async runEnsemble(audioData, carrier) {
    const carrierProfile = this.getCarrierProfile(carrier);

    // Run ML and heuristic in parallel
    const [mlResult, heuristicResult] = await Promise.all([
      this.runMLInference(audioData, carrierProfile),
      this.runHeuristicAnalysis(audioData, carrierProfile)
    ]);

    // Ensemble combination with carrier-specific weights
    const mlWeight = carrierProfile.mlWeight || 0.7;
    const heuristicWeight = 1 - mlWeight;

    const humanProb = (mlResult.humanProb * mlWeight) + 
                      (heuristicResult.humanProb * heuristicWeight);
    
    const confidence = (mlResult.confidence * mlWeight) + 
                       (heuristicResult.confidence * heuristicWeight);

    return {
      classification: humanProb > 0.5 ? 'human' : 'machine',
      humanProbability: humanProb,
      confidence,
      mlResult,
      heuristicResult,
      processingTimeMs: audioData.length / 16 // approximate
    };
  }

  async runMLInference(audioData, carrierProfile) {
    // Extract features
    const features = this.extractFeatures(audioData);

    // Get or load model for this carrier
    const model = await this.getModel(carrierProfile.modelKey);

    // Run inference
    const result = await this.inferencePool.runInference(model, features);

    return {
      humanProb: result.humanProbability,
      machineProb: result.machineProbability,
      confidence: Math.max(result.humanProbability, result.machineProbability)
    };
  }

  runHeuristicAnalysis(audioData, carrierProfile) {
    const features = this.extractBasicFeatures(audioData);
    
    let humanScore = 0;
    let machineScore = 0;

    // Feature 1: Greeting length
    const firstUtterance = this.extractFirstUtterance(audioData, features.vadTimestamps);
    if (firstUtterance) {
      if (firstUtterance.duration < 800) humanScore += 2;
      else if (firstUtterance.duration > 2000) machineScore += 2;
    }

    // Feature 2: Silence pattern
    const silences = features.silenceGaps;
    const hasPreBeepSilence = silences.some(s => s > 300 && s < 1500);
    if (hasPreBeepSilence) machineScore += 3;

    // Feature 3: Voice activity ratio
    const vadRatio = features.voiceActivityMs / features.totalDurationMs;
    if (vadRatio > 0.6) { // Continuous speech (machine greeting)
      machineScore += 1;
    } else if (vadRatio < 0.3) { // Short responses (human)
      humanScore += 1;
    }

    // Feature 4: Spectral characteristics
    if (features.hasBeepTone) machineScore += 4;

    const total = humanScore + machineScore;
    return {
      humanProb: total > 0 ? humanScore / total : 0.5,
      confidence: total > 0 ? Math.max(humanScore, machineScore) / 7 : 0.3,
      features
    };
  }

  async finalizeDetection(context, finalDecision) {
    this.activeDetections.delete(context.callSid);

    const action = this.determineAction(finalDecision, context.carrier);
    
    // Log for analytics
    await this.logDetection(context.callSid, finalDecision, action);

    return {
      status: 'completed',
      detection: {
        callSid: context.callSid,
        classification: finalDecision.classification,
        confidence: finalDecision.confidence,
        humanProbability: finalDecision.humanProbability,
        processingTimeMs: context.buffer.totalDurationMs,
        action
      }
    };
  }

  determineAction(decision, carrier) {
    if (decision.classification === 'human' && decision.confidence > 0.8) {
      return 'connect_agent';
    } else if (decision.classification === 'machine' && decision.confidence > 0.7) {
      return 'voicemail_drop';
    } else {
      return 'uncertain_transfer';
    }
  }
}
```

## Integration Points

- **Telephony Layer (Part 07):** Receives audio chunks from telephony provider streams
- **Call Router:** AMD decision determines where the call is routed (agent, voicemail, or transfer)
- **Voicemail Drop Engine (sec-03):** Machine classification triggers voicemail drop workflow
- **Campaign Analytics (Ch 09):** AMD performance tracking (accuracy, latency, distribution)
- **Carrier Service:** Carrier identification for profile selection
- **Model Service:** ML model loading and management

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- AMD processing must complete before the caller perceives an awkward pause — target <3 seconds total
- GPU inference pools need careful sizing — one GPU can typically handle 50-100 concurrent AMD streams
- Audio quality varies dramatically — mobile calls, speakerphone, background noise all affect accuracy
- Implement a watchdog timer — if AMD doesn't produce a decision within 10 seconds, route to human
- Log raw audio snippets (1-2 seconds) for model improvement, with appropriate privacy safeguards
- ML model updates should be deployable without restarting the AMD engine — hot-reload models
- Monitor false positive rate (human classified as machine) as the most critical AMD KPI
- Carrier profile updates should be automated — AMD accuracy by carrier is tracked and profiles are adjusted
- Test AMD with international numbers — voicemail patterns vary significantly by country
- The AMD engine should be horizontally scalable — each instance handles a subset of active calls
