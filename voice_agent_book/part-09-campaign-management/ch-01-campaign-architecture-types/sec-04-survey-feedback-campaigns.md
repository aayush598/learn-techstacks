# Section 04: Survey & Feedback Campaigns

## Overview

Survey and feedback campaigns leverage AI voice agents to conduct structured interviews, collect customer feedback, and measure satisfaction at scale. Unlike sales campaigns that optimize for conversion, survey campaigns optimize for completion rate and response quality. The architecture must support branching survey logic, sentiment capture, multi-language surveys, and real-time aggregation of results.

Survey campaigns are typically broadcast or progressive dialing types since they don't require live agent involvement — the AI agent conducts the entire survey autonomously. The system must handle different survey methodologies, including multiple-choice questions, Likert scale responses, open-ended questions, and conditional branching where subsequent questions depend on previous answers. Response data must be collected in structured format for quantitative analysis while also capturing verbatim responses for qualitative insights.

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
class SurveyCampaign {
  constructor(surveyDefinition) {
    this.survey = surveyDefinition;
    this.brancher = new SurveyBranchEngine(surveyDefinition.questions);
    this.aggregator = new ResponseAggregator();
  }

  async conductSurvey(contact, agent) {
    let currentQuestion = this.survey.questions[0];
    const responses = [];

    while (currentQuestion) {
      const response = await agent.ask(currentQuestion.text, {
        type: currentQuestion.responseType,
        options: currentQuestion.options,
        validation: currentQuestion.validation
      });

      const validatedResponse = this.validateResponse(response, currentQuestion);
      responses.push({
        questionId: currentQuestion.id,
        response: validatedResponse,
        sentiment: response.sentiment,
        timestamp: Date.now()
      });

      currentQuestion = this.brancher.nextQuestion(
        currentQuestion.id,
        validatedResponse
      );
    }

    await this.aggregator.record(contact.id, responses);
    return responses;
  }

  validateResponse(response, question) {
    switch (question.responseType) {
      case 'likert_scale':
        return this.validateLikert(response, question.scale);
      case 'multiple_choice':
        return this.validateChoice(response, question.options);
      case 'open_ended':
        return this.validateOpenEnded(response, question.minLength);
      case 'numeric':
        return this.validateNumeric(response, question.range);
      default:
        return response;
    }
  }
}
```

## Integration Points

- **AI Agent Runtime (Part 06):** Voice agent conducts the survey conversation
- **Sentiment Analysis (Part 11, Ch 05):** Real-time sentiment capture per response
- **Analytics Pipeline (Part 11, Ch 01):** Response aggregation and reporting
- **CRM Integration (Part 10, Ch 02):** Survey results written back to contact record
- **Export Engine (Part 11, Ch 10):** Survey data export for external analysis tools
- **Translation Engine:** Multi-language survey delivery

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Survey completion rates drop significantly after 5 minutes — design surveys for 3-4 minute completion
- Open-ended question responses require significant NLP processing — batch process non-real-time
- Likert scale responses should be validated against the defined scale to catch agent misinterpretation
- Survey branching must be tested exhaustively to ensure all paths terminate
- Multi-language surveys require per-language question text and response validation
- Compliance: survey campaigns must disclose the purpose and recording consent at the start
- Real-time response aggregation enables dynamic campaign adjustments (e.g., pause if negative sentiment trend detected)
- Survey response data is a valuable asset — ensure proper backup and export capabilities
