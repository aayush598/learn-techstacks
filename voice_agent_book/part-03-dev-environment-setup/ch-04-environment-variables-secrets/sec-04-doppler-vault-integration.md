# Section 04: Doppler/Vault Integration

## Overview

For production environments, secrets must be stored securely outside of version control. HashiCorp Vault provides enterprise-grade secret management with dynamic secrets, audit logging, and automated rotation. Doppler offers a simpler SaaS alternative. This section covers both approaches and their integration with the voice agent platform.

## Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│              Secret Management Architecture                   │
│                                                              │
│  ┌──────────┐    ┌──────────────┐    ┌──────────────────┐  │
│  │ Doppler   │    │ HashiCorp    │    │ GitHub Actions   │  │
│  │ (SaaS)    │    │ Vault        │    │ Secrets          │  │
│  └────┬─────┘    └──────┬───────┘    └────────┬─────────┘  │
│       │                │                       │            │
│       └────────────────┼───────────────────────┘            │
│                        │                                    │
│                        ▼                                    │
│               ┌──────────────────┐                          │
│               │   Application     │                          │
│               │   Startup         │                          │
│               │                  │                          │
│               │  1. Load .env    │                          │
│               │  2. Fetch from   │                          │
│               │     Vault/Doppler│                          │
│               │  3. Merge +      │                          │
│               │     validate     │                          │
│               └──────────────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

## Doppler Integration

### Setup

```bash
# Install Doppler CLI
brew install dopplerhq/cli/doppler
# or
curl -sLf https://cli.doppler.com/install.sh | sh

# Setup project
doppler setup
```

### Doppler Configuration

```bash
# Create environments
doppler environments create dev
doppler environments create staging
doppler environments create prod

# Set secrets per environment
doppler secrets set DATABASE_URL="postgresql://..." --config prod
doppler secrets set OPENAI_API_KEY="sk-..." --config prod

# Download .env for local development
doppler secrets download --config dev --format env > .env.local
```

### Doppler in CI

```yaml
# .github/workflows/deploy.yml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Inject Doppler secrets
        uses: dopplerhq/cli-action@v3
        with:
          setup: |
            echo "DOPPLER_TOKEN=${{ secrets.DOPPLER_TOKEN_PROD }}" >> $GITHUB_ENV

      - name: Deploy with secrets
        run: |
          doppler run --command="pnpm build"
          doppler run --command="pnpm deploy"
```

### Doppler SDK Integration

