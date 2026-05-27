# Section 08: Unified Sentiment Analysis Adapter

## Overview

The unified sentiment analysis adapter is the integration layer that abstracts all sentiment-related functionality behind a single, consistent API. It provides access to real-time sentiment (per-call and per-segment), historical sentiment trends, per-agent sentiment metrics, topic-based sentiment breakdowns, sentiment alerts and insights, and drill-down analysis. The adapter handles routing queries to the appropriate data stores (Redis for real-time, ClickHouse for historical), manages caching, enforces permissions, and transforms data into a unified format.

The adapter implements the Sentiment Data Protocol (SDP), a GraphQL API that exposes sentiment data as a connected graph of types. A single query can fetch a call's real-time sentiment, the agent's 30-day sentiment trend, and the tenant-level topic breakdown for the last week. The adapter also provides WebSocket subscriptions for real-time sentiment updates, enabling live sentiment dashboards and alert notifications.

## Architecture

```
           Unified Sentiment Analysis Adapter

   Dashboard / API Clients
        |
   GraphQL (Sentiment Data Protocol)
        |
   ┌────┴────┐
   | Adapter  |
   └────┬────┘
        |
   ┌────┼────────────┬────────────┬──────────┐
   |    |            |            |          |
   Real-time  Historical  Per-Agent  Topic    Insights
   Resolver   Resolver    Resolver   Resolver Resolver
   |    |            |            |          |
   Redis   ClickHouse   ClickHouse ClickHouse ClickHouse
   (call    (trends,    (agent      (topic     (insight
   sent)    analytics)   metrics)   sent)      store)
```

## Design Decisions

- **GraphQL subscriptions for real-time sentiment over REST polling:** Real-time sentiment needs sub-second updates. GraphQL subscriptions use WebSocket connections established by the existing WebSocket gateway, multiplexed into the sentiment data streams. Each subscription filters by call SID, agent ID, or campaign ID, and the adapter publishes sentiment delta events to the correct subscribers. REST polling would add unnecessary latency and server load. Trade-off: GraphQL subscriptions require the WebSocket gateway to understand sentiment subscription topics, adding complexity to the gateway's channel routing.

- **Unified sentiment type system with common fields across all sentiment data:** All sentiment responses share a common interface: `{ score: Float!, label: String!, confidence: Float!, timestamp: Float!, source: String! }`. This consistency allows frontend components to render any sentiment value the same way, whether it's real-time per-segment sentiment or historical daily average. Extended types (CallSentiment, AgentSentiment, TopicSentiment) add domain-specific fields. Trade-off: the unified type system constrains the schema — if a new sentiment model produces unique metadata, it may not fit the common interface.

- **Adapter-level caching with time-aware invalidation over no caching:** Sentiment data changes at different rates: real-time sentiment changes every 2-5 seconds, per-agent averages change every few calls, topic breakdowns change hourly. The adapter maintains a cache with per-resolver TTLs: 3 seconds for real-time, 5 minutes for per-agent, 30 minutes for topic breakdowns. Cache invalidation is time-based (TTL expiration) rather than event-driven, simplifying the architecture. Trade-off: time-based invalidation means the dashboard may show slightly stale data (up to the TTL); a "last updated" indicator is shown alongside data.

## Implementation Approach

