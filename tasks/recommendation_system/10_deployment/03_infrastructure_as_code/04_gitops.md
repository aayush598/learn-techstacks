# GitOps

GitOps is an operational framework where Git repositories are the single source of truth for declarative infrastructure and application configuration. Every change — application deployments, infrastructure updates, model version promotions — flows through Git, providing complete audit trails, rollback capability, and collaborative review. For recommendation systems, GitOps ensures that model deployments, feature configurations, and infrastructure changes are traceable, reproducible, and reversible. This document covers GitOps principles, ArgoCD and Flux CD architectures, reconciliation, drift detection, rollback patterns, and ML-specific GitOps considerations.

---

## 1. Git as Source of Truth

### 1.1 Core Principles

| Principle | Description | Benefit |
|---|---|---|
| Declarative configuration | Desired state defined in YAML files | Predictable, auditable |
| Version controlled | All changes committed to Git | Full history, blame, bisect |
| Automated delivery | Agents reconcile Git state to cluster | Eliminates manual kubectl apply |
| Continuous reconciliation | Drift is detected and corrected | Self-healing infrastructure |
| Pull-based model | Agents pull from Git (not push) | No cluster access needed from CI |

### 1.2 Repository Structure for GitOps

```
gitops-repo/
├── apps/
│   ├── recommendation-api/
│   │   ├── base/
│   │   │   ├── deployment.yaml
│   │   │   ├── service.yaml
│   │   │   ├── hpa.yaml
│   │   │   └── kustomization.yaml
│   │   └── overlays/
│   │       ├── dev/
│   │       │   ├── kustomization.yaml
│   │       │   └── replicas-patch.yaml
│   │       ├── staging/
│   │       │   ├── kustomization.yaml
│   │       │   └── replicas-patch.yaml
│   │       └── production/
│   │           ├── kustomization.yaml
│   │           ├── replicas-patch.yaml
│   │           └── resource-limits-patch.yaml
│   ├── model-server/
│   │   ├── base/
│   │   └── overlays/
│   └── feature-pipeline/
│       ├── base/
│       └── overlays/
├── infrastructure/
│   ├── networking/
│   ├── monitoring/
│   └── security/
├── models/
│   ├── prod/
│   │   ├── model-config.yaml      # Model version, artifacts, config
│   │   └── experiment-config.yaml  # A/B test allocation
│   └── staging/
└── cluster/
    ├── namespaces/
    ├── quotas/
    └── rbac/
```

### 1.3 Separation of Concerns

| Repository | Content | Audience |
|---|---|---|
| Application GitOps repo | Kubernetes manifests, Helm values | Application team |
| Infrastructure GitOps repo | Terraform outputs, cluster config | Platform team |
| Model GitOps repo | Model versions, experiment configs | ML team |
| Security GitOps repo | RBAC, network policies, secrets | Security team |

---

## 2. ArgoCD Architecture

### 2.1 Core Components

| Component | Role | Resource Requirements |
|---|---|---|
| **ArgoCD API Server** | Web UI, REST API, authentication | 500m CPU, 512Mi memory |
| **ArgoCD Repo Server** | Clones Git repos, generates manifests | 1000m CPU, 1Gi memory |
| **ArgoCD Application Controller** | Reconciles desired vs live state | 1000m CPU, 2Gi memory |
| **Redis** | Caching layer for repo server | 256m CPU, 256Mi memory |
| **Dex** (optional) | OIDC authentication provider | 100m CPU, 128Mi memory |

### 2.2 Application CRD

An ArgoCD Application defines how a Git repository maps to a Kubernetes cluster:

| Field | Description | Example |
|---|---|---|
| `source.repoURL` | Git repository URL | `https://github.com/org/gitops-repo` |
| `source.path` | Path within repo | `apps/recommendation-api/overlays/prod` |
| `source.targetRevision` | Branch, tag, or commit SHA | `main` or `v2.1.0` |
| `destination.server` | Target cluster API server | `https://kubernetes.default` |
| `destination.namespace` | Target namespace | `rec-prod` |
| `syncPolicy.automated` | Enable auto-sync | `prune: true`, `selfHeal: true` |
| `syncPolicy.syncOptions` | Sync behavior | `CreateNamespace=true` |

