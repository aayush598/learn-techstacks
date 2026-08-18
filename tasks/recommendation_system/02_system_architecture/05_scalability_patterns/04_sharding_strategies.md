# Sharding Strategies for Recommendation Systems

## 1. Database Sharding

### 1.1 Shard Key Selection

**User ID Sharding**:
- All data for a user on same shard
- Enables efficient user-centric queries
- Risk: Hot shards for power users
- Best for: User profiles, user interaction history

**Item ID Sharding**:
- All data for an item on same shard
- Enables efficient item-centric queries
- Risk: Hot shards for popular items
- Best for: Item metadata, item statistics

**Geographic Sharding**:
- Data sharded by user location
- Reduces cross-region latency
- Enables data residency compliance
- Best for: Regional recommendation systems

**Hash-Based Sharding**:
- Consistent hash of entity ID determines shard
- Even distribution across shards
- No hot spots (statistically)
- Best for: General-purpose sharding

### 1.2 Sharding Strategies

**Hash-Based Sharding**:
```
shard_id = hash(entity_id) % num_shards
```
- Even distribution
- No range queries across shards
- Adding shards requires resharding

**Range-Based Sharding**:
```
shard_id = range_lookup(entity_id)
```
- Supports range queries
- Risk of hot spots in sequential IDs
- Easier to add new shards

**Directory-Based Sharding**:
```
shard_id = directory_lookup(entity_id)
```
- Maximum flexibility
- Additional lookup overhead
- Can move entities between shards

---

## 2. Cross-Shard Query Handling

### 2.1 Scatter-Gather
- Send query to all shards
- Gather and merge results
- Used when: Query doesn't have shard key
- Drawback: Latency = slowest shard response

### 2.2 Index Tables
- Maintain cross-shard index in separate table
- Index maps entity ID to shard ID
- Used for: Finding which shard contains specific data
- Update index on shard changes

### 2.3 Materialized Views
- Pre-compute cross-shard aggregations
- Store in single table for fast queries
- Used for: Analytics dashboards, reporting
- Update incrementally or on schedule

---

## 3. Shard Rebalancing

### 3.1 Online Resharding
- Add new shard while system is running
- Migrate data from existing shards to new shard
- Update routing rules atomically
- No downtime required
- Process: Add shard → Migrate data → Update routing → Remove old data

### 3.2 Resharding Without Downtime
1. Add new shard to cluster
2. Start dual-write: write to both old and new shard
3. Backfill data from old shard to new shard
4. Verify data consistency
5. Switch reads to new shard
6. Stop writing to old shard
7. Remove old shard

### 3.3 Resharding Challenges
- **Data Migration**: Moving large volumes of data while serving traffic
- **Consistency**: Ensuring no data loss during migration
- **Routing**: Updating routing rules without downtime
- **Performance**: Migration may impact query performance

---

## 4. Sharded Feature Store

### 4.1 Feature Sharding by Entity
- User features sharded by user_id
- Item features sharded by item_id
- Interaction features sharded by user_id (user-centric queries)

### 4.2 Feature Cache Sharding
- Redis Cluster with consistent hashing
- Hash slot assignment based on feature key
- Automatic failover on node failure
- Resharding on capacity changes

### 4.3 Sharded Feature Computation
- Partition feature computation by entity
- Each worker processes a subset of entities
- Enables horizontal scaling of feature pipelines
- Combines results for global features (e.g., trending)

---

## 5. Sharded Model Serving

### 5.1 Model Sharding
- Large models split across multiple GPUs
- Each GPU holds a portion of model parameters
- Forward pass requires communication between GPUs
- Used for: Models too large for single GPU memory

### 5.2 Model Replica Sharding
- Different model replicas on different GPU instances
- Load balancer distributes inference requests
- Each replica handles subset of requests
- Enables horizontal scaling of inference

### 5.3 Feature Vector Sharding
- Feature vectors split across multiple Redis instances
- Each instance holds subset of feature dimensions
- Assemble complete vector from multiple instances
- Trade-off: Memory savings vs additional network calls
