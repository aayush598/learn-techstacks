# Section 06: Quality Gates & Artifacts

## Overview

Quality gates are automated checkpoints that enforce minimum standards before code progresses through the pipeline. If a gate fails, the pipeline stops and the PR is blocked from merging. Gates cover code coverage, lint severity, type safety, bundle size budgets, and security vulnerabilities. Build artifacts are generated at each stage for downstream consumption.

## Quality Gate Architecture

```text
┌────────────────────────────────────────────────────────────┐
│                    Quality Gate Pipeline                     │
├────────────────────────────────────────────────────────────┤
│                                                              │
│  Gate 1: Lint Severity                                       │
│  ├── ESLint: 0 errors, warnings < package count × 5         │
│  └── Prettier: --check must pass                             │
│                                                              │
│  Gate 2: TypeScript                                           │
│  ├── tsc --noEmit: 0 errors                                  │
│  └── No `any` types allowed (strict mode)                     │
│                                                              │
│  Gate 3: Unit Test Coverage                                   │
│  ├── Lines: ≥ 80%                                            │
│  ├── Branches: ≥ 75%                                         │
│  └── Functions: ≥ 80%                                        │
│                                                              │
│  Gate 4: Build                                                │
│  ├── Bundled size (web): ≤ 500 KB initial (gzip)             │
│  ├── API bundle: ≤ 50 MB (uncompressed)                      │
│  └── No circular dependencies                                │
│                                                              │
│  Gate 5: Integration Test                                     │
│  ├── All passing, max 5% flaky retries                       │
│  └── Query count assertions (no N+1 in critical paths)       │
│                                                              │
│  Gate 6: E2E Tests                                            │
│  ├── Critical path: 100% pass                                │
│  └── Visual regression: ≤ 1% diff threshold                  │
│                                                              │
└────────────────────────────────────────────────────────────┘
```

## Code Coverage Enforcement

Coverage thresholds are defined in Vitest configuration and validated in CI:

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json-summary', 'lcov', 'junit'],
      thresholds: {
        lines: 80,
        branches: 75,
        functions: 80,
        statements: 80,
        perFile: true,
      },
      exclude: [
        '**/*.config.*',
        '**/*.d.ts',
        '**/node_modules/**',
        '**/dist/**',
      ],
    },
  },
});
```

The `perFile: true` setting is aggressive — every file must meet the threshold independently. This prevents a pattern where low-coverage files hide behind high-coverage files. The trade-off is that some files (error boundaries, fallback components) are inherently hard to test. These are added to an exclusion list with explicit justification.

```yaml
# CI check (in workflow)
- name: Coverage Gate
  run: |
    # Parse json-summary to get per-file coverage
    for file in packages/*/coverage/coverage-summary.json; do
      package=$(echo $file | cut -d/ -f2)
      lines=$(jq '.total.lines.pct' $file)
      if [ "$lines" -lt 80 ]; then
        echo "❌ $package: ${lines}% line coverage (below 80%)"
        exit 1
      fi
    done
```

## Bundle Size Budgeting

Bundle size regressions are caught using `size-limit` or a custom script:

```jsonc
// packages/web/package.json
{
  "size-limit": [
    {
      "name": "Main JS Bundle",
      "path": ".next/static/chunks/pages/**/*.js",
      "limit": "500 kB",
      "running": false,
      "gzip": true
    },
    {
      "name": "Vendor JS Bundle",
      "path": ".next/static/chunks/framework-*.js",
      "limit": "100 kB",
      "gzip": true
    },
    {
      "name": "CSS Bundle",
      "path": ".next/static/css/**/*.css",
      "limit": "50 kB",
      "gzip": true
    }
  ]
}
```

```yaml
- name: Check Bundle Size
  run: npx size-limit --json 2> /dev/null | jq '.[] | select(.passed == false)'

- name: Upload Size Report
  uses: actions/upload-artifact@v4
  with:
    name: bundle-size-report
    path: size-limit-report.json
