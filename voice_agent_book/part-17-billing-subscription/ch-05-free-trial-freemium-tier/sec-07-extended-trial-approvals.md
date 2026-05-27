# Section 07: Extended Trial Approvals

## Admin Extended Trial

Authorized admin users can extend trials for specific tenants. Extensions are logged and require justification to prevent abuse. The extension applies to the Stripe subscription trial period.

```typescript
interface TrialExtensionRequest {
  id: string;
  tenantId: string;
  trialId: string;
  requestedBy: string;
  additionalDays: number;
  reason: string;
  status: 'pending' | 'approved' | 'rejected';
  approvedBy?: string;
  approvedAt?: string;
  rejectedReason?: string;
  createdAt: string;
}

class TrialExtensionService {
  async requestExtension(
    tenantId: string,
    additionalDays: number,
    reason: string,
    requestedBy: string
  ): Promise<TrialExtensionRequest> {
    const trial = await this.db.trials.findOne({
      tenantId,
      status: 'active',
    });

    if (!trial) throw new Error('No active trial found');

    // Check max extension limit
    const totalExtensions = await this.db.trialExtensions.countDocuments({
      trialId: trial.id,
    });

    const config = await this.getTrialConfig(trial.planId);
    if (totalExtensions >= config.maxExtensions) {
      throw new Error('Maximum number of trial extensions reached');
    }

    const request: TrialExtensionRequest = {
      id: `ext_req_${nanoid(16)}`,
      tenantId,
      trialId: trial.id,
      requestedBy,
      additionalDays: Math.min(additionalDays, config.maxExtensionDays),
      reason,
      status: 'pending',
      createdAt: new Date().toISOString(),
    };

    await this.db.trialExtensionRequests.create(request);

    // If requester has auto-approve permission, process immediately
    if (await this.hasAutoApprovePermission(requestedBy)) {
      return this.approveExtension(request.id, requestedBy);
    }

    // Notify approvers
    await this.notificationService.sendExtensionApprovalRequest(request);

    return request;
  }

  async approveExtension(
    requestId: string,
    approvedBy: string
  ): Promise<TrialExtensionRequest> {
    const request = await this.db.trialExtensionRequests.findOne({
      id: requestId,
      status: 'pending',
    });

    if (!request) throw new Error('Extension request not found');

    // Apply extension to Stripe subscription
    const trial = await this.db.trials.findOne({ id: request.trialId });
    const currentEnd = new Date(trial.endsAt);
    const newEnd = new Date(
      currentEnd.getTime() + request.additionalDays * 86400000
    );

    await stripe.subscriptions.update(trial.subscriptionId, {
      trial_end: Math.floor(newEnd.getTime() / 1000),
    });

    // Update internal record
    await this.db.trials.updateOne(
      { id: trial.id },
      { $set: { endsAt: newEnd.toISOString() } }
    );

    // Mark request as approved
    await this.db.trialExtensionRequests.updateOne(
      { id: requestId },
      {
        $set: {
          status: 'approved',
          approvedBy,
          approvedAt: new Date().toISOString(),
        },
      }
    );

    // Log extension
    await this.db.trialExtensions.create({
      id: `ext_${nanoid(16)}`,
      trialId: trial.id,
      tenantId: trial.tenantId,
      additionalDays: request.additionalDays,
      newEndDate: newEnd.toISOString(),
      reason: request.reason,
      extendedBy: approvedBy,
      createdAt: new Date().toISOString(),
    });

    // Notify tenant
    await this.notificationService.sendTrialExtended(
      trial.tenantId,
      request.additionalDays,
      newEnd.toISOString()
    );

    return { ...request, status: 'approved', approvedBy, approvedAt: new Date().toISOString() };
  }

  private async hasAutoApprovePermission(userId: string): Promise<boolean> {
    const user = await this.userService.getUser(userId);
    return user.roles.includes('admin') || user.roles.includes('sales_manager');
  }
}
```

## Sales-Led Extension

Sales representatives can extend trials during the evaluation process. This is common in enterprise sales cycles where procurement takes longer than the standard trial period.

