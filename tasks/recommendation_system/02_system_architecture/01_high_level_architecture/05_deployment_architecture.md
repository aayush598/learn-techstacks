# Deployment Architecture — Recommendation System

## 1. Production Deployment Topology

### 1.1 Multi-Region Architecture
- **Active-Active**: All regions serve traffic simultaneously; data replicated across regions
- **Active-Passive**: Primary region serves traffic; secondary is standby for failover
- **Geo-Distributed**: Recommendations served from nearest region for low latency
- **Data Replication**: Cross-region Kafka MirrorMaker for event replication; database replication with conflict resolution

### 1.2 Region Design
- **Minimum 2 regions** for production recommendation systems
- **3+ regions** for global user bases (US, EU, APAC)
- **Each region** contains full serving stack (API, features, models, cache)
- **Shared components**: Model registry, experiment configuration, centralized monitoring (can be region-specific or global)

### 1.3 Availability Zones
- **3+ AZs per region** for high availability
- **Each AZ** has independent power, networking, and cooling
- **Load balancing** across AZs with automatic failover
- **Data replication** across AZs within a region

---

## 2. Kubernetes Cluster Architecture

### 2.1 Cluster Layout
```
Production Cluster (per region):
├── System Node Pool (3-5 nodes)
│   ├── API Gateway pods
│   ├── Monitoring stack
│   └── Cluster management
├── Application Node Pool (10-100 nodes)
│   ├── Candidate Generation pods
│   ├── Ranking Service pods
│   ├── Feature Service pods
│   ├── User Profile Service pods
│   └── Other microservice pods
├── GPU Node Pool (2-20 nodes)
│   ├── Model Serving pods (Triton/vLLM)
│   └── GPU-enabled Feature Computation pods
├── Data Node Pool (5-20 nodes)
│   ├── Kafka brokers
│   ├── Redis Cluster nodes
│   ├── PostgreSQL instances
│   └── Elasticsearch nodes
└── Batch Node Pool (0-50 nodes, auto-scaled)
    ├── Spark driver/executor pods
    ├── Airflow workers
    └── Training jobs
```

### 2.2 Resource Quotas and Limits
- **CPU requests/limits**: Set per pod based on profiling
- **Memory requests/limits**: Critical for JVM-based services and model serving
- **GPU requests**: Explicit GPU resource requests for model serving pods
- **Ephemeral storage**: For model artifacts and temporary data
- **Namespace isolation**: Separate namespaces for production, staging, development

### 2.3 Pod Management
- **Deployment**: Stateless services use Deployments with RollingUpdate strategy
- **StatefulSet**: Stateful components (Kafka, Redis, databases) use StatefulSets
- **DaemonSet**: Monitoring agents on every node
- **Job/CronJob**: Batch processing and scheduled tasks
- **Pod Disruption Budgets**: Ensure minimum availability during node maintenance

---

## 3. Model Deployment Architecture

### 3.1 Model Serving Patterns

#### Dedicated Model Serving (Recommended)
- **Triton Inference Server**: NVIDIA's production-grade model serving platform
- **Model Repository**: S3/MinIO-backed model repository with version management
- **GPU Sharing**: Multi-model GPU sharing with MIG (Multi-Instance GPU) on NVIDIA A100
- **Dynamic Batching**: Automatic request batching for GPU efficiency
- **Model Warm-up**: Pre-load models into GPU memory on pod start

#### Sidecar Model Serving
- **Model as Sidecar**: Model served as sidecar container in same pod
- **Benefits**: No network hop for inference; model co-located with application logic
- **Drawbacks**: Model update requires pod restart; GPU sharing difficult
- **Use Case**: Small models, latency-critical serving, edge deployment

#### Embedded Model Serving
- **Model Embedded in Application**: Model loaded directly in application process
- **ONNX Runtime**: For CPU-based model inference embedded in application
- **Benefits**: Minimal latency; simple deployment
- **Drawbacks**: Model update requires application redeployment; resource contention

