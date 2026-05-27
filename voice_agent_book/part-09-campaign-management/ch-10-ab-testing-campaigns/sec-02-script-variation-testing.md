# Section 02: Script Variation Testing

## Overview

Script variation testing applies A/B testing methodology to call scripts — testing different opening lines, value propositions, offers, objection handling approaches, tones (professional vs. conversational), and calls-to-action to determine which generates the best outcomes. Unlike traditional A/B testing where the entire user experience changes, script testing can target individual elements (the first 5 seconds, the offer presentation, the closing) or entire script flows. Element-level testing provides precise insight into what works but requires more complex instrumentation; full-script testing is simpler but provides less granular learning.

Script variation testing in outbound campaigns has unique characteristics compared to digital A/B testing. The agent's delivery affects script performance — a great script delivered poorly underperforms a mediocre script delivered well. Script compliance (do agents actually follow the assigned script?) must be measured and accounted for. Context effects (the script that works for one contact segment may not work for another) require segmented analysis. The system must track which variant was assigned, monitor script adherence, and analyze results with appropriate statistical rigor.

## Architecture

```
                  Script Variation Testing Flow

   +------------------+     +------------------+
   | Script Templates |     | Variation Config |
   | • Opening        |     | • Element A/B    |
   | • Value Prop     |     | • Full script A/B|
   | • Objection      |     | • Multi-variant  |
   | • Closing        |     | • Segmented test |
   +------------------+     +------------------+
           |                        |
           v                        v
   +----------------------------------------------------+
   |              Script Assignment Engine               |
   |                                                    |
   |  Contact enters campaign → Randomize to variant    |
   |  → Inject variant script into agent/voice pipeline |
   |  → Track script delivery and adherence             |
   |  → Capture outcome and associate with variant      |
   +----------------------------------------------------+
           |                        |
           v                        v
   +------------------+     +------------------+
   | Script Adherence |     | Outcome Tracking |
   | • Was script     |     | • Connect rate   |
   |   followed?      |     | • Conversation   |
   | • Deviation      |     |   duration       |
   |   detection      |     | • Conversion     |
   | • Agent feedback |     | • Sentiment      |
   +------------------+     +------------------+
           |                        |
           v                        v
   +----------------------------------------------------+
   |              Results Analysis Engine                |
   |                                                    |
   |  - Element-level performance comparison            |
   |  - Segmented analysis (by contact type, time)      |
   |  - Statistical significance testing                |
   |  - Interaction effect detection                    |
   +----------------------------------------------------+
```

## Design Decisions

- **Element-level testing with isolation guarantees:** When testing a specific script element (e.g., opening line), all other elements remain identical across variants. This ensures observed differences are attributable to the tested element. The system generates variant scripts by applying element changes to the base template. Trade-off: element-level testing requires more sophisticated script template infrastructure but provides cleaner causal inference.

- **Agent-blind variant assignment with post-hoc agent effect correction:** Agents are not told which variant they are delivering to prevent delivery bias. Post-hoc analysis corrects for agent effects by including agent as a random effect in the statistical model. If certain agents are disproportionately assigned to a variant (due to scheduling or campaign allocation), agent-effect correction prevents this from biasing results. Trade-off: agent-blind assignment limits the agent's ability to adapt delivery to the variant content.

- **Adherence-weighted analysis:** Outcomes are weighted by script adherence — calls where the agent deviated significantly from the assigned script contribute less weight to the analysis. This prevents non-compliant calls from diluting the signal. Weight thresholds are configurable (e.g., exclude calls with < 70% adherence from primary analysis, include in secondary intent-to-treat analysis). Trade-off: adherence measurement requires audio analysis or agent self-reporting, adding instrumentation complexity.

## Implementation Approach

```
interface ScriptVariation {
  id: string;
  testId: string;
  variantId: string;
  type: 'element' | 'full_script';
  elementChanges?: Record<string, string>;  // element_name -> new_content
  fullScriptContent?: string;
}

interface ScriptCallOutcome {
  callId: string;
  variationId: string;
  adherenceScore: number;     // 0.0 - 1.0 how well script was followed
  connected: boolean;
  duration: number;
  converted: boolean;
  sentiment: number;          // -1.0 to 1.0
  revenue: number;
  agentFeedback?: string;
}

class ScriptTestAnalyzer {
  async analyzeScriptTest(testId: string) {
    const outcomes = await this.getTestOutcomes(testId);
    const controlOutcomes = outcomes.filter(o => o.variantId === 'control');
    const variantOutcomes = outcomes.filter(o => o.variantId !== 'control');

    const adherenceWeighted = (outcomes) => {
      const totalWeight = outcomes.reduce((sum, o) => sum + o.adherenceScore, 0);
      const conversions = outcomes.reduce((sum, o) => sum + (o.converted ? o.adherenceScore : 0), 0);
      return totalWeight > 0 ? conversions / totalWeight : 0;
    };

    return {
      testId,
      controlRate: adherenceWeighted(controlOutcomes),
      variantRates: this.groupByVariant(variantOutcomes).map(([vid, outcomes]) => ({
        variantId: vid,
        rate: adherenceWeighted(outcomes),
        sampleSize: outcomes.length,
        significance: this.calculateSignificance(controlOutcomes, outcomes)
      })),
      segmentAnalysis: await this.analyzeBySegment(outcomes)
    };
  }

  private async analyzeBySegment(outcomes: ScriptCallOutcome[]) {
    const segments = ['contact_source', 'time_of_day', 'day_of_week', 'contact_industry'];
    return Promise.all(segments.map(async segment => {
      return this.computeSegmentEffects(outcomes, segment);
    }));
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Handlebars** (MIT) | Templates | Script template rendering |
| **simple-statistics** (ISC) | Statistics | Statistical analysis |
| **PostgreSQL** (PostgreSQL) | Data store | Test configuration |
| **ClickHouse** (Apache 2.0) | Analytics | Outcome analysis |

## Production Considerations

**Scaling:** Script variation changes must be available at dial time with sub-millisecond latency — template rendering happens inline during call setup. Pre-render all variants to avoid per-call rendering overhead. Cache rendered scripts in Redis with variant_id as key. For element-level tests, store only the element diffs and apply them at render time.

**Security:** Script content may contain proprietary business logic, pricing, and offers. Restrict script template access to authorized script writers. Version all script changes and maintain audit log. Prevent test configuration changes while test is running.

**Monitoring:** Track adherence rates per agent (low adherence may indicate training needs), variant assignment balance, script rendering latency, and test progress toward statistical significance. Alert when adherence drops below 60% for any agent-variant combination, as this undermines test validity.
