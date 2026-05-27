# Section 06: Batch Processing and ETL

## Overview

The batch processing and ETL layer handles periodic, comprehensive data processing that the real-time stream layer cannot efficiently perform. Batch jobs run on a scheduled basis (hourly, daily, weekly) to compute precise aggregations, handle late-arriving data corrections, build derived datasets, and maintain the data warehouse. The batch layer complements the stream layer by providing accurate, reprocessed results that correct any approximations from real-time processing.

Batch processing covers: hourly aggregation of call metrics (correcting stream approximations with exact counts), daily rollups for long-term trends, data quality validation and gap-filling, schema migration and backfilling, machine learning feature engineering, and data archiving/compaction. The batch framework is built on Apache Spark or the ClickHouse materialized view system, with DAG-based workflow orchestration for managing job dependencies.

## Architecture

```
   Data Lake (Parquet) → Spark/ETL → Data Warehouse (ClickHouse)
        |                      |              |
        v                      v              v
   Raw Events              Derived Tables   Aggregations
        |                      |
        v                      v
   Event Archive           Reports/ML
```

## Design Decisions

- **Hourly run cadence with incremental processing over full refresh:** Batch jobs process data incrementally — they pick up where the previous run left off using a checkpoint (last processed Kafka offset or data lake partition). Incremental processing limits each run to 1-2 hours of data, keeping job duration manageable. A full refresh job runs weekly for data reconciliation and schema migration. Trade-off: incremental processing requires checkpoint management and can produce data gaps if a job fails mid-run but keeps batch processing windows short.

- **Spark for complex ETL, ClickHouse for simple aggregations over unified platform:** Apache Spark handles complex ETL: joining multiple event streams, ML feature engineering, schema transformations, and large-scale data quality checks. ClickHouse's built-in materialized views handle simple aggregations (sum, count, avg, quantile) that do not require joins across disparate event types. Spark jobs write results back to ClickHouse or to Parquet in the data lake. Trade-off: dual platform adds infrastructure complexity but uses each tool for its strengths.

- **Data quality checks as gate before loading over trust-but-verify:** Before batch results are loaded into the serving layer, the ETL pipeline runs data quality checks: row count validation (within 10% of expected), null rate thresholds, distribution shape comparison to prior runs, and referential integrity checks. If checks fail, the batch job alerts and does not load the data (preventing dashboards from showing incorrect data). A manual override allows operators to force-load with a reason. Trade-off: data quality gates can delay data availability during transient issues but prevent bad data from reaching users.

## Implementation Approach

