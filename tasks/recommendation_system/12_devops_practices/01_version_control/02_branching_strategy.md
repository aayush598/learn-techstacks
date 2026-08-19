# Branching Strategy

## Overview

A branching strategy defines how developers use branches to manage parallel workstreams in a recommendation system project. For ML projects, branching is more complex than traditional software because changes span code, data, models, and configuration. The right strategy balances development velocity with stability, enabling rapid experimentation while protecting production systems.

## GitFlow vs Trunk-Based Development

### GitFlow

GitFlow uses long-lived branches with explicit release cycles:

```
main (production)
  └── develop (integration)
        ├── feature/user-embedding-v2
        ├── feature/temporal-features
        └── release/v2.3.0
              └── hotfix/fix-ranking-bug
```

**Branches in GitFlow:**

| Branch | Purpose | Lifetime | Merge Target |
|--------|---------|----------|-------------|
| `main` | Production-ready code | Permanent | — |
| `develop` | Integration branch | Permanent | `main` (via release) |
| `feature/*` | New features | Days–weeks | `develop` |
| `release/*` | Release preparation | Days | `main` + `develop` |
| `hotfix/*` | Production fixes | Hours–days | `main` + `develop` |

### Trunk-Based Development

Trunk-based development uses a single main branch with short-lived feature branches:

```
main (production)
  ├── short-lived-feature (1–2 days)
  ├── short-lived-feature (1 day)
  └── short-lived-feature (3 days)
```

**Branches in Trunk-Based:**

| Branch | Purpose | Lifetime | Merge Target |
|--------|---------|----------|-------------|
| `main` | Production-ready code | Permanent | — |
| `feature/*` | Small, scoped changes | 1–3 days | `main` |
| `release/*` | Version tags (not branches) | N/A | Tagged on `main` |

### Comparison

| Aspect | GitFlow | Trunk-Based |
|--------|---------|-------------|
| Complexity | High (5+ branch types) | Low (1–2 branch types) |
| Release frequency | Scheduled (weekly/monthly) | Continuous (on merge) |
| Merge conflicts | Frequent (long-lived branches) | Rare (short-lived branches) |
| Feature isolation | Strong | Weak |
| CI/CD requirement | Moderate | Critical |
| Best for | Large teams, complex releases | Small–medium teams, continuous delivery |
| ML suitability | Good for separate model releases | Good for rapid experimentation |

### Recommendation for ML Projects

**Hybrid approach**: Use trunk-based development for application code with separate branches for model/data artifacts:

```
main (application code)
  ├── model/experiment-123 (model training code + configs)
  ├── data/schema-v2 (data pipeline changes)
  └── feature/real-time-recs (application feature)
```

## Feature Branches

### Best Practices for ML Feature Branches

| Practice | Description |
|----------|-------------|
| **Scope to one change** | One feature branch = one logical change (model change OR data change OR code change) |
| **Short-lived** | Merge within 1–3 days to minimize conflicts |
| **Named clearly** | Follow naming convention (see below) |
| **Test before merge** | All CI checks pass before merge |
| **Review before merge** | At least one code review approval |

### ML Feature Branch Scenarios

| Scenario | Branch Content | Review Required |
|----------|---------------|----------------|
| New model architecture | Model code, training config, evaluation | Yes (ML expert review) |
| Feature engineering | Feature code, schema changes, tests | Yes (data engineer review) |
| Hyperparameter tuning | Config files, experiment results | Yes (ML engineer review) |
| Evaluation methodology | Evaluation code, metric implementations | Yes (research scientist review) |
| Deployment config | Dockerfile, resource configs, scaling rules | Yes (SRE review) |

## Release Branches

### Release Process for ML Systems

```
1. Create release branch: release/v2.3.0
2. Freeze feature development
3. Run full evaluation suite
4. Validate model performance against baselines
5. Check fairness metrics and bias audits
6. Update model version metadata
7. Merge to main and tag
8. Deploy to staging
9. Validate in staging environment
10. Deploy to production (canary or full)
```

### Release Artifacts

