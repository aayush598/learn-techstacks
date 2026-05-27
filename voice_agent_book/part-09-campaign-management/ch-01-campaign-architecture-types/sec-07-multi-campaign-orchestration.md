# Section 07: Multi-Campaign Orchestration

## Overview

Enterprise contact centers rarely run a single campaign — they run dozens simultaneously across multiple brands, departments, and use cases. Multi-campaign orchestration manages the allocation of shared resources (agent time, trunk capacity, carrier channels) across competing campaigns while respecting each campaign's priority, SLA requirements, and compliance constraints. Without proper orchestration, high-volume campaigns can starve lower-priority campaigns, carrier capacity can be exceeded, and agent utilization can become unpredictable.

The orchestration layer sits between individual campaign dialers and the shared telephony infrastructure. It implements priority-based resource allocation, capacity planning, and dynamic rebalancing as campaign conditions change. The system must support weighted fair queuing, minimum resource guarantees per campaign, and burst allocation for time-sensitive campaigns.

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

```
class MultiCampaignOrchestrator {
  constructor(resourcePool) {
    this.campaigns = new Map();
    this.resourcePool = resourcePool;
    this.allocator = new WeightedFairAllocator();
  }

  registerCampaign(campaign) {
    this.campaigns.set(campaign.id, {
      campaign,
      priority: campaign.config.priority,
      weight: campaign.config.resourceWeight,
      minGuarantee: campaign.config.minTrunks,
      currentAllocation: 0
    });
  }

  async allocateResources() {
    const activeCampaigns = [...this.campaigns.values()]
      .filter(c => c.campaign.isActive());

    const totalWeight = activeCampaigns
      .reduce((sum, c) => sum + c.weight, 0);

    const availableTrunks = this.resourcePool.availableTrunks();
    const availableAgents = this.resourcePool.availableAgents();

    for (const entry of activeCampaigns) {
      const trunkShare = Math.floor(
        (entry.weight / totalWeight) * availableTrunks
      );
      const agentShare = Math.floor(
        (entry.weight / totalWeight) * availableAgents
      );

      const allocation = {
        trunks: Math.max(entry.minGuarantee, trunkShare),
        agents: Math.max(1, agentShare)
      };

      entry.campaign.setResourceAllocation(allocation);
      entry.currentAllocation = allocation;
    }
  }

  onCampaignStateChange(campaignId, newState) {
    // Rebalance when any campaign changes state
    this.allocateResources();
    this.notifyCampaigns();
  }
}
```

## Integration Points

- **Campaign Dialers (Ch 01):** Individual campaign dialers receive resource allocations from the orchestrator
- **Agent Pool (Part 06):** Agent availability and skill-based assignment across campaigns
- **Telephony Layer (Part 07):** SIP trunk capacity sharing and carrier channel allocation
- **Pacing Engine (Ch 08):** Per-campaign pacing is constrained by orchestrator allocations
- **Monitoring (Part 11, Ch 03):** Resource utilization monitoring and bottleneck detection
- **Billing (Part 17):** Resource usage attribution per campaign for chargeback/showback

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Resource rebalancing should be dampened — avoid thrashing by requiring a minimum time between reallocations (e.g., 30 seconds)
- Monitor the resource allocation convergence time — from campaign activation to full allocation should be under 1 second
- Overcommitment ratio must be calculated carefully — if all campaigns simultaneously use full allocation, total resources must still suffice
- Implement emergency resource preemption for compliance-critical campaigns (e.g., time-sensitive regulatory calls)
- Agent time allocation across campaigns requires skill-based matching — an agent may only be eligible for certain campaigns
- Carrier channel allocation should account for regional capacity differences — allocate channels per region
- Log all allocation decisions for billing audit and capacity planning analysis
- Test orchestration behavior under extreme conditions — all campaigns firing simultaneously, then one by one completing
