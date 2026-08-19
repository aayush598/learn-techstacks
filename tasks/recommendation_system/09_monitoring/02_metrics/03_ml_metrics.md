# ML Metrics for Recommendation Monitoring

## 1. Prediction Metrics

### 1.1 Latency Distribution
- **P50 Latency**: Median inference time (target: <50ms)
- **P95 Latency**: 95th percentile (target: <100ms)
- **P99 Latency**: 99th percentile (target: <200ms)
- **Latency Histogram**: Full distribution for capacity planning

### 1.2 Throughput
- **Requests Per Second**: Total inference QPS
- **Concurrent Inferences**: Active parallel predictions
- **GPU Utilization**: Percentage of GPU capacity used
- **Batch Efficiency**: Actual batch size vs optimal batch size

### 1.3 Prediction Quality
- **Confidence Distribution**: Histogram of model confidence scores
- **Prediction Diversity**: Entropy of predicted scores
- **Score Distribution**: Mean, variance, skewness of predictions
- **Calibration**: Predicted probability vs actual outcome alignment

---

## 2. Feature Metrics

### 2.1 Feature Freshness
- **Time Since Update**: Age of each feature in online store
- **Freshness SLA Compliance**: Percentage of features within SLA
- **Stale Feature Count**: Number of features exceeding freshness threshold
- **Freshness Trend**: Feature freshness over time

### 2.2 Feature Quality
- **Missing Value Rate**: Percentage of null/missing features per request
- **Default Value Usage**: How often fallback/default features are used
- **Feature Variance**: Distribution of feature values over time
- **Feature Correlation Changes**: Unexpected correlation shifts

### 2.3 Feature Coverage
- **Feature Hit Rate**: Percentage of requested features found in store
- **Feature Computation Success Rate**: Percentage of features computed successfully
- **Feature Pipeline Lag**: Delay between event and feature availability

---

## 3. Model Health Metrics

### 3.1 Model Availability
- **Model Loading Time**: Time to load model into GPU memory
- **Model Unavailability Rate**: Percentage of time model is unavailable
- **Model Version Mismatch**: Serving requests with wrong model version
- **Cold Start Count**: Number of model cold starts

### 3.2 Model Performance
- **Online A/B Metrics**: CTR, conversion, engagement per model version
- **Prediction vs Actual Gap**: Difference between predicted and observed outcomes
- **Model Staleness**: Time since last model retraining
- **Inference Error Rate**: Percentage of failed inference requests

---

## 4. Training Metrics

### 4.1 Training Progress
- **Training Loss**: Loss curve over epochs
- **Validation Loss**: Validation loss for overfitting detection
- **Learning Rate Schedule**: Current learning rate
- **Gradient Norms**: Gradient clipping effectiveness

### 4.2 Training Quality
- **Offline Evaluation Metrics**: NDCG, Precision, Recall on validation set
- **Convergence Speed**: Epochs to reach target metric
- **Hyperparameter Stability**: Sensitivity to hyperparameter changes
- **Cross-validation Variance**: Variance across CV folds

---

## 5. Prometheus Metric Examples

### 5.1 Counter Metrics
```
recommendation_requests_total{endpoint="home", status="success"}
recommendation_requests_total{endpoint="home", status="error"}
model_inference_errors_total{model="ranking_v4", error_type="timeout"}
feature_computation_errors_total{feature_group="user_behavior", error_type="missing"}
```

### 5.2 Histogram Metrics
```
recommendation_latency_seconds_bucket{endpoint="home"}
model_inference_latency_seconds_bucket{model="ranking_v4"}
feature_retrieval_latency_seconds_bucket{feature_group="user_features"}
```

### 5.3 Gauge Metrics
```
model_gpu_utilization_ratio{model="ranking_v4"}
feature_store_connected{feature_store="redis-primary"}
active_model_version{model="ranking", version="v4.2.1"}
```

---

## 6. Dashboard Design for ML Metrics

### 6.1 Model Health Dashboard
- Model inference latency (P50, P95, P99) over time
- Model error rate over time
- GPU utilization over time
- Model version and staleness indicator
- Active experiments and their metrics

### 6.2 Feature Health Dashboard
- Feature freshness heatmap (features × time)
- Feature missing rate per feature group
- Feature store connection health
- Feature computation pipeline status
- Feature distribution drift alerts

### 6.3 Prediction Quality Dashboard
- Online CTR/conversion over time
- Prediction confidence distribution
- Recommendation diversity score
- Coverage metrics (% of catalog recommended)
- User engagement with recommendations
