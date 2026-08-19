# Apache Airflow for ML Pipelines

## Overview

Apache Airflow is a workflow orchestration platform for programmatically authoring, scheduling, and monitoring data pipelines. In a recommendation system, Airflow orchestrates the end-to-end ML lifecycle: data extraction, feature engineering, model training, evaluation, validation, deployment, and monitoring. Airflow's DAG-based execution model, rich operator ecosystem, and extensibility make it the de facto standard for ML pipeline orchestration at scale.

---

## DAG Design Principles

### Directed Acyclic Graphs

A DAG (Directed Acyclic Graph) in Airflow represents a pipeline as a set of tasks with defined dependencies. The DAG ensures tasks execute in the correct order and provides visibility into pipeline structure.

**Key DAG properties:**

| Property | Description | Recommendation |
|---|---|---|
| `dag_id` | Unique identifier | Use reverse domain naming: `recsys.feature.user_daily` |
| `schedule_interval` | Cron expression or timedelta | Match data freshness requirements |
| `start_date` | When the DAG begins executing | Use a fixed past date, not `datetime.now()` |
| `catchup` | Whether to backfill missed runs | Disable for real-time pipelines, enable for batch |
| `max_active_runs` | Concurrent DAG runs | 1 for sequential pipelines, N for parallel |
| `default_args` | Shared task arguments | Define retries, timeout, owner, email here |
| `tags` | Organizational tags | Use for filtering: `recsys`, `features`, `training` |

### Task Granularity

**Fine-grained tasks** (one operation per task):
- Easier to retry individual steps
- Better visibility in the Airflow UI
- More overhead from task scheduling
- Recommended for most ML pipelines

**Coarse-grained tasks** (multiple operations per task):
- Lower scheduling overhead
- Less granular retry and monitoring
- Simpler DAG structure
- Use only for tightly coupled operations

### Task Organization Patterns

**Layered architecture**: Organize tasks into layers that represent distinct pipeline stages:

```
Extract → Validate → Transform → Feature Engineering → Train → Evaluate → Deploy → Monitor
```

Each layer has clear inputs and outputs, enabling independent testing and debugging.

**Fan-out/Fan-in**: Common pattern in ML pipelines where a single task (e.g., feature extraction) fans out to multiple parallel tasks (e.g., compute different feature groups), which then fan in to a downstream task (e.g., model training).

**Branching**: Use `BranchPythonOperator` to create conditional paths in the pipeline. For example, skip model deployment if evaluation metrics don't meet thresholds.

---

## Task Dependencies

### Dependency Types

| Operator | Description | Use Case |
|---|---|---|
| `>>` | Forward dependency | `task_a >> task_b` (B runs after A) |
| `<<` | Backward dependency | `task_b << task_a` (equivalent to above) |
| `chain` | Sequential chain | `chain(t1, t2, t3)` (t1→t2→t3) |
| `chain_linear` | Linear with branching | Fan-out from a single task |
| `.depends_on()` | Named dependency | `task_b.depends_on(task_a)` |

### Cross-DAG Dependencies

- **ExternalTaskSensor**: Wait for a specific task in another DAG to complete. Useful when pipelines depend on upstream data availability.
- **TriggerDagRunOperator**: Launch another DAG and optionally wait for completion. Useful for modular pipeline design.
- **DAG inheritance**: Share common configuration across related DAGs using a base DAG factory function.

### Data Dependencies vs. Execution Dependencies

**Execution dependencies** control task ordering but don't pass data. Tasks communicate via XCom (Airflow's cross-communication mechanism) or external storage.

**Data dependencies** require that the output of one task is the input of another. In ML pipelines, this is typically managed by:
- **External storage**: S3/GCS paths with structured naming conventions (e.g., `s3://features/user/daily/{ds}/`)
- **Feature stores**: Write features to a feature store; downstream tasks read from it
- **Metadata databases**: Record run metadata (output paths, metrics, model versions) in a database

---

## Retry Logic

### Retry Configuration

| Parameter | Description | Recommended Value |
|---|---|---|
| `retries` | Number of retry attempts | 3 for transient failures, 0 for data quality failures |
| `retry_delay` | Time between retries | 5 minutes (allows upstream recovery) |
| `retry_exponential_backoff` | Exponential increase in retry delay | True for network-dependent tasks |
| `max_retry_delay` | Cap on retry delay | 30 minutes |
| `on_failure_callback` | Function called on final failure | Alert via Slack/PagerDuty |
| `on_retry_callback` | Function called on each retry | Log retry attempt for debugging |

### Retry Strategies by Task Type

