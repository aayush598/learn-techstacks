# Section 05: Multi-Language STT

## Overview

Multi-language support is critical for a global voice AI platform. The STT system must detect the caller's language (or accept an explicit language configuration per call), route to the appropriate model, and handle code-switching (mixing languages within a conversation). The system supports 30+ languages for primary languages and provides graceful fallback for less common languages.

The multi-language strategy uses language detection on the first utterance, per-call language configuration from the IVR or API, and automatic code-switching detection for bilingual conversations. Language-specific custom vocabulary and post-processing rules are applied.

## Architecture

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Call Init    │───▶│ Language     │───▶│ Model        │───▶│ Post-Process │
│ (IVR/API)    │    │ Detection    │    │ Selection    │    │ (lang-       │
│              │    │ or Config    │    │ (en-US,      │    │  specific)   │
└──────────────┘    └──────────────┘    │ es-ES, ja-JP,│    └──────────────┘
                                        │ etc.)        │
                                        └──────────────┘
                                             │
                                    ┌────────▼────────┐
                                    │  Model Routing   │
                                    │  en → Nova-2    │
                                    │  es → Whisper   │
                                    │  ja → Google    │
                                    │  fallback → en  │
                                    └─────────────────┘
```

## Design Decisions

- **First-Utterance Detection**: Use a lightweight language classifier on the first 3 seconds of speech. If confidence <0.8, default to the tenant's configured language. This avoids delaying the first transcript.
- **Per-Call Configuration**: API callers can specify `language: 'es-MX'` to skip detection. IVR callers can select language via DTMF or voice prompt.
- **Code-Switching**: Detect language changes at utterance boundaries using confidence differential. If consecutive utterances show >0.5 confidence for a different language, switch models mid-call.
- **Model Routing**: Different STT providers have different language strengths. Deepgram Nova-2 excels for English and Spanish. Whisper is stronger for Japanese and Korean. A routing table maps languages to the best provider.

## Implementation Approach

```typescript
interface LanguageConfig {
  supportedLanguages: string[];
  defaultLanguage: string;
  detectionModel: LanguageDetector;
  providerRoutes: Record<string, string>; // language -> provider
}

class MultiLanguageSTT {
  private config: LanguageConfig;
  private currentLang: string;

  async determineLanguage(callInit: CallInit, firstAudio: AudioFrame): Promise<string> {
    if (callInit.language) {
      return this.validateLanguage(callInit.language);
    }
    const detected = await this.config.detectionModel.detect(firstAudio);
    return detected.confidence > 0.8 ? detected.language : this.config.defaultLanguage;
  }

  async handleUtterance(text: string, confidence: number): Promise<void> {
    if (this.shouldSwitchLanguage(text)) {
      const newLang = this.detectLanguageChange(text);
      this.currentLang = newLang;
      console.log('Code-switch detected:', newLang);
    }
  }
}
```

## Integration Points

- **TTS (P4 Ch 02)**: Language detection feeds into TTS voice selection. Spanish caller → Spanish TTS voice.
- **LLM Prompt (P5 Ch 01)**: Detected language is injected as context: "Respond in {language} language."
- **Analytics**: Language distribution metrics track adoption per region.

## Open-Source Tools

- **CLD3** (Apache 2.0): Google's Compact Language Detector v3. Fast, lightweight.
- **Franc** (MIT): Language detection with 400+ languages.
- **Whisper**: Native multi-language support covering 99 languages.

## Production Considerations

- **Model Cache**: Cache loaded STT models per language. LRU eviction with max 5 models per pod. Models not used in 10 minutes are unloaded.
- **Cold Start**: First caller in a language pays model load latency (2-8s). Pre-warm top 5 languages per tenant region.
- **Cost**: Multi-language calls cost more due to model diversity. Track cost per language for ROI analysis.
- **Quality Monitoring**: Track word error rate per language. Alert if any language WER exceeds 20%.
