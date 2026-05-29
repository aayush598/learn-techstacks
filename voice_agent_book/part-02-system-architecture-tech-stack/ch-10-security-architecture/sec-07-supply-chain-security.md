# Section 07: Supply Chain Security

## Supply Chain Security Architecture

Supply chain security covers the entire pipeline from dependency declaration to production deployment. **Dependency scanning** (Renovate/Dependabot), **SBOM generation**, **signed commits**, and **artifact verification** ensure that every component is trusted.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SUPPLY CHAIN SECURITY PIPELINE                   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Phase 1: Dependency Management                              │   │
│  │                                                              │   │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐              │   │
│  │  │ Package  │───→│ Renovate │───→│ Dependabot│             │   │
│  │  │ Registry │    │ (Auto PR)│    │ (Security│             │   │
│  │  │ (npm,    │    │          │    │  Alerts) │             │   │
│  │  │ PyPI)    │    └──────────┘    └──────────┘              │   │
│  │  └──────────┘                                              │   │
│  │  ┌──────────┐    ┌──────────┐                              │   │
│  │  │ pnpm     │───→│ Audit    │  Fail on critical vulns     │   │
│  │  │ lockfile │    │ --audit  │                              │   │
│  │  └──────────┘    └──────────┘                              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Phase 2: Build & Sign                                      │   │
│  │                                                              │   │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐              │   │
│  │  │  Build   │───→│  SBOM    │───→│  Sign    │              │   │
│  │  │  Image   │    │  (SPDX)  │    │  (Cosign)│              │   │
│  │  └──────────┘    └──────────┘    └──────────┘              │   │
│  │  ┌──────────┐                                              │   │
│  │  │  Attest  │  In-toto attestation for provenance           │   │
│  │  └──────────┘                                              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Phase 3: Verification & Deploy                              │   │
│  │                                                              │   │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐              │   │
│  │  │  Verify  │───→│  Policy  │───→│  Deploy  │              │   │
│  │  │  Sign    │    │  Check   │    │  (ArgoCD)│              │   │
│  │  └──────────┘    └──────────┘    └──────────┘              │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Dependency Scanning (Renovate)

```javascript
// renovate.json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "config:base",
    ":separateMajorMinor",
    ":enableVulnerabilityAlerts",
    ":automergePatch"
  ],
  "packageRules": [
    {
      "matchUpdateTypes": ["major"],
      "labels": ["dependency-upgrade", "major"],
      "automerge": false,
      "assignees": ["@security-team"]
    },
    {
      "matchUpdateTypes": ["minor", "patch"],
      "matchCurrentVersion": ">=1.0.0",
      "automerge": true,
      "automergeType": "pr",
      "platformAutomerge": true
    }
  ],
  "vulnerabilityAlerts": {
    "labels": ["security"],
    "assignees": ["@security-team"],
    "automerge": true
  },
  "npm": {
    "fileMatch": ["package.json", "pnpm-lock.yaml"]
  }
}
```

## SBOM Generation

```yaml
# CI step for SBOM generation
- name: Generate SBOM
  uses: anchore/sbom-action@v0
  with:
    image: ghcr.io/${{ github.repository }}:${{ github.sha }}
    format: spdx-json
    output-file: sbom.spdx.json

- name: Upload SBOM
  uses: actions/upload-artifact@v4
  with:
    name: sbom
    path: sbom.spdx.json

- name: Attest SBOM
  uses: actions/attest-build-provenance@v1
  with:
    subject-path: sbom.spdx.json
```

## Signed Commits

```bash
# Git configuration for signed commits
git config --global user.signingkey ~/.ssh/id_ecdsa.pub
git config --global gpg.format ssh
git config --global commit.gpgsign true
git config --global tag.gpgsign true

# Verification
git verify-commit HEAD
git verify-tag v1.2.3

# Enforce signed commits in CI
# .github/workflows/verify-signed-commits.yml
steps:
  - uses: actions/checkout@v4
    with:
      fetch-depth: 0

  - name: Verify signed commits
    run: |
      git log --format='%H %G?' origin/main..HEAD | while read hash sig
      do
        if [ "$sig" != "G" ]; then
          echo "ERROR: Commit $hash is not properly signed"
          exit 1
        fi
      done
```

## Artifact Verification

```typescript
// Admission webhook that verifies image signatures before deployment
class ImageVerificationWebhook {
  async validate(image: string): Promise<ValidationResult> {
    // 1. Check image is from trusted registry
    if (!image.startsWith('ghcr.io/voiceagent/')) {
      return { allowed: false, reason: 'Untrusted registry' };
    }

    // 2. Verify Cosign signature
    try {
      await cosign.verify(image, {
        oidcIssuer: 'https://token.actions.githubusercontent.com',
      });
    } catch {
      return { allowed: false, reason: 'Image signature verification failed' };
    }

    // 3. Check Trivy scan result
    const scanResult = await trivyClient.getScanResult(image);
    if (scanResult.criticalVulns > 0) {
      return { allowed: false, reason: `Image has ${scanResult.criticalVulns} critical vulnerabilities` };
    }

    // 4. Verify SBOM is present and attested
    const sbom = await sbomClient.getSBOM(image);
    if (!sbom || !sbom.attested) {
      return { allowed: false, reason: 'SBOM not found or not attested' };
    }

    return { allowed: true };
  }
}
```

## Dependency Audit Dashboard

```typescript
// Dependency health tracking
interface DependencyHealth {
  name: string;
  version: string;
  license: string;
  latestVersion: string;
  vulnerabilities: {
    critical: number;
    high: number;
    medium: number;
    low: number;
  };
  lastAudited: Date;
  isUpToDate: boolean;
}

async function getDependencyHealth(): Promise<DependencyHealth[]> {
  // Aggregate from npm audit, Trivy, Renovate reports
  const audit = await npmAudit();
  const trivyResults = await trivyScan();
  const renovatePRs = await getRenovatePRs();

  return audit.map(dep => ({
    ...dep,
    vulnerabilities: trivyResults.find(r => r.name === dep.name)?.vulnerabilities ?? { critical: 0, high: 0, medium: 0, low: 0 },
    isUpToDate: renovatePRs.every(pr => pr.depName !== dep.name || pr.state === 'merged'),
  }));
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Dependency updates | Renovate (auto-PR) | Configurable, batch updates, vulnerability alerts |
| Vulnerability scanning | npm audit + Trivy | Package-level + OS-level coverage |
| SBOM format | SPDX 2.3 | Industry standard, tooling support |
| Commit signing | SSH keys (vs GPG) | Simpler key management, GitHub-native |
| Attestation | In-toto + Cosign | SLSA Level 2 compliance, verifiable provenance |

## Integration Points

- **Ch 10 (Container Security)** — Image signing and scanning protect container pipeline
- **Ch 08 (DevOps)** — CI/CD pipeline enforces supply chain checks
- **Ch 10 (Incident Response)** — Vulnerability alert → incident response workflow
- **Ch 08 (License Compatibility)** — License checks run alongside vulnerability scanning

## Production Considerations

- **Automated Fixes**: Patch/minor updates auto-merged after CI passes; major updates require manual review
- **Vulnerability SLA**: CRITICAL → patch within 4 hours, HIGH → within 24 hours, MEDIUM → within 7 days
- **SBOM Storage**: SBOMs stored in MinIO with 1-year retention; indexed by image digest
- **Dependency Freeze**: During release, dependencies frozen; only security patches cherry-picked
- **Audit Log**: All dependency changes tracked in audit log with before/after versions
