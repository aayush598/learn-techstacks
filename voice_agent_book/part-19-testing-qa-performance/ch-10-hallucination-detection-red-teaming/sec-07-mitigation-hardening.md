# Section 07: Mitigation & Hardening

## Overview

Mitigation and hardening implements defenses against detected vulnerabilities. Strategies include input sanitization (cleaning user prompts), output filtering (blocking unsafe responses), guardrail implementation (pre-defined safety constraints), prompt hardening (system prompt improvements), and rate limiting (preventing abuse). Each vulnerability type has specific mitigation techniques.

## Implementation Approach

```typescript
class MitigationEngine {
  async hardenPrompt(userInput: string, context: CallContext): Promise<string> {
    // 1. Input sanitization
    let sanitized = this.sanitizeInput(userInput);
    
    // 2. Add guardrails
    const guardrails = this.getGuardrails(context.agentId);
    sanitized = this.applyGuardrails(sanitized, guardrails);
    
    // 3. Context injection
    sanitized = this.injectContext(sanitized, context);
    
    // 4. Constraint enforcement
    sanitized = this.enforceConstraints(sanitized, context.agentConfig);
    
    return sanitized;
  }

  async filterOutput(response: string, context: CallContext): Promise<OutputFilterResult> {
    // 1. Safety check
    const safetyCheck = await this.safetyEvaluator.evaluate(response);
    if (!safetyCheck.passed) {
      return { action: 'block', fallback: context.agentConfig.safeFallback };
    }
    
    // 2. PII removal
    const cleaned = await this.piiRemover.remove(response);
    
    // 3. Length enforcement
    const truncated = cleaned.length > context.agentConfig.maxResponseLength
      ? cleaned.substring(0, context.agentConfig.maxResponseLength)
      : cleaned;
    
    return { action: 'allow', filtered: truncated };
  }

  private sanitizeInput(input: string): string {
    // Remove known injection patterns
    return input
      .replace(/system:\s*/gi, '')
      .replace(/ignore (all )?(previous )?instructions/gi, '')
      .replace(/you are (now |an? )?(different )?/gi, '')
      .trim();
  }

  private applyGuardrails(input: string, guardrails: Guardrail[]): string {
    for (const guardrail of guardrails) {
      if (input.includes(guardrail.triggerPhrase)) {
        // Redirect conversation away from dangerous topics
        input = `${input}\n\n${guardrail.redirectResponse}`;
      }
    }
    return input;
  }
}
```

## Integration Points

- **Pipeline Integration**: Mitigation runs before LLM call and after LLM response
- **Guardrail Management**: Guardrails configured per agent
- **Monitoring**: Mitigation events tracked and analyzed

## Production Considerations

- **False Positives**: Mitigation may block legitimate content
- **Performance**: Mitigation adds 50-200ms per request
- **Evolving Threats**: Mitigation techniques need continuous updating
