# Section 03: Topic Clustering Algorithms

## Overview

Topic clustering algorithms automatically discover themes and conversation patterns from call transcriptions without requiring predefined labels. These algorithms group similar calls or transcription segments into clusters, each representing a distinct topic or theme. Topic clustering serves two purposes: discovering new intents that the predefined taxonomy doesn't cover, and providing an alternative view of call content that doesn't depend on manual taxonomy maintenance.

The system supports multiple clustering approaches: BERTopic (transformer-based, state-of-the-art), LDA (Latent Dirichlet Allocation, classic topic modeling), and TF-IDF + K-means (lightweight baseline). Each approach has different trade-offs in accuracy, interpretability, and computational cost. The system runs clustering nightly on the previous day's calls (or the last 7 days for smaller tenants) and stores the results in ClickHouse alongside the predefined intent classifications.

## Architecture

```
           Topic Clustering Pipeline

   Transcriptions (last N days)
        |
   Preprocessing
   (cleaning, stop word removal,
    lemmatization, sentence splitting)
        |
   ┌────┴────────────┐
   |                 |
   BERTopic          LDA / K-means
   (GPU,             (CPU,
    accurate)         fast, interpretable)
   |                 |
   Cluster Assignments
        |
   Topic Labeling (auto + manual)
        |
   ClickHouse (topic_clusters table)
        |
   Cluster Dashboard
   (topic cards, representative calls,
    trend over time)
```

## Design Decisions

- **Multiple algorithm support with automatic selection over a single algorithm:** Different data volumes and quality levels suit different algorithms. For tenants with >10,000 calls/month, BERTopic provides the best topic quality. For smaller tenants or faster turnaround, LDA or TF-IDF+K-means suffices. The system automatically selects the algorithm based on data volume and available compute resources, with manual override. Trade-off: maintaining multiple algorithms increases code complexity (3 implementations instead of 1) but ensures optimal results across diverse tenant profiles.

- **Hierarchical topic reduction over flat topic assignment:** BERTopic naturally produces a topic hierarchy (broad topics at the top, specific sub-topics below). The system maintains this hierarchy and allows users to drill from broad topics ("Billing") to specific sub-topics ("Disputing a late fee"). Topics with fewer than 10 calls are merged into the parent topic. Trade-off: hierarchical topics require more complex visualization (zoomable circle packing, sunburst) and may confuse users accustomed to flat topic lists.

- **Human-in-the-loop topic labeling over fully automatic labeling:** Auto-generated topic labels (from BERTopic's c-TF-IDF or LDA's top words) are often unintelligible (e.g., "token_1, token_2, token_3"). The system generates suggested labels but requires a human to review and approve or rename them. Unlabeled topics are displayed with the top 5 representative words until labeled. Trade-off: human labeling requires ongoing effort (a few minutes per week for most tenants) but dramatically improves topic interpretability.

## Implementation Approach

