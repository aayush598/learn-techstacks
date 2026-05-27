# Section 04: Topic-Based Sentiment Breakdown

## Overview

Topic-based sentiment breakdown analyzes customer sentiment within specific conversation topics, revealing which subjects drive positive or negative customer emotions. The system extracts topics from call transcriptions using NLP-based topic modeling and text classification, then computes sentiment scores for each topic. This provides actionable insights — for example, "customers discussing billing issues have an average sentiment of -0.4" suggesting the billing process needs improvement, while "customers discussing product features have an average sentiment of 0.6" indicating satisfaction.

Topic extraction supports both predefined topics (configurable by the tenant — e.g., "Billing," "Technical Support," "Account Management") and automatic topic discovery (using LDA or BERTopic for emergent themes). Each topic is associated with a sentiment score, call volume, trend over time, and representative phrases. The breakdown is visualized as a horizontal bar chart (sentiment per topic), a treemap (volume × sentiment), and a heatmap (topic × sentiment over time).

## Architecture

```
           Topic-Based Sentiment Pipeline

   Transcriptions → Topic Classifier (NLP)
                         |
   ┌────┴────────┐
   |             |
   Predefined    Auto-Discovery
   Topics        Topics (LDA/BERTopic)
   |             |
   Sentiment by Topic Calculator
         |
   ClickHouse (topic_sentiment_rollups)
         |
   Topic Sentiment API
         |
   Topic Bar Chart
   Treemap (volume × sentiment)
   Topic Trend Lines
```

## Design Decisions

- **Hybrid topic classification (predefined + auto-discovery) over pure unsupervised:** Predefined topics provide consistent, business-relevant categories that stakeholders understand. Auto-discovered topics capture emerging themes that the predefined list misses. The hybrid approach runs the predefined classifier first, then applies topic modeling to the "unclassified" residual for cluster discovery. Trade-off: managing two topic systems increases complexity; auto-discovered topics need human labeling to be useful in dashboards.

- **Aspect-based sentiment over document-level sentiment per topic:** A single call may discuss multiple topics with different sentiments (e.g., "The product is great, but your billing is confusing"). Aspect-based sentiment analysis identifies each topic mention within the call and assigns a sentiment to that specific mention, rather than assigning one sentiment per call per topic. This provides more accurate topic-sentiment associations. Trade-off: aspect-based models are more complex and slower than document-level models (2-3x inference time).

- **Topic hierarchy with drill-down over flat topic list:** Topics are organized in a hierarchy (e.g., "Billing → Invoice Questions → Missing Charges"), allowing users to drill from high-level trends to specific sub-topics. The system supports up to 3 levels of hierarchy. Flat lists become unwieldy with more than 15-20 topics. Trade-off: hierarchy requires more topic annotations per training example and may not capture all nuances of cross-cutting topics.

## Implementation Approach

