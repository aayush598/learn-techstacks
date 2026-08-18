# Infrastructure Metrics for Recommendation Systems

## Overview

Infrastructure metrics provide visibility into the health and performance of the underlying
compute, storage, and network resources that power the recommendation system. This covers
system-level metrics (CPU, memory, disk, network), Kubernetes-specific metrics (pod, node,
cluster), Prometheus collection architecture, Grafana dashboard design, SLO/SLI definitions,
and capacity planning metrics.

## Core System Metrics

### CPU Metrics

| Metric                        | Description                                       | Alert Threshold        |
|-------------------------------|---------------------------------------------------|-----------------------|
| cpu_usage_seconds_total       | Cumulative CPU time consumed                      | Rate-based analysis   |
| cpu_utilization_ratio         | CPU usage as fraction of available cores          | > 80% for 5 min       |
| cpu_steal_seconds             | Time stolen by hypervisor (cloud VMs)             | > 5% sustained        |
| load_average_1m/5m/15m       | System load averages                              | > 2x CPU cores        |
| context_switches_total        | Rate of context switches                          | Anomaly detection     |
| cpu_throttled_seconds_total   | Cgroup throttling in Kubernetes                   | > 25% of runtime      |

**Recommendation System Context**:
- Model serving pods: CPU-intensive during inference (matrix operations)
- Feature pipeline pods: CPU burst during batch feature computation
- API pods: CPU proportional to request rate
- CPU throttling directly impacts P99 latency for recommendations

### Memory Metrics

| Metric                        | Description                                       | Alert Threshold        |
|-------------------------------|---------------------------------------------------|-----------------------|
| memory_working_set_bytes      | Memory actively in use                            | > 85% of limit        |
| memory_available_bytes        | Memory available for new allocations              | < 15% of total        |
| memory_cache_bytes            | Page cache memory (reclaimable)                   | Informational         |
| memory_rss                    | Resident Set Size (non-reclaimable)               | > 90% of limit        |
| oom_kill_total                | Out-of-memory kill events                         | Any occurrence         |
| memory_swap_usage_bytes       | Swap usage (indicates memory pressure)            | > 0 sustained         |

**Recommendation System Context**:
- Model serving: Models loaded into memory (model size + inference buffers)
- Feature store: In-memory feature caches
- Embedding servers: Large embedding matrices in memory
- OOM kills cause immediate service disruption

### Disk Metrics

| Metric                        | Description                                       | Alert Threshold        |
|-------------------------------|---------------------------------------------------|-----------------------|
| disk_usage_ratio              | Disk space used as fraction of total              | > 85%                 |
| disk_read_bytes_total         | Cumulative bytes read from disk                   | Rate analysis         |
| disk_write_bytes_total        | Cumulative bytes written to disk                  | Rate analysis         |
| disk_read_time_seconds_total  | Time spent reading from disk                      | I/O saturation        |
| disk_write_time_seconds_total | Time spent writing to disk                        | I/O saturation        |
| disk_io_util                  | Percentage of time disk was busy                  | > 90% sustained       |
| disk_iops                     | I/O operations per second                         | Capacity planning     |

**Recommendation System Context**:
- Training data storage: High read throughput during model training
- Model artifact storage: Large reads during model loading
- WAL logs: Continuous write workload
- Feature store: Random read patterns

### Network Metrics

| Metric                        | Description                                       | Alert Threshold        |
|-------------------------------|---------------------------------------------------|-----------------------|
| network_receive_bytes_total   | Incoming network traffic                          | Anomaly detection     |
| network_transmit_bytes_total  | Outgoing network traffic                          | Anomaly detection     |
| network_receive_errors_total  | Incoming packet errors                            | Any sustained errors  |
| network_transmit_errors_total | Outgoing packet errors                            | Any sustained errors  |
| network_receive_dropped_total | Dropped incoming packets                          | > 0 sustained         |
| tcp_connections_established   | Active TCP connections                            | Connection limit      |
| tcp_retransmits_total         | TCP retransmissions (latency indicator)           | > 1% of packets       |

**Recommendation System Context**:
- API responses can be large (10+ items with metadata = 50-500KB per response)
- Feature store traffic: High-throughput, low-latency reads
- Kafka event traffic: Sustained high-bandwidth between producers and consumers
- Model serving: GPU-to-CPU data transfer latency matters

