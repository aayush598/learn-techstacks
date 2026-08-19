# Experiment Management for Recommendation Systems

## Overview

Effective experiment management is the organizational backbone of machine learning teams. Without systematic naming, tagging, and comparison, teams lose institutional knowledge, repeat failed experiments, and struggle to build on previous work. This document covers naming conventions, organization strategies, comparison tools, lineage tracking, and collaborative features for ML experiments.

---

## Naming Conventions

### Experiment Naming Structure

```
[team]_[project]_[model_type]_[variant]_[date]_[run_id]
```

**Example**: `rec_dnn_mlp_depth_search_20260815_0042`

### Naming Components

| Component | Purpose | Example Values |
|-----------|---------|----------------|
| Team | Ownership clarity | `rec`, `ads`, `feed` |
| Project | Business context | `homefeed`, `search`, `similar` |
| Model type | Architecture family | `dnn`, `transformer`, `gnn` |
| Variant | What's being tested | `depth3`, `lr1e-3`, `with_seq` |
| Date | Temporal ordering | `20260815` |
| Run ID | Uniqueness within day | `0042`, `abc123` |

### Hyperparameter Naming Conventions

- Use abbreviations consistently: `lr` (learning rate), `bs` (batch size), `wd` (weight decay)
- Separate values with underscores: `lr1e-3_bs256_wd1e-4`
- Use scientific notation for small values: `lr1e-3` not `lr0.001`
- Include key architecture params: `emb64_d3_h256` (embedding=64, depth=3, hidden=256)

### Anti-Patterns to Avoid

- Generic names: `experiment_1`, `model_v2`, `test_run`
- Missing information: `dnn_final` (what hyperparams? what data?)
- Inconsistent formatting: mix of `camelCase` and `snake_case`
- Name length > 80 characters (hard to read in dashboards)

---

## Experiment Organization

### Hierarchical Structure

```
Projects/
├── homefeed_recommendations/
│   ├── model_architecture/
│   │   ├── embedding_search/
│   │   ├── tower_comparison/
│   │   └── attention_variants/
│   ├── hyperparameter_tuning/
│   │   ├── learning_rate_sweep/
│   │   ├── regularization_search/
│   │   └── batch_size_study/
│   ├── feature_engineering/
│   │   ├── new_features/
│   │   └── feature_selection/
│   └── data_experiments/
│       ├── negative_sampling/
│       └── training_window/
├── search_recommendations/
└── similar_items/
```

### Experiment States

| State | Description | Indicators |
|-------|-------------|-----------|
| Created | Initialized but not started | Config saved, no metrics |
| Running | Actively training | Live metrics updating |
| Completed | Training finished | Final metrics available |
| Failed | Error during training | Error logs, partial metrics |
| Archived | No longer relevant | Moved to archive, read-only |
| Promoted | Selected for further analysis | Tagged, linked to production |

### Workspace Organization

- Separate workspaces per major project (homefeed, search, similar)
- Shared workspace for cross-project work (embeddings, features)
- Archive workspace for completed experiments (read-only, searchable)
- Sandbox workspace for exploratory/throwaway experiments

---

## Tagging and Metadata

### Standard Tags

| Tag Category | Example Tags |
|-------------|-------------|
| Priority | `priority:critical`, `priority:normal`, `priority:exploratory` |
| Status | `status:baseline`, `status:improvement`, `status:regression` |
| Hardware | `gpu:a100`, `gpu:h100`, `tpu:v4` |
| Data | `data:v2.1`, `data:30d`, `data:full` |
| Team ownership | `team:rec-eng`, `team:ml-infra` |
| Business context | `context:q3-launch`, `context:latency-fix` |

### Custom Metadata Fields

```json
{
  "model_type": "deepfm",
  "embedding_dim": 128,
  "num_features": 50000,
  "training_hours": 4.5,
  "gpu_count": 4,
  "dataset_version": "20260801",
  "baseline_comparison": "+1.2% NDCG@10",
  "serving_latency_ms": 12,
  "notes": "Tested wider MLP, marginal improvement"
}
```