### 2.3 Sync Strategies

| Strategy | Behavior | Use Case |
|---|---|---|
| Manual sync | Human clicks "Sync" in UI | Production (review before deploy) |
| Auto-sync with self-heal | Automatically sync + correct drift | Staging, dev |
| Auto-sync with prune | Automatically remove deleted resources | Dev environments |
| Sync windows | Restrict sync to certain hours | Production maintenance windows |

### 2.4 ArgoCD Image Updater

Automatically update container images when new versions are pushed:

- Monitors container registries for new tags
- Updates Git repository with new image tags
- Supports semantic versioning, regex, and alphabetical strategies
- Triggers automated sync when image update is committed

**For ML model deployments:** Update model artifact tag in Git, ArgoCD syncs the ConfigMap/Deployment that references the new model.

---

## 3. Flux CD Architecture

### 3.1 Core Components

| Component | Role | Resource Requirements |
|---|---|---|
| **Source Controller** | Fetches artifacts from Git, Helm repos, S3 | 500m CPU, 512Mi memory |
| **Kustomize Controller** | Applies Kustomize overlays to cluster | 500m CPU, 512Mi memory |
| **Helm Controller** | Manages Helm releases | 500m CPU, 512Mi memory |
| **Notification Controller** | Sends alerts, receives webhooks | 100m CPU, 128Mi memory |
| **Image Automation Controllers** | Auto-update image references | 200m CPU, 256Mi memory |

### 3.2 Flux CRD Hierarchy

| CRD | Purpose | Scope |
|---|---|---|
| `GitRepository` | Source definition (URL, branch, interval) | Per repository |
| `Kustomization` | Kustomize deployment to cluster | Per application |
| `HelmRelease` | Helm chart deployment | Per application |
| `HelmChart` | Helm chart source | Per chart |
| `HelmRepository` | Helm repository source | Per repository |
| `ImageRepository` | Container image source for auto-update | Per image |
| `ImagePolicy` | Rules for selecting image tags | Per image |
| `ImageUpdateAutomation` | Commit updated images to Git | Per repo |

### 3.3 Flux vs ArgoCD

| Dimension | Flux CD | ArgoCD |
|---|---|---|
| Architecture | Distributed controllers | Monolithic (single app) |
| Resource usage | Lower (~1.5 CPU, ~1.5Gi total) | Higher (~3 CPU, ~4Gi total) |
| UI | No built-in UI (use Weave GitOps) | Rich web UI |
| Multi-tenancy | Namespace-based isolation | Project-based isolation |
| RBAC | Kubernetes-native RBAC | Built-in RBAC |
| Image automation | Built-in | Requires Image Updater (separate) |
| Helm support | Native HelmRelease CRD | Application CRD with Helm source |
| Kustomize support | Native Kustomization CRD | Application CRD with Kustomize source |
| Best for | Git-native teams, resource-constrained | Teams wanting UI, complex RBAC |

---

## 4. Continuous Reconciliation

### 4.1 Reconciliation Loop

Both ArgoCD and Flux continuously reconcile desired state (Git) with live state (cluster):

1. **Fetch**: Pull latest manifests from Git repository
2. **Render**: Apply templates, Kustomize overlays, Helm values
3. **Compare**: Diff rendered manifests against live cluster state
4. **Act**: Apply changes if differences exist (sync/prune)
5. **Report**: Update status, emit events, send notifications
6. **Repeat**: Loop every sync interval (default: 3–5 minutes)

### 4.2 Sync Interval Configuration

| Environment | Sync Interval | Rationale |
|---|---|---|
| Development | 1 minute | Fast iteration |
| Staging | 3 minutes | Balanced freshness vs load |
| Production | 5–10 minutes | Stability, reduce cluster load |