| Task Type | Retry Strategy | Rationale |
|---|---|---|
| Data extraction (API calls) | 3 retries, exponential backoff | Transient network failures |
| Data extraction (database) | 2 retries, fixed delay | Possible lock contention |
| Feature computation | 3 retries, same parameters | Deterministic, safe to retry |
| Model training | 0 retries (long-running) | Fail fast, fix and re-trigger |
| Model evaluation | 1 retry | May fail due to data issues |
| Deployment | 0 retries, manual approval | Risk of incorrect deployment |

### Idempotent Retries

Every task must be idempotent—running it twice with the same input produces the same output. This is critical for safe retries:

- **Checkpoint writes**: Write to a temporary path, then atomically move to the final path.
- **Database writes**: Use `INSERT ... ON CONFLICT DO UPDATE` or equivalent upsert semantics.
- **Feature writes**: Use versioned writes where the latest version is determined by a timestamp or sequence number.

---

## SLA Management

### SLA Configuration

Airflow SLAs define the maximum expected time for a task or DAG to complete. If the SLA is breached, Airflow triggers an alert.

| Task | SLA | Alert Channel |
|---|---|---|
| Data extraction | 2 hours | Slack + PagerDuty |
| Feature engineering | 4 hours | Slack |
| Model training | 8 hours | Slack |
| Model evaluation | 1 hour | Slack |
| Full pipeline | 12 hours | PagerDuty |

### SLA Monitoring

- **SLA miss alerts**: Configure `sla_miss_callback` to send alerts when SLAs are breached.
- **SLA dashboards**: Use Airflow's built-in SLA tracking or export to external monitoring (Grafana, Datadog).
- **Historical SLA analysis**: Track SLA compliance over time to identify chronic bottlenecks and capacity constraints.

### SLA vs. Timeout

| Concept | Purpose | Consequence of Breach |
|---|---|---|
| **SLA** | Expected completion time | Alert, task continues |
| **execution_timeout** | Maximum allowed execution time | Task is killed |
| **dagrun_timeout** | Maximum DAG run duration | DAG run is killed |

Use SLAs for monitoring and alerting, timeouts for hard limits and resource protection.

---

## Sensor-Based Triggers

### Sensors

Sensors are operators that wait for an external condition to be true before allowing downstream tasks to execute. They are the primary mechanism for event-driven pipelines.

| Sensor | Condition | Poll Interval | Timeout |
|---|---|---|---|
| `S3KeySensor` | File exists at S3 path | 5 minutes | 1 hour |
| `ExternalTaskSensor` | Task in another DAG completes | 5 minutes | 4 hours |
| `HttpSensor` | HTTP endpoint returns 200 | 1 minute | 30 minutes |
| `SqlSensor` | SQL query returns rows | 5 minutes | 2 hours |
| `TimeSensor` | Clock reaches specified time | 1 minute | Until trigger time |
| `FileSensor` | File exists on local filesystem | 30 seconds | 30 minutes |

### Deferrable Operators

Deferrable operators (introduced in Airflow 2.2) replace sensor polling with event-driven triggers. Instead of continuously polling a condition, the operator releases its worker slot and resumes when the condition is met. This dramatically reduces resource consumption for long-waiting sensors.

**When to use deferrable operators:**
- S3 file arrival with long wait times
- External API callbacks (webhook-based triggers)
- Database change data capture (CDC) events
- Long-running Spark or Kubernetes jobs

### Trigger Strategies

- **Reschedule mode**: `mode='reschedule'` releases the worker slot between polls. Use for sensors with long poll intervals.
- **poke mode**: `mode='poke'` keeps the worker slot occupied. Use for sensors with short poll intervals (< 1 minute).
- **Soft fail**: `soft_fail=True` marks the sensor as skipped (not failed) on timeout. Use for optional dependencies.

---

## Dynamic DAGs

### DAG Generation Patterns

Dynamic DAGs are generated programmatically at parse time based on external configuration. This enables:

- **Configuration-driven pipelines**: Define pipeline structure in YAML/JSON. A single DAG factory generates multiple DAGs from configuration.
- **User-defined pipelines**: Allow data scientists to define feature pipelines in configuration without writing Python code.
- **Parameterized training**: Generate training DAGs for different model configurations, hyperparameters, or data subsets.

### Template-Driven DAGs

Use Jinja templates and Airflow's template engine to parameterize tasks:

- **Airflow Variables**: Store configuration values (feature lists, model hyperparameters, data paths) in Airflow Variables, accessible via `{{ var.value.key }}`.
- **Connection parameters**: Reference Airflow Connections for database credentials, API keys, and service endpoints.
- **Runtime parameters**: Pass parameters at DAG trigger time using `conf` dictionary.

### Multi-Run DAGs

