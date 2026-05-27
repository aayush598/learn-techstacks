# Section 05: Threshold Templates

## Overview

Threshold templates provide pre-built monitoring configurations for common scenarios. Templates include industry-standard defaults for metrics like latency, error rate, throughput, and resource utilization. Users can instantiate templates to quickly set up monitoring, then customize parameters.

## Design Decisions

- **Template Catalog**: Curated templates organized by category
- **Parameterization**: Templates expose configurable parameters
- **Versioning**: Templates versioned; updates propagated to instances
- **Validation**: Templates validated against metric schemas

## Implementation Approach

```typescript
interface ThresholdTemplate {
  id: string;
  name: string;
  category: string;
  description: string;
  version: number;
  parameters: TemplateParameter[];
  thresholdConfig: ThresholdConfig;
  recommendedFor: string[];
}

interface TemplateParameter {
  name: string;
  type: 'number' | 'string' | 'select' | 'duration';
  label: string;
  default: unknown;
  options?: { label: string; value: unknown }[];
  validation?: { min?: number; max?: number; pattern?: string };
}

interface ThresholdConfig {
  metricSource: MetricSource;
  conditions: ThresholdCondition[];
  severity: string;
  evaluationWindow: number;
}

class ThresholdTemplateManager {
  private templates: Map<string, ThresholdTemplate> = new Map();

  async registerTemplate(template: ThresholdTemplate): Promise<void> {
    this.templates.set(template.id, template);
    await this.templateStore.save(template);
  }

  async instantiateTemplate(templateId: string, params: Record<string, unknown>, metricSource: MetricSource): Promise<Threshold> {
    const template = this.templates.get(templateId);
    if (!template) throw new Error('Template not found');

    const resolvedParams = this.resolveParameters(template.parameters, params);
    const thresholdConfig = this.applyParameters(template.thresholdConfig, resolvedParams);

    return this.thresholdManager.createThreshold({
      ...thresholdConfig,
      metricSource,
    });
  }

  private resolveParameters(parameters: TemplateParameter[], params: Record<string, unknown>): Record<string, unknown> {
    const resolved: Record<string, unknown> = {};
    for (const param of parameters) {
      const value = params[param.name] ?? param.default;
      if (param.validation) {
        this.validateParam(param, value);
      }
      resolved[param.name] = value;
    }
    return resolved;
  }

  private applyParameters(config: ThresholdConfig, params: Record<string, unknown>): ThresholdConfig {
    // Substitute template variables with resolved parameters
    const conditions = config.conditions.map(c => ({
      ...c,
      value: typeof c.value === 'string' && c.value.startsWith('{{')
        ? (params[c.value.replace(/{{|}}/g, '')] as number)
        : c.value,
    }));
    return { ...config, conditions };
  }

  // Pre-built templates
  static readonly DEFAULT_TEMPLATES: ThresholdTemplate[] = [
    {
      id: 'latency-p99',
      name: 'P99 Latency',
      category: 'performance',
      description: 'Alert when P99 latency exceeds threshold',
      version: 1,
      parameters: [
        { name: 'threshold', type: 'number', label: 'Latency threshold (ms)', default: 500, validation: { min: 1 } },
        { name: 'window', type: 'duration', label: 'Evaluation window', default: 300 },
      ],
      thresholdConfig: {
        metricSource: { type: 'prometheus', query: 'histogram_quantile(0.99, ...)', aggregation: 'p99', interval: 60 },
        conditions: [{ operator: '>', value: '{{threshold}}', sustainedFor: 3 }],
        severity: 'major',
        evaluationWindow: 300,
      },
      recommendedFor: ['api', 'voice-agent', 'websocket'],
    },
  ];
}
```

## Integration Points

- **Template Catalog UI**: Browse and instantiate templates
- **Metric Catalog**: Templates reference available metrics
- **Onboarding Flow**: Quick-start monitoring with templates

## Production Considerations

- **Template Updates**: Propagate template changes to instances carefully
- **Override Documentation**: Document which parameters users customized
- **Template Governance**: Review and approve templates before publishing
