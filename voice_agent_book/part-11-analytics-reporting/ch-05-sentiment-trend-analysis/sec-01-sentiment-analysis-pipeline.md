# Section 01: Sentiment Analysis Pipeline

## Overview

The sentiment analysis pipeline processes call transcriptions in real-time and batch to extract emotional tone and sentiment scores. It ingests transcription segments from the voice platform's speech-to-text engine, applies natural language processing models to classify sentiment (positive, neutral, negative) and compute a numerical sentiment score (-1.0 to 1.0), and makes the results available for dashboarding, alerting, and historical analysis.

The pipeline operates at two speeds: real-time sentiment for live dashboard updates (per-segment sentiment as the call progresses, updated every 2-5 seconds) and post-call full analysis (complete transcription sentiment with sentence-level breakdown, emotion detection, and key phrase extraction). The real-time path uses a lightweight, fast model (e.g., DistilBERT or a logistic regression classifier), while the post-call path uses a more accurate but slower model (e.g., fine-tuned RoBERTa or GPT-based analysis). Both paths write results to ClickHouse for trend analysis.

## Architecture

```
            Sentiment Analysis Pipeline

   STT Engine → Transcription Segments (Kafka)
                     |
          ┌──────────┴──────────┐
          |                     |
    Real-time Path         Batch Path
    (per-segment,          (post-call,
     lightweight model)     full model)
          |                     |
    Redis (current       ClickHouse
    call sentiment)      (per-call analysis)
          |                     |
    WebSocket            Sentiment Dashboard
    (live updates)       (trends, per-agent)
```

## Design Decisions

- **Two-tier sentiment analysis (real-time lightweight + batch accurate) over single model:** Real-time sentiment must complete in under 200 ms per segment to keep the live dashboard responsive. A lightweight DistilBERT model (66M parameters, ~50 ms inference on GPU) suffices for directional sentiment. Post-call analysis uses a larger model (RoBERTa-large, 355M parameters, ~500 ms per call) that provides sentence-level sentiment, emotion detection (anger, sadness, joy, surprise, fear), and aspect-based sentiment. Trade-off: maintaining two models doubles the MLOps overhead (deployment, monitoring, retraining) but provides the best of both speed and accuracy.

- **Per-segment sentiment with aggregation over whole-transcription sentiment:** Sentiment fluctuates during a call — a customer may start frustrated and end satisfied. Computing a single sentiment score for the entire call masks these dynamics. The pipeline processes each transcription segment independently and provides real-time per-segment scores, with the option to aggregate into call-level statistics (min, max, final, trend). The dashboard shows a sentiment timeline graph for each call. Trade-off: per-segment processing increases the number of inference calls by ~50x (each call has 50-200 segments vs 1 full transcription).

- **Cloud GPU inference via managed service over self-hosted GPU servers:** Running NLP models on GPU instances requires specialized infrastructure management (GPU drivers, model versioning, auto-scaling). Using a managed inference service (AWS SageMaker, GCP Vertex AI, or a serverless GPU platform like Banan or Replicate) reduces operational burden. The sentiment pipeline sends inference requests to the managed service and caches results for identical segments (deduplication). Trade-off: managed services cost 2-3x more per inference than self-hosted at scale (>100K calls/day), but eliminate GPU management overhead.

## Implementation Approach

