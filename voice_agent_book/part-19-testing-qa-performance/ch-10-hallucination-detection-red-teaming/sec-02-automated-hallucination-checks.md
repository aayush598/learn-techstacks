# Section 02: Automated Hallucination Checks

## Overview

Automated hallucination checks run continuously during development and in production. Checks include: knowledge base cross-reference (does the response match the KB?), self-consistency (does the response contradict itself?), NLI-based validation (can we infer the response from the context?), and fact extraction verification (are specific claims verifiable?).

## Implementation Approach

```typescript
class AutomatedHallucinationChecker {
  async checkResponse(response: string, context: ValidationContext): Promise<CheckResult> {
    const results = await Promise.all([
      this.knowledgeBaseCrossReference(response, context.kb),
      this.selfConsistencyCheck(response),
      this.nliValidation(response, context.conversation),
      this.factExtractionVerification(response),
    ]);

    return {
      passed: results.every(r => r.passed),
      checks: results,
      overallScore: results.reduce((s, r) => s + r.score, 0) / results.length,
    };
  }

  private async knowledgeBaseCrossReference(response: string, kb: KnowledgeBase): Promise<Check> {
    const claims = this.extractClaims(response);
    const kbEntries = await kb.search(claims.join(' '), { limit: 5 });
    let supported = 0;
    for (const claim of claims) {
      const relevant = kbEntries.some(e => this.semanticSimilarity(claim, e.content) > 0.8);
      if (relevant) supported++;
    }
    const score = claims.length > 0 ? supported / claims.length : 1;
    return { name: 'kb-cross-ref', passed: score > 0.7, score, details: `${supported}/${claims.length} claims supported` };
  }

  private async selfConsistencyCheck(response: string): Promise<Check> {
    // Check for internal contradictions
    const sentences = response.split(/[.!?]+/).filter(s => s.trim().length > 0);
    let contradictions = 0;
    for (let i = 0; i < sentences.length; i++) {
      for (let j = i + 1; j < sentences.length; j++) {
        if (await this.isContradiction(sentences[i], sentences[j])) contradictions++;
      }
    }
    const score = sentences.length > 1 ? 1 - (contradictions / (sentences.length * (sentences.length - 1) / 2)) : 1;
    return { name: 'self-consistency', passed: score > 0.8, score, details: `${contradictions} contradictions found` };
  }

  private async isContradiction(a: string, b: string): Promise<boolean> {
    // Use NLI model to check if a contradicts b
    const result = await this.nliModel.predict({ premise: a, hypothesis: b });
    return result.label === 'contradiction' && result.confidence > 0.9;
  }
}
```

## Integration Points

- **CI Pipeline**: Hallucination checks on every agent change
- **Production Monitoring**: Continuous production response validation
- **Alerting**: High hallucination rates trigger alerts

## Open-Source Tools

- **Hugging Face Transformers** (Apache 2.0): NLI models
- **Sentence-Transformers** (Apache 2.0): Semantic similarity
- **Spacy** (MIT): Claim extraction

## Production Considerations

- **Model Performance**: NLI models add latency; use lightweight models for real-time
- **Coverage**: Not all hallucinations are detectable by automated checks
- **Continuous Improvement**: Add detected hallucinations to training data
