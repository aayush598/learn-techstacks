# Section 08: Script Performance Testing

## Overview

Script performance testing measures how effectively a script achieves its goals — call completion rate, conversion rate, customer satisfaction, compliance adherence, and average handle time. Unlike A/B testing which compares two complete scripts, script performance testing is a continuous monitoring and optimization process that identifies specific elements of a script that drive or hinder performance.

The testing framework collects metrics per script version, segments performance by contact attributes, identifies underperforming script sections, and provides actionable optimization recommendations. It supports granular analysis at the turn-by-turn level (which parts of the conversation correlate with successful outcomes), sentiment analysis during specific script sections, and drift detection when script performance changes over time.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Script Performance Testing                      │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Metrics Collection by Script Segment                │   │
│  │                                                      │   │
│  │  Opening → Qualification → Offer → Closing          │   │
│  │     │             │           │        │             │   │
│  │  time:2s       time:45s    time:30s  time:5s       │   │
│  │  sent:+0.1     sent:-0.2   sent:+0.3 sent:+0.1    │   │
│  │  dropout:2%    dropout:8%  dropout:5% dropout:1%  │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Segment-Level Analysis                              │   │
│  │                                                      │   │
│  │  • Opening (words 1-50): 92% completion rate        │   │
│  │  • Qualification (words 51-200): 78% completion      │   │
│  │  • Offer presentation (words 201-350): 45% drop-off  │   │
│  │  • Closing (words 351-400): 90% completion          │   │
│  │                                                      │   │
│  │  → High drop-off at "offer" — consider shortening   │   │
│  └──────────────────────┬───────────────────────────────┘   │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Recommendations                                    │   │
│  │  • Shorten offer segment by 15 seconds               │   │
│  │  • Move pricing mention earlier in qualification    │   │
│  │  • Add personalization hook in opening               │   │
│  │  • Test alternative closing CTA                     │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Design Decisions

- **Segment-level analysis:** Scripts are divided into segments (opening, qualification, offer, closing) with performance tracked per segment. This identifies specific problem areas rather than just overall script performance. Trade-off: segment definition overhead vs. precise optimization targeting.

- **Sentiment correlation per section:** Customer sentiment during each script section is captured and correlated with outcomes. A negative sentiment spike during the offer section indicates pricing or messaging issues. Trade-off: sentiment processing cost vs. actionable insight.

- **Normative benchmarking:** Script performance is compared against aggregated benchmarks from similar campaigns (same campaign type, industry, region). This contextualizes whether a 15% drop-off rate is normal or concerning. Trade-off: benchmark data collection vs. contextual evaluation.

- **Automated quality scoring:** Scripts are automatically scored on readability, compliance disclosure inclusion, token usage effectiveness, and length appropriateness. Low-scoring scripts get flagged for review. Trade-off: scoring accuracy vs. review prioritization.

## Implementation Approach

