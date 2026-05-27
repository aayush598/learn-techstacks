# Section 03: Perceptual Quality Models

## Overview

Perceptual quality models estimate how a human listener would rate call quality. These models simulate human auditory perception to predict MOS scores. PESQ (P.862) is the most widely used standard, followed by POLQA (P.863) for wider-band signals, and VISQOL for full-band audio. Each model has trade-offs between accuracy and computational cost.

## Model Comparison

| Model | Bandwidth | Accuracy | CPU Cost | Use Case |
|-------|-----------|----------|----------|----------|
| PESQ | Narrow/Wide | Medium | Medium | Legacy, on-prem |
| POLQA | Wide/Super-wide | High | High | Production monitoring |
| VISQOL | Full-band | Very High | Very High | Detailed analysis |
| E-Model | Any | Low | Very Low | Real-time estimation |

## Implementation Approach

```typescript
class PerceptualQualityModel {
  async evaluate(audio: AudioBuffer, reference: AudioBuffer, model: string): Promise<QualityResult> {
    switch (model) {
      case 'pesq':
        return this.runPESQ(audio, reference);
      case 'polqa':
        return this.runPOLQA(audio, reference);
      case 'visqol':
        return this.runVISQOL(audio, reference);
      case 'emodel':
        return this.runEModel(audio);
      default:
        throw new Error(`Unknown model: ${model}`);
    }
  }

  private async runPESQ(audio: AudioBuffer, ref: AudioBuffer): Promise<QualityResult> {
    // PESQ requires ITU-T P.862 implementation
    // Typically calls external binary or library
    const result = await this.executePESQBinary(audio, ref);
    return {
      mos: result.mos,
      raw: result.rawScore,
      model: 'pesq',
      confidence: 0.9,
      details: result.details,
    };
  }

  private async runEModel(audio: AudioBuffer): Promise<QualityResult> {
    // E-Model: computational model for transmission planning
    const noiseLevel = this.calculateNoiseFloor(audio);
    const delay = this.estimateDelay(audio);
    const packetLoss = this.estimatePacketLoss(audio);
    
    // R-factor calculation
    let R = 93.2; // Maximum possible
    R -= 0.024 * delay; // Delay impairment
    R -= 30 * packetLoss; // Packet loss impairment
    R -= 10 * Math.pow(noiseLevel, 0.5); // Noise impairment
    
    // Convert R-factor to MOS
    const mos = R <= 0 ? 1 :
               R >= 100 ? 4.5 :
               1 + 0.035 * R + R * (R - 60) * (100 - R) * 7e-6;
    
    return { mos: Math.min(5, Math.max(1, mos)), model: 'emodel', confidence: 0.7 };
  }
}
```

## Integration Points

- **Pipeline Integration**: Model runs at end of each call
- **Batch Processing**: Heavy models run asynchronously after call completion
- **Model Selection**: Different models based on call tier

## Open-Source Tools

- **PESQ Binary** (ITU-T): ITU reference implementation
- **FFmpeg** (GPL-2.0): Audio preprocessing for model input
- **librosa** (ISC): Python audio features

## Production Considerations

- **Licensing**: PESQ/POLQA require ITU-T licensing
- **Compute Cost**: POLQA is ~10x slower than PESQ
- **Accuracy vs Speed**: Trade accuracy for speed in real-time scenarios
