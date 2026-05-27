# Section 07: Cross-Tenant Data Sharing Patterns

## Overview

In a multi-tenant voice agent platform, not all data belongs strictly to individual tenants. Certain data must be shared across tenants: platform-wide reference data (country codes, language models), shared AI resources (base LLM models, voice libraries), marketplace items (agent templates, integration connectors), and aggregated analytics. Cross-tenant data sharing must be carefully designed to maintain isolation where required while enabling collaboration and platform-level functionality.

The fundamental principle is that operational data (calls, transcripts, agent configurations) belongs to individual tenants and must remain isolated, while platform data (resources provided by the SaaS vendor) can be shared read-only. Additionally, tenants may opt to share certain data—such as agent templates or campaign configurations—through a marketplace or community library. This creates a spectrum of data visibility: private (tenant-only), shared-within-tenant-hierarchy (parent-child for resellers), platform-shared (all tenants), and public (marketplace).

For a voice agent platform with a reseller model (Part 14, Ch 06), cross-tenant data sharing becomes more complex. A reseller parent needs visibility into their sub-tenants' aggregated usage and performance metrics without seeing individual call content. Similarly, enterprise customers with multiple departments may need some cross-department visibility while maintaining division-level access controls.

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

```typescript
// Data visibility model
enum DataVisibility {
  PRIVATE = 'private',         // Only within tenant
  HIERARCHY = 'hierarchy',     // Tenant + parent resellers
  PLATFORM = 'platform',       // All tenants (read-only)
  MARKETPLACE = 'marketplace', // Public
}

// Shared data access patterns
class CrossTenantDataManager {
  async getAgentTemplate(templateId: string, requestingTenant: Tenant): Promise<AgentTemplate> {
    const template = await this.getTemplate(templateId);
    
    switch (template.visibility) {
      case DataVisibility.PRIVATE:
        if (template.tenantId !== requestingTenant.id) {
          throw new ForbiddenError('Template not accessible');
        }
        return template;
        
      case DataVisibility.HIERARCHY:
        const hierarchy = await this.resellerService.getTenantHierarchy(requestingTenant.id);
        if (!hierarchy.includes(template.tenantId)) {
          throw new ForbiddenError('Template not in your hierarchy');
        }
        return template;
        
      case DataVisibility.PLATFORM:
      case DataVisibility.MARKETPLACE:
        return template; // Publicly accessible
    }
  }

  async shareToMarketplace(
    template: AgentTemplate, 
    ownerTenant: Tenant,
    sharingConfig: SharingConfig
  ): Promise<MarketplaceListing> {
    // Verify ownership
    if (template.tenantId !== ownerTenant.id) {
      throw new ForbiddenError('Cannot share template you do not own');
    }

    // Create a copy with marketing visibility
    const listing = await this.createMarketplaceListing({
      originalTemplateId: template.id,
      name: template.name,
      description: sharingConfig.description,
      category: sharingConfig.category,
      screenshotUrls: sharingConfig.screenshots,
      pricing: sharingConfig.pricing,
      visibility: DataVisibility.MARKETPLACE,
      ownerTenantId: ownerTenant.id,
    });

    // Track analytics for sharing
    await this.analyticsService.track({
      event: 'marketplace.published',
      tenantId: ownerTenant.id,
      templateId: template.id,
    });

    return listing;
  }

  async getAnonymizedPlatformMetrics(
    metricType: string,
    timeRange: TimeRange
  ): Promise<AggregatedMetric> {
    // Query across all tenants with anonymization
    const rawData = await this.analyticsDb.query(`
      SELECT 
        DATE_TRUNC('hour', timestamp) as hour,
        COUNT(*) as total_calls,
        AVG(duration_seconds) as avg_duration,
        COUNT(DISTINCT tenant_id) as active_tenants
      FROM calls
      WHERE timestamp >= $1 AND timestamp <= $2
        AND tenant_id IN (SELECT id FROM tenants WHERE tier != 'enterprise')
      GROUP BY DATE_TRUNC('hour', timestamp)
    `, [timeRange.start, timeRange.end]);

    // Apply differential privacy - add Laplacian noise
    const epsilon = 0.1; // Privacy budget
    return {
      datapoints: rawData.rows.map(row => ({
        ...row,
        total_calls: this.addLaplacianNoise(row.total_calls, epsilon),
        avg_duration: this.addLaplacianNoise(row.avg_duration, epsilon),
      })),
      metadata: {
        anonymized: true,
        epsilon,
        tenantCount: rawData.rows[0]?.active_tenants || 0,
      },
    };
  }

  private addLaplacianNoise(value: number, epsilon: number): number {
    const scale = 1 / epsilon;
    const noise = this.sampleLaplacian(0, scale);
    return Math.max(0, Math.round(value + noise));
  }

  private sampleLaplacian(mean: number, scale: number): number {
    const u = Math.random() - 0.5;
    return mean - scale * Math.sign(u) * Math.log(1 - 2 * Math.abs(u));
  }
}

// Database view for cross-tenant analytics
const CROSS_TENANT_VIEW = `
CREATE VIEW platform.campaign_performance AS
SELECT 
  c.tenant_id,
  DATE_TRUNC('day', c.created_at) as day,
  COUNT(*) FILTER (WHERE c.status = 'completed') as completed,
  COUNT(*) FILTER (WHERE c.status = 'failed') as failed,
  AVG(c.duration) as avg_duration,
  AVG(c.sentiment_score) as avg_sentiment
FROM calls c
JOIN tenants t ON c.tenant_id = t.id
WHERE t.analytics_opt_in = true
GROUP BY c.tenant_id, DATE_TRUNC('day', c.created_at)
`;
```

## Integration Points

- **Marketplace (Part 22):** Cross-tenant sharing is the foundation of template and integration marketplace
- **Reseller Portal (Ch 06):** Hierarchy-based sharing enables reseller parent-child data visibility
- **Analytics & Reporting (Part 11):** Aggregated cross-tenant analytics with anonymization
- **Knowledge Base (Part 13):** Shared knowledge base articles vs tenant-specific knowledge
- **Integration Connectors:** Shared connector configurations vs tenant-specific credentials

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **Data Classification Labels:** Implement a data classification system that marks every data element as private, shared, or public. This drives access control decisions.
- **Sharing Audits:** Log every cross-tenant data access. Tenants should be able to see who accessed their shared data and when.
- **Revocation Support:** If a tenant removes a template from the marketplace, existing installs should be handled carefully (graceful deprecation vs immediate removal).
- **Anonymization Strength:** `epsilon=0.1` provides strong privacy guarantees but may distort metrics for small sample sizes. Consider adaptive epsilon based on the number of contributing tenants.
- **Hierarchy Depth Limits:** Restrict reseller hierarchy depth (e.g., max 3 levels) to prevent overly complex sharing rules.
- **Quota Sharing:** Some plans may allow resource pooling across tenants in the same hierarchy (e.g., shared minute pools). Implement this carefully with usage tracking.
- **Data Leakage Prevention:** Regularly audit cross-tenant views and queries. Automated penetration testing should verify that private data cannot be inferred from aggregated views.
