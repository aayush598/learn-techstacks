# Section 08: Incident Response & Security

## Incident Response Framework

The incident response process follows the **NIST 800-61** framework with four phases: **Detection**, **Containment**, **Eradication**, and **Recovery**. Each phase has documented procedures, runbooks, and postmortem requirements.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    INCIDENT RESPONSE LIFECYCLE                      │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  PHASE 1: DETECTION                                         │   │
│  │                                                              │   │
│  │  Sources:                                                    │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐   │   │
│  │  │  Falco   │ │  WAF     │ │  Rate    │ │  User Report │   │   │
│  │  │  Alerts  │ │  Alerts  │ │  Limit   │ │              │   │   │
│  │  │          │ │          │ │  Spikes  │ │              │   │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────────┘   │   │
│  │  ┌──────────┐ ┌──────────┐                                  │   │
│  │  │  Grafana │ │  Sentry  │                                  │   │
│  │  │  Alerts  │ │  Errors  │                                  │   │
│  │  └──────────┘ └──────────┘                                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  PHASE 2: CONTAINMENT                                      │   │
│  │                                                              │   │
│  │  Actions:                                                    │   │
│  │  • Rotate credentials (Vault)                               │   │
│  │  • Block IP/subnet (WAF)                                    │   │
│  │  • Disable compromised API key                             │   │
│  │  • Isolate affected pod (NetworkPolicy)                     │   │
│  │  • Revoke sessions (Redis)                                  │   │
│  │  • Snapshot compromised resources                           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  PHASE 3: ERADICATION                                      │   │
│  │                                                              │   │
│  │  Actions:                                                    │   │
│  │  • Patch vulnerability                                      │   │
│  │  • Remove unauthorized access                               │   │
│  │  • Rebuild from clean image                                 │   │
│  │  • Reset all secrets                                          │   │
│  │  • Apply security fix to codebase                           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  PHASE 4: RECOVERY                                         │   │
│  │                                                              │   │
│  │  Actions:                                                    │   │
│  │  • Restore from backup                                      │   │
│  │  • Verify system integrity                                  │   │
│  │  • Monitor for recurrence                                   │   │
│  │  • Postmortem within 48 hours                               │   │
│  │  • Update runbooks                                          │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Incident Classification

```typescript
interface IncidentDefinition {
  severity: 'SEV1' | 'SEV2' | 'SEV3' | 'SEV4';
  responseTime: number;     // Minutes to respond
  resolutionTime: number;   // Hours to resolve
  examples: string[];
  notification: string[];   // Who to notify
}

const INCIDENT_SEVERITIES: Record<string, IncidentDefinition> = {
  SEV1: {
    severity: 'SEV1',
    responseTime: 15,        // 15 minutes
    resolutionTime: 4,       // 4 hours
    examples: [
      'Data breach (PII exposure)',
      'Complete service outage',
      'Payment/billing data compromise',
      'Active ongoing attack',
    ],
    notification: ['security-team@pagerduty', 'cto@company.com', 'ceo@company.com'],
  },
  SEV2: {
    severity: 'SEV2',
    responseTime: 30,        // 30 minutes
    resolutionTime: 8,       // 8 hours
    examples: [
      'Partial service degradation',
      'Suspicious access pattern detected',
      'Vulnerability disclosure (confirmed)',
      'API key leak (customer)',
    ],
    notification: ['security-team@pagerduty', 'cto@company.com'],
  },
  SEV3: {
    severity: 'SEV3',
    responseTime: 60,        // 1 hour
    resolutionTime: 24,      // 24 hours
    examples: [
      'Single customer account compromise',
      'Failed login spike',
      'Dependency vulnerability (unexploited)',
      'Misconfigured security control',
    ],
    notification: ['security-team@slack'],
  },
  SEV4: {
    severity: 'SEV4',
    responseTime: 480,       // 8 hours (next business day)
    resolutionTime: 72,      // 72 hours
    examples: [
      'Low-severity vulnerability',
      'Security documentation gap',
      'Minor misconfiguration',
      'Security audit finding',
    ],
    notification: ['security-team@slack'],
  },
};
```

## Automated Incident Response

