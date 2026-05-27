# Section 02: Automated Tenant Provisioning Pipeline

## Overview

The automated provisioning pipeline is the engine that transforms a signed-up user into a fully functional tenant environment. It orchestrates infrastructure creation, database setup, default configuration deployment, and initial data seeding. The pipeline must be reliable (tenants should never receive a broken environment), fast (provisioning should complete within seconds for self-service), and scalable (simultaneous provisioning of hundreds of tenants during peak signup).

Provisioning encompasses multiple services: creating tenant records in the registry database, provisioning infrastructure (database schemas, storage buckets, queues), setting up default configurations (feature flags, quota limits, rate limits), creating first admin user accounts and API keys, configuring white-label defaults, and triggering welcome workflows. Each step is independently tracked for progress monitoring and failure recovery.

The pipeline is implemented as an async job queue (BullMQ, RabbitMQ, or Kafka) with idempotent job processing. Each provisioning step is a separate job with retry logic and dead-letter queuing. The tenant record transitions through states: `pending` → `provisioning` → `active` (or `failed`). If any step fails, the pipeline can be retried from the failure point without re-executing completed steps.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Raw Audio|--->| Codec    |--->| Resample |--->| Buffer   |--->| Formatted|
| Opus/PCM |    | Decode   |    | 48->16kHz|    | (ring    |    | 16kHz    |
| 48kHz    |    | (Opus)   |    | (Kaiser) |    |  buf)    |    | mono PCM |
+----------+    +----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```typescript
interface ProvisioningStep {
  name: string;
  order: number;
  timeout: number; // ms
  retryCount: number;
  execute: (tenantId: string, context: ProvisioningContext) => Promise<void>;
  rollback: (tenantId: string, context: ProvisioningContext) => Promise<void>;
}

class ProvisioningPipeline {
  private steps: ProvisioningStep[];
  private queue: Queue;

  constructor() {
    this.queue = new Queue('tenant-provisioning', {
      connection: { host: process.env.REDIS_URL },
      defaultJobOptions: {
        attempts: 3,
        backoff: { type: 'exponential', delay: 2000 },
      },
    });
  }

  async startProvisioning(signupData: SignupData): Promise<string> {
    const tenantId = crypto.randomUUID();

    // Create initial tenant record (synchronous, lightweight)
    await this.createTenantRecord(tenantId, signupData);

    // Enqueue full provisioning pipeline
    await this.queue.add('provision-tenant', {
      tenantId,
      signupData,
      steps: this.steps.map(s => s.name),
    });

    return tenantId;
  }

  async processProvisioningJob(job: Job): Promise<void> {
    const { tenantId, signupData } = job.data;
    const context = new ProvisioningContext(tenantId, signupData);

    await this.updateTenantStatus(tenantId, 'provisioning');

    for (const step of this.steps) {
      try {
        await this.executeWithTimeout(
          step.execute(tenantId, context),
          step.timeout
        );
        await this.recordStepCompletion(tenantId, step.name);
      } catch (error) {
        await this.handleStepFailure(tenantId, step, error, context);
        throw error; // Trigger job retry
      }
    }

    await this.updateTenantStatus(tenantId, 'active');
    await this.triggerWelcome(tenantId, signupData);
  }

  private async executeWithTimeout(
    promise: Promise<void>, 
    timeout: number
  ): Promise<void> {
    const timeoutPromise = new Promise((_, reject) => {
      setTimeout(() => reject(new Error('Step timeout')), timeout);
    });
    return Promise.race([promise, timeoutPromise]);
  }

  private async handleStepFailure(
    tenantId: string,
    step: ProvisioningStep,
    error: Error,
    context: ProvisioningContext
  ): Promise<void> {
    // Attempt rollback for this step
    try {
      await step.rollback(tenantId, context);
    } catch (rollbackError) {
      // Log rollback failure but don't throw
      await this.alertService.send({
        type: 'provisioning_rollback_failed',
        tenantId,
        step: step.name,
        error: rollbackError.message,
      });
    }

    // If retries exhausted, escalate
    if (context.retryCount[step.name] >= step.retryCount) {
      await this.updateTenantStatus(tenantId, 'failed');
      await this.alertService.send({
        type: 'provisioning_failed',
        tenantId,
        step: step.name,
        error: error.message,
        severity: 'high',
      });
    }
  }

  async recoverFailedProvisioning(tenantId: string): Promise<void> {
    const completedSteps = await this.getCompletedSteps(tenantId);
    const failedStep = await this.getFailedStep(tenantId);
    
    // Resume from failed step
    await this.queue.add('provision-tenant', {
      tenantId,
      resumeFrom: failedStep,
    });
  }

  private async createTenantRecord(tenantId: string, data: SignupData): Promise<void> {
    await this.pool.query(`
      INSERT INTO tenants (id, name, slug, tier, status, settings)
      VALUES ($1, $2, $3, $4, 'pending', $5)
    `, [tenantId, data.companyName, data.slug, data.tier, { industry: data.industry }]);

    await this.pool.query(`
      INSERT INTO tenant_config (tenant_id, feature_flags, quotas)
      VALUES ($1, $2, $3)
    `, [tenantId, this.getDefaultFlags(data.tier), this.getDefaultQuotas(data.tier)]);
  }
}

// Example provisioning step: Database
class DatabaseProvisioningStep implements ProvisioningStep {
  name = 'database';
  order = 2;
  timeout = 30000;
  retryCount = 3;

  async execute(tenantId: string, context: ProvisioningContext): Promise<void> {
    const tier = context.signupData.tier;
    
    if (tier === 'starter') {
      // Shared model - create schema with RLS
      await context.pool.query(`
        INSERT INTO tenant_registry (tenant_id, schema_name, tier)
        VALUES ($1, 'tenant_${tenantId.slice(0, 12)}', $2)
      `, [tenantId, tier]);
      
      // Run baseline migrations
      await this.runMigrations(context.pool, tenantId, tier);
    } else if (tier === 'enterprise') {
      // Dedicated - provision via Terraform
      await this.provisionDedicatedDB(tenantId, context);
    }
  }

  async rollback(tenantId: string, context: ProvisioningContext): Promise<void> {
    await context.pool.query('DELETE FROM tenant_registry WHERE tenant_id = $1', [tenantId]);
  }
}
```

