# Section 01: A/B Testing Fundamentals

## Overview

A/B testing fundamentals establish the statistical and methodological foundation for running experiments on outbound campaigns. In the campaign context, A/B testing compares two or more variants of a campaign element (script, dialing time, offer, call flow) to determine which performs better on a defined success metric (conversion rate, connect rate, revenue per call, customer satisfaction). Unlike traditional digital A/B testing where users are randomly assigned to variants, campaign A/B testing must account for confounding factors like time-of-day effects, agent skill differences, list quality variations, and carryover effects between attempts.

Proper A/B testing requires forming a clear hypothesis before the test begins, calculating the required sample size to detect a meaningful effect, determining the test duration to account for day-of-week and time-of-day variations, and pre-registering the success metric and significance threshold. The system must prevent peeking at results (stopping the test early because results look promising), which inflates false positive rates. The fundamental trade-off is between test rigor (longer tests with larger sample sizes produce more reliable results) and business velocity (faster tests enable quicker optimization).

## Architecture

```
                  A/B Testing Lifecycle

   Hypothesize → Design → Allocate → Execute → Analyze → Decide → Implement
       |           |          |          |         |         |         |
       v           v          v          v         v         v         v
   +---------------------------------------------------------------+
   |                    A/B Test Engine                             |
   |                                                               |
   |  1. Register test hypothesis and parameters                   |
   |  2. Calculate required sample size (power analysis)           |
   |  3. Randomize contact allocation to variants                  |
   |  4. Track execution and prevent peeking                       |
   |  5. Compute statistical significance at test completion       |
   |  6. Declare winner or inconclusive based on criteria          |
   |  7. Automate rollout of winning variant                       |
   +---------------------------------------------------------------+
        |            |            |            |
        v            v            v            v
   +--------+  +--------+  +--------+  +--------+
   | Control |  | Variant|  | Variant|  | Variant|
   | (A)     |  | (B)    |  | (C)    |  | (D)    |
   | Traffic |  | Traffic|  | Traffic|  | Traffic|
   +--------+  +--------+  +--------+  +--------+
```

## Design Decisions

- **Pre-registration with forced minimum sample size and duration:** The system enforces that test parameters (hypothesis, primary metric, minimum detectable effect, significance threshold, power) are registered before the test starts and cannot be changed during the test. The test automatically stops at the pre-calculated sample size + duration, not when results look significant. Trade-off: this prevents optional stopping and p-hacking but may prolong tests that could be concluded earlier with Bayesian methods.

- **Sequential testing as optional alternative to fixed-horizon testing:** For high-traffic campaigns where early decisions have significant business value, the system supports sequential testing (peeking-adjusted confidence intervals) that allows early stopping when results are conclusive. Sequential testing uses alpha-spending functions to maintain statistical validity despite continuous monitoring. Trade-off: sequential testing requires more complex statistics and typically requires larger maximum sample sizes than fixed-horizon tests.

- **Contact-level randomization with stratified allocation:** Contacts are randomized at the individual contact level, not at the list level, to ensure comparable groups. Stratified randomization ensures that key covariates (contact source, prior conversion history, phone number type) are balanced across variants. Trade-off: individual-level randomization is more complex to implement than list-level but provides better statistical properties.

## Implementation Approach

```
interface ABTestRegistration {
  id: string;
  campaignId: string;
  name: string;
  hypothesis: string;
  variants: { id: string; name: string; config: Record<string, any> }[];
  primaryMetric: string;        // e.g., 'conversion_rate', 'revenue_per_call'
  secondaryMetrics: string[];
  parameters: {
    minimumDetectableEffect: number;  // Absolute effect size
    significanceLevel: number;        // Alpha (default 0.05)
    power: number;                    // 1 - Beta (default 0.80)
    expectedBaselineRate: number;     // Expected control conversion rate
  };
  allocationStrategy: '50_50' | 'weighted' | 'multi_armed_bandit';
  status: 'draft' | 'running' | 'completed' | 'stopped';
}

class ABTestManager {
  async registerTest(registration: ABTestRegistration) {
    const sampleSize = this.calculateSampleSize(registration);
    const startDate = Date.now();
    const duration = this.calculateDuration(sampleSize, registration.campaignId);

    await this.db.insert('ab_tests', {
      ...registration,
      requiredSampleSize: sampleSize,
      startDate,
      estimatedEndDate: startDate + duration,
      status: 'draft'
    });
    return { sampleSize, duration };
  }

  calculateSampleSize(test: ABTestRegistration): number {
    const { minimumDetectableEffect, significanceLevel, power, expectedBaselineRate } = test.parameters;
    const z_alpha = 1.96;  // For alpha = 0.05
    const z_beta = 0.84;   // For power = 0.80
    const p1 = expectedBaselineRate;
    const p2 = p1 + minimumDetectableEffect;
    const pooledSE = Math.sqrt(p1 * (1 - p1) + p2 * (1 - p2)) / 2;
    return Math.ceil(
      Math.pow((z_alpha * Math.sqrt(2 * pooledSE) + z_beta * Math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))), 2) /
      Math.pow(minimumDetectableEffect, 2)
    );
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **js-stats** (MIT) | Statistics | Statistical test calculations |
| **simple-statistics** (ISC) | Statistics | Statistical utilities |
| **Redis** (BSD) | Data store | Test allocation tracking |
| **PostgreSQL** (PostgreSQL) | Data store | Test registration and results |

## Production Considerations

**Scaling:** A/B test allocation tracking must be atomic and consistent across distributed dialer instances. Use Redis Lua scripts for atomic variant assignment. For high-traffic campaigns, pre-generate allocation assignments in batches to reduce per-call overhead. Store test results in ClickHouse for fast aggregation across millions of calls.

**Security:** Test configurations should be modifiable only by authorized campaign managers. Prevent test parameter changes while tests are running. Ensure that variant assignments are deterministic and reproducible for audit purposes. Log all test-related configuration changes.

**Monitoring:** Track test progress toward required sample size (percentage complete), remaining duration, interim metric differences (for operational awareness, not stopping decisions), allocation balance across variants, and randomization quality (covariate balance checks). Alert on allocation imbalance exceeding 5% for any variant.
