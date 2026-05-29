# Section 06: Load Testing Simulation

## Overview

Load testing evaluates voice agent performance under concurrent call volumes. The simulation generates synthetic traffic patterns modeling real-world usage, measures response times and throughput, and identifies bottlenecks. Tests simulate gradual load increases, burst traffic, and sustained high load to validate system behavior.

## Architecture

```
Load Testing Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Load Test Config] → [Load Generator] → [Agent Pipeline] → [Metrics Collection]
       │                    │                    │                │
  Concurrent users       Virtual caller       Target system    Prometheus
  Traffic pattern        instances            under test      + Grafana
  Duration               t=0..N                                   │
  Scenario selection    Each instance runs              [Load Test Report]
                         scenario steps                 ┌─────────────┐
                                                         │ Throughput  │
Load Patterns:                                             │ Latency     │
  ── Normal: steady 50 concurrent                         │ Error rate  │
  -·- Spike: 10→200→10                                     │ P50/P95/P99 │
  ── Stress: 10→20→50→100→200→500                         │ Bottlenecks │
                                                         └─────────────┘

Load Generator Architecture:
  ┌─────────────────────────────┐
  │   Load Test Orchestrator   │
  │   (BullMQ worker)          │
  ├─────────────────────────────┤
  │   Virtual Caller Pool      │
  │   ┌───┐ ┌───┐ ┌───┐       │
  │   │V1 │ │V2 │ │V3 │ ...  │
  │   └───┘ └───┘ └───┘       │
  │   Each runs scenario       │
  │   via STT/TTS pipeline     │
  ├─────────────────────────────┤
  │   Metrics Exporter         │
  │   → Prometheus pushgateway │
  └─────────────────────────────┘
```

## Design Decisions

- **Virtual Caller Instances**: Each simulated caller runs as an independent coroutine
- **Configurable Load Patterns**: Pre-defined patterns for common test scenarios
- **Pipeline Under Test**: Tests run against the actual agent pipeline, not mocks
- **Metrics-Backed Analysis**: Results collected via Prometheus for Grafana visualization

## Implementation Approach

