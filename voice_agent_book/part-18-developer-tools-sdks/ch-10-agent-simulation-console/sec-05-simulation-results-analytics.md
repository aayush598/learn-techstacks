# Section 05: Simulation Results & Analytics

## Overview

After simulation execution, detailed results capture the complete conversation transcript, per-step latency measurements, response accuracy metrics, and diff views against expected behavior. Results are stored for trend analysis, regression detection, and compliance auditing.

## Architecture

```
Simulation Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Simulation Engine] → [Results Processor] → [Storage]
                            │                       │
                     Transcript generation      PostgreSQL
                     Latency analysis           S3 (audio)
                     Accuracy scoring           Elasticsearch
                     Diff computation

[Results Dashboard]
       │
  ┌────┴────┐
  │         │
  Table   Detail
  View     View
  (list    (per-step
   of       breakdown,
   runs)    transcript,
            diffs)

Result Schema:
  SimulationResult {
    id: "sim_abc123"
    scenarioName: "Refund Request"
    status: "passed" | "failed" | "timed_out"
    startedAt: ISO timestamp
    completedAt: ISO timestamp
    durationMs: 3847
    transcript: "..."  // Full conversation text
    steps: [StepResult]
    accuracyScore: 0.95
    averageLatencyMs: 342
    audioRecordingUrl: "s3://..."
  }
```

## Design Decisions

- **Separate Result Storage**: Results stored independently from scenarios
- **Audio Recording Preservation**: Full audio recorded for compliance and debugging
- **Diff View Generation**: Side-by-side comparison of expected vs actual behavior
- **Trend Data Aggregation**: Results aggregated for pass rate and latency trends

## Implementation Approach