```
class BatchETLJob {
  private spark: SparkSession;
  private scheduler: JobScheduler;

  constructor() {
    this.spark = SparkSession.builder()
      .appName('VoiceAgentBatchETL')
      .config('spark.sql.parquet.enableVectorizedReader', 'true')
      .getOrCreate();
    this.scheduler = new JobScheduler();
  }

  async registerJobs(): Promise<void> {
    this.scheduler.register('hourly-call-metrics', {
      cron: '5 * * * *',     // Every hour at :05
      timeout: 1800000,       // 30 min timeout
      handler: () => this.computeHourlyCallMetrics(),
      dependsOn: ['data-quality-check'],
    });

    this.scheduler.register('daily-rollup', {
      cron: '0 3 * * *',     // At 3 AM daily
      timeout: 7200000,       // 2 hour timeout
      handler: () => this.computeDailyRollup(),
      dependsOn: ['hourly-call-metrics'],
    });

    this.scheduler.register('full-reconciliation', {
      cron: '0 5 * * 0',     // Weekly on Sunday at 5 AM
      timeout: 14400000,      // 4 hour timeout
      handler: () => this.fullReconciliation(),
      dependsOn: [],
    });
  }

  async computeHourlyCallMetrics(): Promise<JobResult> {
    const lastRun = await this.getLastRunTimestamp('hourly-call-metrics');
    const startDate = lastRun || new Date(Date.now() - 3600000);

    // Read from data lake (incremental)
    const df = this.spark.read
      .format('parquet')
      .load(`s3a://voiceagent-datalake/events/event_type=call.ended/`)
      .filter($"timestamp" >= startDate)
      .filter($"timestamp" <= new Date());

    // Compute hourly aggregations
    const hourlyMetrics = df.groupBy(
      $"tenantId",
      window($"timestamp", "1 hour"),
      $"campaignId"
    ).agg(
      count($"*").as("totalCalls"),
      count(when($"status" === "completed", 1)).as("answeredCalls"),
      avg($"duration").as("avgDuration"),
      approx_count_distinct($"customerPhone").as("uniqueCallers"),
      expr("percentile_approx(duration, 0.95)").as("p95Duration")
    );

    // Data quality check
    const rowCount = hourlyMetrics.count();
    const expectedCount = await this.estimateExpectedCount(startDate);
    if (rowCount < expectedCount * 0.9 || rowCount > expectedCount * 1.1) {
      throw new Error(`Data quality check failed: row count ${rowCount} outside expected range ${expectedCount}`);
    }

    // Write to ClickHouse
    hourlyMetrics.write
      .format("jdbc")
      .option("url", "jdbc:clickhouse://localhost:8123/analytics")
      .option("dbtable", "call_metrics_hourly")
      .mode("append")
      .save();

    // Update checkpoint
    await this.updateLastRunTimestamp('hourly-call-metrics', new Date());

    return { status: 'success', rowsProcessed: rowCount };
  }

  async computeDailyRollup(): Promise<JobResult> {
    const yesterday = new Date(Date.now() - 86400000);

    // Read hourly aggregates
    const df = this.spark.read
      .format("jdbc")
      .option("url", "jdbc:clickhouse://localhost:8123/analytics")
      .option("dbtable", "call_metrics_hourly")
      .load()
      .filter($"hour" >= yesterday)
      .filter($"hour" < new Date());

    // Daily aggregation with corrections for late data
    const correctedDaily = df.groupBy("tenantId", "campaignId")
      .agg(
        sum("totalCalls").as("totalCalls"),
        sum("answeredCalls").as("answeredCalls"),
        avg("avgDuration").as("avgDuration"),
        max("p95Duration").as("p95Duration"),
        sum("uniqueCallers").as("uniqueCallers")
      );

    // Correct stream approximations with exact batch computation
    const exactCounts = this.spark.read
      .format("parquet")
      .load(`s3a://voiceagent-datalake/events/event_type=call.ended/dt=${toDateString(yesterday)}`)
      .groupBy("tenantId", "campaignId")
      .agg(countDistinct("customerPhone").as("exactUniqueCallers"));

    // Merge and correct
    const merged = correctedDaily
      .join(exactCounts, Seq("tenantId", "campaignId"), "left")
      .withColumn("uniqueCallers",
        when($"exactUniqueCallers".isNotNull, $"exactUniqueCallers").otherwise($"uniqueCallers")
      );

    // Write daily rollup
    merged.write
      .mode("overwrite")
      .option("partitionBy", "tenantId")
      .format("parquet")
      .save("s3a://voiceagent-datalake/aggregates/daily/");

    return { status: 'success', rowsProcessed: merged.count() };
  }

  async fullReconciliation(): Promise<JobResult> {
    // Full reprocess from data lake
    const df = this.spark.read
      .format("parquet")
      .load("s3a://voiceagent-datalake/events/call.ended/*");

    const hourlyMetrics = df.groupBy("tenantId", window($"timestamp", "1 hour"), "campaignId")
      .agg(count("*"), avg("duration"), expr("percentile_approx(duration, 0.95)"));

    // Replace hourly metrics table
    hourlyMetrics.write
      .mode("overwrite")
      .format("jdbc")
      .option("url", "jdbc:clickhouse://localhost:8123/analytics")
      .option("dbtable", "call_metrics_hourly")
      .save();

    return { status: 'success', rowsProcessed: hourlyMetrics.count() };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Apache Spark (Apache 2.0) | Server | Distributed data processing |
| Airflow (Apache 2.0) | Server | DAG-based job orchestration |
| Prefect (Apache 2.0) | Server | Workflow orchestration |

## Production Considerations

**Scaling:** Spark jobs should be auto-scaled based on data volume — small tenants get fewer executors, large tenants get more. Shuffle operations (groupBy, join) are the bottleneck — configure spark.sql.shuffle.partitions (default 200, increase to min(200, data_size_in_mb / 100)). Airflow workers should be autoscaled based on queue depth. Batch jobs compete with stream processing for ClickHouse resources — schedule batch writes during low-query periods.

**Security:** Spark jobs access data lake files with PII — ensure IAM roles for Spark have the minimum required permissions. Never pass credentials through Spark job parameters — use secrets manager integration. Airflow connections to databases should be encrypted. Log Spark job parameters exclusions: skip logging PII-containing filter values.

**Monitoring:** Track batch job execution duration, data volume processed per job, row count deviation from expected, checkpoint position (offset/partition), and re-run frequency. Alert on job failures (with retry), data quality check failures, job duration exceeding the schedule interval (cascading delays), and full reconciliation completing successfully (weekly check).
