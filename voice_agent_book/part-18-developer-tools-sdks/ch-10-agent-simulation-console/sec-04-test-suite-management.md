# Section 04: Test Suite Management

## Overview

Test suite management organizes simulation scenarios into test suites for batch execution, scheduling, and reporting. Suites can be grouped by feature, tagged for different testing phases (smoke, regression, integration), and executed on demand or on schedule. Results include pass/fail reporting, trend analysis, and regression detection.

## Architecture

```
Test Suite Management
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Scenario Library] → [Test Suite] → [Execution Engine] → [Results]
       │                  │               │                  │
  Individual          Group of        Queue-based       Pass/fail
  scenarios          scenarios       execution          reports
       │                  │          with timing        trends
  scenario-01.yaml   regression/       limits          diffs
  scenario-02.yaml   smoke/                         regression
  scenario-03.yaml   integration/                      alerts
                     nightly/

Test Suite Structure:
  suites/
  ├── regression.yaml
  │   ├── name: "Regression Suite"
  │   ├── tags: ["regression", "full"]
  │   ├── schedule: "0 2 * * *"  # Daily at 2 AM
  │   ├── timeout: 3600  # 1 hour
  │   └── scenarios:
  │       - path: "../scenarios/refund-request.yaml"
  │       - path: "../scenarios/order-inquiry.yaml"
  │       - path: "../scenarios/account-update.yaml"
  │       - path: "../scenarios/technical-support.yaml"
  │
  ├── smoke.yaml
  │   ├── name: "Smoke Test Suite"
  │   ├── tags: ["smoke", "quick"]
  │   ├── schedule: null  # Manual only
  │   └── scenarios:
  │       - path: "../scenarios/basic-greeting.yaml"
  │       - path: "../scenarios/faq-response.yaml"
  │
  └── nightly.yaml
      ├── name: "Nightly Build Suite"
      ├── tags: ["nightly", "full"]
      ├── schedule: "0 0 * * *"  # Midnight
      └── scenarios:
          - path: "../scenarios/*.yaml"  # Glob pattern
```

## Design Decisions

- **Glob-Based Selection**: Suites can reference scenarios via globs
- **Scheduled Execution**: Cron-based scheduling for automated runs
- **Parallel Execution**: Independent scenarios run in parallel
- **Quality Gates**: Fail suites if pass rate below threshold

## Implementation Approach

