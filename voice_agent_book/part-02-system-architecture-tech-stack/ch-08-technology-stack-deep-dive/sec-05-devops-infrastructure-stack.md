# Section 05: DevOps & Infrastructure Stack

## Technology Overview

The DevOps and infrastructure stack uses **Docker** for containerization, **K3s** (lightweight Kubernetes) for orchestration, **Helm** for package management, **ArgoCD** for GitOps deployment, **Terraform** for infrastructure as code, **GitHub Actions** for CI/CD, and **Prometheus + Grafana** for monitoring.

```
┌─────────────────────────────────────────────────────────────────────┐
│               DEVOPS & INFRASTRUCTURE STACK                         │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Development                        Production              │   │
│  │  ┌──────────────┐                   ┌──────────────────┐   │   │
│  │  │  Docker Compose│                  │  K3s Cluster     │   │   │
│  │  │  (Local dev)  │                  │  (Multi-node)    │   │   │
│  │  └──────────────┘                   └──────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  CI/CD Pipeline (GitHub Actions)                            │   │
│  │                                                              │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │   │
│  │  │  Lint    │  │  Type    │  │  Unit    │  │  Build   │   │   │
│  │  │  & Test  │  │  Check   │  │  Test    │  │  Docker  │   │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │   │
│  │        │             │             │             │          │   │
│  │        └─────────────┴─────────────┴─────────────┘          │   │
│  │                          │                                   │   │
│  │                     ┌────┴────┐                             │   │
│  │                     │  Deploy  │                             │   │
│  │                     │ (ArgoCD) │                             │   │
│  │                     └─────────┘                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Infrastructure (Terraform)                                 │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐    │   │
│  │  │  K3s Cluster  │ │  PostgreSQL  │ │  Redis Cluster   │    │   │
│  │  │  (Hetzner)    │ │  (Elephant   │ │  (Upstash/       │    │   │
│  │  │              │ │  SQL/Self)   │ │   Self-hosted)   │    │   │
│  │  └──────────────┘ └──────────────┘ └──────────────────┘    │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐    │   │
│  │  │  MinIO       │ │  ClickHouse  │ │  Kafka           │    │   │
│  │  │  (Object)    │ │  (Analytics) │ │  (Event Bus)     │    │   │
│  │  └──────────────┘ └──────────────┘ └──────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Monitoring (Prometheus + Grafana)                          │   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐    │   │
│  │  │  Metrics     │ │  Logs        │ │  Traces          │    │   │
│  │  │  (Prometheus)│ │  (Loki)      │ │  (Tempo)         │    │   │
│  │  └──────────────┘ └──────────────┘ └──────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Docker Compose (Development)

```yaml
# docker-compose.yml
version: '3.9'
services:
  postgres:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: voiceagent
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: devpassword
    ports:
      - '5432:5432'
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - '6379:6379'

  minio:
    image: minio/minio
    command: server /data --console-address ':9001'
    ports:
      - '9000:9000'
      - '9001:9001'
    volumes:
      - minio-data:/data

  clickhouse:
    image: clickhouse/clickhouse-server:24.1
    ports:
      - '8123:8123'
      - '9000:9000'

  kafka:
    image: confluentinc/cp-kafka:7.6
    ports:
      - '9092:9092'
    environment:
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092

  app:
    build: .
    ports:
      - '3000:3000'
    environment:
      DATABASE_URL: postgresql://dev:devpassword@postgres:5432/voiceagent
      REDIS_URL: redis://redis:6379
      MINIO_ENDPOINT: minio:9000
    depends_on:
      - postgres
      - redis
      - minio

volumes:
  pgdata:
  minio-data:
```

## GitHub Actions CI/CD

```yaml
# .github/workflows/ci.yml
name: CI/CD
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
      - uses: actions/setup-node@v4
        with: { node-version: '20' }

      - run: pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm typecheck
      - run: pnpm test -- --coverage
      - run: pnpm build

  docker:
    needs: quality
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with: { registry: ghcr.io, username: ${{ github.actor }}, password: ${{ secrets.GITHUB_TOKEN }} }

      - run: docker build -t ghcr.io/${{ github.repository }}:${{ github.sha }} .
      - run: docker push ghcr.io/${{ github.repository }}:${{ github.sha }}

  deploy:
    needs: docker
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: argoproj/argo-cd-actions@v2
        with:
          version: '2.10'
      - run: argocd app sync voiceagent --grpc-web
```

## Terraform Infrastructure

```hcl
# main.tf
terraform {
  required_providers {
    hcloud = { source = "hetznercloud/hcloud" }
    kubernetes = { source = "hashicorp/kubernetes" }
    helm = { source = "hashicorp/helm" }
  }
}

# K3s cluster nodes
resource "hcloud_server" "k3s_nodes" {
  count       = 3
  name        = "k3s-node-${count.index}"
  server_type = "cax21"  # 4 vCPU, 8GB RAM
  image       = "ubuntu-24.04"
  location    = "nbg1"
}

# PostgreSQL (managed)
resource "hcloud_server" "postgres" {
  name        = "postgres-master"
  server_type = "cax31"  # 8 vCPU, 16GB RAM
  image       = "ubuntu-24.04"
}

# MinIO
resource "helm_release" "minio" {
  name       = "minio"
  repository = "https://charts.min.io/"
  chart      = "minio"
  values = [file("${path.module}/values/minio.yaml")]
}

# Prometheus stack
resource "helm_release" "prometheus" {
  name       = "kube-prometheus-stack"
  repository = "https://prometheus-community.github.io/helm-charts"
  chart      = "kube-prometheus-stack"
}
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Orchestration | K3s (lightweight Kubernetes) | Full K8s API, small footprint, edge-compatible |
| CI/CD | GitHub Actions + ArgoCD | GitOps, automated sync, PR-based promotion |
| IaC | Terraform | State management, multi-cloud, declarative |
| Container registry | GitHub Container Registry (ghcr.io) | Co-located with code, no extra service |
| Monitoring | Prometheus + Grafana + Loki + Tempo | CNCF stack, self-hosted, no vendor lock-in |
| Secrets | HashiCorp Vault + External Secrets Operator | Centralized, audited, auto-rotation |

## Integration Points

- **Ch 01 (System Architecture)** — Infrastructure maps to architecture layers
- **Ch 08 (Cost Analysis)** — Infrastructure costs per tier
- **Ch 10 (Security)** — Container scanning, network policies, secrets management
- **Ch 13 (CI/CD)** — Detailed CI/CD pipeline design

## Production Considerations

- **Node Sizing**: K3s nodes: 4 vCPU / 8GB RAM (general), GPU nodes: A10G for voice inference
- **High Availability**: 3 control plane nodes, multiple replicas per service, pod anti-affinity
- **Auto-scaling**: KEDA scaler based on BullMQ queue depth and active call count
- **Cost Optimization**: Spot instances for GPU workers (80% cost reduction with proper interruption handling)
- **Disaster Recovery**: Cluster state backed up to MinIO every hour, cross-region failover plan
- **Resource Limits**: CPU/memory requests and limits set per service; HPA at 70% CPU utilization
