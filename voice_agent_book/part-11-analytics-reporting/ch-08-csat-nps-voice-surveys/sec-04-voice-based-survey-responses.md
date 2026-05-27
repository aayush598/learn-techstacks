# Section 04: Voice-Based Survey Responses

## Overview

Voice-based survey responses enable customers to complete surveys entirely through the voice channel, either via DTMF keypad entry or speech-to-text natural language responses. This is the most accessible channel for phone-centric customer bases and achieves the highest completion rates (35-50% vs. 10-15% for SMS/email). The voice survey system integrates with the existing IVR flow, playing pre-recorded questions and collecting responses through a configurable question tree.

The system supports two input modes: touch-tone (DTMF) for numeric ratings and yes/no questions, and voice recognition for open-ended feedback and natural language responses. Voice responses are transcribed using real-time speech-to-text and analyzed for sentiment, keywords, and intent. The voice survey engine manages call flow state — including timeouts, retries, and barge-in — and publishes structured response events to Kafka for downstream processing.

## Architecture

```
                 Voice Survey Response Pipeline

   Call Connected → IVR Survey Flow Engine
                         |
              ┌──────────┴──────────┐
              ▼                     ▼
        DTMF Collector       Speech Collector
        (keypad 0-9)         (STT transcription)
              |                     |
              ▼                     ▼
        Input Validator       Transcriber Engine
              |                     |
              └──────────┬──────────┘
                         ▼
                   Response Builder
                         |
              ┌──────────┼──────────┐
              ▼          ▼          ▼
           Kafka     Call Flow   Error Handler
          (event)   (next Q /
                     complete)
```

## Design Decisions

- **Barge-in enabled over prompts-play-fully:** Customers can interrupt the voice prompt with their response rather than waiting for the prompt to finish. This reduces survey duration by 30-40% and improves completion rates for experienced users. Trade-off: barge-in requires voice activity detection (VAD) to distinguish intentional responses from background noise, and early cut-off of the prompt may confuse first-time callers who miss the question context.

- **Hybrid DTMF + speech recognition over single-mode input:** The survey flow accepts both DTMF keypad entry and spoken responses for rating questions. If speech recognition confidence is below 0.8, the system falls back to DTMF. This accommodates users in noisy environments (speech fails, DTMF works) and users with hearing impairments (DTMF preferred). Trade-off: hybrid mode increases IVR flow complexity and requires maintaining two parallel input parsers with different error-handling paths.

- **Real-time transcription with local fallback over cloud-only STT:** Speech responses are transcribed using a local Whisper model for latency-sensitive survey flows (target: under 500 ms transcription latency) with cloud STT as a fallback for complex utterances. Local transcription avoids network dependency for basic survey responses while cloud STT handles open-ended feedback requiring higher accuracy. Trade-off: local models have lower accuracy for accented speech and require GPU resources on the voice server.

## Implementation Approach

