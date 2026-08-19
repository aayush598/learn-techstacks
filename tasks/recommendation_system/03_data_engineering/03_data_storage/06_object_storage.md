# Object Storage — S3/MinIO for Recommendation System Artifacts

## 1. Role of Object Storage in Recommendation Systems

### 1.1 What Goes in Object Storage

| Data Type | Example | Access Pattern | Typical Size |
|-----------|---------|---------------|-------------|
| **Model Artifacts** | Trained model weights (PyTorch, TensorFlow) | Write-once, read-many (training → serving) | 100MB–10GB per model version |
| **Training Data Snapshots** | Parquet/CSV files of interaction data | Write-once, read-many (batch training) | 10GB–1TB per snapshot |
| **Feature Snapshots** | Pre-computed feature matrices | Write-daily, read-by-training-pipeline | 50GB–500GB |
| **Embedding Files** | Pre-computed user/item embeddings (NumPy, HDF5) | Write-daily, read-by-serving | 10GB–100GB |
| **Similarity Matrices** | Pre-computed item-item similarities | Write-daily, read-by-retrieval | 50GB–500GB |
| **Item Media** | Product images, video thumbnails | Write-once, read-frequently (CDN-backed) | 100KB–10MB per file |
| **ML Experiment Data** | Hyperparameter configs, metrics logs | Write-per-experiment, read-rarely | 1KB–1MB per experiment |
| **Backup Data** | Database backups, model checkpoints | Write-periodic, read-on-emergency | 10GB–1TB per backup |
| **Data Lake** | Raw event logs, enriched datasets | Write-streaming, read-batch | 1TB–100TB per year |

### 1.2 S3 vs MinIO Comparison

