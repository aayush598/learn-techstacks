# Datadog & Snowflake Interview Patterns

## Table of Contents
1. Datadog Interview Format
2. Datadog Topics & Problems
3. Snowflake Interview Format
4. Snowflake Topics & Problems
5. Common Ground

---

## Part 1: Datadog

### 1. Datadog Interview Format

**Recruiter Screen (30 min)**
- Background, experience, motivation

**Coding Screen (60 min)**
- 1-2 algorithm problems on HackerRank / CodeSignal
- Focus on arrays, strings, time series

**On-site (4-5 rounds)**
- **Coding** (2 rounds): Algorithm + data processing
- **System Design** (1): Monitoring systems, data pipelines
- **Project Deep Dive** (1): Past experience
- **Behavioral** (1): Team fit, culture

### 2. Datadog Topics

| Topic | Frequency | Why Datadog Asks It |
|-------|-----------|-------------------|
| Arrays / Aggregation | Very High | Time series data, metrics |
| HashMaps | High | Event grouping, tagging |
| Intervals | High | Time ranges, monitoring windows |
| Sliding Window | High | Rolling metrics, rate limiting |
| Trees | Medium | Infrastructure hierarchy |
| Graphs | Medium | Service dependencies, tracing |
| Concurrency | Medium | Agent data collection, threading |

### Datadog Problem Types

**Time Series Problems:**
- Aggregate metrics over time windows
- Find outliers in data streams
- Sliding window statistics (avg, p99, max)
- Time-based event correlation

**Aggregation Problems:**
- Group metrics by tags
- Roll up data at different granularities
- Find top N hosts by CPU usage
- Pivot data by dimensions

**Monitoring Problems:**
- Alert threshold detection
- Rate limiting design
- Anomaly detection basics
- Log parsing and extraction

### Example: Sliding Window Rate Calculation
```java
public class RateCalculator {
    private final int windowSize;
    private final Queue<Long> timestamps = new LinkedList<>();

    public RateCalculator(int windowSeconds) {
        this.windowSize = windowSeconds;
    }

    public synchronized void record(long timestamp) {
        timestamps.offer(timestamp);
        // Remove old entries
        while (!timestamps.isEmpty() &&
               timestamps.peek() < timestamp - windowSize * 1000) {
            timestamps.poll();
        }
    }

    public synchronized double getRate() {
        if (timestamps.isEmpty()) return 0;
        long now = System.currentTimeMillis();
        while (!timestamps.isEmpty() &&
               timestamps.peek() < now - windowSize * 1000) {
            timestamps.poll();
        }
        return (double) timestamps.size() / windowSize;
    }
}
```

### Example: Merge Time Intervals
```java
public List<Interval> mergeIntervals(List<Interval> intervals) {
    if (intervals.isEmpty()) return new ArrayList<>();
    intervals.sort((a, b) -> a.start - b.start);
    List<Interval> merged = new ArrayList<>();
    Interval current = intervals.get(0);
    for (int i = 1; i < intervals.size(); i++) {
        Interval next = intervals.get(i);
        if (current.end >= next.start) { // overlap
            current.end = Math.max(current.end, next.end);
        } else {
            merged.add(current);
            current = next;
        }
    }
    merged.add(current);
    return merged;
}
```

---

## Part 2: Snowflake

### 1. Snowflake Interview Format

**Recruiter Screen (30 min)**
- Background and role discussion

**Technical Screen (45-60 min)**
- 1-2 SQL + algorithm problems on shared editor
- Snowflake tests SQL + coding together

**On-site (5 rounds)**
- **SQL + Algorithms** (2 rounds): SQL queries meet DSA
- **System Design** (1): Data warehousing, cloud infrastructure
- **Hiring Manager** (1): Experience and technical depth
- **Behavioral** (1): Culture fit

### 2. Snowflake Topics

| Topic | Frequency | Why Snowflake Asks It |
|-------|-----------|----------------------|
| SQL | Very High | Core product |
| Data Processing | High | ETL, data transformation |
| Arrays & Strings | High | Data parsing, format conversion |
| Trees | Medium | Query plans, optimization |
| Distributed Systems | High | Snowflake architecture |
| Compression / Encoding | Medium | Data storage efficiency |

### Snowflake Problem Types

**SQL + Algorithm Hybrid:**
- Implement a SQL-like operation in code (GROUP BY, JOIN, DISTINCT)
- Process large datasets with limited memory
- Stream processing vs batch processing

**Data Transformation:**
- Parse CSV/JSON/Parquet files
- Convert between data formats
- Validate and clean data
- Schema inference

**Distributed Systems Basics:**
- Consistent hashing
- Data partitioning strategies
- Replication and fault tolerance

### Example: In-Memory GROUP BY
```java
public Map<String, Integer> groupBy(String[] data, String delimiter) {
    Map<String, Integer> result = new HashMap<>();
    for (String line : data) {
        String[] parts = line.split(delimiter);
        if (parts.length >= 2) {
            String key = parts[0];
            int value = Integer.parseInt(parts[1]);
            result.merge(key, value, Integer::sum);
        }
    }
    return result;
}
```

### Example: Hadoop-style Word Count
```java
public Map<String, Integer> wordCount(String[] lines) {
    Map<String, Integer> counts = new HashMap<>();
    for (String line : lines) {
        String[] words = line.toLowerCase().split("\\W+");
        for (String word : words) {
            if (!word.isEmpty()) {
                counts.put(word, counts.getOrDefault(word, 0) + 1);
            }
        }
    }
    return counts;
}
```

---

## 3. Common Ground: Data-Intensive Interview Prep

### Both Companies Value
- **Data processing at scale** — handling GB/TB of data
- **Efficient algorithms** — O(n) or O(n log n) preferred
- **Streaming concepts** — Processing data as it arrives
- **Clean, maintainable code** — Production-ready
- **System design fundamentals** — Distributed systems

### Must-Know Concepts

| Concept | Datadog Relevance | Snowflake Relevance |
|---------|------------------|-------------------|
| Sliding window | Metrics, alerting | Window functions |
| Hash-based grouping | Aggregation | GROUP BY |
| Interval merging | Event correlation | Range partitioning |
| Time series | Core product | Time-based queries |
| External sorting | Log analysis | Large dataset processing |
| Bloom filters | Approximate counting | Data skipping |
| Consistent hashing | Load balancing | Data partitioning |

### Preparation Strategy

1. **Data structure mastery (40%)**
   - Arrays, HashMaps, PriorityQueues
   - Sliding window and two pointers
   - Interval problems

2. **Data processing (40%)**
   - Implement GROUP BY, JOIN, SORT in code
   - Large data handling (external memory algorithms)
   - Stream vs batch processing mindset

3. **System design (20%)**
   - Monitoring system design (Datadog)
   - Data warehouse design (Snowflake)
   - Cloud-native architecture
