# Log Retention Strategy for Recommendation Systems

## 1. Overview

Log retention defines how long log data is stored, in what format, and under what access patterns. For recommendation systems, log retention directly impacts model retraining (historical feature/prediction logs), compliance (audit trails), debugging (recent incident analysis), and cost (storage is a major infrastructure expense). A poorly designed retention strategy either wastes money or loses critical data.

### 1.1 The Retention Tension

- **ML teams** want indefinite retention for model analysis and offline experiments
- **Compliance teams** mandate minimum retention for regulatory audits
- **Finance teams** want aggressive deletion to control costs
- **SRE teams** need fast access to recent logs for incident response

The retention strategy must balance these competing requirements.

### 1.2 Cost Impact

For a mid-scale recommendation system (100M daily active users):

| Log Type | Daily Volume | Daily Cost (Hot) | Daily Cost (Cold) |
|---|---|---|---|
| Request/Response logs | 2TB | $60 | $2 |
| Model prediction logs | 5TB | $150 | $5 |
| User event logs | 10TB | $300 | $10 |
| Infrastructure logs | 1TB | $30 | $1 |
| **Total** | **18TB** | **$540/day** | **$18/day** |

At these volumes, a well-tiered retention strategy can save $500K+ annually.

---

## 2. Hot/Warm/Cold Storage Tiers

### 2.1 Hot Tier (0–7 Days)

**Purpose:** Real-time debugging, active incident investigation, live dashboards.

**Storage characteristics:**
- **Media:** SSD (NVMe preferred)
- **Database:** Elasticsearch/OpenSearch with replicas, ClickHouse with full indexing
- **Access latency:** <100ms for any query
- **Cost:** $0.10–0.30 per GB stored per month

**Data retained:**
- 100% of error and warning logs
- 100% of model prediction logs (for active debugging)
- 100% of user event logs
- 100% of all request/response logs

**Optimization strategies:**
- Real-time indexing with aggressive buffer tuning
- No compaction or merging (maximize query speed)
- Full replication (2–3 replicas) for availability
- Memory-mapped indexes for hot data

### 2.2 Warm Tier (7–90 Days)

**Purpose:** Historical analysis, weekly reports, model feature analysis.

**Storage characteristics:**
- **Media:** HDD or cold SSD
- **Database:** Force-merged indices with reduced replicas
- **Access latency:** 1–10 seconds
- **Cost:** $0.03–0.10 per GB stored per month

**Data retained:**
- 100% of error and warning logs
- 20–50% of model prediction logs (sampled)
- 50% of user event logs (sampled by event type)
- 50% of request/response logs (sampled)

**Optimization strategies:**
- Force-merge indices to single segment (reduces file count by 10–50x)
- Remove replicas (rely on snapshots for durability)
- Enable best_compression codec (30–50% storage reduction)
- Disable real-time refresh (refresh every 30–60 seconds)

### 2.3 Cold Tier (90–365 Days)

**Purpose:** Compliance audits, long-term model analysis, annual reporting.

**Storage characteristics:**
- **Media:** Object storage (S3, GCS, Azure Blob)
- **Database:** Searchable snapshots, Parquet files, or compressed JSON
- **Access latency:** 30–300 seconds for rehydration
- **Cost:** $0.01–0.04 per GB stored per month

**Data retained:**
- 100% of error logs (compliance requirement)
- 10% of model prediction logs (statistical sampling)
- 10% of user event logs (aggregated daily summaries)
- 100% of audit/security logs

**Optimization strategies:**
- Compress with Zstandard (ratio 10:1 to 20:1 for log data)
- Convert to columnar formats (Parquet) for efficient analytical queries
- Partition by date and service for targeted retrieval
- Implement lazy indexing (index on first query)

### 2.4 Archive Tier (>1 Year)

**Purpose:** Legal holds, regulatory compliance, historical reference.

**Storage characteristics:**
- **Media:** Glacier Deep Archive, GCS Coldline, tape
- **Access latency:** Hours to days
- **Cost:** $0.001–0.004 per GB stored per month

**Data retained:**
- Compliance-required logs (varies by regulation)
- Aggregated daily summaries (all log types)
- Model performance historical reports

---

## 3. Compression Strategies

### 3.1 Compression Algorithms Comparison

| Algorithm | Ratio | Speed | CPU Usage | Best For |
|---|---|---|---|---|
| LZ4 | 2–3x | Very fast | Low | Hot tier (real-time) |
| Zstandard | 5–10x | Fast | Medium | Warm tier |
| Gzip (level 6) | 3–5x | Medium | Medium | Cold tier transfer |
| Brotli | 5–8x | Slow | High | Cold storage |
| Zstd (level 19) | 10–20x | Slow | High | Archive tier |

### 3.2 Compression Recommendations by Tier

- **Hot tier:** LZ4 for index segments; Zstandard for bulk storage
- **Warm tier:** Zstandard (level 3–5) for index storage; LZ4 for query results
- **Cold tier:** Zstandard (level 10–19) for archival; Parquet with Snappy for analytics
- **Archive tier:** Zstandard maximum compression or Brotli

