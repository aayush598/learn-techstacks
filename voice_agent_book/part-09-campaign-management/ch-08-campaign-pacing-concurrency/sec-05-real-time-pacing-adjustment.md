# Section 05: Real-Time Pacing Adjustment

## Overview

Real-time pacing adjustment continuously modifies dialing parameters based on instantaneous feedback from the call pipeline. Unlike static pacing (which uses fixed dialing ratios and throttle rates), real-time adjustment monitors call events as they happen — answer events, abandon events, agent availability changes, and carrier latency — and adjusts the pacing algorithm in sub-second timeframes. This feedback loop is what separates an average predictive dialer from a great one: the ability to detect an unexpected drop in answer rates and immediately reduce the dialing ratio before abandonment rates spike.

The adjustment operates on multiple timescales: micro-adjustments (per-second, based on recent answer/abandon ratio), medium adjustments (per-minute, based on rolling window statistics), and macro adjustments (per-hour, based on predicted volume patterns). Each timescale has its own feedback loop with appropriate damping to prevent oscillation. The system uses PID (Proportional-Integral-Derivative) controller concepts from control theory, adapted for the stochastic nature of outbound calling.

## Architecture

```
              Real-Time Pacing Adjustment Loop

  +------------------+     +------------------+
  | Call Events      |     | Agent Events     |
  | (answer, no      |     | (available, busy,|
  |  answer, abandon,|     |  break, ACW)     |
  |  AMD result)     |     |                  |
  +--------+---------+     +--------+---------+
           |                        |
           v                        v
  +---------------------------------------------+
  |           Event Stream Processor             |
  |                                              |
  |  Aggregates events into sliding windows:    |
  |  - 15-second window (micro)                  |
  |  - 5-minute window (medium)                  |
  |  - 30-minute window (macro)                  |
  +---------------------------------------------+
           |                        |
           v                        v
  +---------------------------------------------+
  |          PID Adjustment Controller           |
  |                                              |
  |  Setpoint: target abandon rate (3%)          |
  |  Input: current abandon rate                 |
  |  Output: ratio adjustment factor             |
  |                                              |
  |  P: proportional (react to current error)    |
  |  I: integral (react to accumulated error)    |
  |  D: derivative (react to rate of change)     |
  +---------------------------------------------+
           |                        |
           v                        v
  +------------------+     +------------------+
  | Ratio Adjustment |     | Throttle         |
  | (modify dialing  |     | Adjustment       |
  |  ratio sec-02)   |     | (CPS sec-04)     |
  +------------------+     +------------------+
```

## Design Decisions

- **PID controller with abandonment rate as process variable:** The target abandonment rate (typically 3% for TCPA) is the setpoint. The measured abandonment rate is the process variable. The controller output adjusts the dialing ratio. Trade-off: PID tuning is non-trivial; incorrect gains cause oscillation or slow response.

- **Dual feedback loops — ratio and throttle:** Two independent control loops operate simultaneously: the ratio loop adjusts dial attempts per available agent; the throttle loop adjusts calls per second. The ratio loop handles agent-utilization dynamics while the throttle loop handles carrier/system capacity dynamics. Trade-off: two loops can interact counterproductively if not properly coordinated.

- **Adaptive gain scheduling:** PID gains change based on operating conditions. During steady state, conservative gains prevent oscillation. During rapid change (e.g., campaign launch), aggressive gains enable fast convergence. Trade-off: gain scheduling requires extensive tuning for each operating region.

- **Deadband to prevent dithering:** A deadband around the setpoint (±0.5% abandonment rate) prevents the controller from making small adjustments for statistical noise. Only when the error exceeds the deadband does the controller act. Trade-off: slightly wider steady-state error range vs. reduced control churn.

## Implementation Approach

