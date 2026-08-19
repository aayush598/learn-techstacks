# Cloud Cost Optimization

Cloud costs for recommendation systems can escalate rapidly — GPU instances for model training, large-memory instances for model serving, high-throughput storage for feature data, and cross-region networking for global deployment. Without disciplined cost management, a recommendation system serving millions of users can consume hundreds of thousands of dollars monthly in cloud spend. This document covers pricing models, right-sizing, auto-scaling optimization, storage tiering, data transfer costs, monitoring tools, and FinOps practices.

---

## 1. Instance Pricing Models

### 1.1 Pricing Comparison

| Model | Discount vs On-Demand | Commitment | Best For |
|---|---|---|---|
| On-demand | 0% (baseline) | None | Dev/test, unpredictable workloads |
| Reserved (1 year) | 30–40% | 1 year | Stable production workloads |
| Reserved (3 year) | 50–60% | 3 years | Core infrastructure (databases, caches) |
| Savings Plans (1 year) | 25–40% | $/hr commitment | Flexible workloads across instance types |
| Spot/Preemptible | 60–90% | None (can be interrupted) | Training, batch processing, non-critical |

### 1.2 Instance Allocation Strategy

| Workload | Instance Type | Pricing Model | Rationale |
|---|---|---|---|
| Model serving (prod) | m6i.2xlarge | Reserved (3yr) | Predictable, always-on |
| Feature pipeline | m6i.xlarge | Savings Plan (1yr) | Consistent usage, some flexibility |
| API servers | m6i.xlarge | Savings Plan (1yr) | Scales with traffic |
| Model training | p4d.24xlarge | Spot (70% savings) | Interruptible, checkpoint-based |
| Batch ETL | m6i.4xlarge | Spot (60% savings) | Time-flexible |
| Monitoring | m6i.large | Reserved (1yr) | Always-on, predictable |
| CI/CD runners | m6i.xlarge | Spot (70% savings) | Ephemeral, on-demand |

### 1.3 GPU Cost Optimization for ML Training

| Strategy | Savings | Implementation |
|---|---|---|
| Spot instances | 60–90% | Checkpoint every 5 minutes, resume on preemption |
| Multi-node training | Amortize per-GPU cost | Use distributed training (DDP, FSDP) |
| Mixed precision training | 2x throughput (same cost) | FP16/BF16 training |
| Gradient accumulation | Larger effective batch size | Fewer GPUs needed |
| Right-size GPU selection | Match GPU to model size | A10G for small models, A100 for large |

---

## 2. Right-Sizing

### 2.1 Resource Usage Analysis

Analyze actual vs allocated resources across the fleet:

| Resource | Common Waste | Detection Method |
|---|---|---|
| CPU | Over-provisioned 3–4x | Average utilization < 30% of request |
| Memory | Over-provisioned 2–3x | Average utilization < 50% of request |
| GPU | Under-utilized during inference | SM utilization < 50% |
| Storage | Attached but unused volumes | Volume exists with no read/write |
| Network | Over-provisioned bandwidth | Actual < 20% of allocated |

### 2.2 Right-Sizing Tools

| Tool | Cloud | Capability |
|---|---|---|
| AWS Compute Optimizer | AWS | ML-powered instance recommendations |
| AWS Trusted Advisor | AWS | Over-utilized and under-utilized resources |
| Google Active Assist | GCP | Right-sizing recommendations |
| Spot.io | Multi-cloud | Automated right-sizing + spot |
| Kubecost | Kubernetes | Per-pod resource efficiency scoring |
| OpenCost | Kubernetes | Resource utilization visibility |

### 2.3 Right-Sizing Process

1. **Baseline**: Collect 2 weeks of resource utilization metrics
2. **Identify waste**: Flag instances with < 30% average utilization
3. **Model recommendation impact**: Simulate smaller instances with load testing
4. **Apply changes**: Start with non-critical services, measure impact
5. **Verify**: Monitor for performance degradation (latency, error rate)
6. **Iterate**: Monthly review cycle

