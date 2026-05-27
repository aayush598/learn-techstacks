# Section 06: Message Queue Integration

## Overview

BullMQ provides reliable message queuing for notification delivery. Notifications are enqueued as jobs with priority, delay, and retry settings. Worker processes consume jobs and deliver through the appropriate channel. The queue system handles backpressure, rate limiting, and scheduled delivery.

## Implementation Approach

```typescript
import { Queue, Worker, Job } from 'bullmq';

interface NotificationJob {
  notificationId: string;
  channel: string;
  payload: ChannelPayload;
  tenantId: string;
  priority: number;
  delay?: number;
}

class NotificationQueueManager {
  private queue: Queue;
  private workers: Map<string, Worker> = new Map();

  constructor(connection: RedisConnection) {
    this.queue = new Queue('notifications', {
      connection,
      defaultJobOptions: {
        attempts: 3,
        backoff: { type: 'exponential', delay: 2000 },
        removeOnComplete: { age: 3600 * 24 },
        removeOnFail: { age: 3600 * 24 * 7 },
      },
    });
  }

  async enqueue(notification: NotificationJob): Promise<Job> {
    return this.queue.add(
      `notification:${notification.channel}`,
      notification,
      {
        priority: notification.priority,
        delay: notification.delay,
        jobId: notification.notificationId,
      }
    );
  }

  async enqueueBulk(notifications: NotificationJob[]): Promise<Job[]> {
    const jobs = notifications.map(n => ({
      name: `notification:${n.channel}`,
      data: n,
      opts: { jobId: n.notificationId, priority: n.priority },
    }));
    return this.queue.addBulk(jobs);
  }

  registerWorker(channel: string, processor: (job: Job) => Promise<void>): Worker {
    const worker = new Worker(
      'notifications',
      async job => {
        if (job.data.channel === channel) {
          await processor(job);
        }
      },
      {
        connection: this.queue.opts.connection,
        concurrency: 10,
        limiter: { max: 50, duration: 1000 }, // Rate limit per second
      }
    );

    worker.on('failed', (job, error) => {
      console.error(`Job ${job?.id} failed:`, error);
    });

    this.workers.set(channel, worker);
    return worker;
  }

  async getQueueStatus(): Promise<QueueStatus> {
    const [waiting, active, completed, failed, delayed] = await Promise.all([
      this.queue.getWaitingCount(),
      this.queue.getActiveCount(),
      this.queue.getCompletedCount(),
      this.queue.getFailedCount(),
      this.queue.getDelayedCount(),
    ]);
    return { waiting, active, completed, failed, delayed };
  }
}
```

## Integration Points

- **Redis Backend**: BullMQ requires Redis for job storage
- **Worker Scaling**: Multiple workers can consume from same queue
- **Job Events**: Track job lifecycle for monitoring

## Production Considerations

- **Redis High Availability**: Redis Sentinel or Cluster for production
- **Job Retention**: Clean up completed jobs to prevent memory growth
- **Rate Limiting**: Per-channel rate limits prevent provider throttling
