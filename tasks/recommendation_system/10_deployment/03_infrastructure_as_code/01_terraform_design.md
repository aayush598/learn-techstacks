# Terraform Design for Recommendation Infrastructure

## Overview

Infrastructure as Code (IaC) is the foundation of reproducible, auditable, and scalable infrastructure for recommendation systems. Terraform provides declarative infrastructure management with a rich ecosystem of providers and modules. This document covers module design, state management, workspace strategies, and operational patterns for managing the full infrastructure stack.

## Module Design

### Module Hierarchy

```
infrastructure/
├── modules/
│   ├── networking/
│   │   ├── vpc/
│   │   ├── subnets/
│   │   ├── nat-gateway/
│   │   └── vpc-peering/
│   ├── compute/
│   │   ├── eks-cluster/
│   │   ├── node-groups/
│   │   └── fargate-profiles/
│   ├── data/
│   │   ├── rds-postgresql/
│   │   ├── elasticache-redis/
│   │   ├── opensearch/
│   │   └── msk-kafka/
│   ├── storage/
│   │   ├── s3-bucket/
│   │   ├── efs/
│   │   └── ebs-volumes/
│   ├── ml/
│   │   ├── sagemaker-endpoint/
│   │   ├── ecr-repository/
│   │   ├── feature-store/
│   │   └── mlflow-tracking/
│   ├── security/
│   │   ├── iam-roles/
│   │   ├── kms-keys/
│   │   ├── secrets-manager/
│   │   └── security-groups/
│   └── monitoring/
│       ├── cloudwatch/
│       ├── prometheus/
│       └── grafana/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── production/
└── global/
    ├── iam/
    ├── dns/
    └── certificates/
```

### Module Design Principles

- **Single Responsibility**: Each module manages one logical resource type (e.g., VPC, RDS, EKS).
- **Composability**: Modules should be independently usable and combinable in higher-level compositions.
- **Parameterization**: Expose all environment-specific values as input variables with sensible defaults.
- **Outputs**: Export all values needed by downstream modules and consumers.
- **Documentation**: Every module must include a README with usage examples and variable descriptions.

### Core Module Specifications

**VPC Module**

- Create a VPC with /16 CIDR block (10.0.0.0/16) for maximum flexibility.
- Provision public and private subnets across 3 availability zones.
- Private subnets receive /20 CIDR blocks for approximately 4,096 IPs each.
- Deploy NAT Gateways in each AZ for high-availability outbound traffic.
- Enable VPC Flow Logs to CloudWatch for network monitoring and security audit.
- Output: VPC ID, subnet IDs, NAT Gateway IPs, route table IDs.

**EKS Cluster Module**

- Create an EKS cluster with Kubernetes version pinned explicitly (not auto).
- Enable control plane logging (api, audit, authenticator, controllerManager, scheduler).
- Configure OIDC provider for IAM Roles for Service Accounts (IRSA).
- Create managed node groups with configurable instance types, sizes, and scaling parameters.
- Install EKS Addons: CoreDNS, kube-proxy, VPC CNI, EBS CSI Driver.
- Output: cluster endpoint, CA certificate, cluster security group, OIDC provider ARN.

**RDS PostgreSQL Module**

- Deploy a Multi-AZ RDS instance for high availability.
- Enable automated backups with configurable retention (7-35 days).
- Configure performance insights with 7-day retention (free tier).
- Enable encryption at rest using a customer-managed KMS key.
- Set up read replicas for read-heavy recommendation queries.
- Configure connection pooling via RDS Proxy for efficient connection management.
- Output: endpoint, port, database name, secret ARN, replica endpoint.

**ElastiCache Redis Module**

- Deploy Redis in cluster mode with automatic sharding.
- Configure 3 shards with 2 replicas each for production.
- Enable encryption in transit (TLS) and at rest.
- Set up automatic failover with multi-AZ replication.
- Configure eviction policy based on workload characteristics.
- Output: primary endpoint, reader endpoint, port, auth token ARN.

**S3 Bucket Module**

- Create versioned S3 buckets for model artifacts, training data, and backups.
- Enable server-side encryption with AES-256 or KMS.
- Configure lifecycle policies: transitions to IA after 30 days, Glacier after 90 days.
- Block all public access and enable access logging.
- Set up cross-region replication for disaster recovery buckets.
- Output: bucket ARN, domain name, region.

## State Management

### Remote State with S3 Backend

**Backend Configuration**

- Store Terraform state in S3 with server-side encryption (AES-256).
- Enable DynamoDB state locking to prevent concurrent modifications.
- Use separate state files per environment and per component (VPC, EKS, RDS, etc.).
- Enable S3 versioning for state file history and recovery.

**State File Organization**

| State File | Contains | Depends On |
|------------|----------|------------|
| `global/terraform.tfstate` | IAM roles, DNS zones, certificates | Nothing |
| `dev/networking/terraform.tfstate` | VPC, subnets, NAT gateways | global |
| `dev/compute/terraform.tfstate` | EKS cluster, node groups | networking |
| `dev/data/terraform.tfstate` | RDS, Redis, OpenSearch | networking |
| `dev/ml/terraform.tfstate` | ECR, SageMaker, Feature Store | compute, data |

**State File Dependencies**

- Explicitly define dependencies using `terraform_remote_state` data sources.
- Never use implicit dependencies through shared variables alone.
- Document all cross-state dependencies in module READMEs.
- Use data sources for read-only references to avoid circular dependencies.

### State File Security

- Enable S3 bucket versioning for state file rollback capability.
- Restrict state file access via IAM policies (only CI/CD and admin roles).
- Enable CloudTrail logging for all S3 access to the state bucket.
- Never store sensitive values directly in state files; reference Secrets Manager ARNs.
- Enable MFA delete protection on the state bucket in production.

