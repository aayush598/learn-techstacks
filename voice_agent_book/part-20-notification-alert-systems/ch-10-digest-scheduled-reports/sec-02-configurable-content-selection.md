# Section 02: Configurable Content Selection

## Overview

Users configure which content appears in their digests through preference settings. Content modules can be individually enabled/disabled, ordered, and configured. Smart selection algorithms use engagement history to prioritize relevant content.

## Architecture

```
Content Selection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[User Preferences] → [Content Selector] → [Filtered Content] → [Digest Builder]
       │                     │                      │                │
  Module on/off          Apply filters          Prioritized       Compose final
  Order preferences      Deduplication          by relevance      digest with
  Severity thresholds    Engagement-based       score + user      selected
  Channel selection      scoring                preference        content

Preference UI:
  ┌──────────────────────────────────────────────────────┐
  │ Digest Preferences                                     │
  │                                                        │
  │ Frequency: [Daily ✓] [Weekly] [Hourly]                │
  │ Delivery Time: 08:00 AM (America/New_York)            │
  │                                                        │
  │ Content Modules:                                        │
  │   ┌──────────────────────────────────────────────┐    │
  │   │ ☑ Critical Alerts    [Always include ✓]      │    │
  │   │    Min severity: High                         │    │
  │   │    Max items: 10                              │    │
  │   ├──────────────────────────────────────────────┤    │
  │   │ ☑ Warnings           [Always include ✓]      │    │
  │   │    Include resolved: No                       │    │
  │   ├──────────────────────────────────────────────┤    │
  │   │ ☐ Daily Stats        [Smart select ✓]        │    │
  │   │    Engagement-based ordering                  │    │
  │   ├──────────────────────────────────────────────┤    │
  │   │ ☐ Custom Reports     [Weekly only ✓]         │    │
  │   │    Include: agent performance, call metrics   │    │
  │   └──────────────────────────────────────────────┘    │
  │                                                        │
  │ [Save Preferences]                                     │
  └──────────────────────────────────────────────────────┘
```

## Design Decisions

- **Module-Based Architecture**: Users enable/disable entire content modules
- **Smart Selection**: ML-based relevance scoring for content ordering
- **Engagement Tracking**: Click/open rates influence content priority
- **Preference Inheritance**: Team-level defaults with per-user overrides

## Implementation Approach