### 4.3 Sync Dependencies

For recommendation systems with ordering requirements:

1. Deploy infrastructure (databases, caches) first
2. Deploy feature pipeline after infrastructure is ready
3. Deploy model server after feature pipeline health check passes
4. Deploy API server after all dependencies are healthy

Use ArgoCD sync waves or Flux dependsOn for ordering.

---

## 5. Drift Detection

### 5.1 What Causes Drift

| Drift Source | Example | Detection |
|---|---|---|
| Manual `kubectl edit` | Engineer modifies deployment directly | Reconciliation diff |
| Emergency hotfix | `kubectl patch` during incident | Reconciliation diff |
| Operator changes | HPA scales replicas beyond Git value | Reconciliation (non-breaking) |
| Automated tools | VPA updates resource requests | Reconciliation (non-breaking) |

### 5.2 Drift Response Strategy

| Drift Type | Response | Auto-Correct? |
|---|---|---|
| Replica count (HPA) | Allow drift (expected behavior) | No (ignore annotation) |
| ConfigMap content | Correct to Git state | Yes (self-heal) |
| Image tag | Correct to Git state | Yes (self-heal) |
| Resource limits | Correct to Git state | Yes (self-heal) |
| Manual scale | Correct to Git state | Yes (with annotation exception) |

### 5.3 Excluding Expected Drift

Some drift is intentional — allow it via annotations:

- HPA-managed replica counts
- Pod disruption budget effective count
- Certain annotations added by service mesh or operators

---

## 6. Rollback via Git Revert

### 6.1 Rollback Process

1. Identify the commit that introduced the issue
2. `git revert <commit>` — creates a new commit that undoes the change
3. Push to main branch
4. ArgoCD/Flux detects the change and syncs
5. Kubernetes performs rolling update to previous state
6. Verify health checks and metrics stabilize

### 6.2 Rollback Advantages of GitOps

| Advantage | Description |
|---|---|
| Audit trail | Every change has a commit message and author |
| Reproducibility | Any historical state can be restored |
| Review process | Rollback goes through PR review |
| No special tooling | `git revert` is all you need |
| Atomic rollback | Single commit reverts all related changes |

### 6.3 Rollback for Model Deployments

Model-specific rollback in GitOps:

1. Update model ConfigMap to reference previous model artifact version
2. Commit change to Git
3. ArgoCD/Flux syncs the ConfigMap change
4. Model server detects ConfigMap change and reloads model
5. No pod restart required (hot reload)
6. Verify model metrics stabilize

---

## 7. GitOps for ML Model Deployment

### 7.1 Model Version Tracking in Git

| File | Content | Updated When |
|---|---|---|
| `model-config.yaml` | Model artifact path, version, checksum | New model trained and validated |
| `experiment-config.yaml` | A/B test allocation, feature flags | Experiment starts or ends |
| `feature-config.yaml` | Feature definitions, pipelines | Feature schema changes |
| `training-config.yaml` | Training schedule, data sources | Training pipeline changes |

### 7.2 Model Promotion Workflow

| Stage | Git Branch/Path | Auto-Sync? |
|---|---|---|
| Training complete | `models/staging/model-config.yaml` | Yes |
| Staging validation | Manual review | No |
| Promote to production | `models/prod/model-config.yaml` | Manual sync (approval gate) |
| Rollback | `git revert` on prod config | Yes |

### 7.3 ML-Specific GitOps Challenges

| Challenge | Solution |
|---|---|
| Large model artifacts (>1GB) | Store artifacts in S3/GCS, reference by URL in Git |
| Experiment allocation changes | Use Argo Rollouts or Flagger for progressive delivery |
| Feature store schema evolution | Version features, deploy new versions alongside old |
| Training pipeline scheduling | Argo Workflows or Kubeflow Pipelines orchestrated by Git |