```
class ScriptPerformanceAnalyzer {
  constructor(analyticsDb, sentimentService) {
    this.db = analyticsDb;
    this.sentiment = sentimentService;
  }

  async analyzeScriptPerformance(scriptVersionId, dateRange) {
    const calls = await this.getCallsUsingScript(scriptVersionId, dateRange);
    if (calls.length < 50) return { insufficientData: true };

    const segments = await this.analyzePerSegment(calls);
    const overall = this.calculateOverallMetrics(calls);
    const recommendations = this.generateRecommendations(segments, overall);
    const benchmarks = await this.getBenchmarks(calls[0].campaignType);

    return {
      scriptVersionId,
      totalCalls: calls.length,
      overall,
      segments,
      recommendations,
      benchmarks
    };
  }

  async analyzePerSegment(calls) {
    const segments = {};

    for (const call of calls) {
      const scriptSegments = await this.segmentizeCall(call);
      
      for (const segment of scriptSegments) {
        if (!segments[segment.name]) {
          segments[segment.name] = {
            name: segment.name,
            totalCalls: 0,
            completions: 0,
            totalDuration: 0,
            sentiments: [],
            conversionAfter: 0,
            dropoffsAfter: 0
          };
        }

        segments[segment.name].totalCalls++;
        
        if (segment.completed) {
          segments[segment.name].completions++;
          segments[segment.name].totalDuration += segment.duration;
        }

        if (segment.sentiment) {
          segments[segment.name].sentiments.push(segment.sentiment);
        }

        // Track what happens after this segment
        const nextSegment = this.getNextSegment(scriptSegments, segment);
        if (nextSegment) {
          if (nextSegment.outcome === 'converted') {
            segments[segment.name].conversionAfter++;
          }
        } else if (call.outcome === 'converted') {
          segments[segment.name].conversionAfter++;
        }
      }
    }

    // Calculate rates
    for (const [name, seg] of Object.entries(segments)) {
      seg.completionRate = seg.completions / seg.totalCalls;
      seg.avgDuration = seg.totalDuration / seg.completions;
      seg.avgSentiment = seg.sentiments.reduce((s, v) => s + v, 0) / seg.sentiments.length;
      seg.conversionRate = seg.conversionAfter / seg.totalCalls;
      seg.dropoffRate = 1 - (seg.completions / seg.totalCalls);
    }

    return Object.values(segments);
  }

  async segmentizeCall(call) {
    // Split the call into logical segments based on script structure
    const segments = [];
    const transcript = await this.getTranscript(call.id);
    const script = await this.getScriptContent(call.scriptVersionId);

    // Map transcript turns to script sections
    const sectionBoundaries = this.findSectionBoundaries(script);
    
    for (let i = 0; i < sectionBoundaries.length; i++) {
      const start = sectionBoundaries[i];
      const end = sectionBoundaries[i + 1] || transcript.length;
      
      const segmentText = transcript.slice(start, end).join(' ');
      const duration = this.estimateDuration(segmentText);
      const sentiment = await this.sentiment.analyze(segmentText);

      segments.push({
        name: this.getSectionName(script, start),
        startTime: call.transcript[start]?.timestamp,
        duration,
        completed: end < transcript.length || i < sectionBoundaries.length - 1,
        sentiment: sentiment.score,
        text: segmentText.substring(0, 200) // Truncate for analysis
      });
    }

    return segments;
  }

  calculateOverallMetrics(calls) {
    const completed = calls.filter(c => c.status === 'completed');
    const converted = calls.filter(c => c.outcome === 'converted');

    return {
      completionRate: completed.length / calls.length,
      conversionRate: converted.length / calls.length,
      avgHandleTime: calls.reduce((s, c) => s + c.duration, 0) / calls.length,
      avgSentiment: calls.reduce((s, c) => s + (c.sentiment || 0), 0) / calls.length,
      optOutRate: calls.filter(c => c.disposition === 'opted_out').length / calls.length,
      escalationRate: calls.filter(c => c.disposition === 'escalated').length / calls.length,
      complianceIssueRate: calls.filter(c => c.complianceIssue).length / calls.length
    };
  }

  generateRecommendations(segments, overall) {
    const recommendations = [];

    for (const segment of segments) {
      if (segment.dropoffRate > 0.2) {
        recommendations.push({
          type: 'high_dropoff',
          segment: segment.name,
          severity: segment.dropoffRate > 0.3 ? 'high' : 'medium',
          message: `"${segment.name}" segment has ${(segment.dropoffRate * 100).toFixed(0)}% drop-off rate. Consider shortening or improving engagement.`,
          expectedImpact: `${(segment.dropoffRate * overall.conversionRate * 100).toFixed(1)}% conversion lift`
        });
      }

      if (segment.avgSentiment < -0.2) {
        recommendations.push({
          type: 'negative_sentiment',
          segment: segment.name,
          severity: 'high',
          message: `"${segment.name}" segment has negative average sentiment (${segment.avgSentiment.toFixed(2)}). Review messaging tone and content.`,
          expectedImpact: 'Improved customer experience'
        });
      }

      if (segment.avgDuration > 120 && segment.conversionRate < 0.05) {
        recommendations.push({
          type: 'too_long',
          segment: segment.name,
          severity: 'medium',
          message: `"${segment.name}" segment averages ${segment.avgDuration}s with low conversion. Consider condensing.`,
          expectedImpact: 'Reduced handle time, potentially improved engagement'
        });
      }
    }

    if (optOutRate > 0.05) {
      recommendations.push({
        type: 'high_opt_out',
        severity: 'high',
        message: 'Above-average opt-out rate. Review compliance disclosures and permission messaging.',
        expectedImpact: 'Reduced compliance risk'
      });
    }

    return recommendations;
  }

  async getBenchmarks(campaignType) {
    return this.db.$queryRaw`
      SELECT 
        AVG(completion_rate) as avg_completion,
        AVG(conversion_rate) as avg_conversion,
        AVG(avg_handle_time) as avg_handle_time
      FROM campaign_benchmarks
      WHERE campaign_type = ${campaignType}
        AND created_at > NOW() - INTERVAL '90 days'
    `;
  }

  async findUnderperformingPhrases(scriptVersionId, dateRange) {
    // N-gram analysis to find phrases that correlate with negative outcomes
    const calls = await this.getCallsUsingScript(scriptVersionId, dateRange);
    const transcripts = calls.map(c => c.transcript);
    const outcomes = calls.map(c => c.outcome === 'converted' ? 1 : 0);

    // Extract bigrams and trigrams
    const ngramFrequencies = {};
    
    for (let i = 0; i < transcripts.length; i++) {
      const words = transcripts[i].toLowerCase().split(' ');
      for (let n = 2; n <= 3; n++) {
        for (let j = 0; j <= words.length - n; j++) {
          const ngram = words.slice(j, j + n).join(' ');
          if (!ngramFrequencies[ngram]) {
            ngramFrequencies[ngram] = { count: 0, conversions: 0 };
          }
          ngramFrequencies[ngram].count++;
          ngramFrequencies[ngram].conversions += outcomes[i];
        }
      }
    }

    // Find ngrams with conversion rates significantly below average
    const avgConversionRate = outcomes.reduce((s, v) => s + v, 0) / outcomes.length;
    const underperforming = Object.entries(ngramFrequencies)
      .filter(([_, data]) => data.count >= 10)
      .map(([ngram, data]) => ({
        ngram,
        count: data.count,
        conversionRate: data.conversions / data.count,
        impact: avgConversionRate - (data.conversions / data.count)
      }))
      .filter(item => item.impact > 0.1)
      .sort((a, b) => b.impact - a.impact)
      .slice(0, 10);

    return underperforming;
  }
}
```