```typescript
class SalesExtensionService {
  async salesLedExtension(
    tenantId: string,
    additionalDays: number,
    salesRepId: string,
    opportunityId: string
  ): Promise<void> {
    // Validate sales rep has quota for this extension
    const monthlyBudget = await this.getSalesExtensionBudget(salesRepId);
    const usedBudget = await this.getUsedExtensionDays(salesRepId);

    if (usedBudget + additionalDays > monthlyBudget) {
      throw new Error('Sales extension budget exceeded');
    }

    // Apply extension
    const trial = await this.db.trials.findOne({ tenantId, status: 'active' });
    const currentEnd = new Date(trial.endsAt);
    const newEnd = new Date(
      currentEnd.getTime() + additionalDays * 86400000
    );

    await stripe.subscriptions.update(trial.subscriptionId, {
      trial_end: Math.floor(newEnd.getTime() / 1000),
    });

    await this.db.trials.updateOne(
      { id: trial.id },
      { $set: { endsAt: newEnd.toISOString() } }
    );

    // Track in CRM
    await this.crmService.logActivity(opportunityId, {
      type: 'trial_extension',
      days: additionalDays,
      newExpiry: newEnd.toISOString(),
      salesRepId,
    });
  }

  private async getSalesExtensionBudget(salesRepId: string): Promise<number> {
    // Monthly budget per sales rep
    return 90; // 90 days per month
  }

  private async getUsedExtensionDays(salesRepId: string): Promise<number> {
    const thisMonth = new Date();
    const monthStart = new Date(thisMonth.getFullYear(), thisMonth.getMonth(), 1);

    const extensions = await this.db.trialExtensions.find({
      extendedBy: salesRepId,
      createdAt: { $gte: monthStart.toISOString() },
    }).toArray();

    return extensions.reduce((sum, e) => sum + e.additionalDays, 0);
  }
}
```

## Approval Workflow

Extensions above certain thresholds require multi-level approval. The workflow routes through the appropriate approvers based on the extension duration.

```typescript
interface ApprovalThreshold {
  maxDays: number;
  requiredApprovers: string[];
  autoApproveRoles: string[];
}

const extensionThresholds: ApprovalThreshold[] = [
  { maxDays: 7, requiredApprovers: ['sales_rep'], autoApproveRoles: ['admin', 'sales_manager'] },
  { maxDays: 14, requiredApprovers: ['sales_manager'], autoApproveRoles: ['admin'] },
  { maxDays: 30, requiredApprovers: ['sales_manager', 'finance'], autoApproveRoles: ['admin'] },
  { maxDays: 90, requiredApprovers: ['sales_manager', 'finance', 'ceo'], autoApproveRoles: [] },
];

class ApprovalWorkflowService {
  async routeApproval(request: TrialExtensionRequest): Promise<void> {
    const threshold = extensionThresholds.find(
      t => request.additionalDays <= t.maxDays
    );

    if (!threshold) {
      throw new Error('Extension exceeds maximum allowed days');
    }

    // Check if requester has auto-approve
    const requester = await this.userService.getUser(request.requestedBy);
    const hasAutoApprove = threshold.autoApproveRoles.some(
      role => requester.roles.includes(role)
    );

    if (hasAutoApprove) {
      await this.trialExtensionService.approveExtension(
        request.id,
        request.requestedBy
      );
      return;
    }

    // Route to first approver
    const firstApprover = threshold.requiredApprovers[0];
    await this.notificationService.sendApprovalNotification(
      request,
      firstApprover
    );
  }
}
```

## Open-Source Tools

- **Stripe API** — Trial period updates on subscriptions
- **BullMQ** (MIT) — Schedule extension expiry notifications
- **PostgreSQL** — Extension request tracking and audit log
- **Nodemailer** (MIT) — Approval notification emails

## Integration Points

Extended trial approvals connect to the user management system (role-based approval), the CRM system (sales tracking), the notification service (approval requests), and the Stripe subscription service (trial period updates).

## Production Considerations

- Log all trial extensions for audit and abuse monitoring
- Set monthly extension budgets per sales rep
- Monitor extension-to-conversion ratio (extensions should improve conversion)
- Implement timeouts for approval requests (auto-escalate after 48 hours)
- Review extension patterns for potential abuse

## Open-Source First Philosophy

BullMQ handles extension notification scheduling reliably. PostgreSQL provides the audit trail for all extensions. The approval workflow is built on application-level role-based access control rather than proprietary workflow engines. This open-source approach provides enterprise extension management without workflow automation licensing costs.
