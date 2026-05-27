# Section 03: Agent Utilization Optimization

## Overview

Agent utilization optimization maximizes the productive use of agent time while maintaining quality of service and preventing agent burnout. In outbound call centers, agent time is the most expensive resource — typically 60-80% of total campaign cost. Every second an agent spends idle waiting for a connected call represents direct cost with zero revenue. The goal of utilization optimization is to keep agents as close to 100% occupied with billable call time as possible, while respecting the constraints of predictive dialing: abandonment rate limits, handle time variability, and agent break schedules.

The optimization operates at two levels: macro-level (scheduling agent shifts to match call volume patterns) and micro-level (real-time call distribution to minimize idle time between calls). Macro optimization uses historical call patterns to predict staffing needs by hour and day of week. Micro optimization uses the dialing ratio to ensure agents receive a new connected call within seconds of completing the previous one. The key metric is utilization rate — percentage of logged-in time spent in active call handling. Target utilization for outbound campaigns is typically 65-80%, balancing efficiency against abandonment rate compliance.

## Architecture

```
              Agent Utilization Optimization System

  +------------------+     +------------------+
  | Agent Status     |     | Call Volume      |
  | (available,      |     | Prediction       |
  |  busy, break,    |     | (hourly forecast |
  |  training, etc.) |     |  by campaign)    |
  +--------+---------+     +--------+---------+
           |                        |
           v                        v
  +---------------------------------------------+
  |        Utilization Optimizer                 |
  |                                              |
  |  1. Track agent states in real-time          |
  |  2. Calculate utilization per agent/campaign |
  |  3. Predict handle time for next call        |
  |  4. Optimize dialing ratio for utilization   |
  |  5. Suggest schedule adjustments             |
  +---------------------------------------------+
           |         |                |
           v         v                v
  +-----------+ +---------+ +----------------+
  | Dialing   | | Agent    | | Schedule      |
  | Ratio     | | Routing  | | Optimizer     |
  | (sec-02)  | | (Part 08)| |               |
  +-----------+ +---------+ +----------------+
```

## Design Decisions

- **Utilization target with abandonment trade-off:** The utilization target directly competes with abandonment rate. Higher utilization requires higher dialing ratios, which increase abandonment risk. The optimizer finds the Pareto-optimal point for each campaign. Trade-off: hard to optimize both simultaneously; campaigns must choose their priority.

- **Handle time prediction for precision pacing:** Using historical handle time distributions (not just averages), the system predicts when each agent will be free and pre-positions the next call to arrive just in time. Trade-off: prediction errors cause either idle agents or abandoned calls; requires sophisticated modeling.

- **Skill-based utilization optimization:** Agents with multiple skills are routed to the campaign where their utilization would be highest at that moment. A multi-skilled agent might handle inbound calls during low outbound periods and vice versa. Trade-off: agent assignment complexity vs. overall utilization improvement.

- **Idle time classification:** Not all idle time is wasted — agents need after-call work (ACW), breaks, and training. The system classifies idle time categories and only optimizes against "avoidable idle" (time waiting for calls). Trade-off: classification complexity vs. targeted optimization.

## Implementation Approach