## Workspace Strategy

### Environment Isolation

- Use separate state files per environment rather than Terraform workspaces for isolation.
- Workspaces are useful for ephemeral preview environments only.
- Maintain identical module versions across all environments; vary only input variables.
- Promote infrastructure changes through environments sequentially: dev → staging → production.

### Variable File Organization

```
environments/
├── dev/
│   ├── terraform.tfvars          # Dev-specific values
│   ├── variables.auto.tfvars     # Auto-loaded variables
│   └── backend.hcl               # Dev backend config
├── staging/
│   ├── terraform.tfvars
│   ├── variables.auto.tfvars
│   └── backend.hcl
└── production/
    ├── terraform.tfvars
    ├── variables.auto.tfvars
    └── backend.hcl
```

### Environment Differences

| Resource | Dev | Staging | Production |
|----------|-----|---------|------------|
| EKS Nodes | 2x t3.medium | 3x m5.xlarge | 5x m5.2xlarge (min) |
| RDS Instance | db.t3.micro | db.r5.large | db.r5.xlarge (Multi-AZ) |
| Redis | 1 shard, t3.small | 2 shards, r5.large | 3 shards, r5.xlarge |
| S3 Versioning | Enabled | Enabled | Enabled |
| Backup Retention | 1 day | 7 days | 30 days |
| Enable Deletion Protection | No | No | Yes |

## Drift Detection

### Automated Drift Detection

- Schedule `terraform plan` runs daily via CI/CD pipeline.
- Compare plan output against the last known state to detect drift.
- Alert on any drift via Slack/webhook integration.
- Classify drift: critical (security groups, IAM) vs. non-critical (tags, descriptions).

### Drift Response Process

1. Alert triggers on detected drift in production infrastructure.
2. Determine if drift was intentional (manual change) or unintentional.
3. If intentional: update Terraform configuration to match the new state.
4. If unintentional: investigate root cause and apply `terraform apply` to remediate.
5. Document the drift event and root cause in the change log.
6. Implement guardrails to prevent future drift (SCP, IAM policies, git hooks).

### Preventive Controls

- Restrict manual infrastructure changes via IAM policies.
- Use AWS Config rules to detect non-compliant resources.
- Implement SCP (Service Control Policies) to prevent deletion of critical resources.
- Enable CloudTrail and Config for full infrastructure change audit trail.

## Secrets Management

### Terraform Secrets Strategy

- Store secrets in AWS Secrets Manager or HashiCorp Vault.
- Reference secrets by ARN/ID in Terraform; never store values in `.tf` files.
- Use the `aws_secretsmanager_secret` and `aws_secretsmanager_secret_version` resources.
- Rotate secrets automatically using Lambda-based rotation lambdas.
- Use `sensitive = true` on output variables containing secrets.

### Sensitive Variable Handling

- Mark all secret variables with `sensitive = true` in variable declarations.
- Never log sensitive values in plan or apply output.
- Use `TF_VAR_` environment variables for secrets in CI/CD (not in files).
- Implement pre-commit hooks to prevent accidental commits of `.tfvars` files with secrets.

## Cost Estimation

### Cost Monitoring

- Use `terraform cost-estimation` tools (Infracost) in CI/CD pipelines.
- Generate cost reports for every pull request showing estimated monthly cost.
- Set cost budgets and alerts in AWS Budgets for each environment.
- Review cost allocation tags monthly and optimize unused resources.

### Cost Optimization Strategies

- Use Savings Plans or Reserved Instances for predictable workloads (RDS, EKS control plane).
- Leverage Spot instances for non-critical workloads (training, batch processing).
- Right-size instances using CloudWatch metrics and VPA recommendations.
- Implement S3 Intelligent-Tiering for model artifact storage.
- Use Graviton instances (ARM) for cost savings where compatible.

### Cost Estimation Table

| Component | Dev Monthly | Staging Monthly | Production Monthly |
|-----------|-------------|-----------------|-------------------|
| EKS Control Plane | $73 | $73 | $73 |
| EKS Nodes | $60 | $600 | $2,400 |
| RDS PostgreSQL | $25 | $300 | $1,200 |
| ElastiCache Redis | $15 | $200 | $800 |
| S3 Storage | $5 | $20 | $100 |
| NAT Gateway | $35 | $35 | $100 |
| Monitoring | $50 | $200 | $500 |
| **Total** | **~$263** | **~$1,628** | **~$5,173** |

## Multi-Environment Patterns

### Environment Promotion Workflow

1. Develop infrastructure changes in a feature branch.
2. Run `terraform plan` in CI and attach plan output to the PR.
3. Review plan output in PR review (mandatory for production changes).
4. Merge to main triggers `terraform apply` in dev environment.
5. After dev validation, promote to staging via manual trigger.
6. After staging validation, promote to production via manual trigger with approval gates.

### Blue-Green Infrastructure

- Maintain two complete infrastructure stacks (blue and green).
- Use DNS routing to switch traffic between stacks.
- Deploy changes to the inactive stack, validate, then switch traffic.
- Enable instant rollback by switching DNS back to the previous stack.
- Share data stores between stacks (RDS, Redis) with separate compute layers.

### Disaster Recovery Infrastructure

- Deploy a warm standby stack in a secondary region.
- Use Route53 health checks for automatic DNS failover.
- Replicate RDS cross-region using read replicas.
- Replicate S3 buckets using cross-region replication.
- Test failover quarterly with documented procedures.
- Maintain infrastructure-as-code for the DR stack in the same repository.