| Artifact | Description | Storage |
|----------|-------------|---------|
| Model weights | Serialized model parameters | Model registry (MLflow, S3) |
| Training code | Git commit hash | Git tag |
| Data version | DVC hash or dataset version | Data registry |
| Config files | Hyperparameters, feature lists | Config registry |
| Evaluation report | Metrics, fairness audit, error analysis | Documentation system |
| Deployment manifest | Docker image tag, resource configs | Container registry |

## Hotfix Branches

### Hotfix Process for ML Systems

```
1. Detect issue (monitoring alert, user report, metric degradation)
2. Create hotfix branch: hotfix/fix-ranking-overflow
3. Fix the issue
4. Run regression tests
5. Fast-track code review (1 reviewer minimum)
6. Merge to main and release branch
7. Deploy immediately
8. Verify fix in production
9. Create postmortem (if severity warrants)
```

### ML-Specific Hotfix Scenarios

| Issue Type | Root Cause | Fix Approach |
|-----------|-----------|-------------|
| Model serving error | Incompatible feature format | Revert feature pipeline or fix schema |
| Ranking degradation | Data pipeline failure | Fix pipeline, retrain or revert model |
| Latency spike | Model file corruption | Reload model from registry |
| Fairness violation | Training data bias | Disable affected feature, retrain |
| Security issue | Exposed API key | Rotate key, update secrets |

## ML-Specific Branching

### Model Branches

For tracking model experiments and versions:

```
model/experiment-001 (baseline collaborative filtering)
model/experiment-002 (matrix factorization k=200)
model/experiment-003 (deep ranking model)
model/stable (current production model)
```

### Data Branches

For tracking data pipeline changes:

```
data/add-user-demographics (new data source)
data/fix-null-handling (data quality fix)
data/schema-v2 (breaking schema change)
data/retrain-2024-01 (monthly retraining)
```

### Configuration Branches

For A/B test and feature flag configurations:

```
config/ab-test-ranking-v2
config/enable-diversity-reranking
config/increase-exploration-rate
```

## Branch Naming Conventions

### Convention Format

```
<type>/<ticket-id>-<short-description>
```

### Types

| Prefix | Type | Example |
|--------|------|---------|
| `feature/` | New feature | `feature/REC-123-user-embeddings` |
| `fix/` | Bug fix | `fix/REC-456-ranking-overflow` |
| `model/` | Model change | `model/EXP-007-deep-ranking` |
| `data/` | Data pipeline change | `data/DATA-012-add-demographics` |
| `config/` | Configuration change | `config/CFG-003-ab-test-v2` |
| `hotfix/` | Urgent production fix | `hotfix/REC-789-fix-latency` |
| `release/` | Release preparation | `release/v2.3.0` |
| `chore/` | Maintenance | `chore/CH-045-update-dependencies` |

### Naming Best Practices

- Use lowercase with hyphens (not underscores or camelCase)
- Keep descriptions short but descriptive (< 50 characters after ticket ID)
- Include ticket ID for traceability
- Avoid generic names like `feature/new-feature`

## Merge vs Rebase

### Merge

```bash
git merge feature/branch
```

**Characteristics:**
- Creates a merge commit
- Preserves complete history
- Non-destructive (original commits preserved)
- Can create complex graph history

### Rebase

```bash
git rebase main
```

**Characteristics:**
- Replays commits on top of target branch
- Creates linear history
- No merge commits
- Rewrites commit history (use only on local branches)

### When to Use Each

| Scenario | Recommended | Reason |
|----------|------------|--------|
| Feature branch → develop | Merge (squash) | Clean integration history |
| Updating feature branch with main | Rebase | Keep feature branch history clean |
| Release branch → main | Merge (no-squash) | Preserve release history |
| Hotfix → main | Merge (no-squash) | Preserve hotfix history |
| Multiple developers on same branch | Merge | Rebase causes coordination issues |

### Recommendation for ML Projects

Use **squash merge** for feature branches (combines all commits into one clean commit) and **merge commits** for release/hotfix branches (preserves history).
