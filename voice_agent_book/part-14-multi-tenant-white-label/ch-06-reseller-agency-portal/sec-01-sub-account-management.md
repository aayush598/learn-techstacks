# Section 01: Sub-Account Management

## Overview

Sub-account management enables resellers to create and manage multiple tenant accounts under their hierarchy. Each sub-account is a fully functional tenant with its own agents, calls, configurations, and users, but is owned and managed by the reseller parent. The parent can view aggregated usage, manage billing, apply branding, and provide support across all sub-accounts.

The sub-account hierarchy supports multiple levels: platform (root) → master reseller → sub-reseller → tenant. Each level has appropriate management capabilities and restrictions. A master reseller can create sub-resellers, set their discount rates, and monitor their performance. Sub-resellers can create end-customer tenants and apply their own markup.

For a voice agent platform, sub-account management integrates with white-label branding (each sub-account can have its own branding or inherit from parent), billing (consolidated invoicing), and analytics (roll-up reporting). The reseller dashboard provides a multi-tenant view with aggregate metrics.

## Implementation Approach

```typescript
interface SubAccount {
  id: string;
  parentId: string;
  name: string;
  tier: string;
  status: 'active' | 'suspended' | 'trial';
  branding: 'inherited' | 'custom';
  settings: SubAccountSettings;
  createdAt: Date;
}

class SubAccountManager {
  async createSubAccount(parentId: string, config: CreateSubAccountConfig): Promise<SubAccount> {
    // Validate reseller can create more accounts (quota check)
    await this.checkAccountQuota(parentId);

    const tenantId = crypto.randomUUID();

    // Create tenant
    await this.provisioningPipeline.startProvisioning({
      tenantId,
      companyName: config.name,
      adminEmail: config.adminEmail,
      tier: config.tier || 'starter',
      parentTenantId: parentId,
      brandingInheritance: config.inheritBranding ?? true,
    });

    // Create parent relationship
    await this.db.query(`
      INSERT INTO tenant_hierarchy (parent_id, child_id, relationship_type, created_at)
      VALUES ($1, $2, 'reseller', NOW())
    `, [parentId, tenantId]);

    return { id: tenantId, parentId, name: config.name, tier: config.tier, status: 'active' };
  }

  async getHierarchyTree(tenantId: string): Promise<TenantTreeNode> {
    const children = await this.db.query(`
      WITH RECURSIVE tenant_tree AS (
        SELECT id, parent_id, name, tier, 0 as depth
        FROM tenants WHERE id = $1
        UNION ALL
        SELECT t.id, t.parent_id, t.name, t.tier, tt.depth + 1
        FROM tenants t
        JOIN tenant_hierarchy h ON t.id = h.child_id
        JOIN tenant_tree tt ON h.parent_id = tt.id
      )
      SELECT * FROM tenant_tree ORDER BY depth
    `, [tenantId]);

    return this.buildTree(children.rows, tenantId);
  }

  async getAggregatedUsage(parentId: string, period: TimeRange): Promise<AggregatedMetrics> {
    const children = await this.getSubAccountIds(parentId);

    const result = await this.analyticsDb.query(`
      SELECT 
        COUNT(*) as total_calls,
        SUM(duration_seconds) as total_duration,
        COUNT(DISTINCT agent_id) as active_agents,
        AVG(duration_seconds) as avg_duration
      FROM calls
      WHERE tenant_id = ANY($1)
        AND created_at BETWEEN $2 AND $3
    `, [children, period.start, period.end]);

    return result.rows[0];
  }

  async transferSubAccount(accountId: string, newParentId: string): Promise<void> {
    // Update hierarchy
    await this.db.query(
      `UPDATE tenant_hierarchy SET parent_id = $1 WHERE child_id = $2`,
      [newParentId, accountId]
    );

    // Invalidate caches
    await this.cache.del(`hierarchy:${accountId}`);
    await this.cache.del(`hierarchy:${newParentId}`);
  }
}
```

## Open-Source Tools

- **PostgreSQL Recursive CTE** — Hierarchy traversal for multi-level reseller trees
- **Redis** — Cache hierarchy data for fast lookups
- **BullMQ** — Async sub-account provisioning
- **React DnD** — Drag-and-drop hierarchy management UI
- **d3.js** — Interactive hierarchy visualization

## Production Considerations

- **Hierarchy Depth Limits:** Restrict hierarchy depth (e.g., max 4 levels: platform → master reseller → sub-reseller → tenant). Deep hierarchies increase management complexity.
- **Quota Management:** Each reseller tier has a maximum number of sub-accounts they can create. Auto-approve quota increases for good standing resellers.
- **Account Isolation:** Sub-accounts must be isolated from each other. A reseller should see aggregated data but not individual call content unless explicitly granted.
- **Parent-Child Billing:** Support consolidated billing (parent pays for all sub-accounts) and individual billing (each sub-account pays separately). This is a key reseller feature.
- **Self-Service Upgrades:** Allow resellers to upgrade/downgrade sub-account plans within their authorized range. Parent sets the max tier a sub-reseller can assign.
