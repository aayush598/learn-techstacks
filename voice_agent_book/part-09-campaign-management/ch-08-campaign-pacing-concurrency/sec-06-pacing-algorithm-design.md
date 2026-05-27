# Section 06: Pacing Algorithm Design

## Overview

Pacing algorithm design determines how the dialer decides when to place the next call. The pacing algorithm translates high-level goals (maximize agent utilization, minimize abandonment, respect carrier limits) into concrete dialing decisions. Different algorithm types offer different trade-offs between complexity, adaptiveness, and predictability. The most common approaches are fixed ratio (simplest, least efficient), predictive (balances utilization and abandonment), adaptive (continuously learns and adjusts), and ML-based (most sophisticated, highest data requirements).

The choice of pacing algorithm depends on campaign characteristics: volume (high-volume campaigns benefit from complex algorithms), answer rate stability (stable rates allow simpler algorithms), agent pool size (larger pools justify more sophisticated pacing), and compliance requirements (strict abandonment limits require predictive/adaptive approaches). Many production systems implement a hybrid approach — using different algorithms for different operating modes and switching between them based on conditions.

## Architecture

```
               Pacing Algorithm Selection & Execution

  +--------------------------------------------------------+
  |              Pacing Algorithm Selector                  |
  |                                                        |
  |  Campaign Characteristics → Algorithm Type:            |
  |  - High volume, stable answer rate → Predictive       |
  |  - Low volume, variable answer rate → Adaptive         |
  |  - New campaign, no history → Fixed ratio (1.5:1)     |
  |  - Very high volume, rich data → ML-based             |
  +--------------------------------------------------------+
              |          |          |          |
              v          v          v          v
  +--------+ +---------+ +-------+ +------------+
  | Fixed  | |Predicti | |Adaptiv| | ML-Based   |
  | Ratio  | |ve       | |e      | |            |
  +--------+ +---------+ +-------+ +------------+
              |          |          |          |
              +----------+----------+----------+
                         |
                         v
  +--------------------------------------------------------+
  |              Pacing Execution Engine                    |
  |                                                        |
  |  1. Calculate dial rate from algorithm                 |
  |  2. Check concurrency limits (sec-01)                  |
  |  3. Check throttle (sec-04)                            |
  |  4. Select next contact from queue                     |
  |  5. Place dial request                                 |
  |  6. Record outcome for algorithm feedback              |
  +--------------------------------------------------------+
```

## Design Decisions

- **Algorithm selection per campaign, not global:** Each campaign independently selects its pacing algorithm based on its specific characteristics. Campaigns can be migrated between algorithms as they mature and accumulate data. Trade-off: algorithmic diversity increases maintenance burden vs. optimal pacing for each campaign.

- **Graceful fallback chain:** If the primary algorithm cannot produce a result (insufficient data, model failure), the system falls back to progressively simpler algorithms. ML → predictive → adaptive → fixed ratio. Trade-off: algorithm switching may cause pacing discontinuity vs. guaranteed dialing operation.

- **Hybrid mode with weighted ensemble:** Instead of picking one algorithm, the system can blend outputs from multiple algorithms. For example, 70% weight on predictive + 30% on adaptive. Ensemble averaging produces smoother pacing than any single algorithm. Trade-off: more computationally expensive vs. more stable output.

- **Warm-up phase for new campaigns:** New campaigns start with conservative fixed-ratio pacing for the first 500-1000 dials to build initial statistics, then automatically switch to the configured primary algorithm. Trade-off: initial period of suboptimal pacing vs. avoiding garbage-in-garbage-out algorithm behavior.

## Implementation Approach