### 3.2 Model Rollout Strategy
1. **Upload to Registry**: New model uploaded to model registry in "Development" stage
2. **Automated Validation**: Quality gates run (latency, accuracy, data validation)
3. **Staging Deployment**: Model deployed to staging environment for integration testing
4. **Canary Deployment**: Model deployed to 5% of production traffic
5. **Quality Monitoring**: Monitor key metrics for canary vs control for 24-72 hours
6. **Promotion**: If metrics are positive, gradually increase traffic to 100%
7. **Rollback**: If metrics degrade, instantly rollback to previous version

### 3.3 Model Versioning and Rollback
- **Blue-Green Model Deployment**: Two model versions running simultaneously; traffic switched atomically
- **Model Shadow Mode**: New model runs alongside production model; predictions logged but not served
- **A/B Model Testing**: New model tested against old model using real traffic with controlled split
- **Instant Rollback**: Switch traffic back to previous model version in <1 second

---

## 4. Blue-Green Deployment

### 4.1 Blue-Green for Services
- **Blue Environment**: Current production environment serving live traffic
- **Green Environment**: New version deployed and tested
- **Load Balancer Switch**: Traffic switched from blue to green atomically
- **Rollback**: Switch back to blue if issues detected
- **Database Migration**: Must be backward compatible to support both versions simultaneously

### 4.2 Blue-Green for Models
- **Model A (Blue)**: Current production model
- **Model B (Green)**: New candidate model
- **Traffic Split**: Load balancer routes % of requests to each model
- **Gradual Shift**: Traffic gradually moved from blue to green
- **Automatic Rollback**: If green model metrics degrade, traffic shifts back to blue

---

## 5. Canary Deployment

### 5.1 Canary Strategy
- **Initial**: Route 5% of traffic to new version
- **Monitor**: Watch error rates, latency, and business metrics for 1-4 hours
- **Expand**: If metrics are good, expand to 25%, 50%, 75%, 100%
- **Rollback**: If any metric exceeds threshold, revert to 0% canary traffic

### 5.2 Canary Metrics
- **Error Rate**: Canary error rate should not exceed control by more than 0.1%
- **Latency P99**: Canary P99 latency should not exceed control by more than 10%
- **Business Metrics**: CTR, conversion rate should not degrade vs control
- **Model Metrics**: Prediction distribution should be reasonable (not all same class)

### 5.3 Automated Canary Analysis
- **Statistical Significance**: Automated significance testing before promotion
- **Guardrail Alerts**: Automated rollback if critical metrics degrade
- **Time-based Promotion**: Automatic promotion after configurable monitoring window
- **Manual Approval Gate**: Optional human approval before full promotion

---

## 6. Infrastructure Sizing

### 6.1 Compute Sizing Guidelines

| Service | Per 1M Users | Per 10M Users | Per 100M Users |
|---|---|---|---|
| API Gateway | 2-4 vCPU, 4GB RAM | 8-16 vCPU, 16GB RAM | 40-80 vCPU, 80GB RAM |
| Candidate Generation | 4-8 vCPU, 16GB RAM | 16-32 vCPU, 64GB RAM | 80-160 vCPU, 320GB RAM |
| Ranking Service | 1-2 GPU (A10G) | 4-8 GPU (A10G) | 16-40 GPU (A10G) |
| Feature Service | 4-8 vCPU, 16GB RAM | 16-32 vCPU, 64GB RAM | 80-160 vCPU, 320GB RAM |
| Redis (Features) | 32GB RAM (3 nodes) | 128GB RAM (6 nodes) | 512GB RAM (12 nodes) |
| Kafka | 3 brokers, 1TB disk | 6 brokers, 2TB disk | 12+ brokers, 4TB disk |
| PostgreSQL | 4 vCPU, 16GB RAM | 8 vCPU, 32GB RAM (replica) | 16+ vCPU, 64GB RAM (sharded) |