## Kubernetes Metrics

### Pod-Level Metrics

```
Pod Metrics Stack:
├── kube_pod_info                    — Pod metadata (node, namespace, labels)
├── kube_pod_status_phase            — Current phase (Running, Pending, Failed)
├── kube_pod_container_resource_requests — Requested resources
├── kube_pod_container_resource_limits   — Resource limits
├── container_cpu_usage_seconds_total    — Actual CPU usage
├── container_memory_working_set_bytes   — Actual memory usage
├── kube_pod_status_ready             — Readiness probe status
├── kube_pod_status_restarts_total     — Container restart count
└── kube_pod_status_terminated_reason  — Why a pod terminated (OOMKilled, Error)
```

### Node-Level Metrics

```
Node Metrics Stack:
├── kube_node_info                        — Node metadata
├── kube_node_status_condition            — Node conditions (Ready, MemoryPressure)
├── kube_node_status_allocatable          — Allocatable resources
├── kube_node_status_capacity             — Total node capacity
├── kube_node_spec_taint                  — Taints (affect scheduling)
├── node_cpu_seconds_total                — Node CPU utilization
├── node_memory_MemAvailable_bytes        — Node memory available
└── node_filesystem_avail_bytes           — Node disk space available
```

### Cluster-Level Metrics

| Metric                            | Description                                   |
|----------------------------------|-----------------------------------------------|
| kube_cluster_size                | Number of nodes in cluster                    |
| cluster_memory_total             | Total cluster memory                          |
| cluster_cpu_total                | Total cluster CPU cores                       |
| cluster_storage_total            | Total cluster storage                         |
| cluster_pod_count                | Total running pods                            |
| cluster_namespace_pod_count      | Pods per namespace                            |
| cluster_node_count_by_status     | Ready vs. NotReady nodes                      |

### Resource Utilization Tracking

**Per-Deployment Dashboard Metrics**:
- CPU request vs. actual usage ratio (should be 1.0-1.5 for right-sizing)
- Memory request vs. actual usage ratio (should be 1.0-1.3 for right-sizing)
- CPU throttling percentage per container
- OOM kill events per pod
- Pod restart frequency

## Prometheus Metrics Collection

### Prometheus Architecture for Recommendation Systems

```
Prometheus Server (HA pair)
├── Scrape Targets:
│   ├── recommendation-api pods (metrics endpoint /metrics)
│   ├── model-server pods (inference metrics)
│   ├── feature-pipeline pods (processing metrics)
│   ├── Kafka brokers (JMX metrics)
│   ├── Redis nodes (INFO metrics)
│   ├── PostgreSQL (pg_exporter metrics)
│   ├── Kubernetes node-exporter
│   └── kube-state-metrics
├── Recording Rules:
│   ├── Pre-computed SLO burn rates
│   ├── Pre-computed latency percentiles
│   └── Pre-computed error rate aggregations
├── Alerting Rules:
│   ├── Infrastructure alerts
│   ├── Application alerts
│   └── SLO-based alerts
└── Remote Write:
    ├── Thanos / Cortex (long-term storage)
    └── Grafana Cloud (managed)
```

### Scraping Strategy

| Component           | Scrape Interval | Retention   | Reasoning                           |
|--------------------|----------------|-------------|--------------------------------------|
| API servers        | 15s            | 30 days     | High change rate, latency-critical   |
| Model servers      | 15s            | 30 days     | Inference metrics vary quickly       |
| Feature pipeline   | 30s            | 30 days     | Batch processing, less variable      |
| Kafka              | 15s            | 30 days     | Event throughput monitoring          |
| Redis              | 15s            | 30 days     | Cache hit rate critical              |
| PostgreSQL         | 30s            | 30 days     | Database metrics less volatile       |
| Kubernetes nodes   | 30s            | 30 days     | Infrastructure-level monitoring      |

### Recording Rules for Performance

Pre-compute expensive queries to reduce Prometheus load:

```
# 5-minute error rate (for alerting)
- expr: rate(http_requests_total{status=~"5.."}[5m])
  record: job:http_requests_error_rate:rate5m

# P99 latency (using histogram_quantile)
- expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))
  record: job:http_request_duration_seconds:p99:rate5m

# SLO burn rate (1-hour window)
- expr: (1 - job:http_requests_error_rate:rate5m) / (1 - 0.999)
  record: job:slo_burn_rate:1h
```