```typescript
interface TopicDefinition {
  id: string;
  name: string;
  parentId?: string;
  keywords: string[];                    // for rule-based matching
  trainingPhrases?: string[];            // for ML classifier
  level: 1 | 2 | 3;
  order: number;
}

interface TopicSentimentResult {
  topicId: string;
  topicName: string;
  level: number;
  parentTopic?: string;
  mentions: number;
  callCount: number;
  averageSentiment: number;
  sentimentDistribution: { positive: number; neutral: number; negative: number };
  trend: 'improving' | 'declining' | 'stable';
  representativePhrases: string[];
  subTopics?: TopicSentimentResult[];   // for drill-down
}

interface TopicCallMatch {
  callSid: string;
  topicId: string;
  topicName: string;
  sentimentScore: number;
  mentionCount: number;
  representativeText: string;
}

class TopicSentimentService {
  private clickhouse: ClickHouseClient;
  private topicClassifier: TopicClassifier;
  private topics: Map<string, TopicDefinition> = new Map();

  async classifyCallTopics(transcription: string, callSid: string, tenantId: string): Promise<TopicCallMatch[]> {
    // Run predefined topic classifier
    const predefinedMatches = await this.topicClassifier.classifyPredefined(
      transcription,
      Array.from(this.topics.values())
    );

    // Run auto-discovery on unmatched segments
    const unmatchedSegments = this.getUnmatchedSegments(transcription, predefinedMatches);
    const autoTopics = unmatchedSegments.length > 100
      ? await this.topicClassifier.discoverTopics(unmatchedSegments)
      : [];

    const matches: TopicCallMatch[] = [];

    // Combine results
    for (const match of predefinedMatches) {
      matches.push({
        callSid,
        topicId: match.topicId,
        topicName: match.topicName,
        sentimentScore: match.sentiment,
        mentionCount: match.mentions,
        representativeText: match.representativeText,
      });
    }

    for (const topic of autoTopics) {
      matches.push({
        callSid,
        topicId: `auto_${topic.clusterId}`,
        topicName: topic.label ?? `Topic ${topic.clusterId}`,
        sentimentScore: topic.sentiment,
        mentionCount: topic.mentions,
        representativeText: topic.representativeText,
      });
    }

    return matches;
  }

  async getTopicSentiment(
    tenantId: string,
    start: number,
    end: number,
    parentTopicId?: string
  ): Promise<TopicSentimentResult[]> {
    const conditions = [
      `tenantId = '${tenantId}'`,
      `timestamp >= ${start}`,
      `timestamp <= ${end}`,
    ];

    let topicFilter = '';
    if (parentTopicId) {
      const children = Array.from(this.topics.values())
        .filter(t => t.parentId === parentTopicId)
        .map(t => `'${t.id}'`)
        .join(',');
      topicFilter = `AND topicId IN (${children})`;
    }

    const results = await this.clickhouse.query(`
      SELECT
        topicId,
        count() as mentions,
        count(DISTINCT callSid) as callCount,
        avg(sentimentScore) as avgSentiment,
        countIf(sentimentScore > 0.2) as positive,
        countIf(sentimentScore < -0.2) as negative,
        countIf(sentimentScore >= -0.2 AND sentimentScore <= 0.2) as neutral,
        groupArray(representativeText) as phrases
      FROM call_topic_sentiment
      WHERE ${conditions.join(' AND ')} ${topicFilter}
      GROUP BY topicId
      ORDER BY callCount DESC
    `);

    const topicResults: TopicSentimentResult[] = [];

    for (const row of results) {
      const definition = this.topics.get(row.topicId);
      const total = row.positive + row.neutral + row.negative;

      // Get sub-topics if this is a level 1 topic
      let subTopics: TopicSentimentResult[] | undefined;
      if (definition?.level === 1) {
        subTopics = await this.getTopicSentiment(tenantId, start, end, row.topicId);
        if (subTopics.length === 0) subTopics = undefined;
      }

      topicResults.push({
        topicId: row.topicId,
        topicName: definition?.name ?? row.topicId,
        level: definition?.level ?? 1,
        parentTopic: parentTopicId ? this.topics.get(parentTopicId)?.name : undefined,
        mentions: row.mentions,
        callCount: row.callCount,
        averageSentiment: row.avgSentiment,
        sentimentDistribution: {
          positive: total > 0 ? (row.positive / total) * 100 : 0,
          neutral: total > 0 ? (row.neutral / total) * 100 : 0,
          negative: total > 0 ? (row.negative / total) * 100 : 0,
        },
        trend: await this.computeTopicTrend(tenantId, row.topicId),
        representativePhrases: row.phrases.slice(0, 5),
        subTopics,
      });
    }

    return topicResults;
  }

  private async computeTopicTrend(
    tenantId: string,
    topicId: string
  ): Promise<'improving' | 'declining' | 'stable'> {
    const result = await this.clickhouse.query(`
      SELECT
        toStartOfWeek(timestamp) as week,
        avg(sentimentScore) as avgSentiment
      FROM call_topic_sentiment
      WHERE tenantId = '${tenantId}'
        AND topicId = '${topicId}'
        AND timestamp >= now() - INTERVAL 8 WEEK
      GROUP BY week
      ORDER BY week
    `);

    if (result.length < 2) return 'stable';
    const first = result[0].avgSentiment;
    const last = result[result.length - 1].avgSentiment;
    const diff = last - first;

    if (diff > 0.15) return 'improving';
    if (diff < -0.15) return 'declining';
    return 'stable';
  }

  private getUnmatchedSegments(transcription: string, matches: TopicCallMatch[]): string {
    // Simple approach: return segments that don't contain any matched topic keywords
    const matchedKeywords = new Set<string>();
    for (const match of matches) {
      const def = this.topics.get(match.topicId);
      def?.keywords.forEach(k => matchedKeywords.add(k));
    }

    const sentences = transcription.split(/[.!?]+/);
    return sentences
      .filter(s => !Array.from(matchedKeywords).some(k => s.toLowerCase().includes(k)))
      .join('. ');
  }
}

// Topic sentiment bar chart
const TopicSentimentChart: React.FC<{
  topics: TopicSentimentResult[];
  onDrillDown: (topicId: string) => void;
}> = ({ topics, onDrillDown }) => (
  <div className="topic-sentiment">
    <HorizontalBarChart
      data={topics.map(t => ({
        label: t.topicName,
        value: t.averageSentiment,
        volume: t.callCount,
        onClick: () => t.subTopics ? onDrillDown(t.topicId) : undefined,
      }))}
      xLabel="Average Sentiment"
      colorScale={['#E74C3C', '#F39C12', '#2ECC71']}
    />
    <Treemap
      data={topics.map(t => ({
        name: t.topicName,
        value: t.callCount,
        color: this.sentimentToColor(t.averageSentiment),
      }))}
    />
  </div>
);
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| BERTopic (MIT) | Server | Topic discovery model |
| spaCy (MIT) | Server | Text preprocessing |
| scikit-learn (BSD-3) | Server | LDA topic modeling |
| Apache ECharts (Apache 2.0) | Client | Treemap visualization |

## Production Considerations

**Scaling:** Topic classification runs as a batch post-call job, processing all calls completed in the last hour. For 10,000 calls/hour, each with 50-200 segments, the classifier processes 500K-2M segments/hour. Use a task queue (BullMQ or Celery) with 10-20 worker processes. Auto-discovery topic modeling (BERTopic) runs nightly and processes the last 7 days of unclassified segments. Results are cached in ClickHouse with partitioning by date.

**Security:** Topic definitions are tenant-scoped — each tenant can define their own topic hierarchy. Auto-discovered topics are scoped to the tenant and not shared. Topic analysis at the aggregate level (all calls) is accessible with `analytics:view` permission. Per-agent topic sentiment breakdown requires `agent-performance:view`.

**Monitoring:** Track topic classification coverage (percentage of calls with at least one topic identified), average topics per call, and auto-discovery topic novelty rate. Alert if classification coverage drops below 70% (indicates topic drift or new conversation patterns). Monitor the topic modeling pipeline for drift — if the distribution of topics shifts significantly week-over-week, the predefined topics may need updating.
