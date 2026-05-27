# Section 06: Script Versioning & Management

## Overview

Script versioning tracks changes to campaign scripts over time, enabling controlled rollouts, rollback, audit trails, and A/B comparison. A campaign script is a critical asset — a poorly worded script can reduce conversion rates, damage brand perception, or violate compliance requirements. Versioning ensures that changes are deliberate, attributable, and reversible.

The versioning system treats each script as a versioned resource with draft, review, and published states. Multiple versions can exist simultaneously, with campaigns referencing specific versions. When a new version is published, the campaign can switch to it immediately or gradually through canary deployment. Every version change is recorded with the author, timestamp, and change reason for compliance audit.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Script Versioning & Management                  │
├─────────────────────────────────────────────────────────────┤
│  Script Lifecycle:                                          │
│                                                             │
│  DRAFT ──→ REVIEW ──→ APPROVED ──→ PUBLISHED ──→ ARCHIVED │
│    ↑          │                                   ↑        │
│    └──────────┘                                   │        │
│    (revision)                          (superseded)        │
│                                                             │
│  Version History:                                           │
│  ┌──────┬──────────┬────────────┬──────────┬────────────┐  │
│  │ Ver  │ Status   │ Author     │ Date     │ Change     │  │
│  ├──────┼──────────┼────────────┼──────────┼────────────┤  │
│  │ 1.0  │ Published│ jane@acme  │ 01/15    │ Initial    │  │
│  │ 1.1  │ Published│ bob@acme   │ 02/01    │ Changed    │  │
│  │      │          │            │          │ opening    │  │
│  │ 1.2  │ Draft    │ jane@acme  │ 02/10    │ A/B test   │  │
│  │      │          │            │          │ variant    │  │
│  │ 2.0  │ Published│ alice@acme │ 03/01    │ Major      │  │
│  │      │          │            │          │ rewrite    │  │
│  └──────┴──────────┴────────────┴──────────┴────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Design Decisions

- **Immutable published versions:** Once a script version is published, it cannot be modified. Changes create a new version. This ensures reproducibility of campaign results. Trade-off: version proliferation vs. audit integrity.

- **Workflow-based state transitions:** Scripts go through a configurable approval workflow (draft → review → approved → published). Different tenants can have different workflow requirements. Trade-off: workflow overhead vs. change control.

- **Canary deployment for published versions:** New versions can be rolled out to a percentage of calls, with automatic rollback if key metrics degrade. Trade-off: canary infrastructure complexity vs. safe deployment.

- **Diff visualization for review:** The version diff tool shows exactly what changed between versions, making reviews faster and more accurate. Trade-off: diff computation vs. reviewer efficiency.

## Implementation Approach