```typescript
interface VoiceSurveySession {
  id: string;
  callSid: string;
  tenantId: string;
  surveyId: string;
  currentQuestionIndex: number;
  questions: SurveyQuestion[];
  responses: VoiceSurveyResponse[];
  state: 'playing_question' | 'collecting_dtmf' | 'collecting_speech' | 'completed' | 'failed';
  bargeIn: boolean;
  maxRetries: number;
}

interface VoiceSurveyResponse {
  questionId: string;
  inputType: 'dtmf' | 'speech';
  rawInput: string;
  transcribedText?: string;
  confidence: number;
  normalizedValue?: number | string | boolean;
  timestamp: number;
  durationMs: number;
}

class VoiceSurveyEngine {
  private tts: TextToSpeechProvider;
  private stt: SpeechToTextProvider;
  private dtmfCollector: DTMFCollector;

  async startSurvey(callSid: string, surveyId: string): Promise<void> {
    const session = await this.initializeSession(callSid, surveyId);
    await this.playQuestion(session);
  }

  private async playQuestion(session: VoiceSurveySession): Promise<void> {
    const question = session.questions[session.currentQuestionIndex];

    if (session.bargeIn) {
      await this.tts.playWithBargeIn(session.callSid, question.text);
    } else {
      await this.tts.play(session.callSid, question.text);
    }

    await this.collectResponse(session);
  }

  private async collectResponse(session: VoiceSurveySession): Promise<void> {
    const question = session.questions[session.currentQuestionIndex];

    let response: VoiceSurveyResponse;

    switch (question.type) {
      case 'rating':
      case 'nps_scale': {
        // Try speech first, fall back to DTMF
        const speechResult = await this.stt.listen({
          callSid: session.callSid,
          timeout: 5000,
          language: 'en',
        });

        if (speechResult.confidence >= 0.8) {
          response = {
            questionId: question.id,
            inputType: 'speech',
            rawInput: speechResult.transcript,
            transcribedText: speechResult.transcript,
            confidence: speechResult.confidence,
            normalizedValue: this.parseSpokenNumber(speechResult.transcript),
            timestamp: Date.now(),
            durationMs: speechResult.durationMs,
          };
        } else {
          const dtmfResult = await this.dtmfCollector.collect({
            callSid: session.callSid,
            maxDigits: 2,
            timeout: 5000,
            retries: 2,
          });
          response = {
            questionId: question.id,
            inputType: 'dtmf',
            rawInput: dtmfResult.digits,
            confidence: 1.0,
            normalizedValue: parseInt(dtmfResult.digits, 10),
            timestamp: Date.now(),
            durationMs: dtmfResult.durationMs,
          };
        }
        break;
      }

      case 'open_ended': {
        const speechResult = await this.stt.listen({
          callSid: session.callSid,
          timeout: 15000,
          language: 'en',
          vadEnabled: true,
        });
        response = {
          questionId: question.id,
          inputType: 'speech',
          rawInput: speechResult.transcript,
          transcribedText: speechResult.transcript,
          confidence: speechResult.confidence,
          timestamp: Date.now(),
          durationMs: speechResult.durationMs,
        };
        break;
      }

      default: {
        const dtmfResult = await this.dtmfCollector.collect({
          callSid: session.callSid,
          maxDigits: 1,
          timeout: 5000,
        });
        response = {
          questionId: question.id,
          inputType: 'dtmf',
          rawInput: dtmfResult.digits,
          confidence: 1.0,
          timestamp: Date.now(),
          durationMs: dtmfResult.durationMs,
        };
      }
    }

    session.responses.push(response);
    session.currentQuestionIndex++;

    if (session.currentQuestionIndex < session.questions.length) {
      await this.playQuestion(session);
    } else {
      await this.completeSurvey(session);
    }
  }

  private async completeSurvey(session: VoiceSurveySession): Promise<void> {
    await this.publishToKafka({
      type: 'voice_survey_completed',
      surveyId: session.surveyId,
      callSid: session.callSid,
      tenantId: session.tenantId,
      responses: session.responses,
      duration: Date.now() - session.responses[0]?.timestamp,
    });

    await this.tts.play(session.callSid, 'Thank you for your feedback. Goodbye.');
    await this.hangup(session.callSid);
  }
}
```

## Open-Source Tools

| Tool | License | Purpose |
|------|---------|---------|
| Whisper (MIT) | Server | Local speech-to-text transcription |
| Rasa (Apache 2.0) | Server | Spoken intent parsing for open-ended feedback |
| Twilio Media Streams (Apache 2.0) | Server | Real-time audio streaming |
| WebRTC VAD (BSD-3) | Server | Voice activity detection for barge-in |

## Production Considerations

**Scaling:** Voice survey sessions are stateful and must be pinned to a single voice server for the survey duration. Use a distributed session store (Redis) with call SID as the key to enable recovery if the server restarts. For high-traffic deployments, dedicate a pool of voice servers exclusively to survey flows, separate from live call handling, to avoid resource contention on STT and TTS engines.

**Security:** Voice recordings containing survey responses must be retained only long enough for transcription (configurable: delete raw audio after 24 hours). Transcribed text containing PII should be redacted before storing in the analytics database. The IVR flow must authenticate the caller before presenting survey questions to prevent unauthorized access to survey state.

**Monitoring:** Track voice survey completion rate (abandoned vs. completed), DTMF-vs-speech response ratio, average survey duration, per-question timeout rate, and STT confidence distribution. Alert if completion rate drops below 40%, if DTMF error rate exceeds 10%, or if average survey duration exceeds 3 minutes (indicating confusing question phrasing).
