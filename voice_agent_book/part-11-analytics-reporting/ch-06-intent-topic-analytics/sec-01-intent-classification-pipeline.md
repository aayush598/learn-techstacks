# Section 01: Intent Classification Pipeline

## Overview

The intent classification pipeline processes call transcriptions to identify the customer's underlying intent — the reason they called and what they want to accomplish. Intent classification enables contact centers to understand caller needs at scale, track intent distribution over time, detect emerging intent patterns, and optimize IVR routing and agent training based on intent-driven insights. Intents are hierarchical: broad categories (e.g., "Billing Inquiry") with sub-intents (e.g., "Invoice Question," "Payment Issue," "Refund Request").

The pipeline uses a combination of approaches: rule-based matching for high-confidence known patterns (e.g., "I want to pay my bill"), ML-based classification for ambiguous or novel expressions, and clustering for discovering new intents. Each call can have multiple intents (a customer may call about both billing and technical support), and each intent is associated with the relevant transcription segments. The pipeline processes calls in near-real-time (within 60 seconds of call completion) and writes results to ClickHouse for analytics.

## Architecture

```
           Intent Classification Pipeline

   Transcriptions → Intent Classifier
                        |
            ┌───────────┴───────────┐
            |                       |
      Rule-Based           ML Classifier
      Matcher              (fine-tuned BERT
      (regex,              or fastText)
       keywords)
            |                       |
      Unified Intent Output
      (hierarchical, multi-label)
            |
      ClickHouse (intent_events)
            |
      Intent Analytics Dashboard
      (distribution, trends, routing)
```

## Design Decisions

- **Hybrid rule-based + ML classification over pure ML:** Rule-based matching provides deterministic, explainable classifications for common intents with well-defined language patterns (e.g., "track my order," "reset password"). ML classification handles the long tail of natural language variations. The hybrid approach runs rules first (fast, O(1) lookup), and only invokes the ML model for calls that don't match any rule with high confidence. This reduces ML inference cost by 40-60%. Trade-off: maintaining the rule set requires ongoing effort as language patterns evolve; rules have no confidence score so false positives are harder to detect.

- **Multi-label classification over single-label:** A single call often covers multiple intents ("I need to change my address and also I have a question about my last bill"). Multi-label classification assigns 0 or more intents to each call/segment, with confidence scores for each. The dashboard shows the primary intent (highest confidence) and secondary intents. Trade-off: multi-label training requires more annotated data (each segment labeled with all applicable intents), increasing annotation cost by ~2x.

- **Hierarchical intents with configurable taxonomy over flat intent list:** Intents are organized in a 2-3 level hierarchy: L1 (e.g., "Billing"), L2 (e.g., "Payment"), L3 (e.g., "Late Payment Fee Dispute"). The taxonomy is tenant-configurable — an ecommerce tenant might have "Shipping Questions" while a healthcare tenant has "Appointment Scheduling." The classifier is trained on L2/L3 intents, and L1 is derived from the parent mapping. This allows tenants to define their own granularity while reusing the base ML model. Trade-off: hierarchical classification requires the ML model to output at the lowest level (more classes = harder problem); the parent mapping must be maintained as the taxonomy evolves.

## Implementation Approach