### 3.3 Compression-Sensitive Log Patterns

Logs with high compression ratios:
- Timestamped logs (high temporal locality)
- Repeated service names and log levels
- Structured JSON with consistent field names
- Error stack traces (repetitive across errors)

Logs with low compression ratios:
- Random request IDs and trace IDs
- Feature vectors with high-entropy float values
- User-generated content in log messages
- Binary payloads or embedded files

---

## 4. Archival to Object Storage

### 4.1 Archival Pipeline Architecture

```
Hot Storage → Export Job → Compression → Format Conversion → Object Storage
     │                        │                │                    │
  (daily)              (Zstandard)        (Parquet/JSON)     (S3/GCS)
     │                                                         │
     │                              ┌──────────────────────────┘
     │                              │
     └──────────── Retention Policy ◄┘
                   (lifecycle rules)
```

### 4.2 Object Storage Lifecycle Policies

Configure automated lifecycle rules on object storage:

```json
{
  "rules": [
    {
      "id": "transition-to-cold",
      "filter": { "prefix": "logs/warm/" },
      "transitions": [
        { "days": 90, "storage_class": "GLACIER" },
        { "days": 365, "storage_class": "DEEP_ARCHIVE" }
      ],
      "expiration": { "days": 2555 }
    }
  ]
}
```

### 4.3 Archival Formats

| Format | Query Capability | Compression | Best For |
|---|---|---|---|
| JSON (gzipped) | Full-text search | Medium | Raw log preservation |
| Parquet | Columnar analytics | High | Analytical queries |
| Apache Arrow | In-memory analytics | Medium | ML pipeline input |
| Avro | Schema evolution | High | Long-term archival |
| ORC | Hive/Presto analytics | High | Data lake queries |

### 4.4 Metadata Catalog

Maintain a catalog of archived logs for discoverability:

```json
{
  "archive_id": "rec-logs-2026-Q2",
  "date_range": ["2026-04-01", "2026-06-30"],
  "log_types": ["prediction", "event", "error"],
  "total_size_gb": 1250,
  "compressed_size_gb": 85,
  "record_count": 2.5e9,
  "schema_version": "v3.2",
  "location": "s3://logs-archive/rec/2026/Q2/",
  "format": "parquet+zstd",
  "retention_expiry": "2031-06-30"
}
```

---

## 5. Compliance-Driven Retention

### 5.1 Regulatory Requirements

| Regulation | Minimum Retention | Maximum Retention | Log Types Required |
|---|---|---|---|
| GDPR | No minimum (purpose limitation) | Until purpose fulfilled | Processing records, consent logs |
| CCPA | No minimum | Reasonable period | Sale/disclosure logs |
| SOX | 7 years | No maximum | Financial transaction logs |
| HIPAA | 6 years | No maximum | PHI access logs |
| PCI DSS | 1 year | No maximum | Card transaction logs |
| SOC 2 | 1 year | No maximum | Security event logs |

### 5.2 GDPR-Specific Considerations for Recommendation Logs

- **Purpose limitation**: Log retention must be tied to a documented purpose
- **Data minimization**: Retain only what's necessary for each purpose
- **Right to erasure**: Must be able to delete individual user's logs across all tiers
- **Log pseudonymization**: Replace direct identifiers with pseudonymous tokens
- **Cross-border transfer**: Ensure log storage location complies with data residency

### 5.3 Retention Policy Template

```
Log Type: user_event_clicks
Purpose: Model training and A/B test analysis
Minimum Retention: 30 days (model training needs)
Maximum Retention: 90 days (raw events)
Aggregated Retention: 2 years (daily summaries)
Compliance Requirement: GDPR pseudonymization
Access Control: ML team (read), SRE team (read/write), Compliance (read)
Purge Method: Cryptographic erasure (key deletion for encrypted logs)
Purge Schedule: Weekly automated purge of expired logs
Exception Process: Legal hold can extend retention indefinitely
```

---

## 6. Log Rotation

### 6.1 Rotation Strategies

**Time-based rotation:**
- Rotate log files every hour or daily
- Align rotation with index creation in Elasticsearch
- Ensure rotation boundaries are timezone-aware (always UTC)

**Size-based rotation:**
- Rotate when file exceeds threshold (e.g., 100MB)
- Prevents unbounded file growth
- Use in conjunction with time-based rotation

**Event-based rotation:**
- Rotate on specific events (deployment, configuration change)
- Provides clear boundaries for log analysis

### 6.2 Rotation Configuration

Key parameters:
- **Max file size**: 50–200MB for local files
- **Max file count**: Keep 7–30 rotated files locally
- **Compression on rotation**: Compress rotated files immediately
- **Graceful rotation**: Use signals (SIGHUP) or file handle switching

### 6.3 Container-Specific Considerations

In Kubernetes environments:
- **Use emptyDir volumes** for log buffering (survives pod restarts on same node)
- **Configure logrotate** as a sidecar or DaemonSet
- **Use journald driver** with max-size and max-file options
- **Monitor /var/log usage** to prevent node disk exhaustion

---

## 7. Cost Analysis Per Log Type

