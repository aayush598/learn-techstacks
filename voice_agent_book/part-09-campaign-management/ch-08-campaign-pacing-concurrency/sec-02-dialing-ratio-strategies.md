# Section 02: Dialing Ratio Strategies

## Overview

Dialing ratio strategies determine how many calls to place per available agent in an outbound campaign. In a perfect world with 100% answer rates and instantaneous agent connection, the ratio would be 1:1 — one call per agent. In reality, only 15-40% of outbound calls are answered by humans, and those that are answered require agent connection. The dialing ratio compensates for this inefficiency by placing more calls than agents available, ensuring agents always have a connected call waiting when they become free.

The dialing ratio is the most critical parameter in predictive dialer performance. A ratio that's too low leaves agents idle (wasted agent time, increased cost per contact). A ratio that's too high causes call abandonment (connected calls that no agent is available to handle), which triggers regulatory penalties under TCPA's 3% abandonment rate limit. The optimal ratio depends on real-time answer rates, call duration distribution, agent handle time, and the campaign's abandonment rate target. Modern systems adjust the ratio dynamically based on continuous feedback from answer rate and abandonment rate measurements.

## Architecture

```
              Dialing Ratio Calculation Flow

  +------------------+     +------------------+
  | Answer Rate      |     | Abandonment Rate |
  | Monitor          |     | Monitor          |
  | (rolling 5-min   |     | (rolling 15-min  |
  |  window)         |     |  window)         |
  +--------+---------+     +--------+---------+
           |                        |
           v                        v
  +---------------------------------------------+
  |         Dialing Ratio Calculator             |
  |                                              |
  |  Base calculation:                           |
  |    ratio = 1 / expected_connect_rate         |
  |                                              |
  |  With abandonment constraint:                |
  |    max_ratio = f(abandonment_rate_target,    |
  |                  handle_time,                |
  |                  answer_rate_variance)        |
  |                                              |
  |  Final ratio = min(base, max, config_max)    |
  +---------------------------------------------+
           |                        |
           v                        v
  +------------------+     +------------------+
  | Campaign Config  |     | Pacing Engine    |
  | (min/max ratio,  |     | (token bucket    |
  |  target abandon  |     |  with ratio)     |
  |  rate)           |     |                  |
  +------------------+     +--------+---------+
                                     |
                                     v
                            +------------------+
                            | Dial Request     |
                            | (place 1 call    |
                            |  per token)     |
                            +------------------+
```

## Design Decisions

- **Expected connect rate as primary input:** The ratio is calculated from the inverse of the expected connect rate (answer rate × qualification rate). A 30% answer rate with 50% qualification yields a 1/(0.3×0.5) = 6.67:1 ratio. Trade-off: heavily dependent on accurate rate estimation; sharp rate changes cause over- or under-dialing until the estimator catches up.

- **Rolling window with exponential weighting:** Answer rate measurements use an exponentially weighted moving average (EWMA) rather than a simple average. This gives more weight to recent calls while smoothing out noise. Trade-off: double the implementation complexity vs. significantly better responsiveness to rate changes.

- **Abandonment rate as hard constraint:** The ratio automatically reduces when the rolling abandonment rate approaches the target (typically 3% for TCPA). This creates a negative feedback loop that maintains compliance. Trade-off: can reduce agent utilization significantly during low-answer-rate periods.

- **Campaign-type-specific ratio ranges:** Different campaign types (lead generation, collections, surveys) have different answer rates and appropriate ratio ranges. Predictive dialing for warm leads may use 1.5:1, while cold calling may use 5:1 or higher. Trade-off: per-campaign tuning required vs. better performance for each campaign type.

## Implementation Approach

