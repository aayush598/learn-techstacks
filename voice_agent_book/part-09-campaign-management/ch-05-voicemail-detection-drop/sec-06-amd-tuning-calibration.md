# Section 06: AMD Tuning & Calibration

## Overview

AMD performance varies significantly based on carrier, region, language, and audio quality. A model that achieves 95% accuracy on Verizon US calls may drop to 70% on Vodafone UK calls. Tuning and calibration is the process of adjusting AMD parameters — thresholds, model weights, and processing settings — to optimize accuracy for specific operating conditions. This is an ongoing process that requires monitoring, analysis, and adjustment as conditions change.

The calibration system tracks AMD decisions against actual outcomes (did the system correctly identify human vs. machine?), identifies performance patterns by carrier and region, and suggests or automatically applies calibration adjustments. It maintains per-carrier profiles that include model weights, decision thresholds, and pre-processing parameters. The system also supports A/B testing of calibration profiles to validate improvements before full deployment.

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
class AmdCalibrator {
  constructor(analyticsDb, profileStore) {
    this.analytics = analyticsDb;
    this.profiles = profileStore;
    this.performanceThresholds = {
      minAccuracy: 0.90,
      maxFalsePositive: 0.03,
      minSampleSize: 500 // Minimum calls before calibration
    };
  }

  async getCalibrationReport() {
    const carriers = await this.getActiveCarriers();
    const report = [];

    for (const carrier of carriers) {
      const metrics = await this.getCarrierMetrics(carrier);
      const needsCalibration = this.needsCalibration(metrics);
      
      report.push({
        carrier,
        metrics,
        needsCalibration,
        suggestedChanges: needsCalibration ? 
          this.suggestCalibration(carrier, metrics) : null
      });
    }

    return report;
  }

  async getCarrierMetrics(carrier) {
    const recentCalls = await this.analytics.getCarrierCalls(carrier, {
      start: new Date(Date.now() - 7 * 86400000),
      end: new Date()
    });

    if (recentCalls.length < this.performanceThresholds.minSampleSize) {
      return { 
        carrier, 
        status: 'insufficient_data',
        sampleSize: recentCalls.length 
      };
    }

    // Calculate metrics
    let correct = 0;
    let falsePositive = 0; // Human classified as machine
    let falseNegative = 0; // Machine classified as human

    for (const call of recentCalls) {
      if (call.amdDecision === call.actualOutcome) {
        correct++;
      } else if (call.actualOutcome === 'human' && call.amdDecision === 'machine') {
        falsePositive++;
      } else if (call.actualOutcome === 'machine' && call.amdDecision === 'human') {
        falseNegative++;
      }
    }

    return {
      carrier,
      status: 'sufficient_data',
      sampleSize: recentCalls.length,
      accuracy: correct / recentCalls.length,
      falsePositiveRate: falsePositive / recentCalls.length,
      falseNegativeRate: falseNegative / recentCalls.length,
      humanCount: recentCalls.filter(c => c.actualOutcome === 'human').length,
      machineCount: recentCalls.filter(c => c.actualOutcome === 'machine').length,
      avgConfidence: recentCalls.reduce((s, c) => s + c.amdConfidence, 0) / recentCalls.length
    };
  }

  needsCalibration(metrics) {
    if (metrics.status === 'insufficient_data') return false;
    return metrics.accuracy < this.performanceThresholds.minAccuracy ||
           metrics.falsePositiveRate > this.performanceThresholds.maxFalsePositive;
  }

