# Data Warehouse for Recommendation Analytics

## 1. Data Warehouse Architecture

### 1.1 Purpose in Recommendation System
The data warehouse serves as the analytical backbone for:
- Real-time dashboards showing recommendation performance
- Historical analysis of user behavior and recommendation quality
- Business reporting (revenue impact, engagement metrics)
- Ad-hoc analysis by data scientists and analysts
- Experiment result analysis

### 1.2 Star Schema Design for Recommendations

#### Dimension Tables

**dim_user**:
- user_id (PK)
- registration_date
- country
- age_group
- gender
- subscription_tier
- acquisition_channel
- user_segment
- first_interaction_date
- last_active_date
- is_active

**dim_item**:
- item_id (PK)
- title
- category_l1
- category_l2
- category_l3
- brand
- price_bucket
- content_type
- creation_date
- is_available
- quality_score_bucket
- popularity_bucket

**dim_time**:
- time_id (PK)
- date
- hour
- day_of_week
- month
- quarter
- year
- is_weekend
- is_holiday
- season

**dim_context**:
- context_id (PK)
- device_type
- platform
- browser
- app_version
- screen_size_bucket
- network_type
- country
- city

**dim_recommendation_surface**:
- surface_id (PK)
- surface_name (home_page, detail_page, email, push, search)
- position_type (hero, carousel, grid, list)
- page_section

#### Fact Tables

**fact_impression**:
- impression_id (PK)
- user_id (FK)
- item_id (FK)
- time_id (FK)
- context_id (FK)
- surface_id (FK)
- model_version
- experiment_id
- position
- score
- was_clicked
- was_purchased
- dwell_time_ms
- revenue

**fact_daily_user_agg**:
- user_id (FK)
- date (FK)
- total_impressions
- total_clicks
- total_purchases
- total_revenue
- unique_categories_viewed
- avg_session_duration
- unique_devices_used

**fact_daily_item_agg**:
- item_id (FK)
- date (FK)
- total_impressions
- total_clicks
- total_purchases
- total_revenue
- unique_users_reached
- click_through_rate
- conversion_rate

**fact_model_performance**:
- model_version
- date (FK)
- surface_id (FK)
- total_served
- avg_latency_ms
- p95_latency_ms
- p99_latency_ms
- avg_ctr
- avg_conversion_rate
- avg_diversity_score
- ndcg_at_10
- hit_rate

---

## 2. OLAP Engine Selection

### 2.1 Apache ClickHouse
- **Architecture**: Column-oriented, MPP (massively parallel processing)
- **Performance**: Sub-second queries on billions of rows
- **Features**: Materialized views, projections, approximate query processing
- **Use Case**: Real-time analytics dashboards, user behavior analysis
- **Scale**: Handles petabytes of data
- **Best For**: High-concurrency, low-latency analytical queries

### 2.2 Apache Druid
- **Architecture**: Real-time analytics database
- **Performance**: Sub-second queries with high concurrency
- **Features**: Real-time ingestion, time-series optimization, roll-up
- **Use Case**: Real-time dashboards, time-series analytics
- **Scale**: Billions of events per day
- **Best For**: Real-time event analytics

### 2.3 DuckDB
- **Architecture**: In-process OLAP database
- **Performance**: Fast analytical queries on single node
- **Features**: SQL interface, Parquet integration, zero configuration
- **Use Case**: Ad-hoc analysis, data exploration, small-to-medium datasets
- **Scale**: Single node (up to hundreds of GB)
- **Best For**: Developer analytics, prototyping, local analysis

### 2.4 Apache Pinot
- **Architecture**: Real-time distributed OLAP
- **Features**: Upsert support, real-time and batch ingestion, star schema
- **Use Case**: User-facing analytics, real-time leaderboards
- **Best For**: Low-latency, high-concurrency analytical queries

---

## 3. Real-Time Analytics

### 3.1 Real-Time Dashboard Metrics
- **Active Users**: Current active users with recommendations
- **Recommendation QPS**: Requests per second by endpoint
- **Model Latency**: P50/P95/P99 inference latency
- **CTR (Click-Through Rate)**: Real-time CTR across recommendation surfaces
- **Error Rate**: Percentage of failed recommendation requests
- **Fallback Rate**: Percentage of requests falling back to non-personalized recommendations

### 3.2 Streaming Analytics Pipeline
```
User Events → Kafka → Flink → ClickHouse
                                  ↓
                          Real-time Dashboards
```
- **Kafka**: Event ingestion
- **Flink**: Real-time aggregation (windowed counts, averages, percentiles)
- **ClickHouse**: Storage and query engine for dashboards
- **Grafana**: Visualization layer connected to ClickHouse

### 3.3 Materialized Views in ClickHouse
```sql
-- Real-time CTR by recommendation surface
CREATE MATERIALIZED VIEW realtime_ctr
ENGINE = AggregatingMergeTree()
ORDER BY (surface_id, window_start)
AS SELECT
    surface_id,
    tumbleStart(event_time, 60) AS window_start,
    countState() AS total_impressions,
    countIfState(was_clicked) AS total_clicks
FROM fact_impression
GROUP BY surface_id, window_start;
```

---

## 4. Data Warehouse Sizing

### 4.1 Storage Estimation
- **Raw event data**: ~1KB per impression event
- **Events per day**: 100M events × 1KB = 100GB/day
- **Retention**: 90 days = 9TB
- **With compression** (10:1): ~900GB
- **Aggregated data**: ~10% of raw data
- **Total estimated storage**: ~1TB for 100M events/day with 90-day retention

### 4.2 Compute Estimation
- **Query concurrency**: 10-100 concurrent dashboard queries
- **Query latency target**: < 1 second for dashboard queries
- **Ingestion throughput**: 100K events/second
- **Cluster sizing**: 3-12 ClickHouse nodes depending on query complexity

---

## 5. ETL vs ELT

### 5.1 ETL (Extract-Transform-Load)
- Data transformed before loading into warehouse
- Better for: Simple transformations, compliance requirements
- Drawback: Transformation bottleneck, limited flexibility

### 5.2 ELT (Extract-Load-Transform)
- Data loaded first, then transformed in warehouse
- Better for: Complex transformations, ad-hoc analysis
- Advantage: Raw data preserved, transformations are auditable
- **Recommended for recommendation analytics**: ELT pattern with ClickHouse

### 5.3 ELT Pipeline for Recommendations
1. **Extract**: Pull events from Kafka or data lake
2. **Load**: Load raw data into ClickHouse raw tables
3. **Transform**: Create materialized views and aggregate tables
4. **Consume**: Dashboards and analysts query transformed data