```
enum PacingAlgorithmType {
  FIXED_RATIO,
  PREDICTIVE,
  ADAPTIVE,
  ML_BASED,
  ENSEMBLE
}

interface PacingAlgorithm {
  type: PacingAlgorithmType;
  name: string;
  
  initialize(campaignId: string, config: any): Promise<void>;
  calculateDialRate(campaignId: string, context: PacingContext): Promise<DialRate>;
  recordOutcome(campaignId: string, outcome: CallOutcome): Promise<void>;
  getStatus(campaignId: string): Promise<AlgorithmStatus>;
}

interface PacingContext {
  availableAgents: number;
  connectedCalls: number;
  pendingCalls: number;
  recentAnswerRate: number;
  recentAbandonRate: number;
  averageHandleTimeMs: number;
  systemLoad: number;
  carrierStatus: Record<string, boolean>;
}

interface DialRate {
  callsPerSecond: number;
  ratio: number;
  confidence: number;
  algorithm: PacingAlgorithmType;
}

class PacingAlgorithmManager {
  constructor(metrics) {
    this.metrics = metrics;
    this.algorithms = new Map();
    this.activeCampaigns = new Map(); // campaignId -> { algorithm, config }
  }

  async setupCampaign(campaignId, algorithmType, config) {
    const algorithm = this.createAlgorithm(algorithmType);
    await algorithm.initialize(campaignId, config);

    this.activeCampaigns.set(campaignId, {
      algorithm,
      type: algorithmType,
      config,
      startedAt: Date.now(),
      dialsPlaced: 0
    });

    return algorithm;
  }

  async getDialRate(campaignId, context) {
    const campaign = this.activeCampaigns.get(campaignId);
    if (!campaign) {
      throw new Error(`Campaign ${campaignId} not set up for pacing`);
    }

    try {
      const dialRate = await campaign.algorithm.calculateDialRate(campaignId, context);
      this.metrics.gauge('pacing.algorithm.dial_rate', dialRate.callsPerSecond, {
        campaign: campaignId,
        algorithm: dialRate.algorithm
      });
      return dialRate;
    } catch (error) {
      // Fallback chain
      return this.handleAlgorithmFailure(campaignId, context, error);
    }
  }

  async handleAlgorithmFailure(campaignId, context, error) {
    // Fallback to simpler algorithm
    const current = this.activeCampaigns.get(campaignId);
    const fallbackOrder = [
      PacingAlgorithmType.ML_BASED,
      PacingAlgorithmType.PREDICTIVE,
      PacingAlgorithmType.ADAPTIVE,
      PacingAlgorithmType.FIXED_RATIO
    ];

    const currentIdx = fallbackOrder.indexOf(current.type);
    if (currentIdx < fallbackOrder.length - 1) {
      const fallbackType = fallbackOrder[currentIdx + 1];
      console.warn(`Fallback from ${current.type} to ${fallbackType} for campaign ${campaignId}: ${error.message}`);
      await this.setupCampaign(campaignId, fallbackType, current.config);
      return this.getDialRate(campaignId, context);
    }

    // Last resort: fixed ratio at 1:1
    return {
      callsPerSecond: Math.max(1, context.availableAgents / 60),
      ratio: 1,
      confidence: 1.0,
      algorithm: PacingAlgorithmType.FIXED_RATIO
    };
  }

  createAlgorithm(type) {
    switch (type) {
      case PacingAlgorithmType.FIXED_RATIO:
        return new FixedRatioAlgorithm();
      case PacingAlgorithmType.PREDICTIVE:
        return new PredictiveAlgorithm();
      case PacingAlgorithmType.ADAPTIVE:
        return new AdaptiveAlgorithm();
      case PacingAlgorithmType.ML_BASED:
        return new MlBasedAlgorithm();
      case PacingAlgorithmType.ENSEMBLE:
        return new EnsembleAlgorithm();
      default:
        return new FixedRatioAlgorithm();
    }
  }
}

// Fixed Ratio Algorithm — simplest
class FixedRatioAlgorithm {
  constructor() {
    this.type = PacingAlgorithmType.FIXED_RATIO;
    this.config = null;
  }

  async initialize(campaignId, config) {
    this.config = {
      ratio: config?.initialRatio || 2,
      ...config
    };
  }

  async calculateDialRate(campaignId, context) {
    return {
      callsPerSecond: (context.availableAgents * this.config.ratio) / 60,
      ratio: this.config.ratio,
      confidence: 1.0,
      algorithm: this.type
    };
  }

  async recordOutcome(campaignId, outcome) {
    // Fixed ratio doesn't learn
  }

  async getStatus(campaignId) {
    return {
      type: this.type,
      config: this.config,
      status: 'active'
    };
  }
}

// Predictive Algorithm — uses Erlang-C and answer rate
class PredictiveAlgorithm {
  constructor() {
    this.type = PacingAlgorithmType.PREDICTIVE;
    this.answerRateTracker = null;
    this.handleTimeTracker = null;
  }

  async initialize(campaignId, config) {
    this.config = {
      abandonTarget: config?.abandonTarget || 0.03,
      minRatio: config?.minRatio || 1,
      maxRatio: config?.maxRatio || 8,
      ...config
    };
    this.answerRateTracker = new RateTracker({ windowMs: 300000 });
    this.handleTimeTracker = new RateTracker({ windowMs: 300000 });
  }

  async calculateDialRate(campaignId, context) {
    const answerRate = this.answerRateTracker.getRate(campaignId) || 0.3;
    const handleTime = this.handleTimeTracker.getAverage(campaignId) || 180000;

    // Prevent division by zero
    const effectiveAnswerRate = Math.max(answerRate, 0.01);

    // Base ratio: how many dials per agent to keep them busy
    // ratio = 1 / (answer_rate * (1 - abandon_target))
    const baseRatio = 1 / (effectiveAnswerRate * (1 - this.config.abandonTarget));

    // Clamp ratio
    const ratio = Math.max(
      this.config.minRatio,
      Math.min(baseRatio, this.config.maxRatio)
    );

    // CPS = agents * ratio / (handle_time in seconds)
    const callsPerSecond = (context.availableAgents * ratio) / (handleTime / 1000);

    return {
      callsPerSecond: Math.max(0.1, callsPerSecond),
      ratio,
      confidence: Math.min(1, this.answerRateTracker.getCount(campaignId) / 100),
      algorithm: this.type
    };
  }

  async recordOutcome(campaignId, outcome) {
    if (outcome.type === 'dial') {
      this.answerRateTracker.recordAttempt(campaignId, outcome.answered === true);
    }
    if (outcome.handleTimeMs) {
      this.handleTimeTracker.recordValue(campaignId, outcome.handleTimeMs);
    }
  }

  async getStatus(campaignId) {
    return {
      type: this.type,
      config: this.config,
      status: 'active',
      metrics: {
        answerRate: this.answerRateTracker.getRate(campaignId),
        avgHandleTime: this.handleTimeTracker.getAverage(campaignId),
        sampleCount: this.answerRateTracker.getCount(campaignId)
      }
    };
  }
}

// Adaptive Algorithm — uses PID control from sec-05
class AdaptiveAlgorithm {
  constructor() {
    this.type = PacingAlgorithmType.ADAPTIVE;
    this.controller = null;
    this.baseRatio = 2;
  }

  async initialize(campaignId, config) {
    this.config = config || {};
    this.controller = new PidController({
      setpoint: config?.abandonTarget || 0.03,
      kp: 2.0,
      ki: 0.5,
      kd: 1.0
    });
    this.answerRateTracker = new RateTracker({ windowMs: 120000 }); // 2 min
  }

  async calculateDialRate(campaignId, context) {
    const answerRate = this.answerRateTracker.getRate(campaignId) || 0.3;
    const abandonRate = context.recentAbandonRate || 0;

    // PID adjusts the base ratio
    const pidFactor = this.controller.update(abandonRate);
    let ratio = this.baseRatio * pidFactor;

    // Adjust for answer rate changes
    if (answerRate < 0.2) {
      ratio *= 0.5;
    } else if (answerRate > 0.5) {
      ratio *= 1.5;
    }

    ratio = Math.max(1, Math.min(ratio, 10));

    const callsPerSecond = (context.availableAgents * ratio) / 60;

    return {
      callsPerSecond,
      ratio,
      confidence: 0.7,
      algorithm: this.type
    };
  }

  async recordOutcome(campaignId, outcome) {
    if (outcome.type === 'dial') {
      this.answerRateTracker.recordAttempt(campaignId, outcome.answered === true);
    }
  }

  async getStatus(campaignId) {
    return {
      type: this.type,
      config: this.config,
      status: 'active',
      metrics: {
        answerRate: this.answerRateTracker.getRate(campaignId),
        pidState: {
          integral: this.controller.integral,
          lastError: this.controller.lastError
        }
      }
    };
  }
}

// ML-Based Algorithm — uses machine learning for prediction
class MlBasedAlgorithm {
  constructor() {
    this.type = PacingAlgorithmType.ML_BASED;
    this.model = null;
  }

  async initialize(campaignId, config) {
    this.config = config || {};
    this.campaignId = campaignId;

    // Load pre-trained model or train from scratch
    this.model = await this.loadModel(campaignId);
  }

  async loadModel(campaignId) {
    // Load model from model registry
    try {
      const modelData = await this.modelRegistry.get(`pacing:${campaignId}`);
      if (modelData) return modelData;
    } catch {
      // No model yet
    }
    return null;
  }

  async calculateDialRate(campaignId, context) {
    if (!this.model) {
      // Fallback: use predictive until model is trained
      throw new Error('No ML model available');
    }

    // Feature vector for prediction
    const features = {
      availableAgents: context.availableAgents,
      timeOfDay: new Date().getHours(),
      dayOfWeek: new Date().getDay(),
      recentAnswerRate: context.recentAnswerRate,
      recentAbandonRate: context.recentAbandonRate,
      avgHandleTime: context.averageHandleTimeMs,
      connectedCalls: context.connectedCalls,
      systemLoad: context.systemLoad
    };

    const prediction = this.model.predict(features);

    return {
      callsPerSecond: prediction.optimalCps,
      ratio: prediction.optimalRatio,
      confidence: prediction.confidence,
      algorithm: this.type
    };
  }

  async recordOutcome(campaignId, outcome) {
    // Store outcome for model retraining
    await this.storage.insert('pacing_training_data', {
      campaignId,
      callId: outcome.callId,
      features: outcome.context,
      outcome: {
        answered: outcome.answered,
        handled: outcome.handled,
        abandoned: outcome.abandoned,
        handleTimeMs: outcome.handleTimeMs
      },
      timestamp: new Date()
    });
  }

  async getStatus(campaignId) {
    return {
      type: this.type,
      config: this.config,
      status: this.model ? 'active' : 'training',
      metrics: {
        modelVersion: this.model?.version,
        trainingSamples: this.model?.trainingSamples
      }
    };
  }
}

// Ensemble Algorithm — combines multiple algorithms
class EnsembleAlgorithm {
  constructor() {
    this.type = PacingAlgorithmType.ENSEMBLE;
    this.algorithms = [];
    this.weights = [];
  }

  async initialize(campaignId, config) {
    this.config = config || {};
    const algorithms = config?.algorithms || ['predictive', 'adaptive'];

    this.algorithms = algorithms.map(type => {
      switch (type) {
        case 'predictive': return new PredictiveAlgorithm();
        case 'adaptive': return new AdaptiveAlgorithm();
        default: return new FixedRatioAlgorithm();
      }
    });

    await Promise.all(
      this.algorithms.map(a => a.initialize(campaignId, config))
    );

    // Equal weights initially
    this.weights = this.algorithms.map(() => 1 / this.algorithms.length);
  }

  async calculateDialRate(campaignId, context) {
    const results = await Promise.all(
      this.algorithms.map(a => a.calculateDialRate(campaignId, context))
    );

    // Weighted average
    let totalWeight = 0;
    let weightedRatio = 0;
    let weightedCps = 0;

    for (let i = 0; i < results.length; i++) {
      const weight = this.weights[i] * results[i].confidence;
      totalWeight += weight;
      weightedRatio += results[i].ratio * weight;
      weightedCps += results[i].callsPerSecond * weight;
    }

    if (totalWeight === 0) {
      throw new Error('All ensemble members returned zero confidence');
    }

    return {
      callsPerSecond: weightedCps / totalWeight,
      ratio: weightedRatio / totalWeight,
      confidence: totalWeight / this.algorithms.length,
      algorithm: this.type
    };
  }

  async recordOutcome(campaignId, outcome) {
    await Promise.all(
      this.algorithms.map(a => a.recordOutcome(campaignId, outcome))
    );

    // Update weights based on recent accuracy
    if (outcome.type === 'dial') {
      await this.updateWeights(campaignId);
    }
  }

  async updateWeights(campaignId) {
    // Simple weight update: reward algorithms with better recent predictions
    // In production, this would use proper Bayesian updating or bandit algorithms
    const performances = await Promise.all(
      this.algorithms.map(a => this.evaluateAccuracy(a, campaignId))
    );

    const total = performances.reduce((a, b) => a + b, 0);
    if (total > 0) {
      this.weights = performances.map(p => p / total);
    }
  }

  async evaluateAccuracy(algorithm, campaignId) {
    // Evaluate how well this algorithm predicted the actual outcome
    const status = await algorithm.getStatus(campaignId);
    return 0.5; // Simplified
  }

  async getStatus(campaignId) {
    return {
      type: this.type,
      config: this.config,
      status: 'active',
      weights: this.weights,
      subAlgorithms: await Promise.all(
        this.algorithms.map(a => a.getStatus(campaignId))
      )
    };
  }
}
```

