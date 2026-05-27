# Section 06: Custom Vocabulary & Named Entities

## Overview

Standard STT models fail on domain-specific terms: brand names, technical jargon, product names, acronyms, and proper nouns. For example, "Retell AI" might be transcribed as "retail A.I." and "React Query" as "react quite." Custom vocabulary systems allow tenants to inject domain-specific terms that the ASR model should recognize.

The system supports three mechanisms: (1) hotword/phrase boosting via API parameters, (2) custom vocabulary list submission, and (3) pronunciation dictionaries for phonetic spelling of unusual terms. Each mechanism is configured per-tenant and per-agent.

## Architecture

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Tenant       │───▶│ Vocabulary   │───▶│ ASR Provider │
│ Config UI    │    │ Manager      │    │ (injected    │
│              │    │              │    │  at connect) │
│ - Brand names│    │ - Hotwords   │    └──────────────┘
│ - Products   │    │ - Custom dict│
│ - Acronyms   │    │ - Pronunciat.│
└──────────────┘    └──────────────┘
                          │
                          ▼
                    ┌──────────────┐
                    │  Validation  │
                    │  & Scoring   │
                    │  (WER impact)│
                    └──────────────┘
```

## Design Decisions

- **Hotwords over Custom Model**: Hotword boosting is cheaper and faster than fine-tuning. For most use cases, a well-tuned hotword list achieves 90%+ of fine-tuning accuracy.
- **Phrase Weighting**: Each vocabulary entry has a weight (1-100). Higher weights increase recognition likelihood but may cause false positives. Default weight: 50.
- **Pronunciation Dictionary**: For unusual terms, provide phonetic spelling using ARPAbet notation: "Opencode" → "OW P EH N K OW D". The phoneme sequence guides the acoustic model.

## Implementation Approach

```typescript
interface VocabularyEntry {
  term: string;
  boostWeight: number; // 1-100
  pronunciation?: string; // ARPAbet phonetic spelling
  category: 'brand' | 'product' | 'acronym' | 'jargon';
}

class VocabularyManager {
  private vocabCache: Map<string, VocabularyEntry[]>;

  async getHotwords(tenantId: string): Promise<string[]> {
    const entries = await this.getVocabulary(tenantId);
    return entries.filter(e => e.boostWeight > 50).map(e => e.term);
  }

  async applyToProvider(provider: STTProvider, tenantId: string): Promise<void> {
    const vocab = await this.getVocabulary(tenantId);
    await provider.setVocabulary(vocab.map(v => ({
      text: v.term,
      weight: v.boostWeight,
      pronunciation: v.pronunciation
    })));
  }
}
```

## Integration Points

- **Deepgram**: Uses `keywords` parameter in WebSocket config.
- **Whisper**: Supports `prompt` parameter with hotwords. Self-hosted Whisper.cpp uses `--prompt` flag.
- **Post-Processing**: Regex-based correction pass applies after STT for vocabulary that ASR can't handle.

## Open-Source Tools

- **Deepgram Custom Vocabulary API**: Native keyword boosting.
- **Whisper Prompting**: Use system prompt to bias vocabulary.
- **Natural** (npm): Phonetic matching algorithms.

## Production Considerations

- **Limit**: Max 5000 vocabulary entries per tenant. Each entry adds ~5ms to STT latency.
- **Testing**: WER comparison with/without vocabulary on test set of 100 sample utterances.
- **Update Frequency**: Vocabulary changes propagate within 60 seconds. No need for model retraining.
- **Security**: Vocabulary may contain sensitive business terms. Encrypt at rest (AES-256).

## Additional Production Guidance

### Vocabulary Entry Limits & Performance
| # Entries | Memory | STT Latency Impact | Update Time |
|-----------|--------|-------------------|-------------|
| 100 | 2KB | +1ms | 100ms |
| 1,000 | 20KB | +5ms | 200ms |
| 5,000 | 100KB | +25ms | 600ms |
| 10,000 | 200KB | +50ms | 1.2s (limit) |

### Hotword Testing Protocol
1. Create test set of 100 utterances containing each hotword
2. Run STT with and without vocabulary
3. Compare WER: target improvement >30% for hotwords
4. Monitor false positive rate: should not increase >1%
5. Approve via A/B test (10% traffic for 24h)

### Tenant-Specific Vocabulary Sources
- **CRM Integration**: Import product names, contact names from Salesforce/HubSpot
- **Knowledge Base**: Extract terms from uploaded documentation
- **Call History**: Mine top 100 unrecognized terms from past transcripts
- **Manual Entry**: UI for adding terms with weight and pronunciation

### Privacy & Security
- Vocabulary entries may contain PII (names, account numbers)
- Encrypt at rest (AES-256-GCM)
- Strip from analytics exports by default
- Allow tenants to mark entries as "sensitive" (excluded from logs)