```typescript
// Load test configuration
interface LoadTestConfig {
  name: string;
  scenarioPath: string;
  duration: number; // seconds
  pattern: LoadPattern;
  rampUp?: {
    initial: number;
    target: number;
    duration: number; // seconds
  };
  spike?: {
    baseline: number;
    spike: number;
    spikeDuration: number;
    recoveryDuration: number;
  };
  stress: {
    stages: Array<{ concurrency: number; duration: number }>;
  };
  steady: {
    concurrency: number;
  };
  metricsConfig: {
    prometheusPushgateway: string;
    reportingInterval: number; // seconds
  };
  thresholds: {
    p95LatencyMs: number;
    errorRate: number;
    throughputRps: number;
  };
}

type LoadPattern = 'steady' | 'spike' | 'stress' | 'ramp';

// Load test orchestrator
class LoadTestOrchestrator {
  private callerPool: VirtualCaller[];
  private metricsCollector: MetricsCollector;
  private abortController: AbortController;

  async runLoadTest(config: LoadTestConfig): Promise<LoadTestResult> {
    this.abortController = new AbortController();
    const startTime = Date.now();
    const metrics: MetricsSnapshot[] = [];

    // Start metrics collection
    const metricsInterval = setInterval(() => {
      metrics.push(this.metricsCollector.snapshot());
    }, config.metricsConfig.reportingInterval * 1000);

    try {
      // Execute load pattern
      switch (config.pattern) {
        case 'steady':
          await this.runSteady(config, startTime);
          break;
        case 'ramp':
          await this.runRampUp(config, startTime);
          break;
        case 'spike':
          await this.runSpike(config, startTime);
          break;
        case 'stress':
          await this.runStress(config, startTime);
          break;
      }

      // Final metrics snapshot
      metrics.push(this.metricsCollector.snapshot());
    } finally {
      clearInterval(metricsInterval);
      await this.stopAllCallers();
    }

    return this.generateReport(config, metrics, startTime);
  }

  private async runSteady(config: LoadTestConfig, startTime: number): Promise<void> {
    const concurrency = config.steady.concurrency;
    const endTime = startTime + (config.duration * 1000);

    this.callerPool = await this.createCallers(concurrency);

    while (Date.now() < endTime && !this.abortController.signal.aborted) {
      await this.ensureCallerCount(concurrency);
      await delay(1000); // Re-check every second
    }
  }

  private async runRampUp(config: LoadTestConfig, startTime: number): Promise<void> {
    const { initial, target, duration } = config.rampUp!;
    const rampEnd = startTime + (duration * 1000);

    this.callerPool = await this.createCallers(initial);

    // Gradually increase callers
    while (Date.now() < rampEnd) {
      const progress = (Date.now() - startTime) / (duration * 1000);
      const targetCount = Math.round(initial + (target - initial) * progress);
      await this.ensureCallerCount(targetCount);
      await delay(2000);
    }

    // Hold at target for remaining duration
    await this.ensureCallerCount(target);
    await delay(config.duration * 1000 - duration * 1000);
  }

  private async runSpike(config: LoadTestConfig, startTime: number): Promise<void> {
    const { baseline, spike, spikeDuration, recoveryDuration } = config.spike!;

    // Baseline period
    this.callerPool = await this.createCallers(baseline);
    await delay(30000);

    // Spike
    await this.ensureCallerCount(spike);
    await delay(spikeDuration * 1000);

    // Recovery
    await this.ensureCallerCount(baseline);
    await delay(recoveryDuration * 1000);
  }

  private async runStress(config: LoadTestConfig, startTime: number): Promise<void> {
    for (const stage of config.stress.stages) {
      await this.ensureCallerCount(stage.concurrency);
      const stageStart = Date.now();
      const stageEnd = stageStart + (stage.duration * 1000);

      while (Date.now() < stageEnd) {
        const snapshot = this.metricsCollector.snapshot();
        if (snapshot.errorRate > config.thresholds.errorRate) {
          // Saturation point reached — record and continue
          this.recordSaturationPoint(stage, snapshot);
          break;
        }
      }
    }
  }

  private async createCallers(count: number): Promise<VirtualCaller[]> {
    const callers: VirtualCaller[] = [];
    for (let i = 0; i < count; i++) {
      const caller = new VirtualCaller({
        id: `caller-${i}`,
        scenarioPath: this.currentConfig.scenarioPath,
        onComplete: (result) => this.metricsCollector.record(result),
      });
      await caller.start();
      callers.push(caller);
    }
    return callers;
  }

  private async ensureCallerCount(target: number): Promise<void> {
    const current = this.callerPool.length;
    if (current < target) {
      const newCallers = await this.createCallers(target - current);
      this.callerPool.push(...newCallers);
    } else if (current > target) {
      const toRemove = this.callerPool.splice(target);
      await Promise.all(toRemove.map(c => c.stop()));
    }
  }

  private generateReport(
    config: LoadTestConfig,
    metrics: MetricsSnapshot[],
    startTime: number,
  ): LoadTestResult {
    const allLatencies = this.metricsCollector.getAllLatencies();
    const sortedLatencies = [...allLatencies].sort((a, b) => a - b);

    const maxConcurrency = Math.max(...metrics.map(m => m.activeCallers));
    const totalRequests = metrics.reduce((s, m) => s + m.requestsCompleted, 0);
    const totalErrors = metrics.reduce((s, m) => s + m.errors, 0);

    return {
      testName: config.name,
      durationMs: Date.now() - startTime,
      maxConcurrency,
      totalRequests,
      totalErrors,
      errorRate: totalErrors / totalRequests,
      latency: {
        p50: sortedLatencies[Math.floor(sortedLatencies.length * 0.5)],
        p95: sortedLatencies[Math.floor(sortedLatencies.length * 0.95)],
        p99: sortedLatencies[Math.floor(sortedLatencies.length * 0.99)],
        max: sortedLatencies[sortedLatencies.length - 1],
        average: allLatencies.reduce((s, l) => s + l, 0) / allLatencies.length,
      },
      saturationPoint: this.saturationPoint,
      thresholdsMet: {
        p95Latency: this.getP95() <= config.thresholds.p95LatencyMs,
        errorRate: totalErrors / totalRequests <= config.thresholds.errorRate,
        throughput: this.getThroughput() >= config.thresholds.throughputRps,
      },
      bottlenecks: this.identifyBottlenecks(metrics),
    };
  }

  private identifyBottlenecks(metrics: MetricsSnapshot[]): string[] {
    const bottlenecks: string[] = [];
    // Analyze metrics for bottleneck patterns
    const growingLatency = metrics.slice(-10).every((m, i, arr) => {
      if (i === 0) return true;
      return m.averageLatencyMs > arr[i - 1].averageLatencyMs;
    });

    if (growingLatency) {
      bottlenecks.push('Latency growing with concurrency — possible resource contention');
    }

    return bottlenecks;
  }
}
```

## Integration Points

- **CI/CD Pipeline**: Load tests run before major releases
- **Prometheus + Grafana**: Real-time load test metrics dashboards
- **Alert System**: Threshold violations trigger automatic regression tickets

## Production Considerations

- **Isolated Test Environment**: Load tests run against dedicated staging infrastructure
- **Warm-Up Period**: Initial 60-second warm-up excluded from results
- **Cost Awareness**: Load test costs (TTS/STT usage) tracked and budgeted
- **Test Data Cleanup**: Generated data cleaned after test completion

## Open-Source Tools

- **k6**: Load testing tool for API endpoint testing
- **Prometheus**: Metrics collection and alerting
- **Grafana**: Load test metrics visualization
- **autocannon**: HTTP/2 load testing alternative
