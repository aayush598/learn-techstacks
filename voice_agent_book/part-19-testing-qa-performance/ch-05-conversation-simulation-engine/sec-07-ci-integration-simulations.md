# Section 07: CI Integration for Simulations

## Overview

CI integration for conversation simulations ensures that agent behavior changes are validated before deployment. Simulations run automatically when agent configurations or voice pipeline components change, providing fast feedback on regressions. The CI pipeline executes a configurable suite of simulations, compares results against baselines, and reports pass/fail status.

Simulation CI is designed for speed: only simulations relevant to changed components are executed by default, with full regression suites running on main branch merges. Results are published as CI artifacts and posted to PRs for immediate visibility.

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

```yaml
# .github/workflows/simulations.yml
name: Conversation Simulations
on:
  pull_request:
    paths:
      - 'src/agents/**'
      - 'src/core/voice/**'
      - 'simulations/**'

jobs:
  simulation-smoke:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run build
      
      - name: Run critical simulations
        run: npx voice-sim run --tier=critical --parallel=4
        env:
          AGENT_API_URL: http://localhost:3000
      
      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: simulation-results-critical
          path: simulation-results/

  simulation-regression:
    needs: simulation-smoke
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run build
      
      - name: Run full regression suite
        run: npx voice-sim run --tier=regression --parallel=8
        env:
          AGENT_API_URL: http://localhost:3000
      
      - name: Compare with baseline
        run: npx voice-sim compare --baseline=main
      
      - name: Check thresholds
        run: npx voice-sim check-thresholds
      
      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: simulation-results-regression
          path: simulation-results/
      
      - name: Comment PR
        uses: actions/github-script@v7
        with:
          script: |
            const summary = require('./simulation-results/summary.json');
            github.rest.issues.createComment({
              ...context.repo,
              issue_number: context.issue.number,
              body: `## Simulation Results\n
              - **Pass rate:** ${summary.passRate}%
              - **Total simulations:** ${summary.total}
              - **Failed:** ${summary.failed}
              - **Regressions:** ${summary.regressions}
              [View detailed report](https://example.com/simulations/${summary.id})`,
            });
```

## Integration Points

- **GitHub Actions**: CI pipeline triggers on relevant file changes
- **PR Comments**: Results posted as PR comments with summary
- **Status Checks**: Simulation results as required status checks
- **Slack Notifications**: Failures notified to team channel
- **Dashboard**: Historical results displayed on quality dashboard

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **Pipeline Duration**: Full simulation suite can take 30+ minutes; optimize parallel execution
- **Cost**: Simulation API calls (LLM, STT) incur costs in cloud; use model caching
- **Environment Stability**: Simulation environment must be isolated from other tests
- **Result Consistency**: Baseline comparisons require consistent test environment
- **Threshold Tuning**: Initially set thresholds loosely; tighten as agent behavior stabilizes