```
class PidController {
  constructor(config) {
    this.kp = config.kp || 2.0;   // Proportional gain
    this.ki = config.ki || 0.5;   // Integral gain
    this.kd = config.kd || 1.0;   // Derivative gain
    this.setpoint = config.setpoint || 0.03; // Target abandon rate
    this.deadband = config.deadband || 0.005; // ±0.5% deadband

    this.integral = 0;
    this.lastError = 0;
    this.lastUpdate = Date.now();
    this.integralLimit = config.integralLimit || 1.0;
    this.outputMin = config.outputMin || 0.5;
    this.outputMax = config.outputMax || 2.0;
  }

  update(currentValue) {
    const now = Date.now();
    const dt = Math.max((now - this.lastUpdate) / 1000, 0.01); // seconds
    this.lastUpdate = now;

    const error = this.setpoint - currentValue;

    // Deadband: no action if error is small
    if (Math.abs(error) < this.deadband) {
      return 1.0; // No adjustment
    }

    // Proportional
    const pTerm = this.kp * error;

    // Integral (with anti-windup)
    this.integral += this.ki * error * dt;
    this.integral = Math.max(-this.integralLimit, Math.min(this.integralLimit, this.integral));

    // Derivative
    const dTerm = this.kd * (error - this.lastError) / Math.max(dt, 0.001);
    this.lastError = error;

    // Calculate output
    let output = 1.0 + pTerm + this.integral + dTerm;

    // Clamp output
    output = Math.max(this.outputMin, Math.min(this.outputMax, output));

    return output;
  }

  reset() {
    this.integral = 0;
    this.lastError = 0;
  }
}

class RealTimePacingAdjuster {
  constructor(storage, metrics) {
    this.storage = storage;
    this.metrics = metrics;
    this.controllers = new Map(); // campaignId -> PidController
    this.windows = {
      micro: new SlidingWindow(15000),  // 15s
      medium: new SlidingWindow(300000), // 5min
      macro: new SlidingWindow(1800000) // 30min
    };
    this.gainSchedules = {
      startup: { kp: 4.0, ki: 1.0, kd: 2.0 },
      normal: { kp: 2.0, ki: 0.5, kd: 1.0 },
      stable: { kp: 1.0, ki: 0.2, kd: 0.5 }
    };
  }

  async handleCallEvent(campaignId, event) {
    // Record event in all windows
    this.windows.micro.add(campaignId, event);
    this.windows.medium.add(campaignId, event);
    this.windows.macro.add(campaignId, event);

    // Micro-adjustment: every 15 seconds or on abandon events
    if (event.type === 'abandon' || this.windows.micro.shouldProcess(campaignId)) {
      const adjustment = await this.calculateAdjustment(campaignId, 'micro');
      await this.applyAdjustment(campaignId, adjustment);
    }

    // Medium adjustment: every 5 minutes
    if (this.windows.medium.shouldProcess(campaignId)) {
      const adjustment = await this.calculateAdjustment(campaignId, 'medium');
      await this.applyAdjustment(campaignId, adjustment);
    }

    // Macro adjustment: update gain schedule
    if (this.windows.macro.shouldProcess(campaignId)) {
      await this.updateGainSchedule(campaignId);
    }
  }

  async calculateAdjustment(campaignId, windowType) {
    const window = this.windows[windowType];
    const events = window.getEvents(campaignId);

    if (events.length < 10) {
      return { factor: 1.0, reason: 'insufficient_data' };
    }

    // Calculate current abandonment rate
    const connected = events.filter(e => e.type === 'connect').length;
    const abandoned = events.filter(e => e.type === 'abandon').length;
    const abandonRate = connected > 0 ? abandoned / connected : 0;

    // Calculate answer rate
    const dialed = events.filter(e => e.type === 'dial').length;
    const answered = events.filter(e => e.type === 'answer').length;
    const answerRate = dialed > 0 ? answered / dialed : 0;

    // Get or create PID controller
    if (!this.controllers.has(campaignId)) {
      const schedule = await this.detectOperatingPhase(campaignId);
      const config = this.gainSchedules[schedule];
      this.controllers.set(campaignId, new PidController({
        ...config,
        setpoint: await this.getAbandonTarget(campaignId)
      }));
    }

    const controller = this.controllers.get(campaignId);
    const factor = controller.update(abandonRate);

    this.metrics.gauge('pacing.abandon_rate', abandonRate, { campaign: campaignId });
    this.metrics.gauge('pacing.answer_rate', answerRate, { campaign: campaignId });
    this.metrics.gauge('pacing.pid_factor', factor, { campaign: campaignId });
    this.metrics.gauge('pacing.pid_integral', controller.integral, { campaign: campaignId });

    return {
      factor,
      abandonRate,
      answerRate,
      connected,
      abandoned,
      windowType,
      pid: {
        p: controller.kp * (controller.setpoint - abandonRate),
        i: controller.integral,
        d: controller.kd * (controller.lastError - (controller.setpoint - abandonRate))
      }
    };
  }

  async applyAdjustment(campaignId, adjustment) {
    if (adjustment.factor === 1.0) return;

    // 1. Adjust dialing ratio
    const currentRatio = await this.pacingService.getCurrentRatio(campaignId);
    const newRatio = currentRatio * adjustment.factor;

    // Clamp to campaign limits
    const campaign = await this.campaignService.get(campaignId);
    const clampedRatio = Math.max(
      campaign.pacingConfig.minRatio || 1,
      Math.min(newRatio, campaign.pacingConfig.maxRatio || 10)
    );

    await this.pacingService.setRatio(campaignId, clampedRatio);

    // 2. Adjust throttle rate in proportion to ratio change
    const currentThrottle = await this.throttleService.getCampaignRate(campaignId);
    const newThrottle = currentThrottle * Math.sqrt(adjustment.factor); // Conservative throttle adjustment

    await this.throttleService.setCampaignRate(campaignId, newThrottle);

    // 3. Log adjustment
    await this.logAdjustment(campaignId, adjustment, currentRatio, clampedRatio);

    this.metrics.gauge('pacing.current_ratio', clampedRatio, { campaign: campaignId });
    this.metrics.gauge('pacing.current_throttle', newThrottle, { campaign: campaignId });
  }

  async logAdjustment(campaignId, adjustment, oldRatio, newRatio) {
    const record = {
      campaignId,
      timestamp: new Date(),
      oldRatio,
      newRatio,
      adjustmentFactor: adjustment.factor,
      abandonRate: adjustment.abandonRate,
      answerRate: adjustment.answerRate,
      windowType: adjustment.windowType,
      pidTerms: adjustment.pid,
      reason: adjustment.reason || 'automatic'
    };

    await this.storage.insert('pacing_adjustments', record);
  }

  async detectOperatingPhase(campaignId) {
    const events = this.windows.macro.getEvents(campaignId);

    if (events.length < 100) {
      return 'startup'; // Not enough data, be aggressive
    }

    // Check if abandonment rate has been stable for 30 minutes
    const abandonRates = this.getTimeSeriesRates(events, 'abandon', 10);
    const variance = this.calculateVariance(abandonRates);

    if (variance < 0.001) {
      return 'stable'; // Very stable
    }

    return 'normal';
  }

  async updateGainSchedule(campaignId) {
    const phase = await this.detectOperatingPhase(campaignId);
    const controller = this.controllers.get(campaignId);

    if (controller && phase) {
      const gains = this.gainSchedules[phase];
      controller.kp = gains.kp;
      controller.ki = gains.ki;
      controller.kd = gains.kd;
    }
  }

  async getAbandonTarget(campaignId) {
    // Allow per-campaign override, default to 3%
    const campaign = await this.campaignService.get(campaignId);
    return campaign.pacingConfig?.abandonmentRateTarget || 0.03;
  }

  calculateVariance(values) {
    if (values.length < 2) return Infinity;
    const mean = values.reduce((a, b) => a + b) / values.length;
    const squaredDiffs = values.map(v => (v - mean) ** 2);
    return squaredDiffs.reduce((a, b) => a + b) / (values.length - 1);
  }

  getTimeSeriesRates(events, eventType, numBuckets) {
    // Split events into time buckets and calculate rate for each
    if (events.length === 0) return [];

    const sorted = [...events].sort((a, b) => a.timestamp - b.timestamp);
    const startTime = sorted[0].timestamp;
    const endTime = sorted[sorted.length - 1].timestamp;
    const bucketSize = (endTime - startTime) / numBuckets;

    const buckets = Array(numBuckets).fill(0).map(() => ({ total: 0, event: 0 }));

    for (const event of events) {
      const bucketIndex = Math.min(
        Math.floor((event.timestamp - startTime) / bucketSize),
        numBuckets - 1
      );
      buckets[bucketIndex].total++;
      if (event.type === eventType) {
        buckets[bucketIndex].event++;
      }
    }

    return buckets.map(b => b.total > 0 ? b.event / b.total : 0);
  }
}

class SlidingWindow {
  constructor(durationMs) {
    this.durationMs = durationMs;
    this.events = new Map(); // campaignId -> Event[]
    this.lastProcessed = new Map(); // campaignId -> timestamp
  }

  add(campaignId, event) {
    if (!this.events.has(campaignId)) {
      this.events.set(campaignId, []);
    }
    this.events.get(campaignId).push({
      ...event,
      timestamp: Date.now()
    });
    this.prune(campaignId);
  }

  shouldProcess(campaignId) {
    const lastProcessed = this.lastProcessed.get(campaignId) || 0;
    return (Date.now() - lastProcessed) >= this.durationMs;
  }

  getEvents(campaignId) {
    this.prune(campaignId);
    return this.events.get(campaignId) || [];
  }

  markProcessed(campaignId) {
    this.lastProcessed.set(campaignId, Date.now());
  }

  prune(campaignId) {
    const cutoff = Date.now() - this.durationMs;
    const events = this.events.get(campaignId);
    if (events) {
      this.events.set(campaignId, events.filter(e => e.timestamp >= cutoff));
    }
  }
}
```

