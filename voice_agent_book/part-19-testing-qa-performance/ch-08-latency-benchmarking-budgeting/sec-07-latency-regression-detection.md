# Section 07: Latency Regression Detection

## Overview

Latency regression detection automatically identifies when changes to the codebase or infrastructure cause latency increases. The detection system compares current latency metrics against baselines, using statistical methods to distinguish genuine regressions from normal variance. Regressions are reported with the suspected commit and pipeline stage affected.

## Implementation Approach

```typescript
class LatencyRegressionDetector {
  async detect(testRun: LatencyTestRun): Promise<RegressionResult> {
    const baseline = await this.loadBaseline(testRun.version);
    const regressions: Regression[] = [];

    for (const [stage, current] of Object.entries(testRun.metrics)) {
      const base = baseline.metrics[stage];
      if (!base) continue;

      // Statistical comparison using Mann-Whitney U test
      const significant = this.statisticalTest(current.samples, base.samples);
      if (!significant) continue;

      const changePercent = ((current.p95 - base.p95) / base.p95) * 100;
      if (Math.abs(changePercent) > 5) { // 5% threshold
        regressions.push({
          stage,
          baseline: base.p95,
          current: current.p95,
          changePercent,
          direction: changePercent > 0 ? 'regression' : 'improvement',
          severity: Math.abs(changePercent) > 15 ? 'high' : 'medium',
          pValue: significant.pValue,
        });
      }
    }

    return {
      hasRegression: regressions.some(r => r.direction === 'regression'),
      regressions: regressions.filter(r => r.direction === 'regression'),
      improvements: regressions.filter(r => r.direction === 'improvement'),
    };
  }

  private statisticalTest(current: number[], baseline: number[]): { significant: boolean; pValue: number } {
    // Mann-Whitney U test implementation
    const allValues = [...current, ...baseline];
    const ranks = this.computeRanks(allValues);
    const u1 = current.reduce((sum, v) => sum + ranks.get(v)!, 0);
    const n1 = current.length, n2 = baseline.length;
    const u = u1 - (n1 * (n1 + 1)) / 2;
    const expectedU = (n1 * n2) / 2;
    const stdU = Math.sqrt((n1 * n2 * (n1 + n2 + 1)) / 12);
    const z = (u - expectedU) / stdU;
    const pValue = 2 * (1 - this.normalCDF(Math.abs(z)));
    return { significant: pValue < 0.05, pValue };
  }
}
```

## Integration Points

- **CI Pipeline**: Regression detected during CI performance tests
- **Git Bisect**: Automated git bisect to find regression source
- **Alerting**: Regression notifications to engineering team

## Open-Source Tools

- **Simple Statistics** (MIT): Statistical test library
- **JStat** (MIT): JavaScript statistics
- **Python scipy** (BSD-3): Advanced statistical tests

## Production Considerations

- **Multiple Comparisons**: Adjust for multiple stage comparisons (Bonferroni correction)
- **Sample Size**: Small sample sizes reduce statistical power
- **Context Awareness**: Account for infrastructure changes in regression analysis
