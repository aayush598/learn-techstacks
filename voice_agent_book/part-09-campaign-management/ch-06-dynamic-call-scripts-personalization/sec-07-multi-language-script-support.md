# Section 07: Multi-Language Script Support

## Overview

Multi-language script support enables campaigns to communicate with contacts in their preferred language, dramatically improving engagement rates and customer experience. The system must detect or determine the contact's language preference, select the appropriate script translation, and render the script using the correct TTS voice for that language. This involves language detection at the contact level, translation management for script content, and TTS voice selection per language.

The multi-language system supports translations managed through a web UI (or imported from translation files), with fallback chains when translations are incomplete. Each script template can have multiple language variants, and the system selects the appropriate one at call time. The system also supports region-specific language variants (e.g., Spanish for Spain vs. Mexico, French for France vs. Canada).

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Multi-Language Script Support                   │
├─────────────────────────────────────────────────────────────┤
│  Language Resolution Chain:                                 │
│                                                             │
│  1. Contact language preference (from CRM/profile)         │
│  2. Phone country code → national language                  │
│  3. Area code → regional language (if applicable)          │
│  4. Campaign default language                              │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Translation Management                             │   │
│  │                                                      │   │
│  │  Script Template (English):                         │   │
│  │  "Hi [FirstName], this is a reminder..."            │   │
│  │                                                      │   │
│  │  Translations:                                       │   │
│  │  ┌─────────┬────────────────────────────────────┐   │   │
│  │  │ Spanish │ "Hola [FirstName], esto es un..."   │   │   │
│  │  │ French  │ "Bonjour [FirstName], ceci est..."  │   │   │
│  │  │ German  │ "Hallo [FirstName], dies ist..."    │   │   │
│  │  │ Chinese │ "您好 [FirstName]，这是..."           │   │   │
│  │  └─────────┴────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  TTS Voice Selection                                 │   │
│  │  • English → "en-US-Neural2-D"                       │   │
│  │  • Spanish → "es-ES-Neural2-B"                       │   │
│  │  • French → "fr-FR-Neural2-A"                        │   │
│  │  • Chinese → "cmn-CN-Neural2-A"                      │   │
│  │  • Fallback → English voice for untranslated parts   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Design Decisions

- **Translation-assisted with machine translation fallback:** Primary translations are human-curated for quality. Missing translations use machine translation (Google/DeepL API) as a fallback with a quality flag. Trade-off: translation cost vs. coverage completeness.

- **ICU MessageFormat for translations:** Use ICU MessageFormat syntax which handles pluralization, gender, and select cases correctly across languages. This is the standard for professional localization. Trade-off: format complexity vs. localization correctness.

- **Token compatibility across languages:** Personalization tokens work identically in all language variants. The same token name produces the same data regardless of language. Trade-off: token system simplicity vs. language-specific formatting needs.

- **Voice-appropriate TTS per language:** Each language uses a neural TTS voice that sounds natural in that language. Using a mismatched accent (e.g., English voice reading Spanish) produces poor results. Trade-off: TTS voice management overhead vs. natural quality.

## Implementation Approach

