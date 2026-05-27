# Team-Level Resource Management

## Overview

Team-level resource management controls how agents, phone numbers, call credits, and other resources are allocated and shared across teams. It enables quota management, resource pooling, and ensures fair distribution across organizational units.

## Resource Types

```typescript
enum ResourceType {
  AGENT_SLOTS = 'agent_slots',
  PHONE_NUMBERS = 'phone_numbers',
  CALL_CREDITS = 'call_credits',
  CONCURRENT_CALLS = 'concurrent_calls',
  STORAGE = 'storage',
  API_CALLS = 'api_calls',
  AI_TOKENS = 'ai_tokens',
}

interface TeamResourceQuota {
  id: string;
  teamId: string;
  resourceType: ResourceType;
  quota: number;               // Maximum allowed
  used: number;                // Currently used
  reserved: number;            // Reserved but not yet used
  unit: string;
  resetPeriod: 'daily' | 'weekly' | 'monthly' | 'never';
  lastResetAt: Date;
  overageAllowed: boolean;
  overageRate?: number;        // Cost per unit over quota
}
```

## Resource Allocation

```typescript
class TeamResourceManager {
  async allocateResource(
    teamId: string,
    resourceType: ResourceType,
    quantity: number,
    userId: string
  ): Promise<AllocationResult> {
    const quota = await this.getTeamQuota(teamId, resourceType);
    if (!quota) throw new Error('No quota configured for this resource');

    const available = quota.quota - quota.used - quota.reserved;
    if (quantity > available) {
      // Check parent team for overflow
      const team = await this.teamService.getTeam(teamId);
      if (team?.parentId) {
        return this.borrowFromParent(team.parentId, resourceType, quantity - available, teamId);
      }

      if (quota.overageAllowed) {
        // Allow overage with tracking
        await this.trackOverage(teamId, resourceType, quantity - available);
      } else {
        return { success: false, reason: 'quota_exceeded', available };
      }
    }

    quota.used += quantity;
    await this.updateQuota(quota);

    await this.auditLog.record({
      action: 'resource.allocated',
      actor: userId,
      target: { teamId, resourceType },
      changes: { before: { used: quota.used - quantity }, after: { used: quota.used } },
    });

    return { success: true, remaining: quota.quota - quota.used };
  }

  async releaseResource(
    teamId: string,
    resourceType: ResourceType,
    quantity: number
  ): Promise<void> {
    const quota = await this.getTeamQuota(teamId, resourceType);
    if (!quota) return;

    quota.used = Math.max(0, quota.used - quantity);
    await this.updateQuota(quota);
  }

  async borrowFromParent(
    parentTeamId: string,
    resourceType: ResourceType,
    quantity: number,
    childTeamId: string
  ): Promise<AllocationResult> {
    const parentQuota = await this.getTeamQuota(parentTeamId, resourceType);
    const parentAvailable = parentQuota.quota - parentQuota.used - parentQuota.reserved;

    if (quantity > parentAvailable) {
      return { success: false, reason: 'parent_quota_exceeded', available: parentAvailable + (parentQuota.quota - parentQuota.used - parentQuota.reserved) };
    }

    // Borrow from parent
    parentQuota.reserved += quantity;
    await this.updateQuota(parentQuota);

    // Create borrow record
    await this.db.insert('resource_borrows', {
      childTeamId,
      parentTeamId,
      resourceType,
      quantity,
      borrowedAt: new Date(),
      status: 'active',
    });

    return { success: true, remaining: parentAvailable - quantity, borrowed: true };
  }

  async resetQuotas(teamId: string): Promise<void> {
    const quotas = await this.db.find('team_resource_quotas', { teamId });
    for (const quota of quotas) {
      if (quota.resetPeriod !== 'never') {
        quota.used = 0;
        quota.lastResetAt = new Date();
        await this.updateQuota(quota);
      }
    }
  }

  async getTeamUtilization(teamId: string): Promise<TeamResourceUtilization> {
    const quotas = await this.db.find('team_resource_quotas', { teamId });
    const parentBorrows = await this.db.find('resource_borrows', { childTeamId: teamId, status: 'active' });

    return {
      teamId,
      resources: quotas.map(q => ({
        resourceType: q.resourceType,
        quota: q.quota,
        used: q.used,
        available: q.quota - q.used - q.reserved,
        utilization: Math.round((q.used / q.quota) * 100),
      })),
      borrowedFromParent: parentBorrows.map(b => ({
        resourceType: b.resourceType,
        quantity: b.quantity,
      })),
    };
  }
}

interface AllocationResult {
  success: boolean;
  reason?: string;
  available?: number;
  remaining?: number;
  borrowed?: boolean;
}
```

