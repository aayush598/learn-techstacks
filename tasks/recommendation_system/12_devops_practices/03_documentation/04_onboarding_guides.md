# Onboarding Guides

## Overview

Effective onboarding accelerates new team member productivity and ensures consistent knowledge transfer. For ML recommendation system teams, onboarding must cover not only standard software engineering practices but also ML-specific workflows: data access, model training pipelines, experiment tracking, and evaluation methodologies. A well-structured onboarding program reduces the time-to-first-contribution from weeks to days.

## Onboarding Checklist

### Pre-Start (Before Day 1)

| Task | Owner | Status |
|------|-------|--------|
| Laptop ordered and configured | IT | ☐ |
| GitHub/GitLab access granted | Engineering Manager | ☐ |
| Cloud account provisioned (AWS/GCP) | Platform Team | ☐ |
| VPN access configured | IT | ☐ |
| Slack/communication channels added | Team Lead | ☐ |
| Calendar invites for onboarding meetings | Team Lead | ☐ |
| Reading materials shared | Buddy | ☐ |

### Week 1: Foundation

| Day | Activity | Duration | Owner |
|-----|----------|----------|-------|
| **Day 1** | Welcome, team introductions, office tour | 2 hours | Manager |
| **Day 1** | Development environment setup | 3 hours | Buddy |
| **Day 1** | Access verification (all tools, repos, dashboards) | 1 hour | Buddy |
| **Day 2** | Architecture overview presentation | 2 hours | Tech Lead |
| **Day 2** | Codebase walkthrough (key modules) | 3 hours | Buddy |
| **Day 3** | ML pipeline walkthrough (data → training → serving) | 3 hours | ML Engineer |
| **Day 3** | Read key documentation (API docs, runbooks) | 2 hours | Self |
| **Day 4** | First "hello world" run (local training) | 3 hours | Buddy |
| **Day 4** | Observation of on-call process | 1 hour | On-call Engineer |
| **Day 5** | First small task (bug fix or documentation) | 4 hours | Self |
| **Day 5** | Week 1 retrospective with manager | 1 hour | Manager |

### Week 2: Integration

| Day | Activity | Duration | Owner |
|-----|----------|----------|-------|
| **Day 6–7** | Complete first PR (with review) | Full days | Self + Reviewer |
| **Day 8** | Shadow experiment review meeting | 2 hours | ML Lead |
| **Day 8** | Understand evaluation methodology | 3 hours | Research Scientist |
| **Day 9** | Walk through monitoring dashboards | 2 hours | SRE |
| **Day 9** | Complete first experiment run (reproduce existing) | 3 hours | Self |
| **Day 10** | Week 2 retrospective | 1 hour | Manager |

### Week 3–4: Independence

