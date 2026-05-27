# Section 07: Activity Logging & History

## Overview

Activity logging captures all voice agent interactions as structured activities within the CRM, creating a complete communication history that sales and service teams can review. Each call generates a CRM activity record containing call metadata (duration, timestamp, direction, disposition), conversation summary (AI-generated or manual), call recording link, sentiment analysis, key topics discussed, and action items. These activity records appear in the CRM's timeline view alongside emails, meetings, and notes, providing a unified customer interaction history.

Activity logging supports multiple CRM activity types depending on the target system: Salesforce Tasks, HubSpot Engagements/Calls, Zoho Calls/Activities, Pipedrive Activities, and generic notes for systems without dedicated call objects. The activity logging system also supports retroactive logging (logging calls that occurred before CRM integration was configured), batch logging (uploading historical call data), and activity enrichment (adding AI-generated call summaries and insights after the fact).

## Architecture

```
                    Activity Logging Architecture

   Call Complete Event
        |
        v
   +------------------+
   | Activity Builder  |
   | • Call metadata   |
   | • Transcription   |
   | • Sentiment       |
   | • Key topics      |
   | • Action items    |
   +------------------+
        |
        v
   +------------------+
   | Activity Queue    |  BullMQ
   | (Ordered by       |
   |  call end time)   |
   +------------------+
        |
        v
   +------------------+
   | CRM Activity      |
   | Writer            |
   | • Adapter routing |
   | • Rate limit      |
   | • Retry handling  |
   +------------------+
        |
        v
   +------------------+
   | CRM Activity      |
   | Record            |
   | (Task/Engagement/ |
   |  Call/Activity)   |
   +------------------+
```

## Design Decisions

- **AI-enriched activity creation over raw call logging:** Each activity record includes AI-generated fields: conversation summary (2-3 sentence summary of the call), key topics extracted (ticket number, product interest, objections), sentiment score, action items identified, and follow-up recommendations. This adds significant value beyond basic call logging. Trade-off: AI enrichment adds latency (5-30 seconds post-call) and cost (LLM API calls).

- **Asynchronous activity logging with queue-based processing:** Activity records are created asynchronously after call completion to avoid impacting call handling latency. The activity queue prioritizes records by CRM type (real-time CRM updates first, batch logging second) and handles rate limiting per CRM. If CRM activity creation fails, the record is retried with exponential backoff. Trade-off: asynchronous processing means activity records appear in CRM with a delay (typically 30 seconds to 5 minutes depending on queue depth).

- **Uniform activity schema across CRMs with adapter-specific mapping:** The platform defines a canonical activity schema (call start/end time, duration, direction, disposition, participants, recording URL, summary, sentiment, topics, action items). Each CRM adapter maps this canonical schema to its system-specific activity format. This enables consistent activity logging while accommodating CRM-specific capabilities. Trade-off: the canonical schema is limited to the common denominator of all CRM activity formats, potentially missing CRM-specific features.

## Implementation Approach

```
interface CallActivity {
  callId: string;
  tenantId: string;
  contactId: string;
  externalContactId?: string;
  externalDealId?: string;
  direction: 'outbound' | 'inbound';
  startTime: number;
  endTime: number;
  duration: number;
  disposition: string;
  agentName: string;
  campaignName?: string;
  recordingUrl?: string;
  transcriptionUrl?: string;
  summary: string;
  sentiment: { overall: number; segments: { text: string; score: number }[] };
  topics: { topic: string; relevance: number }[];
  actionItems: string[];
  customFields: Record<string, string>;
}

class ActivityLogger {
  async logActivity(activity: CallActivity): Promise<void> {
    const enrichedActivity = await this.enrichActivity(activity);
    const job = await this.queue.add('log_activity', enrichedActivity, {
      priority: this.getPriority(activity),
      attempts: 5,
      backoff: { type: 'exponential', delay: 5000 }
    });
    return job.id;
  }

  async enrichActivity(activity: CallActivity): Promise<CallActivity> {
    if (activity.summary && activity.topics.length > 0) return activity;

    const enrichment = await this.aiService.enrichCallActivity({
      callId: activity.callId,
      transcriptionUrl: activity.transcriptionUrl
    });

    return {
      ...activity,
      summary: enrichment.summary || activity.summary,
      topics: enrichment.topics || activity.topics,
      sentiment: enrichment.sentiment || activity.sentiment,
      actionItems: enrichment.actionItems || []
    };
  }

  async processActivityJob(job: Job<CallActivity>): Promise<void> {
    const activity = job.data;
    const integrations = await this.getActiveIntegrations(activity.tenantId);

    for (const integration of integrations) {
      if (!integration.config.enableActivityLogging) continue;

      try {
        const adapter = this.adapterRegistry.get(integration.type);
        await adapter.logCallActivity(
          activity.externalContactId,
          this.buildAdapterCallData(activity, integration)
        );
      } catch (error) {
        if (this.isRetryableError(error)) {
          throw error; // BullMQ will retry
        }
        // Non-retryable: log error and continue
        await this.logPermanentFailure(integration, activity.callId, error);
      }
    }
  }

  private buildAdapterCallData(activity: CallActivity, integration: IntegrationConfig) {
    return {
      subject: `${activity.direction === 'outbound' ? 'Outbound' : 'Inbound'} Call - ${activity.disposition}`,
      duration: activity.duration,
      disposition: activity.disposition,
      recordingUrl: activity.recordingUrl,
      summary: activity.summary,
      agentName: activity.agentName,
      campaignName: activity.campaignName,
      customFields: this.mapCustomFields(activity.customFields, integration.config.fieldMapping)
    };
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| **BullMQ** (MIT) | Queue | Activity processing queue |
| **Redis** (BSD) | Data store | Queue state |
| **OpenAI/Anthropic** (API) | AI | Activity enrichment |

## Production Considerations

**Scaling:** Activity logging volume scales with call volume (potentially 1000+ activities/minute during peak). Ensure the activity queue can handle peak throughput. Batch CRM API calls where possible (multiple activities in a single API request). Use separate queues for different CRM types to prevent a slow CRM from blocking others.

**Security:** Activity records contain PII — call recordings, transcriptions, and summaries. Implement field-level encryption for sensitive fields. Ensure activity enrichment services (AI) are compliant with data processing agreements. Delete activity records when the source call recording is deleted per retention policy. Never log full call transcriptions to CRM summary fields (truncate to key points).

**Monitoring:** Track activity logging throughput (activities/minute), enrichment latency, per-CRM write latency, activity failure rate, and queue depth. Alert on activity queue backlog (> 10 minutes of processing), enrichment failures, and per-CRM write failures exceeding 5%.