```typescript
interface IntentDefinition {
  id: string;
  name: string;
  level: number;
  parentId?: string;
  tenantId: string;
  keywords: string[];              // for rule-based matching
  trainingPhrases: string[];       // for ML training
  enabled: boolean;
  createdAt: number;
}

interface IntentClassification {
  callSid: string;
  tenantId: string;
  segmentIndex?: number;           // null for call-level
  intents: Array<{
    intentId: string;
    intentName: string;
    level: number;
    parentIntentId?: string;
    parentIntentName?: string;
    confidence: number;
    classificationMethod: 'rule' | 'ml' | 'cluster';
  }>;
  processingTimeMs: number;
  timestamp: number;
}

interface IntentHierarchy {
  rootId: string;
  rootName: string;
  children: Array<{
    id: string;
    name: string;
    children?: Array<{ id: string; name: string }>;
  }>;
}

class IntentClassifier {
  private rules: Map<string, Array<{ pattern: RegExp; intentId: string }>> = new Map();
  private mlModel: MlInferenceClient;
  private clickhouse: ClickHouseClient;
  private intentDefs: Map<string, IntentDefinition> = new Map();

  async classify(transcription: string, callSid: string, tenantId: string): Promise<IntentClassification> {
    const startTime = Date.now();
    const intents: IntentClassification['intents'] = [];
    const matchedIntentIds = new Set<string>();

    // Step 1: Rule-based matching
    const tenantRules = this.rules.get(tenantId) ?? [];
    for (const rule of tenantRules) {
      const matches = transcription.match(rule.pattern);
      if (matches) {
        const def = this.intentDefs.get(rule.intentId);
        if (def && !matchedIntentIds.has(rule.intentId)) {
          intents.push({
            intentId: rule.intentId,
            intentName: def.name,
            level: def.level,
            parentIntentId: def.parentId,
            parentIntentName: def.parentId ? this.intentDefs.get(def.parentId)?.name : undefined,
            confidence: 1.0,
            classificationMethod: 'rule',
          });
          matchedIntentIds.add(rule.intentId);
        }
      }
    }

    // Step 2: ML classification for high-confidence rules that didn't match
    const mlRequired = Array.from(this.intentDefs.values())
      .filter(d => d.tenantId === tenantId && d.enabled && !matchedIntentIds.has(d.id));

    if (mlRequired.length > 0) {
      const mlResults = await this.mlModel.classify({
        text: transcription,
        candidateIntents: mlRequired.map(d => ({
          id: d.id,
          name: d.name,
          trainingPhrases: d.trainingPhrases,
        })),
      });

      for (const result of mlResults) {
        if (result.confidence >= 0.5 && !matchedIntentIds.has(result.intentId)) {
          const def = this.intentDefs.get(result.intentId);
          intents.push({
            intentId: result.intentId,
            intentName: result.intentName,
            level: def?.level ?? 2,
            parentIntentId: def?.parentId,
            parentIntentName: def?.parentId ? this.intentDefs.get(def.parentId)?.name : undefined,
            confidence: result.confidence,
            classificationMethod: 'ml',
          });
          matchedIntentIds.add(result.intentId);
        }
      }
    }

    const classification: IntentClassification = {
      callSid,
      tenantId,
      intents: intents.sort((a, b) => b.confidence - a.confidence),
      processingTimeMs: Date.now() - startTime,
      timestamp: Date.now(),
    };

    // Store in ClickHouse
    await this.clickhouse.insert('call_intents', classification);

    return classification;
  }

  async classifyBatch(
    transcriptions: Array<{ text: string; callSid: string; tenantId: string }>
  ): Promise<IntentClassification[]> {
    // Batch processing for post-call analysis
    const batchSize = 50;
    const results: IntentClassification[] = [];

    for (let i = 0; i < transcriptions.length; i += batchSize) {
      const batch = transcriptions.slice(i, i + batchSize);
      const batchResults = await Promise.all(
        batch.map(t => this.classify(t.text, t.callSid, t.tenantId))
      );
      results.push(...batchResults);
    }

    return results;
  }

  async loadIntentDefinitions(tenantId: string): Promise<void> {
    const defs = await this.clickhouse.query(`
      SELECT * FROM intent_definitions
      WHERE tenantId = '${tenantId}' AND enabled = 1
    `);

    for (const def of defs) {
      this.intentDefs.set(def.id, def);

      // Build rules
      if (def.keywords && def.keywords.length > 0) {
        const pattern = new RegExp(def.keywords.join('|'), 'gi');
        if (!this.rules.has(tenantId)) this.rules.set(tenantId, []);
        this.rules.get(tenantId)!.push({ pattern, intentId: def.id });
      }
    }
  }

  async getIntentHierarchy(tenantId: string): Promise<IntentHierarchy[]> {
    const defs = Array.from(this.intentDefs.values())
      .filter(d => d.tenantId === tenantId && d.enabled);

    // Build hierarchy tree
    const roots = defs.filter(d => d.level === 1);
    return roots.map(root => ({
      rootId: root.id,
      rootName: root.name,
      children: defs
        .filter(d => d.parentId === root.id && d.level === 2)
        .map(l2 => ({
          id: l2.id,
          name: l2.name,
          children: defs
            .filter(d => d.parentId === l2.id && d.level === 3)
            .map(l3 => ({ id: l3.id, name: l3.name })),
        })),
    }));
  }

  // Discover new intents via clustering
  async discoverNewIntents(
    tenantId: string,
    unclassifiedTranscriptions: string[]
  ): Promise<Array<{ label: string; phrases: string[]; clusterSize: number }>> {
    // This would use BERTopic or similar clustering
    // Simplified: extract common n-grams and group by similarity
    return [];
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Hugging Face Transformers (Apache 2.0) | Server | BERT-based intent classifier |
| fastText (MIT) | Server | Lightweight text classifier |
| scikit-learn (BSD-3) | Server | Clustering for intent discovery |
| ClickHouse (Apache 2.0) | Server | Intent event storage |

## Production Considerations

**Scaling:** The rule-based matcher runs in-process and handles 10,000 calls/second on a single CPU core. The ML model runs on GPU (1 instance handles ~50 calls/second). For higher throughput, deploy multiple ML model replicas behind a load balancer and batch inference requests. Intent definitions are cached in memory and refreshed every 5 minutes from ClickHouse. New intent discovery (clustering) runs nightly on the previous day's unclassified calls.

**Security:** Intent definitions are tenant-scoped — each tenant has their own intent taxonomy. The ML model is trained on per-tenant data and should not be shared across tenants (to avoid data leakage). Intent classifications are stored with call SID and tenant ID — access requires the `analytics:view` permission. Intent discovery results may contain raw transcription snippets — ensure these are masked or excluded from tenant-shared views.

**Monitoring:** Track intent classification coverage (percentage of calls with at least one intent), ML model confidence distribution, rule match rate, and classification latency. Alert if classification coverage drops below 60% (indicates model drift or taxonomy gaps). Monitor the unclassified call rate — if > 30% of calls have no intent match, trigger new intent discovery.
