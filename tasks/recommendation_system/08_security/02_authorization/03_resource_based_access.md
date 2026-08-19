# Resource-Based Access Control

## 1. Overview

Resource-based access control restricts access to resources based on ownership, team
membership, data partitioning, and namespace isolation. For recommendation systems, this
is critical because different tenants, teams, and users should only access the resources
they own or are explicitly authorized to use. This document covers resource ownership,
team-based access, data partitioning, namespace isolation, and multi-tenant access control.

### 1.1 Resource Types in Recommendation Systems

| Resource Type | Examples | Sensitivity | Access Pattern |
|---|---|---|---|
| User data | Profiles, interaction history | High | Per-user isolation |
| Model artifacts | Trained models, embeddings | High | Per-team isolation |
| Feature data | Feature stores, pipelines | Medium | Per-project isolation |
| Configuration | API configs, experiment configs | Medium | Per-environment isolation |
| Analytics data | Metrics, reports | Low-Medium | Per-team aggregation |

---

## 2. Resource Ownership

### 2.1 Ownership Model

Every resource has an owner that determines primary access rights:

```
Resource Ownership Hierarchy:
├── System Owner (infrastructure team)
│   └── Owns all system resources
├── Team Owner (team lead)
│   └── Owns team-specific resources
├── User Owner (individual user)
│   └── Owns personal resources
└── Service Owner (service account)
    └── Owns service-generated resources
```

### 2.2 Ownership Metadata

Every resource stores ownership information:

```json
{
  "resource_id": "model_prod_v2.3",
  "resource_type": "model",
  "owner": {
    "type": "team",
    "id": "team_recommendation",
    "lead": "usr_lead_123"
  },
  "created_by": "usr_ml_456",
  "created_at": "2026-01-15T10:30:00Z",
  "last_modified_by": "usr_ml_789",
  "last_modified_at": "2026-01-20T14:00:00Z",
  "access_control": {
    "read": ["team_recommendation", "team_platform"],
    "write": ["team_recommendation"],
    "delete": ["team_recommendation_lead"],
    "admin": ["system_admin"]
  }
}
```

### 2.3 Ownership Transfer

When resources change ownership:

| Transfer Type | Process | Approval |
|---|---|---|
| Individual → Team | User joins team, resource moves | Team lead approval |
| Team → Team | Cross-team resource sharing | Both team leads + admin |
| Individual → Individual | Personal resource transfer | Both users + admin |
| User departure | Resource reassignment | Automatic (admin override) |

### 2.4 Ownership-Based Permissions

| Owner Role | Read | Write | Delete | Admin | Transfer |
|---|---|---|---|---|---|
| Resource owner | Yes | Yes | Yes | Yes | Yes |
| Team member | Yes | Yes (limited) | No | No | No |
| Team lead | Yes | Yes | Yes | Yes | Yes |
| Other team | Conditional | No | No | No | No |
| System admin | Yes | Yes | Yes | Yes | Yes |

---

## 3. Team-Based Access

### 3.1 Team Structure

```
Organization
├── Platform Team
│   ├── Infrastructure
│   ├── DevOps
│   └── Security
├── ML Team
│   ├── Recommendation
│   ├── Search
│   └── Ads
├── Data Team
│   ├── Data Engineering
│   ├── Analytics
│   └── Data Science
└── Product Team
    ├── Consumer
    ├── Partner
    └── Growth
```

### 3.2 Team Access Policies

| Team | Recommendation Resources | Feature Resources | Model Resources |
|---|---|---|---|
| Recommendation | Full access | Full access | Full access |
| Search | Read access | Read access | Read access (search models) |
| Data Engineering | Read access | Full access | No access |
| Data Science | Read access | Read access | Read access |
| Analytics | Read access (aggregated) | No access | No access |
| Platform | Admin access | Admin access | Admin access |

### 3.3 Team Membership Management

- **Joining a team**: Grant access to team resources, revoke previous team access
- **Leaving a team**: Revoke access, transfer owned resources
- **Role change within team**: Adjust permissions based on new role
- **Team dissolution**: Reassign all resources before decommissioning

### 3.4 Cross-Team Collaboration

For projects requiring multiple teams:

```
Project-Based Access:
├── Create project scope (e.g., "proj_new_rec_algo")
├── Grant specific teams access to project resources
├── Define project-level permissions
├── Time-bound access (project duration)
└── Automatic cleanup on project completion
```

---

## 4. Data Partitioning

### 4.1 Partitioning Strategies

| Strategy | Implementation | Use Case |
|---|---|---|
| Tenant-based | Separate keys per tenant | Multi-tenant SaaS |
| Environment-based | Separate clusters per environment | Dev/staging/prod isolation |
| Region-based | Data locality per region | Data residency compliance |
| Team-based | Namespace per team | Internal data isolation |

