# Section 06: Report Collaboration & Sharing

## Overview

The report collaboration and sharing system enables teams to work together on report definitions, share report snapshots, and manage access permissions. Multiple users can view and edit the same report simultaneously, with changes tracked through version history and conflict resolution. Reports can be shared via public links (with optional password protection), embedded in iframes, or cloned as templates for other users.

The collaboration layer extends the report builder with commenting, annotation, and approval workflows. When a report is published (marked as "final"), the definition is frozen and subsequent edits create a draft version. Reviewers can leave comments on specific widgets or data points. The sharing system integrates with the existing role-based access control, supporting view-only, edit, and admin permission levels for each report.

## Architecture

```

              Report Collaboration Architecture

   Report Builder Client → Collaboration Hub
                               |
                     ┌─────────┴──────────┐
                     ▼                    ▼
              Real-Time Sync         Version Control
              (WebSocket/OT)         (Git-like history)
                     |                    |
                     ▼                    ▼
              Presence Service       Snapshot Store
              (who's viewing)        (immutable diffs)
                     |                    |
                     └─────────┬──────────┘
                               ▼
                        Permission Manager
                               |
                     ┌─────────┴──────────┐
                     ▼                    ▼
              Share Link Generator    Embed Token
              (signed URLs)           (iframes)
```

## Design Decisions

- **Operational Transform (OT) for real-time collaboration over last-write-wins:** When two users edit a report simultaneously, OT merges concurrent changes at the operation level (add widget, move widget, change config). Conflicts are rare because report editing is typically coarse-grained (adding/removing widgets), but OT ensures no data loss. Trade-off: OT requires a coordination server and increases complexity; for reports where concurrent editing is uncommon, a simpler "check-out/check-in" locking model might suffice.

- **Snapshot-based version history with diff storage over full-copy storage:** Each save creates an immutable snapshot stored as a JSON diff (using RFC 6902 JSON Patch) from the previous snapshot. This reduces storage per version from ~50 KB (full definition) to ~2 KB (average diff). The version history shows who changed what, with the ability to revert to any previous version. Trade-off: reconstructing an old version requires replaying all diffs from the initial snapshot, taking ~5 ms per 100 versions for large reports.

- **Signed share links with optional expiry over permanent access:** Share links include a JWT signed with a tenant-specific secret, containing the report ID, permission level, and expiry timestamp. Links can be configured to expire after a set duration (24 hours, 7 days, 30 days, never) and can be revoked by the report owner at any time. Trade-off: signed links cannot be individually revoked after issuance (only by changing the tenant secret, which invalidates all links), so an explicit revoke list is maintained for immediate access removal.

## Implementation Approach

