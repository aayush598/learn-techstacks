# Section 07: Scoring Pipeline Integration

## Overview

The scoring pipeline integrates MOS calculation into the call processing flow. Real-time scoring runs lightweight models during calls for immediate quality feedback. Post-call scoring runs full-quality models on recorded audio for accurate measurements. Batch processing handles historical re-scoring when models improve.

## Implementation Approach

```typescript
class ScoringPipeline {
  async processCall(call: CallRecord): Promise<CallQualityScore> {
    // Phase 1: Real-time scoring (during call)
    const realtimeScore = await this.realtimeScore(call);

    // Phase 2: Post-call scoring (after call ends)
    const audio = await this.loadRecording(call.id);
    const postCallScore = await this.postCallScore(audio, call.metadata);

    // Phase 3: Combine scores
    const combined = this.combineScores(realtimeScore, postCallScore);

    // Phase 4: Store and alert
    await this.storeScore(call.id, combined);
    await this.checkAlerts(combined);

    return combined;
  }

  private async realtimeScore(call: CallRecord): Promise<PartialScore> {
    // Lightweight E-Model calculation
    return {
      mos: this.calculateEModel(call.stats),
      confidence: 0.6,
      latencyMs: 5,
    };
  }

  private async postCallScore(audio: AudioBuffer, metadata: CallMetadata): Promise<PartialScore> {
    // Full PESQ analysis
    const reference = await this.getReferenceAudio(metadata);
    return {
      mos: await this.calculatePESQ(audio, reference),
      confidence: 0.95,
      latencyMs: 5000, // Post-call takes longer
    };
  }

  private combineScores(realtime: PartialScore, postCall: PartialScore): CallQualityScore {
    // Weighted combination, favoring higher confidence
    const totalConfidence = realtime.confidence + postCall.confidence;
    const weightedMOS = (realtime.mos * realtime.confidence + postCall.mos * postCall.confidence) / totalConfidence;
    
    return {
      callId: realtime.callId || postCall.callId,
      mos: Math.round(weightedMOS * 100) / 100,
      realtimeMOS: realtime.mos,
      postCallMOS: postCall.mos,
      confidence: totalConfidence / 2,
      calculatedAt: new Date(),
    };
  }
}
```

## Integration Points

- **Call Processing**: Scores calculated at end of each call
- **Database**: Scores stored in call records
- **Analytics**: Scores sent to analytics pipeline
- **Alerts**: Low scores trigger immediate alerts

## Production Considerations

- **Scoring Latency**: Real-time scoring must complete within 100ms
- **Storage**: Scores add minimal data to existing records
- **Model Updates**: Re-scoring historical calls when models improve
