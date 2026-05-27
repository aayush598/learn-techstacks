# Section 08: User-Reported Quality Correlation

## Overview

User-reported quality correlates objective MOS scores with subjective user feedback. Not all quality issues are detected by automated models. User feedback (post-call ratings, CSAT scores, NPS) provides ground truth for calibrating objective models. Discrepancies between objective and subjective scores indicate areas for model improvement.

## Implementation Approach

```typescript
class QualityCorrelationAnalyzer {
  async analyze(calls: CallWithFeedback[]): Promise<CorrelationReport> {
    const pairs: MOSPair[] = calls
      .filter(c => c.objectiveMOS && c.userRating)
      .map(c => ({ objective: c.objectiveMOS!, subjective: c.userRating! }));

    if (pairs.length < 30) return { insufficient: true };

    const pearson = this.pearsonCorrelation(pairs.map(p => p.objective), pairs.map(p => p.subjective));
    const mae = pairs.reduce((sum, p) => sum + Math.abs(p.objective - p.subjective), 0) / pairs.length;
    const bias = pairs.reduce((sum, p) => sum + (p.objective - p.subjective), 0) / pairs.length;

    // Identify systematic biases
    const underestimates = pairs.filter(p => p.objective < p.subjective - 0.5).length;
    const overestimates = pairs.filter(p => p.objective > p.subjective + 0.5).length;

    return {
      pearsonCorrelation: pearson,
      meanAbsoluteError: mae,
      bias,
      sampleSize: pairs.length,
      calibration: {
        underestimates: underestimates / pairs.length,
        overestimates: overestimates / pairs.length,
      },
      recommendations: this.generateRecommendations(mae, bias, pearson),
    };
  }

  private pearsonCorrelation(x: number[], y: number[]): number {
    const n = x.length;
    const sumX = x.reduce((a, b) => a + b, 0);
    const sumY = y.reduce((a, b) => a + b, 0);
    const sumXY = x.reduce((sum, xi, i) => sum + xi * y[i], 0);
    const sumX2 = x.reduce((sum, xi) => sum + xi * xi, 0);
    const sumY2 = y.reduce((sum, yi) => sum + yi * yi, 0);
    
    const numerator = n * sumXY - sumX * sumY;
    const denom = Math.sqrt((n * sumX2 - sumX * sumX) * (n * sumY2 - sumY * sumY));
    return denom === 0 ? 0 : numerator / denom;
  }
}
```

## Integration Points

- **Post-Call Survey**: Collect user ratings after each call
- **CSAT/NPS Integration**: Quality correlation with satisfaction metrics
- **Model Tuning**: Adjust objective model parameters based on correlation

## Production Considerations

- **Response Bias**: Users who rate are self-selected; may not represent all users
- **Scale Calibration**: User scale may not match MOS 1-5 scale
- **Context Matters**: User expectations vary by use case
