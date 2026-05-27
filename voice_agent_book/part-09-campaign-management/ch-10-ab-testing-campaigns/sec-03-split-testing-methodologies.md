# Section 03: Split Testing Methodologies

## Overview

Split testing methodologies determine how traffic (contacts) is allocated across variants in an experiment. The simplest approach is a 50/50 split where every contact has an equal chance of being assigned to control or variant. More sophisticated approaches include weighted splits (e.g., 80/20 for risky variants), multivariate splits (testing multiple variables simultaneously), sequential testing (adaptive allocation based on accumulating results), and multi-armed bandit algorithms (dynamically allocating more traffic to better-performing variants). Each methodology has different statistical properties, practical trade-offs, and use cases.

The choice of split methodology depends on the test's goals and constraints. A 50/50 split provides the highest statistical power for a given sample size, making it ideal for conclusive winner determination. Multi-armed bandits minimize regret (lost conversions during the test) by allocating more traffic to promising variants, making them ideal for optimization-focused tests where exploration cost matters. Sequential testing enables early stopping when results are conclusive, reducing the time to implement winning changes.

## Architecture

```
                  Split Testing Methodologies

   +------------------+     +------------------+
   | Fixed Allocation |     | Adaptive Allocation
   | • 50/50 split    |     | • Multi-armed     |
   | • Weighted split |     |   bandit          |
   | • Multivariate   |     | • Thompson        |
   |   (factorial)    |     |   sampling        |
   +------------------+     +------------------+
           |                        |
           v                        v
   +----------------------------------------------------+
   |              Allocation Engine                      |
   |                                                    |
   |  Fixed Allocation:                                  |
   |  - Pre-compute allocation table                     |
   |  - Assign contact ID → variant via hash modulo      |
   |  - Deterministic (same contact always → same variant)|
   |                                                    |
   |  Adaptive Allocation:                               |
   |  - Update allocation probabilities after each batch |
   |  - Thompson sampling: sample from Beta posterior    |
   |  - Epsilon-greedy: explore with probability ε       |
   |  - Upper Confidence Bound (UCB): optimistic initial |
   +----------------------------------------------------+
           |                        |
           v                        v
   +------------------+     +------------------+
   | Contact          |     | Variant          |
   | Assignment       |     | Performance      |
   | (Redis/DB)       |     | Tracking         |
   +------------------+     +------------------+
```

## Design Decisions

- **Deterministic assignment for fixed allocation methods:** Contact-to-variant assignment is deterministic based on a hash of contact_id + test_id modulo the number of variants. This ensures the same contact always receives the same variant if they reappear in the campaign (e.g., retry attempts), preventing cross-contamination. It also enables reproducible audit of allocations. Trade-off: deterministic assignment reduces flexibility for dynamic rebalancing during the test.

- **Thompson sampling for multi-armed bandit over epsilon-greedy or UCB:** Thompson sampling maintains a Beta posterior distribution for each variant's conversion rate, samples from these distributions to select the next variant, and naturally balances exploration vs. exploitation. It handles uncertainty better than epsilon-greedy (which wastes constant exploration budget) and converges faster than UCB in practice. Trade-off: Thompson sampling requires more computational resources per allocation decision and is harder to explain to non-technical stakeholders.

- **Stratified allocation for small sample tests:** When total sample size is limited (e.g., low-volume B2B campaigns), stratified allocation ensures that key covariates (industry, company size, region) are balanced across variants. The allocation engine divides contacts into strata based on these covariates and randomizes within each stratum. Trade-off: stratification requires defining strata before the test and reduces the effective degrees of freedom in analysis.

## Implementation Approach

```
type AllocationMethod = '50_50' | 'weighted' | 'multivariate' | 'multi_armed_bandit';

interface AllocationConfig {
  method: AllocationMethod;
  variants: { id: string; weight: number }[];
  seed?: string;
  stratification?: {
    enabled: boolean;
    strataFields: string[];
  };
  banditConfig?: {
    algorithm: 'thompson_sampling' | 'ucb' | 'epsilon_greedy';
    epsilon?: number;         // For epsilon-greedy
    explorationRate?: number; // Initial exploration for UCB
  };
}

class AllocationEngine {
  async assignVariant(contactId: string, testId: string): Promise<string> {
    const test = await this.getTest(testId);

    if (test.config.method === 'multi_armed_bandit') {
      return this.assignBandit(contactId, test);
    }
    return this.assignFixed(contactId, testId, test.config);
  }

  private assignFixed(contactId: string, testId: string, config: AllocationConfig): string {
    const hash = this.deterministicHash(`${contactId}:${testId}`, config.seed);
    const totalWeight = config.variants.reduce((sum, v) => sum + v.weight, 0);
    let cumulativeWeight = 0;

    for (const variant of config.variants) {
      cumulativeWeight += variant.weight;
      if (hash % totalWeight < cumulativeWeight) {
        return variant.id;
      }
    }
    return config.variants[config.variants.length - 1].id;
  }

  private async assignBandit(contactId: string, test: any): Promise<string> {
    // Thompson sampling: sample from each variant's Beta posterior
    const samples = await Promise.all(
      test.config.variants.map(async (variant) => {
        const stats = await this.getVariantStats(test.id, variant.id);
        const alpha = stats.successes + 1;  // Beta prior
        const beta = stats.trials - stats.successes + 1;
        return { variantId: variant.id, sample: this.sampleBeta(alpha, beta) };
      })
    );
    // Select variant with highest sample
    return samples.reduce((best, current) =>
      current.sample > best.sample ? current : best
    ).variantId;
  }

  private sampleBeta(alpha: number, beta: number): number {
    // Uses Marsaglia-Tsang method for gamma sampling
    const x = this.sampleGamma(alpha);
    const y = this.sampleGamma(beta);
    return x / (x + y);
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **js-stats** (MIT) | Statistics | Beta distribution sampling |
| **Redis** (BSD) | Data store | Bandit state storage |
| **ClickHouse** (Apache 2.0) | Analytics | Variant performance tracking |
| **jStat** (MIT) | Statistics | Statistical distributions |

## Production Considerations

**Scaling:** Multi-armed bandit state must be updated atomically after each allocation. Use Redis Lua scripts to atomically read state, sample, and update counters. For high-traffic tests, batch updates (update bandit state every N allocations or every T seconds) to reduce Redis load. Pre-compute deterministic assignments for fixed allocation methods to reduce per-call latency.

**Security:** Prevent testers from knowing their variant assignment to reduce bias. Bandit algorithm parameters (exploration rate, prior) should be configurable only at test creation. Audit all allocation decisions for reproducibility. Protect against allocation manipulation where a bad actor could artificially inflate one variant's performance.

**Monitoring:** Track allocation distribution (observed vs. expected split), exploration rate (for bandits), regret (conversions lost vs. always picking optimal variant), and allocation latency (p99 < 10ms). Alert on allocation imbalance exceeding 5% from expected for fixed methods, as this may indicate a randomization bug.
