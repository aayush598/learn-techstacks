# Section 07: Template Management

## Overview

Digest and report templates control the layout, branding, and styling of delivered content. Templates are customizable per tenant, supporting HTML email templates, Slack message templates, and report layout templates. Users can customize colors, logos, and content organization.

## Architecture

```
Template Management
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Template Store] → [Template Engine] → [Rendered Content] → [Delivery]
       │                  │                       │              │
  Handlebar/            Compile with           Branded,       Send to
  MJML templates        tenant variables       personalized   channel
  Versioned             + content data         output
  Per-tenant

Template Types:
  ┌──────────────────┬──────────────────────────────────────────────────┐
  │ Template Type    │ Usage                                            │
  ├──────────────────┼──────────────────────────────────────────────────┤
  │ digest-email     │ Full digest email with HTML/MJML                 │
  │ digest-slack     │ Slack Block Kit JSON template                    │
  │ report-layout    │ Report page layout (header, footer, sections)    │
  │ report-section   │ Individual report section (table, chart)         │
  │ brand-defaults   │ Brand colors, fonts, logo URL                    │
  └──────────────────┴──────────────────────────────────────────────────┘

Template Variables:
  {{tenant.name}}         → "Acme Corp"
  {{tenant.logoUrl}}      → "https://cdn.acme.com/logo.png"
  {{tenant.primaryColor}} → "#4F46E5"
  {{tenant.secondaryColor}} → "#6366F1"
  {{tenant.domain}}       → "acme.com"
  {{digest.date}}         → "June 10, 2025"
  {{digest.time}}         → "08:00 AM ET"
  {{digest.modules}}      → [ModuleContent[]]
  {{unsubscribe.url}}     → "..."
  {{preferences.url}}     → "..."
```

## Design Decisions

- **Handlebars Templates**: Logic-less templates for security and simplicity
- **Tenant Branding**: Brand variables injected at render time
- **Template Versioning**: Templates versioned for rollback capability
- **Preview Mode**: Render template with sample data before saving

## Implementation Approach

