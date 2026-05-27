# Section 01: MOS Calculation Fundamentals

## Overview

Mean Opinion Score (MOS) is the standard metric for voice quality, ranging from 1 (poor) to 5 (excellent). MOS can be measured through subjective listening tests (real users rating quality) or estimated through objective models (PESQ, POLQA, VISQOL). For the voice AI platform, we use objective MOS estimation in real-time and subjective MOS calibration through user feedback.

## Design Decisions

- **Objective MOS Primary**: Real-time PESQ/POLQA for production monitoring
- **Subjective MOS Calibration**: Monthly listening tests to calibrate objective scores
- **Per-Call Scoring**: MOS calculated for each call segment, not just aggregate
- **Codec-Aware Scoring**: Different MOS ranges for different codecs (Opus, G.711, G.729)

## Implementation Approach

```typescript
interface MOSScore {
  overall: number; // 1-5
  subScores: {
    listening: number;  // Listening quality
    conversational: number; // Conversational quality
    loudness: number;   // Loudness evaluation
    noise: number;     // Background noise impact
  };
  confidence: number; // 0-1 confidence in score
}

class MOSCalculator {
  calculate(audio: AudioBuffer, reference: AudioBuffer): MOSScore {
    // PESQ algorithm implementation
    const pesqScore = this.calculatePESQ(audio, reference);
    
    // Convert PESQ (-0.5 to 4.5) to MOS (1-5)
    const mos = 1 + (pesqScore + 0.5) * (4 / 5);
    
    return {
      overall: Math.min(5, Math.max(1, mos)),
      subScores: {
        listening: this.calculateListeningQuality(audio),
        conversational: this.calculateConversationalQuality(audio),
        loudness: this.calculateLoudness(audio),
        noise: this.calculateNoiseLevel(audio),
      },
      confidence: this.estimateConfidence(pesqScore),
    };
  }

  private calculatePESQ(audio: AudioBuffer, reference: AudioBuffer): number {
    // Simplified PESQ calculation
    // Full PESQ requires ITU-T P.862 implementation
    const snr = this.calculateSNR(audio, reference);
    const distortion = this.calculateSpectralDistortion(audio, reference);
    return 4.5 - (distortion * 0.5) - Math.max(0, (20 - snr) * 0.1);
  }
}
```

## Integration Points

- **Call Recording**: MOS calculated during/after each call
- **Monitoring**: MOS metrics in dashboards and alerts
- **Quality Dashboard**: MOS trends by agent, region, time

## Open-Source Tools

- **PESQ** (ITU-T): Perceptual Evaluation of Speech Quality
- **POLQA** (ITU-T): Perceptual Objective Listening Quality Assessment
- **VISQOL** (Microsoft): Virtual Speech Quality Objective Listener
- **librosa** (ISC): Audio analysis for feature extraction

## Production Considerations

- **Computational Cost**: Full PESQ is expensive; use lighter models for real-time
- **Reference Signal**: Need clean reference for comparison
- **Codec Adaptation**: MOS expectations vary by codec
