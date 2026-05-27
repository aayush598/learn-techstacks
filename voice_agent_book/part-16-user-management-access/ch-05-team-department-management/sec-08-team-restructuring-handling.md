# Team Restructuring Handling

## Overview

Team restructuring involves moving users between teams, merging departments, reorganizing hierarchy, and transferring data ownership. These operations must preserve data integrity, maintain audit trails, and minimize disruption to ongoing operations.

## Restructuring Operations

```
Operations
├── Move User → New Team
│   ├── Reassign agent
│   ├── Transfer call history
│   ├── Notify managers
│   └── Update permissions
├── Merge Teams
│   ├── Combine members
│   ├── Merge resources/quotas
│   ├── Handle naming conflicts
│   └── Archive source team
├── Split Team
│   ├── Distribute members
│   ├── Split resources
│   ├── Create new teams
│   └── Set up new hierarchy
└── Reorganize Hierarchy
    ├── Change parent relationship
    ├── Update materialized paths
    ├── Recalculate permissions
    └── Update reporting lines
```

## Move User Between Teams

```typescript
interface TeamMoveRequest {
  userId: string;
  sourceTeamId: string;
  targetTeamId: string;
  reason: string;
  movedBy: string;
  keepHistory: boolean;        // Keep call history accessible
  transferResources: boolean;  // Move resource allocations
  notifyUsers: boolean;
  dateTime?: Date;             // Schedule for later
}

class TeamMoveService {
  async moveUser(request: TeamMoveRequest): Promise<void> {
    const user = await this.userService.getUser(request.userId);
    if (!user) throw new Error('User not found');

    const sourceTeam = await this.teamService.getTeam(request.sourceTeamId);
    const targetTeam = await this.teamService.getTeam(request.targetTeamId);
    if (!sourceTeam || !targetTeam) throw new Error('Team not found');

    const sourceDept = sourceTeam.departmentId;
    const targetDept = targetTeam.departmentId;

    // Validate move
    if (targetTeam.type === 'department') {
      throw new Error('Cannot move user directly to department');
    }

    // Start transaction
    const tx = await this.db.beginTransaction();

    try {
      // 1. Remove from source team
      await this.teamService.removeMember(request.sourceTeamId, request.userId);

      // 2. Add to target team
      await this.teamService.addMember(request.targetTeamId, request.userId, 'member');

      // 3. Update user's primary team
      await this.userService.updateUser(request.userId, { teamId: request.targetTeamId });

      // 4. Update department if different
      if (sourceDept !== targetDept) {
        await this.userService.updateUser(request.userId, { departmentId: targetDept });
      }

      // 5. Transfer resource allocations
      if (request.transferResources) {
        await this.transferResources(request.userId, request.sourceTeamId, request.targetTeamId);
      }

      // 6. Update permission assignments
      await this.updateTeamPermissions(request.userId, request.sourceTeamId, request.targetTeamId);

      // 7. Schedule call history migration
      if (!request.keepHistory) {
        await this.scheduleHistoryMigration(request.userId, request.sourceTeamId, request.targetTeamId);
      }

      await tx.commit();

      // 8. Notifications
      if (request.notifyUsers) {
        await this.notifyMove(request);
      }

      // 9. Audit log
      await this.auditLog.record({
        action: 'user.moved_team',
        actor: request.movedBy,
        target: { userId: request.userId },
        changes: {
          before: { teamId: request.sourceTeamId, departmentId: sourceDept },
          after: { teamId: request.targetTeamId, departmentId: targetDept },
        },
        metadata: { reason: request.reason },
      });
    } catch (error) {
      await tx.rollback();
      throw error;
    }
  }

  async scheduleBulkMove(
    moves: TeamMoveRequest[],
    scheduledDate: Date
  ): Promise<string> {
    const batchId = generateId('reorg');
    await this.db.insert('scheduled_team_moves', {
      batchId,
      moves,
      scheduledDate,
      status: 'scheduled',
      createdAt: new Date(),
    });

    await this.queue.schedule({
      type: 'process_team_moves',
      data: { batchId },
      at: scheduledDate,
    });

    return batchId;
  }

  private async transferResources(
    userId: string, sourceTeamId: string, targetTeamId: string
  ): Promise<void> {
    const userResources = await this.resourceManager.getUserAllocations(userId, sourceTeamId);
    for (const resource of userResources) {
      await this.resourceManager.releaseResource(sourceTeamId, resource.resourceType, resource.quantity);
      await this.resourceManager.allocateResource(targetTeamId, resource.resourceType, resource.quantity, 'system');
    }
  }
}
```

