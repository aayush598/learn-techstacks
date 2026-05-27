# Section 07: Failed Provisioning Recovery

## Overview

Failed provisioning is a critical incident that blocks a new tenant from using the platform. Recovery must be swift, reliable, and transparent to the affected user. The recovery system combines automatic retry logic (for transient failures), step-level rollback (for partial failures), manual intervention tools (for complex failures), and user communication (to maintain trust during delays).

Common provisioning failures include: database connection timeouts, cloud API rate limits (AWS/Azure throttling), DNS propagation delays, SSL certificate issuance failures (Let's Encrypt rate limits), and third-party service unavailability (Stripe, SendGrid). Each failure type has specific recovery strategies. Transient failures (network blips, rate limits) are handled by automatic retries with exponential backoff. Persistent failures (configuration errors, permission issues) require manual intervention.

The recovery system maintains a provisioning state machine that supports retry from the point of failure, complete rollback, or manual override. Every recovery action is logged for audit and debugging purposes.

## Design Decisions

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```typescript
class ProvisioningRecovery {
  private retryPolicies: Map<string, RetryPolicy> = new Map([
    ['database', { maxRetries: 3, backoff: [2000, 10000, 30000], timeout: 30000 }],
    ['infrastructure', { maxRetries: 3, backoff: [5000, 30000, 60000], timeout: 120000 }],
    ['dns', { maxRetries: 5, backoff: [10000, 30000, 60000, 120000, 300000], timeout: 600000 }],
    ['network', { maxRetries: 3, backoff: [1000, 5000, 15000], timeout: 10000 }],
  ]);

  async handleProvisioningFailure(
    tenantId: string,
    failedStep: string,
    error: ProvisioningError
  ): Promise<RecoveryAction> {
    // Classify the failure
    const failureType = this.classifyFailure(error);
    const policy = this.retryPolicies.get(failureType) || this.retryPolicies.get('network')!;

    // Check retry count
    const stepState = await this.getStepState(tenantId, failedStep);
    
    if (stepState.retryCount < policy.maxRetries) {
      // Automatic retry
      const delay = policy.backoff[stepState.retryCount];
      await this.scheduleRetry(tenantId, failedStep, delay);
      
      return {
        action: 'retry',
        delay,
        message: `Retrying in ${delay / 1000}s (attempt ${stepState.retryCount + 1}/${policy.maxRetries})`,
      };
    } else {
      // Escalate to manual intervention
      await this.escalateToManual(tenantId, failedStep, error);
      
      return {
        action: 'escalate',
        message: 'Automatic retries exhausted. Escalating to operations team.',
      };
    }
  }

  private classifyFailure(error: ProvisioningError): string {
    if (error.message.includes('timeout') || error.code === 'ETIMEDOUT') return 'database';
    if (error.message.includes('rate limit') || error.code === 429) return 'network';
    if (error.message.includes('DNS') || error.message.includes('dns')) return 'dns';
    if (error.message.includes('provision') || error.message.includes('create')) return 'infrastructure';
    return 'network';
  }

  private async scheduleRetry(tenantId: string, stepName: string, delay: number): Promise<void> {
    await this.queue.add(
      `retry-${stepName}`,
      { tenantId, stepName },
      { delay, attempts: 1 }
    );
  }

  private async escalateToManual(
    tenantId: string,
    failedStep: string,
    error: ProvisioningError
  ): Promise<void> {
    // Create support ticket
    await this.supportService.createTicket({
      tenantId,
      subject: `Provisioning failed: ${failedStep}`,
      priority: 'high',
      description: `Automatic provisioning failed for tenant ${tenantId} at step ${failedStep}. Error: ${error.message}`,
    });

    // Notify operations
    await this.alertService.send({
      type: 'provisioning_failed_manual',
      tenantId,
      step: failedStep,
      error: error.message,
      severity: 'critical',
    });

    // Update tenant status
    await this.updateTenantStatus(tenantId, 'provisioning_failed');
  }

  async manualRecovery(
    tenantId: string,
    action: 'retry_step' | 'retry_all' | 'rollback_and_retry' | 'manual_complete',
    targetStep?: string
  ): Promise<void> {
    switch (action) {
      case 'retry_step':
        await this.retryStep(tenantId, targetStep!);
        break;
      case 'retry_all':
        await this.rollbackAllSteps(tenantId);
        await this.restartProvisioning(tenantId);
        break;
      case 'rollback_and_retry':
        await this.rollbackStep(tenantId, targetStep!);
        await this.retryStep(tenantId, targetStep!);
        break;
      case 'manual_complete':
        await this.markTenantActive(tenantId);
        break;
    }
  }

  private async retryStep(tenantId: string, stepName: string): Promise<void> {
    await this.tracker.startStep(tenantId, stepName);
    const step = this.steps.find(s => s.name === stepName);
    
    try {
      await step!.execute(tenantId, this.createContext(tenantId));
      await this.tracker.completeStep(tenantId, stepName);
      
      // Continue with remaining steps
      await this.continueProvisioning(tenantId);
    } catch (error) {
      await this.tracker.failStep(tenantId, stepName, error.message);
      await this.handleProvisioningFailure(tenantId, stepName, error);
    }
  }

  private async rollbackStep(tenantId: string, stepName: string): Promise<void> {
    const step = this.steps.find(s => s.name === stepName);
    if (step?.rollback) {
      await step.rollback(tenantId, this.createContext(tenantId));
    }
  }

  async emailUserAboutFailure(tenantId: string): Promise<void> {
    const tenant = await this.getTenant(tenantId);
    
    await this.emailService.send({
      to: tenant.adminEmail,
      template: 'provisioning-delayed',
      data: {
        name: tenant.name,
        estimatedResolutionTime: '2 hours',
        supportLink: `https://support.voiceagent.com/tickets/new?tenant=${tenantId}`,
      },
    });

    // Schedule follow-up email
    await this.queue.add(
      'provisioning-followup',
      { tenantId },
      { delay: 4 * 60 * 60 * 1000 } // 4 hours
    );
  }
}
```

## Integration Points

- **Alerting System:** Failed provisioning sends alerts to PagerDuty/Opsgenie
- **Support Ticketing:** Escalated failures create tickets in Zendesk/Intercom
- **Email Notifications:** User notification when provisioning is delayed or recovered
- **Admin Dashboard:** Manual recovery tools available in admin panel
- **Audit Logging:** All retry and recovery actions logged

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **Retry Thundering Herd:** If a cloud provider has an outage, many provisioning attempts will fail simultaneously. Implement jitter in retry delays and consider circuit breakers for dependent services.
- **Partial Provisioning Cleanup:** When failing and retrying, ensure partial resources from the failed attempt are cleaned up. Resource leaks (orphaned databases, storage buckets) accumulate quickly at scale.
- **Manual Recovery Training:** Operations and support teams should have documented runbooks for common provisioning failures. Practice recovery procedures regularly.
- **User Expectation Management:** When provisioning is delayed, over-communicate with the user. Send an email immediately, then updates every 2 hours until resolved. Offer a direct contact for priority support.
- **Monitoring Alerts:** Set up alerts for provisioning failure rates. A sudden spike may indicate a deployment issue or cloud provider outage. P95 provisioning duration should be monitored.
- **Recovery SLA:** Define and track recovery SLA for failed provisioning. For example: "95% of provisioning failures are resolved within 1 hour of detection."
- **Root Cause Analysis:** Track provisioning failure reasons. Common causes should trigger process improvements. Escalate systemic issues (e.g., cloud provider quotas) to platform engineering.
