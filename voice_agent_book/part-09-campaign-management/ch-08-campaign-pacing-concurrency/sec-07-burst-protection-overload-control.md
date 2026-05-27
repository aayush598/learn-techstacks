# Section 07: Burst Protection & Overload Control

## Overview

Burst protection and overload control mechanisms prevent the dialing system from exceeding carrier-imposed rate limits, overwhelming agent capacity, or triggering compliance violations during sudden spikes in call volume. Bursts occur when a large batch of contacts becomes available simultaneously (new list import, timezone boundary crossings, campaign activation after pause), when retry queues flush, or when predictive dialing overestimates available capacity. Without burst protection, these spikes can cause call failure rates exceeding 30%, carrier account suspension, TCPA violation risks from abandoned calls exceeding regulatory thresholds, and downstream system overload.

The burst protection system operates as a multi-layered defense: rate limiters at the carrier interface smooth out short-term spikes, circuit breakers prevent cascading failures when downstream systems degrade, load shedding prioritizes high-value calls during capacity crunches, and predictive pacing pre-adjusts dialing rates before burst conditions materialize. Each layer has distinct time constants and response characteristics, from sub-second rate limiting to minute-level circuit breaker recovery.

## Architecture

```
                    Burst Protection Architecture

   Contact Available Events (Batch release, TZ boundary, Queue flush)
              |
              v
   +-----------------------+
   |  Predictive Pacing    |  Prevents bursts before they happen
   |  (Anticipatory)       |  by smoothing release rates
   +-----------------------+
              |
              v (Smoothed flow)
   +-----------------------+
   |  Token Bucket Filter  |  Short-term rate smoothing (100ms-1s)
   |  (Per-campaign,       |  Ensures per-second rate limits
   |   Per-carrier trunk)  |
   +-----------------------+
              |
              v (Regulated flow)
   +-----------------------+
   |  Circuit Breaker      |  Detects downstream degradation
   |  (Carrier, Agent,     |  Opens on error threshold breach
   |   Internal)           |  Half-opens for recovery test
   +-----------------------+
              |
              v (Protected flow)
   +-----------------------+
   |  Load Shedder         |  Prioritizes calls during overload
   |  (Priority Queue)     |  Drops lowest-priority calls first
   +-----------------------+
              |
              v
        Dialing Engine
```

## Design Decisions

- **Token bucket over leaky bucket for burst handling:** Token buckets allow short bursts up to a configured capacity while enforcing a long-term average rate. A leaky bucket forces perfectly smooth output regardless of input patterns. Token buckets better accommodate legitimate burst scenarios (e.g., timezone transitions where thousands of contacts suddenly become callable at 8 AM Eastern) while still protecting carriers. Trade-off: token buckets permit brief rate spikes that could still trigger carrier alarms if the burst capacity is set too high.

- **Three-state circuit breaker (closed/open/half-open) with exponential recovery:** After a circuit opens due to excessive errors, it transitions to half-open after a recovery timeout that doubles with each consecutive failure (30s, 60s, 120s, 300s max). This prevents thundering herd recovery where all campaigns retry simultaneously after a carrier outage. Trade-off: exponential backoff increases recovery time for transient failures that could be resolved quickly.

- **Priority-based load shedding with queued preemption:** When the system exceeds safe capacity, lower-priority calls are preempted from the dial queue in favor of higher-priority calls. Priority levels are campaign-level (revenue > compliance > survey > reminder) with per-contact overrides (high-value customer, time-sensitive offer). Trade-off: lower-priority campaigns may experience prolonged starvation during sustained overload.

- **Real-time burst detection with predictive pre-smoothing:** The system monitors contact release velocity and dial request velocity separately. When release velocity exceeds configurable thresholds, the system automatically throttles contact release to prevent burst generation at the source. This addresses bursts before they reach the rate limiter. Trade-off: pre-smoothing can delay time-sensitive calls if thresholds are set too conservatively.

## Implementation Approach

```
interface BurstProtectionConfig {
  tokenBucket: {
    capacity: number;         // Max burst size (e.g., 50 calls)
    refillRate: number;       // Tokens per second (e.g., 10/sec)
    refillInterval: number;   // Refill tick in ms (e.g., 100)
  };
  circuitBreaker: {
    errorThreshold: number;   // % errors to open circuit (e.g., 50)
    halfOpenTimeout: number;  // Initial recovery wait (ms)
    maxHalfOpenTimeout: number; // Max recovery wait (ms)
    consecutiveFailuresToOpen: number; // e.g., 5
    successCountToClose: number; // e.g., 3
  };
  loadShedder: {
    maxQueueDepth: number;
    priorityLevels: number;   // 1 (highest) to N (lowest)
    preemptionEnabled: boolean;
  };
}

class BurstProtectionManager {
  constructor() {
    this.tokenBuckets = new Map();  // campaign+trunk -> bucket
    this.circuitBreakers = new Map(); // target -> breaker
    this.loadShedder = new LoadShedder();
    this.metrics = new MetricsCollector();
  }

  async shouldDial(callRequest) {
    const breaker = this.circuitBreakers.get(callRequest.target);
    if (breaker && breaker.state === 'open') {
      this.metrics.increment('dial.blocked.circuit_breaker');
      return { allow: false, reason: 'circuit_open' };
    }

    const bucket = this.tokenBuckets.get(
      `${callRequest.campaignId}:${callRequest.trunkId}`
    );
    if (bucket && !bucket.tryConsume()) {
      this.metrics.increment('dial.blocked.rate_limit');
      return { allow: false, reason: 'rate_limited' };
    }

    if (this.loadShedder.shouldDrop(callRequest)) {
      this.metrics.increment('dial.blocked.load_shedding');
      return { allow: false, reason: 'load_shed' };
    }

    return { allow: true };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **Bottleneck** (MIT) | Node.js | Rate limiting and throttling |
| **Opossum** (MIT) | Node.js | Circuit breaker pattern |
| **Rate Limiter Flexible** (MIT) | Node.js | Flexible rate limiting |
| **node-resque** (MIT) | Node.js | Job queue with rate limiting |
| **BullMQ** (MIT) | Node.js | Priority queue with rate limiting |
| **Hystrix** (Apache 2.0) | Java | Circuit breaker (reference) |

## Production Considerations

**Scaling:** Burst protection state is stored in Redis for distributed consistency across multiple dialer instances. Token bucket refill counts must be atomic operations using Redis Lua scripts or `INCR` with expiry to prevent race conditions. Circuit breaker state transitions require distributed locking or a consensus protocol (Redis Redlock) for accuracy under high concurrency.

**Security:** Rate limiting configurations must be protected from tenant manipulation — a compromised tenant should not be able to disable burst protection for their campaigns. Circuit breaker thresholds should be auditable to detect targeted denial-of-service attempts where an attacker intentionally triggers carrier errors.

**Monitoring:** Alert on circuit breaker transitions (open > 5 minutes), sustained rate limiting exceeding 10% of dial attempts, load shedder activity dropping > 5% of calls, and token bucket refill rate approaching zero. Dashboard metrics should show real-time bucket fill levels, circuit breaker states, and dropped call counts by reason code.
