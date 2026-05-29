# Section 06: Coverage & Reporting

## Overview

Code coverage measurement provides visibility into which parts of the codebase are exercised by tests and which are not. Combined with threshold enforcement, coverage reports, and CI annotations, it helps maintain quality standards and identify untested code paths.

## Coverage Configuration

```typescript
// vitest.config.ts (coverage section)
export default defineConfig({
  test: {
    coverage: {
      // Coverage provider
      provider: "v8",

      // Report formats
      reporter: [
        "text",           // Console output
        "json",           // Machine-readable
        "html",           // Interactive HTML report
        "lcov",           // LCOV for IDE integration
        "clover",         // CI integration (Jenkins, etc.)
      ],
      reportsDirectory: "./coverage",

      // Files to include/exclude
      include: [
        "packages/*/src/**/*.ts",
        "packages/*/src/**/*.tsx",
        "apps/*/src/**/*.ts",
        "apps/*/src/**/*.tsx",
      ],
      exclude: [
        "**/node_modules/**",
        "**/dist/**",
        "**/coverage/**",
        "**/*.config.*",
        "**/*.d.ts",
        "**/types/**",
        "**/generated/**",
        "**/migrations/**",
        "**/*.test.*",
        "**/*.spec.*",
        "**/__tests__/**",
        "**/test/**",
        "**/mocks/**",
      ],

      // Per-directory thresholds
      thresholds: {
        // Global thresholds
        statements: 80,
        branches: 75,
        functions: 80,
        lines: 80,

        // Per-package thresholds (override global)
        perFile: true,
        overrides: {
          "packages/types/": {
            statements: 95,
            branches: 90,
            functions: 95,
            lines: 95,
          },
          "packages/config/": {
            statements: 90,
            branches: 85,
            functions: 90,
            lines: 90,
          },
          "packages/db/": {
            statements: 80,
            branches: 75,
            functions: 80,
            lines: 80,
          },
          "packages/voice/": {
            statements: 75,
            branches: 70,
            functions: 75,
            lines: 75,
          },
          "packages/ai/": {
            statements: 75,
            branches: 70,
            functions: 75,
            lines: 75,
          },
          "packages/ui/": {
            statements: 80,
            branches: 75,
            functions: 80,
            lines: 80,
          },
          "apps/web/": {
            statements: 60,
            branches: 55,
            functions: 60,
            lines: 60,
          },
          "apps/api/": {
            statements: 65,
            branches: 60,
            functions: 65,
            lines: 65,
          },
        },
      },

      // Watermarks for HTML report coloring
      watermarks: {
        statements: [70, 90],
        branches: [65, 85],
        functions: [70, 90],
        lines: [70, 90],
      },
    },
  },
});
```

## Running Coverage

```bash
# Run all tests with coverage
pnpm test -- --coverage

# Run coverage for specific package
pnpm --filter @voice-agent/db test -- --coverage

# Generate only HTML report (skip text output)
pnpm test -- --coverage --reporter=html

# Run coverage with specific thresholds
COVERAGE_THRESHOLDS=true pnpm test -- --coverage
```

## CI Coverage Enforcement

```yaml
# .github/workflows/coverage.yml
name: Coverage
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  coverage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Run tests with coverage
        run: pnpm test -- --coverage
        env:
          NODE_ENV: test

      - name: Check coverage thresholds
        run: |
          # Parse coverage summary
          COVERAGE_FILE="./coverage/coverage-summary.json"
          if [ -f "$COVERAGE_FILE" ]; then
            LINES=$(jq '.total.lines.pct' "$COVERAGE_FILE")
            STATEMENTS=$(jq '.total.statements.pct' "$COVERAGE_FILE")
            FUNCTIONS=$(jq '.total.functions.pct' "$COVERAGE_FILE")
            BRANCHES=$(jq '.total.branches.pct' "$COVERAGE_FILE")

            echo "Coverage Summary:"
            echo "  Lines: ${LINES}%"
            echo "  Statements: ${STATEMENTS}%"
            echo "  Functions: ${FUNCTIONS}%"
            echo "  Branches: ${BRANCHES}%"

            # Fail if below thresholds
            FAIL=false
            if (( $(echo "$LINES < 80" | bc -l) )); then
              echo "::error::Lines coverage (${LINES}%) is below threshold (80%)"
              FAIL=true
            fi
            if (( $(echo "$STATEMENTS < 80" | bc -l) )); then
              echo "::error::Statements coverage (${STATEMENTS}%) is below threshold (80%)"
              FAIL=true
            fi
            if (( $(echo "$FUNCTIONS < 80" | bc -l) )); then
              echo "::error::Functions coverage (${FUNCTIONS}%) is below threshold (80%)"
              FAIL=true
            fi
            if (( $(echo "$BRANCHES < 75" | bc -l) )); then
              echo "::error::Branches coverage (${BRANCHES}%) is below threshold (75%)"
              FAIL=true
            fi

            if [ "$FAIL" = true ]; then
              exit 1
            fi
          fi

      - name: Upload coverage report
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage/
          retention-days: 30

      - name: Comment PR with coverage
        if: github.event_name == 'pull_request'
        uses: davelosert/vitest-coverage-report-action@v2
        with:
          json-summary-path: ./coverage/coverage-summary.json
          json-final-path: ./coverage/coverage-final.json
```

