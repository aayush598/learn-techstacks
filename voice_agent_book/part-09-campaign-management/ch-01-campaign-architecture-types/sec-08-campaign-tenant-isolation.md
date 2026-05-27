# Section 08: Campaign Tenant Isolation

## Overview

In a multi-tenant SaaS deployment, campaign data belonging to different tenants (customers) must be isolated to prevent cross-tenant data leaks, ensure regulatory compliance, and maintain fair resource allocation. Tenant isolation in campaign management spans database partitioning, access control, resource quotas, and operational boundaries. Each tenant's campaigns, contact lists, configurations, and analytics must be completely invisible to other tenants.

Tenant isolation strategies range from shared-everything (row-level security) to shared-nothing (dedicated database per tenant). The choice depends on tenant count, data volume, compliance requirements, and operational complexity. The campaign system must support tenant-aware data access at every layer — API, database, cache, queue, and storage.

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

```
class TenantContext {
  constructor(tenantId) {
    this.tenantId = tenantId;
  }

  static fromRequest(request) {
    const token = request.headers.authorization;
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    return new TenantContext(decoded.tenant_id);
  }
}

class TenantAwareCampaignService {
  async getCampaign(campaignId, tenantContext) {
    // RLS handles this automatically if connection is configured
    return prisma.campaign.findFirst({
      where: {
        id: campaignId,
        tenant_id: tenantContext.tenantId // Explicit filter + RLS
      }
    });
  }

  async createCampaign(data, tenantContext) {
    await this.validateQuota(tenantContext);
    
    const campaign = await prisma.campaign.create({
      data: {
        ...data,
        tenant_id: tenantContext.tenantId
      }
    });

    // Tenant-prefixed Redis key
    await redis.set(
      `tenant:${tenantContext.tenantId}:campaign:${campaign.id}`,
      JSON.stringify(campaign)
    );

    return campaign;
  }

  async validateQuota(tenantContext) {
    const { count } = await prisma.campaign.count({
      where: { tenant_id: tenantContext.tenantId }
    });
    
    const quota = await this.getTenantQuota(tenantContext);
    if (count >= quota.maxActiveCampaigns) {
      throw new QuotaExceededError('active_campaigns', quota);
    }
  }
}
```

## Integration Points

- **Auth Service (Part 16):** JWT contains tenant_id for request authentication
- **API Gateway:** Routes requests and injects tenant context into headers
- **Database Layer:** RLS policies configured for every campaign-related table
- **Object Storage (Part 12, Ch 04):** Tenant-prefixed S3 paths for recordings and exports
- **Queue System:** Tenant-specific queue naming or namespace isolation
- **Analytics (Part 11):** Tenant-filtered analytics views and dashboards

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- RLS can impact query performance — monitor for query plan changes as tenant data grows
- Test tenant isolation thoroughly — penetration test for cross-tenant data access vulnerabilities
- Tenant resource quotas should be adjustable without campaign restart
- Implement a tenant activity de-escalation mechanism — idle tenants should not consume resources
- Cache tenant context at the API gateway level to avoid JWT decoding on every request
- Storage lifecycle policies should be tenant-aware — different tenants may have different retention requirements
- Cross-tenant analytics should use anonymized/aggregated data only, never raw contact or campaign data
- Bulk operations (like all-campaigns pause) should iterate tenants with individual tenant context, never with a global query
- Tenant data export/deletion must support complete purging without affecting other tenants
- Monitor for noisy neighbor tenants that consume disproportionate shared resources