```
class DialingRatioCalculator {
  constructor(storage, metrics) {
    this.storage = storage;
    this.metrics = metrics;
    this.answerRateTracker = new RateTracker({
      windowMs: 300000, // 5 minute rolling window
      ewmaAlpha: 0.3    // Exponential weighting factor
    });
    this.abandonmentRateTracker = new RateTracker({
      windowMs: 900000, // 15 minute rolling window
      ewmaAlpha: 0.2
    });
  }

  async calculateRatio(campaignId) {
    const campaign = await this.campaignService.get(campaignId);
    const config = campaign.pacingConfig;

    // 1. Get real-time answer rate
    const answerRate = this.answerRateTracker.getRate(campaignId);
    const connectRate = answerRate * (campaign.qualificationRate || 1);

    // 2. Calculate base ratio
    let baseRatio = connectRate > 0 ? (1 / connectRate) : config.maxRatio;

    // 3. Apply abandonment constraint
    const abandonRate = this.abandonmentRateTracker.getRate(campaignId);
    const abandonTarget = config.abandonmentRateTarget || 0.03;

    if (abandonRate > 0) {
      const abandonRatio = this.calculateAbandonmentConstrainedRatio(
        abandonRate,
        abandonTarget,
        campaign
      );
      baseRatio = Math.min(baseRatio, abandonRatio);
    }

    // 4. Clamp to configured range
    const finalRatio = Math.max(
      config.minRatio || 1,
      Math.min(baseRatio, config.maxRatio || 10)
    );

    // 5. Log and return
    this.recordRatioCalculation(campaignId, {
      answerRate,
      connectRate,
      abandonRate,
      baseRatio,
      finalRatio,
      config
    });

    return finalRatio;
  }

  calculateAbandonmentConstrainedRatio(currentAbandonRate, targetAbandonRate, campaign) {
    // If current abandon rate is above target, reduce ratio
    if (currentAbandonRate <= targetAbandonRate) {
      return Infinity; // No constraint
    }

    // How much we need to reduce ratio to bring abandon rate down
    // abandon_rate = overflow_calls / total_connected
    // overflow = dialed * connect_rate - agent_capacity
    // ratio = dialed / agents

    const avgHandleTime = await this.getAverageHandleTime(campaign.id);
    const agentCount = await this.getAvailableAgentCount(campaign.id);
    const callsPerAgentPerMinute = 60 / (avgHandleTime / 1000);

    const currentExcess = currentAbandonRate - targetAbandonRate;
    const reductionFactor = 1 - (currentExcess / currentAbandonRate) * 0.5;

    // Reduce current ratio by up to 50% to bring abandon rate down
    return Math.max(
      campaign.pacingConfig.minRatio || 1,
      reductionFactor * (1 / (this.answerRateTracker.getRate(campaign.id) || 0.3))
    );
  }

  async getAverageHandleTime(campaignId) {
    const recent = await this.storage.query(
      `SELECT AVG(handle_time_ms) as avg_handle_time
       FROM call_records
       WHERE campaign_id = $1
         AND handle_time_ms IS NOT NULL
         AND ended_at > NOW() - INTERVAL '1 hour'`,
      [campaignId]
    );
    return recent[0]?.avg_handle_time || 180000; // Default 3 minutes
  }

  async getAvailableAgentCount(campaignId) {
    const campaign = await this.campaignService.get(campaignId);
    const poolId = campaign.agentPoolId;
    const total = await this.agentPool.getTotalAgents(poolId);
    const busy = await this.agentPool.getBusyAgents(poolId);
    return Math.max(1, total - busy);
  }

  recordRatioCalculation(campaignId, data) {
    this.metrics.gauge('pacing.ratio', data.finalRatio, { campaign: campaignId });
    this.metrics.gauge('pacing.answer_rate', data.answerRate, { campaign: campaignId });
    this.metrics.gauge('pacing.abandon_rate', data.abandonRate, { campaign: campaignId });
    this.metrics.gauge('pacing.connect_rate', data.connectRate, { campaign: campaignId });
  }
}

class RateTracker {
  constructor(config) {
    this.windowMs = config.windowMs || 300000;
    this.ewmaAlpha = config.ewmaAlpha || 0.3;
    this.rates = new Map(); // campaignId -> { numerator, denominator, ewma }
  }

  recordAttempt(campaignId, wasAnswered) {
    const now = Date.now();

    if (!this.rates.has(campaignId)) {
      this.rates.set(campaignId, {
        attempts: [],
        ewma: null
      });
    }

    const tracker = this.rates.get(campaignId);
    tracker.attempts.push({
      timestamp: now,
      answered: wasAnswered
    });

    // Update EWMA
    if (tracker.ewma === null) {
      tracker.ewma = wasAnswered ? 1 : 0;
    } else {
      tracker.ewma = this.ewmaAlpha * (wasAnswered ? 1 : 0) + (1 - this.ewmaAlpha) * tracker.ewma;
    }

    // Prune old entries
    this.prune(campaignId, now);
  }

  getRate(campaignId) {
    const tracker = this.rates.get(campaignId);
    if (!tracker) return null;

    this.prune(campaignId, Date.now());

    const attempts = tracker.attempts;
    if (attempts.length === 0) return null;

    const answered = attempts.filter(a => a.answered).length;
    return answered / attempts.length;
  }

  getEWMA(campaignId) {
    const tracker = this.rates.get(campaignId);
    return tracker?.ewma ?? null;
  }

  prune(campaignId, now) {
    const tracker = this.rates.get(campaignId);
    if (!tracker) return;

    const cutoff = now - this.windowMs;
    tracker.attempts = tracker.attempts.filter(a => a.timestamp >= cutoff);
  }
}

// PredictiveRatioStrategy — more sophisticated approach
class PredictiveRatioStrategy {
  constructor(answerRatePredictor, abandonRateMonitor) {
    this.predictor = answerRatePredictor;
    this.abandonMonitor = abandonRateMonitor;
  }

  async calculate(campaignId, availableAgents) {
    // Use ML prediction for more accurate dialing
    const predictedAnswerRate = await this.predictor.predict(campaignId);
    const predictedHandleTime = await this.predictor.predictHandleTime(campaignId);

    // Erlang-C based dialing ratio
    // λ = call arrival rate, μ = service rate, c = agents
    // We want P(no agent available) < abandon target
    const serviceRate = 1 / (predictedHandleTime / 3600000); // calls per hour per agent
    const expectedCallsPerHour = availableAgents * serviceRate;
    const targetAbandonRate = this.abandonMonitor.getTarget(campaignId);

    // Modified Erlang-C: find λ such that probability of queueing ≤ abandon target
    const trafficIntensity = this.findMaxTrafficIntensity(
      availableAgents,
      predictedHandleTime / 3600000,
      targetAbandonRate
    );

    // Convert traffic intensity to dialing ratio
    const expectedConnectRate = predictedAnswerRate;
    const maxCallsPerHour = trafficIntensity * serviceRate * availableAgents;
    const dialsPerHour = maxCallsPerHour / expectedConnectRate;
    const ratio = dialsPerHour / (availableAgents * serviceRate);

    return {
      ratio: Math.max(1, Math.min(ratio, 10)),
      expectedAnswerRate: predictedAnswerRate,
      expectedHandleTime: predictedHandleTime,
      trafficIntensity,
      maxCallsPerHour: maxCallsPerHour / 3600 // Convert to per-second
    };
  }

  findMaxTrafficIntensity(agents, serviceTimeHours, targetAbandonRate) {
    // Binary search for the maximum traffic intensity
    // such that probability of delay > target abandon rate
    let low = 0.1;
    let high = agents * 0.99;
    let intensity = low;

    for (let i = 0; i < 20; i++) {
      intensity = (low + high) / 2;
      const probDelay = this.erlangC(agents, intensity);

      if (probDelay > targetAbandonRate) {
        high = intensity;
      } else {
        low = intensity;
      }
    }

    return intensity;
  }

  erlangC(agents, trafficIntensity) {
    // Erlang-C formula: P(queuing) = (A^c / c! * c/(c-A)) / (sum(A^k/k!, k=0..c-1) + A^c/c! * c/(c-A))
    let numerator = Math.pow(trafficIntensity, agents) / this.factorial(agents);
    numerator *= agents / (agents - trafficIntensity);

    let denominator = 0;
    for (let k = 0; k < agents; k++) {
      denominator += Math.pow(trafficIntensity, k) / this.factorial(k);
    }
    denominator += numerator;

    return numerator / denominator;
  }

  factorial(n) {
    let result = 1;
    for (let i = 2; i <= n; i++) result *= i;
    return result;
  }
}
```

