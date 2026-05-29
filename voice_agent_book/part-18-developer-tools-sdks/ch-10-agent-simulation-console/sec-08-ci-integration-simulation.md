# Section 08: CI Integration for Simulation

## Overview

Simulation tests integrate into CI/CD pipelines via GitHub Actions and similar tools. Automated test runs execute on pull requests, nightly builds, and release candidates. Quality gates enforce pass rate thresholds, and regression detection alerts teams when agent performance degrades.

## Architecture

```
CI/CD Integration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[GitHub PR] → [CI Pipeline] → [Simulation Tests] → [Quality Gate]
    │              │                   │                   │
  Push or      GitHub Actions       Execute test       Check pass
  PR open      workflow             suites             rate ≥ 95%
                                                                  │
                                                      ┌───────────┴──────────┐
                                                      │                      │
                                                  [PASS] ✅              [FAIL] ❌
                                                  Merge allowed         Block merge
                                                  No regression         Regression alert
                                                                        Created ticket

GitHub Actions Workflow:
  .github/workflows/simulation-tests.yml
  ┌─────────────────────────────────────────────┐
  │ name: Simulation Tests                       │
  │ on:                                          │
  │   pull_request:                              │
  │     paths: ['agent/**', 'scenarios/**']      │
  │   schedule:                                  │
  │     - cron: '0 2 * * *'  # Nightly          │
  │                                              │
  │ jobs:                                        │
  │   smoke-tests:                               │
  │     runs-on: ubuntu-latest                   │
  │     steps:                                   │
  │       - uses: actions/checkout@v4            │
  │       - uses: voiceagent/sim-action@v1       │
  │         with:                                │
  │           suite: smoke                       │
  │           api-key: ${{ secrets.SIM_API_KEY }}│
  │           threshold: 90                      │
  └─────────────────────────────────────────────┘
```

## Design Decisions

- **GitHub Action Custom Action**: Reusable action for simulation test execution
- **Path-Based Triggers**: Tests run only when agent or scenario files change
- **Check Run Results**: Test results published as GitHub check runs
- **Parallel Suites**: Smoke, regression, and load test suites run in parallel

## Implementation Approach

```typescript
// GitHub Action entry point
// action.yml
const core = require('@actions/core');
const github = require('@actions/github');

interface SimulationActionInputs {
  suite: string;
  apiKey: string;
  threshold: number;
  scenarioFilter?: string;
}

async function runSimulationAction() {
  const inputs: SimulationActionInputs = {
    suite: core.getInput('suite'),
    apiKey: core.getInput('api-key'),
    threshold: Number(core.getInput('threshold')),
    scenarioFilter: core.getInput('scenario-filter'),
  };

  const octokit = github.getOctokit(inputs.apiKey);

  // Create check run
  const checkRun = await octokit.rest.checks.create({
    owner: github.context.repo.owner,
    repo: github.context.repo.repo,
    name: `Simulation: ${inputs.suite}`,
    head_sha: github.context.sha,
    status: 'in_progress',
  });

  try {
    const simulationClient = new SimulationClient({
      baseUrl: process.env.SIMULATION_API_URL || 'https://api.voiceagent.com/v1/simulate',
      apiKey: inputs.apiKey,
    });

    // Load and execute suite
    const suite = await simulationClient.loadSuite(inputs.suite);
    const result = await simulationClient.executeSuite(suite, {
      scenarioFilter: inputs.scenarioFilter,
    });

    // Determine pass/fail status
    const passRate = result.passedScenarios / result.totalScenarios;
    const thresholdMet = passRate >= (inputs.threshold / 100);

    const conclusion = thresholdMet ? 'success' : 'failure';
    const summaryLines = [
      `## Simulation Test Results: ${inputs.suite}`,
      '',
      `| Metric | Value |`,
      `|---|---|`,
      `| Total Scenarios | ${result.totalScenarios} |`,
      `| Passed | ${result.passedScenarios} |`,
      `| Failed | ${result.failedScenarios} |`,
      `| Pass Rate | ${(passRate * 100).toFixed(1)}% |`,
      `| Threshold | ${inputs.threshold}% |`,
      `| Threshold Met | ${thresholdMet ? '✅' : '❌'} |`,
      `| Duration | ${result.durationMs}ms |`,
      '',
    ];

    // Add failed scenarios
    if (result.failedScenarios > 0) {
      summaryLines.push('### Failed Scenarios', '');
      for (const failed of result.failedResults) {
        summaryLines.push(`- **${failed.scenarioName}**: ${failed.failureReason}`);
      }
      summaryLines.push('');
    }

    // Update check run
    await octokit.rest.checks.update({
      owner: github.context.repo.owner,
      repo: github.context.repo.repo,
      check_run_id: checkRun.data.id,
      status: 'completed',
      conclusion,
      completed_at: new Date().toISOString(),
      output: {
        title: `Simulation: ${inputs.suite} — ${thresholdMet ? 'Passed' : 'Failed'}`,
        summary: summaryLines.join('\n'),
      },
    });

    if (!thresholdMet) {
      core.setFailed(`Pass rate ${(passRate * 100).toFixed(1)}% below threshold ${inputs.threshold}%`);
    }
  } catch (error) {
    await octokit.rest.checks.update({
      owner: github.context.repo.owner,
      repo: github.context.repo.repo,
      check_run_id: checkRun.data.id,
      status: 'completed',
      conclusion: 'failure',
      output: {
        title: `Simulation: ${inputs.suite} — Error`,
        summary: `Error running simulation suite: ${error}`,
      },
    });
    core.setFailed(error);
  }
}

