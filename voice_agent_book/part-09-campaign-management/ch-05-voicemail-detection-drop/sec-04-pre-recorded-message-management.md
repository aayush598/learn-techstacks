# Section 04: Pre-Recorded Message Management

## Overview

Pre-recorded message management handles the creation, storage, organization, and deployment of voice messages used for voicemail drops. A campaign may have multiple messages for different segments, A/B test variants, languages, and outcomes. The management system provides a complete workflow — from recording or text-to-speech generation, through approval, to campaign deployment and performance tracking.

Messages can be created via professional recording (highest quality), text-to-speech generation (fastest turnaround), or synthesized from the AI agent's voice (brand consistency). Each message is stored as an audio file with metadata including duration, language, tone, and performance metrics. The system supports message versioning, A/B testing, and dynamic content injection (personalization within messages).

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
class MessageManager {
  constructor(storage, ttsService, audioProcessor) {
    this.storage = storage; // MinIO/S3
    this.tts = ttsService;
    this.processor = audioProcessor;
  }

  async createMessage(data) {
    let audioRef;

    if (data.source === 'upload') {
      audioRef = await this.processUpload(data.file);
    } else if (data.source === 'tts') {
      audioRef = await this.generateTTS(data.text, data.voice, data.language);
    } else if (data.source === 'ai_clone') {
      audioRef = await this.cloneFromAgent(data.agentId, data.text);
    }

    // Process the audio
    const processedAudio = await this.processor.process(audioRef);

    // Store
    const message = await this.prisma.voicemailMessage.create({
      data: {
        campaign_id: data.campaignId,
        name: data.name,
        source: data.source,
        language: data.language,
        duration_ms: processedAudio.durationMs,
        audio_ref: processedAudio.key,
        transcript: processedAudio.transcript,
        text_content: data.text || null,
        tts_voice: data.voice || null,
        tags: data.tags || [],
        status: 'active',
        version: 1
      }
    });

    return message;
  }

  async generateTTS(text, voice, language) {
    const ttsResult = await this.tts.synthesize({
      text,
      voice,
      language,
      format: 'wav',
      sampleRate: 8000 // Telephony quality
    });

    const key = `messages/${ttsResult.id}.wav`;
    await this.storage.put(key, ttsResult.audio);

    return { key, duration: ttsResult.duration };
  }

  async selectMessage(contact, campaign, context) {
    // Find best message for this contact and context
    const candidates = await this.prisma.voicemailMessage.findMany({
      where: {
        campaign_id: campaign.id,
        status: 'active',
        language: contact.language || campaign.language
      }
    });

    // Score messages by relevance
    const scored = candidates.map(msg => ({
      ...msg,
      score: this.calculateRelevanceScore(msg, contact, context)
    }));

    scored.sort((a, b) => b.score - a.score);
    return scored[0] || null;
  }

  calculateRelevanceScore(message, contact, context) {
    let score = 0;

    // Prefer messages in the contact's language
    if (message.language === contact.language) score += 10;

    // Prefer messages tagged for this campaign type
    if (message.tags.includes(context.campaignType)) score += 5;

    // Boost A/B test winning messages
    if (message.isWinningVariant) score += 3;

    // Penalize messages with high opt-out rates
    score -= (message.optOutRate || 0) * 10;

    // Penalize very long messages (contact may not listen)
    if (message.duration_ms > 30000) score -= 5;
    if (message.duration_ms > 45000) score -= 10;

    return score;
  }

  async createMessageVariant(originalId, variantData) {
    const original = await this.prisma.voicemailMessage.findUnique({
      where: { id: originalId }
    });

    const variant = await this.createMessage({
      ...variantData,
      campaignId: original.campaign_id
    });

    // Link as variant for A/B testing
    await this.prisma.messageVariant.create({
      data: {
        original_id: originalId,
        variant_id: variant.id,
        test_status: 'pending'
      }
    });

    return variant;
  }

  async getMessagePerformance(messageId, dateRange) {
    const attempts = await this.prisma.callAttempt.findMany({
      where: {
        voicemail_message_id: messageId,
        timestamp: { gte: dateRange.start, lte: dateRange.end }
      }
    });

    const total = attempts.length;
    const callbacks = attempts.filter(a => a.outcome === 'callback').length;
    const optOuts = attempts.filter(a => a.disposition === 'opted_out').length;
    const played = attempts.filter(a => a.voicemail_played).length;

    return {
      totalDeliveries: total,
      callbackRate: total > 0 ? callbacks / total : 0,
      optOutRate: total > 0 ? optOuts / total : 0,
      completionRate: total > 0 ? played / total : 0
    };
  }
}
```

## Integration Points

- **Voicemail Drop Engine (sec-03):** Selects and plays messages during voicemail drops
- **TTS Service:** Generates messages from text with configurable voice and language
- **AI Agent (Part 06):** Provides voice cloning for brand-consistent synthesized messages
- **Campaign Configuration (Ch 01):** Message assignment per campaign and segment
- **A/B Testing (Ch 10):** Message variant testing and winner selection
- **Analytics (Ch 09):** Message performance tracking and reporting
- **Compliance (Ch 07):** Message content must include required disclosures

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- TTS-generated messages should be reviewed before deployment — TTS can mispronounce names, numbers, and uncommon words
- Studio recordings provide 15-20% higher callback rates than TTS — use for high-value campaigns
- Message storage for audio files requires significantly more space than text — plan S3/MinIO capacity
- Audio processing (normalization, format conversion) should be automated in a pipeline triggered on upload
- Messages must include the business name and purpose per TCPA requirements — validate during upload
- Personalization in messages (e.g., "Hi John") requires dynamic assembly at call time, adding latency
- CDN caching of frequently used messages reduces playback latency for voicemail drops
- Monitor message performance by segment — a message that works for residential may not work for business
- Implement content moderation for TTS-generated messages to prevent inappropriate content
- Message versions should be immutable once deployed to a campaign to ensure reproducibility