Generate DAGs that process multiple entities in parallel:

- **Per-item training**: Generate a training DAG for each item category or model variant.
- **Per-user-group features**: Compute features separately for different user segments.
- **A/B test variants**: Deploy multiple model versions for online experimentation.

---

## KubernetesPodOperator for Isolated Execution

### Why KubernetesPodOperator

ML pipelines often require isolated environments with specific dependencies, resource limits, and execution contexts. The `KubernetesPodOperator` runs each task in an isolated Kubernetes pod, providing:

- **Dependency isolation**: Each task can use a different Docker image with specific library versions.
- **Resource control**: Set CPU, memory, GPU, and disk limits per task.
- **Security isolation**: Network policies, service accounts, and RBAC per task.
- **Failure isolation**: A task failure doesn't corrupt the shared environment.

### Configuration

| Parameter | Description | Example |
|---|---|---|
| `image` | Docker image for the task | `recsys/training:latest` |
| `image_pull_policy` | When to pull the image | `IfNotPresent` for stable, `Always` for latest |
| `namespace` | Kubernetes namespace | `ml-pipelines` |
| `service_account_name` | K8s service account | `airflow-worker` |
| `resources` | CPU/memory/GPU limits | `{"cpu": "4", "memory": "16Gi", "gpu": "1"}` |
| `volumes` | Mounted volumes | PVC for data, ConfigMap for configs |
| `env_vars` | Environment variables | Feature store connection strings |
| `node_selector` | Node placement | GPU nodes for training tasks |
| `tolerations` | Node tolerations | For GPU/preemptible node pools |

### Image Management

- **Base images**: Maintain a set of base images (training, inference, feature engineering) with common dependencies.
- **Versioned images**: Tag images with pipeline version or Git commit SHA for reproducibility.
- **Image pull secrets**: Store registry credentials as Kubernetes secrets, referenced by the service account.
- **Pre-pulled images**: Use DaemonSets or node image caching to reduce pod startup time.

### Resource Management

- **Request vs. limit**: Set resource requests for scheduling (guaranteed allocation) and limits for capping (enforced maximum). For training tasks, set requests close to limits to ensure stable performance.
- **GPU scheduling**: Use NVIDIA device plugin for GPU allocation. Set `nvidia.com/gpu: 1` in resources.
- **Ephemeral storage**: ML tasks may write large intermediate results. Set `ephemeral-storage` limits and use fast local SSDs.

---

## Data Quality Gates

### Quality Gate Pattern

Data quality gates are checkpoints in the pipeline that validate data before allowing downstream processing to proceed. A gate either passes (data meets quality criteria) or fails (triggers alert and optionally halts the pipeline).

### Quality Gate Implementation in Airflow

1. **Pre-execution gates**: Run quality checks before expensive computations (e.g., validate input data before training).
2. **Post-execution gates**: Validate outputs after each stage (e.g., check feature distributions after feature engineering).
3. **Cross-pipeline gates**: Ensure upstream pipelines have completed successfully before starting downstream work.

### Quality Metrics and Thresholds

| Metric | Threshold | Action on Failure |
|---|---|---|
| Row count change | < 20% deviation from expected | Alert, continue |
| Null rate per column | < 5% | Alert, continue |
| Feature distribution shift | KS test p-value > 0.01 | Alert, skip downstream |
| Schema match | 100% column match | Halt pipeline |
| Freshness | Data timestamp < 24 hours | Alert, continue |
| Uniqueness | Primary key uniqueness = 100% | Halt pipeline |

### Branching on Quality

Use `BranchPythonOperator` to create conditional pipeline paths based on quality gate results:

- **Pass**: Continue to the next pipeline stage.
- **Warn**: Continue but log warnings and send alerts.
- **Fail**: Halt the pipeline and trigger incident response.
- **Fallback**: Switch to a fallback data source or model version.

---

## Operational Best Practices

1. **Code versioning**: Store DAGs in Git with branch protection and code review. Use CI/CD to deploy DAGs to Airflow.
2. **Testing**: Write unit tests for task logic and integration tests for DAG structure. Use `TestDag` to validate DAG parsing.
3. **Monitoring**: Export Airflow metrics to Prometheus. Monitor DAG run duration, task failures, SLA misses, and pool usage.
4. **Secrets management**: Use Airflow's secrets backend (AWS Secrets Manager, HashiCorp Vault) instead of environment variables for sensitive data.
5. **Capacity planning**: Monitor worker utilization, pool slots, and Kubernetes resource usage. Scale workers based on historical workload patterns.
6. **Documentation**: Use Airflow's doc_md and task doc_md to document DAG purpose, task logic, and dependencies. Maintain a pipeline catalog.
