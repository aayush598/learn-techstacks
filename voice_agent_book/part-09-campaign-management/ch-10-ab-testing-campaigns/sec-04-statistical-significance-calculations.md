# Section 04: Statistical Significance Calculations

## Overview

Statistical significance calculations determine whether observed differences between test variants are likely due to actual performance differences rather than random chance. The core question is: if the null hypothesis (no difference between variants) were true, what is the probability of observing data at least as extreme as what we actually observed? If this probability (p-value) is below a pre-determined threshold (typically 0.05), we reject the null hypothesis and declare the difference statistically significant.

The system supports multiple statistical testing approaches based on the type of metric being tested. For binary outcomes (converted/did not convert), the z-test for proportions or chi-squared test is appropriate. For continuous outcomes (revenue per call, call duration), the t-test is used. For multiple variants, ANOVA or pairwise comparisons with multiple testing correction (Bonferroni, Holm-Bonferroni, Benjamini-Hochberg) are needed. The system also supports Bayesian A/B testing which produces a probability distribution of the treatment effect rather than a binary significant/not-significant decision.

## Architecture

```
                  Statistical Significance Calculation

   +------------------+     +------------------+
   | Test Results     |     | Test Parameters  |
   | • Control data   |     | • Significance   |
   | • Variant data   |     |   level (alpha)  |
   | • Sample sizes   |     | • Test type      |
   | • Metric values  |     | • One/two-tailed |
   +------------------+     +------------------+
           |                        |
           v                        v
   +----------------------------------------------------+
   |           Statistical Test Selector                 |
   |                                                    |
   |  Metric Type → Test Method                          |
   |  Binary (conversion) → z-test or chi-squared        |
   |  Continuous (revenue) → t-test or Welch's t-test    |
   |  Count (calls) → Poisson test or negative binomial  |
   |  Ordinal (rating) → Mann-Whitney U test             |
   |  Multiple variants → ANOVA + post-hoc tests         |
   +----------------------------------------------------+
           |                        |
           v                        v
   +----------------------------------------------------+
   |              Calculation Engine                     |
   |                                                    |
   |  Frequentist:                                       |
   |  - Compute test statistic (z, t, chi-sq, F)         |
   |  - Compute p-value from distribution                |
   |  - Compute confidence interval                      |
   |  - Apply multiple testing correction                |
   |                                                    |
   |  Bayesian:                                          |
   |  - Specify prior (Beta for binary, Normal for cont) |
   |  - Compute posterior distribution                   |
   |  - Compute probability of superiority               |
   |  - Compute expected loss                            |
   +----------------------------------------------------+
```

## Design Decisions

- **Dual reporting (Frequentist + Bayesian) with clear labeling:** The system calculates both frequentist p-values with confidence intervals and Bayesian posterior probabilities. Frequentist results are used for regulatory/compliance decisions where binary significance is required. Bayesian results are used for business decisions where understanding the magnitude and uncertainty of the effect is more important than a binary decision. Trade-off: dual reporting can confuse users who don't understand the difference between p-values and posterior probabilities.

- **Automatic test selection based on metric type and data distribution:** The system automatically selects the appropriate statistical test based on the metric type (binary, continuous, count, ordinal) and validates assumptions (normality for t-tests, expected counts for chi-squared). If assumptions are violated, the system falls back to non-parametric alternatives (Mann-Whitney, bootstrap). Trade-off: automatic selection may choose a suboptimal test in edge cases — expert users can override the selection.