```typescript
// Result types
interface SimulationResult {
  id: string;
  scenarioName: string;
  scenarioVersion: string;
  suiteRunId?: string;
  status: 'passed' | 'failed' | 'timed_out';
  startedAt: Date;
  completedAt: Date;
  durationMs: number;
  transcript: string;
  steps: StepResultData[];
  accuracyScore: number;
  averageLatencyMs: number;
  maxLatencyMs: number;
  p95LatencyMs: number;
  audioRecordingUrl?: string;
  errorMessage?: string;
  metadata: Record<string, string>;
}

interface StepResultData {
  stepIndex: number;
  role: 'caller' | 'agent';
  callerInput?: string;
  agentResponse: string;
  expectedAgentResponse?: string;
  latencyMs: number;
  verificationResults: VerificationCheckResult[];
  status: 'passed' | 'failed' | 'timed_out';
  diff?: DiffResult;
}

interface DiffResult {
  expected: string;
  actual: string;
  additions: string[];   // Lines in actual but not expected
  deletions: string[];   // Lines in expected but not actual
  substitutions: Array<{ expected: string; actual: string }>;
  similarityScore: number;
}

// Results processor
class SimulationResultProcessor {
  async processResult(rawResult: RawSimulationResult): Promise<SimulationResult> {
    const transcript = this.generateTranscript(rawResult.steps);
    const accuracyScore = this.calculateAccuracy(rawResult.steps);
    const latencyMetrics = this.calculateLatencyMetrics(rawResult.steps);

    const enrichedSteps = await Promise.all(
      rawResult.steps.map(async (step) => ({
        ...step,
        diff: step.expectedAgentResponse
          ? this.computeDiff(step.expectedAgentResponse, step.agentResponse)
          : undefined,
      })),
    );

    return {
      id: rawResult.id,
      scenarioName: rawResult.scenarioName,
      scenarioVersion: rawResult.scenarioVersion,
      suiteRunId: rawResult.suiteRunId,
      status: rawResult.status,
      startedAt: rawResult.startedAt,
      completedAt: rawResult.completedAt,
      durationMs: rawResult.completedAt.getTime() - rawResult.startedAt.getTime(),
      transcript,
      steps: enrichedSteps,
      accuracyScore,
      averageLatencyMs: latencyMetrics.average,
      maxLatencyMs: latencyMetrics.max,
      p95LatencyMs: latencyMetrics.p95,
      audioRecordingUrl: rawResult.audioRecordingUrl,
      errorMessage: rawResult.errorMessage,
      metadata: rawResult.metadata,
    };
  }

  private calculateAccuracy(steps: StepResultData[]): number {
    const verificationSteps = steps.filter(s => s.verificationResults.length > 0);
    if (verificationSteps.length === 0) return 1.0;

    let totalChecks = 0;
    let passedChecks = 0;

    for (const step of verificationSteps) {
      for (const check of step.verificationResults) {
        totalChecks++;
        if (check.passed) passedChecks++;
      }
    }

    return totalChecks > 0 ? passedChecks / totalChecks : 1.0;
  }

  private calculateLatencyMetrics(steps: StepResultData[]): LatencyMetrics {
    const latencies = steps.map(s => s.latencyMs).filter(l => l > 0);
    const sorted = [...latencies].sort((a, b) => a - b);

    return {
      average: latencies.reduce((s, l) => s + l, 0) / latencies.length,
      max: Math.max(...latencies),
      p95: sorted[Math.floor(sorted.length * 0.95)],
      min: Math.min(...latencies),
    };
  }

  private computeDiff(expected: string, actual: string): DiffResult {
    const expectedLines = expected.split('\n');
    const actualLines = actual.split('\n');

    const expectedWords = new Set(expected.split(/\s+/));
    const actualWords = actual.split(/\s+/);
    const actualSet = new Set(actualWords);

    const additions = actualWords.filter(w => !expectedWords.has(w));
    const deletions = [...expectedWords].filter(w => !actualSet.has(w));

    // Similarity score based on word overlap
    const commonWords = actualWords.filter(w => expectedWords.has(w)).length;
    const totalWords = actualWords.length + expectedWords.size;
    const similarityScore = totalWords > 0
      ? (commonWords * 2) / totalWords
      : 1.0;

    return {
      expected,
      actual,
      additions: [...new Set(additions)],
      deletions: [...new Set(deletions)],
      substitutions: deletions.slice(0, 5).map((del, i) => ({
        expected: del,
        actual: additions[i] || '',
      })),
      similarityScore,
    };
  }

  private generateTranscript(steps: StepResultData[]): string {
    return steps
      .map(s => {
        if (s.role === 'caller') {
          return `[Caller (${s.stepIndex})]: ${s.callerInput || ''}`;
        }
        if (s.role === 'agent') {
          return `[Agent (${s.stepIndex})]: ${s.agentResponse}${s.expectedAgentResponse ? `\n  Expected: ${s.expectedAgentResponse}` : ''}`;
        }
        return '';
      })
      .filter(Boolean)
      .join('\n\n');
  }
}

// Trend analysis
class SimulationTrendAnalyzer {
  async getTrends(scenarioName: string, days = 30): Promise<TrendAnalysis> {
    const results = await this.db.find('simulation_results', {
      scenarioName,
      startedAt: { $gte: daysAgo(days) },
    }, { sort: { startedAt: 1 } });

    return {
      scenarioName,
      totalRuns: results.length,
      passRate: results.filter(r => r.status === 'passed').length / results.length,
      averageLatencyMs: results.reduce((s, r) => s + r.averageLatencyMs, 0) / results.length,
      latencyTrend: this.calculateTrend(results.map(r => r.averageLatencyMs)),
      accuracyTrend: this.calculateTrend(results.map(r => r.accuracyScore)),
      dailyResults: this.groupByDay(results),
    };
  }

  private calculateTrend(values: number[]): 'improving' | 'stable' | 'degrading' {
    if (values.length < 10) return 'stable';
    const recent = values.slice(-5);
    const earlier = values.slice(0, 5);
    const recentAvg = recent.reduce((s, v) => s + v, 0) / recent.length;
    const earlierAvg = earlier.reduce((s, v) => s + v, 0) / earlier.length;
    const diff = (recentAvg - earlierAvg) / earlierAvg;

    if (Math.abs(diff) < 0.05) return 'stable';
    return diff < 0 ? 'improving' : 'degrading';
  }
}
```

## Integration Points

- **Developer Portal**: Results dashboard with filterable views
- **CI/CD Pipeline**: Test results published to CI output and status checks
- **Notification System**: Significant pass rate drops trigger alerts

## Production Considerations

- **Audio Storage Retention**: Audio recordings retained for 90 days
- **Result Data Retention**: Result summaries retained indefinitely; detailed step data for 1 year
- **Trend Data Caching**: Aggregated trends cached for dashboard performance
- **Export Capability**: Results downloadable as JSON or CSV

## Open-Source Tools

- **Chart.js**: Trend visualization in dashboard
- **diff**: Text diff library for expected vs actual comparison
- **PapaParse**: CSV export for result data