```
class MultiLanguageScriptEngine {
  constructor(translationStore, ttsService, languageDetector) {
    this.translations = translationStore;
    this.tts = ttsService;
    this.languageDetector = languageDetector;
  }

  async resolveLanguage(contact, campaign) {
    // Check contact language preference
    if (contact.language) {
      const supported = await this.translations.getSupportedLanguages(campaign.id);
      if (supported.includes(contact.language)) {
        return { language: contact.language, source: 'contact_profile', confidence: 1.0 };
      }
    }

    // Detect from phone number country code
    const country = this.languageDetector.countryFromPhone(contact.phone);
    const countryLanguage = this.languageDetector.languageForCountry(country);
    
    if (countryLanguage && await this.translations.isSupported(campaign.id, countryLanguage)) {
      return { language: countryLanguage, source: 'phone_country', confidence: 0.7 };
    }

    // Fall back to campaign default
    return { language: campaign.defaultLanguage, source: 'campaign_default', confidence: 0.5 };
  }

  async getScriptContent(campaignId, language) {
    // Try to get translated version
    const translation = await this.translations.getTranslation(
      campaignId, 
      language
    );

    if (translation && translation.completeness >= 0.95) {
      return translation;
    }

    // If translation is incomplete, fill gaps with machine translation
    if (translation) {
      const filled = await this.translations.fillGaps(
        translation,
        language,
        this.tts
      );
      return filled;
    }

    // No translation exists — machine translate entire script
    const original = await this.translations.getOriginal(campaignId);
    const machineTranslated = await this.translateScript(original, language);
    
    return {
      ...machineTranslated,
      quality: 'machine',
      completeness: 1.0
    };
  }

  async renderScript(template, language, context) {
    // Get raw template in target language
    const scriptContent = await this.getScriptContent(
      context.campaign.id,
      language
    );

    // Template rendering handles token replacement (tokens are language-agnostic)
    const tokenized = this.tokenEngine.replaceTokens(scriptContent.content, context);

    // Handle ICU MessageFormat (pluralization, gender, etc.)
    const icuFormatted = this.processICUMessageFormat(
      tokenized,
      language,
      context
    );

    return {
      text: icuFormatted,
      language,
      quality: scriptContent.quality,
      ttsVoice: this.getTTSVoice(language, scriptContent.quality)
    };
  }

  processICUMessageFormat(text, language, context) {
    // Handle {count, plural, one {# item} other {# items}}
    // and gender-based variations
    const icuPattern = /\{([^}]+)\}/g;
    
    return text.replace(icuPattern, (match, expression) => {
      const parts = expression.split(',');
      if (parts.length < 3) return match;

      const variable = parts[0].trim();
      const category = parts[1].trim();
      const value = this.resolveVariable(variable, context);

      if (category === 'plural') {
        const forms = {};
        for (let i = 2; i < parts.length; i++) {
          const formMatch = parts[i].match(/(\w+)\s+\{(.+)\}/);
          if (formMatch) {
            forms[formMatch[1]] = formMatch[2];
          }
        }

        // CLDR plural rules for the language
        const pluralForm = this.getPluralForm(value, language);
        return forms[pluralForm] || forms['other'] || '';
      }

      return match;
    });
  }

  getPluralForm(value, language) {
    // CLDR plural rules vary by language
    // English: one (1), other (0,2+)
    // Russian: one (1), few (2-4), many (5+), other
    // Japanese: other (all)
    const rules = {
      'en': (n) => n === 1 ? 'one' : 'other',
      'es': (n) => n === 1 ? 'one' : 'other',
      'ru': (n) => {
        if (n % 10 === 1 && n % 100 !== 11) return 'one';
        if (n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 10 || n % 100 >= 20)) return 'few';
        return 'other';
      },
      'ja': () => 'other',
      'zh': () => 'other',
    };

    const rule = rules[language] || rules['en'];
    return rule(value);
  }

  getTTSVoice(language, quality) {
    const voiceMap = {
      'en': { neural: 'en-US-Neural2-J', standard: 'en-US-Standard-C' },
      'es': { neural: 'es-ES-Neural2-B', standard: 'es-ES-Standard-A' },
      'fr': { neural: 'fr-FR-Neural2-D', standard: 'fr-FR-Standard-A' },
      'de': { neural: 'de-DE-Neural2-B', standard: 'de-DE-Standard-A' },
      'zh': { neural: 'cmn-CN-Neural2-A', standard: 'cmn-CN-Standard-A' },
      'ja': { neural: 'ja-JP-Neural2-B', standard: 'ja-JP-Standard-A' },
    };

    const voices = voiceMap[language] || voiceMap['en'];
    return quality === 'professional' ? voices.neural : voices.standard;
  }
}

class TranslationManagementUI {
  async getTranslationProgress(campaignId) {
    const campaign = await this.getCampaign(campaignId);
    const languages = campaign.targetLanguages;
    const totalSegments = await this.countSegments(campaign.scriptId);
    
    const progress = [];
    for (const lang of languages) {
      const translated = await this.countTranslated(campaign.scriptId, lang);
      progress.push({
        language: lang,
        translatedSegments: translated,
        totalSegments,
        completeness: translated / totalSegments,
        lastUpdated: await this.getLastUpdate(campaign.scriptId, lang)
      });
    }

    return progress;
  }
}
```

## Integration Points

- **TTS Service (Part 04):** Voice selection per language for script execution
- **Contact Service (Ch 02):** Contact language preference from profile
- **Translation API (Google Cloud / DeepL):** Machine translation for missing translations
- **Language Detection Service:** Phone number to country to language detection
- **Campaign Configuration (Ch 01):** Campaign target languages configuration
- **Analytics (Ch 09):** Language-specific performance tracking

## Open-Source Tools

- **ICU4X / intl-messageformat:** ICU MessageFormat parsing and formatting
- **i18next:** Internationalization framework with translation management
- **Polyglot.js:** AirBnB's internationalization library with pluralization
- **Google Cloud TTS / Azure Speech:** Neural TTS voices per language
- **DeepL API / Google Translate:** Machine translation for fallback
- **cldr-core:** CLDR plural rules database

## Production Considerations

- Translations should be reviewed by native speakers before deployment — machine translation quality varies by language pair
- Right-to-left (RTL) languages (Arabic, Hebrew) require UI adjustments in script editors and preview panels
- Token values may need language-specific formatting — dates (MM/DD vs DD/MM), currencies, number formats
- Language detection from phone numbers is approximate — a US number may belong to a Spanish speaker
- TTS voice quality varies significantly by language — neural voices for some languages may not be available
- Translation completeness should be monitored — campaigns launching with incomplete translations use fallback
- Cache translated scripts aggressively — translation is expensive and scripts change infrequently
- Provide translation memory (TM) — previously translated phrases are reused across campaigns
- Test multi-language scripts with native speakers to catch cultural inappropriateness, not just translation errors
- Monitor language distribution per campaign — if Spanish speakers are underserved, adjust targeting
