# Section 07: Multi-Language Email Support

## Overview

Multi-language email support delivers emails in the user's preferred locale. Templates are maintained per language, with fallback chains when translations are unavailable. The system handles RTL languages, locale-specific formatting, and translation variable injection.

## Implementation Approach

```typescript
interface LocalizedTemplate {
  templateId: string;
  locale: string;
  subject: string;
  html: string;
  text: string;
  isRTL: boolean;
  metadata: TemplateMeta;
}

class MultiLanguageEmailEngine {
  async renderLocalized(templateId: string, locale: string, data: Record<string, unknown>): Promise<RenderedEmail> {
    const template = await this.getLocalizedTemplate(templateId, locale);
    const html = this.renderTemplate(template.html, data);
    const text = this.renderTemplate(template.text, data);
    const subject = this.renderTemplate(template.subject, data);

    return {
      html: template.isRTL ? this.wrapRTL(html) : html,
      text,
      subject,
      locale,
    };
  }

  private async getLocalizedTemplate(templateId: string, locale: string): Promise<LocalizedTemplate> {
    // Try exact locale first (e.g., pt-BR)
    let template = await this.templateStore.findOne({ templateId, locale });

    // Fallback to language-only (e.g., pt)
    if (!template) {
      const lang = locale.split('-')[0];
      template = await this.templateStore.findOne({ templateId, locale: lang });
    }

    // Fallback to default locale
    if (!template) {
      template = await this.templateStore.findOne({ templateId, locale: 'en' });
    }

    if (!template) throw new Error(`No template found for ${templateId} in any locale`);
    return template;
  }

  async uploadTranslation(templateId: string, locale: string, translation: TranslationInput): Promise<void> {
    const existing = await this.templateStore.findOne({ templateId, locale });
    if (existing) {
      existing.subject = translation.subject;
      existing.html = translation.html;
      existing.text = translation.text;
      existing.isRTL = this.isRTL(locale);
      await this.templateStore.update(existing);
    } else {
      await this.templateStore.save({
        templateId,
        locale,
        subject: translation.subject,
        html: translation.html,
        text: translation.text,
        isRTL: this.isRTL(locale),
        metadata: { createdAt: new Date().toISOString() },
      });
    }
  }

  private isRTL(locale: string): boolean {
    const rtlLocales = ['ar', 'he', 'fa', 'ur', 'yi'];
    const lang = locale.split('-')[0];
    return rtlLocales.includes(lang);
  }

  private wrapRTL(html: string): string {
    return `<div dir="rtl">${html}</div>`;
  }

  private renderTemplate(template: string, data: Record<string, unknown>): string {
    // Replace {{variable}} placeholders with values
    return template.replace(/\{\{(\w+)\}\}/g, (_, key) => {
      const value = data[key];
      if (value === undefined || value === null) return '';
      return String(value);
    });
  }

  async getSupportedLocales(): Promise<LocaleInfo[]> {
    const locales = await this.templateStore.distinct('locale');
    return locales.map(l => ({
      code: l,
      name: new Intl.DisplayNames([l], { type: 'language' }).of(l) || l,
      rtl: this.isRTL(l),
    }));
  }
}
```

## Integration Points

- **Translation Management**: Admin UI for uploading translations
- **Locale Detection**: User locale from profile or Accept-Language header
- **Translation Service**: Integration with translation management platforms

## Production Considerations

- **Translation Coverage**: Track which locales have complete translations
- **Fallback Chain**: Always have en as fallback
- **RTL Testing**: Test RTL rendering across email clients