```typescript
// === Sentiment Data Protocol Types ===

interface SentimentValue {
  score: number;              // -1.0 to 1.0
  label: 'positive' | 'neutral' | 'negative';
  confidence: number;         // 0-1
  timestamp: number;
  source: 'realtime' | 'post_call' | 'aggregated';
}

interface CallSentiment extends SentimentValue {
  callSid: string;
  tenantId: string;
  agentId: string;
  segmentIndex?: number;
  speaker?: 'agent' | 'customer';
  timeline?: Array<{ timeOffset: number; score: number; speaker: string }>;
  agentSentiment?: number;
  customerSentiment?: number;
  emotions?: Record<string, number>;
}

// === Unified Adapter Implementation ===

class SentimentAdapter {
  private redis: Redis;
  private clickhouse: ClickHouseClient;
  private sentimentPipeline: SentimentPipeline;
  private trendService: SentimentTrendService;
  private perAgentService: PerAgentSentimentService;
  private topicService: TopicSentimentService;
  private insightGenerator: InsightsGenerator;
  private drillService: SentimentDrillService;
  private cache: CacheManager;

  constructor() {
    this.redis = new Redis({ host: process.env.REDIS_HOST });
    this.clickhouse = new ClickHouseClient({ host: process.env.CLICKHOUSE_HOST });
    this.cache = new CacheManager({ adapter: 'redis' });
  }

  // Resolvers

  async getCallSentiment(callSid: string, tenantId: string): Promise<CallSentiment | null> {
    // Try real-time first
    const realtime = await this.sentimentPipeline.getRealtimeSentiment(callSid);
    if (realtime) {
      return {
        callSid, tenantId, agentId: '',
        score: realtime.score,
        label: realtime.label,
        confidence: 0.8,
        timestamp: realtime.lastUpdated,
        source: 'realtime',
      };
    }

    // Fall back to post-call analysis
    const cacheKey = `sentiment:call:${tenantId}:${callSid}`;
    return this.cache.wrap(cacheKey, async () => {
      const full = await this.sentimentPipeline.getCallSentimentSummary(callSid, tenantId);
      if (!full) return null;

      return {
        callSid, tenantId, agentId: full.agentId ?? '',
        score: full.overallScore,
        label: full.overallLabel,
        confidence: 0.9,
        timestamp: Date.now(),
        source: 'post_call',
        timeline: full.sentimentTimeline,
        customerSentiment: full.customerSentiment,
        agentSentiment: full.agentSentiment,
        emotions: full.emotionSummary,
      };
    }, 60); // 1 min TTL
  }

  async getAgentSentimentTrend(
    agentId: string,
    tenantId: string,
    start: number,
    end: number,
    granularity: string = 'day'
  ): Promise<SentimentValue[]> {
    const cacheKey = `sentiment:agent:${tenantId}:${agentId}:${granularity}:${start}:${end}`;
    return this.cache.wrap(cacheKey, async () => {
      const trend = await this.trendService.getTrend({
        tenantId,
        granularity: granularity as any,
        start: new Date(start).toISOString(),
        end: new Date(end).toISOString(),
      });
      return trend.data.map(d => ({
        score: d.averageSentiment,
        label: d.averageSentiment > 0.2 ? 'positive' : d.averageSentiment < -0.2 ? 'negative' : 'neutral',
        confidence: 0.9,
        timestamp: new Date(d.period).getTime(),
        source: 'aggregated' as const,
      }));
    }, 300); // 5 min TTL
  }

  async getTopicSentimentBreakdown(
    tenantId: string,
    start: number,
    end: number
  ): Promise<Array<{ topic: string; sentiment: SentimentValue; callCount: number }>> {
    const cacheKey = `sentiment:topic:${tenantId}:${start}:${end}`;
    return this.cache.wrap(cacheKey, async () => {
      const topics = await this.topicService.getTopicSentiment(tenantId, start, end);
      return topics.map(t => ({
        topic: t.topicName,
        sentiment: {
          score: t.averageSentiment,
          label: t.averageSentiment > 0.2 ? 'positive' : t.averageSentiment < -0.2 ? 'negative' : 'neutral',
          confidence: t.mentions > 50 ? 0.9 : 0.7,
          timestamp: end,
          source: 'aggregated' as const,
        },
        callCount: t.callCount,
      }));
    }, 1800); // 30 min TTL
  }

  async generateInsights(
    tenantId: string,
    start: number,
    end: number
  ): Promise<Array<{ title: string; description: string; severity: string; recommendation?: string }>> {
    const insights = await this.insightGenerator.generateInsights(tenantId, start, end);
    return insights.map(i => ({
      title: i.title,
      description: i.description,
      severity: i.severity,
      recommendation: i.recommendation,
    }));
  }

  // GraphQL schema definition
  typeDefs = `
    type Sentiment {
      score: Float!
      label: String!
      confidence: Float!
      timestamp: Float!
      source: String!
    }

    type CallSentiment implements Sentiment {
      score: Float!
      label: String!
      confidence: Float!
      timestamp: Float!
      source: String!
      callSid: String!
      agentId: String!
      timeline: [SentimentTimelinePoint!]
      customerSentiment: Float
      agentSentiment: Float
    }

    type SentimentTimelinePoint {
      timeOffset: Float!
      score: Float!
      speaker: String!
    }

    type TopicSentiment {
      topic: String!
      sentiment: Sentiment!
      callCount: Int!
    }

    type SentimentInsight {
      title: String!
      description: String!
      severity: String!
      recommendation: String
    }

    type Query {
      callSentiment(callSid: String!): CallSentiment
      agentSentimentTrend(agentId: String!, start: Float!, end: Float!, granularity: String): [Sentiment!]!
      topicSentimentBreakdown(start: Float!, end: Float!): [TopicSentiment!]!
      sentimentInsights(start: Float!, end: Float!): [SentimentInsight!]!
    }

    type Subscription {
      callSentimentUpdated(callSid: String!): CallSentiment!
      agentSentimentUpdated(agentId: String!): Sentiment!
    }
  `;

  // Subscription resolvers (using WebSocket gateway)
  subscriptions = {
    callSentimentUpdated: {
      subscribe: async function* (callSid: string, context: Context) {
        const channel = `sentiment:call:${callSid}`;
        for await (const message of context.wsGateway.subscribe(channel)) {
          yield { callSentimentUpdated: JSON.parse(message) };
        }
      },
    },
  };
}

// React hook for sentiment subscription
function useCallSentiment(callSid: string) {
  const [sentiment, setSentiment] = useState<CallSentiment | null>(null);

  useEffect(() => {
    const subscription = graphqlClient.subscribe(
      `subscription { callSentimentUpdated(callSid: "${callSid}") { score label timeline } }`,
      (data) => setSentiment(data.callSentimentUpdated)
    );
    return () => subscription.unsubscribe();
  }, [callSid]);

  return sentiment;
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Apollo Server (MIT) | Server | GraphQL server |
| GraphQL Yoga (MIT) | Server | Alternative GraphQL implementation |
| Redis (RSAL) | Server | Cache and real-time sentiment store |
| ClickHouse (Apache 2.0) | Server | Historical sentiment data |

## Production Considerations

**Scaling:** The adapter is stateless and scales horizontally. Each resolver uses DataLoader-style batching where possible (e.g., fetching sentiment for 20 calls in one Redis pipeline). Cache TTLs are tuned to balance freshness with database load — real-time resolvers have short TTLs (3 seconds) and bypass cache entirely for WebSocket subscriptions. For high-traffic tenants (100+ dashboard users), add a CDN in front of the GraphQL endpoint for trend data (cache at 5-min granularity).

**Security:** Every resolver checks the context's permissions and tenant ID. The `callSentiment` resolver requires `calls:view` permission for the call's tenant. The `agentSentimentTrend` resolver requires `agent-performance:view`. The `topicSentimentBreakdown` resolver requires `analytics:view`. Subscription resolvers validate that the subscribing user has permission for the specific call or agent.

**Monitoring:** Track resolver call rate, cache hit rate per resolver, GraphQL query depth and complexity, and subscription count per tenant. Alert if any resolver's p95 exceeds 200 ms. Monitor the WebSocket subscription count — if it exceeds 10,000 concurrent subscriptions, consider partitioning by tenant across gateway instances.
