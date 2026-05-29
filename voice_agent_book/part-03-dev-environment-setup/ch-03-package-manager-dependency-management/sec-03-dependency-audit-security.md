# Section 03: Dependency Audit & Security

## Overview

Dependency security is critical for a voice agent platform that processes sensitive audio data and PII. This section covers pnpm audit, Snyk/Trivy scanning, dependency review in CI, and CVE monitoring to ensure the supply chain remains secure.

## Security Threat Model

```text
┌─────────────────────────────────────────────────────────────┐
│              Dependency Security Threat Model                 │
│                                                              │
│  Attack Vector                Impact                         │
│  ─────────────────────────────────────────────────────       │
│  Compromised npm package     Remote code execution           │
│  Typosquatting               Credential theft                │
│  Dependency confusion        Data exfiltration               │
│  Malicious patch update      Backdoor in production          │
│  Transitive dep vulnerability Indirect exploit               │
│  Supply chain attack          Full system compromise         │
│                                                              │
│  Attack Surface: 500+ direct + transitive deps               │
└─────────────────────────────────────────────────────────────┘
```

## pnpm Audit

```bash
# Run security audit
pnpm audit

# Audit with severity filtering
pnpm audit --audit-level=high

# Audit in CI — fail on high/critical
pnpm audit --audit-level=high || exit 1

# Produce JSON output for analysis
pnpm audit --json > audit-report.json
```

### Audit Configuration in CI

```yaml
# .github/workflows/security-audit.yml
name: Security Audit
on:
  schedule:
    - cron: '0 6 * * *'     # Daily at 6 AM
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  audit:
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

      - name: Run pnpm audit
        run: |
          pnpm audit --audit-level=high --json > audit.json || true
          # Check for critical vulnerabilities
          if jq -e '.vulnerabilities.critical > 0' audit.json > /dev/null 2>&1; then
            echo "::error::Critical vulnerabilities found!"
            jq '.vulnerabilities' audit.json
            exit 1
          fi

      - name: Upload audit report
        uses: actions/upload-artifact@v4
        with:
          name: audit-report
          path: audit.json
```

## Snyk Integration

```yaml
# .github/workflows/snyk-scan.yml
name: Snyk Security Scan
on:
  schedule:
    - cron: '0 6 * * 1'   # Weekly on Monday
  push:
    branches: [main]

jobs:
  snyk:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Snyk to check for vulnerabilities
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: >
            --severity-threshold=high
            --fail-on=all
            --json-file-output=snyk-report.json
```

## Trivy Scanning

Trivy scans not just npm packages but also Docker images, filesystem, and IaC:

```bash
# Install Trivy
brew install trivy
# or
docker pull aquasec/trivy

# Scan npm dependencies
trivy fs --scanners vuln .

# Scan with severity filtering
trivy fs --scanners vuln --severity CRITICAL,HIGH .

# Generate SARIF output for GitHub
trivy fs --format sarif --output trivy-results.sarif .
```

```yaml
# .github/workflows/trivy-scan.yml
name: Trivy Scan
on:
  push:
    branches: [main]
  pull_request:

jobs:
  trivy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'

      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'
```

## Dependency Review in CI

GitHub's Dependency Review action blocks PRs that introduce vulnerabilities:

```yaml
# .github/workflows/dependency-review.yml
name: Dependency Review
on:
  pull_request:
    branches: [main]

permissions:
  contents: read
  pull-requests: write

jobs:
  dependency-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Dependency Review
        uses: actions/dependency-review-action@v4
        with:
          fail-on-severity: high
          comment-summary-in-pr: true
          allow-licenses: |
            MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause,
            ISC, 0BSD, Unlicense
          deny-licenses: GPL-3.0, AGPL-3.0
```

## CVE Monitoring

```yaml
# .github/workflows/cve-monitor.yml
name: CVE Monitoring
on:
  schedule:
    - cron: '0 */6 * * *'   # Every 6 hours

jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Check for npm advisories
        run: |
          # Fetch recent npm advisories
          curl -s "https://registry.npmjs.org/-/npm/v1/advisories?limit=20" \
            | jq -r '.[] | select(.severity == "critical" or .severity == "high") | .title'
```

