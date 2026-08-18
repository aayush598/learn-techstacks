# Git Workflow for ML Projects

## Overview

Version control for machine learning projects extends far beyond traditional software version control. ML projects require tracking not only code but also data, model artifacts, experiment configurations, and hyperparameters. A well-designed Git workflow accommodates these unique requirements while maintaining development velocity and code quality.

## Branching Strategy

### GitFlow for ML Projects

GitFlow provides structured branching for release-based development cycles, which aligns well with ML model release cadences.

**Branch Structure**:

| Branch | Purpose | Lifetime | Merge Target |
|--------|---------|----------|-------------|
| `main` | Production-ready code | Permanent | — |
| `develop` | Integration branch | Permanent | main |
| `feature/*` | New features, experiments | Temporary | develop |
| `experiment/*` | ML experiments, hyperparameter sweeps | Temporary | develop |
| `release/*` | Release preparation | Temporary | main + develop |
| `hotfix/*` | Production fixes | Temporary | main + develop |
| `data/*` | Data pipeline changes | Temporary | develop |
| `model/*` | Model architecture changes | Temporary | develop |

**When to Use GitFlow**:

- Release cadence is periodic (weekly, biweekly, monthly).
- Multiple model versions coexist in production.
- Strict quality gates between development and production.
- Large team with specialized roles (data engineers, ML engineers, SREs).

### Trunk-Based Development

Trunk-based development uses short-lived feature branches merged to main frequently.

**Branch Structure**:

| Branch | Purpose | Lifetime | Merge Target |
|--------|---------|----------|-------------|
| `main` | Always deployable | Permanent | — |
| `feature/*` | All changes (code, data, model) | 1-2 days | main |
| `release` | Tag for production releases | Permanent (tag) | — |

**When to Use Trunk-Based**:

- Fast iteration cycle with continuous deployment.
- Small team with strong CI/CD practices.
- Feature flags to control feature rollout.
- Model serving infrastructure supports gradual rollouts.

### Hybrid Approach (Recommended for Most Teams)

Combine trunk-based development for infrastructure code with feature-branch development for model experiments.

- Use trunk-based development for serving code, infrastructure, and utilities.
- Use feature branches for model experiments (longer iteration cycles).
- Use release tags for model versioning (not branch-based releases).
- Keep experiment branches short-lived and well-documented.

## Code Review Process

### Review Requirements

- All code changes require at least one approval before merge.
- Model architecture changes require approval from the ML lead.
- Infrastructure changes require approval from both ML lead and SRE.
- Data pipeline changes require data engineering review.
- Experiment results require peer review before being used for production decisions.

### ML-Specific Review Checklist

**Code Quality**

- [ ] Code follows project style guide (linting passes).
- [ ] Type hints are present on all function signatures.
- [ ] Docstrings are present on all public functions.
- [ ] Error handling is appropriate.
- [ ] No hardcoded paths, credentials, or magic numbers.

**ML-Specific**

- [ ] Random seeds are fixed for reproducibility.
- [ ] Data splitting methodology is documented.
- [ ] Evaluation metrics are correctly computed.
- [ ] Baseline comparison is provided.
- [ ] Feature engineering logic is documented.
- [ ] Model configuration is externalized (not hardcoded).

**Infrastructure**

- [ ] Resource requirements are specified (CPU, memory, GPU).
- [ ] Scaling behavior is documented.
- [ ] Monitoring and alerting are configured.
- [ ] Security implications are considered.
- [ ] Cost impact is estimated.

**Data**

- [ ] Data schema is validated.
- [ ] Data quality checks are in place.
- [ ] PII handling complies with privacy policies.
- [ ] Data versioning is documented.

## ML-Specific Considerations

### Model Files and Artifacts

- Do not commit large model files (>100MB) to Git.
- Use Git LFS (Large File Storage) for model files under 100MB.
- Use DVC (Data Version Control) for larger model files and datasets.
- Store model artifacts in cloud storage (S3, GCS) and reference by version in Git.

**Git LFS Configuration**:

- Track: `*.onnx`, `*.pt`, `*.pth`, `*.pb`, `*.h5`, `*.joblib`, `*.pkl` (small configs only).
- Do not track: training data, large feature stores, raw datasets.
- LFS bandwidth: Plan for adequate LFS storage and bandwidth on your hosting platform.

