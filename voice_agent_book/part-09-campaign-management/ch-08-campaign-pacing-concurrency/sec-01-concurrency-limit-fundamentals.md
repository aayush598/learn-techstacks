# Section 01: Concurrency Limit Fundamentals

## Overview

Concurrency limit fundamentals define the maximum number of simultaneous calls a campaign can place at any given moment. These limits operate at multiple levels: per-campaign (how many calls can this campaign make at once?), per-agent (how many simultaneous calls can one agent handle?), trunk-level (how many concurrent calls can the carrier handle?), and global (how many total calls across all campaigns?). Concurrency limits prevent resource exhaustion — both on the carrier side (rate limiting, throttling, account suspension) and on the agent side (overwhelmed agents, call abandonment, poor customer experience).

Setting concurrency limits requires understanding the constraints at each layer of the system. Carrier trunks have hard capacity limits — exceeding them causes call failures or carrier penalties. Agent pools have soft capacity limits — agents can handle only one call at a time (or a small number for async channels). The dialer's internal resources (CPU, memory, network) also impose limits. Concurrency limit management is the art of distributing a finite pool of connection capacity across campaigns in a way that maximizes total throughput while respecting all constraints.

## Architecture

```
                    Concurrency Limit Hierarchy

       Global Limit (Total system-wide concurrency)
                 |
     +-----------+-----------+-----------+
     |           |           |           |
  Campaign A  Campaign B  Campaign C  Campaign D
   (limit:    (limit:     (limit:     (limit:
    max=50)    max=100)    max=30)     max=200)
     |           |           |           |
     v           v           v           v
  +-------------------------------------------+
  |          Concurrency Limit Manager         |
  |                                           |
  |  Limits evaluated on each dial request:   |
  |  1. Check global used < global limit       |
  |  2. Check campaign used < campaign limit   |
  |  3. Check agent pool available > 0         |
  |  4. Check trunk capacity used < trunk cap  |
  |  5. If all pass → allow dial               |
  |  6. If any fail → queue or reject         |
  +-------------------------------------------+
              |          |          |
              v          v          v
        +----------+ +---------+ +---------+
        | Carrier  | | Agent   | | Internal|
        | Trunk    | | Pool    | | Resource|
        | Limits   | | (SIP)   | | Limits  |
        +----------+ +---------+ +---------+
```

## Design Decisions

- **Hierarchical limit evaluation with strictest-wins:** Dial requests must pass all applicable limits. A dial that passes the campaign limit but fails the global limit is rejected. Trade-off: sometimes underutilizes a specific limit when another is hit, but prevents any single resource from being overwhelmed.

- **Soft limits with warning vs. hard limits with block:** Soft limits trigger alerts at 80% utilization; hard limits block at 100%. This provides early warning for capacity planning while ensuring limits are never exceeded. Trade-off: the 80% warning threshold requires tuning per environment.

- **Per-campaign limit override with campaign priority:** Higher-priority campaigns can request limit overrides during peak hours. A "critical" campaign may temporarily borrow capacity from lower-priority campaigns. Trade-off: priority-based borrowing can starve lower-priority campaigns.

- **Dynamic limit adjustment based on agent availability:** Concurrency limits automatically reduce when agent availability drops, preventing answered calls from queuing without agent coverage. Trade-off: fluctuating limits make capacity planning harder.

## Implementation Approach