## Integration Points

- **Signup Flow (Sec 01):** Triggers provisioning after signup completion
- **Infrastructure-as-Code:** Terraform/Pulumi for database and storage provisioning
- **Database Migration System:** Runs baseline migrations during provisioning
- **Feature Flag Service:** Sets per-tenant feature flags based on plan
- **Welcome Automation:** Triggers email sequence and in-app onboarding

## Open-Source Tools

- **SoX** (GPL 2.0): Audio processing
- **node-opus** (MIT): Opus codec
- **lame** (LGPL): MP3 encoding
## Production Considerations

- **Provisioning Storm:** Plan for sudden signup spikes (product launch, viral marketing). The provisioning pipeline must handle 100+ concurrent signups. Use queue backpressure and horizontal scaling for the provisioning workers.
- **Idempotency at Step Level:** Each step must handle partial execution. Use database upserts, idempotency keys, and state checks to ensure retries don't cause duplicate work.
- **Provisioning Timeouts:** Some steps (like creating an RDS instance) can take 10+ minutes. Use long-running job patterns with asynchronous completion callbacks (e.g., wait for RDS to be available via polling or event bridge).
- **Cost Management:** Dedicated database provisioning for enterprise tenants should include cost estimates and approval gates. Don't auto-provision expensive resources without budget verification.
- **Monitoring:** Track provisioning duration per step, per tier. Alert on steps exceeding p95 duration. Monitor provisioning queue depth.
- **Manual Recovery Tools:** Build admin tools for recovering failed provisioning: retry specific steps, reset tenant status, manually complete provisioning with audit trail.
- **Provisioning Parallelism:** Steps that are independent (database + storage bucket can be parallelized). Dependent steps (must have tenant record before creating admin user) must be sequential.
