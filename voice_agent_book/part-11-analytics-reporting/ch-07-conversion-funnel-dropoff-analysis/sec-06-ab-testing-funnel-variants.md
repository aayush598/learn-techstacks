# Section 06: A/B Testing Funnel Variants

## Overview

A/B testing funnel variants enables contact centers to run controlled experiments on IVR flows, agent scripts, routing algorithms, and post-call processes to measure their impact on conversion rates. The system supports splitting call traffic between two or more variants (control and treatment) and comparing the full funnel metrics to determine which variant performs better. A/B tests are created and managed through a dedicated experiment configuration interface.

The A/B testing framework handles traffic splitting (percentage-based or cookie/session-based assignment), randomization (consistent assignment per caller), sample size calculations (minimum required calls for statistical power), and automatic result computation with frequentist and Bayesian analysis. Tests run for a configurable minimum duration (to account for weekly seasonality) and a minimum sample size (to ensure statistical validity). Results are computed in real-time as events arrive, with a "results are ready" indicator when the test reaches statistical significance.

## Architecture

```
           A/B Testing Funnel Variants

   Experiment Config → Traffic Splitter → Variant A / Variant B
        |
   Funnel Events (tagged with variant)
        |
   ClickHouse (variant-specific funnel_events)
        |
   A/B Test Analyzer
        |
   ┌────┴────────────┐
   |                 |
   Frequentist       Bayesian
   Analysis          Analysis
   (z-test,          (Beta-Bernoulli
    chi-square)       model)
   |                 |
   Results Dashboard
   (winning variant,
    expected lift,
    confidence,
    sample size)
```

## Design Decisions

- **Server-side traffic splitting over client-side:** Traffic is split at the voice platform level (Twilio Studio, Nexmo, or custom SIP proxy) based on the caller's anonymous ID or phone number hash. This ensures consistent assignment (same caller always gets the same variant) and prevents client-side tampering. The platform tags all events with the variant ID before sending to the analytics pipeline. Trade-off: server-side splitting requires integration with the voice platform's routing configuration; changes to the split ratio require a platform restart.

- **Bayesian analysis (Beta-Bernoulli model) as primary, frequentist as secondary:** Bayesian analysis provides intuitive results ("87% probability that Variant B is better") that non-technical stakeholders can understand. The Beta-Bernoulli conjugate model is computationally simple — updates are O(1) per event. Frequentist results (p-value, z-statistic) are provided alongside for data scientists who prefer them. The test stops when either: Bayesian probability > 95%, frequentist p < 0.05, or the test reaches the maximum planned duration. Trade-off: Bayesian analysis requires a prior (typically Beta(1,1) uniform prior), which may influence results for very small samples.

- **Sequential testing with early stopping over fixed-horizon testing:** Traditional A/B tests require a fixed sample size, but stopping early when results are clear reduces the cost of running the inferior variant. The system uses a sequential testing approach (always-valid p-values or Bayesian posterior monitoring) that allows early stopping when the evidence is conclusive. The spending function controls the Type I error rate across multiple looks. Trade-off: sequential testing is more complex to implement and requires more conservative significance thresholds to control for multiple looks.

## Implementation Approach

