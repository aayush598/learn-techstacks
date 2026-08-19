# Log Aggregation for Recommendation Systems

## 1. Centralized vs Distributed Logging

### 1.1 Centralized Logging
- All logs shipped to a central location for analysis
- Single query interface across all services
- Easier debugging and correlation
- **Tools**: ELK Stack (Elasticsearch + Logstash + Kibana), Loki + Grafana

### 1.2 Distributed Logging
- Logs stored locally on each node/service
- Query requires accessing multiple locations
- Better for high-throughput, low-latency needs
- **Tools**: Fluentd, Filebeat, Promtail as log shippers

### 1.3 Hybrid Approach (Recommended)
- Real-time logs: Ship to Loki/Elasticsearch for live querying
- Historical logs: Archive to object storage (S3/MinIO) for long-term retention
- Debug logs: Keep locally for recent debugging; ship on demand

---

## 2. Log Shipping Agents

### 2.1 Fluentd
- Unified logging layer with 500+ plugins
- Buffering and retry for reliability
- Filter plugins for log transformation
- Kubernetes native (DaemonSet deployment)
- Low resource footprint

### 2.2 Filebeat
- Lightweight log shipper from Elastic
- Backpressure handling
- At-least-once delivery
- Module-based parsing for common formats
- Integration with Elasticsearch

### 2.3 Promtail
- Log collector for Loki
- Label-based indexing (not full-text)
- Kubernetes service discovery
- Pipeline stages for log processing
- Very low resource usage

---

## 3. Storage Backends

### 3.1 Elasticsearch
- Full-text search on log content
- Structured field querying
- Aggregation analytics
- High storage cost (~1KB per log entry)
- Best for: Interactive log analysis, complex queries

### 3.2 Loki
- Label-indexed (not full-text indexed)
- 10x cheaper storage than Elasticsearch
- Query via LogQL (Prometheus-inspired)
- Integrates natively with Grafana
- Best for: Cost-effective log aggregation with Grafana

### 3.3 ClickHouse
- Column-oriented for analytical log queries
- Very fast aggregation queries
- High compression ratio
- Best for: Log analytics at scale

---

## 4. Retention Tiers

| Tier | Duration | Storage | Query Speed | Cost |
|---|---|---|---|---|
| Hot | 7 days | SSD (Elasticsearch/Loki) | <1 second | High |
| Warm | 30 days | HDD (Elasticsearch/Loki) | <5 seconds | Medium |
| Cold | 90 days | Object storage (S3) | Minutes | Low |
| Archive | 1+ years | Glacier/MinIO | Hours | Very Low |

---

## 5. Cost Optimization

### 5.1 Log Volume Reduction
- **Sampling**: Log 100% of errors, 10% of info-level logs
- **Deduplication**: Remove repeated log entries
- **Compression**: GZIP/ZSTD before shipping
- **Structured Format**: JSON is more compact than free-form text

### 5.2 Storage Optimization
- **Index Lifecycle Management**: Automatic tier rotation
- **Field Mapping**: Only index fields that are actually queried
- **Delete Policies**: Auto-delete old logs based on retention
- **Shrink Indices**: Merge small indices into larger ones

---

## 6. Log Analysis for Recommendation Systems

### 6.1 Key Log Types
- **Request Logs**: Every recommendation request/response
- **Model Logs**: Inference latency, prediction confidence, model version
- **Feature Logs**: Feature freshness, missing features, default values
- **Error Logs**: Service failures, timeouts, data validation errors
- **Audit Logs**: Security events, model deployments, configuration changes

### 6.2 Log-Based Alerting
- Error rate spike in recommendation logs
- Model inference latency increase
- Feature store timeout frequency
- Unusual request pattern detection