```typescript
// packages/config/src/providers/doppler.ts
import { env } from "../env-validator";

interface DopplerConfig {
  project: string;
  config: string;
  token: string;
}

export async function fetchFromDoppler(): Promise<Record<string, string>> {
  const dopplerConfig: DopplerConfig = {
    project: env().DOPPLER_PROJECT,
    config: env().DOPPLER_CONFIG,
    token: env().DOPPLER_TOKEN,
  };

  const response = await fetch(
    `https://api.doppler.com/v3/configs/config/secrets/download?format=json`,
    {
      headers: {
        Authorization: `Bearer ${dopplerConfig.token}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error(`Doppler API error: ${response.statusText}`);
  }

  const data = await response.json();
  return data.secrets as Record<string, string>;
}
```

## HashiCorp Vault Integration

### Vault Setup

```hcl
# vault/policies/voice-agent.hcl
path "secret/data/voice-agent/*" {
  capabilities = ["read", "list"]
}

path "secret/data/voice-agent/rotation/*" {
  capabilities = ["create", "update", "read", "delete"]
}

# Dynamic database credentials
path "database/creds/voice-agent-role" {
  capabilities = ["read"]
}
```

```hcl
# vault/policies/voice-agent-admin.hcl
path "secret/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

path "sys/*" {
  capabilities = ["read", "sudo"]
}
```

### Application Integration

```typescript
// packages/config/src/providers/vault.ts
import Vault from "node-vault";

interface VaultConfig {
  apiEndpoint: string;
  token: string;
  mountPoint: string;
  roleId?: string;
  secretId?: string;
}

export class VaultProvider {
  private client: Vault.client;
  private mountPoint: string;

  constructor(config: VaultConfig) {
    this.client = Vault({
      endpoint: config.apiEndpoint,
      token: config.token,
    });
    this.mountPoint = config.mountPoint;
  }

  // Authenticate using AppRole
  static async fromAppRole(
    endpoint: string,
    roleId: string,
    secretId: string,
  ): Promise<VaultProvider> {
    const vault = Vault({ endpoint });

    const result = await vault.approleLogin({
      role_id: roleId,
      secret_id: secretId,
    });

    return new VaultProvider({
      apiEndpoint: endpoint,
      token: result.auth.client_token,
      mountPoint: "secret",
    });
  }

  // Fetch a secret
  async getSecret(path: string): Promise<Record<string, string>> {
    const fullPath = `${this.mountPoint}/data/${path}`;
    const result = await this.client.read(fullPath);
    return result.data.data;
  }

  // Fetch all secrets for our application
  async getAppSecrets(): Promise<Record<string, string>> {
    const [database, auth, voice, llm] = await Promise.all([
      this.getSecret("voice-agent/database"),
      this.getSecret("voice-agent/auth"),
      this.getSecret("voice-agent/voice-providers"),
      this.getSecret("voice-agent/llm-providers"),
    ]);

    return {
      ...database,
      ...auth,
      ...voice,
      ...llm,
    };
  }

  // Get dynamic database credentials
  async getDatabaseCredentials(): Promise<{
    username: string;
    password: string;
  }> {
    const result = await this.client.read(
      "database/creds/voice-agent-role"
    );
    return {
      username: result.data.username,
      password: result.data.password,
    };
  }
}
```

### Kubernetes Integration (Sidecar)

```yaml
# k8s/api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: voice-agent-api
spec:
  template:
    metadata:
      annotations:
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/agent-init-first: "true"
        vault.hashicorp.com/role: "voice-agent"
        vault.hashicorp.com/agent-inject-secret-database: "secret/data/voice-agent/database"
        vault.hashicorp.com/agent-inject-secret-auth: "secret/data/voice-agent/auth"
        vault.hashicorp.com/agent-inject-template-database: |
          {{- with secret "secret/data/voice-agent/database" -}}
          export DATABASE_URL={{ .Data.data.DATABASE_URL }}
          {{- end -}}
```

## Environment Sync

### Local Development Sync

```bash
#!/bin/bash
# scripts/sync-env.sh
# Sync production secrets to local .env.local

MODE=${1:-"dev"}

case $MODE in
  dev)
    doppler secrets download --config dev --format env > .env.local
    echo "✅ Development secrets synced to .env.local"
    ;;
  staging)
    doppler secrets download --config staging --format env > .env.local
    echo "✅ Staging secrets synced to .env.local"
    ;;
  prod)
    echo "⚠️  WARNING: You are syncing PRODUCTION secrets!"
    read -p "Are you sure? (y/N) " confirm
    if [[ "$confirm" == "y" ]]; then
      doppler secrets download --config prod --format env > .env.local
      echo "✅ Production secrets synced to .env.local"
      echo "⚠️  Delete .env.local immediately after use!"
    fi
    ;;
esac
```

### CI Integration

```yaml
# .github/workflows/ci.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Option 1: Doppler
      - name: Inject Doppler secrets
        uses: dopplerhq/cli-action@v3
        with:
          setup: |
            echo "DOPPLER_TOKEN=${{ secrets.DOPPLER_TOKEN_DEV }}" >> $GITHUB_ENV

      - name: Run tests with secrets
        run: doppler run -- pnpm test

      # Option 2: Vault
      - name: Inject Vault secrets
        uses: hashicorp/vault-action@v3
        with:
          url: ${{ secrets.VAULT_URL }}
          method: approle
          roleId: ${{ secrets.VAULT_ROLE_ID }}
          secretId: ${{ secrets.VAULT_SECRET_ID }}
          secrets: |
            secret/data/voice-agent/database DATABASE_URL;
            secret/data/voice-agent/auth JWT_SECRET;

      - name: Run tests
        run: pnpm test
```

## Comparison: Doppler vs. Vault

| Feature | Doppler | HashiCorp Vault |
|---------|---------|-----------------|
| Setup complexity | Low (SaaS) | High (self-host/cloud) |
| Cost | Per-seat subscription | Free (OSS) + infra cost |
| Dynamic secrets | No | Yes (DB, cloud) |
| Audit logging | Built-in | Built-in |
| Kubernetes integration | CLI/Sidecar | Native sidecar |
| Rotation automation | Built-in | Requires scripting |
| Encryption | AES-256 at rest | AES-256 + HSM support |
| Compliance (SOC2) | Yes | Yes (with Enterprise) |

**Decision**: Use Doppler as the primary secrets manager for its simplicity and built-in automation. Use Vault alongside Doppler when dynamic database credentials or HSM-backed encryption is required.

## Design Decisions

### Why not just use GitHub Actions secrets?

GitHub Actions secrets are limited to 64KB per secret and are environment-agnostic. For a multi-environment platform with 50+ secrets per environment, Doppler/Vault provide:
- Hierarchical environment management
- Audit trails for secret access
- Automated rotation
- Integration with local development

### AppRole vs. Token Authentication

**Decision**: Use AppRole authentication (Role ID + Secret ID) for machine-to-machine authentication to Vault.

**Rationale**: Tokens can be leaked in logs or CI output. AppRole uses a two-part credential that can be rotated independently. Role ID is like a username (non-secret), Secret ID is like a password (rotatable).

## Integration Points

- **packages/config**: Providers for Doppler and Vault
- **Local development**: `doppler secrets download` syncs to `.env.local`
- **CI/CD**: Inject secrets at build/deploy time
- **Kubernetes**: Vault sidecar injects secrets into pods
- **Application**: Startup loads secrets from provider before Zod validation

## Production Considerations

1. **High availability**: Vault requires a highly available cluster with Raft storage backend. Plan for at least 3 nodes
2. **Seal/unseal**: Vault auto-seals on restart. Use auto-unseal with AWS KMS or GCP Cloud KMS for zero-touch recovery
3. **Secret caching**: Application should cache fetched secrets in memory with a TTL (typically 30-60 seconds). Avoid fetching from Vault on every request
4. **Fallback**: If Vault/Doppler is unreachable at startup, the application should fail with a clear error, not proceed with empty secrets
5. **Disaster recovery**: Regularly back up Vault's encrypted storage and test restoration. Without the backup, all secrets are permanently lost if the cluster is destroyed