```typescript
interface DigestPreferences {
  userId: string;
  tenantId: string;
  frequency: 'hourly' | 'daily' | 'weekly';
  preferredTime: string;
  timezone: string;
  modules: ModulePreference[];
  channelPreferences: ChannelPreference[];
  smartSelection: boolean;
  maxItemsPerModule: number;
}

interface ModulePreference {
  moduleId: string;
  enabled: boolean;
  order: number;
  mode: 'always' | 'smart' | 'conditional';
  config?: {
    minSeverity?: 'critical' | 'high' | 'medium' | 'low';
    maxItems?: number;
    includeResolved?: boolean;
    reportTypes?: string[];
  };
}

interface ChannelPreference {
  channel: 'email' | 'in_app' | 'slack' | 'sms';
  enabled: boolean;
  digestFormat: 'full' | 'summary' | 'minimal';
}

class ContentSelector {
  private engagementTracker: EngagementTracker;

  async selectContent(
    availableModules: DigestModuleContent[],
    preferences: DigestPreferences,
  ): Promise<DigestModuleContent[]> {
    const selected: DigestModuleContent[] = [];

    for (const pref of preferences.modules.sort((a, b) => a.order - b.order)) {
      if (!pref.enabled) continue;

      const module = availableModules.find(m => m.moduleId === pref.moduleId);
      if (!module) continue;

      switch (pref.mode) {
        case 'always':
          selected.push(this.applyConfigFilter(module, pref));
          break;
        case 'smart':
          const smartSelected = await this.smartSelect(module, pref, preferences.userId);
          if (smartSelected) selected.push(smartSelected);
          break;
        case 'conditional':
          if (this.checkCondition(module, pref)) {
            selected.push(this.applyConfigFilter(module, pref));
          }
          break;
      }
    }

    return selected;
  }

  private async smartSelect(
    module: DigestModuleContent,
    pref: ModulePreference,
    userId: string,
  ): Promise<DigestModuleContent | null> {
    const engagement = await this.engagementTracker.getUserEngagement(userId, module.moduleId);

    // Score each item by engagement relevance
    const scored = module.items.map(item => {
      const itemEngagement = engagement.items.find(e => e.id === item.id);
      const score = itemEngagement
        ? this.computeRelevanceScore(item, itemEngagement)
        : this.computeDefaultScore(item);

      return { ...item, _score: score };
    });

    // Sort by score and filter
    const sorted = scored
      .sort((a, b) => b._score - a._score)
      .slice(0, pref.config?.maxItems || 10)
      .map(({ _score, ...item }) => item);

    if (sorted.length === 0) return null;

    return {
      ...module,
      items: sorted,
    };
  }

  private computeRelevanceScore(
    item: DigestItem,
    engagement: ItemEngagement,
  ): number {
    let score = 0;

    // Recency
    const hoursAgo = (Date.now() - item.timestamp.getTime()) / 3600000;
    score += Math.max(0, 1 - hoursAgo / 24) * 0.3;

    // Severity boost
    const severityScore = { critical: 1, warning: 0.6, info: 0.3 };
    score += (severityScore[item.severity] || 0.3) * 0.3;

    // Engagement boost (if previously clicked similar items)
    if (engagement.clickCount > 0) {
      score += Math.min(engagement.clickCount / 10, 1) * 0.2;
    }

    // Similar item engagement
    if (engagement.similarItemClicks > 0) {
      score += Math.min(engagement.similarItemClicks / 5, 1) * 0.2;
    }

    return score;
  }

  private checkCondition(module: DigestModuleContent, pref: ModulePreference): boolean {
    if (module.items.length === 0) return false;
    if (pref.config?.minSeverity) {
      const severityOrder = ['critical', 'high', 'medium', 'low'];
      const minOrder = severityOrder.indexOf(pref.config.minSeverity);
      const hasItemsAboveMin = module.items.some(
        item => severityOrder.indexOf(item.severity) <= minOrder
      );
      if (!hasItemsAboveMin) return false;
    }
    return true;
  }

  private applyConfigFilter(
    module: DigestModuleContent,
    pref: ModulePreference,
  ): DigestModuleContent {
    let items = module.items;

    if (pref.config?.minSeverity) {
      const severityOrder = ['critical', 'high', 'medium', 'low'];
      const minOrder = severityOrder.indexOf(pref.config.minSeverity);
      items = items.filter(
        item => severityOrder.indexOf(item.severity) <= minOrder
      );
    }

    if (pref.config?.maxItems) {
      items = items.slice(0, pref.config.maxItems);
    }

    if (pref.config?.includeResolved === false) {
      items = items.filter(item => item.metadata?.status !== 'resolved');
    }

    return { ...module, items };
  }
}

class EngagementTracker {
  async trackOpen(userId: string, digestId: string, moduleId: string): Promise<void> {
    await this.db.insert('digest_engagement', {
      userId, digestId, moduleId,
      action: 'open',
      timestamp: new Date(),
    });
  }

  async trackClick(userId: string, digestId: string, itemId: string): Promise<void> {
    await this.db.insert('digest_engagement', {
      userId, digestId, itemId,
      action: 'click',
      timestamp: new Date(),
    });
  }

  async getUserEngagement(userId: string, moduleId: string): Promise<UserEngagement> {
    const recent = await this.db.find('digest_engagement', {
      userId,
      timestamp: { $gte: daysAgo(30) },
    });

    const moduleClicks = recent.filter(e => e.moduleId === moduleId && e.action === 'click');

    return {
      moduleId,
      clickCount: moduleClicks.length,
      similarItemClicks: recent.filter(e => e.action === 'click').length - moduleClicks.length,
      items: recent.map(e => ({ id: e.itemId, clicks: 1 })),
    };
  }
}
```

## Integration Points

- **User Preferences API**: CRUD for digest configuration
- **Engagement Analytics**: Click/open tracking for smart selection
- **Notification Bus**: Preference changes trigger digest regeneration

## Production Considerations

- **Default Preferences**: Sensible defaults for new users
- **Preference Migration**: Backward compatible preference schema changes
- **Smart Selection Cold Start**: Default ordering until sufficient engagement data
- **A/B Testing**: Test smart selection vs always-include mode

## Open-Source Tools

- **Zod**: Preference schema validation
- **Lodash**: Utility for preference merging and defaults