### 2.4 Right-Sizing Targets

| Metric | Current Average | Target | Method |
|---|---|---|---|
| CPU utilization | 25% | 60–70% | Reduce instance sizes |
| Memory utilization | 35% | 60–70% | Reduce instance sizes |
| GPU utilization (inference) | 40% | 70–80% | Batch requests, right-size GPU |
| GPU utilization (training) | 60% | 85%+ | Optimize data loading, mixed precision |

---

## 3. Auto-Scaling Optimization

### 3.1 Horizontal Pod Autoscaler (HPA) Tuning

| Parameter | Default | Optimized | Rationale |
|---|---|---|---|
| CPU target | 80% | 65–70% | Scale up before saturation |
| Memory target | 80% | 70–75% | Prevent OOM while utilizing well |
| Scale-up stabilization | 15s | 30s | Prevent rapid scale-up oscillation |
| Scale-down stabilization | 300s | 600s | Prevent premature scale-down |
| Min replicas | 1 | 2 | Ensure availability during scaling |

### 3.2 Cluster Autoscaler Configuration

| Setting | Value | Rationale |
|---|---|---|
| Scale-down utilization threshold | 50% | Remove under-utilized nodes |
| Scale-down delay | 10 minutes | Wait before removing nodes |
| Max node provisioning time | 15 minutes | Timeout for node readiness |
| Expander strategy | `least-waste` | Choose node groups that minimize waste |

### 3.3 Predictive Scaling

- Analyze traffic patterns (hourly, daily, weekly seasonality)
- Pre-scale before predicted traffic spikes
- For recommendation systems: scale up before morning commute, evening browsing peaks
- AWS Predictive Scaling, GCP Predictive Autoscaling

### 3.4 Time-Based Scaling

| Period | Scaling Policy | Instances |
|---|---|---|
| Weekday 6am–10am | Scale up to peak | 12 pods, 6 nodes |
| Weekday 10am–10pm | Maintain peak | 12 pods, 6 nodes |
| Weekday 10pm–6am | Scale to minimum | 4 pods, 3 nodes |
| Weekend | Scale to minimum | 4 pods, 3 nodes |

---

## 4. Storage Tiering

### 4.1 Data Lifecycle for Recommendation Systems

| Data Type | Hot (0–7 days) | Warm (7–90 days) | Cold (90+ days) | Archive (365+ days) |
|---|---|---|---|---|
| User interaction events | S3 Standard | S3 IA | S3 Glacier IR | S3 Glacier Deep Archive |
| Feature snapshots | EBS (SSD) | S3 Standard | S3 IA | S3 Glacier |
| Model artifacts | S3 Standard | S3 Standard | S3 IA | S3 Glacier |
| Training datasets | S3 Standard | S3 IA | S3 Glacier IR | S3 Glacier Deep Archive |
| Recommendation logs | CloudWatch | S3 Standard | S3 IA | S3 Glacier |
| User profiles | DynamoDB/RDS | S3 Standard | S3 IA | Deleted |

### 4.2 Storage Cost Optimization

| Technique | Savings | Implementation |
|---|---|---|
| Lifecycle policies | 50–90% for aged data | S3 lifecycle rules, automatic transition |
| Compression | 50–70% | Gzip for logs, Parquet for analytics |
| Deduplication | 20–40% | Remove duplicate feature snapshots |
| Right-size volumes | Variable | Delete unattached EBS volumes |
| EFS Intelligent-Tiering | 30–50% | Automatic file access pattern analysis |

### 4.3 Data Retention Policy

| Data Category | Retention | Rationale |
|---|---|---|
| Raw interaction events | 90 days hot, 1 year archive | Regulatory + model retraining |
| Feature snapshots | 30 days hot, 90 days warm | Debugging + audit |
| Model artifacts | Permanent (all versions) | Rollback + lineage |
| Prediction logs | 30 days hot, 90 days archive | Monitoring + analysis |
| Audit logs | 7 years | Compliance |
| User profiles | Active + 30 days post-deletion | GDPR right to erasure |