```typescript
interface ReportCollaboration {
  reportId: string;
  version: number;
  lastEditor: string;
  editors: EditorPresence[];
  comments: ReportComment[];
  status: 'draft' | 'review' | 'published' | 'archived';
}

interface EditorPresence {
  userId: string;
  userName: string;
  lastActiveAt: number;
  cursor?: { widgetId?: string; section?: string };
}

interface ReportComment {
  id: string;
  reportId: string;
  widgetId?: string;
  dataPoint?: Record<string, unknown>;
  authorId: string;
  authorName: string;
  text: string;
  resolved: boolean;
  createdAt: number;
  replies: ReportComment[];
}

interface ShareLink {
  id: string;
  reportId: string;
  tenantId: string;
  permission: 'view' | 'comment' | 'edit';
  expiresAt: number | null;
  passwordHash?: string;
  maxUses: number | null;
  useCount: number;
  createdAt: number;
  createdBy: string;
  revoked: boolean;
}

class CollaborationManager {
  private wsServer: WebSocketServer;
  private versionStore: VersionStore;
  private permissionManager: PermissionManager;

  async joinSession(userId: string, reportId: string): Promise<void> {
    // Add user to presence
    await this.presenceService.join(reportId, userId);

    // Send current version to new joiner
    const currentVersion = await this.versionStore.getCurrent(reportId);
    this.wsServer.send(userId, {
      type: 'session_state',
      reportId,
      version: currentVersion,
      editors: await this.presenceService.getEditors(reportId),
    });
  }

  async applyOperation(
    userId: string,
    reportId: string,
    operation: ReportOperation
  ): Promise<void> {
    // Get current document state
    const doc = await this.versionStore.getDocument(reportId);

    // Transform operation against any concurrent operations
    const concurrentOps = await this.getConcurrentOperations(reportId, userId);
    let transformedOp = operation;
    for (const concurrentOp of concurrentOps) {
      transformedOp = this.transform(transformedOp, concurrentOp);
    }

    // Apply operation
    const newDoc = this.applyToDocument(doc, transformedOp);
    const newVersion = doc.version + 1;

    // Store diff
    await this.versionStore.saveDiff(reportId, newVersion, userId, {
      patch: this.generatePatch(doc, newDoc),
      timestamp: Date.now(),
    });

    // Broadcast to all collaborators
    this.wsServer.broadcast(reportId, {
      type: 'operation',
      userId,
      version: newVersion,
      operation: transformedOp,
    }, [userId]); // Exclude sender
  }

  private transform(op1: ReportOperation, op2: ReportOperation): ReportOperation {
    // OT transformation function
    // For widget operations, check if they affect different widgets (commutative)
    if (op1.type === 'add_widget' && op2.type === 'remove_widget') {
      if (op1.widgetId === op2.widgetId) {
        // Counteracting operations — remove wins
        return { ...op1, type: 'noop' };
      }
      return op1; // Different widgets, no conflict
    }

    if (op1.type === 'move_widget' && op2.type === 'move_widget') {
      if (op1.widgetId === op2.widgetId) {
        // Same widget moved twice — the later move wins
        return op1;
      }
      return op1;
    }

    return op1;
  }

  async generateShareLink(params: {
    reportId: string;
    tenantId: string;
    permission: 'view' | 'comment' | 'edit';
    expiresIn?: number; // ms from now, null = never
    password?: string;
    maxUses?: number;
    createdBy: string;
  }): Promise<{ url: string; linkId: string }> {
    const linkId = generateId();
    const token = await this.signShareToken({
      linkId,
      reportId: params.reportId,
      tenantId: params.tenantId,
      permission: params.permission,
      exp: params.expiresIn ? Date.now() + params.expiresIn : null,
    });

    await this.shareStore.create({
      id: linkId,
      reportId: params.reportId,
      tenantId: params.tenantId,
      permission: params.permission,
      expiresAt: params.expiresIn ? Date.now() + params.expiresIn : null,
      passwordHash: params.password ? await hash(params.password) : undefined,
      maxUses: params.maxUses || null,
      useCount: 0,
      createdAt: Date.now(),
      createdBy: params.createdBy,
      revoked: false,
    });

    return {
      url: `${BASE_URL}/shared/${token}`,
      linkId,
    };
  }

  async accessSharedReport(token: string, password?: string): Promise<ReportDefinition | null> {
    const payload = await this.verifyShareToken(token);
    if (!payload) return null;

    const link = await this.shareStore.get(payload.linkId);
    if (!link || link.revoked) return null;
    if (link.expiresAt && Date.now() > link.expiresAt) return null;
    if (link.maxUses && link.useCount >= link.maxUses) return null;

    if (link.passwordHash) {
      if (!password) throw new Error('Password required');
      if (!await verify(password, link.passwordHash)) throw new Error('Invalid password');
    }

    // Increment use count
    await this.shareStore.incrementUse(link.id);

    // Return report definition (anonymized for view-only)
    const report = await this.reportStore.get(link.reportId);

    if (link.permission === 'view') {
      return this.anonymizeReport(report);
    }

    return report;
  }

  private async signShareToken(payload: Record<string, unknown>): Promise<string> {
    const secret = await this.getTenantSecret(payload.tenantId as string);
    return jwt.sign(payload, secret, { algorithm: 'HS256' });
  }

  private async verifyShareToken(token: string): Promise<Record<string, unknown> | null> {
    try {
      // Try each tenant secret (brute force over known secrets)
      const secrets = await this.getAllTenantSecrets();
      for (const secret of secrets) {
        try {
          return jwt.verify(token, secret, { algorithms: ['HS256'] }) as Record<string, unknown>;
        } catch {
          continue;
        }
      }
      return null;
    } catch {
      return null;
    }
  }

  private anonymizeReport(report: ReportDefinition): ReportDefinition {
    // Remove data source credentials, strip PII filter values
    return {
      ...report,
      widgets: report.widgets.map(w => ({
        ...w,
        dataSource: { ...w.dataSource, sourceId: w.dataSource.sourceId },
      })),
    };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Socket.IO (MIT) | Server/Client | WebSocket real-time collaboration |
| ShareDB (Apache 2.0) | Server | OT engine for concurrent editing |
| json0 (MIT) | Server | JSON OT type for report definitions |
| jsonpatch (MIT) | Server | RFC 6902 JSON Patch for version diffs |

## Production Considerations

**Scaling:** The OT server maintains in-memory document state for actively-edited reports. For tenants with 100+ simultaneous editors, partition document state across Redis shards. Version diffs are stored in PostgreSQL with a 90-day retention policy — older versions are compacted into full-snapshot archives. WebSocket connections are load-balanced with sticky sessions; if a user's connection drops, the client reconnects and re-fetches the current state.

**Security:** Share link tokens are short-lived (default 7 days) and can be revoked individually. The share link view mode strips all PII and data source connection details from the report definition. Report comments are visible only to users with access to the report; external commenters via share links cannot see other comments. All collaboration operations are logged with user ID, timestamp, and operation type for audit.

**Monitoring:** Track active collaboration sessions, OT operation throughput (ops/second), version history size per report, share link creation and usage count, and conflict resolution rate. Alert if OT operation latency exceeds 200 ms, if version history exceeds 5 MB per report (trigger compaction), or if share link access failures exceed 1% of attempts.
