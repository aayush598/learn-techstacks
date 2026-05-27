# Section 08: Bulk & Batch Email Processing

## Overview

Bulk email processing sends large volumes of transactional emails efficiently. Batch processing groups multiple emails for delivery, applies rate limiting per provider, and tracks delivery at scale. The system handles list segmentation, batch prioritization, and throttle control.

## Implementation Approach

```typescript
interface BatchConfig {
  batchSize: number;
  maxConcurrent: number;
  ratePerSecond: number;
  retryOnFailure: boolean;
  maxRetries: number;
}

interface BatchJob {
  id: string;
  emails: EmailPayload[];
  config: BatchConfig;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress: BatchProgress;
  createdAt: string;
}

class BulkEmailProcessor {
  async processBatch(batch: BatchJob): Promise<BatchResult> {
    const results: EmailResult[] = [];
    const batches = this.chunkArray(batch.emails, batch.config.batchSize);

    for (const chunk of batches) {
      const chunkResults = await this.sendWithRateLimit(chunk, batch.config);
      results.push(...chunkResults);
      batch.progress.sent += chunkResults.filter(r => r.status === 'sent').length;
      batch.progress.failed += chunkResults.filter(r => r.status === 'failed').length;
      await this.updateProgress(batch);
    }

    batch.status = 'completed';
    await this.storage.update(batch);
    return { batchId: batch.id, results, summary: this.summarize(results) };
  }

  private async sendWithRateLimit(emails: EmailPayload[], config: BatchConfig): Promise<EmailResult[]> {
    const results: EmailResult[] = [];
    const throttle = new TokenBucket({ capacity: config.ratePerSecond, refillRate: config.ratePerSecond, refillInterval: 1000 });

    const sendPromises = emails.map(async email => {
      await throttle.consume();
      for (let attempt = 1; attempt <= config.maxRetries; attempt++) {
        try {
          const result = await this.provider.send(email);
          return result;
        } catch (error) {
          if (attempt === config.maxRetries) return { status: 'failed', error: error.message };
          await new Promise(r => setTimeout(r, Math.pow(2, attempt) * 1000));
        }
      }
      return { status: 'failed', error: 'max retries' };
    });

    return Promise.all(sendPromises);
  }

  async segmentList(users: UserRecord[], criteria: SegmentCriteria): Promise<UserRecord[][]> {
    const segments: UserRecord[][] = [];
    for (const criterion of criteria.rules) {
      const segment = users.filter(u => this.matchesCriterion(u, criterion));
      segments.push(segment);
    }
    return segments;
  }

  private matchesCriterion(user: UserRecord, criterion: SegmentRule): boolean {
    switch (criterion.field) {
      case 'plan':
        return user.plan === criterion.value;
      case 'active_days':
        return user.daysSinceActive <= criterion.value;
      case 'email_engagement':
        return (user.emailOpens / user.emailSent) >= criterion.value;
      default:
        return false;
    }
  }

  private chunkArray<T>(array: T[], size: number): T[][] {
    const chunks: T[][] = [];
    for (let i = 0; i < array.length; i += size) {
      chunks.push(array.slice(i, i + size));
    }
    return chunks;
  }

  private summarize(results: EmailResult[]): BatchSummary {
    return {
      total: results.length,
      sent: results.filter(r => r.status === 'sent').length,
      failed: results.filter(r => r.status === 'failed').length,
      avgLatency: results.reduce((s, r) => s + (r.latency || 0), 0) / results.length,
    };
  }
}
```

## Integration Points

- **Email Queue**: Queue jobs for batch processing
- **Segment Service**: User segmentation for targeted sends
- **Progress Tracking**: Real-time batch progress via WebSocket

## Production Considerations

- **Provider Limits**: Stay within provider sending limits
- **Memory Management**: Stream large batches to avoid OOM
- **Error Recovery**: Resume failed batches from checkpoint
