# Section 02: Audio Quality Metrics Collection

## Overview

Audio quality metrics collection gathers the raw data needed for MOS calculation and quality analysis. Key metrics include jitter (variation in packet arrival time), packet loss (percentage of lost audio packets), round-trip time, codec bitrate, signal level (volume), and noise floor. These are collected per-call-segment from WebRTC statistics and network measurements.

## Implementation Approach

```typescript
interface AudioQualityMetrics {
  callId: string;
  timestamp: number;
  jitter: { min: number; max: number; avg: number }; // ms
  packetLoss: { total: number; rate: number }; // count, percentage
  roundTripTime: { min: number; max: number; avg: number }; // ms
  codec: string; // e.g., 'opus', 'pcmu', 'pcma'
  bitrate: number; // kbps
  signalLevel: number; // dBm
  noiseFloor: number; // dBm
  snr: number; // dB
}

class QualityMetricsCollector {
  private metrics: Map<string, AudioQualityMetrics[]> = new Map();

  collect(callId: string, stats: RTCPeerConnectionStats): void {
    const metric: AudioQualityMetrics = {
      callId,
      timestamp: Date.now(),
      jitter: {
        min: stats.jitterMin,
        max: stats.jitterMax,
        avg: stats.jitterAverage,
      },
      packetLoss: {
        total: stats.packetsLost,
        rate: stats.packetsSent > 0 ? stats.packetsLost / stats.packetsSent : 0,
      },
      roundTripTime: {
        min: stats.rttMin,
        max: stats.rttMax,
        avg: stats.rttAverage,
      },
      codec: stats.codecName,
      bitrate: stats.bitrate,
      signalLevel: this.measureSignalLevel(stats),
      noiseFloor: this.measureNoiseFloor(stats),
      snr: this.calculateSNR(stats),
    };

    if (!this.metrics.has(callId)) this.metrics.set(callId, []);
    this.metrics.get(callId)!.push(metric);
  }
}
```

## Integration Points

- **WebRTC Stats**: Collected from RTCPeerConnection.getStats()
- **Call Records**: Stored alongside call metadata
- **Analytics Pipeline**: Metrics aggregated into analytics database

## Production Considerations

- **Collection Overhead**: Stats collection should not impact call quality
- **Sampling Rate**: Collect stats every 1-5 seconds per call
- **Storage Volume**: Quality metrics for millions of calls require efficient storage
