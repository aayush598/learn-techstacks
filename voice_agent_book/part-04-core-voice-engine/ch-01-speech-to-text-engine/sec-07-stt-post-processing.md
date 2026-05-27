# Section 07: STT Post-Processing

## Overview

Raw STT output is typically all lowercase, lacks punctuation, and contains disfluencies ("um", "uh", false starts). Post-processing transforms raw transcripts into clean, readable text suitable for LLM consumption and human review. The pipeline applies punctuation restoration, capitalization, profanity filtering, and domain-specific formatting.

The post-processor is a configurable pipeline where tenants can enable/disable stages and set formatting rules. It runs asynchronously on finalized utterances and adds minimal latency (~20ms per utterance).

## Architecture

```
Raw Text ──▶ Punctuation ──▶ Capitalization ──▶ Profanity ──▶ Formatting ──▶ Clean Text
(no punct,   Restoration    (True/Title     Filter       (numbers,       (ready for
 all lower)   (BERT/DL      Case)          (blocklist    dates,           LLM)
              model)                         + regex)     phones)
```

## Design Decisions

- **ML-based Punctuation**: BERT-based punctuation restoration model (fine-tuned on conversational data) achieves 95% accuracy vs 80% for regex-based approaches. Latency: ~15ms per utterance.
- **Disfluency Filtering**: Remove filled pauses ("um", "uh", "like"), false starts (repeated words), and backchannel corrections using a lightweight CRF model.
- **Formatting Rules**: Apply tenant-specific formatting: phone numbers → (555) 123-4567, dates → May 15, 2026, currency → $1,234.56.

## Implementation Approach

```typescript
interface PostProcessConfig {
  punctuation: boolean;
  capitalization: 'none' | 'sentence' | 'title';
  profanityFilter: boolean;
  profanityReplacement: string;
  formatting: string[]; // ['phone', 'date', 'currency', 'ssn']
  disfluencyFilter: boolean;
}

class STTPostProcessor {
  private punctModel: PunctuationModel;
  private profanityList: Set<string>;

  async process(rawText: string, config: PostProcessConfig): Promise<string> {
    let text = rawText;

    if (config.disfluencyFilter) {
      text = this.removeDisfluencies(text);
    }
    if (config.punctuation) {
      text = await this.punctModel.restore(text);
    }
    if (config.capitalization === 'sentence') {
      text = this.capitalizeSentences(text);
    }
    if (config.profanityFilter) {
      text = this.filterProfanity(text, config.profanityReplacement);
    }
    text = this.applyFormatting(text, config.formatting);

    return text;
  }

  private removeDisfluencies(text: string): string {
    return text
      .replace(/\b(?:um|uh|er|ah|like)\b/gi, '')
      .replace(/\b(\w+)(?: \1)+\b/g, '$1') // repeated words
      .trim();
  }
}
```

## Integration Points

- **LLM Context**: Clean text reduces token usage by 10-15% compared to raw STT output.
- **Analytics**: Track disfluency rate per caller as a quality metric.
- **Storage**: Post-processed text stored in call records. Raw transcripts stored for debugging.

## Open-Source Tools

- **punctuator** (MIT): LSTM-based punctuation restoration.
- **bad-words** (MIT): Profanity filter with customizable word list.
- **compromise** (MIT): Lightweight NLP for sentence detection.

## Production Considerations

- **Latency Budget**: Post-processing <50ms total. If ML model exceeds 30ms, fall back to regex-based approach.
- **Profanity Edge Cases**: Handle intentional misspellings ("sh!t"), homoglyphs, and Unicode tricks.
- **Tenant Config**: Cache post-processing config per tenant in Redis. Evict on changes.
- **Testing**: Maintain a test suite of 1000 utterances per tenant for post-processing quality regression.

## Additional Production Guidance

### Disfluency Handling Examples
| Input | Output | Technique |
|-------|--------|-----------|
| "I um want to uh order a uh pizza" | "I want to order a pizza" | Regex + ML filter |
| "The the the account number is 1234" | "The account number is 1234" | Repetition detection |
| "So anyway like I was saying" | "I was saying" | Discourse marker removal |

### Performance Benchmarking
| Stage | Latency p50 | Latency p99 | Model |
|-------|-------------|-------------|-------|
| Punctuation restoration | 15ms | 35ms | BERT-tiny |
| Disfluency filtering | 3ms | 8ms | CRF |
| Profanity filtering | 2ms | 5ms | Hash set |
| Formatting | 1ms | 3ms | Regex |

### Tenant Configuration Cache
Post-processing configuration is cached per tenant in Redis (TTL: 60s). Cache key: `pp_config:{tenant_id}`. Cache miss loads from database and populates cache. This configuration includes:
- Enabled/disabled stages
- Profanity replacement string
- Capitalization style
- Formatting rules (phone, date, currency)
- Custom replacement pairs

### Testing & QA
Maintain a regression test suite of 500 utterances per tenant. Run on every configuration change. Key metrics:
- Punctuation F1 score (target: >0.95)
- False positive profanity rate (target: <0.1%)
- Formatting accuracy (target: >99%)