### 4.2 Tenant-Based Partitioning

```
Redis Key Structure:
├── tenant:acme:features:user:123 → Feature values for Acme's user 123
├── tenant:acme:recommendations:user:456 → Recommendations for Acme's user 456
├── tenant:globex:features:user:789 → Feature values for Globex's user 789
└── (Complete isolation between tenants)
```

**Partition enforcement:**

- All data access queries include tenant filter
- Cross-tenant queries blocked at database proxy level
- Tenant context extracted from JWT and enforced at PEP
- Monitoring detects any cross-tenant access attempts

### 4.3 Database Partitioning

| Approach | Implementation | Isolation Level |
|---|---|---|
| Schema per tenant | Separate database schemas | Strong |
| Database per tenant | Separate database instances | Strongest |
| Row-level security | PostgreSQL RLS policies | Strong |
| Column-level security | Column masking based on tenant | Moderate |
| Application-level | WHERE clause filtering | Moderate (risk of bugs) |

### 4.4 Partition Testing

| Test | Method | Acceptance Criteria |
|---|---|---|
| Isolation test | Attempt cross-partition access | Access denied |
| Performance test | Query within partition | Latency within SLA |
| Scaling test | Multiple partitions active | Linear performance scaling |
| Recovery test | Partition failure | Other partitions unaffected |

---

## 5. Namespace Isolation

### 5.1 Namespace Structure

```
Namespace Hierarchy:
├── production
│   ├── recommendation-service
│   │   ├── models
│   │   ├── features
│   │   └── configs
│   └── feature-pipeline
│       ├── jobs
│       └── outputs
├── staging
│   ├── recommendation-service
│   └── feature-pipeline
└── development
    ├── recommendation-service
    └── feature-pipeline
```

### 5.2 Namespace Access Rules

| Namespace | Who Can Access | Who Can Modify | Who Can Delete |
|---|---|---|---|
| production | Platform team (read/write) | Platform team (with approval) | Admin only |
| staging | All engineering | Team members | Team leads |
| development | All engineers | Individual engineers | Individual engineers |
| shared | All teams | Shared ownership | Admin approval |

### 5.3 Namespace Resource Quotas

| Namespace | CPU Limit | Memory Limit | Storage Limit | QPS Limit |
|---|---|---|---|---|
| production | Unlimited | Unlimited | Per-tenant SLA | Per-tenant SLA |
| staging | 50% of prod | 50% of prod | 100 GB | 1000 QPS |
| development | 10% of prod | 10% of prod | 50 GB | 100 QPS |

---

## 6. Multi-Tenant Access Control

### 6.1 Tenant Isolation Model

```
Tenant Isolation Layers:
├── Network isolation (separate VPC/subnets for sensitive tenants)
├── Compute isolation (separate pods/namespaces)
├── Storage isolation (separate databases/buckets)
├── Cache isolation (separate Redis instances or key prefixes)
└── Monitoring isolation (separate dashboards/alerts)
```

### 6.2 Tenant Access Control Matrix

| Resource | Tenant A | Tenant B | Platform Admin |
|---|---|---|---|
| Tenant A's data | Full access | No access | Admin access |
| Tenant B's data | No access | Full access | Admin access |
| Shared models | Read access | Read access | Full access |
| Platform configs | No access | No access | Full access |
| Cross-tenant analytics | No access | No access | Aggregated only |

### 6.3 Tenant Onboarding

```
Tenant Onboarding Process:
1. Create tenant namespace and database schema
2. Generate tenant-specific API keys
3. Configure tenant-specific rate limits
4. Set up tenant monitoring and alerting
5. Deploy tenant-specific configurations
6. Validate isolation with penetration test
7. Document tenant-specific runbooks
```

### 6.4 Tenant Offboarding

```
Tenant Offboarding Process:
1. Notify tenant of impending deactivation
2. Export tenant data (per retention policy)
3. Revoke all tenant API keys and sessions
4. Delete tenant data from all systems
5. Remove tenant namespace and configurations
6. Verify complete data deletion
7. Document offboarding completion
```

### 6.5 Tenant Security Monitoring

| Metric | Alert Threshold | Action |
|---|---|---|
| Cross-tenant access attempt | Any attempt | Block + alert security |
| Tenant data export volume | > 10x normal | Alert + investigate |
| Tenant API usage spike | > 5x normal | Alert + investigate |
| Tenant authentication failures | > 10 in 5 minutes | Alert + possible lockout |
| Tenant resource quota exceeded | > 90% usage | Alert + capacity planning |
