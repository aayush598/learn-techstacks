# Section 07: Intent Correlation Analysis

## Overview

Intent correlation analysis discovers relationships between different intents — which intents tend to co-occur in the same call, which intents precede or follow each other, and how intent patterns correlate with business outcomes (conversion, churn, repeat calls). Understanding intent correlations helps contact centers optimize IVR routing, agent training, and process workflows. For example, if "Billing Question" and "Account Cancellation" frequently co-occur, the billing team should be trained on retention techniques.

The analysis uses multiple statistical methods: co-occurrence analysis (how often two intents appear together), sequence analysis (intent A → intent B transition probabilities), and outcome correlation (intent patterns associated with positive vs negative outcomes). Results are visualized as a correlation matrix (heatmap of pairwise co-occurrence), a directed graph (intent flow diagram), and a sequence sunburst (hierarchical intent paths).

## Architecture

```
           Intent Correlation Pipeline

   ClickHouse (call_intents with
   multi-intent calls)
        |
   Correlation Engine
        |
   ┌────┴────────────┐
   |                 |
   Co-occurrence    Sequence         Outcome
   Analysis         Analysis         Correlation
   (pairwise)       (markov chain)   (chi-square)
   |                 |                 |
   Correlation Matrix / Flow Graph / Outcome Table
        |
   Dashboard Widgets
```

## Design Decisions

- **Co-occurrence scoring using Pointwise Mutual Information (PMI) over simple count:** Simple co-occurrence counts favor high-frequency intents (Billing Question appears with everything). PMI measures how much more often two intents co-occur than would be expected by chance, normalizing for base frequency. PMI > 0 means intents co-occur more than expected, PMI < 0 means they co-occur less. Trade-off: PMI can over-emphasize rare co-occurrences — the system filters to pairs with minimum 10 co-occurrences before computing PMI.

- **Markov chain for sequence analysis over simple transition probabilities:** A first-order Markov chain models the probability of intent B following intent A, based on the order segments were classified in the call. This captures intent flows — a typical call might start with "Account Inquiry" → transition to "Billing Question" → end with "Payment." The chain is visualized as a directed graph with edge weights representing transition probabilities. Trade-off: Markov chains only capture first-order dependencies (intent N only depends on intent N-1), missing longer-range patterns.

- **Chi-square test for outcome correlation over logistic regression:** Simplified outcome correlation uses chi-square tests to determine whether the presence of a specific intent is significantly associated with a binary outcome (e.g., call resulted in successful resolution vs repeat call within 7 days). This is computationally cheaper than logistic regression and produces intuitive results ("Billing Dispute calls are 2.3x more likely to result in a repeat call"). Trade-off: chi-square tests only detect association, not causation; they also require expected cell counts > 5.

## Implementation Approach