## Integration Points

- **Call Analytics (Ch 09):** Primary data source for call outcomes and metrics
- **Transcript Service (Part 12):** Full call transcripts for segment-level analysis
- **Sentiment Analysis (Part 11, Ch 05):** Per-segment sentiment scoring
- **A/B Testing (Ch 10):** Script A/B test results inform performance analysis
- **Campaign Config (Ch 01):** Script version association with campaigns
- **QA & Testing (Part 19):** Automated quality scoring of script content

## Open-Source Tools

- **Natural (Node.js):** NLP for text analysis, keyword extraction, n-gram analysis
- **Apache ECharts / Recharts:** Performance visualization (segment funnels, sentiment trends)
- **PostgreSQL / ClickHouse:** Performance data storage and aggregation
- **simple-statistics:** Statistical analysis for performance significance testing
- **compromise / wink-nlp:** Lightweight NLP for phrase extraction and analysis

## Production Considerations

- Segment-level analysis requires structured call transcripts aligned with script sections — ensure the AI agent logs script section transitions
- Minimum sample size of 50 calls per script version for statistically meaningful analysis
- Sentiment analysis during specific script sections may be noisy — aggregate over multiple calls
- N-gram analysis for underperforming phrases requires careful PII handling — avoid leaking contact names or data in phrase analysis
- Benchmarks should be updated quarterly as industry averages change
- Performance testing results should be accessible to campaign managers in plain language, not raw statistics
- Automated recommendations should include expected impact estimates to help prioritize changes
- Script performance degradation over time may indicate concept drift — monitor trend lines, not just point-in-time metrics
- Correlate script changes with performance — a new script version should show clear improvement or be reverted
- Provide a script scorecard that summarizes key metrics in a single view for quick assessment
