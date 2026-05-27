# Anomaly Detection

## Overview

Session-level anomaly detection identifies suspicious behavior patterns that may indicate account compromise. Detection covers impossible travel, unusual IP addresses, device changes, and behavioral baselines.

## Detection Types

```typescript
interface AnomalyDetectionConfig {
  enableImpossibleTravel: boolean;
  impossibleTravelThresholdKm: number;    // 500km minimum for impossible travel
  impossibleTravelTimeThresholdMin: number; // 60 min window

  enableUnusualIp: boolean;
  unusualIpThreshold: number;              // Z-score threshold

  enableDeviceChangeAlerts: boolean;
  maxDeviceChangesPerDay: number;          // 3

  enableBehavioralBaseline: boolean;
  baselineTrainingDays: number;            // 30
  baselineDeviationThreshold: number;      // 2 standard deviations
}

class SessionAnomalyDetector {
  async analyze(userId: string, session: Session): Promise<AnomalyResult[]> {
    const anomalies: AnomalyResult[] = [];

    if (config.enableImpossibleTravel) {
      const travelAnomaly = await this.checkImpossibleTravel(userId, session);
      if (travelAnomaly) anomalies.push(travelAnomaly);
    }

    if (config.enableUnusualIp) {
      const ipAnomaly = await this.checkUnusualIp(userId, session);
      if (ipAnomaly) anomalies.push(ipAnomaly);
    }

    if (config.enableDeviceChangeAlerts) {
      const deviceAnomaly = await this.checkDeviceChangeRate(userId);
      if (deviceAnomaly) anomalies.push(deviceAnomaly);
    }

    return anomalies;
  }

  private async checkImpossibleTravel(userId: string, session: Session): Promise<AnomalyResult | null> {
    const previousSession = await this.getPreviousSession(userId);
    if (!previousSession) return null;

    const currentIp = session.ipAddress;
    const previousIp = previousSession.ipAddress;
    const timeDiff = (session.lastActivity.getTime() - previousSession.lastActivity.getTime()) / 60000;

    if (timeDiff < config.impossibleTravelTimeThresholdMin) {
      const distance = this.calculateDistance(currentIp, previousIp);
      if (distance > config.impossibleTravelThresholdKm) {
        return {
          type: 'impossible_travel',
          severity: 'critical',
          details: {
            distanceKm: distance,
            timeMinutes: timeDiff,
            previousIp,
            currentIp,
            previousLocation: previousSession.ipAddress,
            currentLocation: session.ipAddress,
          },
        };
      }
    }

    return null;
  }

  private async checkDeviceChangeRate(userId: string): Promise<AnomalyResult | null> {
    const recentFingerprints = await this.getRecentFingerprints(userId, 86400000);
    if (recentFingerprints.length >= config.maxDeviceChangesPerDay) {
      return {
        type: 'excessive_device_changes',
        severity: 'high',
        details: { deviceCount: recentFingerprints.length, timeWindow: '24h' },
      };
    }
    return null;
  }
}
```

## Behavioral Baseline

```typescript
class BehavioralBaseline {
  async buildBaseline(userId: string): Promise<UserBehaviorBaseline> {
    const sessions = await this.getHistoricalSessions(userId, 30);

    return {
      userId,
      typicalLoginHours: this.getTypicalHours(sessions),
      typicalIpRanges: this.getTypicalIpRanges(sessions),
      typicalUserAgents: this.getTypicalUserAgents(sessions),
      avgSessionDuration: this.average(sessions.map(s =>
        (s.expiresAt.getTime() - s.createdAt.getTime()) / 3600000
      )),
      stdDevSessionDuration: this.stdDev(sessions.map(s =>
        (s.expiresAt.getTime() - s.createdAt.getTime()) / 3600000
      )),
      commonResources: this.getFrequentResources(sessions),
    };
  }

  async checkDeviation(userId: string, currentSession: Session): Promise<DeviationResult> {
    const baseline = await this.getBaseline(userId);
    const deviations: string[] = [];

    const loginHour = currentSession.lastActivity.getHours();
    if (!baseline.typicalLoginHours.includes(loginHour)) {
      deviations.push(`Unusual login hour: ${loginHour}`);
    }

    return {
      hasDeviation: deviations.length > 0,
      deviations,
      score: deviations.length / 5, // 0-1 score
    };
  }
}
```

## Open-Source Tools

- **maxmind** — GeoIP databases for travel detection
- **stats-lite** (MIT) — Statistical functions (z-score, std dev)
- **simple-statistics** (MIT) — Statistical analysis

## Production Considerations

- Anomaly detection runs asynchronously (do not block login)
- Score anomalies and only alert on high/critical severity
- Allow users to confirm legitimate activity to train baseline
- Send anomaly alerts to security team via Slack/PagerDuty
- Store anomaly events for 90 days for retrospective analysis
- Rate-limit anomaly alerts per user (max 5 per hour)
- Provide anomaly review dashboard for security operations
- Support per-tenant anomaly detection configuration