```

Bundle size gates are particularly important for our voice agent platform because the WebSocket client and audio processing libraries are heavy. A 10 KB increase in the main bundle might seem small but can push initial load time past the 3-second threshold for voice applications.

## Build Artifacts

Artifacts are produced at each pipeline stage and passed to downstream jobs:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: npx turbo build

      - name: Upload Web Build
        uses: actions/upload-artifact@v4
        with:
          name: web-build
          path: apps/web/.next/
          retention-days: 7

      - name: Upload API Build
        uses: actions/upload-artifact@v4
        with:
          name: api-build
          path: apps/api/dist/
          retention-days: 7

      - name: Upload Docker Images
        run: |
          docker save voice-agent-api:latest | gzip > api-image.tar.gz
          docker save voice-agent-web:latest | gzip > web-image.tar.gz
      - uses: actions/upload-artifact@v4
        with:
          name: docker-images
          path: "*-image.tar.gz"
          retention-days: 3

  deploy:
    needs: [build]
    steps:
      - name: Download Docker Images
        uses: actions/download-artifact@v4
        with:
          name: docker-images
      - name: Load and Deploy
        run: |
          docker load < api-image.tar.gz
          docker load < web-image.tar.gz
          docker compose up -d
```

Artifact retention policies balance storage cost against debuggability:
- Build outputs: 7 days (long enough for post-deploy investigation)
- Docker images: 3 days (images are also in the registry)
- Test reports and screenshots: 30 days (useful for trend analysis)
- Coverage reports: 90 days (historical coverage tracking)

## Report Generation

After each gate, structured reports are produced and published to the PR:

```yaml
- name: Publish Test Results
  uses: dorny/test-reporter@v1
  if: always()
  with:
    name: "Test Results (${{ matrix.package }})"
    path: "reports/junit-*.xml"
    reporter: java-junit
    fail-on-error: true
    fail-on-flaky: false
```

```yaml
- name: Comment Coverage on PR
  uses: dorny/test-reporter@v1
  if: always()
  with:
    name: "Coverage Report"
    path: "packages/*/coverage/coverage-summary.json"
    reporter: java-json
```

The `fail-on-flaky: false` setting reports flaky tests but doesn't block the pipeline. This prevents spurious failures from blocking PRs while still tracking flakiness in a separate dashboard.

## Quality Gate Configuration

Gates are centralized in a configuration file rather than scattered across workflow YAML:

```yaml
# .github/config/quality-gates.yml
gates:
  lint:
    eslint_errors: 0
    eslint_warnings_max: 25
    prettier_check: required

  coverage:
    lines: 80
    branches: 75
    functions: 80
    per_file: true
    exclude_paths:
      - "**/*.stories.tsx"
      - "**/error-boundary.tsx"
      - "**/__mocks__/**"

  bundle_size:
    web_initial_gzip_kb: 500
    web_vendor_gzip_kb: 100
    api_uncompressed_mb: 50
    circular_deps_allowed: false

  security:
    audit_high: 0
    audit_critical: 0
    sast_errors: 0

  performance:
    lighthouse_score_min: 85
    api_p95_latency_ms: 500
    websocket_connect_ms: 200
```

This externalization means gate thresholds can be adjusted without modifying workflow files — a simple PR against the config file triggers a review of the standards themselves.

## Integration Points

- **GitHub Checks API**: Each quality gate reports as a separate check, visible in the PR's check suite
- **PR Comments**: Coverage changes and bundle size deltas are posted as PR comments by a bot
- **Dashboard**: Historical quality metrics are pushed to Datadog or Grafana for trend visualization
- **Slack Alerts**: Gate failures on main branch trigger alerts to the team channel

## Production Considerations

1. **Flaky test quarantine**: Tests that fail intermittently are automatically quarantined after 3 failures in 10 runs. Quarantined tests don't block CI but are reported separately for investigation.
2. **Gradual threshold enforcement**: New packages get a 30-day grace period at 60% coverage before the 80% threshold applies. This prevents blocking new code from landing while maintaining the standard.
3. **Artifact storage costs**: Monitor GitHub Actions artifact storage usage. Set retention days aggressively. Use external storage (S3) for long-term artifact archival.
4. **Gate bypass mechanism**: Emergency fixes can bypass gates with a `[skip gates]` commit message marker, but this is logged and audited weekly. Any bypass triggers an incident review.
5. **Differential comparison**: For bundle size and coverage, compare against the base branch, not an absolute threshold. A PR that increases bundle size by 5% should fail even if under the absolute limit.