| Activity | Duration | Owner |
|----------|----------|-------|
| Own first feature/bug (small scope) | Full week | Self |
| Participate in code review (review others' PRs) | Ongoing | Self |
| Attend experiment review and contribute | 1 hour/week | Self |
| Complete first on-call shadow | 1 day | Self + On-call |
| End of month check-in with manager | 1 hour | Manager |

## Development Environment Setup

### Required Tools

| Tool | Purpose | Setup Command |
|------|---------|--------------|
| **Python 3.11+** | Primary language | `pyenv install 3.11` |
| **Poetry** | Dependency management | `curl -sSL https://install.python-poetry.org \| bash` |
| **Git** | Version control | Pre-installed or `brew install git` |
| **Docker** | Containerization | Install Docker Desktop |
| **kubectl** | Kubernetes management | `brew install kubectl` |
| **DVC** | Data versioning | `pip install dvc` |
| **VS Code** | IDE | `brew install --cask visual-studio-code` |
| **Postman** | API testing | `brew install --cask postman` |

### Environment Setup Script

```bash
#!/bin/bash
# setup-dev-environment.sh

# Clone the repository
git clone git@github.com:company/recsys-platform.git
cd recsys-platform

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install poetry
poetry install

# Install pre-commit hooks
pre-commit install

# Configure DVC remote
dvc remote add -d myremote s3://company-dvc-bucket/recsys
dvc pull

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials

# Run tests to verify setup
pytest tests/unit/ -v

# Verify type checking
mypy src/

# Verify linting
ruff check src/ tests/
```

### Docker Development Environment

```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - ENV=development
      - DATABASE_URL=postgresql://user:pass@db:5432/recsys
    depends_on:
      - db
      - redis
      - feature-store

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: recsys
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    ports:
      - "5432:5432"

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  feature-store:
    image: company/feature-store:latest
    ports:
      - "8080:8080"
```

## Architecture Overview for Newcomers

### System Architecture

```
User Request
    ↓
API Gateway (rate limiting, auth)
    ↓
Recommendation Service
    ├── Feature Store (real-time features)
    ├── Model Serving (inference)
    │   ├── Candidate Generation (retrieve ~1000 items)
    │   ├── Ranking (score ~100 items)
    │   └── Re-ranking (diversity, business rules)
    └── Response Assembly
    ↓
Response to User
```

### Key Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **API Gateway** | Kong/Nginx | Rate limiting, authentication, routing |
| **Recommendation Service** | Python/FastAPI | Business logic, orchestration |
| **Feature Store** | Redis + PostgreSQL | Real-time and batch feature serving |
| **Model Serving** | TorchServe/Triton | Model inference |
| **Training Pipeline** | Airflow/Kubeflow | Scheduled model training |
| **Experiment Tracking** | MLflow/W&B | Experiment logging and comparison |
| **Model Registry** | MLflow Model Registry | Model versioning and staging |
| **Monitoring** | Prometheus + Grafana | Metrics collection and visualization |
| **Alerting** | PagerDuty | Incident notification |

### Data Flow

```
1. Raw Data → Data Pipeline (Spark/Airflow)
2. Processed Data → Feature Store (batch features)
3. User Request → Feature Store (real-time features)
4. Features → Model Serving (prediction)
5. Predictions → Re-ranking (diversity, business rules)
6. Recommendations → API Response
7. User Interaction → Event Logging
8. Event Logging → Data Pipeline (feedback loop)
```

## Codebase Walkthrough

### Directory Structure

```
recsys-platform/
├── src/
│   ├── api/                 # API endpoints and request handling
│   ├── features/            # Feature computation and serving
│   ├── models/              # Model definitions and training
│   ├── serving/             # Model serving and inference
│   ├── evaluation/          # Evaluation metrics and pipelines
│   ├── data/                # Data processing and pipelines
│   └── utils/               # Shared utilities
├── tests/
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── e2e/                 # End-to-end tests
├── configs/                 # Configuration files
├── notebooks/               # Exploration and analysis notebooks
├── scripts/                 # Utility scripts
├── data/                    # Local data (DVC-tracked)
├── models/                  # Local model artifacts (DVC-tracked)
├── docker/                  # Docker configurations
├── terraform/               # Infrastructure as code
└── docs/                    # Documentation
```

### Key Files to Read First

| File | Purpose | Read Time |
|------|---------|----------|
| `README.md` | Project overview and setup | 10 min |
| `src/api/main.py` | API entry point | 15 min |
| `src/models/train.py` | Training pipeline | 30 min |
| `src/serving/predict.py` | Inference pipeline | 20 min |
| `src/features/feature_store.py` | Feature retrieval | 15 min |
| `configs/model_config.yaml` | Model configuration | 10 min |
| `tests/unit/test_model.py` | Testing patterns | 15 min |

## Key Contacts

| Role | Name | Responsibility | Contact |
|------|------|---------------|---------|
| **Engineering Manager** | [Name] | People management, priorities | Slack, Calendar |
| **Tech Lead** | [Name] | Architecture, technical decisions | Slack, Code Review |
| **ML Lead** | [Name] | Model strategy, research direction | Slack, Experiment Review |
| **SRE On-Call** | Rotation | Production incidents | PagerDuty |
| **Data Engineer** | [Name] | Data pipelines, feature store | Slack, Data Channel |
| **Platform Engineer** | [Name] | Infrastructure, CI/CD | Slack, Platform Channel |

## ML-Specific Onboarding

### Data Access

| Data Source | Access Method | Request Process |
|------------|--------------|-----------------|
| Training data (S3) | DVC pull | Automatic with repo access |
| Feature store (Redis) | VPN + credentials | Request via platform team |
| User events (Kafka) | Schema registry access | Request via data team |
| Production logs | Kibana/Grafana | Request via SRE |
| Experiment data | MLflow | Automatic with repo access |

### Model Training

```bash
# 1. Pull latest data
dvc pull

# 2. Run a training experiment
python -m src.models.train \
  --config configs/model_config.yaml \
  --experiment-name my-first-experiment

# 3. View results
mlflow ui  # Open http://localhost:5000

# 4. Compare with existing experiments
mlflow experiments compare --experiment-id 1
```

### Experiment Tracking

| Tool | Purpose | URL |
|------|---------|-----|
| **MLflow** | Experiment logging, model registry | http://mlflow.company.com |
| **Weights & Biases** | Visualization, collaboration | http://wandb.company.com |
| **Grafana** | Production metrics | http://grafana.company.com |
| **Kibana** | Log analysis | http://kibana.company.com |

### First Experiment Guide

```
1. Choose a baseline experiment to reproduce
2. Pull the data and configuration
3. Run the training script locally
4. Log results to MLflow
5. Compare your results with the original
6. If results match, you've verified your setup
7. If results differ, investigate (data version? config? code version?)
```

## First PR Plan

### Ideal First PR

| Criteria | Description |
|----------|-------------|
| **Scope** | Small (1–3 files changed) |
| **Risk** | Low (non-critical path) |
| **Learning** | Touches key parts of codebase |
| **Impact** | Visible but not critical |
| **Timeline** | Completable in 1–2 days |

### Good First PR Examples

1. **Fix a typo** in documentation
2. **Add a missing test** for an existing function
3. **Improve error message** for a common failure case
4. **Add logging** for a key operation
5. **Update dependencies** to latest compatible versions
6. **Refactor** a small piece of code for clarity

### PR Review Expectations

- Expect 1–3 rounds of review comments
- Don't take feedback personally—reviews are about code quality
- Ask questions if feedback is unclear
- Respond to all comments (even with "Done")
- Thank reviewers for their time