### 7.1 Cost Model Framework

```
Total Cost = Ingestion Cost + Storage Cost + Query Cost + Transfer Cost

Where:
- Ingestion Cost = Volume × Ingestion Rate
- Storage Cost = Volume × Retention Days × Cost per GB/day × Tier Weight
- Query Cost = Query Volume × Query Compute Cost
- Transfer Cost = Cross-region/Egress Volume × Transfer Rate
```

### 7.2 Cost Optimization Decision Tree

```
Is the log type queried in real-time?
├── Yes → Keep in hot tier (7 days)
│   ├── Is it high-volume (>1TB/day)?
│   │   └── Apply sampling (10–50%)
│   └── Can it be aggregated?
│       └── Pre-aggregate and store summary
└── No → Move to warm tier after 24 hours
    ├── Is it needed for compliance?
    │   └── Archive to cold tier with full retention
    ├── Is it needed for ML training?
    │   └── Keep 30 days raw, then aggregate
    └── Can it be sampled?
        └── Apply aggressive sampling (1–10%)
```

### 7.3 Cost Reduction Tactics

| Tactic | Savings | Implementation Effort |
|---|---|---|
| Aggressive hot→warm transition (24h) | 40–60% | Low |
| Log sampling at source (50%) | 30–50% | Low |
| Compression optimization | 20–40% | Medium |
| Aggregation before archival | 50–80% | High |
| Per-type retention policies | 30–50% | Medium |
| Object storage lifecycle policies | 60–80% | Low |

### 7.4 Monthly Cost Tracking

Maintain a monthly log cost dashboard:

```
| Log Type       | Hot Cost | Warm Cost | Cold Cost | Total    | % of Budget |
|----------------|----------|-----------|-----------|----------|-------------|
| Request logs   | $2,400   | $800      | $50       | $3,250   | 25%         |
| Prediction logs| $3,600   | $600      | $30       | $4,230   | 33%         |
| Event logs     | $1,800   | $400      | $20       | $2,220   | 17%         |
| Infra logs     | $900     | $200      | $10       | $1,110   | 9%          |
| Audit logs     | $300     | $150      | $80       | $530     | 4%          |
| Debug logs     | $600     | $0        | $0        | $600     | 5%          |
| **Total**      | **$9,600**| **$2,150**| **$190**  | **$11,940**| **100%**  |
```

---

## 8. Automated Retention Management

### 8.1 Retention Policy Engine

Implement a centralized retention policy engine:

1. **Policy definition**: YAML/JSON files defining retention per log type, environment, and compliance requirement
2. **Policy enforcement**: Automated jobs that delete/rotate data based on policy
3. **Policy auditing**: Track policy changes and their impact on storage costs
4. **Exception handling**: Legal hold overrides that suspend automatic deletion

### 8.2 Purge Automation

```
Daily Purge Job:
  1. Query retention policies from configuration store
  2. For each log type:
     a. Identify data exceeding hot tier retention
     b. Export to warm tier (if sampled)
     c. Delete from hot tier
  3. Weekly: Identify warm tier data exceeding retention
     a. Export to cold tier
     b. Compress and archive
     c. Delete from warm tier
  4. Monthly: Identify cold tier data exceeding retention
     a. Transition to archive tier
     b. Delete from cold tier
```

### 8.3 Retention Monitoring

Alert on:
- Log volume exceeding projected growth (>20% above forecast)
- Retention policy violations (data older than max retention in hot tier)
- Storage cost exceeding budget threshold
- Purge job failures or delays

---

## 9. Disaster Recovery for Log Storage

### 9.1 Backup Strategy

- **Hot tier**: Replicate across availability zones; daily snapshots
- **Warm tier**: Cross-region replication; weekly snapshots
- **Cold tier**: Object storage versioning; cross-region replication
- **Archive tier**: Multiple copies in different geographic regions

### 9.2 Recovery Objectives

| Tier | RPO | RTO | Impact |
|---|---|---|---|
| Hot | 0 (synchronous replication) | <1 hour | Dashboard and alerting gaps |
| Warm | 1 hour (async replication) | <4 hours | Historical analysis gaps |
| Cold | 24 hours (daily snapshots) | <24 hours | Audit and compliance gaps |
| Archive | 7 days (weekly backups) | <72 hours | Historical reference gaps |

---

## 10. Key Takeaways

1. **Implement tiered storage** — hot/warm/cold/archive with automated lifecycle management
2. **Sample aggressively for high-volume logs** — 10–50% sampling is sufficient for most analytics
3. **Compress at every tier** — Zstandard provides the best ratio/speed tradeoff
4. **Archive to object storage** with proper lifecycle policies to minimize costs
5. **Maintain a cost dashboard** per log type to track and optimize spending
6. **Compliance-driven retention** should be defined per log type with documented purposes
7. **Automate purge jobs** and monitor for retention violations
8. **Never delete without verification** — use soft-delete with a grace period
9. **Aggregate before archival** — daily summaries provide 80% of the value at 1% of the storage
10. **Test recovery procedures** quarterly — an untested backup is not a backup
