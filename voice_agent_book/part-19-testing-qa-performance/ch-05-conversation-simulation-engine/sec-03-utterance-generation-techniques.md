# Section 03: Utterance Generation Techniques

## Overview

Utterance generation creates realistic user speech inputs for conversation simulations. The generator produces varied phrasings of the same intent to test that the agent correctly understands different ways users express themselves. Generation techniques range from template-based substitution (simple) to LLM-generated variations (complex, realistic).

A good utterance generator produces linguistically diverse inputs that cover the full spectrum of how real users might express an intent. This includes variations in vocabulary, sentence structure, filler words, accents (via phonetic hints), and even common mistakes like grammar errors or background noise.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Audio    |--->| WebSocket|--->| Jitter   |--->| PLC      |--->| Player   |
| Producer |    | (WSS)    |    | Buffer   |    | (Packet  |    | (smooth  |
| (100ms   |    | (binary) |    | (adaptive|    |  Loss    |    |  output) |
|  chunks) |    |          |    |  60-200) |    |  Conceal)|    +----------+
+----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```typescript
class UtteranceGenerator {
  private templates: Map<string, Template[]> = new Map();
  private synonyms: Map<string, string[]> = new Map();

  constructor(
    private llm?: LLMClient,
    private config: GeneratorConfig = {}
  ) {
    this.loadTemplates();
    this.loadSynonyms();
  }

  async generate(intent: string, options: GenerationOptions = {}): Promise<Utterance[]> {
    const utterances: Utterance[] = [];

    // 1. Template-based (fast, deterministic)
    const templates = this.templates.get(intent) || [];
    for (const template of templates.slice(0, options.maxTemplates || 5)) {
      utterances.push(this.expandTemplate(template, options));
    }

    // 2. Variation (rule-based transformations)
    const variations = this.generateVariations(utterances, options.variationCount || 3);
    utterances.push(...variations);

    // 3. LLM-enhanced (optional, high variety)
    if (this.llm && options.useLLM) {
      const llmUtterances = await this.generateWithLLM(intent, options.llmCount || 5);
      utterances.push(...llmUtterances);
    }

    return utterances;
  }

  private expandTemplate(template: Template, options: GenerationOptions): Utterance {
    let text = template.text;
    
    // Substitute synonyms
    for (const [key, values] of this.synonyms) {
      if (text.includes(`{${key}}`)) {
        const synonym = options.seededRandom
          ? values[this.hash(text) % values.length]
          : faker.helpers.arrayElement(values);
        text = text.replace(`{${key}}`, synonym);
      }
    }

    // Apply random filler
    if (options.includeFillers && Math.random() > 0.5) {
      const filler = faker.helpers.arrayElement([
        'um', 'uh', 'like', 'you know', 'well', 'so',
      ]);
      text = `${filler}, ${text.toLowerCase()}`;
    }

    return { text, intent: template.intent };
  }

  private async generateWithLLM(intent: string, count: number): Promise<Utterance[]> {
    const prompt = `Generate ${count} natural ways a customer might express the intent "${intent}" when calling customer support. Return a JSON array of strings.`;
    
    const response = await this.llm!.complete(prompt);
    return JSON.parse(response).map((text: string) => ({ text, intent }));
  }
}
```

## Integration Points

- **Simulation Engine**: Utterances fed into conversation simulation
- **Intent Testing**: Generated utterances validate intent classification
- **Edge Case Discovery**: LLM-generated utterances find unexpected phrasings
- **Localization**: Utterance generation supports multiple languages
- **Quality Metrics**: Utterance diversity measured and tracked

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- **Generation Cost**: LLM generation costs scale with variety; use templates for baseline
- **Content Quality**: Validate utterances are appropriate and non-toxic
- **Deterministic Reproducibility**: Seed-based generation for reproducible test suites
- **Language Support**: Utterance generation must support all platform languages
- **Performance**: Pre-generate utterance sets for common flows to improve simulation speed
