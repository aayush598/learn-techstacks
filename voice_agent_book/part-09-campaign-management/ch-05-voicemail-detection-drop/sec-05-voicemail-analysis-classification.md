# Section 05: Voicemail Analysis & Classification

## Overview

Voicemail analysis goes beyond simple detection (machine vs. human) to extract insights from the voicemail greeting itself. By analyzing the greeting content, the system can determine whether it's a personal mailbox, a business line, a disconnected number, or a fax line. This classification enables more intelligent routing — a business line greeting might warrant different handling than a residential one, while a disconnected number should trigger immediate suppression.

The voicemail analysis engine uses speech-to-text transcription of the greeting combined with acoustic analysis to classify the mailbox type and extract useful metadata. It can detect out-of-office messages, full mailbox indicators, language preference, and whether the mailbox is set up at all. This information feeds back into campaign optimization, contact list management, and compliance workflows.

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

```
class VoicemailAnalyzer {
  constructor(sttService, classifier) {
    this.stt = sttService;
    this.classifier = classifier;
    this.keywords = {
      disconnected: [
        'disconnected', 'not in service', 'no longer', 'has been changed',
        'has been disconnected', 'is not available', 'incorrect number'
      ],
      full_mailbox: [
        'mailbox is full', 'unable to accept', 'cannot accept',
        'is full', 'storage is full'
      ],
      out_of_office: [
        'out of the office', 'out of office', 'on vacation', 'on leave',
        'will return', 'back on', 'will be back', 'out until'
      ],
      business: [
        'thank you for calling', 'welcome to', 'you have reached',
        'please hold', 'press 1 for', 'for sales'
      ],
      unconfigured: [
        'has not been set up', 'not yet set up', 'not been configured',
        'temporarily unavailable'
      ],
      no_greeting_keywords: [
        'leave a message', 'please leave a', 'record your name'
      ]
    };
  }

  async analyze(greetingAudio, language) {
    // Transcribe
    const transcription = await this.stt.transcribe(greetingAudio, {
      language: language || null, // Auto-detect if not specified
      model: 'whisper-1',
      responseFormat: 'verbose_json'
    });

    // Parallel classification
    const [keywordResult, mlResult, acousticResult] = await Promise.all([
      this.keywordClassify(transcription.text),
      transcription.text ? this.mlClassify(transcription.text) : Promise.resolve(null),
      this.acousticClassify(greetingAudio)
    ]);

    // Ensemble decision
    const classification = this.ensembleDecision(
      keywordResult, mlResult, acousticResult
    );

    return {
      classification: classification.category,
      confidence: classification.confidence,
      transcription: transcription.text,
      language: transcription.language,
      durationMs: this.getDuration(greetingAudio),
      acoustic: acousticResult,
      actions: this.getRecommendedActions(classification.category)
    };
  }

  keywordClassify(text) {
    if (!text) return { category: 'no_greeting', confidence: 0.9 };

    const lowerText = text.toLowerCase();
    const scores = {};

    for (const [category, keywords] of Object.entries(this.keywords)) {
      let matchCount = 0;
      for (const keyword of keywords) {
        if (lowerText.includes(keyword)) {
          matchCount++;
        }
      }
      if (matchCount > 0) {
        scores[category] = Math.min(1.0, matchCount / keywords.length * 2);
      }
    }

    // Find best matching category
    const entries = Object.entries(scores);
    if (entries.length === 0) return { category: 'personal', confidence: 0.4 };

    entries.sort((a, b) => b[1] - a[1]);
    
    return {
      category: entries[0][0],
      confidence: entries[0][1],
      allScores: scores
    };
  }

  async mlClassify(text) {
    // Use ML classifier for nuanced categorization
    const result = await this.classifier.classify(text, [
      'personal', 'business', 'out_of_office', 'full_mailbox',
      'disconnected', 'unconfigured', 'fax', 'other'
    ]);

    return {
      category: result.category,
      confidence: result.confidence,
      probabilities: result.probabilities
    };
  }

  acousticClassify(audioData) {
    const features = this.extractAcousticFeatures(audioData);
    
    // Fax/modem detection
    if (this.detectFaxTone(features)) {
      return { category: 'fax', confidence: 0.95, features };
    }

    // No speech detected
    if (!features.hasSpeech) {
      return { category: 'silence', confidence: 0.7, features };
    }

    // Very short greeting
    if (features.voiceDurationMs < 1000) {
      return { category: 'minimal_greeting', confidence: 0.5, features };
    }

    return { category: null, confidence: 0, features };
  }

  ensembleDecision(keywordResult, mlResult, acousticResult) {
    // Acoustic takes priority for fax/silence
    if (acousticResult.category && acousticResult.confidence > 0.8) {
      return { category: acousticResult.category, confidence: acousticResult.confidence };
    }

    // If keyword classification is confident, use it
    if (keywordResult.confidence > 0.7) {
      return { category: keywordResult.category, confidence: keywordResult.confidence };
    }

    // If ML is available and confident, use it
    if (mlResult && mlResult.confidence > 0.6) {
      return { category: mlResult.category, confidence: mlResult.confidence };
    }

    // Low confidence — default to personal
    return { category: 'personal', confidence: keywordResult.confidence * 0.5 };
  }

  getRecommendedActions(category) {
    const actions = {
      'disconnected': [
        { type: 'suppress_contact', priority: 'immediate' },
        { type: 'flag_list_quality', priority: 'high' }
      ],
      'full_mailbox': [
        { type: 'reduce_retry_frequency', priority: 'medium' },
        { type: 'retry_in_7_days', priority: 'medium' }
      ],
      'out_of_office': [
        { type: 'extract_return_date', priority: 'high' },
        { type: 'schedule_retry_after_return', priority: 'medium' }
      ],
      'business': [
        { type: 'tag_as_business_line', priority: 'medium' },
        { type: 'adjust_calling_window', priority: 'medium' }
      ],
      'unconfigured': [
        { type: 'try_alternate_contact_method', priority: 'medium' }
      ],
      'personal': [
        { type: 'standard_retry', priority: 'normal' }
      ],
      'fax': [
        { type: 'suppress_contact', priority: 'immediate' }
      ]
    };

    return actions[category] || [{ type: 'standard_retry', priority: 'normal' }];
  }
}
```

## Integration Points

- **AMD Engine (sec-01, sec-02):** Provides the greeting audio after machine classification
- **STT Service (Part 12):** Speech-to-text for greeting transcription
- **Contact Suppression (Ch 02, sec-06):** Disconnected/fax classifications trigger suppression
- **Contact Data Enrichment (Ch 02, sec-07):** Language, business type enrichments
- **Retry Engine (Ch 04):** Full mailbox, OOO classifications adjust retry strategy
- **Compliance (Ch 07):** Disconnected detection helps maintain list hygiene
- **Campaign Analytics (Ch 09):** Voicemail type distribution reporting

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Greeting transcription adds latency (1-3 seconds) and cost — determine if the value justifies the overhead
- Not all voicemail systems have greetings — some just play a beep (especially newer mobile systems)
- Language detection is valuable for multilingual campaigns but adds another processing step
- Disconnected detection is high-value — it prevents future wasted dials and improves list quality
- Full mailbox detection should trigger a longer retry interval — the mailbox may be cleared later
- Fax/modem detection is important — dialing fax lines wastes money and annoys businesses
- Out-of-office detection with return date extraction is valuable but NLP-dependent
- Voicemail analysis results should be cached per contact to avoid re-analysis on subsequent calls
- Classification accuracy should be monitored — incorrect classifications can lead to wrong actions
- Consider a human review queue for low-confidence voicemail classifications to train the model
