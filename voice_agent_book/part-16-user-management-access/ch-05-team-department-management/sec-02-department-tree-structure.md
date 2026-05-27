# Department Tree Structure

## Overview

The department tree represents the top-level organizational structure within a tenant. Departments contain teams and sub-teams, have designated department heads, support matrix reporting where employees report to multiple managers, and enable cross-functional collaboration.

## Department Model

```typescript
interface Department {
  id: string;
  tenantId: string;
  name: string;
  code: string;                // Short code (e.g., "SALES", "ENG")
  headUserId?: string;         // Department head (manager)
  parentDepartmentId?: string; // For nested departments
  budgetCode?: string;         // Billing/cost center code
  settings: DepartmentSettings;
  metadata: DepartmentMetadata;
  createdAt: Date;
  updatedAt: Date;
}

interface DepartmentSettings {
  allowCrossDepartmentVisibility: boolean;
  requireManagerApprovalForTransfers: boolean;
  defaultTeamSettings: Partial<TeamSettings>;
  budgetAllocation?: {
    monthlyLimit: number;
    currency: string;
    notifyAtPercent: number;   // Alert at 80% usage
  };
}

interface DepartmentMetadata {
  employeeCount: number;
  teamCount: number;
  createdAt: Date;
  headSince?: Date;
}
```

## Matrix Reporting

```typescript
interface MatrixReport {
  userId: string;
  primaryDepartmentId: string;   // Home department
  secondaryDepartmentIds: string[]; // Matrix/cross-functional departments
  managerId: string;              // Primary manager
  matrixManagerIds: string[];     // Secondary managers
  startDate: Date;
  endDate?: Date;
  allocation: number;             // Percentage (0-100) of time
}

class MatrixReportingService {
  async assignMatrixReport(
    userId: string,
    secondaryDeptId: string,
    matrixManagerId: string,
    allocation: number
  ): Promise<MatrixReport> {
    const user = await this.userService.getUser(userId);
    if (!user) throw new Error('User not found');

    const department = await this.getDepartment(secondaryDeptId);
    if (!department || !department.settings.allowCrossDepartmentVisibility) {
      throw new Error('Matrix reporting not allowed for this department');
    }

    const existing = await this.db.findOne('matrix_reports', {
      userId,
      secondaryDepartmentId: secondaryDeptId,
      endDate: null,
    });

    if (existing) {
      throw new Error('Matrix assignment already exists for this department');
    }

    // Calculate total allocation
    const currentAllocations = await this.getCurrentAllocations(userId);
    const totalAfterAdd = currentAllocations.reduce((sum, a) => sum + a.allocation, 0) + allocation;
    if (totalAfterAdd > 100) {
      throw new Error(`Total allocation would exceed 100% (currently ${totalAfterAdd - allocation}%)`);
    }

    const report: MatrixReport = {
      userId,
      primaryDepartmentId: user.departmentId,
      secondaryDepartmentId: secondaryDeptId,
      managerId: user.managerId,
      matrixManagerIds: [matrixManagerId],
      startDate: new Date(),
      allocation,
    };

    await this.db.insert('matrix_reports', report);

    // Add user to cross-functional team if exists
    await this.teamService.addUserToTeam(userId, department.id, 'member');

    return report;
  }

  async getEffectiveManager(userId: string, context: {
    departmentId?: string;
    projectId?: string;
  }): Promise<string> {
    if (context.departmentId) {
      const matrixAssignment = await this.db.findOne('matrix_reports', {
        userId,
        secondaryDepartmentId: context.departmentId,
        endDate: null,
      });
      if (matrixAssignment) {
        return matrixAssignment.matrixManagerIds[0];
      }
    }

    // Fall back to primary manager
    const user = await this.userService.getUser(userId);
    return user.managerId;
  }

  async getDirectReports(managerId: string): Promise<User[]> {
    // Primary reports
    const primaryReports = await this.userService.getUsers({ managerId });

    // Matrix reports
    const matrixReports = await this.db.find('matrix_reports', {
      matrixManagerIds: managerId,
      endDate: null,
    });

    const matrixUserIds = matrixReports.map(r => r.userId);
    const matrixUsers = await this.userService.getUsersByIds(matrixUserIds);

    return [...primaryReports, ...matrixUsers];
  }

  async getOrganizationChart(departmentId: string): Promise<OrgChartNode> {
    const dept = await this.getDepartment(departmentId);
    if (!dept) throw new Error('Department not found');

    const teams = await this.teamService.getDepartmentTeams(departmentId);
    const deptHead = dept.headUserId ? await this.userService.getUser(dept.headUserId) : null;

    return {
      department: dept,
      head: deptHead,
      teams: await Promise.all(teams.map(async team => ({
        team,
        lead: team.teamLeadId ? await this.userService.getUser(team.teamLeadId) : null,
        members: await this.teamService.getTeamMembers(team.id),
      }))),
      matrixAssignments: await this.db.find('matrix_reports', {
        $or: [
          { primaryDepartmentId: departmentId },
          { secondaryDepartmentId: departmentId },
        ],
        endDate: null,
      }),
    };
  }
}

interface OrgChartNode {
  department: Department;
  head: User | null;
  teams: Array<{
    team: Team;
    lead: User | null;
    members: TeamMember[];
  }>;
  matrixAssignments: MatrixReport[];
}
```

## Cross-Functional Teams

```typescript
class CrossFunctionalTeamService {
  async createCrossFunctionalTeam(
    name: string,
    departments: string[],
    leadUserId: string
  ): Promise<Team> {
    // Create a virtual team spanning multiple departments
    const team = await this.teamService.createTeam({
      tenantId: currentTenant,
      name,
      type: 'subteam',
      parentId: null, // Standalone cross-functional team
      settings: {
        allowCrossTeamAccess: true,
        requireApprovalForJoin: false,
        visibility: 'join_request',
      },
      metadata: {
        isCrossFunctional: true,
        departments,
        leadUserId,
      },
    });

    // Add department heads as observers
    for (const deptId of departments) {
      const dept = await this.getDepartment(deptId);
      if (dept?.headUserId) {
        await this.teamService.addMember(team.id, dept.headUserId, 'observer');
      }
    }

    return team;
  }

  async getDepartmentCrossFunctionalTeams(departmentId: string): Promise<Team[]> {
    return this.db.find('teams', {
      'metadata.isCrossFunctional': true,
      'metadata.departments': departmentId,
      isActive: true,
    });
  }
}
```

## Department Dashboard

```
Department: Engineering
├── Employees: 45
├── Teams: 6 (backend, frontend, infra, mobile, QA, devops)
├── Matrix Assignments: 8
├── Budget Usage: 62% ($124k/$200k)
│
└── Org Chart
    ├── VP Engineering (dept head)
    ├── Backend (10 members) ← Lead: Alice
    ├── Frontend (8 members) ← Lead: Bob
    ├── Infrastructure (5 members) ← Lead: Charlie
    └── ...
```

## Open-Source Tools

- **d3-org-chart** (MIT) — Organization chart visualization
- **react-org-chart** (MIT) — React org chart component

## Production Considerations

- Enforce one primary department per user with optional matrix assignments
- Cap cross-functional allocations to prevent over-commitment (max 200% total)
- Matrix assignments expire by default (12 months) with renewal option
- Notify primary and matrix managers when allocation changes
- Department head role grants admin-level permissions within the department
- Audit all department structure changes with before/after snapshots
- Allow department-level custom fields and metadata for tenant-specific needs
