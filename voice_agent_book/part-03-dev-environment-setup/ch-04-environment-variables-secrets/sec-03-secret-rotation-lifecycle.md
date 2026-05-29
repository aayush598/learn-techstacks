# Section 03: Secret Rotation & Lifecycle

## Overview

Secrets — API keys, database passwords, JWT signing keys, and encryption keys — require careful lifecycle management. A rotation strategy ensures that compromised secrets have a limited window of exploitability and that key changes happen without downtime.

## Secret Lifecycle

```text
┌─────────────────────────────────────────────────────────────┐
│                   Secret Lifecycle                            │
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌───────────┐             │
│  │ Creation  │───►│ Active    │───►│ Rotation   │             │
│  │ (issue)   │    │ (use)     │    │ (renew)    │             │
│  └──────────┘    └──────────┘    └─────┬─────┘             │
│                                        │                     │
│                                        ▼                     │
│                               ┌──────────────┐              │
│                               │  Deactivation │              │
│                               │  (grace       │              │
│                               │   period)     │              │
│                               └──────┬───────┘              │
│                                      │                       │
│                                      ▼                       │
│                               ┌──────────────┐              │
│                               │   Expired     │              │
│                               │   (delete)    │              │
│                               └──────────────┘              │
└─────────────────────────────────────────────────────────────┘
```

## Rotation Schedule

```typescript
// packages/config/src/rotation-policy.ts
export interface RotationPolicy {
  secret: string;
  description: string;
  rotationInterval: number; // days
  gracePeriod: number;     // days (overlap period)
  impact: "none" | "low" | "medium" | "high";
  automation: "manual" | "semi-automated" | "fully-automated";
}

export const rotationPolicies: RotationPolicy[] = [
  {
    secret: "JWT_SECRET",
    description: "JWT signing key for authentication tokens",
    rotationInterval: 90,        // Every 3 months
    gracePeriod: 7,              // 7 days overlap
    impact: "medium",            // All sessions invalidated
    automation: "semi-automated", // Automated rotation, manual verification
  },
  {
    secret: "DATABASE_URL",
    description: "PostgreSQL connection string with password",
    rotationInterval: 180,       // Every 6 months
    gracePeriod: 1,              // 1 day overlap
    impact: "high",              // DB connection loss if misconfigured
    automation: "semi-automated",
  },
  {
    secret: "OPENAI_API_KEY",
    description: "OpenAI API key for LLM calls",
    rotationInterval: 90,        // Every 3 months
    gracePeriod: 2,              // 2 days overlap
    impact: "high",              // All AI features affected
    automation: "semi-automated",
  },
  {
    secret: "ELEVENLABS_API_KEY",
    description: "ElevenLabs TTS API key",
    rotationInterval: 90,        // Every 3 months
    gracePeriod: 2,
    impact: "high",              // Voice synthesis affected
    automation: "semi-automated",
  },
  {
    secret: "JWT_SECRET",
    description: "JWT signing key for authentication tokens",
    rotationInterval: 90,        // Every 3 months
    gracePeriod: 7,              // 7 days overlap
    impact: "medium",
    automation: "semi-automated",
  },
];
```

## Rotation Implementation

### Dual-Key Strategy for Zero-Downtime Rotation

```typescript
// packages/config/src/secret-rotation.ts
export class SecretManager {
  private activeSecret: string | null = null;
  private previousSecret: string | null = null;

  constructor() {
    this.loadSecrets();
  }

  private loadSecrets(): void {
    // Primary secret
    this.activeSecret = process.env.JWT_SECRET ?? null;

    // Previous secret during rotation grace period
    this.previousSecret = process.env.JWT_SECRET_PREVIOUS ?? null;

    if (!this.activeSecret && !this.previousSecret) {
      throw new Error("No JWT secret configured");
    }
  }

  // Verify against active OR previous secret
  verify(token: string): boolean {
    try {
      verifyJWT(token, this.activeSecret!);
      return true;
    } catch {
      if (this.previousSecret) {
        try {
          verifyJWT(token, this.previousSecret);
          return true;
        } catch {
          return false;
        }
      }
      return false;
    }
  }

  // Sign with the active secret
  sign(payload: Record<string, unknown>): string {
    return signJWT(payload, this.activeSecret!, {
      expiresIn: process.env.JWT_EXPIRES_IN ?? "1h",
    });
  }
}
```

### Automated Rotation Script

```bash
#!/bin/bash
# scripts/rotate-secret.sh
# Usage: ./rotate-secret.sh JWT_SECRET

set -euo pipefail

SECRET_NAME=$1
NEW_VALUE=$(openssl rand -base64 32)

echo "Rotating ${SECRET_NAME}..."

# 1. Store current secret as previous
export "${SECRET_NAME}_PREVIOUS"="${!SECRET_NAME}"

# 2. Set new secret
export "${SECRET_NAME}"="${NEW_VALUE}"

# 3. Update Vault/Doppler
if command -v vault &> /dev/null; then
  vault kv put secret/voice-agent/${SECRET_NAME,,} \
    value="${NEW_VALUE}" \
    previous="${!SECRET_NAME}_PREVIOUS"
fi

# 4. Trigger rolling restart
kubectl rollout restart deployment/api -n voice-agent

# 5. Wait for grace period, then remove previous
echo "Previous secret will be removed after grace period."
echo "Run: ./scripts/cleanup-secret.sh ${SECRET_NAME}"
```

### Grace Period Cleanup

