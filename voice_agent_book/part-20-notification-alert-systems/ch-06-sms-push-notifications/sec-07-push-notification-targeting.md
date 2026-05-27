# Section 07: Push Notification Targeting

## Overview

Push notification targeting delivers personalized notifications to specific user segments. Targeting criteria include user behavior, preferences, location, device type, and engagement history. A/B testing compares notification variants. Personalization uses user attributes for dynamic content.

## Implementation Approach

```typescript
interface TargetingCriteria {
  segments: SegmentDefinition[];
  conditions: TargetingCondition[];
  exclusionSegments: string[];
  priority: number;
}

interface SegmentDefinition {
  id: string;
  name: string;
  rules: SegmentRule[];
  source: 'static' | 'dynamic' | 'computed';
}

interface SegmentRule {
  field: string;
  operator: 'eq' | 'neq' | 'gt' | 'lt' | 'in' | 'contains' | 'between';
  value: unknown;
}

class PushTargetingEngine {
  async getTargetUsers(criteria: TargetingCriteria): Promise<string[]> {
    let users: string[] = [];

    for (const segment of criteria.segments) {
      const segmentUsers = await this.evaluateSegment(segment);
      users = [...new Set([...users, ...segmentUsers])];
    }

    // Apply conditions
    for (const condition of criteria.conditions) {
      users = users.filter(u => this.evaluateCondition(u, condition));
    }

    // Exclude segments
    for (const excludeId of criteria.exclusionSegments) {
      const excludeSegment = await this.segmentStore.get(excludeId);
      const excludeUsers = await this.evaluateSegment(excludeSegment);
      users = users.filter(u => !excludeUsers.includes(u));
    }

    return users;
  }

  private async evaluateSegment(segment: SegmentDefinition): Promise<string[]> {
    switch (segment.source) {
      case 'static':
        return this.staticSegmentStore.getUsers(segment.id);
      case 'dynamic':
        return this.evaluateDynamicSegment(segment);
      case 'computed':
        return this.evaluateComputedSegment(segment);
      default:
        return [];
    }
  }

  private async evaluateDynamicSegment(segment: SegmentDefinition): Promise<string[]> {
    const conditions = segment.rules.map(r => this.buildCondition(r));
    return this.userStore.query({ $and: conditions });
  }

  // A/B Testing
  async runABTest(test: ABTestConfig): Promise<ABTestResult> {
    const users = await this.getTargetUsers(test.targeting);
    const variants = this.assignVariants(users, test.variants);
    const results: VariantResult[] = [];

    for (const [variantId, variantUsers] of Object.entries(variants)) {
      const variant = test.variants.find(v => v.id === variantId)!;
      const sentAt = new Date().toISOString();

      // Send notifications
      for (const user of variantUsers) {
        await this.sendPush(user, variant.payload);
      }

      // Track results after test duration
      setTimeout(async () => {
        const engagement = await this.measureEngagement(variantUsers, test.metrics);
        results.push({ variantId, usersCount: variantUsers.length, engagement });
      }, test.duration * 1000);
    }

    return { testId: test.id, variants: results, startTime: new Date().toISOString() };
  }

  private assignVariants(users: string[], variants: ABVariant[]): Record<string, string[]> {
    const assignment: Record<string, string[]> = {};
    for (const variant of variants) {
      assignment[variant.id] = [];
    }

    users.forEach((user, index) => {
      const variantIndex = index % variants.length;
      assignment[variants[variantIndex].id].push(user);
    });

    return assignment;
  }

  private async measureEngagement(users: string[], metrics: string[]): Promise<EngagementMetrics> {
    const results: EngagementMetrics = {};
    for (const metric of metrics) {
      results[metric] = await this.analyticsService.getMetric(metric, users);
    }
    return results;
  }
}
```

## Integration Points

- **User Segment Store**: Pre-computed and dynamic segments
- **Analytics Service**: Engagement measurement
- **A/B Test Framework**: Variant assignment and result analysis

## Production Considerations

- **Segment Freshness**: Refresh dynamic segments periodically
- **A/B Test Size**: Ensure statistical significance
- **Personalization Privacy**: Respect user privacy in targeting