```typescript
// Test suite types
interface TestSuite {
  name: string;
  description?: string;
  tags: string[];
  schedule?: string; // Cron expression
  timeout: number; // Seconds
  scenarios: SuiteScenarioRef[];
  qualityGate?: {
    minPassRate: number; // 0.0 - 1.0
    maxFailureCount: number;
  };
  parallel?: boolean;
  maxConcurrency?: number;
}

interface SuiteScenarioRef {
  path: string; // File path or glob
  parameters?: Record<string, string>; // Override variables
}

interface SuiteExecution {
  id: string;
  suiteName: string;
  startedAt: Date;
  completedAt?: Date;
  status: 'running' | 'completed' | 'failed' | 'timed_out';
  scenarioResults: ScenarioResultSummary[];
  totalPassed: number;
  totalFailed: number;
  passRate: number;
  durationMs: number;
}

interface ScenarioResultSummary {
  scenarioName: string;
  status: 'passed' | 'failed' | 'timed_out';
  durationMs: number;
  failureReason?: string;
  runId: string;
}

// Test suite manager
class TestSuiteManager {
  private engine: SimulationEngine;
  private jobQueue: BullQueue;

  async loadSuite(suitePath: string): Promise<TestSuite> {
    const content = fs.readFileSync(suitePath, 'utf-8');
    return yaml.parse(content) as TestSuite;
  }

  async executeSuite(suite: TestSuite): Promise<SuiteExecution> {
    const execution: SuiteExecution = {
      id: crypto.randomUUID(),
      suiteName: suite.name,
      startedAt: new Date(),
      status: 'running',
      scenarioResults: [],
      totalPassed: 0,
      totalFailed: 0,
      passRate: 0,
      durationMs: 0,
    };

    const scenarios = await this.resolveScenarios(suite.scenarios);

    if (suite.parallel) {
      const results = await this.executeInParallel(scenarios, suite.maxConcurrency || 5);
      execution.scenarioResults = results;
    } else {
      for (const scenario of scenarios) {
        const result = await this.executeScenario(scenario);
        execution.scenarioResults.push(result);
      }
    }

    execution.completedAt = new Date();
    execution.durationMs = execution.completedAt.getTime() - execution.startedAt.getTime();
    execution.totalPassed = execution.scenarioResults.filter(r => r.status === 'passed').length;
    execution.totalFailed = execution.scenarioResults.filter(r => r.status === 'failed').length;
    execution.passRate = execution.totalPassed / execution.scenarioResults.length;

    // Check quality gate
    if (suite.qualityGate) {
      if (execution.passRate < suite.qualityGate.minPassRate) {
        execution.status = 'failed';
        await this.triggerQualityGateAlert(suite, execution);
      } else {
        execution.status = 'completed';
      }
    } else {
      execution.status = execution.totalFailed === 0 ? 'completed' : 'failed';
    }

    await this.storeExecutionResult(execution);
    return execution;
  }

  private async executeInParallel(
    scenarios: Scenario[],
    maxConcurrency: number,
  ): Promise<ScenarioResultSummary[]> {
    const results: ScenarioResultSummary[] = [];

    // Process in batches of maxConcurrency
    for (let i = 0; i < scenarios.length; i += maxConcurrency) {
      const batch = scenarios.slice(i, i + maxConcurrency);
      const batchResults = await Promise.all(
        batch.map(scenario => this.executeScenario(scenario))
      );
      results.push(...batchResults);
    }

    return results;
  }

  private async executeScenario(scenario: Scenario): Promise<ScenarioResultSummary> {
    const start = performance.now();

    try {
      const result = await this.engine.runScenario(scenario);

      return {
        scenarioName: scenario.name,
        status: result.failedSteps === 0 ? 'passed' : 'failed',
        durationMs: performance.now() - start,
        failureReason: result.failedSteps > 0
          ? `${result.failedSteps} step(s) failed`
          : undefined,
        runId: crypto.randomUUID(),
      };
    } catch (error) {
      return {
        scenarioName: scenario.name,
        status: 'failed',
        durationMs: performance.now() - start,
        failureReason: error instanceof Error ? error.message : 'Unknown error',
        runId: crypto.randomUUID(),
      };
    }
  }

  private async resolveScenarios(refs: SuiteScenarioRef[]): Promise<Scenario[]> {
    const scenarios: Scenario[] = [];

    for (const ref of refs) {
      if (ref.path.includes('*')) {
        // Glob pattern
        const files = await glob(ref.path);
        for (const file of files) {
          const scenario = await this.loadScenario(file);
          if (ref.parameters) {
            scenario.variables = { ...scenario.variables, ...ref.parameters };
          }
          scenarios.push(scenario);
        }
      } else {
        const scenario = await this.loadScenario(ref.path);
        if (ref.parameters) {
          scenario.variables = { ...scenario.variables, ...ref.parameters };
        }
        scenarios.push(scenario);
      }
    }

    return scenarios;
  }

  async scheduleSuite(suite: TestSuite): Promise<void> {
    if (!suite.schedule) return;

    await this.jobQueue.add(
      { type: 'suite', suite },
      {
        repeat: { cron: suite.schedule },
        removeOnComplete: true,
      },
    );
  }

  async getExecutionHistory(suiteName: string, limit = 20): Promise<SuiteExecution[]> {
    return this.db.find('suite_executions', { suiteName }, {
      sort: { startedAt: -1 },
      limit,
    });
  }

  async getTrendData(suiteName: string): Promise<TrendData> {
    const recent = await this.getExecutionHistory(suiteName, 30);

    return {
      suiteName,
      recentRuns: recent.map(r => ({
        date: r.startedAt,
        passRate: r.passRate,
        durationMs: r.durationMs,
      })),
      averagePassRate: recent.reduce((sum, r) => sum + r.passRate, 0) / recent.length,
      regressionDetected: this.detectRegression(recent),
    };
  }

  private detectRegression(executions: SuiteExecution[]): boolean {
    if (executions.length < 5) return false;
    const lastThree = executions.slice(0, 3);
    const previous = executions.slice(3, 8);
    const avgRecent = lastThree.reduce((s, e) => s + e.passRate, 0) / lastThree.length;
    const avgPrev = previous.reduce((s, e) => s + e.passRate, 0) / previous.length;
    return avgRecent < avgPrev - 0.1; // 10% drop
  }
}
```

## Integration Points

- **CI/CD Pipeline**: Suites triggered by GitHub Actions or scheduled cron
- **Developer Portal**: Test suite dashboard with pass/fail visualization
- **Alert System**: Quality gate failures trigger team notifications

## Production Considerations

- **Suite Execution Time**: Maximum 2-hour suite timeout
- **Cost Budgeting**: Parallel execution costs tracked per suite
- **Trend Analysis**: Pass rate trends visualized in dashboard
- **Regression Alerts**: Automatic alerts when pass rate drops significantly

## Open-Source Tools

- **BullMQ**: Job queue for suite execution and scheduling
- **node-cron**: Cron expression parsing for scheduled suites
- **glob**: Glob pattern matching for scenario selection
