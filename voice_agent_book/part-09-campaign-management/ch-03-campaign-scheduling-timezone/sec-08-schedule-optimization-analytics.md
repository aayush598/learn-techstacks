# Section 08: Schedule Optimization Analytics

## Overview

Schedule optimization analytics uses historical campaign data to determine the most effective calling times for different contact segments. Rather than relying on fixed schedules, the system analyzes answer rates, conversion rates, and compliance data to recommend optimal calling windows that maximize contact rates while maintaining compliance. This data-driven approach can improve answer rates by 15-30% compared to static scheduling.

The analytics engine collects per-contact call outcome data tagged with timestamps, timezone, day of week, and hour of day. Machine learning models identify patterns in when specific contact segments are most likely to answer and convert. The recommendations feed back into campaign scheduling, allowing campaigns to dynamically adjust their calling windows based on observed effectiveness. The system also tracks schedule adherence and the cost impact of off-hours calling.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Audio    |--->| WebSocket|--->| Jitter   |--->| PLC      |--->| Player   |
| Producer |    | (WSS)    |    | Buffer   |    | (Packet  |    | (smooth  |
| (100ms   |    | (binary) |    | (adaptive|    |  Loss    |    |  output) |
|  chunks) |    |          |    |  60-200) |    |  Conceal)|    +----------+
+----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```
class ScheduleOptimizer {
  constructor(analyticsDb, mlModel) {
    this.db = analyticsDb;
    this.model = mlModel;
    this.minSampleSize = 100; // Minimum calls per segment for analysis
  }

  async analyzeOptimalWindows(campaignId, segmentIds, dateRange) {
    const data = await this.collectCallData(campaignId, segmentIds, dateRange);
    
    if (data.length < this.minSampleSize) {
      return {
        sufficientData: false,
        message: `Only ${data.length} calls. Need ${this.minSampleSize}.`
      };
    }

    // Calculate answer rates by hour x day
    const heatmap = this.buildHeatmap(data);
    
    // Run ML model for pattern detection
    const predictions = await this.model.predict(heatmap);
    
    // Generate recommendations
    const recommendations = this.generateRecommendations(heatmap, predictions);

    return {
      sufficientData: true,
      totalCalls: data.length,
      heatmap,
      predictions,
      recommendations,
      segments: segmentIds
    };
  }

  buildHeatmap(callRecords) {
    const heatmap = {};

    for (const record of callRecords) {
      const hour = record.localHour;
      const day = record.localDayOfWeek;
      const key = `${day}_${hour}`;

      if (!heatmap[key]) {
        heatmap[key] = { calls: 0, answers: 0, conversions: 0 };
      }

      heatmap[key].calls++;
      if (record.answered) heatmap[key].answers++;
      if (record.converted) heatmap[key].conversions++;
    }

    // Calculate rates
    for (const [key, data] of Object.entries(heatmap)) {
      data.answerRate = data.answers / data.calls;
      data.conversionRate = data.conversions / data.calls;
      data.confidence = this.calculateConfidence(data.calls);
    }

    return heatmap;
  }

  generateRecommendations(heatmap, predictions) {
    const days = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'];
    const hours = Array.from({ length: 12 }, (_, i) => i + 8); // 8 AM - 8 PM

    // Find top 5 time slots by predicted answer rate
    const slots = [];
    
    for (const day of days) {
      for (const hour of hours) {
        const key = `${day}_${hour}`;
        const predicted = predictions[key] || 0;
        const actual = heatmap[key];
        
        slots.push({
          day,
          hour,
          predictedAnswerRate: predicted,
          actualAnswerRate: actual?.answerRate || 0,
          sampleSize: actual?.calls || 0
        });
      }
    }

    slots.sort((a, b) => b.predictedAnswerRate - a.predictedAnswerRate);

    const topSlots = slots.slice(0, 5);
    const currentRate = this.calculateCurrentAnswerRate(heatmap);
    const predictedRate = this.calculateWeightedAverage(topSlots);

    return {
      currentBestSlots: this.findCurrentBest(heatmap),
      recommendedSlots: topSlots,
      expectedImprovement: predictedRate - currentRate,
      confidence: this.calculateRecommendationConfidence(heatmap)
    };
  }

  async applyRecommendation(campaignId, recommendation, operatorId) {
    // Recommendation creates a schedule change request
    const changeRequest = await this.prisma.scheduleChange.create({
      data: {
        campaign_id: campaignId,
        proposed_schedule: recommendation.recommendedSlots,
        expected_improvement: recommendation.expectedImprovement,
        confidence: recommendation.confidence,
        proposed_by: 'system_optimizer',
        reviewed_by: operatorId,
        status: 'pending_review'
      }
    });

    return changeRequest;
  }

  calculateConfidence(sampleSize) {
    if (sampleSize < 100) return 0.3;
    if (sampleSize < 500) return 0.6;
    if (sampleSize < 1000) return 0.8;
    return 0.95;
  }
}
```

## Integration Points

- **Campaign Schedule (sec-01):** Optimization recommendations update campaign schedules
- **Calling Window Enforcement (sec-03):** Optimized windows still subject to compliance constraints
- **A/B Testing (Ch 10):** Schedule optimization can be A/B tested against current schedules
- **Analytics Pipeline (Part 11, Ch 01):** Call outcome data feeds the optimization engine
- **Campaign Dashboard (Ch 09):** Optimization recommendations displayed in campaign management UI
- **ML Pipeline:** Model training infrastructure for periodic model retraining

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Schedule optimization requires sufficient data — at least 1,000 calls per segment for meaningful analysis
- Seasonal patterns (holidays, summer vs. winter) affect optimal calling times — compare same-season data
- Contact behavior changes over time — retrain optimization models monthly
- Optimized schedules must still comply with all regulatory calling windows — optimization is within bounds
- Present optimization as "suggested changes" with expected impact rather than automatic adjustments
- Track optimization effectiveness — compare answer rates before and after schedule changes
- Small segments may never have enough data for reliable optimization — fall back to global patterns
- External events (sports games, major news) can temporarily shift optimal calling times
- Consider "time to answer" (calls that ring for 30+ seconds) as a signal — different time zones or working patterns
- Optimization analytics can also identify worst-performing times to avoid — equally valuable as best times