## Resource Pool Configuration

```typescript
interface PoolConfig {
  teamId: string;
  poolingStrategy: 'dedicated' | 'shared_pool' | 'hierarchical';
  parentPoolId?: string;
  burstCapacity?: number;       // Temporary over-quota allowance
  priority: number;             // Higher = gets resources first
}

class ResourcePoolService {
  async configurePool(teamId: string, config: PoolConfig): Promise<void> {
    const existing = await this.db.findOne('resource_pools', { teamId });
    if (existing) {
      await this.db.update('resource_pools', { teamId }, config);
    } else {
      await this.db.insert('resource_pools', { ...config, createdAt: new Date() });
    }
  }

  async getAvailableFromPool(
    resourceType: ResourceType,
    excludeTeamId?: string
  ): Promise<number> {
    const pools = await this.db.find('resource_pools', { poolingStrategy: 'shared_pool' });

    let totalAvailable = 0;
    for (const pool of pools) {
      if (pool.teamId === excludeTeamId) continue;
      const quota = await this.teamResourceManager.getTeamQuota(pool.teamId, resourceType);
      if (quota) {
        totalAvailable += quota.quota - quota.used - quota.reserved;
      }
    }

    return totalAvailable;
  }

  async redistributeResources(teamId: string, resourceType: ResourceType): Promise<void> {
    // Rebalance resources across sibling teams
    const team = await this.teamService.getTeam(teamId);
    if (!team?.parentId) return;

    const siblings = await this.teamService.getChildTeams(team.parentId);
    const totalQuota = await this.calculateTotalQuota(siblings, resourceType);
    const fairShare = Math.floor(totalQuota / siblings.length);

    for (const sibling of siblings) {
      const quota = await this.teamResourceManager.getTeamQuota(sibling.id, resourceType);
      if (quota && quota.quota !== fairShare) {
        quota.quota = Math.max(quota.used, fairShare);
        await this.teamResourceManager.updateQuota(quota);
      }
    }
  }
}
```

## Agent Assignment to Teams

```typescript
class AgentAssignmentService {
  async assignAgentToTeam(agentId: string, teamId: string): Promise<void> {
    const team = await this.teamService.getTeam(teamId);
    if (!team) throw new Error('Team not found');

    // Check agent slot availability
    const allocation = await this.teamResourceManager.allocateResource(
      teamId, ResourceType.AGENT_SLOTS, 1, 'system'
    );
    if (!allocation.success) {
      throw new Error(`No agent slots available in team: ${allocation.reason}`);
    }

    // Assign agent
    await this.db.insert('team_agents', {
      agentId,
      teamId,
      assignedAt: new Date(),
      assignedBy: 'system',
    });

    // Update team metadata
    await this.db.increment('teams', { id: teamId }, 'agentCount');
  }

  async unassignAgentFromTeam(agentId: string, teamId: string): Promise<void> {
    await this.db.delete('team_agents', { agentId, teamId });
    await this.teamResourceManager.releaseResource(teamId, ResourceType.AGENT_SLOTS, 1);
    await this.db.decrement('teams', { id: teamId }, 'agentCount');
  }
}
```

## Open-Source Tools

- **BullMQ** (MIT) — Queue for resource allocation and deallocation
- **Redis** — Resource counter storage with atomic operations

## Production Considerations

- Use atomic Redis counters for resource allocation to prevent race conditions
- Implement resource borrowing time limits (auto-return after 24h)
- Send team lead notifications at 80%, 90%, and 100% quota usage
- Provide per-resource dashboards for team leads to monitor consumption
- Allow tenants to set default quotas per team level (department/team/subteam)
- Audit all resource allocation changes for billing and compliance
- Support temporary quota increases (burst) for campaigns and events
