# Section 02: Template Engine Integration

## Overview

The email template engine renders React Email components, MJML templates, or Handlebars templates into HTML emails. Templates support variables, conditional content, and responsive design. A preview server allows testing templates during development, and versioning tracks template changes.

## Implementation Approach

```typescript
interface EmailTemplate {
  id: string;
  name: string;
  version: number;
  type: 'react_email' | 'mjml' | 'handlebars';
  content: string;
  compiled?: string;
  variables: TemplateVariable[];
  previewData: Record<string, unknown>;
}

class EmailTemplateEngine {
  private cache: Map<string, CompiledTemplate> = new Map();

  async render(templateId: string, data: Record<string, unknown>, options?: RenderOptions): Promise<RenderedEmail> {
    const cacheKey = `${templateId}:${options?.version || 'latest'}`;
    let compiled = this.cache.get(cacheKey);

    if (!compiled) {
      const template = await this.getTemplate(templateId);
      compiled = this.compile(template);
      this.cache.set(cacheKey, compiled);
    }

    const html = compiled.render(data);
    const text = this.stripHtml(html);

    return { html, text, subject: compiled.renderSubject(data) };
  }

  private compile(template: EmailTemplate): CompiledTemplate {
    switch (template.type) {
      case 'react_email':
        return this.compileReactEmail(template);
      case 'mjml':
        return this.compileMJML(template);
      case 'handlebars':
        return this.compileHandlebars(template);
    }
  }

  private compileReactEmail(template: EmailTemplate): CompiledTemplate {
    // React Email templates are React components
    // They get compiled to HTML at build time via @react-email/render
    return {
      render: (data: Record<string, unknown>) => {
        // In production, this uses pre-compiled HTML
        // In development, it renders on-the-fly
        return this.renderReactEmail(template.content, data);
      },
      renderSubject: (data: Record<string, unknown>) => {
        const template = Handlebars.compile(template.subject || '');
        return template(data);
      },
    };
  }

  private compileMJML(template: EmailTemplate): CompiledTemplate {
    const mjml2html = require('mjml');
    const compiled = mjml2html(template.content);

    return {
      render: (data: Record<string, unknown>) => {
        const template = Handlebars.compile(compiled.html);
        return template(data);
      },
      renderSubject: (data: Record<string, unknown>) => {
        const template = Handlebars.compile(template.subject || '');
        return template(data);
      },
    };
  }

  private compileHandlebars(template: EmailTemplate): CompiledTemplate {
    const compiled = Handlebars.compile(template.content);

    return {
      render: (data: Record<string, unknown>) => compiled(data),
      renderSubject: (data: Record<string, unknown>) => {
        const subTemplate = Handlebars.compile(template.subject || '');
        return subTemplate(data);
      },
    };
  }

  async preview(templateId: string, data?: Record<string, unknown>): Promise<string> {
    const template = await this.getTemplate(templateId);
    const previewData = data || template.previewData;
    const rendered = await this.render(templateId, previewData);
    return rendered.html;
  }

  private stripHtml(html: string): string {
    return html.replace(/<[^>]*>/g, '')
      .replace(/&amp;/g, '&')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .replace(/&quot;/g, '"');
  }
}
```

## Integration Points

- **Template Management UI**: Edit and preview templates
- **Variable Registry**: Document available template variables
- **Preview Server**: Dev server for template development

## Production Considerations

- **Template Caching**: Cache compiled templates for performance
- **Error Handling**: Fallback text for rendering failures
- **Responsive Design**: Test templates across email clients
