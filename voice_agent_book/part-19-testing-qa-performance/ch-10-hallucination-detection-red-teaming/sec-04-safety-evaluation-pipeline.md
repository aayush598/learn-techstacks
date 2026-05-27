# Section 04: Safety Evaluation Pipeline

## Overview

The safety evaluation pipeline checks LLM responses for harmful content before delivery to users. Checks include toxicity detection (hate speech, harassment), PII leakage (phone numbers, SSN, credit cards), policy violations (specific product policies), and content safety (violence, self-harm, illegal activities). Multiple models are ensembled for robust detection.

## Implementation Approach

```typescript
interface SafetyCheck {
  type: 'toxicity' | 'pii' | 'policy' | 'content_safety';
  passed: boolean;
  score: number;
  details: string;
}

class SafetyEvaluator {
  async evaluate(response: string): Promise<SafetyResult> {
    const checks: SafetyCheck[] = await Promise.all([
      this.checkToxicity(response),
      this.checkPII(response),
      this.checkPolicyViolations(response),
      this.checkContentSafety(response),
    ]);

    return {
      passed: checks.every(c => c.passed),
      checks,
      blocked: checks.some(c => !c.passed && c.score > 0.9),
    };
  }

  private async checkPII(text: string): Promise<SafetyCheck> {
    const patterns = {
      email: /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g,
      phone: /\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/g,
      ssn: /\b\d{3}-\d{2}-\d{4}\b/g,
      creditCard: /\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b/g,
    };
    const found: string[] = [];
    for (const [type, pattern] of Object.entries(patterns)) {
      const matches = text.match(pattern);
      if (matches) found.push(...matches.map(m => `${type}: ${m}`));
    }
    return {
      type: 'pii',
      passed: found.length === 0,
      score: found.length / 10,
      details: found.length > 0 ? `Found PII: ${found.join(', ')}` : 'No PII detected',
    };
  }

  private async checkToxicity(text: string): Promise<SafetyCheck> {
    const score = await this.toxicityModel.predict(text);
    return {
      type: 'toxicity',
      passed: score < 0.7,
      score,
      details: `Toxicity score: ${(score * 100).toFixed(0)}%`,
    };
  }

  private async checkContentSafety(text: string): Promise<SafetyCheck> {
    const categories = ['violence', 'self-harm', 'harassment', 'hate_speech', 'illegal'];
    const results = await Promise.all(categories.map(c => this.categoryModel.predict(text, c)));
    const maxScore = Math.max(...results);
    return { type: 'content_safety', passed: maxScore < 0.8, score: maxScore, details: 'Content safety check complete' };
  }
}
```

## Integration Points

- **Response Pipeline**: Safety check runs before delivering response
- **Blocking Mechanism**: Unsafe responses replaced with fallback
- **Monitoring**: Safety violation rates tracked
- **Human Review**: Flagged responses reviewed by safety team

## Open-Source Tools

- **Detoxify** (Apache 2.0): Toxicity detection
- **Microsoft Presidio** (MIT): PII detection
- **LLM Guard** (MIT): LLM output safety
- **Hugging Face Safety Models** (Apache 2.0): Content moderation

## Production Considerations

- **False Positive Rate**: Overly strict blocking harms user experience
- **Latency**: Safety checks add 200-500ms; run in parallel
- **Customization**: Safety policies vary by use case and region