## Integration Points

- **Dialing Ratio (sec-02):** Primary control output — adjusts ratio in real-time
- **Campaign Throttling (sec-04):** Secondary control output — adjusts CPS limits
- **Pacing Algorithm (sec-06):** PID controller feeds adjusted parameters to the algorithm
- **Burst Protection (sec-07):** Abrupt adjustments may trigger burst detection; coordinate thresholds
- **Concurrency Limits (sec-01):** Ratio changes affect concurrency limit consumption
- **Agent Utilization (sec-03):** Pacing adjustments directly impact agent idle/busy patterns
- **Campaign Analytics (Ch 09):** Pacing adjustment history for post-campaign analysis
- **Monitoring (sec-08):** PID metrics, adjustment frequency, and effectiveness tracking

## Open-Source Tools

- **node-pid-controller:** PID controller implementation reference
- **Redis (with sorted sets):** Event window storage for distributed pacing state
- **Apache Kafka / Redis Streams:** Call event stream processing for adjustment calculations
- **Prometheus:** PID controller metrics (setpoint, process variable, output)
- **Grafana:** Real-time pacing adjustment dashboards
- **simple-statistics:** Statistical functions for variance and rate calculations

## Production Considerations

- PID controller gains must be tuned per campaign type — a collections campaign behaves differently from a survey campaign
- Abandonment rate measurement window must be long enough for statistical significance (>100 connected calls)
- Micro-adjustments should be dampened to prevent over-reaction to single abandon events
- PID integral windup protection is critical — accumulated error from past poor performance should not cause runaway adjustments
- Deadband prevents dithering but must be small enough to maintain compliance (±0.5% is typical)
- Adjustment logging is essential for debugging pacing issues — log every adjustment with context
- Controller reset on campaign config changes (ratio limits, abandon target) prevents stale state
- Gain scheduling transitions should be smooth — sudden gain changes can cause oscillation
- Consider override capability for manual pacing during campaigns with special requirements
- Real-time adjustments create observable agent experience changes — communicate ratio changes to supervisors
- Adjustment frequency should decrease as confidence in the model increases (stable phase)
- PID parameters should be versioned alongside campaign config for reproducibility
- Monitor adjustment effectiveness: compare abandonment rate variance with and without adjustments
- Distributed systems must use consistent event ordering for PID calculations across instances
- Circuit breaker: if adjustment factor exceeds safe bounds (e.g., <0.3 or >3.0), reset controller to default