| Aspect | AWS S3 | MinIO (Self-Hosted) |
|--------|--------|---------------------|
| Managed Service | Fully managed by AWS | Self-managed on Kubernetes/VMs |
| API Compatibility | S3 API (de facto standard) | S3 API compatible |
| Durability | 99.999999999% (11 9's) | Configurable (replication-based) |
| Cost Model | Pay-per-use (storage + requests + transfer) | Fixed infrastructure cost |
| Latency | 10–100ms (first byte) | 1–5ms (same data center) |
| Max Object Size | 5 TB | 5 TB |
| Best For | Cloud-native deployments, variable workloads | On-premise, data sovereignty, predictable workloads |
| Integration | Native AWS ecosystem (SageMaker, Lambda, etc.) | Kubernetes-native, S3-compatible tools |

---

## 2. Model Artifact Management

### 2.1 Model Artifact Directory Structure

```
s3://recsys-models/
├── production/
│   ├── deep_ranking/
│   │   ├── v2.3.0/
│   │   │   ├── model.pt                    # Model weights
│   │   │   ├── config.json                 # Model configuration
│   │   │   ├── feature_schema.json         # Expected input features
│   │   │   ├── scaler_params.json          # Feature scaling parameters
│   │   │   ├── encoder_params.json         # Categorical encoder state
│   │   │   ├── evaluation_report.json      # Offline evaluation metrics
│   │   │   ├── training_data_hash.txt      # Hash of training data snapshot
│   │   │   └── deployment_manifest.yaml    # Deployment configuration
│   │   └── v2.3.1/
│   │       └── ...
│   └── candidate_generation/
│       └── v1.5.0/
│           └── ...
├── staging/
│   └── experimental/
│       └── transformer_ranking_v0.1/
├── archived/
│   └── deprecated_models/
├── training_data/
│   ├── snapshots/
│   │   ├── 2026-08-15/
│   │   │   ├── interactions.parquet
│   │   │   ├── user_features.parquet
│   │   │   └── item_features.parquet
│   │   └── 2026-08-16/
│   └── embeddings/
│       ├── user_embeddings_2026-08-19.npy
│       └── item_embeddings_2026-08-19.npy
└── backups/
    ├── model_checkpoints/
    └── database_backups/
```

### 2.2 Model Versioning Strategy

- **Immutable Versions**: Once a model version is written to object storage, it must never be modified. New versions create new directories.
- **Metadata Tagging**: Each model version directory contains a `metadata.json` with training configuration, data version, metrics, and deployment status.
- **Pointer Files**: A `latest` pointer file in each model family's directory points to the current production version, enabling fast lookups.
- **Retention**: Keep the last 10 model versions in standard storage; move older versions to infrequent access or archive after 90 days.

---

## 3. Data Lake Architecture

### 3.1 Data Lake Layers

| Layer | Format | Partitioning | Retention | Access Pattern |
|-------|--------|-------------|-----------|---------------|
| **Raw (Bronze)** | JSON/CSV/Avro | By date + source | 1 year | Write-once, rare reads |
| **Processed (Silver)** | Parquet/ORC | By date + entity | 2 years | Write-daily, read-by-training |
| **Curated (Gold)** | Parquet + Delta Lake | By date + feature_group | Indefinite | Write-daily, read-frequently |
| **Serving** | Parquet + embedding files | By entity ID | 90 days | Read-intensive (training) |

### 3.2 Partitioning Strategy

```
s3://recsys-datalake/
├── raw/
│   ├── interactions/
│   │   ├── year=2026/month=08/day=19/
│   │   │   ├── source=kafka/
│   │   │   │   ├── part-00000.avro
│   │   │   │   └── part-00001.avro
│   │   │   └── source=clickstream/
│   ├── user_events/
│   │   ├── year=2026/month=08/day=19/
├── processed/
│   ├── user_features/
│   │   ├── date=2026-08-19/
│   │   │   ├── user_features.parquet
│   │   │   └── _SUCCESS
│   ├── item_features/
│   │   ├── date=2026-08-19/
│   ├── interactions_enriched/
│   │   ├── date=2026-08-19/
├── curated/
│   ├── training_datasets/
│   │   ├── version=v2026.08.19/
│   │   │   ├── train/
│   │   │   ├── validation/
│   │   │   └── test/
│   └── feature_tables/
│       ├── user_feature_table/
│       └── item_feature_table/
```

### 3.3 File Format Optimization

| Format | Compression | Columnar | Schema Evolution | Best For |
|--------|------------|---------|-----------------|----------|
| **Parquet** | Snappy/Zstd | Yes | Limited (new columns) | Training data, feature tables |
| **ORC** | Zlib/Zstd | Yes | Limited | Hive-based analytics |
| **Avro** | Snappy/Deflate | No | Full (schema evolution) | Raw event ingestion |
| **Delta Lake** | Parquet-based | Yes | Full + ACID | Curated datasets requiring transactions |

### 3.4 Z-Ordering for Query Performance

For frequently filtered columns in Parquet files, apply Z-ordering to co-locate related data:

```python
# Z-order by user_id and timestamp for efficient user-history queries
df.write \
  .partitionBy("date") \
  .option("dataSkippingOrderColumns", "user_id,timestamp") \
  .parquet("s3://recsys-datalake/processed/interactions_enriched/")

# This ensures that data for the same user across different events
# is physically co-located, reducing I/O for user-history queries.
```

---

## 4. Image and Media Storage

### 4.1 Item Image Storage

```python
# Image storage structure
s3://recsys-media/
├── items/
│   ├── images/
│   │   ├── {item_id}/
│   │   │   ├── original/
│   │   │   │   └── image_001.jpg
│   │   │   ├── thumbnails/
│   │   │   │   ├── 100x100.jpg
│   │   │   │   ├── 300x300.jpg
│   │   │   │   └── 800x800.jpg
│   │   │   └── embeddings/
│   │   │       ├── visual_embedding.npy  # CNN-based image embedding
│   │   │       └── aesthetic_score.json
├── users/
│   ├── avatars/
│   │   └── {user_id}/
│   │       └── avatar.jpg
└── ui/
    ├── icons/
    └── backgrounds/
```

### 4.2 CDN Integration

- **CloudFront / Cloudflare**: Serve item images through a CDN with edge caching.
- **Cache-Control Headers**: Set `Cache-Control: public, max-age=86400` for item images (images change infrequently).
- **On-the-Fly Resizing**: Use Lambda@Edge or Cloudflare Workers to generate thumbnail variants on first request, then cache the generated size.

### 4.3 Image Processing Pipeline

```
Original Image Upload → S3 Event Trigger → Lambda/Worker
    ↓
Resize to Multiple Sizes (100x100, 300x300, 800x800)
    ↓
Generate Thumbnail + WebP variant
    ↓
Extract Visual Embedding (CNN model)
    ↓
Write processed images to S3 + Update metadata in catalog DB
```

---

## 5. Lifecycle Policies and Cost Optimization

### 5.1 Lifecycle Policy Configuration

```json
{
  "Rules": [
    {
      "ID": "ModelArtifactLifecycle",
      "Filter": { "Prefix": "production/" },
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 90,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 365,
          "StorageClass": "GLACIER"
        }
      ],
      "NoncurrentVersionTransitions": [
        {
          "NoncurrentDays": 30,
          "StorageClass": "STANDARD_IA"
        },
        {
          "NoncurrentDays": 90,
          "StorageClass": "GLACIER"
        }
      ]
    },
    {
      "ID": "RawDataLifecycle",
      "Filter": { "Prefix": "datalake/raw/" },
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 90,
          "StorageClass": "GLACIER"
        }
      ],
      "Expiration": {
        "Days": 365
      }
    },
    {
      "ID": "TrainingDataLifecycle",
      "Filter": { "Prefix": "training_data/snapshots/" },
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 7,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 30,
          "StorageClass": "GLACIER"
        }
      ],
      "Expiration": {
        "Days": 90
      }
    }
  ]
}
```

### 5.2 Cost Optimization Strategies

| Strategy | Expected Savings | Implementation |
|----------|-----------------|----------------|
| **Lifecycle Policies** | 40–60% on storage costs | Auto-transition to IA/Glacier/Archive |
| **Compression** | 60–80% on storage, 30–50% on transfer | Zstd/Snappy for Parquet; gzip for JSON |
| **Deduplication** | 10–30% on training data | Content-hash-based dedup before upload |
| **Right-Sizing** | 10–20% on request costs | Batch operations instead of individual PUT/GET |
| **Intelligent Tiering** | 20–40% on mixed workloads | S3 Intelligent-Tiering auto-moves to cheapest tier |
| **Cross-Region Optimization** | 30–50% on transfer costs | Replicate only to regions with active workloads |
| **Selective Replication** | 20–40% on storage costs | Replicate only production models; not staging/experimental |

### 5.3 Cost Estimation Formula

```
Monthly Storage Cost = Σ (Data Size × Storage Class Price × Days in Month)
Monthly Request Cost = Σ (Request Count × Request Type Price)
Monthly Transfer Cost = Data Transfer Out × Transfer Price

Example:
- 500 GB model artifacts at $0.023/GB (Standard) = $11.50/month
- 10 TB training data at $0.0125/GB (IA) = $125.00/month
- 500K PUT requests at $0.005/1K = $2.50/month
- 10M GET requests at $0.0004/1K = $4.00/month
- 100 GB/month transfer out at $0.09/GB = $9.00/month
Total: ~$152/month
```

---

## 6. Cross-Region Replication

### 6.1 When Cross-Region Replication is Needed

- **Disaster Recovery**: Model artifacts and training data must survive a regional outage.
- **Multi-Region Serving**: Models deployed to multiple serving regions need local copies.
- **Data Sovereignty**: Data must be stored within specific geographic regions for regulatory compliance.

### 6.2 Replication Strategies

| Strategy | RPO | Cost | Complexity | Use Case |
|----------|-----|------|-----------|----------|
| **Same-Region Replication** | Near-zero | Low | Low | High-durability within a region |
| **Cross-Region Replication (CRR)** | Minutes | Medium | Medium | DR + multi-region serving |
| **Bi-Directional CRR** | Minutes | High | High | Active-active multi-region |
| **Eventual Replication (Custom)** | Minutes–Hours | Low | High | Selective replication of specific prefixes |

### 6.3 Replication Configuration

```json
{
  "Rules": [
    {
      "ID": "ReplicateModelsToDR",
      "Status": "Enabled",
      "Filter": { "Prefix": "production/" },
      "Destination": {
        "Bucket": "arn:aws:s3:::recsys-models-dr-us-east-1",
        "StorageClass": "STANDARD"
      },
      "ReplicationTime": {
        "Status": "Enabled",
        "Time": { "Minutes": 15 }
      },
      "ReplicaModifications": {
        "Status": "Enabled"
      }
    }
  ]
}
```
