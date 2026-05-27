# Device Fingerprinting

## Overview

Device fingerprinting creates a unique identifier for each device based on passive characteristics. This enables trusted device recognition, helps detect account takeover, and supports risk-based authentication decisions.

## Fingerprint Collection

```typescript
interface DeviceFingerprint {
  id: string;
  hash: string;              // SHA-256 hash of collected signals
  signals: FingerprintSignals;
  firstSeen: Date;
  lastSeen: Date;
  trustScore: number;        // 0-100 (higher = more trusted)
  userId: string;
}

interface FingerprintSignals {
  // Browser/OS signals
  userAgent: string;
  platform: string;
  language: string;
  timezone: string;
  screenResolution: string;
  colorDepth: number;
  deviceMemory?: number;
  hardwareConcurrency?: number;

  // Network signals
  ipAddress: string;
  ipOrganization?: string;

  // Canvas/webgl fingerprint (with user consent)
  canvasHash?: string;
  webglHash?: string;

  // Font detection
  fontsHash?: string;

  // Audio fingerprint
  audioHash?: string;

  // Storage
  localStorageEnabled: boolean;
  cookiesEnabled: boolean;
}
```

## Fingerprint Service

```typescript
class DeviceFingerprintService {
  async collectFingerprint(req: Request): Promise<FingerprintSignals> {
    return {
      userAgent: req.headers['user-agent'] || '',
      platform: req.headers['sec-ch-ua-platform'] || '',
      language: req.headers['accept-language'] || '',
      timezone: req.headers['timezone'] || '',
      screenResolution: req.headers['sec-ch-viewport-width']
        ? `${req.headers['sec-ch-viewport-width']}x${req.headers['sec-ch-viewport-height']}`
        : '',
      ipAddress: req.ip,
      localStorageEnabled: true,
      cookiesEnabled: true,
    };
  }

  async computeHash(signals: FingerprintSignals): Promise<string> {
    const normalized = {
      ua: signals.userAgent,
      platform: signals.platform,
      lang: signals.language,
      tz: signals.timezone,
      screen: signals.screenResolution,
      fonts: signals.fontsHash,
    };

    const json = JSON.stringify(normalized);
    return createHash('sha256').update(json).digest('hex');
  }

  async identify(signals: FingerprintSignals): Promise<DeviceFingerprint | null> {
    const hash = await this.computeHash(signals);
    return this.db.findOne('device_fingerprints', { hash });
  }

  async trustDevice(userId: string, signals: FingerprintSignals): Promise<DeviceFingerprint> {
    const hash = await this.computeHash(signals);

    let fp = await this.db.findOne('device_fingerprints', { hash });
    if (fp) {
      fp.lastSeen = new Date();
      fp.trustScore = Math.min(100, fp.trustScore + 5);
      fp.userId = userId;
      await this.db.update('device_fingerprints', { id: fp.id }, fp);
    } else {
      fp = {
        id: generateId('fp'),
        hash,
        signals,
        firstSeen: new Date(),
        lastSeen: new Date(),
        trustScore: 20, // Initial trust score
        userId,
      };
      await this.db.insert('device_fingerprints', fp);
    }

    return fp;
  }

  async isDeviceTrusted(userId: string, hash: string, minTrustScore: number = 50): Promise<boolean> {
    const fp = await this.db.findOne('device_fingerprints', { hash, userId });
    if (!fp) return false;

    // Trust decays over time
    const daysSinceLastSeen = (Date.now() - fp.lastSeen.getTime()) / 86400000;
    const decayedScore = fp.trustScore - daysSinceLastSeen * 2;

    return decayedScore >= minTrustScore;
  }
}
```

## Anomaly Detection

```typescript
class FingerprintAnomalyDetector {
  async detect(userId: string, currentFingerprint: string, ip: string): Promise<AnomalyResult> {
    const userFingerprints = await this.db.find('device_fingerprints', { userId });
    const knownHashes = userFingerprints.map(f => f.hash);

    // New device detection
    if (!knownHashes.includes(currentFingerprint)) {
      const recentNewDevices = userFingerprints.filter(
        f => f.firstSeen.getTime() > Date.now() - 86400000
      );

      if (recentNewDevices.length >= 3) {
        return { anomaly: true, risk: 'high', reason: 'Multiple new devices in 24h' };
      }

      return { anomaly: true, risk: 'medium', reason: 'Unknown device' };
    }

    // Known device from unusual location
    const knownDevice = userFingerprints.find(f => f.hash === currentFingerprint);
    if (knownDevice && knownDevice.signals.ipAddress !== ip) {
      const ipChanged = await this.ipChangedRecently(userId, currentFingerprint, ip);
      if (ipChanged) {
        return { anomaly: true, risk: 'low', reason: 'Known device, new IP' };
      }
    }

    return { anomaly: false, risk: 'low', reason: 'Normal' };
  }
}
```

## Open-Source Tools

- **FingerprintJS** (MIT) — Browser fingerprinting library
- **ClientJS** (MIT) — Device fingerprinting
- **maxmind** — GeoIP lookup for location signals

## Production Considerations

- Require user consent for canvas/WebGL fingerprinting (GDPR)
- Store fingerprint hashes, never raw signal data
- Fingerprint trust score increases with successful logins (+5 per login)
- Trust decays over time (-2 per day since last seen)
- Max 20 stored fingerprints per user
- Do not use fingerprints as sole authentication factor
- Refresh fingerprint on each login to detect device changes
- Allow users to view and revoke trusted devices in settings
