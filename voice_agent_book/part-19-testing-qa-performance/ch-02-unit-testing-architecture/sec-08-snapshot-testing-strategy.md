# Section 08: Snapshot Testing Strategy

## Overview

Snapshot testing captures the output of a function or component and compares it to a stored reference file on subsequent runs. For the voice AI platform, snapshot testing is used for: configuration objects (agent configs, knowledge base states), conversation transcripts, API response structures, UI component renderings, and data transformation outputs.

The snapshot strategy is conservative: snapshots are used only for stable outputs where changes should be intentional and reviewed. Snapshots are stored alongside test files in `__snapshots__` directories and versioned in Git. Snapshot updates are treated as code changes requiring code review.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Simulator|--->| Utterance|--->| Flow     |--->| Debug    |--->| Report   |
| (in-     |    | Player   |    | Executor |    | Panel    |    | (pass/   |
|  browser)|    | (text/   |    | (step    |    | (log,    |    |  fail    |
|          |    |  audio)  |    |  thru)   |    |  state)  |    |  + trace)|
+----------+    +----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **In-Browser Simulator**: Full conversation simulation with WASM runtime. No backend needed.
- **Utterance Testing**: Pre-defined test utterances with assertions on path and response.
- **Flow Validation**: Graph analysis for unreachable nodes, infinite loops, missing required fields.
## Implementation Approach

```typescript
// Snapshot testing for agent configuration
describe('Agent Configuration', () => {
  it('generates correct default configuration', () => {
    const config = new AgentConfigBuilder()
      .withDefaultLanguage('en-US')
      .withDefaultVoice('natural-female')
      .withGreeting('Hello, how can I help you?')
      .build();

    expect(config).toMatchSnapshot();
  });

  it('generates configuration with custom properties', () => {
    const config = new AgentConfigBuilder()
      .withLanguage('es-ES')
      .withVoice('spanish-male')
      .withWhisperMode(true)
      .withCustomPrompt('Eres un asistente amigable')
      .build();

    // Use property matchers for dynamic fields
    expect(config).toMatchSnapshot({
      id: expect.any(String),
      createdAt: expect.any(String),
      updatedAt: expect.any(String),
      config: {
        temperature: expect.any(Number),
      },
    });
  });
});

// Inline snapshot for simple cases
it('returns sorted supported languages', () => {
  const languages = getSupportedLanguages();
  expect(languages).toMatchInlineSnapshot(`
    [
      "de-DE",
      "en-US",
      "es-ES",
      "fr-FR",
      "ja-JP",
      "pt-BR",
    ]
  `);
});
```

## Integration Points

- **CI Pipeline**: Snapshot tests run as part of the unit test suite
- **Review Workflow**: Snapshot changes visible in PR diff for review
- **Visual Regression**: Visual snapshots (screenshots) handled by Playwright
- **API Contracts**: API response snapshots serve as contract tests
- **Configuration Changes**: Config changes reflected in snapshot diffs

## Open-Source Tools

- **Vitest** (MIT): Unit testing
- **Playwright** (Apache 2.0): E2E
- **React Testing Library** (MIT): Components
## Production Considerations

- **Snapshot Bloat**: Large snapshots slow down tests and make reviews hard; keep focused
- **False Positives**: Dynamic content (dates, IDs) in snapshots causes unnecessary failures; use matchers
- **Update Discipline**: Never update snapshots without reviewing the diff; `--update` is powerful
- **Binary Snapshots**: Avoid binary snapshots (images, audio) in unit tests; use separate tools
- **Snapshot Hygiene**: Regularly review and clean up unused snapshot files
