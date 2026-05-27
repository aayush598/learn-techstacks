# Section 01: Regression Testing Architecture

## Overview

Regression testing for conversation flows automatically detects when agent behavior changes unexpectedly. The regression suite consists of a curated set of conversation scenarios that represent core agent capabilities. Each scenario is simulated before and after changes, and results are compared to detect behavioral differences.

The regression architecture is built around baseline management: a set of known-good simulation results stored with each agent version. When code changes are proposed, simulations are run against the modified system and compared to baselines. Significant deviations indicate regressions that must be reviewed before deployment.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Canvas   |--->| Node     |--->| Edge     |--->| Validator|--->| Serializ |
| (React   |    | Registry |    | Router   |    | (cycle   |    | ation    |
|  Flow)   |    | (types)  |    | (condit) |    |  detect) |    | (JSON)   |
+----------+    +----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **React Flow over Custom**: Battle-tested node/edge rendering. Saves 6+ months custom development.
- **Local-First State**: Zustand + debounced saves (2s). Instant UI response without waiting for API.
- **Function-as-Edge**: Edges carry conditions and transforms. Flow evaluates conditions at each step.
## Implementation Approach

```typescript
class RegressionTestSystem {
  async runRegression(agentId: string, version: string): Promise<RegressionReport> {
    // Load baseline for previous version
    const baseline = await this.baselineManager.load(agentId, version);
    
    // Run current simulation suite
    const current = await this.suiteRunner.runAll(agentId);
    
    // Compare results
    const diffs = this.diffEngine.compare(baseline, current);
    
    // Classify regressions
    const regressions = diffs.filter(d => d.significance > this.config.threshold);
    
    // Report results
    return {
      baselineId: baseline.id,
      currentId: current.id,
      totalTests: current.results.length,
      passed: current.results.filter(r => r.passed).length,
      regressions: regressions.length,
      improvements: diffs.filter(d => d.significance < -this.config.threshold).length,
      breakingChanges: regressions.filter(r => r.severity === 'high'),
      details: regressions,
    };
  }
}
```

## Integration Points

- **CI/CD Pipeline**: Regression suite runs before deployment
- **Agent Configuration**: Test suite defined per agent configuration
- **Version Control**: Baselines stored in git
- **Alert System**: Regressions trigger Slack/PagerDuty alerts
- **Dashboard**: Regression trends displayed on quality dashboard
