# Helm Charts

Helm is the package manager for Kubernetes, and Helm charts are the standard packaging format for deploying complex applications. For recommendation systems, Helm charts encapsulate the deployment configuration for multiple interconnected services — API servers, model servers, feature stores, worker queues — into versioned, configurable, and reusable packages. A well-structured Helm chart transforms a complex multi-service deployment into a single `helm upgrade` command. This document covers chart architecture, values management, templating patterns, versioning, testing, and alternatives.

---

## 1. Chart Structure

### 1.1 Standard Directory Layout

```
recommendation-system/
├── Chart.yaml              # Chart metadata, version, dependencies
├── values.yaml             # Default configuration values
├── values-staging.yaml     # Staging overrides
├── values-production.yaml  # Production overrides
├── templates/
│   ├── _helpers.tpl        # Template helper functions
│   ├── NOTES.txt           # Post-install instructions
│   ├── api-server/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── hpa.yaml
│   │   ├── pdb.yaml
│   │   └── servicemonitor.yaml
│   ├── model-server/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── configmap.yaml
│   │   └── job.yaml        # Model loading job
│   ├── feature-pipeline/
│   │   ├── deployment.yaml
│   │   ├── cronjob.yaml
│   │   └── configmap.yaml
│   ├── shared/
│   │   ├── networkpolicy.yaml
│   │   ├── serviceaccount.yaml
│   │   └── secret.yaml
│   └── tests/
│       └── test-connection.yaml
├── charts/                  # Dependency charts
│   └── redis/
├── .helmignore
└── README.md
```

### 1.2 Chart.yaml Configuration

| Field | Description | Recommendation |
|---|---|---|
| `apiVersion` | Helm API version | `v2` (Helm 3) |
| `name` | Chart name | Lowercase, hyphenated |
| `version` | Chart version (semver) | Increments with every release |
| `appVersion` | Application version | Matches container image tag |
| `type` | `application` or `library` | `application` for deployable charts |
| `dependencies` | Sub-charts (Redis, PostgreSQL) | Pinned to specific versions |
| `keywords` | Search keywords | Include service name, team |
| `maintainers` | Team contacts | Include on-call rotation |

### 1.3 Umbrella Chart Pattern

For a recommendation system with multiple services, use an umbrella chart:

- Single chart that deploys all services together
- Each service is a sub-chart in `charts/` directory
- Shared values (image registry, namespace, labels) at umbrella level
- Per-service values nested under service name keys
- Enables atomic deployment and rollback of the entire system

---

## 2. Values Files Per Environment

### 2.1 Values Layering Strategy

Helm merges values in this order (later overrides earlier):

1. `values.yaml` — Defaults for all environments
2. `values-{environment}.yaml` — Environment-specific overrides
3. `--set` flags — Runtime overrides (use sparingly)

### 2.2 Environment Configuration Matrix

| Setting | Default | Staging | Production |
|---|---|---|---|
| Replicas (API server) | 2 | 2 | 6 |
| Replicas (model server) | 1 | 2 | 4 |
| CPU request (API) | 250m | 250m | 1000m |
| CPU limit (API) | 500m | 500m | 2000m |
| Memory request (model) | 2Gi | 2Gi | 8Gi |
| Memory limit (model) | 4Gi | 4Gi | 16Gi |
| HPA min replicas | 2 | 2 | 4 |
| HPA max replicas | 4 | 6 | 20 |
| Log level | info | debug | info |
| Feature store endpoint | localhost:6379 | staging-redis.internal | prod-redis.internal |
| Model artifact path | local | s3://staging-models | s3://prod-models |

### 2.3 Secrets Management

- Never store secrets in values files (even encrypted)
- Use Kubernetes Secrets referenced by name in values
- External secret management: AWS Secrets Manager, HashiCorp Vault
- Use `external-secrets-operator` or `secrets-store-csi-driver` to sync external secrets into Kubernetes Secrets
- Values files reference secret names, not secret values

---

## 3. Template Patterns

### 3.1 Helper Templates (_helpers.tpl)

Helper templates eliminate repetition and enforce consistency.

**Common helper functions:**

| Helper | Purpose | Example Usage |
|---|---|---|
| `recommendation-system.name` | Standardized chart name | All resource names |
| `recommendation-system.fullname` | Full name with release prefix | Service names, config maps |
| `recommendation-system.labels` | Common labels for all resources | Label selectors, metadata |
| `recommendation-system.selectorLabels` | Labels for pod selection | Deployment selectors |
| `recommendation-system.serviceAccountName` | SA name resolution | Service account references |
| `recommendation-system.imagePullSecrets` | Registry credentials | Image pull secrets |

### 3.2 Standard Labels

Apply these labels to every resource:

- `app.kubernetes.io/name`: Service name
- `app.kubernetes.io/instance`: Helm release name
- `app.kubernetes.io/version`: Application version
- `app.kubernetes.io/component`: Component role (api, model-server, feature-pipeline)
- `app.kubernetes.io/part-of`: System name (recommendation-system)
- `app.kubernetes.io/managed-by`: `Helm`
- `helm.sh/chart`: Chart name and version

