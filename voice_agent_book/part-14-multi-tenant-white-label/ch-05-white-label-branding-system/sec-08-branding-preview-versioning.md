# Section 08: Branding Preview & Versioning

## Overview

The branding preview and versioning system allows tenants to experiment with their brand configuration before publishing, maintain a history of changes, and roll back to previous versions if needed. This is critical for white-label deployments where branding mistakes affect the tenant's end users. The system supports draft/published states, version history with diffs, scheduled publishing, and team collaboration.

A branding change goes through a lifecycle: draft (in progress, not visible), preview (viewable by admins only), published (live for all users), and archived (superseded by newer version). Each change is recorded as a version entry with the full snapshot of branding configuration, the user who made the change, and a timestamp. Versions can be compared to show specific changes between any two versions.

The preview mode allows applying upcoming branding changes to a subset of pages or user sessions. This enables the tenant admin to verify how the branding will look across the dashboard, login page, and email templates before publishing. Preview can be scoped to the admin's session, a specific IP range, or a percentage of users.

## Implementation Approach

```typescript
interface BrandingVersion {
  id: string;
  tenantId: string;
  version: number;
  branding: BrandingConfig;
  status: 'draft' | 'preview' | 'published' | 'archived';
  createdBy: string;
  createdAt: Date;
  publishedAt?: Date;
  notes?: string;
}

class BrandingVersionService {
  async createDraft(tenantId: string, branding: BrandingConfig, userId: string): Promise<BrandingVersion> {
    const lastVersion = await this.getLatestVersion(tenantId);
    const nextVersion = (lastVersion?.version || 0) + 1;

    const draft = await this.db.query(`
      INSERT INTO branding_versions (tenant_id, version, branding, status, created_by, created_at)
      VALUES ($1, $2, $3, 'draft', $4, NOW())
      RETURNING *
    `, [tenantId, nextVersion, JSON.stringify(branding), userId]);

    return draft.rows[0];
  }

  async previewVersion(versionId: string, scope?: PreviewScope): Promise<string> {
    const version = await this.getVersion(versionId);
    
    // Apply branding to preview
    const previewUrl = `${this.previewHost}/preview/${versionId}`;
    
    // Set preview cookie/header to activate this brand version
    await this.cache.setex(`preview:${version.tenantId}`, 3600, versionId);

    return previewUrl;
  }

  async publishVersion(versionId: string, userId: string): Promise<void> {
    const version = await this.getVersion(versionId);
    
    // Unpublish current live version
    await this.db.query(
      `UPDATE branding_versions SET status = 'archived' 
       WHERE tenant_id = $1 AND status = 'published'`,
      [version.tenant_id]
    );

    // Publish new version
    await this.db.query(
      `UPDATE branding_versions SET status = 'published', published_at = NOW() WHERE id = $1`,
      [versionId]
    );

    // Apply branding to production
    await this.applyBrandingToProduction(version);
  }

  async getDiff(versionId1: string, versionId2: string): Promise<BrandingDiff> {
    const [v1, v2] = await Promise.all([
      this.getVersion(versionId1),
      this.getVersion(versionId2),
    ]);

    const changes: Change[] = [];
    for (const key of Object.keys({ ...v1.branding, ...v2.branding })) {
      if (JSON.stringify(v1.branding[key]) !== JSON.stringify(v2.branding[key])) {
        changes.push({
          field: key,
          oldValue: v1.branding[key],
          newValue: v2.branding[key],
        });
      }
    }

    return { version1: versionId1, version2: versionId2, changes };
  }

  async rollback(tenantId: string, targetVersion: number, userId: string): Promise<void> {
    const target = await this.db.query(
      `SELECT * FROM branding_versions 
       WHERE tenant_id = $1 AND version = $2`,
      [tenantId, targetVersion]
    );

    if (target.rows.length === 0) {
      throw new Error('Target version not found');
    }

    // Create a new version from the target (immutable history)
    await this.createDraft(tenantId, target.rows[0].branding, userId);
    
    // Publish immediately
    const draft = await this.getLatestDraft(tenantId);
    await this.publishVersion(draft.id, userId);
  }

  private async applyBrandingToProduction(version: BrandingVersion): Promise<void> {
    // Invalidate cache
    await this.cache.del(`theme:${version.tenant_id}`);
    
    // Send event to update CDN, email templates, etc.
    await this.eventBus.publish('branding.updated', {
      tenantId: version.tenant_id,
      branding: version.branding,
      timestamp: new Date(),
    });
  }
}

// Preview middleware
async function brandingPreviewMiddleware(req, res, next) {
  const previewId = req.cookies?.branding_preview;
  
  if (previewId) {
    const version = await brandVersionService.getVersion(previewId);
    if (version) {
      // Apply this branding version to the response
      res.locals.brandingOverride = version.branding;
      res.setHeader('X-Branding-Preview', version.version);
    }
  }
  
  next();
}
```

## Open-Source Tools

- **deep-diff** — JavaScript object diff library for version comparison
- **React DnD** — Drag-and-drop for preview mode
- **Immer** — Immutable state management for version snapshots
- **PostgreSQL JSONB** — Store version snapshots as JSONB with GIN indexes
- **jsondiffpatch** — Visual diff display for branding changes

## Production Considerations

- **Version Storage:** Branding snapshots can be large (logos, CSS). Store only the configuration (color values, URLs to assets, not the assets themselves). Assets are versioned separately.
- **Preview Cookie:** Preview mode uses a session cookie scoped to the admin. Never expose preview branding to end users accidentally.
- **Rollback Safety:** Rolling back to a previous version should be an atomic operation. Use database transactions to unpublish current and publish old version simultaneously.
- **Audit Trail:** All branding changes are logged with user attribution. This is important for SOC 2 compliance and internal governance.
- **Scheduled Publishing:** Support scheduling branding changes for specific dates/times. This is useful for rebranding events, holiday themes, or marketing campaigns.
