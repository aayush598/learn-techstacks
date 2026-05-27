# Section 04: Campaign Throttling Mechanisms

## Overview

Campaign throttling mechanisms control the rate at which dial attempts are placed for a campaign, independent of agent availability and concurrency limits. While concurrency limits (sec-01) cap the number of simultaneous active calls, throttling controls the rate of new call initiation — typically measured in calls per second (CPS) or calls per minute (CPM). Throttling prevents carrier rate limiting (telecom carriers enforce strict CPS limits per trunk group), protects downstream systems (CRM, dialer database) from request spikes, and ensures fair resource allocation across campaigns.

The primary throttling mechanism is the token bucket algorithm, which allows bursty traffic up to a configured peak rate while enforcing a sustained average rate. This is superior to simple fixed-rate limiting because it accommodates natural burstiness in dialing patterns while still providing hard rate guarantees. Token bucket parameters — refill rate (sustained CPS), bucket size (burst CPS), and initial tokens — are configurable per campaign, per carrier trunk, and per time-of-day to optimize throughput while respecting carrier constraints.

## Architecture

```
              Campaign Throttling Architecture

  +------------------+     +------------------+
  | Dial Request     |     | Campaign Config  |
  | (from pacing     |     | (CPS limits,     |
  |  engine)         |     |  burst size)     |
  +--------+---------+     +--------+---------+
           |                        |
           v                        v
  +---------------------------------------------+
  |        Token Bucket Throttle                 |
  |                                              |
  |  Layer 1: Campaign-level throttle            |
  |    - refill_rate = campaign_max_cps          |
  |    - bucket_size = campaign_burst_cps        |
  |                                              |
  |  Layer 2: Trunk-level throttle               |
  |    - refill_rate = trunk_max_cps             |
  |    - bucket_size = trunk_burst_cps           |
  |                                              |
  |  Layer 3: Global throttle                    |
  |    - refill_rate = global_max_cps            |
  |    - bucket_size = burst_cps                 |
  +---------------------------------------------+
           |         |                |
           v         v                v
  +-----------+ +---------+ +----------------+
  | Allow     | | Delay   | | Reject        |
  | (proceed  | | (queue  | | (return error |
  |  to dial) | |  & wait)| |  to caller)   |
  +-----------+ +---------+ +----------------+
```

## Design Decisions

- **Multi-layer token bucket with cascade evaluation:** Each dial request must pass through campaign → trunk → global token buckets sequentially. If any bucket is empty, the request is either queued (delay strategy) or rejected (fail-fast strategy). Trade-off: multi-layer check adds latency but provides precise control at each level.

- **Queue-based backpressure with timeout:** When throttled, dial requests enter a priority queue with configurable TTL (typically 5-30 seconds). The queue drains as tokens become available. Requests that timeout in the queue are returned to the pacing engine for re-evaluation. Trade-off: queue depth management complexity vs. better throughput during brief throttling periods.

- **Time-of-day throttling profiles:** Throttle parameters change automatically based on time-of-day profiles. Nighttime may have lower CPS limits to comply with calling hour regulations; peak hours may have higher limits. Trade-off: additional configuration complexity vs. regulatory compliance and optimal resource use.

- **Carrier-aware throttle adjustment:** Carrier responses (429 rate limited, 503 service unavailable) automatically reduce the throttle rate for that carrier. The system learns carrier-specific limits and self-tunes to avoid hitting rate limits. Trade-off: requires carrier response monitoring and feedback loop vs. static carrier-rated limits.

## Implementation Approach