## Package Allowlisting

Maintain an allowlist of approved packages and versions to prevent dependency confusion attacks:

```yaml
# .github/package-allowlist.yaml
allowed_packages:
  # Runtime dependencies
  - name: next
    allowed_versions: ">=14.0.0 <15.0.0"
    source: npm
  - name: react
    allowed_versions: ">=18.0.0 <19.0.0"
    source: npm
  - name: zod
    allowed_versions: ">=3.20.0 <4.0.0"
    source: npm

  # Scoped packages
  - name: "@voice-agent/*"
    allowed_versions: ">=0.0.0"
    source: workspace

  # Database
  - name: "@prisma/client"
    allowed_versions: ">=5.0.0 <6.0.0"
    source: npm

blocked_packages:
  - name: left-pad
  - name: faker
  - name: colors
```

## Security Best Practices

### .npmrc Security Configuration

```ini
# .npmrc
# Enforce engine requirements
engine-strict=true

# Disable package scripts during CI
ignore-scripts=false  # Keep true locally, audit scripts

# Verify integrity
verify-store-integrity=true

# Enable audit
audit=true
audit-level=high
```

### package.json Security Settings

```jsonc
{
  "scripts": {
    "preinstall": "npx only-allow pnpm",
    "postinstall": "pnpm audit --audit-level=high"
  }
}
```

## Dependency Review Process

```text
┌─────────────────────────────────────────────────────────────┐
│              Dependency Review Process                       │
│                                                              │
│  New Dependency Suggestion                                  │
│       │                                                      │
│       ▼                                                      │
│  1. Business justification required                         │
│  2. Security scan (pnpm audit + Snyk)                       │
│  3. License compatibility check                             │
│  4. Bundle size impact assessment                           │
│  5. Maintenance activity review (recent commits?)           │
│  6. Alternative evaluation                                  │
│       │                                                      │
│       ▼                                                      │
│  ┌────────────┐      ┌──────────────┐                      │
│  │ Approved    │      │  Rejected     │                      │
│  │ Add to      │      │  Document     │                      │
│  │ allowlist   │      │  rationale    │                      │
│  └────────────┘      └──────────────┘                      │
└─────────────────────────────────────────────────────────────┘
```

## Design Decisions

### pnpm audit vs. Snyk vs. Trivy

| Tool | Scope | CI Integration | False Positives | Cost |
|------|-------|---------------|----------------|------|
| pnpm audit | npm only | Native | Low | Free |
| Snyk | Multi-language | Excellent | Medium | Freemium |
| Trivy | All artifacts | Good | Low | Free |

**Decision**: Use all three in a layered approach — pnpm audit for immediate CI feedback, Snyk for comprehensive monitoring and fix advice, Trivy for container and filesystem scanning.

### Why block GPL dependencies?

GPL-licensed packages can impose licensing obligations on the entire application, especially if distributed. For a SaaS platform, AGPL is particularly problematic. The dependency review action rejects PRs that introduce copyleft licenses.

## Integration Points

- **CI pipeline**: pnpm audit runs on every PR, Snyk/Trivy on schedule
- **GitHub Security**: Vulnerability alerts from Dependabot and CodeQL
- **Notifications**: Slack/email alerts for critical vulnerabilities via GitHub Actions
- **Dashboard**: Security posture dashboard aggregating audit results

## Production Considerations

1. **Zero-day response**: When a CVE is published for a dependency, the response time should be < 4 hours for critical, < 24 hours for high. Maintain a runbook for emergency dependency updates
2. **SBOM generation**: Generate a Software Bill of Materials for compliance: `pnpm sbom --format cyclonedx > sbom.json`
3. **Vulnerability database lag**: pnpm audit relies on the npm advisory database, which can lag behind CVE publication. Supplement with Snyk for faster coverage
4. **False positive handling**: Not all audit findings are exploitable in your specific application context. Document false positives and configure suppression in the allowlist
5. **Dependency freezing**: Before major releases, freeze dependencies at known-good versions and run a comprehensive security scan. Document the freeze in release notes
