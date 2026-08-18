# MLflow for Experiment Tracking

## Overview

MLflow is an open-source platform for managing the machine learning lifecycle, encompassing experiment tracking, model packaging, model registry, and deployment. For recommendation systems with dozens of model variants, hyperparameter combinations, and evaluation metrics, MLflow provides the infrastructure to maintain reproducibility, facilitate collaboration, and streamline the path from experimentation to production.

---

## Experiment Organization

### Concepts

| Concept | Description | Analogy |
|---------|-------------|---------|
| Experiment | A named collection of related runs | Research project |
| Run | A single execution of a training script | Lab notebook entry |
| Parameter | Input configuration (hyperparameters, settings) | Input variables |
| Metric | Output measurements (loss, NDCG, latency) | Results |
| Artifact | Output files (model weights, plots, data) | Lab artifacts |
| Tag | Key-value metadata on runs | Labels |

### Experiment Structure for Recommendations

```
Experiment: "ranking_model_v3"
├── Run: "deepfm_lr0.001_emb256_neg10"
│   ├── Params: {lr: 0.001, embedding_dim: 256, neg_samples: 10, ...}
│   ├── Metrics: {ndcg@10: 0.42, hr@20: 0.67, loss: 0.31}
│   └── Artifacts: model_weights/, eval_plots/, feature_importance/
├── Run: "deepfm_lr0.0005_emb128_neg20"
│   ├── Params: {lr: 0.0005, embedding_dim: 128, neg_samples: 20, ...}
│   ├── Metrics: {ndcg@10: 0.41, hr@20: 0.65, loss: 0.33}
│   └── Artifacts: model_weights/, eval_plots/
└── Run: "transformer_lr0.0001_heads4_layers3"
    ├── Params: {lr: 0.0001, num_heads: 4, num_layers: 3, ...}
    ├── Metrics: {ndcg@10: 0.45, hr@20: 0.71, loss: 0.28}
    └── Artifacts: model_weights/, attention_weights/, eval_plots/
```

### Naming Conventions

- **Experiments**: `{project}_{model_type}_{version}` (e.g., `ranking_deepfm_v3`)
- **Runs**: `{config_hash}_{timestamp}` or descriptive names
- **Metrics**: Use consistent naming (e.g., `train/loss`, `val/ndcg@10`, `test/hr@20`)
- **Tags**: `mlflow.runName`, `model.type`, `dataset.version`, `team`

---

## Parameter Logging

### What to Log

| Category | Parameters | Why |
|----------|-----------|-----|
| Model architecture | Layers, dimensions, activations | Reproduce model structure |
| Training config | Learning rate, optimizer, batch size | Reproduce training dynamics |
| Data config | Dataset version, sampling strategy, preprocessing | Reproduce input data |
| Feature config | Feature set version, embedding sizes, feature crosses | Reproduce feature engineering |
| Evaluation config | Test set, metrics computed, threshold values | Reproduce evaluation |

### Logging Patterns

```python
import mlflow

# Log individual parameters
mlflow.log_param("learning_rate", 0.001)
mlflow.log_param("embedding_dim", 256)
mlflow.log_param("num_layers", 3)

# Log multiple parameters at once
mlflow.log_params({
    "model.type": "deepfm",
    "optimizer": "adam",
    "weight_decay": 1e-5,
    "negative_sampling_ratio": 10,
    "sequence_length": 50,
    "dropout_rate": 0.2,
})

# Log nested parameters (flattened automatically)
config = {
    "model": {"type": "deepfm", "embedding_dim": 256},
    "training": {"lr": 0.001, "epochs": 100}
}
mlflow.log_params(flatten_dict(config))
```

### Best Practices

- **Log before training starts**: Parameters should be available even if training fails
- **Use consistent naming**: `snake_case` for parameter names
- **Log derived parameters**: Compute and log effective batch size, total parameters, etc.
- **Version your configs**: Log the config file path or hash as a parameter
- **Log negative results**: Failed experiments with parameters are still valuable

---

## Metric Tracking

### Training and Evaluation Metrics

```python
# Log single metrics
mlflow.log_metric("train_loss", 0.342, step=epoch)
mlflow.log_metric("val_ndcg@10", 0.423, step=epoch)

# Log multiple metrics at once
mlflow.log_metrics({
    "train_loss": 0.342,
    "val_loss": 0.381,
    "val_ndcg@5": 0.389,
    "val_ndcg@10": 0.423,
    "val_hr@10": 0.651,
    "val_mrr": 0.287,
    "val_coverage": 0.142,
    "val_diversity": 0.734,
}, step=epoch)
```

