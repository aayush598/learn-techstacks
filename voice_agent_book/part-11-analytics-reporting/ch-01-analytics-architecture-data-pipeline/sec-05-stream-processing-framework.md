# Section 05: Stream Processing Framework

## Overview

The stream processing framework provides real-time computation on event streams as they flow through the analytics pipeline. It transforms raw events into meaningful analytics in near real-time (sub-5-second latency), computing metrics such as active call counts, average sentiment scores, agent performance indicators, and anomaly detection signals. The framework handles windowed aggregations, event time processing, late-arriving data, and stateful computations across distributed worker instances.

The framework operates on Kafka topics using a consumer group with configurable parallelism. Each worker instance processes one or more Kafka partitions, maintaining local state for windowed operations and emitting results to output topics and the analytics database. The framework supports multiple stream processing patterns: filter/transform, windowed aggregation, stream-stream join, stream-table join (enrichment), and pattern detection (e.g., "customer called 3 times in 5 minutes").

## Architecture

```
   Kafka Events → Stream Processor → Output Topics → Dashboards
                    |         |
                    v         v
               State Store  Side Outputs
               (RocksDB)    (Alerts)
```

## Design Decisions

- **Event time processing with watermark tracking over processing time:** The framework uses event timestamps (when the event occurred at the source) rather than processing timestamps (when the event was processed). Watermarks track the progress of event time and handle late-arriving data — events that arrive within a configurable lateness threshold (default 30 seconds) are included in the correct window; events beyond the threshold are sent to a late-event topic. Trade-off: event time processing requires watermark management and handles out-of-order events but provides correct temporal alignment regardless of processing delays.

- **RocksDB-backed state stores for windowed operations over in-memory state:** Windowed aggregations (count of calls in the last 5 minutes) maintain state that must survive process restarts. RocksDB provides disk-backed, embeddable key-value storage with in-memory caches for hot data. State is changelogged to a Kafka topic for fault tolerance — if a worker fails, the state is rebuilt from the changelog topic. Trade-off: RocksDB adds disk I/O and serialization overhead but provides fault-tolerant state management without external dependencies.

- **KSQL/flink SQL for standard aggregations, custom processors for complex logic:** The framework uses SQL-based stream processing (KSQL or Flink SQL) for common patterns: filtering, projection, windowed counts, averages, and simple joins. Custom processors (Kafka Streams DSL or Flink ProcessFunction) handle complex logic: sentiment trend detection (sudden drops), conversation flow analysis (call path sequences), and anomaly detection. Trade-off: SQL processing is easier to maintain but limited to operations expressible in SQL; custom processors are more flexible but require more development effort.

## Implementation Approach