```typescript
interface Template {
  id: string;
  tenantId: string;
  type: 'digest-email' | 'digest-slack' | 'report-layout' | 'report-section' | 'brand-defaults';
  name: string;
  version: number;
  content: string; // Handlebars template
  variables: string[]; // Expected template variables
  isDefault: boolean;
  createdAt: Date;
  updatedAt: Date;
  createdBy: string;
}

interface BrandDefaults {
  primaryColor: string;
  secondaryColor: string;
  accentColor: string;
  fontFamily: string;
  logoUrl: string;
  faviconUrl: string;
  footerText: string;
}

class TemplateManager {
  private compiledCache: Map<string, HandlebarsTemplateDelegate> = new Map();

  async createTemplate(template: Omit<Template, 'id' | 'version' | 'createdAt' | 'updatedAt'>): Promise<Template> {
    const newTemplate: Template = {
      ...template,
      id: crypto.randomUUID(),
      version: 1,
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    // Validate template compilation
    this.compileTemplate(newTemplate.content);

    await this.store.create('templates', newTemplate);
    return newTemplate;
  }

  async updateTemplate(id: string, updates: Partial<Template>): Promise<Template> {
    const existing = await this.store.findOne('templates', { id });
    if (!existing) throw new Error('Template not found');

    const updated: Template = {
      ...existing,
      ...updates,
      version: existing.version + 1,
      updatedAt: new Date(),
    };

    // Validate new content
    if (updates.content) {
      this.compileTemplate(updates.content);
    }

    await this.store.update('templates', { id }, updated);

    // Invalidate cache
    this.compiledCache.delete(`${existing.tenantId}:${existing.type}`);

    return updated;
  }

  async render(
    tenantId: string,
    type: Template['type'],
    data: Record<string, unknown>,
  ): Promise<string> {
    const template = await this.getTemplate(tenantId, type);
    const compiled = this.getCompiled(template);
    return compiled(data);
  }

  async renderWithBranding(
    tenantId: string,
    type: Template['type'],
    data: Record<string, unknown>,
  ): Promise<string> {
    const [template, brandDefaults] = await Promise.all([
      this.getTemplate(tenantId, type),
      this.getBrandDefaults(tenantId),
    ]);

    const compiled = this.getCompiled(template);
    return compiled({
      ...data,
      tenant: brandDefaults,
    });
  }

  async getBrandDefaults(tenantId: string): Promise<BrandDefaults> {
    const template = await this.store.findOne('templates', {
      tenantId,
      type: 'brand-defaults',
    });

    if (!template) {
      return this.getDefaultBranding();
    }

    // Brand defaults stored as JSON in template content
    return JSON.parse(template.content);
  }

  async updateBrandDefaults(tenantId: string, branding: Partial<BrandDefaults>): Promise<void> {
    const existing = await this.store.findOne('templates', {
      tenantId,
      type: 'brand-defaults',
    });

    const defaults = existing
      ? { ...JSON.parse(existing.content), ...branding }
      : { ...this.getDefaultBranding(), ...branding };

    if (existing) {
      await this.store.update('templates', { id: existing.id }, {
        content: JSON.stringify(defaults),
        updatedAt: new Date(),
        version: existing.version + 1,
      });
    } else {
      await this.store.create('templates', {
        id: crypto.randomUUID(),
        tenantId,
        type: 'brand-defaults',
        name: 'Brand Defaults',
        version: 1,
        content: JSON.stringify(defaults),
        variables: Object.keys(defaults),
        isDefault: true,
        createdAt: new Date(),
        updatedAt: new Date(),
        createdBy: 'system',
      });
    }
  }

  async preview(template: Template, data: Record<string, unknown>): Promise<string> {
    const compiled = this.compileTemplate(template.content);
    return compiled(data);
  }

  async getTemplateHistory(id: string): Promise<Template[]> {
    // In production, store version history in separate table
    return this.store.find('templates', { id });
  }

  async rollback(id: string, version: number): Promise<Template> {
    const history = await this.getTemplateHistory(id);
    const target = history.find(t => t.version === version);
    if (!target) throw new Error('Version not found');

    return this.updateTemplate(id, { content: target.content });
  }

  private async getTemplate(tenantId: string, type: Template['type']): Promise<Template> {
    // First try tenant-specific, then default
    let template = await this.store.findOne('templates', { tenantId, type, isDefault: false });

    if (!template) {
      template = await this.store.findOne('templates', { type, isDefault: true });
    }

    if (!template) {
      throw new Error(`No template found for ${type}`);
    }

    return template;
  }

  private getCompiled(template: Template): HandlebarsTemplateDelegate {
    const cacheKey = `${template.tenantId}:${template.type}:${template.version}`;
    let compiled = this.compiledCache.get(cacheKey);

    if (!compiled) {
      compiled = this.compileTemplate(template.content);
      this.compiledCache.set(cacheKey, compiled);
    }

    return compiled;
  }

  private compileTemplate(content: string): HandlebarsTemplateDelegate {
    try {
      return Handlebars.compile(content);
    } catch (error) {
      throw new Error(`Template compilation error: ${error.message}`);
    }
  }

  private getDefaultBranding(): BrandDefaults {
    return {
      primaryColor: '#4F46E5',
      secondaryColor: '#6366F1',
      accentColor: '#10B981',
      fontFamily: 'Inter, sans-serif',
      logoUrl: 'https://cdn.voiceagent.com/logo.png',
      faviconUrl: 'https://cdn.voiceagent.com/favicon.ico',
      footerText: '© Voice Agent. All rights reserved.',
    };
  }
}

// Template validation service
class TemplateValidator {
  validateContent(content: string, expectedVariables: string[]): ValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];

    // Check for unclosed mustache tags
    const openCount = (content.match(/\{\{/g) || []).length;
    const closeCount = (content.match(/\}\}/g) || []).length;

    if (openCount !== closeCount) {
      errors.push(`Mismatched template tags: ${openCount} opening, ${closeCount} closing`);
    }

    // Extract used variables
    const usedVars = new Set(
      Array.from(content.matchAll(/\{\{([^#/][^}]*)\}\}/g), m => m[1].trim().split('.')[0])
    );

    // Check for missing expected variables
    for (const expected of expectedVariables) {
      if (!usedVars.has(expected) && !expected.startsWith('$')) {
        warnings.push(`Expected variable "${expected}" not used in template`);
      }
    }

    return { valid: errors.length === 0, errors, warnings };
  }
}
```

## Integration Points

- **Tenant Settings**: Brand defaults managed in tenant settings
- **Template Editor**: Web-based template editor in developer portal
- **Version Control**: Template changes tracked with version history

## Production Considerations

- **Template Execution Safety**: Sandboxed template rendering to prevent code injection
- **Size Limits**: Maximum 100KB template content
- **Default Templates**: Ship with sensible default templates for new tenants
- **Migration Path**: Template schema changes backward compatible

## Open-Source Tools

- **Handlebars**: Logic-less template engine
- **MJML**: Responsive email template framework
- **CodeMirror**: In-browser template editor