### Metric Naming Convention

| Metric | Format | Example |
|--------|--------|---------|
| Training loss | `train/loss` | 0.342 |
| Validation metrics | `val/{metric}@{k}` | `val/ndcg@10` |
| Test metrics | `test/{metric}@{k}` | `test/hr@20` |
| System metrics | `system/{metric}` | `system/gpu_utilization` |
| Latency | `serving/{metric}` | `serving/p99_latency_ms` |

### Custom Metrics

For recommendation-specific metrics, log custom implementations:

```python
def compute_ndcg_at_k(recommendations, ground_truth, k=10):
    # Custom NDCG computation
    ...

# Log custom metric
ndcg = compute_ndcg_at_k(recs, gt, k=10)
mlflow.log_metric("val/custom_ndcg@10", ndcg)
```

### Metric Visualization

MLflow automatically provides:
- **Metric history**: Line plots of metrics over steps
- **Comparison views**: Side-by-side comparison of runs
- **Parallel coordinate plots**: Multi-parameter metric relationships
- **Contour plots**: Metric landscape over two parameters

---

## Artifact Management

### Types of Artifacts

| Artifact | Description | Storage |
|----------|-------------|---------|
| Model weights | Trained model parameters | S3/GCS/HDFS |
| ONNX model | Exported model for serving | S3/GCS/HDFS |
| Evaluation plots | ROC curves, calibration plots | S3/GCS/HDFS |
| Feature importance | SHAP values, permutation importance | S3/GCS/HDFS |
| Training logs | Console output, tensorboard logs | S3/GCS/HDFS |
| Data samples | Sample datasets for debugging | S3/GCS/HDFS |
| Config files | Full training configuration | S3/GCS/HDFS |

### Logging Artifacts

```python
# Log a single file
mlflow.log_artifact("model.onnx")

# Log a directory
mlflow.log_artifacts("output/")

# Log artifact with a specific path
mlflow.log_artifact("plot.png", artifact_path="eval_plots")

# Log model (native MLflow format)
mlflow.pytorch.log_model(model, "model")
mlflow.sklearn.log_model(model, "model")
```

### Artifact Organization

```
Run artifacts/
├── model/
│   ├── mlflow-model/     (MLflow model format)
│   ├── model.onnx        (ONNX export)
│   └── model.pt          (PyTorch checkpoint)
├── eval_plots/
│   ├── ndcg_curve.png
│   ├── calibration_plot.png
│   └── coverage_analysis.png
├── feature_analysis/
│   ├── feature_importance.csv
│   ├── shap_summary.png
│   └── embedding_clusters.png
└── configs/
    ├── training_config.yaml
    └── feature_config.yaml
```

---

## Model Registry

### Model Lifecycle

```
None → Registered Model → Version 1 (stage: None)
                                    ↓
                              Stage: Staging
                                    ↓
                              Stage: Production
                                    ↓
                              Stage: Archived
```

### Registration

```python
# Register model during logging
mlflow.pytorch.log_model(
    model, 
    "model",
    registered_model_name="ranking_deepfm_v3"
)

# Or register after the fact
result = mlflow.register_model(
    "runs:/<run_id>/model",
    "ranking_deepfm_v3"
)
```

### Stage Transitions

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Transition to staging
client.transition_model_version_stage(
    name="ranking_deepfm_v3",
    version=3,
    stage="Staging"
)

# Transition to production
client.transition_model_version_stage(
    name="ranking_deepfm_v3",
    version=3,
    stage="Production"
)

# Add description
client.update_model_version(
    name="ranking_deepfm_v3",
    version=3,
    description="DeepFM with INT8 quantization, 0.3ms P99 latency"
)
```

### Model Version Annotations

```python
# Add tags to model versions
client.set_model_version_tag(
    name="ranking_deepfm_v3",
    version=3,
    key="validated_by",
    value="team_leads"
)