```bash
#!/bin/bash
# scripts/cleanup-secret.sh
# Run after grace period expires

SECRET_NAME=$1

echo "Cleaning up previous ${SECRET_NAME}..."

# Verify all pods have restarted
kubectl rollout status deployment/api -n voice-agent

# Remove previous secret
unset "${SECRET_NAME}_PREVIOUS"

# Update Vault
vault kv patch secret/voice-agent/${SECRET_NAME,,} \
  previous=""

echo "Rotation complete for ${SECRET_NAME}"
```

## Rotating Provider API Keys

Third-party API keys (OpenAI, ElevenLabs, etc.) can't be rotated through our infrastructure alone — they require coordination with the provider:

```yaml
# .github/workflows/rotate-api-keys.yml
name: Rotate API Keys
on:
  schedule:
    - cron: '0 0 1 */3 *'   # Quarterly
  workflow_dispatch:
    inputs:
      key_name:
        description: 'Key to rotate (or "all")'
        required: true
        default: 'all'

jobs:
  rotate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Rotate keys
        run: |
          if [[ "${{ github.event.inputs.key_name }}" == "all" ]]; then
            # Rotate OpenAI key
            ./scripts/rotate-provider-key.sh OPENAI_API_KEY

            # Rotate ElevenLabs key
            ./scripts/rotate-provider-key.sh ELEVENLABS_API_KEY

            # Rotate Deepgram key
            ./scripts/rotate-provider-key.sh DEEPGRAM_API_KEY
          else
            ./scripts/rotate-provider-key.sh "${{ github.event.inputs.key_name }}"
          fi

      - name: Update secrets in GitHub
        env:
          GH_TOKEN: ${{ secrets.GH_PAT }}
        run: |
          gh secret set OPENAI_API_KEY --body "${{ env.OPENAI_API_KEY_NEW }}"
          gh secret set OPENAI_API_KEY_PREVIOUS --body "${{ env.OPENAI_API_KEY_OLD }}"

      - name: Notify team
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "API key rotation completed for ${{ github.event.inputs.key_name || 'all keys' }}"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

## Emergency Rotation

When a secret is compromised, rotation must happen immediately:

```yaml
# .github/workflows/emergency-rotation.yml
name: Emergency Secret Rotation
on:
  workflow_dispatch:
    inputs:
      compromised_secret:
        description: 'Name of compromised secret'
        required: true
      reason:
        description: 'Reason for emergency rotation'
        required: true

jobs:
  emergency-rotate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Emergency rotate
        run: |
          echo "⚠️ EMERGENCY ROTATION: ${{ github.event.inputs.compromised_secret }}"
          echo "Reason: ${{ github.event.inputs.reason }}"

      - name: Rotate and deploy
        run: |
          ./scripts/emergency-rotate.sh \
            "${{ github.event.inputs.compromised_secret }}"

      - name: Post-incident review ticket
        run: |
          gh issue create \
            --title "Post-Incident: ${{ github.event.inputs.compromised_secret }} rotation" \
            --label "security,incident" \
            --body "Reason: ${{ github.event.inputs.reason }}"
```

## Monitoring Rotation Success

```typescript
// packages/monitoring/src/rotation-health.ts
import { env } from "@voice-agent/config";

export function checkRotationStatus(): RotationStatus {
  const results: RotationStatus = {
    lastRotation: getLastRotationTimestamp(),
    secretsWithinGracePeriod: [],
    secretsExpired: [],
  };

  // Check each secret
  for (const policy of rotationPolicies) {
    const lastRotation = getSecretLastRotation(policy.secret);
    const daysSinceRotation = daysBetween(lastRotation, new Date());
    const daysUntilExpiry = policy.rotationInterval - daysSinceRotation;

    if (daysUntilExpiry < 0) {
      results.secretsExpired.push({
        secret: policy.secret,
        daysOverdue: Math.abs(daysUntilExpiry),
      });
    } else if (daysUntilExpiry < policy.gracePeriod) {
      results.secretsWithinGracePeriod.push({
        secret: policy.secret,
        daysRemaining: daysUntilExpiry,
      });
    }
  }

  return results;
}
```

## Design Decisions

### Grace Period vs. Immediate Rotation

**Decision**: Use overlapping grace periods where the old and new secrets are both valid for configurable durations.

**Rationale**: Immediate rotation invalidates all active sessions, connections, or cached data. A grace period allows:
- In-flight requests to complete with the old secret
- Connections to be re-established at natural teardown points
- Gradual rollout if the rotation causes issues
- Scheduled rotation during low-traffic windows

### Automated vs. Manual Rotation

**Decision**: Semi-automated — the rotation itself is automated, but a human must verify and approve the results.

**Rationale**: Fully automated rotation of database credentials could cause catastrophic failure if the new password doesn't propagate to all connection pools simultaneously. A human-in-the-loop catches issues before they affect users.

## Integration Points

- **Vault/Doppler**: Stores current and previous secrets
- **CI/CD**: Rotation workflows triggered on schedule
- **Monitoring**: Health checks verify secrets are valid and within rotation windows
- **Application code**: SecretManager handles dual-key verification transparently

## Production Considerations

1. **Connection pools**: Database and Redis connection pools hold persistent connections. After rotation, existing connections remain valid until closed. Use `pgbouncer` or connection proxy with `SET SESSION AUTHORIZATION` for zero-downtime DB credential rotation
2. **Cached tokens**: JWTs signed with the old secret remain valid until expiry. The dual-key strategy handles verification of tokens signed with either key
3. **Provider rate limits**: Rotating an API key involves creating a new key with the provider and testing it before deactivating the old one. Account for provider-side propagation delays (typically 5-60 minutes)
4. **Audit logging**: Log all rotation events (who, what, when) to an immutable audit log. This is critical for SOC2 and HIPAA compliance
5. **Chaos testing**: Periodically trigger a "surprise" rotation in staging to verify that the automated rotation process works and monitoring catches it
