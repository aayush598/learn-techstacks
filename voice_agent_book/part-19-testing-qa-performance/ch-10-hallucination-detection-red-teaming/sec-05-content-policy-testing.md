# Section 05: Content Policy Testing

## Overview

Content policy testing validates that agent responses adhere to defined policies. Policies are expressed as a DSL (Domain-Specific Language) that defines allowed content, prohibited topics, required disclosures, and response constraints. Automated policy checks run against every response, with violations flagged and blocked.

## Implementation Approach

```typescript
interface PolicyRule {
  id: string;
  type: 'block_topic' | 'require_disclosure' | 'max_length' | 'allow_list' | 'format_check';
  parameters: Record<string, unknown>;
  severity: 'error' | 'warning';
}

class PolicyEngine {
  async evaluate(response: string, policies: PolicyRule[]): Promise<PolicyResult> {
    const violations: PolicyViolation[] = [];
    for (const rule of policies) {
      const violation = await this.checkRule(response, rule);
      if (violation) violations.push(violation);
    }
    return { passed: violations.every(v => v.severity !== 'error'), violations };
  }

  private async checkRule(response: string, rule: PolicyRule): Promise<PolicyViolation | null> {
    switch (rule.type) {
      case 'block_topic': {
        const topics = rule.parameters.topics as string[];
        for (const topic of topics) {
          if (await this.isAboutTopic(response, topic)) {
            return { rule, message: `Response discusses blocked topic: ${topic}`, severity: rule.severity };
          }
        }
        return null;
      }
      case 'require_disclosure': {
        const required = rule.parameters.text as string;
        if (!response.includes(required)) {
          return { rule, message: `Missing required disclosure: "${required}"`, severity: rule.severity };
        }
        return null;
      }
      case 'max_length': {
        const maxLen = rule.parameters.length as number;
        if (response.length > maxLen) {
          return { rule, message: `Response exceeds max length (${response.length} > ${maxLen})`, severity: rule.severity };
        }
        return null;
      }
      default:
        return null;
    }
  }
}

// Policy DSL example
const policies: PolicyRule[] = [
  { id: 'no_medical_advice', type: 'block_topic', parameters: { topics: ['diagnosis', 'medication', 'treatment'] }, severity: 'error' },
  { id: 'disclosure_ai', type: 'require_disclosure', parameters: { text: 'I am an AI assistant' }, severity: 'error' },
  { id: 'response_length', type: 'max_length', parameters: { length: 500 }, severity: 'warning' },
];
```

## Integration Points

- **Policy Management UI**: Define and manage policies
- **Response Pipeline**: Checks run before response delivery
- **Monitoring**: Policy violation tracking
- **Audit Log**: Policy violations logged for review

## Production Considerations

- **Policy Updates**: Policies evolve with product and regulatory requirements
- **False Positives**: Topic blocking can be overly broad
- **Performance**: Policy checks should complete in <50ms