### 6.2 Storage Sizing
- **Data Lake**: 10x raw data size (compressed Parquet reduces ~10x)
- **Feature Store Online**: ~1KB per user feature vector × number of active users
- **Model Artifacts**: ~100MB-10GB per model version
- **Event Retention**: ~1KB per event × events per day × retention days
- **Logs**: ~10GB per day per service (with structured logging)

### 6.3 Network Bandwidth
- **Intra-cluster**: 10-25 Gbps for data-heavy services
- **Cross-region**: 1-10 Gbps for replication
- **External**: 1-10 Gbps for user-facing APIs (varies with traffic)

---

## 7. Cost Optimization

### 7.1 Compute Cost Optimization
- **Spot/Preemptible Instances**: For training and batch processing (60-90% savings)
- **Right-sizing**: Regular resource usage analysis and pod right-sizing
- **Cluster Autoscaler**: Scale node pools based on actual demand
- **Spot Mix**: Use 70% spot + 30% on-demand for cost-efficient resilience
- **Reserved Instances**: For predictable baseline workloads (30-50% savings)

### 7.2 Storage Cost Optimization
- **Data Lifecycle**: Automatically tier old data to cheaper storage
- **Compression**: Use Parquet with Snappy/ZSTD for data lake storage
- **Deduplication**: Deduplicate model artifacts and data
- **Garbage Collection**: Regular cleanup of old model versions, expired events, debug data

### 7.3 GPU Cost Optimization
- **GPU Sharing**: MIG (Multi-Instance GPU) for serving multiple small models
- **Dynamic Batching**: Maximize GPU utilization through request batching
- **Model Optimization**: Quantization and pruning to reduce GPU requirements
- **GPU Auto-scaling**: Scale GPU nodes based on inference demand

### 7.4 Network Cost Optimization
- **CDN for Cached Results**: Offload static recommendation results to CDN
- **Compression**: Compress network traffic between services
- **Data Locality**: Co-locate services that communicate frequently
- **Regional Data Processing**: Process data in the region where it originates

---

## 8. Disaster Recovery

### 8.1 RPO and RTO Targets
- **RPO (Recovery Point Objective)**: < 1 hour for recommendation data; < 5 minutes for user profiles
- **RTO (Recovery Time Objective)**: < 30 minutes for full service restoration; < 5 minutes for failover

### 8.2 Backup Strategy
- **Database Backups**: Continuous WAL archiving + daily full backups
- **Model Artifacts**: Versioned in object storage (S3/MinIO) with cross-region replication
- **Configuration**: Git-managed; entire infrastructure reproducible from code
- **Feature Store**: Regular snapshots of online store; offline store backed by data lake

### 8.3 Failover Procedures
1. **Detection**: Automated health checks detect region/AZ failure
2. **Traffic Routing**: DNS/load balancer routes traffic to healthy region
3. **Data Recovery**: Promote read replicas to primary; reconcile any data loss
4. **Service Restoration**: Verify all services operational in failover region
5. **Validation**: Run end-to-end smoke tests
6. **Communication**: Notify stakeholders of failover status

---

## 9. Security Architecture

### 9.1 Network Security
- **Network Policies**: Kubernetes NetworkPolicy for pod-to-pod communication control
- **Service Mesh**: mTLS for all inter-service communication
- **WAF**: Web Application Firewall for external API endpoints
- **DDoS Protection**: Rate limiting and traffic analysis at edge

### 9.2 Secrets Management
- **Kubernetes Secrets**: Encrypted at rest in etcd
- **External Secrets Operator**: Sync from external secret stores (Vault, AWS Secrets Manager)
- **Secret Rotation**: Automated rotation of database credentials, API keys, certificates
- **Zero Secrets in Code**: All secrets managed externally, never in source code

### 9.3 Container Security
- **Image Scanning**: Scan images for vulnerabilities before deployment
- **Minimal Base Images**: Use distroless or Alpine-based images
- **Non-root Containers**: Run all containers as non-root user
- **Read-only Filesystem**: Mount filesystems as read-only where possible
- **Security Policies**: Pod Security Standards enforced at namespace level
