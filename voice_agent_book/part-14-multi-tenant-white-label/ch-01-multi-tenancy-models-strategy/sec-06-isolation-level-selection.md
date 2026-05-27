# Section 06: Tenant Isolation Level Selection Guide

## Overview

Selecting the appropriate isolation level for each tenant is a strategic decision that balances compliance requirements, security posture, operational cost, and customer expectations. Rather than offering a single isolation model for all tenants, a mature voice agent platform provides a decision framework that maps customer characteristics to recommended isolation levels. This guide presents a systematic approach to making this decision, considering both technical and business factors.

The decision process starts with compliance requirements—the hardest constraint. Healthcare customers handling PHI under HIPAA, financial services processing card payments under PCI DSS, and European customers subject to GDPR all have specific data isolation expectations. Following compliance, customer size and growth trajectory influence the recommended model: a startup with 100 minutes/month of usage doesn't need a dedicated database, but a Fortune 500 company processing 100,000 call-hours/month does.

The framework also considers operational maturity of the customer. Some enterprise customers require SOC 2 reports at the tenant level, independent backup/restore capabilities, and the ability to schedule maintenance windows. These operational requirements often drive the decision toward dedicated infrastructure regardless of data sensitivity.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Audio    |--->| WebSocket|--->| Jitter   |--->| PLC      |--->| Player   |
| Producer |    | (WSS)    |    | Buffer   |    | (Packet  |    | (smooth  |
| (100ms   |    | (binary) |    | (adaptive|    |  Loss    |    |  output) |
|  chunks) |    |          |    |  60-200) |    |  Conceal)|    +----------+
+----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```typescript
interface IsolationRecommendation {
  tier: 'shared' | 'schema' | 'dedicated';
  rationale: string[];
  estimatedCost: CostEstimate;
  estimatedLatency: string;
  complianceSatisfied: string[];
}

class IsolationAdvisor {
  private complianceMatrix: Map<string, string> = new Map([
    ['hipaa', 'dedicated'],
    ['pci_dss', 'dedicated'],
    ['gdpr', 'schema'],
    ['soc2', 'schema'],
    ['hipaa_baa', 'dedicated'],
  ]);

  async recommend(customer: CustomerProfile): Promise<IsolationRecommendation> {
    const constraints = new Set<string>();
    const recommendations: string[] = [];

    // 1. Check compliance requirements
    for (const compliance of customer.complianceRequirements) {
      constraints.add(this.complianceMatrix.get(compliance) || 'shared');
    }

    // 2. Check volume
    if (customer.expectedCallVolume > 50000) {
      constraints.add('dedicated');
    } else if (customer.expectedCallVolume > 5000) {
      constraints.add('schema');
    }

    // 3. Check contract value
    if (customer.contractValue > 5000) {
      constraints.add('dedicated');
    } else if (customer.contractValue > 500) {
      constraints.add('schema');
    }

    // 4. Determine highest required tier
    const tier = this.highestTier(Array.from(constraints));

    // 5. Generate rationale
    const rationale: string[] = [];
    for (const compliance of customer.complianceRequirements) {
      rationale.push(`Compliance requirement "${compliance}" requires ${this.complianceMatrix.get(compliance)}`);
    }
    if (customer.expectedCallVolume > 50000) {
      rationale.push(`Expected call volume of ${customer.expectedCallVolume} min/mo justifies dedicated infrastructure`);
    }

    return {
      tier,
      rationale,
      estimatedCost: this.calculateCost(tier, customer),
      estimatedLatency: this.estimateLatency(tier),
      complianceSatisfied: this.satisfiedCompliance(tier, customer.complianceRequirements),
    };
  }

  private highestTier(tiers: string[]): 'shared' | 'schema' | 'dedicated' {
    if (tiers.includes('dedicated')) return 'dedicated';
    if (tiers.includes('schema')) return 'schema';
    return 'shared';
  }

  private calculateCost(tier: string, customer: CustomerProfile): CostEstimate {
    const baseCost = { shared: 0, schema: 500, dedicated: 2000 };
    const variableCost = customer.expectedCallVolume * 0.001;
    return { monthly: baseCost[tier] + variableCost };
  }

  private estimateLatency(tier: string): string {
    if (tier === 'shared') return '<10ms avg (shared pool)';
    if (tier === 'schema') return '<5ms avg (shared instance)';
    return '<2ms avg (dedicated instance)';
  }

  private satisfiedCompliance(
    tier: string, 
    requirements: string[]
  ): string[] {
    const satisfied: string[] = [];
    for (const req of requirements) {
      const requiredTier = this.complianceMatrix.get(req);
      if (requiredTier && this.tierRank(tier) >= this.tierRank(requiredTier)) {
        satisfied.push(req);
      }
    }
    return satisfied;
  }

  private tierRank(tier: string): number {
    return { shared: 1, schema: 2, dedicated: 3 }[tier] || 0;
  }
}
```

## Integration Points

- **Sales Pipeline:** Integration with CRM (Salesforce/HubSpot) to recommend isolation level during quoting
- **Onboarding (Ch 03):** Isolation tier determined during signup affects which provisioning workflow runs
- **Plan Management (Part 17):** Isolation tier is a plan attribute that can be upgraded
- **Provisioning Pipeline:** Each tier has different infrastructure provisioning workflows
- **Contract Management:** Enterprise contracts specify isolation tier as a deliverable

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **Re-evaluate Periodically:** A tenant's needs change over time. Implement annual isolation reviews where the system re-evaluates each tenant's tier recommendation based on current usage patterns and contract value.
- **Graceful Upgrades:** Tier migration should be self-service with zero downtime. Customers shouldn't need to contact support to upgrade their isolation level.
- **Tier Visibility:** Show tenants their current isolation tier in the dashboard. Enterprise customers specifically want to know they have dedicated resources.
- **Cost Communication:** Be transparent about cost implications of higher isolation tiers. Some customers may not need dedicated databases but want them for peace of mind.
- **Contractual SLAs:** Link isolation tier to SLA guarantees. Dedicated tiers can offer higher availability SLAs because they're not affected by noisy neighbors.
- **Tier Downgrade:** Rare but should be supported. A customer who overestimated their needs should be able to downgrade to a lower isolation level (with proper data migration).
- **Free Trial Tier:** Always use shared+RLS for free trials. Don't provision dedicated resources until the customer has converted to paid.
