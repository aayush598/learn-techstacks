# Section 03: Smart Retry & Best Time Calling

## Overview

Smart retry uses machine learning to predict the optimal time to call each contact, maximizing the probability of a successful connection. Instead of applying fixed intervals or simple rules, the system analyzes historical patterns — when has this contact answered before? When do similar contacts in the same segment answer? What time of day, day of week, and time of month yields the highest answer rate for this individual?

The smart retry model is trained on per-contact call history data, enriched with contact attributes and contextual features. It generates a personalized "best time score" for each contact at each potential calling time, enabling the retry engine to prioritize the most promising times. Over time, the model improves as more call outcome data is collected, creating a continuous optimization loop.

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
class SmartRetryEngine {
  constructor(modelServer, featureStore, attemptStore) {
    this.modelServer = modelServer;
    this.features = featureStore;
    this.attempts = attemptStore;
    this.confidenceThresholds = {
      high: 0.7,
      medium: 0.4,
      low: 0.0
    };
  }

  async getBestTime(contact, campaign, availableWindows) {
    const features = await this.buildFeatures(contact, campaign);
    
    // Score each available window
    const scoredWindows = [];

    for (const window of availableWindows) {
      const windowFeatures = {
        ...features,
        hour: window.start.getHours(),
        dayOfWeek: window.start.getDay(),
        daysSinceLastContact: this.daysSince(contact.lastContactAt),
        isHolidayProximity: await this.isNearHoliday(window.start, contact.timezone)
      };

      const score = await this.modelServer.predict(windowFeatures);
      scoredWindows.push({ window, score });
    }

    // Sort by score descending
    scoredWindows.sort((a, b) => b.score - a.score);

    // Select best window based on confidence
    const best = scoredWindows[0];
    
    if (best.score >= this.confidenceThresholds.high) {
      return { time: best.window.start, confidence: 'high', score: best.score };
    } else if (best.score >= this.confidenceThresholds.medium) {
      return { time: best.window.start, confidence: 'medium', score: best.score };
    } else {
      // No good time — return null and let the system apply fallback
      return null;
    }
  }

  async buildFeatures(contact) {
    // Gather per-contact features
    const history = await this.attempts.getHistory(contact.id);
    const heatmap = this.buildPersonalHeatmap(history);

    // Gather segment features for cold-start
    const segmentFeatures = await this.features.getSegmentAverages(
      contact.segmentId
    );

    return {
      personalHeatmap: heatmap,
      totalAttempts: history.length,
      lastOutcome: history[0]?.outcome || null,
      daysSinceLastAttempt: this.daysSince(history[0]?.timestamp),
      contactType: contact.type,
      timezone: contact.timezone,
      segmentAvgAnswerRate: segmentFeatures.avgAnswerRate,
      segmentBestHour: segmentFeatures.bestHour,
      segmentBestDay: segmentFeatures.bestDay,
      hasPriorPositiveOutcome: history.some(h => h.outcome === 'converted')
    };
  }

  buildPersonalHeatmap(history) {
    const heatmap = {};
    for (const h of history) {
      const hour = h.timestamp.getHours();
      const day = h.timestamp.getDay();
      const key = `${day}_${hour}`;
      
      if (!heatmap[key]) heatmap[key] = { attempts: 0, answers: 0 };
      heatmap[key].attempts++;
      if (h.answered) heatmap[key].answers++;
    }

    // Convert to rates
    for (const key of Object.keys(heatmap)) {
      heatmap[key].answerRate = heatmap[key].answers / heatmap[key].attempts;
    }

    return heatmap;
  }

  async recordOutcome(contactId, attemptResult) {
    // Feedback loop — record outcome for model improvement
    await this.attempts.record(contactId, attemptResult);

    // If we have enough new data, trigger async model update
    const recentCount = await this.attempts.countRecent(contactId, 24 * 60 * 60 * 1000);
    if (recentCount >= 5) {
      // Queue a model update job for this contact's model
      await this.queueModelUpdate(contactId);
    }
  }

  daysSince(date) {
    if (!date) return 999; // Large value for no history
    return Math.floor((Date.now() - new Date(date).getTime()) / 86400000);
  }
}
```

## Integration Points

- **Retry Interval Calculator (sec-02):** Smart retry time overrides interval-based calculations
- **Calling Window Enforcer (Ch 03):** Best times are constrained to valid calling windows
- **ML Pipeline (Part 18):** Model training, evaluation, and deployment pipeline
- **Feature Store (Redis/PostgreSQL):** Pre-computed features for low-latency inference
- **Campaign Analytics (Ch 09):** Smart retry effectiveness tracking
- **Contact History UI:** Display predicted best times and confidence scores

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Inference latency target: <10ms per contact — pre-compute features and cache model predictions
- Cold-start problem: segment-level fallback needs at least 100 contacts in the segment for statistical significance
- Model drift: consumer behavior changes over time — retrain models monthly with latest data
- Feature importance analysis: operators should see which features drive best-time predictions
- Privacy: per-contact models should not leak information across tenants
- A/B test smart retry vs. rule-based retry to measure actual improvement
- Smart retry may suggest the same optimal time for many contacts — ensure enough trunk capacity at that time
- Feedback loop latency: outcomes should be recorded in real-time for rapid model adjustment
- Model interpretability: provide explanation for recommendations (e.g., "John answers best at 10 AM — 80% answer rate")
- Fallback: if the ML model is unavailable, fall back to configured interval strategy
- Monitor smart retry effectiveness: compare answer rates of smart-scheduled vs. interval-scheduled calls