// CI/CD integration SDK
class SimulationClient {
  private baseUrl: string;
  private apiKey: string;

  constructor(config: { baseUrl: string; apiKey: string }) {
    this.baseUrl = config.baseUrl;
    this.apiKey = config.apiKey;
  }

  async loadSuite(suiteName: string): Promise<TestSuite> {
    const response = await fetch(`${this.baseUrl}/suites/${suiteName}`, {
      headers: { Authorization: `Bearer ${this.apiKey}` },
    });
    return response.json();
  }

  async executeSuite(
    suite: TestSuite,
    options?: { scenarioFilter?: string },
  ): Promise<SuiteResult> {
    const response = await fetch(`${this.baseUrl}/execute`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        suite: suite.name,
        scenarioFilter: options?.scenarioFilter,
      }),
    });

    // Poll for completion
    const executionId = (await response.json()).id;
    return this.pollExecution(executionId);
  }

  private async pollExecution(executionId: string): Promise<SuiteResult> {
    const maxAttempts = 60; // 5 minutes
    for (let i = 0; i < maxAttempts; i++) {
      const response = await fetch(`${this.baseUrl}/executions/${executionId}`, {
        headers: { Authorization: `Bearer ${this.apiKey}` },
      });
      const result = await response.json();

      if (result.status !== 'running') {
        return result;
      }

      await delay(5000);
    }

    throw new Error('Execution timed out');
  }
}

// Regression detection in CI
class RegressionDetector {
  async checkForRegressions(suiteName: string): Promise<RegressionReport> {
    const historicalResults = await this.getHistoricalResults(suiteName, 30);
    const currentResult = await this.getLatestResult(suiteName);

    if (historicalResults.length < 5) {
      return { hasRegression: false, message: 'Insufficient historical data' };
    }

    const avgPassRate = historicalResults
      .slice(0, 10)
      .reduce((s, r) => s + r.passRate, 0) / 10;

    const currentPassRate = currentResult.passRate;
    const regression = currentPassRate < avgPassRate - 0.1; // 10% drop

    if (regression) {
      const report: RegressionReport = {
        hasRegression: true,
        suiteName,
        previousAverageRate: avgPassRate,
        currentRate: currentPassRate,
        drop: avgPassRate - currentPassRate,
        failingScenarios: currentResult.failedResults.map(r => r.scenarioName),
        recommendedAction: 'Block merge and investigate agent changes',
      };

      // Create GitHub issue for regression
      await this.createRegressionIssue(report);

      return report;
    }

    return { hasRegression: false };
  }
}
```

## Integration Points

- **GitHub Checks API**: Results published as check runs on each PR
- **Slack Notifications**: Regression alerts sent to team channel
- **Jira Integration**: Automatic ticket creation for regression bugs
- **Dashboard API**: Test results pushed to developer portal dashboard

## Production Considerations

- **Execution Time Limits**: CI jobs timeout after 30 minutes
- **Cost Allocation**: CI simulation usage billed to development team
- **Parallel Execution**: Multiple suites run in parallel across CI matrix
- **Secrets Management**: API keys stored as GitHub Actions secrets

## Open-Source Tools

- **GitHub Actions**: CI/CD workflow runner
- **@actions/core**: GitHub Actions toolkit
- **Octokit**: GitHub API client for check runs and PR status
