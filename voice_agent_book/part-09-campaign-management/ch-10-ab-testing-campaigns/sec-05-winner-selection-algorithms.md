# Section 05: Winner Selection Algorithms

## Overview

Winner selection algorithms determine when and how to declare a test variant as the winner and implement it as the new default. The decision is rarely as simple as "pick the variant with the highest observed metric." The system must consider statistical significance (is the difference real?), practical significance (is the difference big enough to matter?), business constraints (does the winning variant have negative side effects on secondary metrics?), and uncertainty (what is the probability that another variant is actually better?).

Winner selection involves multiple criteria beyond primary metric performance. A variant might show a 15% improvement in conversion rate but a 25% increase in call duration (reducing agent capacity). Another might show a 10% improvement in conversion but a 5% decrease in customer satisfaction. The system uses multi-criteria decision frameworks that balance the primary metric against secondary metrics, cost implications, and operational constraints. The winner is declared only when the evidence meets pre-registered criteria, and the system supports both automatic winner declaration and manual review workflows.

## Architecture

```
                  Winner Selection Decision Flow

   Test Completion Reached (required sample size + duration met)
        |
        v
   +----------------------------------------------------+
   |          Winner Selection Engine                    |
   |                                                    |
   |  1. Check statistical significance                  |
   |     - Is p-value < alpha?                           |
   |     - Is Bayesian prob(treatment better) > threshold?|
   |                                                    |
   |  2. Check practical significance                     |
   |     - Is effect size > minimum detectable effect?    |
   |     - Is relative improvement > business threshold?  |
   |                                                    |
   |  3. Check secondary metrics                          |
   |     - Are any secondary metrics significantly worse? |
   |     - If yes, check if still acceptable with override|
   |                                                    |
   |  4. Multi-criteria scoring                          |
   |     - Weighted composite score across all metrics   |
   |     - Cost-benefit analysis                         |
   |     - Expected value of implementing winner         |
   |                                                    |
   |  5. Decision                                        |
   |     - Declare winner (A > B with confidence)        |
   |     - Declare tie (no practical difference)         |
   |     - Inconclusive (need more data)                 |
   +----------------------------------------------------+
```

## Design Decisions

- **Practical significance gate over pure statistical significance:** A variant must clear both statistical significance (p < 0.05) and practical significance (effect size > minimum detectable effect specified in test registration). A statistically significant 0.1% improvement with 100,000 sample size is still practically irrelevant. The practical significance threshold is set during test registration and cannot be changed post-hoc. Trade-off: requiring practical significance increases the required sample size but ensures business-meaningful results.

- **Multi-criteria winner selection with configurable weights:** The winner selection engine computes a composite score from primary metric (weight 50%), secondary metrics (25% total), cost impact (15%), and operational risk (10%). Weights are configured at test registration. A variant that wins on primary metric but has unacceptable secondary metric impact can be flagged for manual review rather than automatic rollout. Trade-off: multi-criteria scoring introduces subjectivity in weight selection and may obscure simple "which variant won?" answers.

- **Two-stage winner declaration (provisional → confirmed):** Winners are first declared as "provisional" and optionally run in a holdout period (e.g., 1 week at 80/20 split) before "confirmed" status. The holdout confirms that results replicate in a slightly different time period and allocation ratio. This guards against temporal effects (Monday traffic is different from Friday traffic) that could have biased the test. Trade-off: two-stage declaration delays full rollout by the holdout period, typically 1-2 weeks.

## Implementation Approach

```
interface WinnerSelectionInput {
  testId: string;
  primaryMetric: { name: string; observedEffect: number; pValue: number; practicalThreshold: number };
  secondaryMetrics: { name: string; observedEffect: number; pValue: number; direction: 'higher_better' | 'lower_better' }[];
  costs: { variantId: string; perContactCost: number; totalCost: number }[];
  parameters: {
    statisticalSignificanceThreshold: number;  // alpha
    practicalSignificanceThreshold: number;     // minimum detectable effect
    multiCriteriaWeights: { primary: number; secondary: number; cost: number; risk: number };
  };
}

interface WinnerDeclaration {
  variantId: string;
  status: 'provisional' | 'confirmed' | 'tie' | 'inconclusive';
  confidence: {
    statisticalSignificance: boolean;
    practicalSignificance: boolean;
    secondaryMetricsAcceptable: boolean;
  };
  compositeScore: number;
  expectedLift: number;          // Expected improvement vs. control
  expectedValue: number;         // Expected dollar value of implementing
  recommendation: 'auto_rollout' | 'manual_review' | 'extend_test' | 'no_change';
}

class WinnerSelector {
  selectWinner(input: WinnerSelectionInput): WinnerDeclaration {
    // Check statistical and practical significance
    const statSig = input.primaryMetric.pValue < input.parameters.statisticalSignificanceThreshold;
    const pracSig = Math.abs(input.primaryMetric.observedEffect) >= input.parameters.practicalSignificanceThreshold;

    // Check secondary metrics for regressions
    const secondaryOK = input.secondaryMetrics.every(m => {
      if (m.direction === 'higher_better') return m.pValue > 0.05 || m.observedEffect > 0;
      return m.pValue > 0.05 || m.observedEffect < 0;
    });

    // Compute composite score
    const primaryScore = input.primaryMetric.observedEffect * input.parameters.multiCriteriaWeights.primary;
    const secondaryScore = input.secondaryMetrics
      .reduce((sum, m) => sum + m.observedEffect, 0) / input.secondaryMetrics.length
      * input.parameters.multiCriteriaWeights.secondary;
    const compositeScore = primaryScore + secondaryScore;

    return {
      variantId: input.primaryMetric.observedEffect > 0 ? 'variant' : 'control',
      status: this.determineStatus(statSig, pracSig, secondaryOK),
      confidence: { statisticalSignificance: statSig, practicalSignificance: pracSig, secondaryMetricsAcceptable: secondaryOK },
      compositeScore,
      expectedLift: input.primaryMetric.observedEffect,
      expectedValue: this.calculateExpectedValue(input),
      recommendation: this.getRecommendation(statSig, pracSig, secondaryOK)
    };
  }

  private determineStatus(statSig: boolean, pracSig: boolean, secondaryOK: boolean): string {
    if (statSig && pracSig && secondaryOK) return 'provisional';
    if (statSig && pracSig && !secondaryOK) return 'inconclusive';
    return 'inconclusive';
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **simple-statistics** (ISC) | Statistics | Statistical tests |
| **PostgreSQL** (PostgreSQL) | Data store | Test configuration |
| **ClickHouse** (Apache 2.0) | Analytics | Result analysis |

## Production Considerations

**Scaling:** Winner selection runs at test completion and is not performance-critical for individual tests. For platforms running thousands of concurrent tests, batch the winner selection process into a queue (BullMQ) with configurable concurrency to avoid overwhelming the analytics database.

**Security:** Winner selection configuration (weights, thresholds) must be set at test registration and immutable thereafter to prevent manipulation. Winner declarations should be signed and stored immutably for audit. Automated rollout decisions should require explicit configuration to enable automatic rollout; manual review is the safer default.

**Monitoring:** Track winner declaration statistics (what % of tests declare a winner vs. inconclusive), average effect size of winners, correlation between test duration and effect size (short tests may overestimate effects), and holdout confirmation rate (% of provisional winners confirmed in holdout). Alert when holdout confirmation rate drops below 50%, as this indicates systematic winner overestimation.