```
interface ThrottleConfig {
  refillRate: number;  // Tokens per second (sustained CPS)
  bucketSize: number;  // Maximum tokens (burst CPS)
  refillInterval: number; // ms between refills
}

class TokenBucket {
  constructor(config) {
    this.config = config;
    this.tokens = config.bucketSize;
    this.lastRefill = Date.now();
    this.maxTokens = config.bucketSize || config.refillRate;
  }

  tryConsume(count = 1) {
    this.refill();
    if (this.tokens >= count) {
      this.tokens -= count;
      return true;
    }
    return false;
  }

  refill() {
    const now = Date.now();
    const elapsed = now - this.lastRefill;
    const refillAmount = (elapsed / 1000) * this.config.refillRate;
    this.tokens = Math.min(this.maxTokens, this.tokens + refillAmount);
    this.lastRefill = now;
  }

  getWaitTime(count = 1) {
    this.refill();
    if (this.tokens >= count) return 0;
    const deficit = count - this.tokens;
    return (deficit / this.config.refillRate) * 1000;
  }

  get utilization() {
    return 1 - (this.tokens / this.maxTokens);
  }
}

class CampaignThrottle {
  constructor(storage, metrics) {
    this.storage = storage;
    this.metrics = metrics;
    this.buckets = {
      campaign: new Map(), // campaignId -> TokenBucket
      trunk: new Map(),    // trunkId -> TokenBucket
      global: new TokenBucket({
        refillRate: 100, // 100 CPS global max
        bucketSize: 200,  // 200 burst
        refillInterval: 100
      })
    };
    this.requestQueue = new Map(); // priority -> Request[]
  }

  async canProceed(campaignId, trunkId, priority = 'normal') {
    const campaignBucket = await this.getCampaignBucket(campaignId);
    const trunkBucket = await this.getTrunkBucket(trunkId);

    // Evaluate all layers
    const globalOk = this.buckets.global.tryConsume();
    const campaignOk = campaignBucket.tryConsume();
    const trunkOk = trunkBucket ? trunkBucket.tryConsume() : true;

    const allowed = globalOk && campaignOk && trunkOk;

    // Metrics
    this.metrics.increment('throttle.check', {
      campaign: campaignId,
      trunk: trunkId,
      allowed: allowed.toString(),
      reason: !globalOk ? 'global' : !campaignOk ? 'campaign' : !trunkOk ? 'trunk' : 'ok'
    });

    return {
      allowed,
      waitTime: allowed ? 0 : Math.max(
        this.buckets.global.getWaitTime(),
        campaignBucket.getWaitTime()
      )
    };
  }

  async throttleDialRequest(campaignId, trunkId, request, priority = 'normal') {
    const result = await this.canProceed(campaignId, trunkId, priority);

    if (result.allowed) {
      return { action: 'proceed', delayMs: 0 };
    }

    // Check if we should queue or reject
    const config = await this.getCampaignThrottleConfig(campaignId);
    if (config.strategy === 'queue') {
      const queued = await this.enqueueRequest(campaignId, request, priority, result.waitTime);
      return { action: 'queued', delayMs: result.waitTime, queuePosition: queued };
    }

    return { action: 'rejected', delayMs: 0, reason: 'throttled' };
  }

  async enqueueRequest(campaignId, request, priority, estimatedWaitMs) {
    const maxQueueTime = await this.getMaxQueueTime(campaignId);

    if (estimatedWaitMs > maxQueueTime) {
      return null; // Would timeout, don't queue
    }

    const queueKey = this.getQueueKey(campaignId, priority);
    if (!this.requestQueue.has(queueKey)) {
      this.requestQueue.set(queueKey, []);
    }

    const queue = this.requestQueue.get(queueKey);
    const entry = {
      request,
      enqueuedAt: Date.now(),
      timeoutAt: Date.now() + maxQueueTime,
      priority: this.priorityValue(priority),
      callId: request.callId
    };

    queue.push(entry);
    // Sort by priority then enqueue time
    queue.sort((a, b) => b.priority - a.priority || a.enqueuedAt - b.enqueuedAt);

    this.metrics.gauge('throttle.queue_depth', queue.length, {
      campaign: campaignId,
      priority
    });

    return queue.length;
  }

  async drainQueue(campaignId) {
    const priorities = ['critical', 'high', 'normal', 'low'];

    for (const priority of priorities) {
      const queueKey = this.getQueueKey(campaignId, priority);
      const queue = this.requestQueue.get(queueKey) || [];
      const now = Date.now();

      while (queue.length > 0) {
        const entry = queue[0];

        // Check timeout
        if (now > entry.timeoutAt) {
          queue.shift(); // Remove timed-out request
          this.metrics.increment('throttle.queue_timeout', {
            campaign: campaignId,
            priority
          });
          continue;
        }

        // Try to consume token
        const trunkId = entry.request.trunkId;
        const result = await this.canProceed(campaignId, trunkId, priority);

        if (result.allowed) {
          queue.shift();
          return entry.request; // Process this request
        }

        break; // No tokens available for remaining queue
      }
    }

    return null;
  }

  async getCampaignBucket(campaignId) {
    if (!this.buckets.campaign.has(campaignId)) {
      const config = await this.getCampaignThrottleConfig(campaignId);
      this.buckets.campaign.set(campaignId, new TokenBucket(config));
    }
    return this.buckets.campaign.get(campaignId);
  }

  async getTrunkBucket(trunkId) {
    if (!trunkId) return null;
    if (!this.buckets.trunk.has(trunkId)) {
      const trunk = await this.trunkService.get(trunkId);
      this.buckets.trunk.set(trunkId, new TokenBucket({
        refillRate: trunk.maxCps || 10,
        bucketSize: trunk.burstCps || 20
      }));
    }
    return this.buckets.trunk.get(trunkId);
  }

  async getCampaignThrottleConfig(campaignId) {
    const campaign = await this.campaignService.get(campaignId);
    const now = new Date();
    const hour = now.getHours();

    // Time-of-day profile selection
    let profile = campaign.throttleProfiles?.default || {
      refillRate: 5,
      bucketSize: 10,
      strategy: 'queue',
      maxQueueTimeMs: 10000
    };

    if (campaign.throttleProfiles?.timeOfDay) {
      for (const todProfile of campaign.throttleProfiles.timeOfDay) {
        if (hour >= todProfile.startHour && hour < todProfile.endHour) {
          profile = todProfile;
          break;
        }
      }
    }

    return profile;
  }

  async handleCarrierRateLimit(trunkId, response) {
    // Carrier returned rate limit — reduce trunk throttle
    const trunkBucket = await this.getTrunkBucket(trunkId);
    if (trunkBucket) {
      const reductionFactor = 0.5; // Reduce by 50%
      trunkBucket.config.refillRate *= reductionFactor;
      trunkBucket.config.bucketSize = Math.max(
        1,
        Math.floor(trunkBucket.config.bucketSize * reductionFactor)
      );

      // Schedule gradual recovery
      setTimeout(async () => {
        const original = await this.trunkService.get(trunkId);
        trunkBucket.config.refillRate = Math.min(
          trunkBucket.config.refillRate * 1.5,
          original.maxCps
        );
        trunkBucket.config.bucketSize = Math.min(
          trunkBucket.config.bucketSize * 1.5,
          original.burstCps
        );
      }, 300000); // Recover over 5 minutes
    }

    this.metrics.increment('throttle.carrier_rate_limit', { trunk: trunkId });
  }

  async adjustForSystemLoad() {
    // Reduce throttling when system is under load
    const cpuUsage = await this.getSystemCpuUsage();
    const memUsage = await this.getSystemMemoryUsage();

    if (cpuUsage > 0.8 || memUsage > 0.85) {
      this.buckets.global.config.refillRate *= 0.8;
      this.buckets.global.maxTokens = Math.floor(this.buckets.global.maxTokens * 0.8);
    } else if (cpuUsage < 0.5 && memUsage < 0.6) {
      this.buckets.global.config.refillRate = Math.min(
        this.buckets.global.config.refillRate * 1.1,
        this.buckets.global.maxTokens
      );
    }
  }

  getQueueKey(campaignId, priority) {
    return `${campaignId}:${priority}`;
  }

  priorityValue(priority) {
    const values = { critical: 4, high: 3, normal: 2, low: 1 };
    return values[priority] || 2;
  }
}
```