```
class AgentUtilizationOptimizer {
  constructor(storage, metrics) {
    this.storage = storage;
    this.metrics = metrics;
    this.agentStates = new Map(); // agentId -> current state
    this.utilizationTargets = {
      default: 0.75,
      minimum: 0.50,
      maximum: 0.85
    };
  }

  async calculateUtilization(campaignId, windowMinutes = 60) {
    const agents = await this.getCampaignAgents(campaignId);
    const windowStart = new Date(Date.now() - windowMinutes * 60000);
    const now = new Date();

    let totalAvailableMs = 0;
    let totalBusyMs = 0;
    let totalAcwMs = 0;
    let totalIdleMs = 0;

    for (const agent of agents) {
      const states = await this.getAgentStatesInWindow(
        agent.id, windowStart, now
      );

      for (const state of states) {
        const durationMs = Math.min(
          state.endedAt?.getTime() || now.getTime(),
          now.getTime()
        ) - Math.max(state.startedAt.getTime(), windowStart.getTime());

        switch (state.status) {
          case 'on_call':
            totalBusyMs += durationMs;
            break;
          case 'after_call_work':
            totalAcwMs += durationMs;
            break;
          case 'available':
          case 'idle':
            totalIdleMs += durationMs;
            break;
        }
        totalAvailableMs += durationMs;
      }
    }

    const utilizationRate = totalAvailableMs > 0 
      ? totalBusyMs / (totalBusyMs + totalAcwMs + totalIdleMs)
      : 0;

    return {
      utilizationRate,
      totalBusyMs,
      totalAcwMs,
      totalIdleMs,
      totalAvailableMs,
      agentCount: agents.length,
      periodMinutes: windowMinutes
    };
  }

  async optimizeDialingRatioForUtilization(campaignId) {
    const campaign = await this.campaignService.get(campaignId);
    const utilization = await this.calculateUtilization(campaignId, 15); // Last 15 min

    // Target utilization range
    const target = this.utilizationTargets[campaign.type] || this.utilizationTargets.default;
    const currentRatio = await this.pacingService.getCurrentRatio(campaignId);

    let suggestedRatio;
    if (utilization.utilizationRate < target - 0.05) {
      // Underutilized — increase ratio
      suggestedRatio = currentRatio * (target / Math.max(utilization.utilizationRate, 0.1));
    } else if (utilization.utilizationRate > target + 0.05) {
      // Over-utilized — reduce ratio
      suggestedRatio = currentRatio * (target / utilization.utilizationRate);
    } else {
      // In range — keep ratio
      suggestedRatio = currentRatio;
    }

    // Clamp to campaign limits
    suggestedRatio = Math.max(
      campaign.pacingConfig.minRatio || 1,
      Math.min(suggestedRatio, campaign.pacingConfig.maxRatio || 10)
    );

    return {
      currentUtilization: utilization.utilizationRate,
      targetUtilization: target,
      currentRatio,
      suggestedRatio,
      adjustment: suggestedRatio > currentRatio ? 'increase' : 'decrease',
      agentCount: utilization.agentCount,
      idleToReduce: target > utilization.utilizationRate
        ? utilization.idleMs * (1 - target / (target + 0.1))
        : 0
    };
  }

  async optimizeAgentAssignment(callContext) {
    // Find the best agent for this call based on utilization optimization
    const campaignId = callContext.campaignId;
    const availableAgents = await this.agentPool.getAvailableAgents(campaignId);

    if (availableAgents.length === 0) return null;

    // Score each agent
    const scored = await Promise.all(
      availableAgents.map(async agent => ({
        agent,
        score: await this.scoreAgentForCall(agent, callContext)
      }))
    );

    // Sort by score descending, pick best
    scored.sort((a, b) => b.score - a.score);
    return scored[0].agent;
  }

  async scoreAgentForCall(agent, callContext) {
    let score = 0;

    // 1. Skill match (highest weight)
    const skillMatch = this.calculateSkillMatch(
      agent.skills,
      callContext.requiredSkills
    );
    score += skillMatch * 40;

    // 2. Current utilization (lower utilization = higher score)
    const utilization = await this.getAgentUtilization(agent.id, 10);
    score += (1 - utilization) * 25;

    // 3. Proximity to break (avoid sending to agents about to go on break)
    if (agent.nextBreakIn && agent.nextBreakIn < 300000) { // <5 min to break
      score -= 20;
    }

    // 4. Handle time efficiency (faster agents handle more calls)
    const efficiency = agent.handleTimeEfficiency || 1;
    score += (efficiency - 1) * 15;

    // 5. Recent activity (avoid overloading recently freed agents)
    const lastCallEnded = agent.lastCallEndedAt;
    if (lastCallEnded && (Date.now() - lastCallEnded) < 10000) { // <10s ago
      score -= 10; // Give them a brief breather
    }

    return Math.max(0, score);
  }

  calculateSkillMatch(agentSkills, requiredSkills) {
    if (!requiredSkills || requiredSkills.length === 0) return 1;

    const matched = requiredSkills.filter(s => 
      agentSkills.includes(s)
    ).length;

    return matched / requiredSkills.length;
  }

  async getAgentUtilization(agentId, windowMinutes) {
    const states = await this.getAgentStatesInWindow(
      agentId,
      new Date(Date.now() - windowMinutes * 60000),
      new Date()
    );

    let totalMs = 0;
    let busyMs = 0;

    for (const state of states) {
      const duration = state.durationMs || 0;
      totalMs += duration;
      if (state.status === 'on_call') {
        busyMs += duration;
      }
    }

    return totalMs > 0 ? busyMs / totalMs : 0;
  }

  async getAgentStatesInWindow(agentId, start, end) {
    return this.storage.query(
      `SELECT * FROM agent_states
       WHERE agent_id = $1
         AND started_at < $2
         AND (ended_at IS NULL OR ended_at > $3)
       ORDER BY started_at ASC`,
      [agentId, end, start]
    );
  }

  async getCampaignAgents(campaignId) {
    const campaign = await this.campaignService.get(campaignId);
    if (campaign.agentAssignmentMode === 'pool') {
      return this.agentPool.getAgents(campaign.agentPoolId);
    }
    return this.agentPool.getAgentsBySkills(campaign.requiredSkills);
  }

  async recordAgentState(agentId, status, metadata = {}) {
    const previousState = this.agentStates.get(agentId);

    if (previousState) {
      previousState.endedAt = new Date();
    }

    const newState = {
      agentId,
      status,
      startedAt: new Date(),
      endedAt: null,
      metadata: {
        ...metadata,
        campaignId: metadata.campaignId,
        callId: metadata.callId
      }
    };

    this.agentStates.set(agentId, newState);

    await this.storage.insert('agent_states', newState);

    this.metrics.increment('agent.state_change', {
      agent: agentId,
      from: previousState?.status || 'initial',
      to: status
    });

    // Update utilization metrics
    if (status === 'on_call') {
      this.metrics.increment('agent.calls_received', { agent: agentId });
    }
  }

  async generateUtilizationReport(campaignId, dateRange) {
    const campaign = await this.campaignService.get(campaignId);
    const agents = await this.getCampaignAgents(campaignId);

    const report = {
      campaign: campaign.name,
      period: dateRange,
      agents: []
    };

    let totalUtilization = 0;

    for (const agent of agents) {
      const states = await this.getAgentStatesInWindow(
        agent.id,
        dateRange.start,
        dateRange.end
      );

      let onCallMs = 0;
      let acwMs = 0;
      let idleMs = 0;
      let otherMs = 0;
      let totalMs = 0;

      for (const state of states) {
        const duration = state.durationMs || 0;
        totalMs += duration;

        switch (state.status) {
          case 'on_call': onCallMs += duration; break;
          case 'after_call_work': acwMs += duration; break;
          case 'available':
          case 'idle': idleMs += duration; break;
          default: otherMs += duration;
        }
      }

      const utilization = totalMs > 0 ? onCallMs / totalMs : 0;
      totalUtilization += utilization;

      report.agents.push({
        agentId: agent.id,
        agentName: agent.name,
        onCallMinutes: Math.round(onCallMs / 60000),
        acwMinutes: Math.round(acwMs / 60000),
        idleMinutes: Math.round(idleMs / 60000),
        otherMinutes: Math.round(otherMs / 60000),
        totalMinutes: Math.round(totalMs / 60000),
        utilizationRate: utilization,
        callsHandled: states.filter(s => s.status === 'on_call').length
      });
    }

    report.averageUtilization = report.agents.length > 0 
      ? totalUtilization / report.agents.length 
      : 0;

    return report;
  }
}
```