## Merge Teams

```typescript
interface TeamMergeRequest {
  sourceTeamIds: string[];
  targetTeamId: string;
  newName?: string;
  mergeStrategy: 'absorb' | 'combine';
  mergedBy: string;
}

class TeamMergeService {
  async mergeTeams(request: TeamMergeRequest): Promise<Team> {
    const targetTeam = await this.teamService.getTeam(request.targetTeamId);
    if (!targetTeam) throw new Error('Target team not found');

    const tx = await this.db.beginTransaction();

    try {
      for (const sourceId of request.sourceTeamIds) {
        const sourceTeam = await this.teamService.getTeam(sourceId);
        if (!sourceTeam) continue;

        // Move all members
        const members = await this.teamService.getTeamMembers(sourceId);
        for (const member of members) {
          await this.teamService.addMember(targetTeam.id, member.userId, member.role);
        }

        // Merge quotas
        await this.mergeQuotas(sourceId, targetTeam.id);

        // Merge analytics data
        await this.mergeAnalytics(sourceId, targetTeam.id);

        // Reassign resources
        const resources = await this.db.find('team_resources', { teamId: sourceId });
        for (const resource of resources) {
          resource.teamId = targetTeam.id;
          await this.db.update('team_resources', { id: resource.id }, resource);
        }

        // Deactivate source team
        await this.db.update('teams', { id: sourceId }, {
          isActive: false,
          mergedInto: targetTeam.id,
          mergedAt: new Date(),
        });
      }

      // Update team name if requested
      if (request.newName) {
        await this.db.update('teams', { id: targetTeam.id }, { name: request.newName });
      }

      // Update audit trail
      await this.auditLog.record({
        action: 'team.merge',
        actor: request.mergedBy,
        target: { teamId: targetTeam.id },
        changes: {
          before: { sourceCount: request.sourceTeamIds.length },
          after: { sourceCount: 0 },
        },
      });

      await tx.commit();
      return this.teamService.getTeam(targetTeam.id) as Promise<Team>;
    } catch (error) {
      await tx.rollback();
      throw error;
    }
  }
}
```

## Data Ownership Transfer

```typescript
class DataOwnershipTransfer {
  async transferOwnership(
    resourceType: string,
    resourceId: string,
    fromTeamId: string,
    toTeamId: string
  ): Promise<void> {
    const resource = await this.resourceService.getResource(resourceType, resourceId);
    if (!resource) throw new Error('Resource not found');

    resource.ownerTeamId = toTeamId;
    resource.transferredAt = new Date();
    resource.transferredBy = 'system';

    await this.db.update(resourceType, { id: resourceId }, resource);

    // Reset related permissions
    await this.db.update('resource_permissions', { resourceId }, {
      teamId: toTeamId,
      updatedAt: new Date(),
    });
  }

  async reindexOwnership(
    teamId: string,
    newTeamId: string
  ): Promise<TransferSummary> {
    // Transfer all resources owned by this team
    const resources = await this.resourceService.getTeamResources(teamId);
    let transferred = 0;

    for (const resource of resources) {
      await this.transferOwnership(
        resource.type, resource.id, teamId, newTeamId
      );
      transferred++;
    }

    return { transferred, teamId, newTeamId };
  }
}
```

## Open-Source Tools

- **BullMQ** (MIT) — Queue for scheduled moves and async restructuring tasks
- **Prisma** (MIT) — Transaction support for multi-table restructuring operations

## Production Considerations

- Use database transactions for all restructuring operations to ensure atomicity
- Schedule large moves during maintenance windows to avoid data inconsistency
- Validate all operations against the team hierarchy depth limit
- Provide dry-run mode to preview restructuring outcomes before execution
- Maintain a restructuring history viewable in admin dashboard
- Allow rollback of restructuring within 24 hours (point-in-time recovery)
- Communicate all team changes to affected users via email and in-app notification
- Update permission evaluation cache after restructuring to reflect new hierarchy
