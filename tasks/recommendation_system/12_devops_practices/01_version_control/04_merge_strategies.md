# Merge Strategies

## Overview

Merge strategies determine how changes from feature branches are integrated into the main branch. For recommendation system projects, the choice of merge strategy affects history readability, commit traceability, and the ability to roll back changes. Additionally, ML projects require special tools (DVC, Git LFS) for managing large files like model weights and training datasets.

## Merge Commit vs Squash Merge vs Rebase

### Merge Commit

```bash
git merge --no-ff feature/branch
```

Creates a merge commit that preserves the complete history of the feature branch.

**History:**
```
* Merge branch 'feature/model-v2'
|\
| * Add deep ranking model
| * Add attention layer
| * Add user embedding
|/
* Previous commit on main
```

**Pros:** Complete history, preserves context, easy to revert
**Cons:** Cluttered graph, many merge commits

### Squash Merge

```bash
git merge --squash feature/branch
git commit -m "Add deep ranking model (#123)"
```

Combines all feature branch commits into a single commit on the target branch.

**History:**
```
* Add deep ranking model (#123)
* Previous commit on main
```

**Pros:** Clean linear history, easy to understand, single atomic commit
**Cons:** Loses individual commit history, harder to bisect

### Rebase

```bash
git rebase main
git checkout main
git merge feature/branch  # fast-forward
```

Replays feature branch commits on top of the target branch, creating linear history.

**History:**
```
* Add user embedding
* Add attention layer
* Add deep ranking model
* Previous commit on main
```

**Pros:** Clean linear history, preserves individual commits
**Cons:** Rewrites history, dangerous for shared branches

### Strategy Comparison