---

## 5. Data Transfer Costs

### 5.1 Cost Sources

| Transfer Type | Cost Driver | Typical Cost |
|---|---|---|
| Cross-AZ transfer | Per GB between availability zones | $0.01/GB |
| Cross-region transfer | Per GB between regions | $0.02/GB |
| Internet egress | Per GB to internet | $0.09/GB (first 10TB) |
| S3 to CloudFront | Per GB from origin to edge | $0.00 (free) |
| Cross-cloud transfer | Per GB between providers | $0.01–0.02/GB + VPN cost |

### 5.2 Transfer Cost Reduction

| Strategy | Implementation | Savings |
|---|---|---|
| Keep traffic in same AZ | Co-locate related services | 100% of cross-AZ cost |
| Use CloudFront as origin shield | Serve from edge, reduce origin calls | 50–80% of egress cost |
| Compress responses | Gzip/Brotli at origin or edge | 60–80% of transfer volume |
| Reduce polling frequency | Event-driven instead of polling | 50–90% of API transfer |
| VPC endpoints | Use private connectivity for S3, DynamoDB | 100% of NAT gateway cost |

### 5.3 Recommendation System Transfer Patterns

| Pattern | Data Volume | Cost Optimization |
|---|---|---|
| Feature retrieval | 10KB per request × millions | Cache aggressively, edge compute |
| Model serving response | 1–5KB per request | Compress, paginate |
| Event ingestion | 500 bytes × millions/day | Batch, use Kinesis/Kafka |
| Model artifact download | 100MB–10GB per update | CDN, peer-to-peer distribution |

---

## 6. Cost Monitoring and FinOps

### 6.1 Kubecost / OpenCost

| Feature | Kubecost | OpenCost |
|---|---|---|
| Cost allocation | Per namespace, label, annotation | Per namespace, label |
| Real-time pricing | Yes | Yes |
| Right-sizing recommendations | Yes | Yes |
| Multi-cluster | Yes (Enterprise) | Yes |
| Alerts | Budget alerts, anomaly detection | Basic |
| Open source | Partially (core is free) | Fully open source |

### 6.2 FinOps Practices

| Practice | Implementation | Frequency |
|---|---|---|
| Cost review meetings | Review cloud spend with engineering leads | Weekly |
| Budget alerts | Alert at 50%, 75%, 90%, 100% of budget | Continuous |
| Anomaly detection | ML-based spend anomaly detection | Continuous |
| Chargeback reporting | Allocate costs to teams/products/features | Monthly |
| Cost optimization reviews | Review right-sizing recommendations | Bi-weekly |
| Commitment planning | Review Reserved Instance / Savings Plan coverage | Quarterly |

### 6.3 Cost Allocation Tags

Apply these tags to every resource:

| Tag | Example | Purpose |
|---|---|---|
| `team` | `rec-ml` | Team ownership |
| `service` | `model-server` | Service attribution |
| `environment` | `production` | Environment separation |
| `cost-center` | `recommendations` | Business unit allocation |
| `project` | `rec-v2-redesign` | Project-based tracking |
| `managed-by` | `terraform` | IaC tracking |

### 6.4 Monthly Cost Report Template

| Category | Last Month | This Month | Change | Notes |
|---|---|---|---|---|
| Compute (EC2/VMs) | $45,000 | $42,000 | -6.7% | Right-sizing applied |
| Storage (S3/EBS) | $12,000 | $11,500 | -4.2% | Lifecycle policies |
| Networking | $8,000 | $8,200 | +2.5% | Traffic increase |
| GPU instances | $30,000 | $28,000 | -6.7% | More spot usage |
| Managed services | $15,000 | $15,000 | 0% | No changes |
| **Total** | **$110,000** | **$104,700** | **-4.8%** | |