## Integration Points

- **Real-Time Adjustment (sec-05):** PID feedback loop adjusts algorithm parameters
- **Dialing Ratio (sec-02):** Algorithm output includes ratio calculation
- **Concurrency Limits (sec-01):** CPS output feeds into concurrency limit check
- **Campaign Throttling (sec-04):** CPS output feeds into throttle check
- **Agent Utilization (sec-03):** Algorithm optimization target includes utilization
- **ML Pipeline (Part 18):** Model training dataset from dialing outcomes
- **Campaign Config (Ch 01):** Algorithm selection and configuration per campaign
- **Monitoring (sec-08):** Algorithm performance metrics for comparison

## Open-Source Tools

- **TensorFlow.js / ONNX Runtime:** ML model inference for ML-based pacing
- **node-erlang / mathjs:** Erlang-C and queueing theory calculations
- **node-pid-controller:** PID control for adaptive algorithm
- **Redis:** Algorithm state persistence and distributed coordination
- **Prometheus:** Algorithm performance metrics and comparison
- **PostgreSQL (with window functions):** Answer rate and handle time tracking
- **simple-statistics:** Statistical functions for rate calculations

## Production Considerations

- Fixed ratio is better than no algorithm but leaves 15-30% agent utilization on the table
- Predictive algorithm requires >500 dials/day for statistical significance
- Adaptive algorithm handles rate changes better than predictive but may oscillate with poor PID tuning
- ML-based algorithms require significant training data (>10,000 dials) and ongoing retraining
- Ensemble algorithms are most robust but most complex to debug and tune
- Algorithm switching during a campaign should be controlled — manual approval recommended for ML→predictive transitions
- New algorithm rollout should start with low-volume campaigns for validation
- Algorithm performance comparison dashboard enables data-driven algorithm selection
- Warm-up phase should use conservative ratio (1.5:1) to avoid early abandonment spikes
- Algorithm re-initialization should preserve accumulated statistics where possible
- A/B test algorithms within the same campaign for empirical comparison (see Ch 10)
- Algorithm decision logs should capture feature vectors for post-hoc analysis
- Consider campaign lifecycle: different algorithms may be optimal at different campaign stages
- Algorithm latency must be <5ms to avoid becoming the bottleneck in the dialing pipeline
- Monitor algorithm confidence — low confidence should trigger fallback and alert