## Integration Points

- **Concurrency Limits (sec-01):** Ratio determines how many calls to place per available agent
- **Pacing Algorithm (sec-06):** Ratio feeds into token bucket pacing rate
- **Real-Time Adjustment (sec-05):** Ratio dynamically adjusts based on answer/abandon feedback
- **Agent Utilization (sec-03):** Optimal ratio directly impacts agent idle time
- **Campaign Config (Ch 01):** Min/max ratio and abandon rate target per campaign
- **Analytics (Ch 09):** Ratio effectiveness tracking — ratio vs. utilization vs. abandon rate

## Open-Source Tools

- **stats-lite / simple-statistics:** Statistical functions for ratio calculations
- **mathjs:** Advanced math for Erlang-C calculations
- **Redis:** Real-time answer rate and abandon rate tracking
- **Prometheus:** Ratio calculation metrics
- **node-pace / Bottleneck:** Rate limiting inspired by pacing algorithms
- **PostgreSQL (with window functions):** Handle time and answer rate querying

## Production Considerations

- Abandonment rate is regulated at 3% max under TCPA — this is a hard constraint, not a target
- Answer rates vary significantly by time of day, day of week, and season — adjust ratio continuously
- Predictive dialing ratios (5:1+) work only for high-volume campaigns with stable answer rates
- Low-volume campaigns (<1000 dials/day) should use fixed ratio (2:1) to avoid statistical noise
- Handle time variance drives abandonment — high-variance campaigns need lower ratios
- Ratio should never go below 1:1 (one call per agent) to prevent intentional agent idle time
- Monitor ratio effectiveness: utilization vs. abandonment rate trade-off curve per campaign
- Carrier answer rates change after carrier maintenance, routing changes, or number pooling changes
- Ratio calculation latency must be <10ms to avoid delaying dial requests
- Test ratio changes with gradual increments (10% steps) to observe abandonment rate impact
- ML-predicted answer rates outperform simple moving averages once sufficient training data exists
- Store ratio history for post-campaign analysis and future campaign configuration
- Ratio floor should prevent starvation — a minimum ratio ensures some dialing even during low-rate periods
- Answer rate consolidation across similar campaigns improves statistical significance for low-volume campaigns
