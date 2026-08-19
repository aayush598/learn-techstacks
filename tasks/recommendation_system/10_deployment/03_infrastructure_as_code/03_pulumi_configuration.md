# Pulumi Configuration

Pulumi is an infrastructure-as-code tool that uses general-purpose programming languages (Python, TypeScript, Go, C#) instead of declarative configuration languages like HCL. For recommendation systems where infrastructure and application logic are deeply intertwined — feature stores, model serving endpoints, GPU clusters, caching layers — Pulumi enables expressing complex infrastructure patterns using the same language as application code, with loops, conditionals, functions, and type safety. This document covers programmatic IaC with Python/TypeScript, state management, stack composition, secrets, dynamic providers, and Pulumi vs Terraform.

---

## 1. Programmatic IaC with Python and TypeScript

### 1.1 Why Programming Languages Matter

| Capability | YAML/HCL (Terraform) | Python/TypeScript (Pulumi) |
|---|---|---|
| Loops | `for_each` meta-argument | Native `for` loops |
| Conditionals | `count` + ternary expressions | `if/else` statements |
| Abstractions | Modules (limited) | Classes, functions, packages |
| Type safety | Schema-defined | Native type hints / TypeScript types |
| Testing | `terratest` (external) | `unittest`, `pytest`, `jest` |
| Code reuse | Module registry | Standard package ecosystem |
| IDE support | Limited | Full IDE support (autocomplete, refactoring) |

### 1.2 Python Example Structure

```
pulumi/
├── Pulumi.yaml              # Project definition
├── Pulumi.dev.yaml          # Stack-specific config (dev)
├── Pulumi.staging.yaml      # Stack-specific config (staging)
├── Pulumi.prod.yaml         # Stack-specific config (production)
├── __main__.py              # Main infrastructure code
├── config.py                # Configuration loading
├── components/
│   ├── __init__.py
│   ├── networking.py        # VPC, subnets, security groups
│   ├── compute.py           # EC2 instances, EKS clusters
│   ├── storage.py           # S3 buckets, EBS volumes
│   ├── database.py          # RDS, ElastiCache
│   ├── ml_platform.py       # Feature store, model serving
│   └── monitoring.py        # Prometheus, Grafana
├── requirements.txt
└── tests/
    ├── __init__.py
    └── test_networking.py
```

### 1.3 TypeScript Example Structure

```
pulumi/
├── Pulumi.yaml
├── Pulumi.prod.yaml
├── index.ts
├── components/
│   ├── networking.ts
│   ├── compute.ts
│   ├── ml-platform.ts
│   └── monitoring.ts
├── package.json
├── tsconfig.json
└── tests/
    └── networking.test.ts
```

### 1.4 Component Resources

Pulumi component resources encapsulate related infrastructure into reusable abstractions:

| Component | Resources Encapsulated | Interface |
|---|---|---|
| `MLCluster` | EKS node group, GPU instances, autoscaler | cluster_name, endpoint, kubeconfig |
| `FeatureStore` | Redis cluster, schemas, replication | endpoint, port, auth_token |
| `ModelServingPlatform` | Ingress, service mesh config, HPA | api_endpoint, health_url |
| `MonitoringStack` | Prometheus, Grafana, alerts | grafana_url, prometheus_url |
| `DataPipeline` | S3 bucket, Glue crawlers, Airflow | pipeline_role_arn, bucket_name |

---

## 2. State Management

### 2.1 State Backend Options

| Backend | Use Case | Features |
|---|---|---|
| Pulumi Cloud (SaaS) | Default, managed | State locking, history, RBAC, audit log |
| AWS S3 + DynamoDB | Self-managed on AWS | State locking via DynamoDB, encryption via KMS |
| Azure Blob Storage | Self-managed on Azure | State locking via Blob lease |
| GCP Cloud Storage | Self-managed on GCP | State locking via object versioning |
| Local filesystem | Development only | No locking, no sharing — not for teams |

### 2.2 State Security

| Concern | Mitigation |
|---|---|
| State contains secrets | Use Pulumi's built-in secret encryption |
| Unauthorized state access | Backend encryption (S3 SSE-KMS) + IAM policies |
| State corruption | State locking (DynamoDB) + regular backups |
| State drift | Import existing resources + periodic drift detection |
| Concurrent modifications | State locking prevents simultaneous operations |

### 2.3 Secret Encryption in State

Pulumi encrypts secrets before storing them in state:

- Uses a project-specific encryption key (per-stack)
- Secrets are marked with `pulumi.Secret()` in Python or `pulumi.secret()` in TypeScript
- Encrypted values never appear in state files or CLI output
- Rotation: re-encrypt state with new key via `pulumi state rotate-key`

---

## 3. Stack Composition

### 3.1 Stack Architecture for Recommendation Systems

| Stack | Resources | Dependencies |
|---|---|---|
| `networking` | VPC, subnets, NAT gateways, security groups | None (base stack) |
| `database` | RDS, ElastiCache, S3 | networking |
| `compute` | EKS cluster, node groups, IAM roles | networking |
| `ml_platform` | Feature store, model serving endpoints | compute, database |
| `monitoring` | Prometheus, Grafana, alerts | compute |
| `application` | Kubernetes deployments, services | ml_platform, monitoring |

### 3.2 Cross-Stack References

Stacks export values that other stacks consume:

| Source Stack | Export | Consuming Stack |
|---|---|---|
| `networking` | `vpc_id`, `private_subnet_ids` | All others |
| `database` | `rds_endpoint`, `redis_endpoint` | ml_platform |
| `compute` | `cluster_name`, `kubeconfig` | ml_platform, application |
| `ml_platform` | `feature_store_endpoint` | application |

### 3.3 Stack Configuration (Pulumi.{stack}.yaml)

| Config Key | Dev | Staging | Production |
|---|---|---|---|
| `aws:region` | us-west-2 | us-west-2 | us-east-1 |
| `ml:num_replicas` | 2 | 4 | 12 |
| `ml:instance_type` | m5.large | m5.xlarge | m5.2xlarge |
| `ml:gpu_enabled` | false | true | true |
| `db:instance_class` | db.t3.micro | db.r5.large | db.r5.2xlarge |
| `db:multi_az` | false | false | true |
| `monitoring:retention_days` | 7 | 30 | 90 |

---

## 4. Secrets Management

### 4.1 Pulumi Secret Providers

| Provider | Backend | Use Case |
|---|---|---|
| Built-in | Pulumi state encryption | Default, simple |
| AWS Secrets Manager | AWS | AWS-native workloads |
| HashiCorp Vault | Self-hosted Vault | Enterprise, audit requirements |
| SOPS | File-level encryption | Git-friendly, multi-backend |
| 1Password | 1Password Connect | Team-oriented, developer-friendly |

### 4.2 Secret Handling Patterns

- Mark all sensitive values as secrets using `pulumi.Secret()`
- Never print or log secret values
- Use `--show-secrets` flag only for debugging
- Reference secrets from external providers for rotation support
- Separate secret configuration from resource definition

### 4.3 Dynamic Secret Rotation

For credentials that rotate (database passwords, API keys):

1. External provider rotates the secret (Vault, AWS Secrets Manager)
2. Pulumi stack reads the latest secret value on next update
3. Resource configuration references the secret
4. Pulumi detects the change and updates the resource

---

## 5. Dynamic Providers

### 5.1 What Are Dynamic Providers?

Dynamic providers fill gaps where Pulumi doesn't have a native resource type. They implement CRUD operations for custom resources.

### 5.2 Use Cases for Recommendation Systems

| Custom Resource | Purpose | CRUD Operations |
|---|---|---|
| ML model registry entry | Register model in custom registry | Create: register, Update: version, Delete: deregister |
| Feature store schema | Manage feature definitions | Create: deploy schema, Update: evolve, Delete: drop |
| A/B test configuration | Configure experiments | Create: start, Update: modify allocation, Delete: stop |
| Custom metric alert | Domain-specific alerts | Create: deploy, Update: threshold, Delete: remove |

### 5.3 Dynamic Provider Implementation Pattern

Each dynamic provider implements:

- `create(inputs)`: Create the resource, return output ID
- `update(id, oldInputs, newInputs)`: Update existing resource
- `delete(id)`: Clean up resource
- `check(inputs)`: Validate inputs before creation
- `diff(id, oldInputs, newInputs)`: Determine if update requires replacement

---

## 6. Pulumi vs Terraform

### 6.1 Feature Comparison

| Dimension | Pulumi | Terraform |
|---|---|---|
| Language | Python, TypeScript, Go, C# | HCL (Terraform) + Python (CDKTF) |
| State management | Pulumi Cloud, S3, GCS, local | Terraform Cloud, S3, local |
| Provider ecosystem | All Terraform providers + custom | Largest provider ecosystem |
| Testing | Native language test frameworks | `terratest`, `check` blocks (TF 1.6+) |
| Maturity | Growing (2017+) | Established (2014+) |
| Community | Smaller but growing | Large, extensive documentation |
| Enterprise features | Pulumi Business Critical | Terraform Cloud/Enterprise |
| Drift detection | Built-in | `terraform plan` |
| Import existing resources | `pulumi import` | `terraform import` |
| Policy as code | CrossGuard (OPA-based) | Sentinel (Enterprise) or OPA |

### 6.2 When to Choose Pulumi

| Scenario | Rationale |
|---|---|
| Team knows Python/TypeScript well | Lower learning curve, better productivity |
| Complex conditional infrastructure | Loops and conditionals are more natural |
| Tight integration with application code | Same language, shared libraries |
| Custom infrastructure abstractions needed | Component resources with full programming power |
| Need programmatic testing | pytest/jest with mocking and assertions |

### 6.3 When to Choose Terraform

| Scenario | Rationale |
|---|---|
| Team has strong HCL experience | Existing expertise, no retraining |
| Infrastructure is straightforward | HCL is simpler for basic provisioning |
| Large ecosystem of modules needed | Terraform Registry has more modules |
| Enterprise compliance requirements | Terraform Enterprise/Sentinel |
| Vendor preference (HashiCorp ecosystem) | Consul, Vault, Nomad integration |

### 6.4 Migration Between Tools

- Pulumi can import existing Terraform state
- Both tools can manage the same cloud resources (don't run simultaneously)
- Use `pulumi import` to adopt existing infrastructure
- Gradual migration: new stacks in Pulumi, existing stacks in Terraform