### Tag Governance

- Enforce required tags via experiment creation pipeline
- Use controlled vocabularies for team-specific tags
- Regular tag audits to prevent tag proliferation
- Merge similar tags to maintain searchability

---

## Comparison Tools

### Metric Comparison Dashboard

Essential metrics for recommendation model comparison:

| Metric | Purpose | Target Direction |
|--------|---------|-----------------|
| NDCG@K | Ranking quality | Higher |
| Recall@K | Coverage of relevant items | Higher |
| AUC | Discrimination ability | Higher |
| Log-loss | Calibration quality | Lower |
| Coverage | Catalog diversity | Higher |
| Novelty | Discovery of new items | Higher |
| Fairness metrics | Equity across groups | Balanced |
| Inference latency | Serving efficiency | Lower |
| Model size | Deployment cost | Lower |

### Statistical Comparison

- Report mean ± standard deviation across multiple seeds
- Use paired t-test or Wilcoxon signed-rank test for significance
- Compute effect sizes (Cohen's d) to assess practical significance
- Apply Bonferroni correction for multiple comparison scenarios

### Visualization

- **Parallel coordinates plot**: Compare multiple hyperparameters and metrics simultaneously
- **Scatter plot matrix**: Identify correlations between metrics
- **Learning curves**: Compare convergence speed and final performance
- **Ablation charts**: Visualize contribution of individual components

---

## Experiment Lineage

### Dependency Tracking

Record the full provenance of each experiment:

```
data_source → preprocessing → feature_engineering → model_training → evaluation → deployment
```

### Lineage Metadata

| Stage | Key Information |
|-------|----------------|
| Data | Dataset version, sampling strategy, time window |
| Preprocessing | Feature transforms, normalization params, encoders |
| Features | Feature list, feature groups, feature interactions |
| Training | Architecture, hyperparams, optimizer, schedule |
| Evaluation | Test set, metrics, comparison baseline |
| Deployment | Serving config, A/B test parameters, rollout plan |

### Git Integration

- Link experiments to specific git commits
- Store model code and config as experiment artifacts
- Track code changes between experiments
- Enable reproduction: checkout commit + restore config → reproduce experiment

---

## Collaborative Features

### Experiment Sharing

- Shared experiment dashboards visible to entire team
- Comment threads on experiments for discussion
- @mention team members for review of key experiments
- Export experiment reports as PDF/HTML for stakeholders

### Review Workflows

1. **Peer review**: Team member reviews experiment design before training
2. **Result review**: Team reviews metrics after completion
3. **Decision record**: Document why a model was/wasn't selected
4. **Knowledge capture**: What was learned, what to try next

### Best Practices for Collaboration

- Always write experiment notes (what you're testing and why)
- Tag experiments with your name for accountability
- Share negative results (failed experiments are informative)
- Maintain a "lab notebook" of key decisions and learnings
- Schedule regular experiment review meetings with the team

---

## Experiment Management Tools

### Open-Source Options

| Tool | Key Features | Best For |
|------|-------------|----------|
| MLflow | Experiment tracking, model registry, deployment | General ML teams |
| Weights & Biases | Visualization, collaboration, sweeps | Research-oriented teams |
| Neptune.ai | Metadata store, comparison, dashboards | Enterprise teams |
| Comet ML | Experiment tracking, optimization | Production ML |

### Custom Implementation

For large-scale recommendation systems, many teams build custom solutions:
- Experiment database with structured schema
- Dashboard built on internal metrics infrastructure
- Integration with internal training pipeline
- Custom comparison and analysis tools

### Integration Points

- **Training pipeline**: Automatic experiment creation on job start
- **CI/CD**: Experiment results feed into deployment decisions
- **Monitoring**: Production metrics linked back to training experiments
- **Communication**: Slack/Teams notifications for experiment completion