```
// Kafka Streams topology builder
class StreamProcessorTopology {
  private builder: StreamsBuilder;

  constructor(private config: StreamProcessorConfig) {
    this.builder = new StreamsBuilder();
  }

  buildCallMetricsStream(): Topology {
    // Source: call.ended events
    const callEvents = this.builder.stream('events.call.ended', {
      consumedWith: Consumed.with(Serdes.String(), Serdes.JSON())
        .withTimestampExtractor(new EventTimeExtractor()),
    });

    // Windowed count of calls per tenant
    const callCounts = callEvents
      .groupBy((key, event) => event.tenantId, Grouped.with(Serdes.String(), Serdes.JSON()))
      .windowedBy(TimeWindows.of(Duration.ofMinutes(1)).grace(Duration.ofSeconds(30)))
      .count()
      .toStream();

    callCounts.to('analytics.call_counts_minute', Produced.with(
      WindowedSerdes.timeWindowedSerdesFrom(String),
      Serdes.Long()
    ));

    // Average call duration per campaign (tumbling window, 5 minutes)
    const campaignDurations = callEvents
      .filter((key, event) => event.campaignId !== null)
      .groupBy((key, event) => `${event.tenantId}:${event.campaignId}`)
      .windowedBy(TimeWindows.of(Duration.ofMinutes(5)).grace(Duration.ofSeconds(30)))
      .aggregate(
        () => ({ totalDuration: 0, count: 0 }),
        (key, event, aggregate) => ({
          totalDuration: aggregate.totalDuration + event.duration,
          count: aggregate.count + 1,
        }),
        Materialized.with(Serdes.String(), Serdes.serdesFrom(AggregateSerde))
      )
      .toStream()
      .mapValues(agg => ({
        avgDuration: agg.count > 0 ? agg.totalDuration / agg.count : 0,
        callCount: agg.count,
      }));

    campaignDurations.to('analytics.campaign_metrics_5min');

    return this.builder.build();
  }

  buildSentimentTrendStream(): Topology {
    const sentimentEvents = this.builder.stream('events.call.sentiment');

    // Detect negative sentiment trends: 3 consecutive negative scores in 2 minutes
    sentimentEvents
      .groupBy((key, event) => event.agentId, Grouped.with(Serdes.String(), Serdes.JSON()))
      .windowedBy(SessionWindows.with(Duration.ofMinutes(2)))
      .aggregate(
        () => ({ consecutiveNegatives: 0, alerted: false }),
        (key, event, aggregate) => {
          if (event.sentiment.label === 'negative') {
            aggregate.consecutiveNegatives++;
            if (aggregate.consecutiveNegatives >= 3 && !aggregate.alerted) {
              aggregate.alerted = true;
              this.alertService.sendAlert({
                type: 'negative_sentiment_trend',
                agentId: event.agentId,
                callSid: event.callSid,
                timestamp: event.timestamp,
              });
            }
          } else {
            aggregate.consecutiveNegatives = 0;
          }
          return aggregate;
        },
        Materialized.with(Serdes.String(), Serdes.serdesFrom(SentimentAggregateSerde))
      );
  }
}

// Custom processor for transcription analysis
class TranscriptionAnalysisProcessor implements StreamProcessor {
  async process(event: TranscriptionEvent): Promise<void> {
    // Check for keywords, compliance phrases, objection handling
    const analysis = {
      hasGreeting: this.containsAny(event.text, GREETING_PHRASES),
      hasClosing: this.containsAny(event.text, CLOSING_PHRASES),
      hasObjection: this.containsAny(event.text, OBJECTION_PHRASES),
      hasProfanity: this.containsAny(event.text, PROFANITY_LIST),
      talkRatio: event.agentTalkTime / event.customerTalkTime,
    };

    await this.produceToTopic('analytics.transcription_analysis', {
      callSid: event.callSid,
      timestamp: event.timestamp,
      analysis,
    });

    // Real-time compliance alert
    if (analysis.hasProfanity) {
      await this.produceToTopic('alerts.compliance', {
        type: 'profanity_detected',
        severity: 'high',
        callSid: event.callSid,
      });
    }
  }

  private containsAny(text: string, phrases: string[]): boolean {
    const lower = text.toLowerCase();
    return phrases.some(phrase => lower.includes(phrase));
  }
}

// Flink SQL alternative (for reference)
/*
CREATE TABLE call_events (
  callSid STRING,
  tenantId STRING,
  duration INT,
  status STRING,
  campaignId STRING,
  eventTime TIMESTAMP(3) METADATA FROM 'timestamp',
  WATERMARK FOR eventTime AS eventTime - INTERVAL '30' SECOND
) WITH (
  'connector' = 'kafka',
  'topic' = 'events.call.ended',
  'properties.bootstrap.servers' = '...',
  'format' = 'json'
);

CREATE TABLE minute_metrics AS
SELECT
  tenantId,
  TUMBLE_START(eventTime, INTERVAL '1' MINUTE) AS windowStart,
  COUNT(*) AS totalCalls,
  AVG(duration) AS avgDuration
FROM call_events
GROUP BY tenantId, TUMBLE(eventTime, INTERVAL '1' MINUTE);
*/
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Kafka Streams (Apache 2.0) | Library | Stream processing library |
| Apache Flink (Apache 2.0) | Server | Distributed stream processor |
| RocksDB (Apache 2.0) | Library | Embedded state store |
| KSQLDB (Confluent) | Server | SQL stream processing |

## Production Considerations

**Scaling:** Stream processor parallelism equals the number of input topic partitions. Add partitions to increase throughput (each partition can process ~10MB/s). State store size grows with window duration and data volume — monitor RocksDB disk usage. For 1-minute windows with 10,000 calls/minute, state store needs ~100MB per worker. Use standby replicas (Kafka Streams) for faster recovery from worker failure.

**Security:** Stream processors have access to all event data — ensure they run in a trusted security context. Use Kafka ACLs to restrict which consumers can read specific topics. Never output raw PII data from stream processors to output topics. Sanitize transcription data before publishing to analytics topics.

**Monitoring:** Track stream processor lag (event time vs. processing time), watermark progression, state store size and disk usage, RocksDB compaction status, and processing rate (events/second per partition). Alert on processing lag exceeding 30 seconds (indicates under-provisioned workers), watermark stall (no events arriving — potential upstream issue), and state store growing beyond configured limits.