## Integration Points

- **Pacing Algorithm (sec-06):** Throttling limits the rate passed to the pacing algorithm
- **Concurrency Limits (sec-01):** Throttling and concurrency work together to prevent overload
- **Carrier Trunks (Part 07):** Carrier CPS limits feed into trunk-level throttling
- **Dialing Request Flow (Ch 01):** All dial requests pass through throttle before execution
- **Burst Protection (sec-07):** Throttling is the first line of defense against burst-induced overload
- **Campaign Config (Ch 01):** Throttle parameters configured per campaign with time-of-day profiles
- **Monitoring (sec-08):** Throttle utilization and queue depth monitoring

## Open-Source Tools

- **Bottleneck (npm):** Token bucket and rate limiter implementation reference
- **node-redis (with Lua):** Distributed token bucket for multi-instance deployments
- **BullMQ:** Request queue management for throttled dial requests
- **express-rate-limit / rate-limiter-flexible:** Rate limiting patterns reference
- **Prometheus:** Throttle metrics — token utilization, queue depth, rejection rate
- **node-cron:** Time-of-day throttle profile switching

## Production Considerations

- Token bucket clock synchronization is critical in distributed systems — use Redis with atomic Lua scripts
- Throttle queue depth should be bounded to prevent memory exhaustion from queued requests
- Carrier rate limit detection must be reactive — a 429 response should immediately reduce the throttle rate
- Throttle reset periods (e.g., carrier resets CPS at start of each second) should be aligned
- Queue TTL prevents stale requests from being processed minutes after their intended dial time
- Throttle metrics should include "available tokens" gauge for capacity planning
- Campaign throttle limits should be auditable — log all throttle configuration changes
- Over-throttling (setting limits too low) is as harmful as under-throttling — monitor throttle rejection rate
- Gradual throttle reduction/restoration avoids oscillation when carriers enforce dynamic rate limits
- Time-of-day profiles should account for DST transitions and holiday schedules
- Priority queuing must have fairness guarantees to prevent starvation of low-priority campaigns
- Throttle bypass for administrative/manual calls (compliance testing, quality assurance)
- Consider adaptive throttling that learns carrier limits from historical responses
- High-priority throttling should have dedicated token buckets so critical campaigns aren't blocked by normal traffic
