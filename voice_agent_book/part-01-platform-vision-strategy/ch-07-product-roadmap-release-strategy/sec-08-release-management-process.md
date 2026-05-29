# Section 08: Release Management Process

## Release Philosophy

We follow continuous deployment with release trains. Features are released when ready (not on a fixed schedule), but major versions follow a predictable cadence for enterprise customers. Every release is production-proven through staging, canary, and gradual rollout.

```
Release Pipeline
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ Develop   │→│ Preview  │→│ Staging  │→│ Canary  │→│ Production│
│ PR → Main │  │ Preview  │  │ Pre-prod  │  │ 5% → 20%   │  │ 100%     │
│           │  │ Environment│  │ (mirror)  │  │ → 50%    │  │          │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
     │              │              │              │              │
     ▼              ▼              ▼              ▼              ▼
  Unit Tests    Integration    Load Tests     Smoke Tests    Monitoring
  Lint/Type     Tests (E2E)    Performance    Golden Signals    48h
```

## Versioning Strategy

We use Semantic Versioning (SemVer 2.0) with the following convention:

**Major (X.0.0):** Breaking API changes, significant feature releases. Announced 60+ days in advance with migration guides. Example: v2.0.0 (new API).

**Minor (0.X.0):** New features, non-breaking additions. Released every 2-4 weeks. Example: v1.5.0 (marketplace launch).

**Patch (0.0.X):** Bug fixes, performance improvements, security patches. Released as needed (often daily). Example: v1.5.3 (fix transcript encoding bug).

**Pre-release:** v1.5.0-beta.1, v1.5.0-rc.1. Used for early access program.

## Release Cadence

| Release Type | Frequency | Audience | Communication |
|-------------|-----------|----------|---------------|
| Daily patch | As needed | All | Automatic (no notice) |
| Weekly release | Every Friday | All | #releases Slack |
| Monthly minor | First Tuesday | All | Changelog + blog post |
| Quarterly major | Quarterly | All | Blog post, webinar, docs |
| Enterprise patch | As needed | Enterprise | TAM notification |
| Security patch | Immediate | All | Incident process |

## Release Process

```typescript
interface Release {
  version: string;
  semver: 'major' | 'minor' | 'patch';
  releaseDate: Date;
  features: Feature[];
  bugfixes: Bugfix[];
  breakingChanges: BreakingChange[];
  deprecations: Deprecation[];
  status: 'planned' | 'development' | 'staging' | 'canary' | 'released' | 'rolled_back';
}

class ReleaseManager {
  async promoteRelease(version: string, stage: string): Promise<PromotionResult> {
    const release = await this.getRelease(version);
    
    // Run gates for this stage
    const gates = this.getGates(stage);
    const results = await Promise.all(gates.map(g => g.check(release)));
    
    const failed = results.filter(r => !r.passed);
    if (failed.length > 0) {
      await this.reportGateFailures(failed);
      return { promoted: false, failures: failed };
    }
    
    // Promote to next stage
    await this.deploy(stage, release);
    await this.runSmokeTests(stage);
    
    return { promoted: true, stage };
  }
  
  async canaryRollout(version: string, percentages: number[]): Promise<void> {
    for (const pct of percentages) {
      await this.setTrafficSplit(version, pct);
      await this.monitorCanary(version, 60 * 60 * 1000); // 1 hour per step
      
      const health = await this.checkCanaryHealth(version);
      if (!health.healthy) {
        await this.rollback(version);
        throw new Error(`Canary failed: ${health.reason}`);
      }
    }
  }
}
```

## Release Gates

### Gate 1: CI/CD (Automatic)
- All unit tests pass (>90% coverage maintained)
- TypeScript compilation passes (strict mode)
- Lint passes (ESLint + Prettier)
- Build succeeds for all packages
- Security scan (Snyk/Trivy) passes

### Gate 2: Staging (Automatic)
- Integration tests pass (Cypress/Playwright)
- E2E tests pass (critical user journeys)
- Performance budget met (Lighthouse)
- API contract tests pass
- Database migration validation

### Gate 3: Canary (Automatic monitoring)
- Error rate < baseline + 0.1%
- Latency p99 < baseline + 100ms
- Call success rate > baseline - 0.5%
- Memory/CPU usage within 20% of baseline

### Gate 4: Production (Manual approval)
- Release manager approval
- Product manager approval (for features)
- Compliance approval (for compliance-related changes)
- Support team notified

## Feature Flags

All new features are behind feature flags (GrowthBook). This enables: (1) Gradual rollout to users, (2) A/B testing, (3) Quick kill switch, (4) Internal-only testing.

```typescript
interface FeatureFlag {
  key: string;
  description: string;
  owner: string;
  status: 'dev' | 'staging' | 'internal' | 'beta' | 'ga' | 'removed';
  
  targeting: {
    users: string[]; // specific users
    segments: string[]; // percentage, properties
    environment: string[];
  };
  
  schedule: {
    startDate: Date;
    endDate?: Date;
    gradualRollout: number[]; // [5, 20, 50, 100] percentages
  };
  
  metrics: {
    successMetrics: string[]; // PostHog events to track
    experimentId: string; // A/B test ID
  };
}

const featureFlags: FeatureFlag[] = [
  {
    key: 'ff-visual-agent-builder',
    description: 'Visual agent builder with drag-and-drop flow editor',
    owner: 'product-team',
    status: 'beta',
    targeting: { users: [], segments: [{ property: 'plan', value: 'pro' }], environment: ['production'] },
    schedule: { startDate: new Date('2026-01-15'), gradualRollout: [5, 20, 50, 100] },
    metrics: { successMetrics: ['agent_created', 'onboarding_completed'], experimentId: 'exp-visual-builder' },
  },
];
```

## Changelog & Communication

- **External changelog:** changelog.md in repository + `/changelog` page on website
- **Internal changelog:** #releases Slack channel
- **Major releases:** Blog post + email to customers + in-app notification
- **Breaking changes:** 60-day notice, migration guide, deprecated endpoint continues for 6 months
- **Security patches:** CVE documentation, notify affected customers via email

## Hotfix Process

For critical bugs in production: (1) Engineer identifies fix, (2) PR with "hotfix" label bypasses regular queue, (3) Fast-tracked through CI (test only, no canary), (4) Deployed to production immediately, (5) Post-mortem within 24 hours.

## Deprecation Policy

| Change Type | Notice Period | Migration Support | Sunset Timeline |
|-------------|---------------|-------------------|-----------------|
| API endpoint deprecation | 90 days | Migration guide + response header | 6 months after notice |
| SDK version deprecation | 180 days | Migration guide | 12 months after notice |
| Feature removal | 60 days | Alternative recommended | 3 months after notice |
| Pricing change | 30 days | Grandfather existing customers | Immediate for new |

## Tools & Resources

- **CI/CD:** GitHub Actions
- **Feature flags:** GrowthBook (self-hosted open-source)
- **Monitoring:** Grafana + Prometheus + Sentry
- **Incident management:** PagerDuty, Incident.io
- **Changelog:** GitHub releases + custom page
- **Documentation:** Nextra, Docusaurus
- **Release coordination:** Linear (tracking), Slack (communication)