## Coverage Report Visualization

```typescript
// scripts/coverage-report.ts
// Custom script to generate a Markdown coverage report
import { readFileSync, writeFileSync } from "fs";

interface CoverageSummary {
  total: MetricSummary;
  [filePath: string]: MetricSummary;
}

interface MetricSummary {
  lines: { pct: number };
  statements: { pct: number };
  functions: { pct: number };
  branches: { pct: number };
}

function generateReport(): void {
  const summary: CoverageSummary = JSON.parse(
    readFileSync("./coverage/coverage-summary.json", "utf-8"),
  );

  let markdown = "# Coverage Report\n\n";
  markdown += "| File | Lines | Statements | Functions | Branches |\n";
  markdown += "|------|-------|------------|-----------|----------|\n";

  for (const [file, metrics] of Object.entries(summary)) {
    if (file === "total") continue;
    markdown += `| ${file} | ${metrics.lines.pct}% | ${metrics.statements.pct}% | ${metrics.functions.pct}% | ${metrics.branches.pct}% |\n`;
  }

  markdown += `\n**Total:** Lines ${summary.total.lines.pct}%, Statements ${summary.total.statements.pct}%, Functions ${summary.total.functions.pct}%, Branches ${summary.total.branches.pct}%\n`;

  writeFileSync("./coverage/coverage-report.md", markdown);
  console.log("Coverage report generated: coverage/coverage-report.md");
}

generateReport();
```

## Uncovered Code Detection

```typescript
// scripts/find-uncovered.ts
// Find functions/modules with zero test coverage
import { readFileSync, readdirSync, statSync } from "fs";
import { join } from "path";

interface UncoveredModule {
  file: string;
  lines: number;
  functions: Array<{ name: string; line: number }>;
}

function findUncoveredModules(coverageDir: string): UncoveredModule[] {
  const uncovered: UncoveredModule[] = [];
  const coverageData = JSON.parse(
    readFileSync(join(coverageDir, "coverage-final.json"), "utf-8"),
  );

  for (const [filePath, data] of Object.entries(coverageData)) {
    const fileData = data as {
      s: Record<string, number>;
      f: Record<string, number>;
      b: Record<string, number[]>;
      path: string;
    };

    // Check if file has any coverage at all
    const isUncovered = Object.values(fileData.s).every((c) => c === 0);

    if (isUncovered) {
      uncovered.push({
        file: fileData.path,
        lines: Object.keys(fileData.s).length,
        functions: [],
      });
    }
  }

  return uncovered.sort((a, b) => b.lines - a.lines);
}

const uncovered = findUncoveredModules("./coverage");
console.log(`\nFound ${uncovered.length} uncovered modules:`);
uncovered.slice(0, 20).forEach((m) => {
  console.log(`  ${m.file} (${m.lines} lines)`);
});
```

## Coverage Badges

```yaml
# .github/workflows/coverage-badge.yml
name: Update Coverage Badge
on:
  push:
    branches: [main]

jobs:
  badge:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4

      - name: Run tests with coverage
        run: pnpm test -- --coverage

      - name: Generate badge
        uses: schneegans/dynamic-badges-action@v1
        with:
          auth: ${{ secrets.GIST_SECRET }}
          gistID: your-gist-id
          filename: coverage.json
          label: coverage
          message: ${{ steps.coverage.outputs.lines }}%
          color: green
```

## Design Decisions

### v8 vs. istanbul provider

**Decision**: Use v8 provider (default in Vitest).

**Rationale**: The v8 provider is faster (native V8 coverage) and produces more accurate results. Istanbul (via c8) is a fallback for environments where v8 coverage isn't available.

### Per-file thresholds

Different packages have different coverage expectations:
- **Types package**: 95% (pure logic, no external deps)
- **Database package**: 80% (complex queries are hard to cover fully)
- **UI package**: 80% (visual components are covered by E2E)
- **Apps**: 60% (integration points are harder to unit test)

Lower thresholds for apps reflects the reality that E2E tests provide most coverage for application-level code.

## Integration Points

- **CI**: Coverage thresholds block PRs with insufficient coverage
- **PR comments**: Coverage report is posted on every PR
- **Badges**: Repository README shows current coverage
- **IDE**: LCOV files enable inline coverage display in VS Code

## Production Considerations

1. **Coverage inflation**: High coverage doesn't guarantee test quality. Review test assertions alongside coverage numbers. A test that calls a function without asserting anything provides 100% coverage but zero confidence
2. **Branch coverage**: Focus on branch coverage, which reveals untested conditional paths. A function with 100% line coverage but 50% branch coverage has untested edge cases
3. **Excluded files**: Keep the exclusion list minimal. Excluding files from coverage makes them invisible — they could rot without anyone noticing
4. **Trend analysis**: Track coverage over time. A decreasing trend is a warning sign, even if absolute numbers are above threshold
5. **PR-level reporting**: Individual PRs should show coverage diff (change from base branch), not just absolute coverage. This prevents "coverage debt" from accumulating