### 3.3 Conditional Resources

Use Helm conditions to enable/disable resources per environment:

- Feature flags for optional components (monitoring sidecars, debug endpoints)
- Ingress resources (only in staging/production, not dev)
- PodDisruptionBudgets (not needed in dev with single replica)
- ServiceMonitor/PrometheusRule (only when Prometheus operator is installed)

### 3.4 Template Functions for Recommendation Systems

- `include` and `template` for reusable resource definitions
- `toYaml` and `nindent` for flexible indentation in annotations
- `lookup` for reading existing cluster state (e.g., existing PVCs)
- `jsonMarshal` for generating JSON configuration embedded in ConfigMaps

---

## 4. Chart Versioning

### 4.1 Semantic Versioning

| Change Type | Version Bump | Example |
|---|---|---|
| New feature or service | Minor bump | 1.2.0 → 1.3.0 |
| Bug fix | Patch bump | 1.3.0 → 1.3.1 |
| Breaking change | Major bump | 1.3.1 → 2.0.0 |
| App version update | Minor or patch | 1.3.0 (app v2.1) → 1.3.0 (app v2.2) |

### 4.2 Chart Releasing Process

1. Update `Chart.yaml` version
2. Update `appVersion` if container images changed
3. Update `values.yaml` if new options added
4. Run `helm lint` to validate templates
5. Run `ct lint` (chart-testing) for best practices
6. Run `helm template` and verify rendered manifests
7. Push chart to Helm repository
8. Create Git tag matching chart version
9. Update deployment pipeline to use new chart version

### 4.3 Chart Artifact Storage

| Repository Type | Tool | Use Case |
|---|---|---|
| OCI registry | GHCR, ECR, Artifact Registry | Modern, recommended |
| ChartMuseum | Self-hosted | Air-gapped environments |
| Chart repositories via Pages | GitHub Pages | Open-source charts |
| Harbor | Self-hosted with scanning | Enterprise environments |

---

## 5. Chart Testing

### 5.1 Lint and Validate

```bash
# Lint chart for errors
helm lint ./charts/recommendation-system

# Template rendering test
helm template test-release ./charts/recommendation-system \
  -f values-staging.yaml

# Validate rendered manifests against Kubernetes API
helm template test-release ./charts/recommendation-system | \
  kubectl apply --dry-run=client -f -
```

### 5.2 Chart Testing (ct)

The `ct` tool automates chart testing:

- `ct lint` — Lint charts against best practices
- `ct install` — Install charts in a test cluster and verify
- `ct lint-and-install` — Combined lint + install
- Supports changed-chart detection (only test modified charts)
- Can run against kind clusters in CI

### 5.3 Helm Unit Tests

Use **helm-unittest** plugin to test template output:

- Verify correct number of replicas rendered
- Verify resource requests/limits are set correctly
- Verify labels are applied consistently
- Verify conditional resources are included/excluded based on values
- Verify secret references are correct (not secret values)

### 5.4 Integration Tests

- Deploy chart to ephemeral kind/minikube cluster in CI
- Verify pods become ready
- Verify services are reachable
- Run smoke tests against deployed services
- Capture and compare rendered manifests as golden files

---

## 6. Dependency Management

### 6.1 Sub-chart Dependencies

| Dependency | Version Strategy | Purpose |
|---|---|---|
| Redis | Pinned minor (e.g., 18.x) | Feature cache, session store |
| PostgreSQL | Pinned minor (e.g., 13.x) | User metadata storage |
| Kafka | Pinned minor (e.g., 26.x) | Event streaming |
| Prometheus | Pinned minor (e.g., 25.x) | Monitoring stack |

### 6.2 Dependency Update Workflow

1. Check for updates: `helm dependency update`
2. Review changelog for breaking changes
3. Test in staging with updated dependencies
4. Validate no regressions in integration tests
5. Update `Chart.yaml` dependency version constraints
6. Commit lock file (`Chart.lock`) for reproducibility

---

## 7. Helm vs Kustomize

| Dimension | Helm | Kustomize |
|---|---|---|
| Approach | Template-based (Go templates) | Overlay-based (strategic merge) |
| Configuration | Values files | Patches and overlays |
| Packaging | Chart archives (tar.gz) | Directory structure |
| Reusability | Sub-charts, dependencies | Overlays composition |
| Versioning | Built-in semver for charts | Git tags for versions |
| Testing | `helm unittest`, `ct` | `kustomize build --validate` |
| Learning curve | Moderate (Go templates) | Lower (YAML-only) |
| Complex logic | Supported (functions, conditionals) | Limited (patches only) |
| Best for | Application deployment with parameters | Infrastructure with env overlays |

**Recommendation for ML systems:** Use Helm when you need complex templating logic, dependency management, and versioned releases. Use Kustomize when you have simple per-environment overlays and prefer YAML-only configuration. Many teams use both — Helm for application charts, Kustomize for cluster-level infrastructure.