```
class ScriptVersionManager {
  constructor(prisma, campaignService, notificationService) {
    this.prisma = prisma;
    this.campaigns = campaignService;
    this.notifications = notificationService;
  }

  async createDraft(campaignId, content, author, parentVersionId) {
    const currentVersion = await this.prisma.scriptVersion.findFirst({
      where: { campaign_id: campaignId, status: 'published' },
      orderBy: { version: 'desc' }
    });

    const version = await this.prisma.scriptVersion.create({
      data: {
        campaign_id: campaignId,
        version: (currentVersion?.version || 0) + 0.1,
        content,
        status: 'draft',
        author,
        parent_version_id: parentVersionId || currentVersion?.id,
        created_at: new Date()
      }
    });

    return version;
  }

  async submitForReview(versionId) {
    const version = await this.prisma.scriptVersion.update({
      where: { id: versionId },
      data: { status: 'review' }
    });

    // Notify reviewers
    await this.notifications.sendToRole('campaign_reviewer', {
      type: 'script_review_requested',
      versionId,
      campaignId: version.campaign_id,
      versionNumber: version.version
    });

    return version;
  }

  async approveVersion(versionId, reviewer) {
    const version = await this.prisma.scriptVersion.update({
      where: { id: versionId },
      data: {
        status: 'approved',
        reviewed_by: reviewer,
        reviewed_at: new Date()
      }
    });

    return version;
  }

  async publishVersion(versionId, publisher, options = {}) {
    const version = await this.prisma.scriptVersion.update({
      where: { id: versionId },
      data: {
        status: 'publishing',
        published_by: publisher
      }
    });

    if (options.canaryPercent) {
      // Canary deployment — only apply to X% of calls
      await this.campaigns.setScriptCanary(
        version.campaign_id,
        version.id,
        options.canaryPercent
      );
    } else {
      // Full publication
      await this.prisma.scriptVersion.updateMany({
        where: { 
          campaign_id: version.campaign_id, 
          status: 'published' 
        },
        data: { status: 'archived' }
      });

      await this.prisma.scriptVersion.update({
        where: { id: versionId },
        data: { 
          status: 'published',
          published_at: new Date()
        }
      });

      // Update campaign to use this version
      await this.campaigns.updateActiveScript(
        version.campaign_id,
        version.id
      );
    }

    return version;
  }

  async rollback(campaignId, targetVersionId, actor) {
    const targetVersion = await this.prisma.scriptVersion.findUnique({
      where: { id: targetVersionId }
    });

    if (!targetVersion || targetVersion.status !== 'published') {
      throw new Error('Can only rollback to a published version');
    }

    // Create a new version that reverts to the target
    const rollbackVersion = await this.createDraft(
      campaignId,
      targetVersion.content,
      actor,
      targetVersionId
    );

    // Fast-track approval for rollback
    await this.approveVersion(rollbackVersion.id, actor);
    await this.publishVersion(rollbackVersion.id, actor, {
      reason: `Rollback to version ${targetVersion.version}`
    });

    return rollbackVersion;
  }

  async getVersionDiff(versionIdA, versionIdB) {
    const [a, b] = await Promise.all([
      this.prisma.scriptVersion.findUnique({ where: { id: versionIdA } }),
      this.prisma.scriptVersion.findUnique({ where: { id: versionIdB } })
    ]);

    return this.computeDiff(a.content, b.content);
  }

  computeDiff(contentA, contentB) {
    // Line-level diff using a diff algorithm
    const linesA = contentA.split('\n');
    const linesB = contentB.split('\n');
    const changes = [];

    let idxA = 0;
    let idxB = 0;

    while (idxA < linesA.length || idxB < linesB.length) {
      if (linesA[idxA] === linesB[idxB]) {
        changes.push({ type: 'unchanged', content: linesA[idxA] });
        idxA++;
        idxB++;
      } else if (this.isSimilar(linesA[idxA], linesB[idxB])) {
        changes.push({ type: 'modified', old: linesA[idxA], new: linesB[idxB] });
        idxA++;
        idxB++;
      } else if (idxB < linesB.length && 
                 (idxA >= linesA.length || this.isSimilar(linesA[idxA + 1], linesB[idxB]))) {
        changes.push({ type: 'removed', content: linesA[idxA] });
        idxA++;
      } else {
        changes.push({ type: 'added', content: linesB[idxB] });
        idxB++;
      }
    }

    return changes;
  }

  async getScriptTimeline(campaignId) {
    return this.prisma.scriptVersion.findMany({
      where: { campaign_id: campaignId },
      orderBy: { version: 'desc' },
      include: {
        campaign: { select: { name: true } }
      }
    });
  }
}
```

## Integration Points

- **Campaign Configuration (Ch 01):** Campaign references active script version
- **Compliance Audit (Ch 07):** Script version history is part of compliance records
- **A/B Testing (Ch 10):** A/B test variants use different script versions
- **API (Part 10, Ch 01):** External API can manage script versions programmatically
- **Analytics (Ch 09):** Script version correlated with campaign performance
- **Notification System:** Alerts for pending reviews and publication events

## Open-Source Tools

- **diff / jsdiff:** Text diffing algorithm for version comparison
- **React Diff Viewer:** UI component for visual diff display
- **PostgreSQL:** Version storage with JSON content field
- **BullMQ:** Scheduled rollback timer for canary deployments that auto-rollback
- **Zod:** Script content validation schema for draft creation

## Production Considerations

- Script storage per campaign grows with versions — set a maximum version retention (e.g., 50 versions, then archive oldest)
- Canary deployments need careful monitoring — auto-rollback if conversion drops by >10% in canary group
- Approval workflow should include automated validation — check for required compliance disclosures, missing tokens, excessive length
- Script diffs for long scripts with minor changes can be noisy — consider semantic diffing (paragraph-level instead of line-level)
- Rollback should be available within one click with automatic creation of the reversion version
- Script versions should be cached at the campaign level for fast call-time access
- Version API endpoints should support programmatic management for CI/CD pipeline integration
- Author attribution is important for compliance — require authentication for all version changes
- Test script version switchover time — switching from version 1.0 to 2.0 should not cause call setup delays
- Correlate script versions with campaign analytics to measure the impact of script changes on performance