```
interface ConcurrencyLimit {
  type: 'campaign' | 'agent' | 'trunk' | 'global';
  max: number;
  current: number;
  softWarningThreshold: number; // 0.0 to 1.0
}

class ConcurrencyLimitManager {
  constructor(storage, metrics) {
    this.storage = storage;
    this.metrics = metrics;
    this.cache = new Map(); // Distributed cache via Redis
    this.limits = {
      global: { max: 1000, current: 0, type: 'global' },
      trunk: new Map(), // trunk_id -> limit
      campaign: new Map(), // campaign_id -> limit
      agent: new Map() // agent_id -> limit
    };
  }

  async canDial(campaignId, trunkId) {
    // Evaluate all applicable limits
    const globalLimit = await this.getGlobalLimit();
    const campaignLimit = await this.getCampaignLimit(campaignId);
    const trunkLimit = await this.getTrunkLimit(trunkId);
    const agentLimit = await this.getAgentLimit(campaignId);

    const checks = [
      { name: 'global', allowed: globalLimit.current < globalLimit.max, current: globalLimit.current, max: globalLimit.max },
      { name: 'campaign', allowed: campaignLimit.current < campaignLimit.max, current: campaignLimit.current, max: campaignLimit.max },
      { name: 'trunk', allowed: !trunkLimit || trunkLimit.current < trunkLimit.max, current: trunkLimit?.current || 0, max: trunkLimit?.max || Infinity },
      { name: 'agent', allowed: agentLimit.current < agentLimit.max, current: agentLimit.current, max: agentLimit.max }
    ];

    const allAllowed = checks.every(c => c.allowed);

    // Record check for metrics
    this.recordCheck(campaignId, checks, allAllowed);

    return {
      allowed: allAllowed,
      checks,
      blockedBy: checks.filter(c => !c.allowed).map(c => c.name)
    };
  }

  async reserveSlot(campaignId, trunkId, callId) {
    // Atomically increment all counters
    await this.incrementGlobal();
    await this.incrementCampaign(campaignId);
    await this.incrementTrunk(trunkId);
    await this.incrementAgentPool(campaignId);

    this.metrics.gauge('concurrency.global.current', this.limits.global.current);
    this.metrics.gauge('concurrency.campaign.current', this.limits.campaign.get(campaignId)?.current || 0);
  }

  async releaseSlot(campaignId, trunkId, callId) {
    // Atomically decrement all counters
    await this.decrementGlobal();
    await this.decrementCampaign(campaignId);
    await this.decrementTrunk(trunkId);
    await this.decrementAgentPool(campaignId);

    this.metrics.gauge('concurrency.global.current', this.limits.global.current);
  }

  async setCampaignLimit(campaignId, max, priority) {
    await this.storage.set(`campaign:${campaignId}:concurrency`, {
      max,
      priority: priority || 'normal',
      softThreshold: 0.8,
      updatedAt: new Date()
    });
    this.limits.campaign.set(campaignId, { max, current: 0, type: 'campaign' });
  }

  async getCampaignLimit(campaignId) {
    if (!this.limits.campaign.has(campaignId)) {
      const stored = await this.storage.get(`campaign:${campaignId}:concurrency`);
      if (stored) {
        this.limits.campaign.set(campaignId, {
          max: stored.max,
          current: await this.getCurrentCampaignCount(campaignId),
          type: 'campaign'
        });
      } else {
        // Default limit
        this.limits.campaign.set(campaignId, { max: 50, current: 0, type: 'campaign' });
      }
    }
    return this.limits.campaign.get(campaignId);
  }

  async getGlobalLimit() {
    // Check if we need to adjust based on system health
    if (this.shouldReduceGlobal()) {
      return { ...this.limits.global, max: Math.floor(this.limits.global.max * 0.8) };
    }
    return this.limits.global;
  }

  async getAgentLimit(campaignId) {
    const availableAgents = await this.getAvailableAgentCount(campaignId);

    // Each agent can handle 1 call at a time for voice
    const agentCallCapacity = availableAgents;

    // Dialing ratio: for predictive dialing, we may need more calls than agents
    const dialingRatio = await this.getCampaignDialingRatio(campaignId);
    const effectiveAgentLimit = Math.floor(agentCallCapacity * dialingRatio);

    return {
      max: effectiveAgentLimit,
      current: await this.getCurrentConnectedCalls(campaignId),
      type: 'agent'
    };
  }

  async getAvailableAgentCount(campaignId) {
    const campaign = await this.campaignService.get(campaignId);

    if (campaign.agentSelectionMode === 'pool') {
      // From agent pool
      const poolId = campaign.agentPoolId;
      const totalAgents = await this.agentPool.getTotalAgents(poolId);
      const busyAgents = await this.agentPool.getBusyAgents(poolId);
      return totalAgents - busyAgents;
    }

    // Skill-based routing
    const qualifiedAgents = await this.agentPool.getQualifiedAgents(
      campaign.requiredSkills
    );
    const busyQualified = await this.agentPool.getBusyAgents(
      qualifiedAgents.map(a => a.id)
    );
    return qualifiedAgents.length - busyQualified.length;
  }

  shouldReduceGlobal() {
    // Reduce global limit under system stress
    const cpuUsage = os.loadavg()[0] / os.cpus().length;
    const memoryUsage = 1 - (os.freemem() / os.totalmem());

    return cpuUsage > 0.8 || memoryUsage > 0.85;
  }

  recordCheck(campaignId, checks, allowed) {
    this.metrics.increment('concurrency.check', {
      campaign: campaignId,
      allowed: allowed.toString(),
      blockedBy: checks.filter(c => !c.allowed).map(c => c.name).join(',') || 'none'
    });

    for (const check of checks) {
      if (check.current / check.max >= 0.8) {
        this.metrics.increment('concurrency.warning', {
          level: check.name,
          utilization: (check.current / check.max * 100).toFixed(0)
        });
      }
    }
  }

  async getCurrentCampaignCount(campaignId) {
    // Query active calls for this campaign
    return this.redis.scard(`campaign:${campaignId}:active_calls`);
  }

  async getCurrentConnectedCalls(campaignId) {
    // Query connected (answered) calls for this campaign
    return this.redis.scard(`campaign:${campaignId}:connected_calls`);
  }
}
```