## Integration Points

- **Dialing Ratio (sec-02):** Utilization feedback adjusts the dialing ratio in real-time
- **Agent Router (Part 08):** Agent assignment optimization routes calls to right agent
- **Campaign Config (Ch 01):** Utilization targets configured per campaign
- **Pacing Algorithm (sec-06):** Utilization feed influences pacing decisions
- **Burst Protection (sec-07):** Low utilization may indicate burst opportunity; high utilization triggers protection
- **Analytics (Ch 09):** Utilization KPIs in campaign performance dashboards
- **Workforce Management:** Agent schedule optimization based on utilization forecasts

## Open-Source Tools

- **Redis:** Real-time agent state tracking with pub/sub for state changes
- **PostgreSQL (with time-series extensions):** Agent state history and utilization analytics
- **node-cron / node-schedule:** Utilization report generation scheduling
- **Prometheus + Grafana:** Real-time agent utilization dashboards
- **BullMQ:** Agent state event processing and notification queues
- **socket.io:** Real-time agent state broadcast to supervisor dashboards

## Production Considerations

- Agent utilization must never exceed 90% sustained — burnout and quality degradation occur above this threshold
- After-call work (ACW) time counts as productive, not idle — agents need this time for disposition and notes
- Break schedules should be coordinated with predicted low-volume periods to minimize impact on utilization
- Monitor utilization by agent to identify outliers — low utilization may indicate training needs, high utilization may indicate burnout risk
- Utilization optimization requires accurate handle time prediction — invest in ML-based prediction models
- Agents handling multiple campaigns need per-campaign utilization tracking to prevent over-assignment
- Idle time buffer of 5-10 seconds between calls improves agent experience and readiness
- Utilization reporting should exclude offline activities (training, meetings, 1:1s) from the denominator
- Supervisor overrides should be available to manually adjust utilization targets for specific agents
- Real-time utilization alerts notify supervisors when utilization drops below or exceeds thresholds
- Utilization trends by hour, day, and agent tenure inform staffing and training decisions
- Peak utilization periods may require part-time or surge staffing strategies
- Compliance note: utilization optimization must never encourage agents to rush calls at the expense of quality
- Cross-training agents increases routing flexibility and improves overall pool utilization
- Regular calibration: compare reported utilization against actual call volume to validate metrics accuracy
