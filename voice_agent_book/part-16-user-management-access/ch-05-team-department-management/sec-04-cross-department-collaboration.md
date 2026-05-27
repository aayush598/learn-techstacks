# Cross-Department Collaboration

## Overview

Cross-department collaboration enables teams from different departments to share campaigns, access data across organizational boundaries, and collaborate on shared projects while maintaining proper access controls and audit trails.

## Permission Boundary Extension

```typescript
interface CrossDepartmentPermission {
  id: string;
  sourceTeamId: string;
  targetTeamId: string;
  permissions: CrossDeptPermission[];
  grantedBy: string;
  grantedAt: Date;
  expiresAt?: Date;
  reason: string;
  status: 'active' | 'expired' | 'revoked';
}

interface CrossDeptPermission {
  resourceType: string;
  actions: string[];
  scope: 'read_only' | 'read_write' | 'full';
}

class CrossDepartmentService {
  async grantCrossDeptAccess(
    sourceTeamId: string,
    targetTeamId: string,
    permissions: CrossDeptPermission[],
    grantedBy: string,
    reason: string,
    expiresAt?: Date
  ): Promise<CrossDepartmentPermission> {
    // Validate teams belong to different departments
    const sourceTeam = await this.teamService.getTeam(sourceTeamId);
    const targetTeam = await this.teamService.getTeam(targetTeamId);

    if (!sourceTeam || !targetTeam) throw new Error('Team not found');
    if (sourceTeam.departmentId === targetTeam.departmentId) {
      // Same department - use normal team access instead
      throw new Error('Cross-department access only needed for different departments');
    }

    // Check permission boundaries
    const sourceDept = await this.departmentService.getDepartment(sourceTeam.departmentId);
    if (!sourceDept?.settings.allowCrossDepartmentVisibility) {
      throw new Error('Source department does not allow cross-department access');
    }

    const grant: CrossDepartmentPermission = {
      id: generateId('xdept'),
      sourceTeamId,
      targetTeamId,
      permissions,
      grantedBy,
      grantedAt: new Date(),
      expiresAt,
      reason,
      status: 'active',
    };

    await this.db.insert('cross_dept_permissions', grant);

    // Notify both department heads
    await this.notificationService.notify({
      type: 'cross_dept_access_granted',
      recipients: [
        sourceDept.headUserId,
        (await this.departmentService.getDepartment(targetTeam.departmentId))?.headUserId,
      ],
      data: { grant },
    });

    return grant;
  }

  async checkCrossDeptAccess(
    userId: string,
    targetTeamId: string,
    resourceType: string,
    action: string
  ): Promise<boolean> {
    const user = await this.userService.getUser(userId);
    if (!user) return false;

    const userTeamIds = await this.teamService.getUserTeamIds(userId);

    // Check each of user's teams for cross-dept grants to the target
    for (const sourceTeamId of userTeamIds) {
      const grants = await this.db.find('cross_dept_permissions', {
        sourceTeamId,
        targetTeamId,
        status: 'active',
        $or: [
          { expiresAt: null },
          { expiresAt: { $gt: new Date() } },
        ],
      });

      for (const grant of grants) {
        const hasAccess = grant.permissions.some(p =>
          p.resourceType === resourceType && (
            p.actions.includes(action) || p.actions.includes('*')
          )
        );
        if (hasAccess) return true;
      }
    }

    return false;
  }
}
```

## Shared Campaigns Across Departments

```typescript
interface SharedCampaign {
  id: string;
  campaignId: string;
  ownerDepartmentId: string;
  collaboratingDepartmentIds: string[];
  sharedResources: SharedResource[];
  accessLevel: 'view' | 'contribute' | 'co_own';
  createdAt: Date;
}

interface SharedResource {
  type: 'agents' | 'phone_numbers' | 'contacts' | 'scripts' | 'analytics';
  ids: string[];
  sharingMode: 'copy' | 'reference' | 'pool';
}

class CampaignSharingService {
  async shareCampaign(
    campaignId: string,
    ownerDeptId: string,
    collaboratorDeptIds: string[],
    accessLevel: SharedCampaign['accessLevel']
  ): Promise<SharedCampaign> {
    const share: SharedCampaign = {
      id: generateId('shared_camp'),
      campaignId,
      ownerDepartmentId: ownerDeptId,
      collaboratingDepartmentIds: collaboratorDeptIds,
      sharedResources: await this.getSharedResources(campaignId, collaboratorDeptIds),
      accessLevel,
      createdAt: new Date(),
    };

    await this.db.insert('shared_campaigns', share);

    // Copy or reference resources based on sharing mode
    for (const resource of share.sharedResources) {
      await this.shareResource(resource, ownerDeptId, collaboratorDeptIds);
    }

    return share;
  }

  async getCrossDeptCampaigns(userId: string): Promise<Campaign[]> {
    const userDeptIds = await this.departmentService.getUserDepartmentIds(userId);
    const sharedCampaigns = await this.db.find('shared_campaigns', {
      collaboratingDepartmentIds: { $in: userDeptIds },
    });

    const campaignIds = sharedCampaigns.map(s => s.campaignId);
    return this.campaignService.getCampaigns({ ids: campaignIds });
  }

  private async shareResource(
    resource: SharedResource,
    ownerDeptId: string,
    collaboratorDeptIds: string[]
  ): Promise<void> {
    switch (resource.sharingMode) {
      case 'copy':
        // Create copies for each collaborator
        for (const deptId of collaboratorDeptIds) {
          await this.resourceService.copyResources(ownerDeptId, deptId, resource);
        }
        break;
      case 'reference':
        // Create read-only references
        for (const deptId of collaboratorDeptIds) {
          await this.resourceService.createReference(ownerDeptId, deptId, resource);
        }
        break;
      case 'pool':
        // Create shared pool
        await this.resourceService.createSharedPool(resource, [
          ownerDeptId,
          ...collaboratorDeptIds,
        ]);
        break;
    }
  }
}
```

## Cross-Team Data Access Middleware

```typescript
function requireCrossDeptAccess(resourceType: string) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const user = req.user;
    const targetTeamId = req.params.teamId;

    // Check if user has normal access
    const normalAccess = await permissionEngine.check({
      userId: user.id,
      tenantId: user.tenantId,
      action: req.method.toLowerCase(),
      resource: resourceType,
      resourceId: targetTeamId,
    });

    if (normalAccess.allowed) {
      return next();
    }

    // Check cross-department access
    const crossDeptAccess = await crossDeptService.checkCrossDeptAccess(
      user.id,
      targetTeamId,
      resourceType,
      req.method.toLowerCase()
    );

    if (crossDeptAccess) {
      req.crossDeptAccess = true;
      req.originalTeam = targetTeamId;
      return next();
    }

    return res.status(403).json({ error: 'Cross-department access denied' });
  };
}
```

## Open-Source Tools

- **Casbin** (Apache 2.0) — Cross-tenant/ cross-department permission models
- **Permit.io** (Apache 2.0) — Relationship-based access control (ReBAC) for org structures

## Production Considerations

- Default-deny cross-department access; must be explicitly granted
- Time-bound grants with automatic expiry (default 30 days, renewable)
- Audit all cross-department data access with reason tracking
- Notify department heads when cross-department access is used
- Provide cross-department collaboration views in analytics dashboards
- Rate-limit cross-department data access to prevent bulk extraction
- Allow department heads to view a report of all active cross-department grants
- Support approval workflows for sensitive cross-department resource sharing