## Integration Points

- **Campaign Dialing (Ch 01):** Concurrency check before every dial attempt
- **Agent Management (Part 08):** Agent availability feeds into agent pool concurrency limits
- **Carrier Trunks (Part 07):** Trunk capacity limits from carrier configuration
- **Pacing Algorithms (sec-06):** Concurrency limits interact with pacing ratio calculations
- **Campaign Throttling (sec-04):** Token bucket algorithm enforces dialing rate in addition to concurrency
- **Monitoring (sec-08):** Concurrency utilization metrics for capacity planning
- **Analytics (Ch 09):** Concurrency-related abandonment tracking

## Open-Source Tools

- **Redis (with SCARD/SADD):** Active call tracking for concurrency counting
- **BullMQ:** Queue for pending dial requests when concurrency limits are hit
- **Prometheus:** Concurrency metrics and limit utilization gauges
- **node-os-utils:** System resource monitoring for global limit adjustment
- **node-redis (with Lua scripting):** Atomic increment/decrement for concurrency counters
- **ioredis:** Redis client with cluster support for distributed concurrency management

## Production Considerations

- Concurrency limits must be enforced atomically to prevent race conditions (use Lua scripts or Redis transactions)
- Global limit should be set to ~80% of carrier trunk capacity to leave headroom for bursts
- Agent concurrency for voice is always 1:1 — each call requires a dedicated agent
- Dialing ratio can inflate concurrency beyond agent count for predictive dialing (typically 1.5x-3x)
- Concurrency limit violations (exceeding limits) must trigger immediate alerts
- Soft limits with warning at 80% provide time to scale resources before hitting hard limits
- Campaign priority should affect limit enforcement during contention — higher-priority campaigns get preference
- Concurrency counters must be decremented on all call end paths (hangup, error, timeout)
- Consider per-IP or per-data-center limits for multi-region deployments
- Monitor concurrency limit hit rate — frequent blocking indicates need for capacity increase
- Limit configuration should be hot-reloadable without restarting the dialer
- Stale concurrency counters (from crashed processes) require periodic reconciliation jobs
- For async channels (SMS, email), concurrency limits are per-second, not simultaneous
- Trunk-level limits are carrier-specific and may change without notice — monitor trunk failure rate
