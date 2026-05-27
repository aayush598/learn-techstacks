# Key Security Best Practices

## Overview

API key security prevents accidental exposure and limits damage if a key is compromised. Guidelines cover storage, logging, transmission, and monitoring.

## Best Practices Document

```typescript
interface KeySecurityGuideline {
  category: string;
  rules: SecurityRule[];
}

const KEY_SECURITY_GUIDELINES: KeySecurityGuideline[] = [
  {
    category: 'Storage',
    rules: [
      { rule: 'Store API keys in environment variables, never in code', severity: 'critical' },
      { rule: 'Use .env files locally, secrets manager in production', severity: 'critical' },
      { rule: 'Never commit keys to version control', severity: 'critical' },
      { rule: 'Encrypt keys at rest if stored in database', severity: 'high' },
    ],
  },
  {
    category: 'Transmission',
    rules: [
      { rule: 'Always use HTTPS for API requests', severity: 'critical' },
      { rule: 'Include API key in Authorization header, not URL', severity: 'high' },
      { rule: 'Never log or print API keys', severity: 'critical' },
      { rule: 'Use short-lived keys for CI/CD pipelines', severity: 'medium' },
    ],
  },
  {
    category: 'Server-Side',
    rules: [
      { rule: 'Hash keys with SHA-256 before storing', severity: 'critical' },
      { rule: 'Implement key rotation policies', severity: 'high' },
      { rule: 'Apply least-privilege scoping to each key', severity: 'high' },
      { rule: 'Monitor for unusual key usage patterns', severity: 'medium' },
    ],
  },
  {
    category: 'Client-Side',
    rules: [
      { rule: 'Never expose API keys in client-side code', severity: 'critical' },
      { rule: 'Use proxy/BFF for client-side API calls', severity: 'high' },
      { rule: 'Implement key expiry and rotation in SDK', severity: 'medium' },
    ],
  },
];
```

## Automated Scanning

```typescript
class KeyLeakDetectionService {
  private patterns = [
    /sk_(live|test)_[a-z0-9]{8}_[a-f0-9]{64}/g,
    /API_KEY=['"][A-Za-z0-9_-]{20,}['"]/g,
  ];

  async scanForLeaks(content: string, source: string): Promise<LeakResult[]> {
    const leaks: LeakResult[] = [];

    for (const pattern of this.patterns) {
      const matches = content.match(pattern);
      if (matches) {
        for (const match of matches) {
          if (this.isActiveKey(match)) {
            leaks.push({
              pattern: match.slice(0, 20) + '...',
              source,
              severity: 'critical',
              recommendation: 'Revoke key immediately. Check git history for removal.',
            });
          }
        }
      }
    }

    return leaks;
  }

  async scanGitHistory(repoPath: string): Promise<LeakResult[]> {
    // Check git diff and recent commits for key patterns
    const diff = execSync(`cd ${repoPath} && git log --all --diff-filter=A -p`).toString();
    return this.scanForLeaks(diff, `git:${repoPath}`);
  }
}
```

## Open-Source Tools

- **git-secrets** (Apache 2.0) — Prevent committing secrets
- **truffleHog** (Apache 2.0) — Git secret scanning
- **Gitleaks** (MIT) — Git repo secret scanning

## Production Considerations

- Run secret scanning in CI/CD pipeline
- Auto-revoke keys detected in public repositories
- Send alert to security team on key leak detection
- Provide pre-commit hook for key pattern detection
- Integrate with GitHub secret scanning alerts
- Generate compliance report for key management practices
- Educate developers on key security via onboarding docs
- Never include key values in error messages or responses
