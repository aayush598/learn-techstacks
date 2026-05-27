# Bulk User Import

## Overview

Bulk user import enables onboarding multiple users simultaneously via CSV/JSON upload with validation, duplicate detection, error reporting, and rollback on failure. Ideal for migrating teams from legacy systems.

## Import Pipeline

```
Upload CSV/JSON → Parse → Validate → Preview → Confirm → Import
                    ↓          ↓          ↓
               Schema      Duplicate   Error Report
               Validation  Check
```

## Implementation

```typescript
interface BulkImportRequest {
  tenantId: string;
  fileName: string;
  users: ImportedUser[];
  defaultRoleId: string;
  defaultTeamId?: string;
  sendInvitations: boolean;
  onDuplicate: 'skip' | 'update' | 'error';
  importedBy: string;
}

interface ImportedUser {
  email: string;
  name: string;
  role?: string;
  team?: string;
  department?: string;
  phone?: string;
}

class BulkImportService {
  async validate(rows: ImportedUser[]): Promise<ImportValidation> {
    const errors: ImportError[] = [];
    const emails = new Map<string, number>();

    for (let i = 0; i < rows.length; i++) {
      const row = rows[i];
      const lineNum = i + 2; // Header + 1-indexed

      if (!row.email || !row.email.includes('@')) {
        errors.push({ line: lineNum, field: 'email', error: 'Invalid email address' });
      }
      if (!row.name || row.name.length < 2) {
        errors.push({ line: lineNum, field: 'name', error: 'Name too short' });
      }

      const existing = emails.get(row.email);
      if (existing) {
        errors.push({ line: lineNum, field: 'email', error: `Duplicate email (also on line ${existing})` });
      } else {
        emails.set(row.email, lineNum);
      }
    }

    return {
      valid: errors.length === 0,
      errors,
      totalRows: rows.length,
      validRows: rows.length - new Set(errors.map(e => e.line)).size,
    };
  }

  async import(request: BulkImportRequest): Promise<ImportResult> {
    const result: ImportResult = { success: 0, failed: 0, errors: [] };
    const batchSize = 50;

    for (let i = 0; i < request.users.length; i += batchSize) {
      const batch = request.users.slice(i, i + batchSize);
      const operations = batch.map(async (row, idx) => {
        try {
          const existing = await this.userService.findByEmail(row.email, request.tenantId);
          if (existing) {
            switch (request.onDuplicate) {
              case 'skip':
                result.success++;
                return;
              case 'update':
                await this.userService.updateUser(existing.id, { name: row.name });
                result.success++;
                return;
              case 'error':
                throw new Error('User already exists');
            }
          }

          const user = await this.userService.createUser({
            email: row.email, name: row.name, tenantId: request.tenantId, status: 'pending',
          });

          const roleId = row.role ? await this.lookupRoleId(row.role, request.tenantId) : request.defaultRoleId;
          await this.roleService.assignRole(user.id, roleId, request.importedBy);

          if (request.sendInvitations) {
            await this.invitationService.sendInvitation(user.id, request.importedBy);
          }

          result.success++;
        } catch (error) {
          result.failed++;
          result.errors.push({ line: i + idx + 2, error: String(error) });
        }
      });

      await Promise.allSettled(operations);
    }

    return result;
  }
}
```

## CSV Format

```csv
email,name,role,team
alice@example.com,Alice Johnson,Agent,Sales Team
bob@example.com,Bob Smith,Manager,Sales Team
```

## Open-Source Tools

- **papaparse** (MIT) — CSV parsing
- **xlsx** (MIT) — Excel file parsing

## Production Considerations

- Max 10,000 users per import
- Process in batches of 50 with transaction per batch
- Preview before confirm with error count
- Generate detailed import report with per-user status
- Rate-limit imports: max 5 per hour per tenant
- Rollback on critical errors (schema mismatch, auth failure)