client.set_model_version_tag(
    name="ranking_deepfm_v3",
    version=3,
    key="ab_test_result",
    value="positive_ndcg_2pct"
)
```

---

## Reproducibility

### Ensuring Reproducible Runs

| Component | How to Reproduce | What to Log |
|-----------|-----------------|-------------|
| Random seeds | Set all RNG seeds | `seed`, `torch.manual_seed`, `np.random.seed` |
| Data version | Pin dataset version | `dataset.version`, `data.hash` |
| Code version | Git commit hash | `mlflow.log_param("git_commit", commit_hash)` |
| Environment | Conda/pip freeze | `mlflow.log_artifact("requirements.txt")` |
| Library versions | Log versions | `torch.__version__`, `transformers.__version__` |
| Hardware | Log GPU type, driver | `system.gpu_type`, `system.gpu_count` |

### Environment Capturing

```python
import mlflow

# Log the entire conda environment
mlflow.mlflow.log_artifacts(mlflow.get_artifacts_uri())

# Or log just requirements
import subprocess
subprocess.run(["pip", "freeze"], stdout=open("requirements.txt", "w"))
mlflow.log_artifact("requirements.txt")

# Log the conda environment
mlflow.sklearn.log_model(model, "model", conda_env=conda_env)
```

### Replay Experiments

```python
# Load parameters from a previous run
client = MlflowClient()
run = client.get_run("<run_id>")
params = run.data.params

# Use params to reproduce the experiment
for key, value in params.items():
    config[key] = cast_to_original_type(value)
```

---

## Collaboration Features

### Team Organization

```
MLflow Server (shared backend)
├── Experiment: "ranking_team_alpha"
│   ├── Run by Alice
│   ├── Run by Bob
│   └── Run by Charlie
├── Experiment: "ranking_team_beta"
│   ├── Run by Dave
│   └── Run by Eve
└── Model Registry
    ├── ranking_deepfm_v3 (Production)
    ├── ranking_transformer_v1 (Staging)
    └── ranking_widedeep_v2 (Archived)
```

### Sharing and Comparison

- **Compare runs**: Select multiple runs for side-by-side comparison
- **Filter by tags**: Filter runs by team member, model type, dataset
- **Comment on runs**: Add notes about observations or decisions
- **Share experiment links**: Share URLs to specific runs or comparisons

### Review Workflow

```
Developer pushes training code
      ↓
CI triggers training run with MLflow tracking
      ↓
MLflow logs all params, metrics, artifacts
      ↓
Reviewer checks MLflow dashboard for results
      ↓
If approved → Register model in Model Registry
      ↓
Transition to Staging → Run integration tests
      ↓
Transition to Production → Deploy to serving
```

---

## MLflow Deployment Patterns

### Backend Configuration

| Backend | Storage | Best For |
|---------|---------|----------|
| Local file | `mlruns/` directory | Individual development |
| SQLite | `sqlite:///mlflow.db` | Small team |
| PostgreSQL | `postgresql://...` | Production deployment |
| MySQL | `mysql://...` | Production deployment |

### Artifact Storage

| Store | Configuration | Best For |
|-------|--------------|----------|
| Local | `file:///path/to/artifacts` | Development |
| S3 | `s3://bucket/path` | AWS production |
| GCS | `gs://bucket/path` | GCP production |
| Azure Blob | `wasbs://container@account` | Azure production |

### Integration with Training Infrastructure

```
Training Job (Spark/Kubernetes/Airflow)
      ↓
MLflow.start_run()
      ↓
Training Loop with mlflow.log_* calls
      ↓
MLflow.end_run()
      ↓
MLflow Server (stores to backend DB + artifact store)
      ↓
MLflow UI / API for querying results
      ↓
Model Registry → Serving Infrastructure
```

---

## Best Practices

### Organization

1. **One experiment per model family**: Don't mix DeepFM and Transformer runs
2. **Consistent naming**: Establish team conventions for parameter and metric names
3. **Tag extensively**: Use tags for filtering (team, status, dataset version)
4. **Archive old experiments**: Don't delete; archive for historical reference

### Workflow

1. **Log early, log often**: Start logging before training begins
2. **Log failures**: Failed runs with parameters are valuable learning
3. **Review before production**: Require human review of metrics before model promotion
4. **Document decisions**: Use run descriptions to explain why certain parameters were chosen

### Performance

1. **Batch metric logging**: Log metrics every N steps, not every step
2. **Compress artifacts**: Zip large files before logging
3. **Use remote artifact store**: Don't store large artifacts on the MLflow server
4. **Database connection pooling**: Use connection pooling for high-concurrency environments