| Aspect | Merge Commit | Squash Merge | Rebase |
|--------|-------------|-------------|--------|
| History | Complete graph | Single commit | Linear |
| Commit preservation | All commits | Squashed | All commits |
| Revert ease | Easy (revert merge commit) | Easy (revert single commit) | Hard (multiple commits) |
| Collaboration safety | Safe | Safe | Unsafe for shared branches |
| Code review | Full diff visible | Clean single diff | Full diff visible |
| Bisectability | Good | Single commit (can't bisect) | Good |
| Best for | Release branches, hotfixes | Feature branches | Local cleanup |

### Recommended Strategy per Branch Type

| Branch Type | Strategy | Reason |
|-------------|----------|--------|
| Feature → develop | Squash merge | Clean history, atomic changes |
| Feature → main | Squash merge | Clean release history |
| Release → main | Merge commit | Preserve release context |
| Hotfix → main | Merge commit | Preserve hotfix context |
| Hotfix → develop | Merge commit | Track hotfix in develop |
| Local cleanup | Rebase | Before pushing, never on shared |

## DVC (Data Version Control) for Data Files

### Why DVC

Git cannot handle large files (GBs of training data, model weights) efficiently. DVC extends Git to track large files, datasets, and models without bloating the repository.

### Core Concepts

| Concept | Description |
|---------|-------------|
| **DVC files** | Small pointer files in Git that reference large files in remote storage |
| **Remote storage** | S3, GCS, Azure Blob, or local storage for large files |
| **Pipeline** | DVC tracks ML pipelines (data processing → training → evaluation) |
| **Metrics** | DVC tracks experiment metrics alongside code |

### DVC Workflow

```bash
# Initialize DVC in a Git repo
dvc init

# Track a large file
dvc add data/training_data.parquet
git add data/training_data.parquet.dvc .gitignore

# Configure remote storage
dvc remote add -d myremote s3://my-bucket/dvc-storage

# Push data to remote
dvc push

# Pull data from remote
dvc pull

# Track a pipeline stage
dvc run -n train \
  -d data/training_data.parquet \
  -d src/train.py \
  -o models/model.pkl \
  -M metrics.json \
  python src/train.py

# Reproduce the pipeline
dvc repro

# Compare experiments
dvc experiments show
```

### DVC for Model Artifacts

```
# Track model with DVC
dvc add models/production_model_v2.pkl
git add models/production_model_v2.pkl.dvc

# Model registry via Git tags
git tag -a v2.3.0 -m "Release model v2.3.0"
git push origin v2.3.0
dvc push
```

### DVC Best Practices

| Practice | Description |
|----------|-------------|
| **Track data schemas** | Use DVC + Great Expectations for schema validation |
| **Version datasets** | Each dataset version tracked separately |
| **Pin dependencies** | Use `dvc.lock` for deterministic pipelines |
| **Cache management** | Set up `.dvc/cache` with proper retention policy |
| **Remote backups** | Configure multiple remotes for disaster recovery |
| **Metrics comparison** | Use `dvc experiments compare` for model selection |

## DVC for Model Artifacts

### Model Versioning Strategy

```
models/
├── production/
│   ├── model.pkl.dvc       # DVC pointer to current production model
│   └── metadata.json       # Model metadata (version, date, metrics)
├── staging/
│   ├── model.pkl.dvc       # DVC pointer to staging model
│   └── metadata.json
└── experiments/
    ├── exp_001/
    │   ├── model.pkl.dvc
    │   └── metrics.json
    └── exp_002/
        ├── model.pkl.dvc
        └── metrics.json
```

### Model Lifecycle with DVC

```
1. Development: Train model locally, track with DVC
   dvc add models/experiments/exp_001/model.pkl

2. Experiment tracking: Log metrics alongside code
   dvc experiments run -S train.lr=0.001

3. Promotion: Move from experiments to staging
   cp models/experiments/exp_001/model.pkl models/staging/model.pkl
   dvc add models/staging/model.pkl

4. Validation: Run full evaluation on staging model
   dvc repro -s evaluate_staging

5. Production: Move from staging to production
   cp models/staging/model.pkl models/production/model.pkl
   dvc add models/production/model.pkl

6. Tagging: Tag the release
   git tag -a model-v2.3.0 -m "Production model v2.3.0"
```

## Git LFS for Large Files

### When to Use Git LFS

| File Type | Size | Use LFS? | Alternative |
|-----------|------|---------|------------|
| Model weights (.pt, .h5, .pkl) | > 100MB | Yes | DVC |
| Training datasets | > 1GB | No | DVC |
| Config files | < 1MB | No | Git |
| Notebooks | < 10MB | No | Git |
| Docker images | > 500MB | No | Container registry |
| Evaluation reports | < 5MB | No | Git |

### Git LFS Setup

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.h5"
git lfs track "*.pt"
git lfs track "*.onnx"

# Verify tracking
git lfs track

# Push LFS files
git lfs push --all origin
```

### LFS vs DVC

| Aspect | Git LFS | DVC |
|--------|---------|-----|
| **Purpose** | Version control for large files | ML pipeline + data versioning |
| **Storage** | Git-compatible (any Git host) | Separate remote (S3, GCS) |
| **Pipeline tracking** | No | Yes |
| **Experiment tracking** | No | Yes |
| **Metrics tracking** | No | Yes |
| **Collaboration** | Standard Git workflow | DVC + Git workflow |
| **Best for** | Binary assets in repos | End-to-end ML workflow |

**Recommendation**: Use DVC for training data and model artifacts. Use Git LFS for other large binary assets (pre-trained embeddings, static assets).

## .gitignore for ML Artifacts

### Essential .gitignore Entries

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
dist/
build/
*.egg
.eggs/

# Virtual environments
venv/
.venv/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Jupyter
.ipynb_checkpoints/

# Data files (tracked by DVC)
*.parquet
*.csv
*.h5
*.hdf5
data/raw/
data/interim/
data/processed/

# Model files (tracked by DVC or LFS)
models/*.pkl
models/*.pt
models/*.onnx
models/*.h5
models/*.pb
*.joblib

# Training artifacts
logs/
runs/
wandb/
mlruns/
lightning_logs/

# DVC
.dvc/config.local

# Environment
.env
.env.local
*.env

# OS
.DS_Store
Thumbs.db

# Temporary files
tmp/
temp/
*.tmp
```

### .dvcignore

```
# DVC equivalent of .gitignore
data/raw/
data/temp/
*.log
tmp/
```

### Pre-commit Hooks for ML

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=100']  # Prevent committing files > 100KB without LFS

  - repo: https://github.com/psf/black
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    hooks:
      - id: mypy
```