```typescript
interface AbTestConfig {
  id: string;
  tenantId: string;
  name: string;
  funnelId: string;
  description: string;
  variants: Array<{
    id: string;
    name: string;
    trafficPercent: number;
    isControl: boolean;
    config: Record<string, any>;    // Variant-specific configuration
  }>;
  targetStage: string;               // Primary success stage
  targetMetric: 'conversion' | 'duration' | 'dropoff';
  minimumSampleSize: number;        // Per variant
  minimumDurationDays: number;
  maximumDurationDays: number;
  status: 'draft' | 'running' | 'completed' | 'cancelled';
  startedAt?: number;
  completedAt?: number;
  winnerVariantId?: string;
  createdAt: number;
}

interface AbTestResult {
  testId: string;
  variantId: string;
  variantName: string;
  isControl: boolean;
  entries: number;
  conversions: number;
  conversionRate: number;
  historicalConversionRate?: number; // Pre-test baseline
  // Frequentist
  zStatistic?: number;
  pValue?: number;
  // Bayesian
  posteriorAlpha: number;
  posteriorBeta: number;
  winProbability: number;            // Probability this variant is the best
  expectedLift: number;              // Expected improvement over control
  credibleInterval: [number, number]; // 95% credible interval for conversion rate
  result: 'winning' | 'losing' | 'inconclusive';
  samplesNeeded: number;             // Estimated remaining samples
}

class AbTestEngine {
  private clickhouse: ClickHouseClient;
  private redis: Redis;

  async startTest(config: AbTestConfig): Promise<void> {
    // Validate configuration
    if (config.variants.reduce((s, v) => s + v.trafficPercent, 0) !== 100) {
      throw new Error('Traffic percentages must sum to 100');
    }
    if (!config.variants.some(v => v.isControl)) {
      throw new Error('At least one variant must be the control');
    }

    config.status = 'running';
    config.startedAt = Date.now();

    // Store test configuration
    await this.clickhouse.insert('ab_tests', config);

    // Notify traffic splitter
    await this.redis.publish('abtest:start', JSON.stringify({
      testId: config.id,
      tenantId: config.tenantId,
      variants: config.variants.map(v => ({
        id: v.id,
        trafficPercent: v.trafficPercent,
      })),
    }));
  }

  async recordEvent(
    testId: string,
    callSid: string,
    variantId: string,
    eventType: string,
    stageId: string
  ): Promise<void> {
    const event = {
      testId,
      callSid,
      variantId,
      eventType,
      stageId,
      timestamp: Date.now(),
    };

    await this.clickhouse.insert('ab_test_events', event);

    // Update Redis counters for real-time results
    const targetStage = await this.getTestTargetStage(testId);
    if (stageId === targetStage) {
      const hourKey = `abtest:${testId}:${variantId}:counters`;
      if (eventType === 'stage_entry') {
        await this.redis.hincrby(hourKey, 'entries', 1);
      }
      if (eventType === 'stage_exit') {
        await this.redis.hincrby(hourKey, 'conversions', 1);
      }
    }
  }

  async getResults(testId: string): Promise<AbTestResult[]> {
    const test = await this.getTestConfig(testId);
    if (!test) throw new Error(`Test ${testId} not found`);

    const results: AbTestResult[] = [];

    for (const variant of test.variants) {
      // Get counts from ClickHouse
      const counts = await this.clickhouse.query(`
        SELECT
          countIf(eventType = 'stage_entry') as entries,
          countIf(eventType = 'stage_exit') as conversions
        FROM ab_test_events
        WHERE testId = '${testId}'
          AND variantId = '${variant.id}'
          AND stageId = '${test.targetStage}'
      `);

      const entries = counts[0]?.entries ?? 0;
      const conversions = counts[0]?.conversions ?? 0;

      // Bayesian analysis (Beta-Bernoulli)
      const priorAlpha = 1;
      const priorBeta = 1;
      const posteriorAlpha = priorAlpha + conversions;
      const posteriorBeta = priorBeta + entries - conversions;

      const conversionRate = entries > 0 ? (conversions / entries) * 100 : 0;
      const winProbability = this.computeWinProbability(
        posteriorAlpha, posteriorBeta,
        results.filter(r => !r.isControl).map(r => [r.posteriorAlpha, r.posteriorBeta])
      );

      // 95% credible interval (using normal approximation for computational efficiency)
      const mean = posteriorAlpha / (posteriorAlpha + posteriorBeta);
      const variance = (posteriorAlpha * posteriorBeta) /
        ((posteriorAlpha + posteriorBeta) ** 2 * (posteriorAlpha + posteriorBeta + 1));
      const stdErr = Math.sqrt(variance);
      const ci: [number, number] = [
        Math.max(0, (mean - 1.96 * stdErr) * 100),
        Math.min(100, (mean + 1.96 * stdErr) * 100),
      ];

      // Expected lift over control
      const controlResult = results.find(r => r.isControl);
      const expectedLift = controlResult
        ? ((conversionRate - controlResult.conversionRate) / controlResult.conversionRate) * 100
        : 0;

      // Sample size estimation (using normal approximation)
      const baselineRate = controlResult?.conversionRate ?? conversionRate;
      const minimumDetectableEffect = 0.05; // 5% relative improvement
      const samplesNeeded = this.estimateSampleSize(
        baselineRate / 100,
        (baselineRate * (1 + minimumDetectableEffect)) / 100,
        0.8, 0.05
      );

      results.push({
        testId,
        variantId: variant.id,
        variantName: variant.name,
        isControl: variant.isControl,
        entries,
        conversions,
        conversionRate,
        posteriorAlpha,
        posteriorBeta,
        winProbability,
        expectedLift,
        credibleInterval: ci,
        result: winProbability > 0.95 ? 'winning'
          : winProbability < 0.05 ? 'losing'
          : 'inconclusive',
        samplesNeeded: Math.max(0, samplesNeeded - entries),
      });
    }

    return results.sort((a, b) => b.winProbability - a.winProbability);
  }

  private computeWinProbability(
    alpha: number, beta: number,
    others: Array<[number, number]>
  ): number {
    // Monte Carlo estimation of P(this variant > all others)
    const samples = 10000;
    let wins = 0;

    for (let i = 0; i < samples; i++) {
      const thisSample = this.sampleBeta(alpha, beta);
      const otherSamples = others.map(([a, b]) => this.sampleBeta(a, b));
      if (thisSample > Math.max(...otherSamples)) {
        wins++;
      }
    }

    return wins / samples;
  }

  private sampleBeta(alpha: number, beta: number): number {
    // Gamma distribution sampling (Marsaglia & Tsang method)
    const gammaSample = (shape: number): number => {
      if (shape < 1) {
        const u = Math.random();
        return gammaSample(shape + 1) * Math.pow(u, 1 / shape);
      }
      const d = shape - 1 / 3;
      const c = 1 / Math.sqrt(9 * d);
      while (true) {
        const x = this.normalSample();
        const v = 1 + c * x;
        if (v <= 0) continue;
        const v3 = v * v * v;
        const u = Math.random();
        if (u < 1 - 0.0331 * x * x * x * x) return d * v3;
        if (Math.log(u) < 0.5 * x * x + d * (1 - v3 + Math.log(v3))) return d * v3;
      }
    };

    const x = gammaSample(alpha);
    const y = gammaSample(beta);
    return x / (x + y);
  }

  private normalSample(): number {
    const u1 = Math.random();
    const u2 = Math.random();
    return Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
  }

  private estimateSampleSize(
    p1: number, p2: number,
    power: number = 0.8,
    alpha: number = 0.05
  ): number {
    const zAlpha = 1.96; // z for alpha = 0.05 (two-tailed)
    const zBeta = 0.84;  // z for power = 0.80
    const p = (p1 + p2) / 2;
    const numerator = Math.pow(zAlpha * Math.sqrt(2 * p * (1 - p)) + zBeta * Math.sqrt(p1 * (1 - p1) + p2 * (1 - p2)), 2);
    const denominator = Math.pow(p2 - p1, 2);
    return Math.ceil(numerator / denominator);
  }

  private async getTestConfig(testId: string): Promise<AbTestConfig | null> {
    const result = await this.clickhouse.query(`
      SELECT * FROM ab_tests WHERE id = '${testId}'
    `);
    return result[0] ?? null;
  }

  private async getTestTargetStage(testId: string): Promise<string> {
    const test = await this.getTestConfig(testId);
    return test?.targetStage ?? '';
  }
}

// A/B test results widget
const AbTestResultCard: React.FC<{
  results: AbTestResult[];
  testConfig: AbTestConfig;
}> = ({ results, testConfig }) => {
  const winner = results.find(r => r.result === 'winning');
  const control = results.find(r => r.isControl);

  return (
    <div className={`ab-test-results ${winner ? 'has-winner' : 'inconclusive'}`}>
      <div className="test-header">
        <h3>{testConfig.name}</h3>
        <StatusBadge status={testConfig.status} />
      </div>
      {winner && (
        <div className="winner-banner">
          <span>{winner.variantName} is winning</span>
          <span>Expected lift: {winner.expectedLift.toFixed(1)}%</span>
          <span>Win probability: {(winner.winProbability * 100).toFixed(1)}%</span>
        </div>
      )}
      <div className="variant-comparison">
        {results.map(r => (
          <VariantResultCard key={r.variantId} result={r} />
        ))}
      </div>
    </div>
  );
};
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| ClickHouse (Apache 2.0) | Server | A/B test event storage |
| Redis (RSAL) | Server | Traffic split config & real-time counters |
| jStat (MIT) | Server | Statistical distributions |
| Apache ECharts (Apache 2.0) | Client | Result visualization |

## Production Considerations

**Scaling:** A/B test event storage uses the same funnel_events table with an added `testId` and `variantId` column — create an index on (testId, variantId, stageId) for fast per-test queries. Real-time counters use Redis hashes with test TTL (max test duration + 7 days). For tests with 50+ variants, limit to pairwise comparison vs the control rather than all-vs-all comparison.

**Security:** A/B test configuration requires `analytics:configure` permission. Test results are visible with `analytics:view` permission. The traffic split percentage must be validated to prevent assigning 100% of traffic to a non-control variant. Test events are tenant-scoped.

**Monitoring:** Track active test count, test result availability time (time to significance), and test cancellation rate. Alert if a test runs for more than the maximum duration without reaching significance (indicates effect size is too small to detect or test is underpowered). Monitor the traffic splitter for consistency — if the actual split deviates from the configured split by more than 5%, alert the operations team.
