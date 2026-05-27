# Team Hierarchy Model

## Overview

The team hierarchy model defines the organizational tree structure within a tenant. It supports nested teams, parent-child relationships, configurable depth limits, and flexible reporting lines to model any organizational structure.

## Hierarchy Structure

```
Tenant Root
└── Department (e.g., Sales)
    ├── Team (e.g., Outbound Sales)
    │   ├── Sub-team (e.g., Senior Agents)
    │   │   ├── Agent User
    │   │   └── Agent User
    │   └── Sub-team (e.g., Junior Agents)
    └── Team (e.g., Inside Sales)
        └── Sub-team
```

## Data Model

```typescript
interface Team {
  id: string;
  tenantId: string;
  name: string;
  description?: string;
  parentId: string | null;       // Null = root-level team
  departmentId?: string;
  teamLeadId?: string;           // User ID of team lead
  type: 'department' | 'team' | 'subteam';
  settings: TeamSettings;
  path: string;                  // Materialized path: /root/team/subteam
  depth: number;
  sortOrder: number;
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
  metadata?: Record<string, unknown>;
}

interface TeamSettings {
  allowCrossTeamAccess: boolean;
  requireApprovalForJoin: boolean;
  visibility: 'open' | 'join_request' | 'closed';
  maxMembers?: number;
  inheritParentPermissions: boolean;
  autoAssignNewUsers: boolean;
}

interface TeamMember {
  id: string;
  teamId: string;
  userId: string;
  role: 'lead' | 'member' | 'observer';
  joinedAt: Date;
  expiresAt?: Date;
  permissions?: TeamSpecificPermission[];
}
```

## Team Operations

```typescript
class TeamService {
  async createTeam(team: Omit<Team, 'id' | 'path' | 'depth' | 'createdAt' | 'updatedAt'>): Promise<Team> {
    // Validate parent exists
    if (team.parentId) {
      const parent = await this.getTeam(team.parentId);
      if (!parent) throw new Error('Parent team not found');
      if (parent.depth >= MAX_TEAM_DEPTH) {
        throw new Error(`Maximum team depth (${MAX_TEAM_DEPTH}) exceeded`);
      }

      team.depth = parent.depth + 1;
      team.path = `${parent.path}/${team.name}`;
    } else {
      team.depth = 0;
      team.path = `/${team.name}`;
    }

    // Validate no duplicate name at same level
    const existing = await this.db.findOne('teams', {
      tenantId: team.tenantId,
      parentId: team.parentId,
      name: team.name,
    });
    if (existing) throw new Error('Team name already exists at this level');

    const newTeam: Team = {
      ...team,
      id: generateId('team'),
      createdAt: new Date(),
      updatedAt: new Date(),
      isActive: true,
      sortOrder: await this.getNextSortOrder(team.tenantId, team.parentId),
    };

    await this.db.insert('teams', newTeam);

    // Update parent team metadata
    if (parentId) {
      await this.incrementChildCount(parentId);
    }

    return newTeam;
  }

  async moveTeam(teamId: string, newParentId: string | null): Promise<void> {
    const team = await this.getTeam(teamId);
    if (!team) throw new Error('Team not found');

    const oldParentId = team.parentId;

    // Update team position
    const newPath = newParentId
      ? `${(await this.getTeam(newParentId))!.path}/${team.name}`
      : `/${team.name}`;

    // Update all descendants' paths (materialized path update)
    const descendants = await this.getDescendantTeamIds(teamId);
    for (const desc of descendants) {
      const descTeam = await this.getTeam(desc);
      if (descTeam) {
        descTeam.path = descTeam.path.replace(team.path, newPath);
        await this.db.update('teams', { id: desc.id }, { path: descTeam.path });
      }
    }

    await this.db.update('teams', { id: teamId }, {
      parentId: newParentId,
      path: newPath,
      updatedAt: new Date(),
    });

    // Recalculate depth for team and descendants
    await this.recalculateDepths(teamId);
  }

  async getTeamTree(tenantId: string, rootId?: string): Promise<TeamTreeNode> {
    const root = rootId
      ? await this.getTeam(rootId)
      : await this.getRootTeam(tenantId);

    if (!root) throw new Error('Root team not found');

    const children = await this.db.find('teams', { parentId: root.id, isActive: true });

    return {
      ...root,
      children: await Promise.all(
        children.map(child => this.getTeamTree(tenantId, child.id))
      ),
    };
  }

  async getAncestorTeamIds(teamId: string): Promise<string[]> {
    const team = await this.getTeam(teamId);
    if (!team || !team.parentId) return [];
    const ancestors: string[] = [];
    let current = team;
    while (current.parentId) {
      const parent = await this.getTeam(current.parentId);
      if (parent) {
        ancestors.unshift(parent.id);
        current = parent;
      } else break;
    }
    return ancestors;
  }

  async getDescendantTeamIds(teamId: string): Promise<string[]> {
    return this.db.find('teams', {
      path: { $regex: `^${team.path}/` },
      tenantId: team.tenantId,
    }).then(teams => teams.map(t => t.id));
  }

  async getSubtreeUserIds(teamId: string): Promise<string[]> {
    const descendantIds = await this.getDescendantTeamIds(teamId);
    const allTeamIds = [teamId, ...descendantIds];

    const members = await this.db.find('team_members', {
      teamId: { $in: allTeamIds },
      role: { $ne: 'observer' },
    });

    return [...new Set(members.map(m => m.userId))];
  }

  async getTeamHierarchyPath(teamId: string): Promise<Team[]> {
    const team = await this.getTeam(teamId);
    if (!team) return [];

    const path: Team[] = [team];
    let current = team;
    while (current.parentId) {
      const parent = await this.getTeam(current.parentId);
      if (parent) {
        path.unshift(parent);
        current = parent;
      } else break;
    }
    return path;
  }
}
```

## Materialized Path Strategy

```typescript
// The materialized path enables efficient subtree queries
// Path format: /root/engineering/backend/team-alpha

// Query all descendants of a node:
const descendants = await db.find('teams', {
  path: { $regex: `^/root/engineering/backend/team-alpha/` },
});

// Query all ancestors (parsing the path):
const ancestors = team.path.split('/').filter(Boolean);
// Returns: ['root', 'engineering', 'backend', 'team-alpha']
```

## Open-Source Tools

- **closure-table** pattern via Prisma or TypeORM for hierarchy queries
- **materialized-path** (npm) — Node.js utility for path-based tree operations
- **treeize** (npm) — Convert flat arrays to nested tree structures

## Production Considerations

- Enforce maximum team depth (recommended: 5 levels) to prevent overly complex hierarchies
- Use materialized path for efficient subtree queries (single indexed regex query vs recursive CTEs)
- Cache team hierarchy in Redis with TTL (5 minutes) and invalidate on structure changes
- Validate no circular references when moving teams
- Soft-delete teams to preserve historical data and audit trails
- Index the path field for efficient subtree queries
- Batch team member operations to avoid N+1 queries on large teams
- Provide team search by name, parent, and member count for admin UI
