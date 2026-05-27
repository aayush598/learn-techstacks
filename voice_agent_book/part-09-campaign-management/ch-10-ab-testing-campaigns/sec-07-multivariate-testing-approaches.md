# Section 07: Multivariate Testing Approaches

## Overview

Multivariate testing (MVT) evaluates multiple variables simultaneously to measure both individual variable effects and interaction effects between variables. Unlike A/B testing which tests one change at a time, MVT can answer questions like: "Does a conversational opening work better with a discount offer, while a professional opening works better with a value proposition?" MVT is particularly valuable for script optimization where multiple elements (opening, offer, tone, closing) may interact in complex ways.

MVT uses factorial design — testing all combinations of variables (full factorial) or a carefully selected subset (fractional factorial). Full factorial MVT tests every possible combination of variable levels. For k variables each with 2 levels, this requires 2^k combinations. With 5 variables, that's 32 combinations, requiring substantial traffic. Fractional factorial designs reduce this by testing only a subset of combinations that allow estimation of main effects and selected interactions, assuming higher-order interactions are negligible.

## Architecture

```
                  Multivariate Testing Architecture

   +----------------------------------------------------+
   |           Factorial Design Engine                   |
   |                                                    |
   |  Variables & Levels:                                |
   |  - Opening: [Professional, Conversational, Direct]  |
   |  - Offer: [Discount, Free trial, Value prop]        |
   |  - Tone: [Formal, Casual, Urgent]                   |
   |  - Closing: [Soft, Hard, Implied]                   |
   |                                                    |
   |  Design Selection:                                  |
   |  - Full factorial: 3^4 = 81 combinations            |
   |  - Fractional: L9 Taguchi (9 combinations)          |
   |  - Custom: User-selected combinations               |
   +----------------------------------------------------+
        |
        v
   +----------------------------------------------------+
   |           Contact-to-Combination Allocation          |
   |                                                    |
   |  - Stratified randomization                         |
   |  - Ensure sufficient sample per combination         |
   |  - Track allocation balance across variables        |
   +----------------------------------------------------+
        |
        v
   +----------------------------------------------------+
   |           Analysis Engine (ANOVA)                   |
   |                                                    |
   |  Results:                                           |
   |  - Main effect: Opening_Conversational has +5% conv |
   |  - Main effect: Offer_Discount has +3% conv         |
   |  - Interaction: Opening_Conv × Offer_Discount = +2%  |
   |  - Optimal combination: Conv opening + Discount      |
   +----------------------------------------------------+
```

## Design Decisions

- **Fractional factorial with resolution V as default over full factorial:** Resolution V designs allow estimation of all main effects and two-way interactions without confounding, while requiring far fewer combinations than full factorial. For most campaign optimization use cases, three-way and higher interactions are negligible. The system provides full factorial only when traffic is abundant (100K+ contacts per variant) and interaction effects are of primary interest. Trade-off: fractional factorial cannot detect higher-order interactions if they are unexpectedly important.

- **Taguchi orthogonal arrays for robust design:** Taguchi methods provide pre-defined orthogonal arrays (L4, L8, L9, L12, L16, L18) that minimize the number of experimental runs while maintaining orthogonality. These are particularly useful when the number of factors is moderate (3-8) and the primary goal is finding robust optimal settings rather than estimating all effects precisely. Trade-off: Taguchi designs sacrifice some statistical efficiency for practical simplicity and are less familiar to statistically trained analysts.

- **Sequential MVT with factor screening and refinement:** For many-factor tests (6+ variables), the system uses a two-stage approach: Stage 1 screens all factors using a low-resolution design (resolution III) to identify the 2-4 most impactful factors; Stage 2 tests the selected factors using a higher-resolution design to precisely estimate main effects and interactions. This reduces total traffic requirements by 50-70% compared to testing all factors at high resolution from the start. Trade-off: screening may miss factors that are only impactful in combination with other factors (interaction effects that are confounded with main effects in resolution III).

## Implementation Approach

```
interface MVTVariable {
  name: string;
  levels: string[];
}

interface MVTDesign {
  type: 'full_factorial' | 'fractional_factorial' | 'taguchi' | 'custom';
  variables: MVTVariable[];
  combinations: { id: string; levels: Record<string, string>; }[];
  resolution?: 'III' | 'IV' | 'V';
}

interface MVTResults {
  mainEffects: { variable: string; level: string; effect: number; pValue: number }[];
  interactions: { variables: string[]; levels: string[]; effect: number; pValue: number }[];
  optimalCombination: { levels: Record<string, string>; predictedEffect: number };
  explainedVariance: number;  // R-squared of the model
}

class MultivariateTestEngine {
  generateDesign(variables: MVTVariable[], type: string, maxCombinations: number): MVTDesign {
    const totalCombinations = variables.reduce((p, v) => p * v.levels.length, 1);

    if (type === 'full_factorial' || totalCombinations <= maxCombinations) {
      return this.generateFullFactorial(variables);
    }
    if (type === 'taguchi') {
      return this.generateTaguchiDesign(variables);
    }
    return this.generateFractionalFactorial(variables, maxCombinations);
  }

  private generateFractionalFactorial(variables: MVTVariable[], maxCombinations: number): MVTDesign {
    // Select smallest resolution V design that fits within maxCombinations
    const numFactors = variables.length;
    const factorLevels = variables.map(v => v.levels.length);
    // Use a design generator to create the fractional factorial
    return this.designGenerator.createResolutionVDesign(variables, maxCombinations);
  }

  async analyzeMVT(testId: string): Promise<MVTResults> {
    const outcomes = await this.getOutcomes(testId);
    const combinations = await this.getCombinations(testId);

    // Fit ANOVA model
    const anova = this.fitANOVA(outcomes, combinations);

    return {
      mainEffects: this.extractMainEffects(anova),
      interactions: this.extractInteractions(anova, 2),  // Two-way interactions
      optimalCombination: this.findOptimal(anova, combinations),
      explainedVariance: anova.rSquared
    };
  }

  private fitANOVA(outcomes: any[], combinations: any[]) {
    // ANOVA decomposition:
    // SS_total = SS_variables + SS_interactions + SS_error
    // F-test for each variable and interaction
    return this.statisticalCalculator.performANOVA(outcomes, combinations);
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **js-stats** (MIT) | Statistics | ANOVA calculations |
| **simple-statistics** (ISC) | Statistics | Statistical utilities |
| **PostgreSQL** (PostgreSQL) | Data store | Design configuration |
| **Python statsmodels** (BSD) | Statistics | Offline design generation |
| **R with FrF2** (GPL) | Statistics | Fractional factorial design |

## Production Considerations

**Scaling:** MVT with many combinations (32+) requires careful traffic management. Monitor sample size per combination and alert when any combination falls below minimum viable sample size. Use uneven allocation (allocate more traffic to combinations that are more uncertain, following a multi-armed bandit approach across combinations). For very large designs, consider using a Bayesian hierarchical model that borrows strength across combinations.

**Security:** MVT designs and results reveal strategic optimization priorities. Protect design configurations at campaign-manager level. Results showing interaction effects (e.g., "offer X only works with script Y") may be commercially sensitive and should be restricted.

**Monitoring:** Track design efficiency (number of combinations vs. total traffic), per-combination sample size distribution, ANOVA model fit (R-squared), and identification of significant interactions. Alert when per-combination sample size is highly imbalanced (coefficient of variation > 0.5) or when no significant main effects are found (may indicate the test variables are not impactful).
