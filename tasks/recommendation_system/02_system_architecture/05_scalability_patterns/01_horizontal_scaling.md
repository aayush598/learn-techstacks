# Horizontal Scaling for Recommendation Systems

## 1. Scaling Principles

### 1.1 Stateless Service Design
- No session state stored in application memory
- All state externalized to databases or caches
- Any instance can handle any request
- Enables arbitrary horizontal scaling
- Health checks validate instance readiness

### 1.2 Scaling Dimensions
- **CPU Scaling**: Add instances when CPU utilization >70%
- **Memory Scaling**: Add instances when memory utilization >80%
- **GPU Scaling**: Add GPU instances when inference queue grows
- **Network Scaling**: Add instances when network bandwidth approaches limits
- **Storage Scaling**: Shard databases, add read replicas

### 1.3 Auto-Scaling Policies
```yaml
# CPU-based scaling
min_replicas: 3
max_replicas: 50
target_cpu_utilization: 70%
scale_up_stabilization: 60s
scale_down_stabilization: 300s

# Custom metric scaling (QPS)
min_replicas: 3
max_replicas: 100
target_metrics:
  - metric: requests_per_second
    target: 1000  # per replica
  - metric: latency_p99_ms
    target: 200
```

---

## 2. Database Connection Pooling

### 2.1 Connection Pool Configuration
- **Pool Size**: Number of connections per instance
  - Calculation: (2 × CPU cores) + effective_spindle_count
  - Typical: 10-50 connections per instance
- **Max Overflow**: Additional connections beyond pool size
- **Connection Timeout**: Maximum wait for a connection
- **Idle Timeout**: Close connections idle beyond timeout
- **Max Lifetime**: Maximum connection age before recycling

### 2.2 Connection Pooling Tools
- **PgBouncer**: PostgreSQL connection pooler
- **ProxySQL**: MySQL proxy and pooler
- **HikariCP**: JDBC connection pool (Java)
- **asyncpg**: Python async connection pool
- **PgCat**: PostgreSQL proxy with pooling and load balancing

### 2.3 Connection Pool Monitoring
- Active connections vs pool size
- Connection wait time (time waiting for available connection)
- Connection error rate
- Idle connections
- Connection leak detection

---

## 3. Distributed Caching for Scale

### 3.1 Redis Cluster Architecture
- **Sharding**: 16,384 hash slots distributed across nodes
- **Replication**: Each master has at least one replica
- **Failover**: Automatic failover on master failure
- **Consistency**: Eventually consistent (async replication)

### 3.2 Redis Cluster Sizing
```
Cache memory per key: ~500 bytes average
Number of active users: 10M
Features per user: 20 features
Total keys: 10M × 20 = 200M keys
Total memory: 200M × 500 bytes = 100GB
With overhead (1.5x): 150GB
Redis nodes (32GB each): 5 nodes minimum
```

### 3.3 Consistent Hashing
- Maps cache keys to positions on a hash ring
- Each cache node responsible for a range of the ring
- Adding/removing nodes only affects neighboring keys
- Minimizes cache redistribution on scaling events

---

## 4. Load Balancing Strategies

### 4.1 Application-Level Load Balancing
- **Round Robin**: Distribute requests evenly
- **Weighted Round Robin**: Distribute based on instance capacity
- **Least Connections**: Route to instance with fewest active connections
- **Consistent Hashing**: Route by user_id for cache locality

### 4.2 Infrastructure Load Balancing
- **NGINX**: High-performance L4/L7 load balancer
- **HAProxy**: Enterprise-grade TCP/HTTP load balancer
- **Envoy**: Modern L4/L7 proxy with advanced features
- **Kubernetes Services**: Built-in load balancing for pod-to-pod

### 4.3 Load Balancing for ML Inference
- **GPU-Aware Routing**: Route to instances with available GPU memory
- **Model-Aware Routing**: Route requests to instances loaded with correct model
- **Batch-Aware Routing**: Route batch requests to dedicated batch instances
- **Priority Routing**: Route high-priority requests to less-loaded instances

---

## 5. Database Scaling Strategies

### 5.1 Read Replicas
- Offload read queries from primary database
- Scale reads linearly with number of replicas
- Eventual consistency (async replication)
- Use for: Feature queries, user profile reads, item metadata reads

### 5.2 Connection Multiplexing
- Proxy layer manages database connections
- Multiple application instances share fewer database connections
- Reduces connection overhead on database
- Tools: PgBouncer, ProxySQL

### 5.3 Query Optimization
- **Indexing**: Add indexes for frequently queried columns
- **Query Plans**: Analyze and optimize slow queries
- **Materialized Views**: Pre-compute expensive aggregations
- **Partitioning**: Partition large tables by time or entity

---

## 6. Scaling ML Model Serving

### 6.1 Horizontal GPU Scaling
- Add GPU instances as inference demand increases
- Use Kubernetes GPU scheduling for automatic allocation
- Model sharding for models too large for single GPU
- Multi-GPU serving with model parallelism

### 6.2 GPU Memory Optimization
- **Model Quantization**: FP32 → FP16 → INT8 (2-4x memory reduction)
- **Model Pruning**: Remove unnecessary parameters
- **Batching**: Serve multiple requests in single GPU forward pass
- **Multi-Model GPU**: Share GPU across multiple small models (MIG)

### 6.3 Inference Auto-Scaling
```
Scaling Triggers:
  - GPU utilization > 80%: Scale up
  - Inference queue depth > 10: Scale up
  - P99 latency > 100ms: Scale up
  - GPU utilization < 30% for 10min: Scale down
  - Queue depth < 2 for 5min: Scale down
```