### Data Version Control (DVC)

DVC provides Git-like version control for large files and datasets.

**DVC Workflow**:

1. `dvc init` — Initialize DVC in the repository.
2. `dvc add data/training.csv` — Track a large file with DVC.
3. `git add data/training.csv.dvc .gitignore` — Commit the DVC pointer file to Git.
4. `dvc push` — Push the actual file to remote storage (S3, GCS).
5. `dvc pull` — Pull the file from remote storage.
6. `dvc checkout` — Switch to the file version tracked by the current Git commit.

**DVC Integration with Git**:

- DVC pointer files (`.dvc`) are committed to Git; actual data files are stored in remote storage.
- `dvc.yaml` defines pipelines (training, evaluation) as DAGs.
- `dvc.lock` records the exact state of pipeline stages and their dependencies.
- `dvc plots` visualizes experiment metrics and learning curves.

### Experiment Configurations

- Store all experiment configurations in YAML or JSON files.
- Track configuration changes alongside code changes.
- Use experiment tracking tools (MLflow, W&B) with Git commit SHA tagging.
- Never modify experiment configurations after the experiment completes.

**Configuration Hierarchy**:

```
configs/
├── defaults.yaml          # Default hyperparameters
├── models/
│   ├── collaborative_filtering.yaml
│   ├── deep_learning.yaml
│   └── hybrid.yaml
├── experiments/
│   ├── exp_001_baseline.yaml
│   ├── exp_002_tuned.yaml
│   └── exp_003_new_features.yaml
└── environments/
    ├── dev.yaml
    ├── staging.yaml
    └── production.yaml
```

### Configuration Management

- Use hierarchical configuration with inheritance (base → environment → experiment).
- Validate configuration schemas using tools like `pydantic`, `marshmallow`, or `jsonschema`.
- Version-control all configuration files.
- Store secrets (API keys, database credentials) in a secrets manager, not in Git.
- Log configuration alongside experiment results for reproducibility.

## Release Management

### Model Release Process

1. **Experiment Approval**: Review experiment results and approve for production.
2. **Code Freeze**: Freeze the experiment branch; no further changes allowed.
3. **Release Branch**: Create `release/v{model_version}` from the approved branch.
4. **Integration Testing**: Run full integration test suite against the release branch.
5. **Model Validation**: Validate model performance against production baseline.
6. **Staging Deployment**: Deploy to staging and run smoke tests.
7. **Approval Gate**: Obtain ML lead and SRE approval for production deployment.
8. **Production Deployment**: Deploy using canary rollout strategy.
9. **Tag and Archive**: Tag the release, archive the model artifact, update registry.

### Version Numbering for Models

```
v{MAJOR}.{MINOR}.{PATCH}
```

- **MAJOR**: Breaking changes in model input/output schema, training data, or serving infrastructure.
- **MINOR**: New model version with improved performance, compatible API.
- **PATCH**: Configuration changes, dependency updates, bug fixes.

### Release Notes Template

```markdown
## Model Release v{version}

### Summary
- Brief description of changes

### Performance
- Offline metrics: NDCG@10: {value} (delta: {change})
- Expected online impact: {description}

### Changes
- Code changes list
- Data changes list
- Configuration changes list

### Rollback Plan
- Steps to rollback if issues are detected

### Monitoring
- Key metrics to watch post-deployment
```

## Branch Protection Rules

### Main Branch Protection

- Require pull request reviews before merging.
- Require status checks (lint, test, build) to pass.
- Require branches to be up to date before merging.
- Require signed commits for audit trail.
- Disallow force pushes and branch deletion.
- Require linear history (no merge commits) or allow merge commits based on team preference.

### Develop Branch Protection

- Require pull request reviews (at least 1 approval).
- Require CI checks to pass.
- Allow force pushes only by authorized personnel.
- Auto-delete branches after merge.

### Experiment Branch Guidelines

- Name convention: `experiment/{descriptive-name}-{ticket-id}`.
- Maximum lifetime: 2 weeks (longer experiments need justification).
- Document experiment hypothesis in the PR description.
- Include experiment results summary before merging.
- Squash merge to keep history clean.
