# Section 08: Simulation Orchestration & Scaling

## Overview

Simulation orchestration manages the execution of conversation simulations at scale, distributing work across multiple workers, managing result aggregation, and handling failure scenarios. The orchestration layer is critical for running large simulation suites efficiently, especially when testing across multiple agent configurations, languages, and conversation flows.

The orchestrator supports running simulations in parallel across a cluster of worker nodes, with intelligent load balancing, result deduplication, and centralized monitoring. It handles worker failures gracefully, rescheduling failed simulations on healthy workers.

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
class SimulationOrchestrator {
  private queue: Queue;
  private workers: Worker[];

  constructor(private config: OrchestratorConfig) {
    this.queue = new Queue('simulations', {
      connection: config.redisUrl,
      defaultJobOptions: {
        attempts: 3,
        backoff: { type: 'exponential', delay: 1000 },
        removeOnComplete: 100,
        removeOnFail: 50,
      },
    });
  }

  async orchestrate(suite: SimulationSuite): Promise<OrchestrationResult> {
    // Create jobs from suite configuration
    const jobs = this.createJobs(suite);
    
    // Add all jobs to queue
    const queuedJobs = await this.queue.addBulk(jobs);
    
    // Start workers
    await this.startWorkers(suite);
    
    // Wait for completion
    const results = await this.waitForCompletion(queuedJobs);
    
    // Aggregate results
    return this.aggregate(results);
  }

  private createJobs(suite: SimulationSuite): JobData[] {
    const jobs: JobData[] = [];
    
    for (const flow of suite.flows) {
      for (const agent of suite.agents) {
        for (const language of suite.languages) {
          for (let i = 0; i < suite.iterations; i++) {
            jobs.push({
              name: `${flow.name}-${agent.id}-${language}-${i}`,
              data: {
                flowName: flow.name,
                agentId: agent.id,
                language,
                seed: i,
                config: suite.config,
              },
              opts: {
                priority: flow.tier === 'critical' ? 1 : 5,
              },
            });
          }
        }
      }
    }
    
    return jobs;
  }

  private async startWorkers(suite: SimulationSuite): Promise<void> {
    const workerCount = suite.parallelism || this.config.defaultWorkers;
    
    for (let i = 0; i < workerCount; i++) {
      const worker = new Worker('simulations', async (job) => {
        const engine = new SimulationEngine(this.config.engineConfig);
        return engine.simulate(job.data.flowName, {
          agentId: job.data.agentId,
          language: job.data.language,
          seed: job.data.seed,
        });
      }, {
        connection: this.config.redisUrl,
        concurrency: this.config.simulationsPerWorker,
      });
      
      this.workers.push(worker);
    }
  }

  private async waitForCompletion(jobs: Job[]): Promise<SimulationResult[]> {
    const results: SimulationResult[] = [];
    
    for (const job of jobs) {
      const result = await job.waitUntilFinished(
        this.config.jobTimeout
      );
      results.push(result);
    }
    
    return results;
  }
}
```

## Integration Points

- **CI/CD Pipeline**: Orchestrator integrated with CI for automated simulation runs
- **Analytics Dashboards**: Results consumed by analytics platform
- **Alerting System**: Failed simulations trigger alerts
- **Agent Testing Dashboard**: Real-time progress displayed during simulation runs
- **API Gateway**: Simulation results accessible via API

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **Worker Scaling**: Auto-scale workers based on queue depth
- **Resource Allocation**: CPU-intensive simulations need dedicated workers
- **Cost Management**: Cloud worker costs can grow; use spot instances
- **Failure Modes**: Handle worker crashes, queue corruption, result loss
- **Job Timeout**: Enforce per-job timeout to prevent hanging workers
