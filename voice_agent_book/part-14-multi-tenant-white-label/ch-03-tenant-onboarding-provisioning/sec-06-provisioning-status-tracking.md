# Section 06: Provisioning Status Tracking

## Overview

Provisioning status tracking provides real-time visibility into the tenant provisioning process for both the end user (during signup) and operations teams (for monitoring and debugging). The status is communicated through a progress indicator in the signup flow, an admin dashboard for support teams, and API endpoints for automation. Each provisioning step transitions through defined states, with timestamps and error details for troubleshooting.

The tenant provisioning state machine includes: `pending` (created but not started), `provisioning` (in progress), `active` (fully provisioned), `failed` (provisioning failed, requires intervention), and `degraded` (provisioned but with non-critical failures). Each state tracks which steps have completed, which are in progress, and which have failed.

Provisioning status is persisted in the database and cached in Redis for fast API access. WebSocket events push status updates to the browser in real-time, so the user sees progress without refreshing. The status endpoint is also consumed by automated monitoring systems for SLA tracking.

## Design Decisions

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```typescript
interface ProvisioningState {
  tenantId: string;
  status: TenantStatus;
  steps: StepState[];
  startedAt: Date;
  completedAt?: Date;
  error?: string;
}

interface StepState {
  name: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed' | 'skipped';
  startedAt?: Date;
  completedAt?: Date;
  duration?: number;
  error?: string;
  retryCount: number;
}

class ProvisioningTracker {
  constructor(
    private pool: Pool,
    private redis: Redis,
    private eventBus: EventBus
  ) {}

  async initializeTracking(tenantId: string, steps: string[]): Promise<void> {
    const state: ProvisioningState = {
      tenantId,
      status: 'provisioning',
      steps: steps.map(name => ({
        name,
        status: 'pending',
        retryCount: 0,
      })),
      startedAt: new Date(),
    };

    await this.saveState(state);
    await this.emitStatusUpdate(tenantId, state);
  }

  async startStep(tenantId: string, stepName: string): Promise<void> {
    const state = await this.getState(tenantId);
    const step = state.steps.find(s => s.name === stepName);
    if (!step) throw new Error(`Unknown step: ${stepName}`);

    step.status = 'in_progress';
    step.startedAt = new Date();
    step.retryCount++;
    
    await this.saveState(state);
    await this.emitStatusUpdate(tenantId, state);
  }

  async completeStep(tenantId: string, stepName: string): Promise<void> {
    const state = await this.getState(tenantId);
    const step = state.steps.find(s => s.name === stepName);
    if (!step) return;

    step.status = 'completed';
    step.completedAt = new Date();
    step.duration = step.completedAt.getTime() - step.startedAt!.getTime();

    // Check if all steps complete
    const allComplete = state.steps.every(s => s.status === 'completed');
    if (allComplete) {
      state.status = 'active';
      state.completedAt = new Date();
    }

    await this.saveState(state);
    await this.emitStatusUpdate(tenantId, state);
  }

  async failStep(tenantId: string, stepName: string, error: string): Promise<void> {
    const state = await this.getState(tenantId);
    const step = state.steps.find(s => s.name === stepName);
    if (!step) return;

    step.status = 'failed';
    step.error = error;
    step.completedAt = new Date();
    
    // Determine overall state
    const canRetry = step.retryCount < 3;
    state.status = canRetry ? 'provisioning' : 'failed';
    
    if (!canRetry) {
      state.error = `Step ${stepName} failed after ${step.retryCount} attempts: ${error}`;
    }

    await this.saveState(state);
    await this.emitStatusUpdate(tenantId, state);
  }

  async getProvisioningProgress(tenantId: string): Promise<ProgressResponse> {
    const state = await this.getState(tenantId);
    const completedCount = state.steps.filter(s => s.status === 'completed').length;
    const failedCount = state.steps.filter(s => s.status === 'failed').length;
    
    return {
      status: state.status,
      progress: Math.round((completedCount / state.steps.length) * 100),
      completedSteps: completedCount,
      totalSteps: state.steps.length,
      failedSteps: failedCount,
      currentStep: state.steps.find(s => s.status === 'in_progress')?.name || null,
      error: state.error || null,
      estimatedRemaining: this.estimateRemainingTime(state),
    };
  }

  private async emitStatusUpdate(tenantId: string, state: ProvisioningState): Promise<void> {
    const progress = await this.getProvisioningProgress(tenantId);
    await this.eventBus.publish(`provisioning:${tenantId}`, {
      type: 'provisioning.status',
      tenantId,
      data: progress,
    });
  }

  private async saveState(state: ProvisioningState): Promise<void> {
    await Promise.all([
      this.pool.query(
        `UPDATE tenant_provisioning SET status = $1, state = $2, updated_at = NOW() WHERE tenant_id = $3`,
        [state.status, JSON.stringify(state.steps), state.tenantId]
      ),
      this.redis.setex(
        `provisioning:${state.tenantId}`,
        3600,
        JSON.stringify(state)
      ),
    ]);
  }

  private estimateRemainingTime(state: ProvisioningState): number | null {
    const completedSteps = state.steps.filter(s => s.status === 'completed');
    if (completedSteps.length === 0) return null;
    
    const avgDuration = completedSteps.reduce((sum, s) => sum + (s.duration || 5000), 0) / completedSteps.length;
    const remainingSteps = state.steps.filter(s => s.status === 'pending' || s.status === 'in_progress').length;
    
    return Math.round(avgDuration * remainingSteps);
  }
}

// WebSocket event handler
class ProvisioningWebSocket {
  async handleConnection(ws: WebSocket, tenantId: string): Promise<void> {
    // Subscribe to provisioning updates
    const subscription = await this.eventBus.subscribe(
      `provisioning:${tenantId}`,
      (event) => {
        ws.send(JSON.stringify(event));
      }
    );

    ws.on('close', () => subscription.unsubscribe());
  }
};

// Status display component
function ProvisioningProgress({ tenantId }: { tenantId: string }) {
  const [progress, setProgress] = useState<ProgressResponse | null>(null);
  const socket = useWebSocket(`/ws/provisioning/${tenantId}`);

  useEffect(() => {
    socket.onmessage = (event) => {
      setProgress(JSON.parse(event.data).data);
    };
  }, [socket]);

  if (!progress) return <div>Initializing...</div>;

  return (
    <div className="provisioning-progress">
      <h2>Setting up your workspace</h2>
      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${progress.progress}%` }} />
      </div>
      <div className="steps-list">
        {steps.map(step => (
          <div key={step.name} className={`step ${step.status}`}>
            <StepIcon status={step.status} />
            <span>{formatStepName(step.name)}</span>
            {step.error && <span className="error-message">{step.error}</span>}
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Integration Points

- **Signup/Success Page:** Status display embedded in post-signup redirect page
- **Admin Dashboard:** Full provisioning status view for support team
- **Monitoring/Alerting:** Failed provisioning triggers alerts to operations
- **Analytics:** Provisioning duration metrics feed into operational dashboards
- **API Endpoint:** `GET /api/v1/tenants/:id/provisioning` for external status checks

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **Redis Persistence:** While cached in Redis, always persist provisioning state to PostgreSQL. Redis is for fast reads; PostgreSQL is the source of truth.
- **Stale Provisioning Detection:** Alert on tenants stuck in provisioning state for >30 minutes. This may indicate a worker crash or infrastructure issue.
- **Progress Estimation Accuracy:** Estimated remaining time will be inaccurate for the first few steps. Consider using historical averages from similar tenants for better estimates.
- **User Experience:** Show a positive, encouraging progress screen. Use micro-animations and messages to keep the user engaged during longer provisioning steps.
- **Failure Recovery:** If provisioning fails, present a clear, actionable error message. Offer a "retry" button and a support contact option.
- **Unattended Provisioning:** For API/automated signups, provide a webhook callback when provisioning completes, rather than requiring status polling.