```typescript
interface TopicCluster {
  topicId: string;
  tenantId: string;
  level: number;
  parentTopicId?: string;
  label?: string;              // human-assigned label
  autoLabel: string;           // auto-generated label
  topWords: string[];
  callCount: number;
  representativeCalls: string[];  // call SIDs most representative of this topic
  averageSentiment: number;
  coherenceScore: number;      // topic cohesion metric
  createdAt: number;
  updatedAt: number;
  children?: TopicCluster[];
}

interface TopicClusteringConfig {
  tenantId: string;
  algorithm: 'bertopic' | 'lda' | 'tfidf_kmeans';
  numTopics?: number;          // approximate number of topics
  minTopicSize: number;        // minimum calls per topic (default 10)
  ngramRange: [number, number]; // 1-3 for unigrams+bigrams+trigrams
  language: string;
}

class TopicClusteringEngine {
  private clickhouse: ClickHouseClient;
  private bertopicWorker: Worker;
  private ldaModel: LdaModel;
  private kmeansModel: KMeansModel;

  async runClustering(config: TopicClusteringConfig): Promise<TopicCluster[]> {
    // Get transcriptions
    const transcriptions = await this.getTranscriptions(config.tenantId);
    if (transcriptions.length < config.minTopicSize) {
      return [];
    }

    let clusters: TopicCluster[];

    switch (config.algorithm) {
      case 'bertopic':
        clusters = await this.runBertopic(transcriptions, config);
        break;
      case 'lda':
        clusters = await this.runLda(transcriptions, config);
        break;
      case 'tfidf_kmeans':
        clusters = await this.runTfidfKmeans(transcriptions, config);
        break;
      default:
        // Auto-select based on call volume
        clusters = transcriptions.length > 10000
          ? await this.runBertopic(transcriptions, config)
          : await this.runLda(transcriptions, config);
    }

    // Store in ClickHouse
    await this.storeClusters(clusters, config.tenantId);

    return clusters;
  }

  private async runBertopic(
    transcriptions: Array<{ callSid: string; text: string }>,
    config: TopicClusteringConfig
  ): Promise<TopicCluster[]> {
    // Send to BERTopic worker (GPU process)
    const result = await this.bertopicWorker.send({
      texts: transcriptions.map(t => t.text),
      callSids: transcriptions.map(t => t.callSid),
      minTopicSize: config.minTopicSize,
      ngramRange: config.ngramRange,
    });

    // BERTopic returns hierarchical topics
    return this.buildHierarchy(result, config.tenantId);
  }

  private async runLda(
    transcriptions: Array<{ callSid: string; text: string }>,
    config: TopicClusteringConfig
  ): Promise<TopicCluster[]> {
    // Preprocess texts
    const processed = transcriptions.map(t => this.preprocess(t.text));

    // Train LDA model
    const numTopics = config.numTopics ?? Math.min(20, Math.floor(transcriptions.length / 50));
    const ldaResult = this.ldaModel.fitTransform(processed, numTopics);

    // Build flat topic list
    const clusters: TopicCluster[] = [];
    for (let i = 0; i < ldaResult.topics.length; i++) {
      const topic = ldaResult.topics[i];
      const assignedCalls = ldaResult.assignments
        .map((assignment: number, idx: number) => ({ idx, assignment }))
        .filter(a => a.assignment === i)
        .map(a => transcriptions[a.idx].callSid);

      if (assignedCalls.length < config.minTopicSize) continue;

      clusters.push({
        topicId: `lda_${i}_${Date.now()}`,
        tenantId: config.tenantId,
        level: 1,
        label: undefined,
        autoLabel: topic.topWords.slice(0, 5).join(', '),
        topWords: topic.topWords.slice(0, 10),
        callCount: assignedCalls.length,
        representativeCalls: assignedCalls.slice(0, 3),
        averageSentiment: 0, // Compute separately
        coherenceScore: topic.coherence,
        createdAt: Date.now(),
        updatedAt: Date.now(),
      });
    }

    return clusters;
  }

  private async runTfidfKmeans(
    transcriptions: Array<{ callSid: string; text: string }>,
    config: TopicClusteringConfig
  ): Promise<TopicCluster[]> {
    // TF-IDF vectorization
    const processed = transcriptions.map(t => this.preprocess(t.text));
    const numTopics = config.numTopics ?? Math.min(15, Math.floor(transcriptions.length / 100));

    const result = this.kmeansModel.fitTransform(processed, numTopics);

    const clusters: TopicCluster[] = [];
    for (let i = 0; i < numTopics; i++) {
      const assignedIndices = result.labels
        .map((label: number, idx: number) => ({ idx, label }))
        .filter(l => l.label === i)
        .map(l => l.idx);

      if (assignedIndices.length < config.minTopicSize) continue;

      // Get top words from centroid
      const centroid = result.centroids[i];
      const topWordIndices = centroid
        .map((val: number, idx: number) => ({ val, idx }))
        .sort((a: any, b: any) => b.val - a.val)
        .slice(0, 10)
        .map((w: any) => w.idx);

      clusters.push({
        topicId: `kmeans_${i}_${Date.now()}`,
        tenantId: config.tenantId,
        level: 1,
        label: undefined,
        autoLabel: topWordIndices.join(', '),
        topWords: topWordIndices.map((idx: number) => this.vocabulary[idx]),
        callCount: assignedIndices.length,
        representativeCalls: assignedIndices.slice(0, 3).map(i => transcriptions[i].callSid),
        averageSentiment: 0,
        coherenceScore: this.calculateCoherence(assignedIndices, transcriptions),
        createdAt: Date.now(),
        updatedAt: Date.now(),
      });
    }

    return clusters;
  }

  private buildHierarchy(bertopicResult: any, tenantId: string): TopicCluster[] {
    // BERTopic returns a hierarchical structure
    // Recursively build TopicCluster objects
    const buildNode = (node: any, level: number): TopicCluster => ({
      topicId: node.topicId ?? `bertopic_${level}_${Date.now()}`,
      tenantId,
      level,
      label: undefined,
      autoLabel: node.representation ?? node.topWords?.join(', ') ?? '',
      topWords: node.topWords ?? [],
      callCount: node.calls?.length ?? 0,
      representativeCalls: node.representativeDocs?.slice(0, 3) ?? [],
      averageSentiment: 0,
      coherenceScore: node.coherence ?? 0,
      createdAt: Date.now(),
      updatedAt: Date.now(),
      children: node.children?.map((c: any) => buildNode(c, level + 1)),
    });

    return [buildNode(bertopicResult.tree, 1)];
  }

  private preprocess(text: string): string {
    return text
      .toLowerCase()
      .replace(/[^\w\s]/g, '')
      .replace(/\d+/g, '')
      .split(/\s+/)
      .filter(w => w.length > 2)
      .join(' ');
  }

  private calculateCoherence(indices: number[], transcriptions: any[]): number {
    // Simplified coherence score based on word co-occurrence
    return 0.7; // Placeholder
  }

  private async storeClusters(clusters: TopicCluster[], tenantId: string): Promise<void> {
    // Flatten hierarchy for storage
    const flatten = (clusters: TopicCluster[]): any[] => {
      const rows: any[] = [];
      for (const c of clusters) {
        rows.push(c);
        if (c.children) rows.push(...flatten(c.children));
      }
      return rows;
    };

    // Delete old clusters for this tenant
    await this.clickhouse.query(`DELETE FROM topic_clusters WHERE tenantId = '${tenantId}'`);

    // Insert new clusters
    for (const row of flatten(clusters)) {
      await this.clickhouse.insert('topic_clusters', {
        ...row,
        representativeCalls: JSON.stringify(row.representativeCalls),
        topWords: JSON.stringify(row.topWords),
      });
    }
  }

  private async getTranscriptions(tenantId: string): Promise<Array<{ callSid: string; text: string }>> {
    const result = await this.clickhouse.query(`
      SELECT callSid, transcription
      FROM call_transcriptions
      WHERE tenantId = '${tenantId}'
        AND timestamp >= now() - INTERVAL 7 DAY
        AND transcription IS NOT NULL
        AND transcription != ''
    `);
    return result.map((r: any) => ({ callSid: r.callSid, text: r.transcription }));
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| BERTopic (MIT) | Server | Transformer-based topic modeling |
| Gensim (LGPL-2.1) | Server | LDA topic modeling |
| scikit-learn (BSD-3) | Server | TF-IDF + K-means clustering |
| ClickHouse (Apache 2.0) | Server | Topic cluster storage |

## Production Considerations

**Scaling:** BERTopic requires GPU for reasonable performance. A single GPU (NVIDIA T4) processes ~5,000 transcriptions/hour. For tenants with 50,000 calls/week, allocate 2 GPU hours per week for clustering. LDA and K-means run on CPU and handle 50,000 transcriptions in < 30 minutes. Topic clustering runs nightly — results are available the next morning. Once clustering is complete, topic assignments are cached in Redis for dashboard queries.

**Security:** Topic cluster results contain transcription snippets (representative calls) — these are PII. Access to the representative calls requires the `calls:view-transcription` permission. Cluster-level aggregate data (topic name, call count, average sentiment) is accessible with `analytics:view`. Topic definitions and auto-labels are tenant-scoped.

**Monitoring:** Track clustering algorithm runtime, topic count, coherence score, and coverage (percentage of calls assigned to a topic). Alert if BERTopic GPU utilization exceeds 90% for more than 30 minutes. Alert if coherence score drops below 0.3 (indicates poor topic quality). Monitor the number of unlabeled topics — if > 10 topics remain unlabeled for more than 7 days, send a reminder to the tenant admin.
