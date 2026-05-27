# Section 04: Deduplication Strategies

## Overview

Deduplication prevents alert storms by identifying and suppressing duplicate or correlated alerts. Strategies include window-based dedup (same alert within time window), fingerprinting (content-based hash), aggregation (group similar alerts), and suppression (silence after N occurrences).

## Implementation Approach

```typescript
interface DedupConfig {
  strategy: 'window' | 'fingerprint' | 'aggregation' | 'suppression';
  window: number; // seconds
  maxOccurrences: number;
  aggregateKey: string; // field to aggregate on
}

class DeduplicationEngine {
  async process(event: EnrichedEvent, rule: AlertRule): Promise<DedupResult> {
    const config = rule.dedupConfig;
    if (!config) return { action: 'pass', event };

    switch (config.strategy) {
      case 'window':
        return this.windowDedup(event, rule, config);
      case 'fingerprint':
        return this.fingerprintDedup(event, config);
      case 'aggregation':
        return this.aggregationDedup(event, config);
      case 'suppression':
        return this.suppressionDedup(event, rule, config);
      default:
        return { action: 'pass', event };
    }
  }

  private async windowDedup(event: EnrichedEvent, rule: AlertRule, config: DedupConfig): Promise<DedupResult> {
    const key = `dedup:${rule.id}:${event.tenantId}`;
    const lastTriggered = await this.cache.get(key);
    if (lastTriggered) {
      const elapsed = (Date.now() - parseInt(lastTriggered)) / 1000;
      if (elapsed < config.window) {
        return { action: 'suppress', event, reason: 'dedup_window' };
      }
    }
    await this.cache.set(key, Date.now().toString(), { EX: config.window });
    return { action: 'pass', event };
  }

  private async fingerprintDedup(event: EnrichedEvent, config: DedupConfig): Promise<DedupResult> {
    const fingerprint = this.computeFingerprint(event);
    const existing = await this.storage.findOne({ fingerprint });
    if (existing) return { action: 'suppress', event, reason: 'duplicate_fingerprint' };
    return { action: 'pass', event };
  }

  private computeFingerprint(event: EnrichedEvent): string {
    const components = [
      event.type,
      event.tenantId,
      event.metricName,
      JSON.stringify(event.dimensions),
    ];
    return crypto.createHash('md5').update(components.join(':')).digest('hex');
  }

  private async aggregationDedup(event: EnrichedEvent, config: DedupConfig): Promise<DedupResult> {
    const key = event.dimensions[config.aggregateKey] || 'default';
    const group = await this.aggregationStore.getGroup(key);
    group.events.push(event);
    if (group.events.length >= config.maxOccurrences) {
      const aggregated = this.mergeEvents(group.events);
      await this.aggregationStore.clearGroup(key);
      return { action: 'pass', event: aggregated, aggregated: true };
    }
    await this.aggregationStore.saveGroup(key, group);
    return { action: 'suppress', event, reason: 'aggregating' };
  }
}
```

## Integration Points

- **State Store**: Redis for dedup state (TTL-based cleanup)
- **Alert Pipeline**: Dedup runs before alert creation
- **Dashboard**: Dedup stats tracked (suppressed vs created)

## Production Considerations

- **Memory Management**: TTL on dedup keys prevents memory leak
- **False Suppression**: Window too long may miss legitimate duplicates
- **Tuning**: Adjust window and max occurrences based on alert patterns