```typescript
interface CoOccurrenceResult {
  intentA: string;
  intentB: string;
  coOccurrenceCount: number;
  expectedCount: number;
  pmi: number;                      // Pointwise Mutual Information
  lift: number;                     // observed / expected
  correlation: number;              // -1 to 1
  direction: 'positive' | 'negative' | 'none';
  significant: boolean;
}

interface IntentTransition {
  fromIntent: string;
  toIntent: string;
  transitionCount: number;
  transitionProbability: number;
}

interface OutcomeCorrelation {
  intentId: string;
  intentName: string;
  outcome: string;
  callsWithIntent: number;
  callsWithIntentAndOutcome: number;
  callsWithoutIntent: number;
  callsWithoutIntentAndOutcome: number;
  oddsRatio: number;
  chiSquare: number;
  pValue: number;
  significant: boolean;
  direction: 'increases' | 'decreases' | 'none';
}

class IntentCorrelationEngine {
  private clickhouse: ClickHouseClient;

  async computeCoOccurrence(
    tenantId: string,
    start: number,
    end: number
  ): Promise<CoOccurrenceResult[]> {
    // Get all calls with multiple intents
    const callIntents = await this.clickhouse.query(`
      SELECT callSid, groupArray(intentId) as intents
      FROM call_intents
      WHERE tenantId = '${tenantId}'
        AND timestamp >= ${start}
        AND timestamp <= ${end}
      GROUP BY callSid
      HAVING length(intents) > 1
    `);

    // Count single-intent calls for base frequency
    const totalResult = await this.clickhouse.query(`
      SELECT count(DISTINCT callSid) as total
      FROM call_intents
      WHERE tenantId = '${tenantId}'
        AND timestamp >= ${start}
        AND timestamp <= ${end}
    `);
    const totalCalls = totalResult[0]?.total ?? 1;

    // Count individual intent frequencies
    const intentCounts = await this.clickhouse.query(`
      SELECT intentId, count(DISTINCT callSid) as count
      FROM call_intents
      WHERE tenantId = '${tenantId}'
        AND timestamp >= ${start}
        AND timestamp <= ${end}
      GROUP BY intentId
    `);
    const freqMap = new Map(intentCounts.map((r: any) => [r.intentId, r.count]));
    const intentIds = Array.from(freqMap.keys());

    // Count co-occurrences
    const coOccurrenceMap = new Map<string, number>();
    for (const row of callIntents) {
      const intents: string[] = row.intents;
      for (let i = 0; i < intents.length; i++) {
        for (let j = i + 1; j < intents.length; j++) {
          const pair = [intents[i], intents[j]].sort().join(':');
          coOccurrenceMap.set(pair, (coOccurrenceMap.get(pair) ?? 0) + 1);
        }
      }
    }

    // Compute PMI for each pair
    const results: CoOccurrenceResult[] = [];
    for (const [pair, observed] of coOccurrenceMap) {
      if (observed < 10) continue; // Minimum threshold

      const [a, b] = pair.split(':');
      const freqA = freqMap.get(a) ?? 1;
      const freqB = freqMap.get(b) ?? 1;

      // Expected co-occurrence if independent
      const expected = (freqA * freqB) / totalCalls;
      const pmi = Math.log2(observed / expected);
      const lift = observed / expected;

      // Correlation coefficient (phi coefficient for binary variables)
      const correlation = this.phiCoefficient(
        observed,
        freqA - observed,
        freqB - observed,
        totalCalls - freqA - freqB + observed
      );

      results.push({
        intentA: a,
        intentB: b,
        coOccurrenceCount: observed,
        expectedCount: expected,
        pmi,
        lift,
        correlation,
        direction: pmi > 0 ? 'positive' : pmi < 0 ? 'negative' : 'none',
        significant: Math.abs(pmi) > 1, // PMI > 1 or < -1 is meaningful
      });
    }

    return results.sort((a, b) => b.pmi - a.pmi);
  }

  private phiCoefficient(
    n11: number, n10: number, n01: number, n00: number
  ): number {
    const numerator = n11 * n00 - n10 * n01;
    const denominator = Math.sqrt(
      (n11 + n10) * (n01 + n00) * (n11 + n01) * (n10 + n00)
    );
    return denominator === 0 ? 0 : numerator / denominator;
  }

  async computeSequenceTransitions(
    tenantId: string,
    start: number,
    end: number
  ): Promise<IntentTransition[]> {
    // Get sequentially ordered intents per call
    const callSequences = await this.clickhouse.query(`
      SELECT callSid, groupArray(intentId) as intents
      FROM (
        SELECT callSid, intentId, segmentIndex
        FROM call_intents
        WHERE tenantId = '${tenantId}'
          AND timestamp >= ${start}
          AND timestamp <= ${end}
          AND segmentIndex IS NOT NULL
        ORDER BY callSid, segmentIndex
      )
      GROUP BY callSid
    `);

    const transitionMap = new Map<string, number>();

    for (const row of callSequences) {
      const intents: string[] = row.intents;
      for (let i = 0; i < intents.length - 1; i++) {
        const from = intents[i];
        const to = intents[i + 1];
        if (from !== to) { // Skip self-transitions
          const key = `${from}:${to}`;
          transitionMap.set(key, (transitionMap.get(key) ?? 0) + 1);
        }
      }
    }

    // Compute transition probabilities
    const fromTotalMap = new Map<string, number>();
    for (const [key, count] of transitionMap) {
      const [from] = key.split(':');
      fromTotalMap.set(from, (fromTotalMap.get(from) ?? 0) + count);
    }

    return Array.from(transitionMap.entries()).map(([key, count]) => {
      const [fromIntent, toIntent] = key.split(':');
      const fromTotal = fromTotalMap.get(fromIntent) ?? 1;
      return {
        fromIntent,
        toIntent,
        transitionCount: count,
        transitionProbability: count / fromTotal,
      };
    }).sort((a, b) => b.transitionProbability - a.transitionProbability);
  }

  async computeOutcomeCorrelation(
    tenantId: string,
    start: number,
    end: number,
    outcome: string = 'repeat_call_7d'
  ): Promise<OutcomeCorrelation[]> {
    const results: OutcomeCorrelation[] = [];
    const intents = await this.clickhouse.query(`
      SELECT DISTINCT intentId FROM call_intents WHERE tenantId = '${tenantId}'
    `);

    for (const { intentId } of intents) {
      const stats = await this.clickhouse.query(`
        SELECT
          countIf(hasIntent = 1 AND ${outcome} = 1) as a_and_b,
          countIf(hasIntent = 1 AND ${outcome} = 0) as a_not_b,
          countIf(hasIntent = 0 AND ${outcome} = 1) as not_a_b,
          countIf(hasIntent = 0 AND ${outcome} = 0) as not_a_not_b
        FROM (
          SELECT
            ci.callSid,
            max(ci.intentId = '${intentId}') as hasIntent,
            max(cr.${outcome}) as ${outcome}
          FROM call_intents ci
          JOIN call_records cr ON ci.callSid = cr.callSid
          WHERE ci.tenantId = '${tenantId}'
            AND ci.timestamp >= ${start}
            AND ci.timestamp <= ${end}
          GROUP BY ci.callSid
        )
      `);

      const s = stats[0];
      if (!s || s.a_and_b + s.a_not_b < 10) continue; // Minimum threshold

      // Odds ratio
      const oddsRatio = (s.a_and_b * s.not_a_not_b) / 
        Math.max(1, (s.a_not_b * s.not_a_b));

      // Chi-square
      const total = s.a_and_b + s.a_not_b + s.not_a_b + s.not_a_not_b;
      const expectedAandB = ((s.a_and_b + s.a_not_b) * (s.a_and_b + s.not_a_b)) / total;
      const chiSquare = expectedAandB > 0
        ? ((s.a_and_b - expectedAandB) ** 2) / expectedAandB
        : 0;

      // Approximate p-value from chi-square (df=1)
      const pValue = this.chiSquarePValue(chiSquare, 1);

      results.push({
        intentId,
        intentName: intentId,
        outcome,
        callsWithIntent: s.a_and_b + s.a_not_b,
        callsWithIntentAndOutcome: s.a_and_b,
        callsWithoutIntent: s.not_a_b + s.not_a_not_b,
        callsWithoutIntentAndOutcome: s.not_a_b,
        oddsRatio,
        chiSquare,
        pValue,
        significant: pValue < 0.05,
        direction: oddsRatio > 1.5 ? 'increases' : oddsRatio < 0.67 ? 'decreases' : 'none',
      });
    }

    return results.sort((a, b) => b.chiSquare - a.chiSquare);
  }

  private chiSquarePValue(chiSquare: number, df: number): number {
    // Simplified p-value approximation
    if (chiSquare <= 0 || df < 1) return 1;
    // For df=1, use normal approximation
    const z = Math.sqrt(chiSquare);
    const p = 2 * (1 - this.normalCdf(z));
    return p;
  }

  private normalCdf(x: number): number {
    const a1 = 0.254829592; const a2 = -0.284496736;
    const a3 = 1.421413741; const a4 = -1.453152027;
    const a5 = 1.061405429; const p = 0.3275911;

    const sign = x < 0 ? -1 : 1;
    x = Math.abs(x) / Math.sqrt(2);
    const t = 1 / (1 + p * x);
    const y = 1 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);
    return 0.5 * (1 + sign * y);
  }
}

// Co-occurrence heatmap component
const CorrelationMatrix: React.FC<{
  results: CoOccurrenceResult[];
  intents: string[];
}> = ({ results, intents }) => {
  const matrix = intents.map(a =>
    intents.map(b => {
      if (a === b) return 1;
      const key = [a, b].sort().join(':');
      const found = results.find(r =>
        (r.intentA === a && r.intentB === b) ||
        (r.intentA === b && r.intentB === a)
      );
      return found?.correlation ?? 0;
    })
  );

  return (
    <div className="correlation-matrix">
      <EChartsHeatmap
        xLabels={intents}
        yLabels={intents}
        data={intents.flatMap((a, i) =>
          intents.map((b, j) => [i, j, matrix[i][j]])
        )}
        colorScale={['#E74C3C', '#FFFFFF', '#2ECC71']}
        minValue={-1}
        maxValue={1}
      />
    </div>
  );
};
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| ClickHouse (Apache 2.0) | Server | Co-occurrence and sequence queries |
| Apache ECharts (Apache 2.0) | Client | Correlation heatmap |
| D3.js (ISC) | Client | Directed graph for intent flow |
| Recharts (MIT) | Client | Outcome correlation bar charts |

## Production Considerations

**Scaling:** Co-occurrence computation is O(n²) in the number of intent pairs. For 100 intents, there are 4,950 pairs — each requiring a co-occurrence count from ClickHouse. Pre-compute co-occurrence nightly and store in a `intent_co_occurrence` table with columns (tenantId, intentA, intentB, pmi, lift, correlation). Sequence analysis requires segment-ordered intent data — ensure the `call_intents` table has a `segmentIndex` column with an index on (callSid, segmentIndex).

**Security:** Correlation results are aggregated and do not expose individual calls or callers. Access requires `analytics:view` permission. Outcome correlation data (e.g., "Billing Dispute leads to 2x repeat calls") is business-sensitive — access may be restricted to supervisors and above.

**Monitoring:** Track the number of significant correlations found per month. Alert if the correlation between two intents changes dramatically (> 0.5 change in PMI) — this may indicate a change in caller behavior or routing. Monitor the outcome correlation computation — if p-values are all > 0.05, the data may be insufficient or the outcome metric may need refinement.
