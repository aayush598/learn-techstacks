# Section 02: Channel Abstraction Layer

## Overview

The channel abstraction layer provides a uniform interface for all notification delivery channels. Each channel implements a common `NotificationChannel` interface, allowing the notification bus to send messages through any channel without knowing channel-specific details. The adapter pattern wraps third-party APIs, and the channel registry manages available channels.

## Design Decisions

- **Interface-Driven**: All channels implement same `send` interface
- **Adapter Pattern**: Third-party APIs wrapped in adapters
- **Fallback Chains**: Channels configured in fallback order
- **Health Checking**: Each channel reports its health status

## Implementation Approach

```typescript
interface ChannelConfig {
  id: string;
  type: 'email' | 'slack' | 'sms' | 'push' | 'webhook' | 'in_app';
  enabled: boolean;
  priority: number;
  rateLimit: number;
  retryConfig: RetryConfig;
}

interface DeliveryResult {
  success: boolean;
  channelId: string;
  providerMessageId?: string;
  error?: string;
  latency: number;
}

interface NotificationChannel {
  send(payload: ChannelPayload): Promise<DeliveryResult>;
  validate(config: ChannelConfig): Promise<ValidationResult>;
  health(): Promise<HealthStatus>;
}

abstract class BaseChannel implements NotificationChannel {
  abstract send(payload: ChannelPayload): Promise<DeliveryResult>;
  abstract validate(config: ChannelConfig): Promise<ValidationResult>;
  abstract health(): Promise<HealthStatus>;

  protected async withRetry(fn: () => Promise<DeliveryResult>, config: RetryConfig): Promise<DeliveryResult> {
    for (let attempt = 1; attempt <= config.maxRetries; attempt++) {
      try {
        return await fn();
      } catch (error) {
        if (attempt === config.maxRetries) throw error;
        await this.delay(config.backoffMs * Math.pow(2, attempt - 1));
      }
    }
    throw new Error('Retry exhausted');
  }
}

class ChannelRegistry {
  private channels: Map<string, NotificationChannel> = new Map();

  register(type: string, channel: NotificationChannel): void {
    this.channels.set(type, channel);
  }

  getChannel(type: string): NotificationChannel {
    const channel = this.channels.get(type);
    if (!channel) throw new Error(`Unknown channel: ${type}`);
    return channel;
  }

  async sendWithFallback(payload: ChannelPayload, fallbackOrder: string[]): Promise<DeliveryResult> {
    for (const channelType of fallbackOrder) {
      const channel = this.getChannel(channelType);
      if (await this.isHealthy(channel)) {
        const result = await channel.send(payload);
        if (result.success) return result;
      }
    }
    throw new Error('All channels failed');
  }
}
```

## Integration Points

- **Channel Adapters**: Wrapper implementations for each provider
- **Registry Injection**: Channels registered at application startup
- **Config Management**: Channel configs stored in database

## Production Considerations

- **Channel Health**: Unhealthy channels are skipped in fallback
- **Rate Limiting**: Per-channel rate limits prevent provider throttling
- **Timeout**: Each channel send has a configurable timeout