```typescript
interface TranscriptionSegment {
  callSid: string;
  tenantId: string;
  segmentIndex: number;
  text: string;
  speaker: 'agent' | 'customer';
  startTime: number;      // offset from call start in ms
  endTime: number;
  confidence: number;     // STT confidence 0-1
  timestamp: number;      // event timestamp
}

interface SentimentResult {
  callSid: string;
  segmentIndex: number;
  score: number;           // -1.0 to 1.0
  label: 'positive' | 'neutral' | 'negative';
  confidence: number;      // model confidence
  emotions?: {
    anger: number;
    sadness: number;
    joy: number;
    surprise: number;
    fear: number;
  };
  language: string;
  processingTimeMs: number;
}

interface CallSentimentSummary {
  callSid: string;
  tenantId: string;
  overallScore: number;
  overallLabel: string;
  sentimentTimeline: Array<{ timeOffset: number; score: number; speaker: string }>;
  agentSentiment: number;
  customerSentiment: number;
  sentimentTrend: 'improving' | 'declining' | 'stable' | 'volatile';
  keyPhrases: string[];
  emotionSummary: Record<string, number>;
  processingModel: string;
}

class SentimentPipeline {
  private kafka: KafkaProducer;
  private redis: Redis;
  private clickhouse: ClickHouseClient;
  private inferenceClient: InferenceServiceClient;

  // Real-time segment processing
  async processSegment(segment: TranscriptionSegment): Promise<void> {
    // Quick check: skip empty or too-short segments
    if (segment.text.length < 3) return;

    const startTime = Date.now();

    // Call real-time sentiment model
    const sentiment = await this.inferenceClient.analyzeSentiment({
      text: segment.text,
      model: 'distilbert-sentiment',
      fast: true,
    });

    const result: SentimentResult = {
      callSid: segment.callSid,
      segmentIndex: segment.segmentIndex,
      score: sentiment.score,
      label: sentiment.label,
      confidence: sentiment.confidence,
      processingTimeMs: Date.now() - startTime,
    };

    // Update Redis for current call sentiment
    await this.redis.hset(
      `call:sentiment:${segment.callSid}`,
      'latestScore', result.score.toString(),
      'latestLabel', result.label,
      'latestSegment', segment.segmentIndex.toString(),
      'lastUpdated', Date.now().toString(),
    );
    await this.redis.expire(`call:sentiment:${segment.callSid}`, 7200); // 2 hours

    // Publish to WebSocket stream
    await this.kafka.send({
      topic: 'sentiment.realtime',
      key: segment.callSid,
      value: JSON.stringify({
        callSid: segment.callSid,
        tenantId: segment.tenantId,
        segmentIndex: segment.segmentIndex,
        score: sentiment.score,
        label: sentiment.label,
        speaker: segment.speaker,
        timeOffset: segment.startTime,
        timestamp: Date.now(),
      }),
    });
  }

  // Post-call full analysis
  async analyzeFullCall(callSid: string, segments: TranscriptionSegment[]): Promise<CallSentimentSummary> {
    const fullTranscription = segments
      .map(s => `[${s.speaker}] ${s.text}`)
      .join('\n');

    const startTime = Date.now();

    // Call full sentiment model
    const analysis = await this.inferenceClient.analyzeSentiment({
      text: fullTranscription,
      model: 'roberta-sentiment-advanced',
      includeEmotions: true,
      includeKeyPhrases: true,
      includeTimeline: true,
      segments: segments.map(s => ({ text: s.text, offset: s.startTime, speaker: s.speaker })),
    });

    const summary: CallSentimentSummary = {
      callSid,
      tenantId: segments[0]?.tenantId ?? '',
      overallScore: analysis.overallScore,
      overallLabel: this.scoreToLabel(analysis.overallScore),
      sentimentTimeline: analysis.timeline,
      agentSentiment: this.computeSpeakerAvg(analysis.timeline, 'agent'),
      customerSentiment: this.computeSpeakerAvg(analysis.timeline, 'customer'),
      sentimentTrend: this.determineTrend(analysis.timeline),
      keyPhrases: analysis.keyPhrases ?? [],
      emotionSummary: analysis.emotions ?? {},
      processingModel: 'roberta-sentiment-advanced',
    };

    // Store in ClickHouse
    await this.clickhouse.insert('call_sentiment_analysis', {
      callSid: summary.callSid,
      tenantId: summary.tenantId,
      overallScore: summary.overallScore,
      overallLabel: summary.overallLabel,
      agentSentiment: summary.agentSentiment,
      customerSentiment: summary.customerSentiment,
      sentimentTrend: summary.sentimentTrend,
      keyPhrases: summary.keyPhrases,
      emotionSummary: JSON.stringify(summary.emotionSummary),
      processingTimeMs: Date.now() - startTime,
      timestamp: Date.now(),
    });

    return summary;
  }

  async getRealtimeSentiment(callSid: string): Promise<{ score: number; label: string; lastUpdated: number } | null> {
    const data = await this.redis.hgetall(`call:sentiment:${callSid}`);
    if (!data || Object.keys(data).length === 0) return null;

    return {
      score: parseFloat(data.latestScore),
      label: data.latestLabel,
      lastUpdated: parseInt(data.lastUpdated),
    };
  }

  async getCallSentimentSummary(
    callSid: string,
    tenantId: string
  ): Promise<CallSentimentSummary | null> {
    // Check ClickHouse for full analysis
    const result = await this.clickhouse.query(`
      SELECT * FROM call_sentiment_analysis
      WHERE callSid = '${callSid}' AND tenantId = '${tenantId}'
    `);
    if (result.length > 0) return result[0];

    // Fall back to real-time data from segments
    const realtime = await this.getRealtimeSentiment(callSid);
    if (!realtime) return null;

    return {
      callSid,
      tenantId,
      overallScore: realtime.score,
      overallLabel: realtime.label,
      sentimentTimeline: [],
      agentSentiment: 0,
      customerSentiment: realtime.score,
      sentimentTrend: 'stable',
      keyPhrases: [],
      emotionSummary: {},
      processingModel: 'realtime',
    };
  }

  private scoreToLabel(score: number): 'positive' | 'neutral' | 'negative' {
    if (score > 0.2) return 'positive';
    if (score < -0.2) return 'negative';
    return 'neutral';
  }

  private computeSpeakerAvg(timeline: Array<{ score: number; speaker: string }>, speaker: string): number {
    const filtered = timeline.filter(t => t.speaker === speaker);
    if (filtered.length === 0) return 0;
    return filtered.reduce((s, t) => s + t.score, 0) / filtered.length;
  }

  private determineTrend(timeline: Array<{ timeOffset: number; score: number }>): string {
    if (timeline.length < 3) return 'stable';
    const firstHalf = timeline.slice(0, Math.floor(timeline.length / 2));
    const secondHalf = timeline.slice(Math.floor(timeline.length / 2));
    const firstAvg = firstHalf.reduce((s, t) => s + t.score, 0) / firstHalf.length;
    const secondAvg = secondHalf.reduce((s, t) => s + t.score, 0) / secondHalf.length;
    const diff = secondAvg - firstAvg;

    if (diff > 0.2) return 'improving';
    if (diff < -0.2) return 'declining';
    if (Math.abs(diff) < 0.05) return 'stable';
    return 'volatile';
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Hugging Face Transformers (Apache 2.0) | Server | Sentiment models |
| spaCy (MIT) | Server | Text preprocessing |
| Redis (RSAL) | Server | Real-time sentiment cache |
| ClickHouse (Apache 2.0) | Server | Sentiment analysis storage |

## Production Considerations

**Scaling:** The real-time sentiment path processes segments as they arrive. For 100 concurrent calls, each generating a segment every 2 seconds, throughput is 50 segments/second. The lightweight DistilBERT model on a single GPU handles ~100 segments/second. For higher volume, scale inference endpoints horizontally behind a load balancer. The post-call analysis is queued (in Kafka) and processed asynchronously — analysis latency is acceptable up to 30 seconds after call end.

**Security:** Sentiment results include the call SID and tenant ID. Transcription text is PII — ensure the inference service is in the same VPC and data does not leave the trusted network. The Redis sentiment cache is per-call and auto-expires. ClickHouse tables are tenant-partitioned. Sentiment results aggregated over agents (per-agent average sentiment) require the `agent-performance:view` permission.

**Monitoring:** Track inference latency (p50 < 200 ms real-time, p95 < 1 sec batch), inference throughput, model confidence distribution, and sentiment label distribution per tenant. Alert if real-time inference latency exceeds 500 ms (switch to fallback rule-based classifier). Alert if model confidence drops below 0.6 for more than 10% of inferences (potential model drift).