- **Sequential testing with alpha-spending for continuous monitoring:** For tests that support early stopping, the system implements alpha-spending functions (Pocock, O'Brien-Fleming) that adjust significance thresholds for each interim analysis. The O'Brien-Fleming boundary is conservative early (requires very strong evidence to stop) and more liberal later, maintaining overall type I error rate. Trade-off: sequential testing requires pre-specifying the number and timing of interim analyses, adding complexity to test design.

## Implementation Approach

```
interface SignificanceResult {
  method: 'z_test' | 't_test' | 'chi_squared' | 'mann_whitney' | 'bayesian';
  pValue: number;
  confidenceInterval: [number, number];
  confidenceLevel: number;          // e.g., 0.95
  isSignificant: boolean;
  effectSize: number;
  bayesianPosterior?: {
    probTreatmentBetter: number;
    expectedLoss: number;
    credibleInterval: [number, number];
  };
  assumptions: {
    normalityMet: boolean;
    equalVarianceMet: boolean;
    expectedCountsMet: boolean;
  };
}

class StatisticalCalculator {
  calculateSignificance(
    control: { successes: number; trials: number; values?: number[] },
    variant: { successes: number; trials: number; values?: number[] },
    metricType: 'binary' | 'continuous',
    alpha: number = 0.05
  ): SignificanceResult {
    if (metricType === 'binary') {
      return this.zTestProportions(control.successes, control.trials, variant.successes, variant.trials, alpha);
    }
    return this.tTest(control.values, variant.values, alpha);
  }

  private zTestProportions(
    successes1: number, trials1: number,
    successes2: number, trials2: number,
    alpha: number
  ): SignificanceResult {
    const p1 = successes1 / trials1;
    const p2 = successes2 / trials2;
    const pPooled = (successes1 + successes2) / (trials1 + trials2);
    const se = Math.sqrt(pPooled * (1 - pPooled) * (1 / trials1 + 1 / trials2));
    const z = (p1 - p2) / se;
    const pValue = 2 * (1 - this.normalCDF(Math.abs(z)));
    const margin = this.zScore(1 - alpha / 2) * se;
    const effectSize = p2 - p1;

    return {
      method: 'z_test',
      pValue,
      confidenceInterval: [effectSize - margin, effectSize + margin],
      confidenceLevel: 1 - alpha,
      isSignificant: pValue < alpha,
      effectSize,
      assumptions: {
        normalityMet: true,  // CLT applies for proportions
        equalVarianceMet: true,
        expectedCountsMet: trials1 * pPooled >= 5 && trials1 * (1 - pPooled) >= 5
      }
    };
  }

  private normalCDF(x: number): number {
    return 0.5 * (1 + this.erf(x / Math.SQRT2));
  }

  private erf(x: number): number {
    // Approximation of error function
    const a1 = 0.254829592;
    const a2 = -0.284496736;
    const a3 = 1.421413741;
    const a4 = -1.453152027;
    const a5 = 1.061405429;
    const p = 0.3275911;
    const sign = x < 0 ? -1 : 1;
    x = Math.abs(x);
    const t = 1 / (1 + p * x);
    return sign * (1 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x));
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **jStat** (MIT) | Statistics | Statistical distributions |
| **simple-statistics** (ISC) | Statistics | Statistical functions |
| **Bayes.js** (MIT) | Statistics | Bayesian computation |
| **PyMC** (Apache 2.0) | Statistics | Bayesian modeling (offline) |

## Production Considerations

**Scaling:** Statistical calculations are performed at test completion or on-demand during analysis, not per-call. Computation time is dominated by Bayesian methods that may require MCMC sampling — use analytical solutions (Beta-Binomial conjugate for binary metrics) to avoid MCMC overhead. Cache results with test_id + metric + date_range as key to avoid recomputation.

**Security:** Statistical results should be accessible only to authorized test owners and analysts. Prevent premature disclosure of interim results that could lead to peeking and early stopping (for fixed-horizon tests). Bayesian posterior distributions are as sensitive as frequentist results and require equal access controls.

**Monitoring:** Track the ratio of significant tests at alpha=0.05. Under the null hypothesis, 5% of tests should be significant. A significantly higher rate suggests p-hacking, multiple testing without correction, or systematic bias. Track also the distribution of p-values (should be uniform under null) and effect size distributions across tests.