```typescript
// Automated response playbook for common incidents
class AutomatedResponder {
  async handleRateLimitSpike(tenantId: string): Promise<void> {
    // Auto-block if threshold exceeded
    const rate = await this.redis.get(`rate:${tenantId}:1m`);
    if (parseInt(rate) > 10000) { // 10K requests in 1 minute
      await this.blockTenant(tenantId, 'rate_limit_abuse');
      await this.alertService.sendAlert({
        severity: 'SEV2',
        title: `Tenant ${tenantId} rate limit spike`,
        description: `10K+ req/min — auto-blocked`,
      });
    }
  }

  async handleCompromisedKey(keyPrefix: string): Promise<void> {
    // Revoke key and notify
    await this.apiKeyService.revokeByPrefix(keyPrefix);
    await this.alertService.sendAlert({
      severity: 'SEV2',
      title: `API Key compromised: ${keyPrefix}...`,
      description: 'Key revoked automatically. Notifying affected tenant.',
    });

    // Notify tenant
    const tenant = await this.tenantService.getByKeyPrefix(keyPrefix);
    if (tenant) {
      await this.notificationService.sendEmail({
        to: tenant.adminEmail,
        subject: 'Security Alert: API Key Rotated',
        body: `Your API key starting with ${keyPrefix} was compromised and has been rotated. Please generate a new key.`,
      });
    }
  }
}
```

## Postmortem Template

```markdown
# Security Incident Postmortem

## Incident Summary
- **Date**: YYYY-MM-DD
- **Severity**: SEV1/SEV2/SEV3/SEV4
- **Duration**: HH:MM
- **Impact**: [Description of user/business impact]

## Timeline
| Time (UTC) | Event |
|------------|-------|
| 14:30 | First alert triggered |
| 14:32 | Engineer acknowledged |
| 14:35 | Containment initiated |
| 15:00 | Incident contained |
| 16:30 | Root cause identified |
| 18:00 | Fix deployed |
| 18:30 | Monitoring confirms resolution |

## Root Cause
[Technical explanation of what caused the incident]

## Containment Actions
1. [Action taken]
2. [Action taken]

## Resolution Actions
1. [Code fix / configuration change]

## Lessons Learned
### What went well
- [Positive aspects of response]

### What went wrong
- [Areas for improvement]

### Action Items
| Action | Owner | Due Date |
|--------|-------|----------|
| [Action] | [Name] | YYYY-MM-DD |
```

## Tabletop Exercise Scenarios

```typescript
const TABLETOP_SCENARIOS = [
  {
    name: 'Ransomware Attack',
    description: 'Production database encrypted. Attacker demands payment.',
    injects: [
      'Alert: Unusual database write patterns detected',
      'Alert: Falco reports crypto miner in container',
      'Phone call: Attacker email received with ransom note',
    ],
    questions: [
      'How do we isolate the affected systems?',
      'How do we restore from backup?',
      'Who communicates with law enforcement?',
      'Do we pay the ransom?',
    ],
  },
  {
    name: 'API Key Leak',
    description: 'Customer API key found in public GitHub repository.',
    injects: [
      'Alert: GitHub secret scanning notification',
      'Alert: Unusual API usage from new IP range',
    ],
    questions: [
      'How do we identify the affected tenant?',
      'Do we rotate the key automatically?',
      'How do we notify the customer?',
      'What scope was the key compromised?',
    ],
  },
  {
    name: 'Data Breach',
    description: 'Attacker exploited SQL injection — potential PII exposure.',
    injects: [
      'Alert: WAF detecting SQL injection attempt',
      'Alert: Large data export from production DB',
    ],
    questions: [
      'How do we determine the scope of data accessed?',
      'What are our legal notification obligations?',
      'How do we prove the vulnerability is fixed?',
      'When do we notify affected users?',
    ],
  },
];
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| IR framework | NIST 800-61 | Industry standard, well-documented phases |
| Severity model | 4-tier (SEV1-SEV4) | Escalation clarity, appropriate response time |
| Auto-response | Limited to defined patterns | Reduce human error, controlled automation |
| Postmortem | Required within 48 hours | Blameless, learning-focused |
| Tabletop exercises | Quarterly | Practice without production impact |

## Integration Points

- **Ch 10 (All)** — Incident response ties all security controls together
- **Ch 01 (Monitoring)** — Alerts trigger incident response workflow
- **Ch 10 (Secrets Management)** — Credential rotation is a containment action
- **Ch 10 (Supply Chain)** — Vulnerability disclosures may trigger incidents

## Production Considerations

- **Incident Commander**: Rotating on-call schedule; clear escalation path
- **Communication**: Internal Slack channel for active incidents; status page for customers
- **Legal Hold**: Preserve logs and evidence for potential litigation
- **Training**: Annual incident response training; new hire security onboarding
- **Metrics**: Mean time to detect (MTTD), mean time to respond (MTTR), mean time to resolve
- **Continuous Improvement**: Postmortem action items tracked in project management system with weekly review