  suggestCalibration(carrier, metrics) {
    const profile = this.profiles.get(carrier) || this.profiles.getDefault();
    const changes = {};

    // If false positive rate is too high, increase human threshold
    if (metrics.falsePositiveRate > this.performanceThresholds.maxFalsePositive) {
      changes.humanThreshold = Math.min(1.0, (profile.humanThreshold || 0.8) + 0.05);
      changes.message = `False positive rate ${(metrics.falsePositiveRate * 100).toFixed(1)}% exceeds ${(this.performanceThresholds.maxFalsePositive * 100).toFixed(0)}% threshold. Increasing human classification threshold.`;
    }

    // If overall accuracy is low, adjust ML/heuristic weight
    if (metrics.accuracy < this.performanceThresholds.minAccuracy) {
      // Reduce ML weight if it's performing poorly
      changes.mlWeight = Math.max(0.3, (profile.mlWeight || 0.7) - 0.05);
      changes.heuristicWeight = 1 - changes.mlWeight;
    }

    // If average confidence is low, increase minimum audio duration
    if (metrics.avgConfidence < 0.7) {
      changes.minAudioMs = Math.min(5000, (profile.minAudioMs || 2000) + 500);
    }

    return Object.keys(changes).length > 0 ? changes : null;
  }

  async applyCalibration(carrier, changes, operator) {
    const currentProfile = this.profiles.get(carrier) || this.profiles.getDefault();
    
    const newProfile = {
      ...currentProfile,
      ...changes,
      lastCalibrated: new Date(),
      lastCalibratedBy: operator
    };

    // Create test profile — apply to 10% of calls initially
    const testProfile = await this.profiles.createTestProfile(
      carrier, 
      newProfile, 
      { trafficPercent: 10 }
    );

    return {
      testProfileId: testProfile.id,
      currentProfile: currentProfile,
      proposedProfile: newProfile,
      testTrafficPercent: 10,
      estimatedDuration: this.estimateTestDuration(newProfile)
    };
  }

  async analyzeABTest(testProfileId) {
    const test = await this.profiles.getTestProfile(testProfileId);
    const testMetrics = await this.getCarrierMetrics(test.carrier, test.profileId);
    const controlMetrics = await this.getCarrierMetrics(test.carrier);

    const improvement = {
      accuracy: testMetrics.accuracy - controlMetrics.accuracy,
      falsePositive: controlMetrics.falsePositiveRate - testMetrics.falsePositiveRate
    };

    const significant = testMetrics.sampleSize >= this.performanceThresholds.minSampleSize;

    return {
      testProfileId,
      testMetrics,
      controlMetrics,
      improvement,
      statisticallySignificant: significant,
      recommendation: significant && improvement.falsePositive > 0
        ? 'deploy'
        : 'continue_testing'
    };
  }

  async autoTune() {
    // Background job that runs periodically
    const report = await this.getCalibrationReport();
    
    for (const entry of report) {
      if (entry.needsCalibration && entry.suggestedChanges) {
        await this.applyCalibration(
          entry.carrier, 
          entry.suggestedChanges,
          'system_auto_tune'
        );
      }
    }
  }
}
```

## Integration Points

- **AMD Engine (sec-02):** Consumes carrier profiles for runtime calibration
- **Analytics Pipeline (Part 11):** Provides call outcome data for performance monitoring
- **Carrier Detection Service:** Maps calls to carriers for profile selection
- **A/B Testing Framework (Ch 10):** Tests calibration profiles before full deployment
- **Admin UI:** Calibration dashboard and manual override controls
- **ML Model Service:** Carrier-specific model selection and weighting

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- False positive rate (human misclassified as machine) is the most important AMD metric — target <2%
- Carrier-specific calibration requires enough data per carrier — low-volume carriers (<500 calls/month) share default profiles
- Automated calibration changes should be reversible — maintain profile versioning with rollback capability
- A/B test duration should be at least 7 days to capture day-of-week variations
- AMD performance degrades over time as carriers change voicemail systems — continuous monitoring is essential
- Notify operators when any carrier drops below 85% accuracy
- International carriers may need language-specific calibration in addition to carrier-specific
- Calibration profiles should include model version — track which ML model version powers each profile
- Consider seasonal calibration — calling patterns change during holidays and summer months
- Test calibration changes on a small subset first, then gradually roll out based on confidence
