# Section 04: Template System

## Overview

The notification template system manages multi-channel templates with dynamic content rendering. Templates are defined per channel variant (email HTML, Slack blocks, SMS plaintext) and support variable injection, conditional content, and versioning. The renderer processes templates with notification data to produce channel-specific payloads.

## Design Decisions

- **Per-Channel Templates**: Each channel variant has its own template
- **Mustache/Liquid**: Industry-standard template syntax
- **Template Versioning**: Templates versioned for rollback
- **Preview Mode**: Render templates in UI for editing

## Implementation Approach

```typescript
interface NotificationTemplate {
  id: string;
  name: string;
  versions: TemplateVersion[];
  channels: ChannelTemplateVariant[];
  variables: TemplateVariable[];
}

interface TemplateVersion {
  version: number;
  content: string;
  engine: 'handlebars' | 'liquid' | 'mjml';
  createdAt: string;
  published: boolean;
}

interface ChannelTemplateVariant {
  channel: string;
  subject?: string; // For email
  body: string;
  preheader?: string;
}

class TemplateRenderer {
  async render(templateId: string, channel: string, data: Record<string, unknown>): Promise<RenderedTemplate> {
    const template = await this.templateService.getTemplate(templateId);
    const variant = template.channels.find(c => c.channel === channel);
    if (!variant) throw new Error(`No template variant for channel: ${channel}`);

    const engine = this.getEngine(template.versions[0].engine);
    const rendered = engine.render(variant.body, data);

    return {
      channel,
      subject: variant.subject ? engine.render(variant.subject, data) : undefined,
      body: rendered,
      renderedAt: new Date().toISOString(),
    };
  }

  private getEngine(type: string): TemplateEngine {
    switch (type) {
      case 'handlebars': return new HandlebarsEngine();
      case 'liquid': return new LiquidEngine();
      case 'mjml': return new MJMLEngine();
      default: throw new Error(`Unknown engine: ${type}`);
    }
  }

  async preview(templateId: string, channel: string, data: Record<string, unknown>): Promise<string> {
    const rendered = await this.render(templateId, channel, data);
    return rendered.body;
  }
}
```

## Integration Points

- **Template Management UI**: CRUD interface for templates
- **Variable Registry**: Available variables documented and validated
- **Channel Renderers**: Each channel has specific rendering logic

## Production Considerations

- **Cache Frequently Used Templates**: Template compilation is expensive
- **Variable Validation**: Missing variables should not crash rendering
- **HTML Security**: Sanitize user-provided content in templates