## Grafana Dashboard Design

### Dashboard Hierarchy

```
Level 1: Executive Dashboard
├── Overall system health (green/yellow/red)
├── SLO compliance (99.9% availability)
├── Request volume and error rate trends
└── Cost metrics (requests per dollar)

Level 2: Service Dashboard
├── Per-service latency percentiles (P50, P95, P99)
├── Per-service error rate and breakdown
├── Per-service throughput (requests/second)
└── Per-service resource utilization

Level 3: Component Dashboard
├── Pod-level CPU, memory, network
├── Model inference latency and throughput
├── Feature store hit rate and latency
├── Cache effectiveness metrics
└── Queue depth and processing lag

Level 4: Debug Dashboard
├── Per-request trace analysis
├── Error stack traces and frequency
├── Slow request investigation
└── Dependency health and latency
```

### Key Grafana Panels for Recommendation Systems

| Panel                   | Visualization   | Refresh | Purpose                           |
|------------------------|----------------|---------|-----------------------------------|
| Request rate            | Time series     | 15s     | Traffic volume monitoring         |
| Error rate              | Time series     | 15s     | Error detection and trending      |
| P50/P95/P99 latency    | Time series     | 15s     | Latency distribution tracking     |
| Model inference time    | Heatmap         | 30s     | Inference latency distribution    |
| Feature store hit rate  | Gauge           | 15s     | Cache effectiveness               |
| Recommendation count    | Bar chart       | 1m      | Output volume per algorithm       |
| Active pod count        | Stat            | 30s     | Deployment health                 |
| CPU throttling          | Time series     | 15s     | Resource contention               |

## SLO/SLI Metrics

### Service Level Indicators for Recommendation Systems

| SLI                          | Metric                                        | Target    |
|------------------------------|-----------------------------------------------|-----------|
| Availability                 | Successful requests / total requests           | 99.9%     |
| Latency                      | Requests with P95 < 200ms / total requests    | 99.5%     |
| Correctness                  | Valid recommendations returned / total         | 99.99%    |
| Freshness                    | Features < 1 hour old / total features        | 99.0%     |
| Throughput                    | Requests served within budget / total          | 99.9%     |

### Error Budget Calculation

```
Monthly Error Budget = (1 - SLO) * Total Requests in Month

Example:
  SLO: 99.9%
  Monthly requests: 100 million
  Error budget: 0.1% * 100M = 100,000 failed requests allowed

Usage tracking:
  Week 1: 15,000 errors (15% of budget used) — On track
  Week 2: 35,000 errors (35% of budget used) — On track
  Week 3: 80,000 errors (80% of budget used) — Freeze non-critical deploys
  Week 4: 110,000 errors (110% of budget used) — SLO violated, incident review
```

### SLO-Based Alerting Rules

- **Page**: Error budget burn rate > 14.4x (2% of budget consumed in 1 hour)
- **Ticket**: Error budget burn rate > 3x (1% of budget consumed in 6 hours)
- **Warning**: Error budget burn rate > 1x (budget consumed at expected rate)

## Capacity Metrics

### Capacity Planning Indicators

| Metric                        | Description                                       | Action Trigger            |
|------------------------------|---------------------------------------------------|---------------------------|
| CPU headroom                 | 1 - (avg CPU usage / CPU limit)                   | < 20% → scale up          |
| Memory headroom              | 1 - (avg memory usage / memory limit)             | < 15% → scale up          |
| Pod autoscaler min/max       | Current replicas vs. autoscaler bounds            | At max → increase bounds  |
| Storage growth rate          | GB per day of storage increase                    | Projection to 85% in 30d  |
| Feature store memory usage   | Redis memory used / max memory                    | > 80% → add nodes         |
| Model server GPU utilization | GPU compute utilization                           | > 70% → add GPUs          |

### Resource Utilization Reports

Generate weekly resource utilization reports:
- Average and peak CPU/memory usage per deployment
- Resource request vs. actual usage (right-sizing opportunities)
- Storage growth trends and projections
- Cost allocation by service and team
- Recommendations for resource optimization
