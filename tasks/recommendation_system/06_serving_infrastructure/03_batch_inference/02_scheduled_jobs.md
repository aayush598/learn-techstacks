# Scheduled Batch Jobs for Recommendation Systems

## Overview

Batch inference jobs generate recommendations for users who aren't actively using the application. These jobs score large user populations on a schedule, pre-computing recommendations that can be served from cache with minimal latency. This covers scheduling, SLA management, resource allocation, and monitoring.

---

## Cron-Based Scheduling

### Schedule Design

| Recommendation Type | Frequency | Window | Priority |
|--------------------|-----------|--------|----------|
| Daily personalized | 2:00 AM UTC | 4 hours | High |
| Weekly digest email | Sunday 6:00 AM UTC | 6 hours | Medium |
| Trending items | Every 30 minutes | 10 minutes | High |
| Catalog reranking | Every 6 hours | 2 hours | Medium |
| Cold-start items | Every hour | 20 minutes | High |
| Model evaluation | Daily 4:00 AM UTC | 2 hours | Low |

### Cron Expression Best Practices

- **Avoid peak hours**: Schedule heavy jobs during low-traffic periods (2-6 AM)
- **Stagger dependent jobs**: Don't start all jobs simultaneously
- **Buffer time**: Allow 30-60 minutes between dependent job starts
- **Weekend vs weekday**: Adjust schedules for traffic patterns

### Schedule Management

```
Job Scheduler (Airflow/Prefect) →
  1. Parse cron expression
  2. Check dependencies (upstream jobs completed)
  3. Check resource availability
  4. Allocate resources
  5. Launch job
  6. Monitor until completion
  7. Notify on success/failure
```

---

## SLA Management

### SLA Definition

| SLA Component | Target | Measurement |
|---------------|--------|-------------|
| Completion time | 95% of jobs complete within window | Job runtime |
| Freshness | Recommendations no older than TTL | Cache timestamp |
| Quality | Metrics within 1% of validation | Metric comparison |
| Availability | 99.9% of scheduled runs complete | Job success rate |

### SLA Monitoring

- Track job completion time vs allocated window
- Alert if job is unlikely to complete within SLA
- Track freshness of served recommendations
- Monitor quality metrics of batch-generated recommendations

### SLA Breach Handling

1. **Early warning**: Job at 50% of window with < 50% progress → alert
2. **Critical alert**: Job at 80% of window with < 80% progress → page on-call
3. **SLA breach**: Job not completed within window → execute fallback
4. **Post-mortem**: Analyze root cause and implement prevention

### Fallback Strategies

- Serve stale recommendations from previous batch
- Fall back to popularity-based recommendations
- Serve cached real-time recommendations for affected users
- Reduce candidate set size to complete within remaining time

---

## Resource Allocation

### Resource Planning

| Job Type | CPU | Memory | GPU | Duration |
|----------|-----|--------|-----|----------|
| Daily personalized (10M users) | 64 cores | 256 GB | 8 A100 | 3 hours |
| Trending update (1M items) | 16 cores | 64 GB | 2 A100 | 15 minutes |
| Model evaluation | 32 cores | 128 GB | 4 A100 | 1 hour |
| Feature pipeline | 48 cores | 192 GB | None | 2 hours |

### Resource Scheduling

- **Capacity planning**: Ensure cluster has resources for peak batch load
- **Job packing**: Schedule multiple small jobs on same resources
- **Priority-based allocation**: High-priority jobs get resources first
- **Spot instances**: Use preemptible instances for non-critical batch jobs
- **Dynamic allocation**: Scale cluster up/down based on batch job schedule

### Parallelization

- Shard users across multiple worker instances
- Process each shard independently (embarrassingly parallel)
- Aggregate results after all shards complete
- Use MapReduce or Spark for large-scale parallel batch scoring

---

## Dependency Management

### Job Dependency Graph

```
Data Pipeline → Feature Pipeline → Candidate Generation → Scoring → Cache Write → Notification
     ↓                                                ↑
  Data Quality Check                          Model Registry
```

### Dependency Types

| Type | Description | Handling |
|------|-------------|---------|
| Data dependency | Upstream data must be available | Check data freshness before starting |
| Model dependency | Model must be in registry | Verify model version exists |
| Resource dependency | Resources must be available | Queue if resources busy |
| Temporal dependency | Must run after specific time | Cron scheduling |
| Output dependency | Previous job output needed | Check file existence |

### Dependency Resolution

- Use DAG-based orchestrators (Airflow, Prefect, Dagster)
- Define dependencies explicitly in job configuration
- Implement circuit breakers for failing dependencies
- Cache dependency check results to avoid redundant checks

---

## Failure Handling

### Failure Categories

| Category | Example | Recovery |
|----------|---------|----------|
| Transient | Network timeout, OOM | Automatic retry |
| Persistent | Data corruption, model error | Manual intervention |
| Resource | Out of memory, disk full | Scale up, retry |
| Dependency | Upstream job failed | Wait for upstream fix |
| Quality | Output metrics below threshold | Rollback, alert |

### Retry Strategy

```
Retry Policy:
  max_retries: 3
  retry_delay: exponential (5m, 15m, 45m)
  retry_on: [transient_errors]
  alert_after: 2 failures
  escalate_after: 3 failures
```

### Dead Letter Queue

- Failed jobs go to a review queue
- Manual inspection to determine root cause
- Reprocess after fix, or mark as acceptable failure
- Track failure rates for trending and alerting

### Data Quality Gates

- Validate output schema before writing to cache
- Check metric ranges (NDCG should be 0-1, latency should be positive)
- Verify output count matches expected (no silent data loss)
- Compare output statistics with previous successful run

---

## Monitoring and Alerting

### Job-Level Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|----------------|
| Job duration | Time from start to completion | > 120% of expected |
| Job success rate | % of jobs completing successfully | < 95% weekly |
| Output quality | Key metric comparison to baseline | > 2% regression |
| Resource utilization | CPU/memory/GPU during job | < 30% for > 50% of runtime |

### Dashboard Components

- Job execution timeline (Gantt chart style)
- SLA compliance rate over time
- Resource utilization heatmap
- Failure count and root cause breakdown
- Output quality trend over time

### Alerting Rules

- **Critical**: Job failed 2+ consecutive times
- **Warning**: Job duration > 80% of SLA window
- **Info**: Job completed with quality regression > 1%
- **Critical**: Output count deviates > 10% from expected
