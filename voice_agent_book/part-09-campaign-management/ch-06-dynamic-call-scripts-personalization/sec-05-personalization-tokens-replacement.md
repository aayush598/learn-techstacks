# Section 05: Personalization Tokens & Replacement

## Overview

Personalization tokens are placeholders in script templates that get replaced with contact-specific data at render time. While the template variable system handles the core resolution, the token replacement system provides a simplified syntax for non-technical campaign managers, safe substitution with proper escaping, and comprehensive preview capabilities. Tokens are more limited than full template expressions but much simpler to use — users just insert `[FirstName]` or `[BusinessName]` into their script text.

The token system supports nested tokens, token chaining with fallbacks, conditional tokens that are replaced only when the contact has the associated data, and formatting directives within tokens (e.g., `[FirstName:capitalize]`). It also provides a token picker UI in the script editor that shows available tokens, their current values for the test contact, and preview of the rendered output.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Personalization Tokens & Replacement            │
├─────────────────────────────────────────────────────────────┤
│  Token Syntax Examples:                                     │
│                                                             │
│  [FirstName]          → "John"                             │
│  [FullName]           → "John Doe"                         │
│  [BusinessName]       → "Acme Corporation"                 │
│  [AccountBalance:currency] → "one hundred twenty-three"    │
│  [LastContactDate:relative] → "3 days ago"                │
│  [FirstName|Friend]   → "John" or "Friend" if no name     │
│  [[CompanyName]]      → Escaped literal "[CompanyName]"   │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Token Processing Pipeline                           │   │
│  │                                                      │   │
│  │  Raw Text: "Hi [FirstName], this is [AgentName]..."  │   │
│  │       │                                              │   │
│  │       ▼                                              │   │
│  │  Tokenizer: Find [Token] patterns                   │   │
│  │       │                                              │   │
│  │       ▼                                              │   │
│  │  Token Registry: Match to known tokens              │   │
│  │       │                                              │   │
│  │       ▼                                              │   │
│  │  Variable Resolution: Resolve token → value         │   │
│  │       │                                              │   │
│  │       ▼                                              │   │
│  │  Formatting: Apply formatter (currency, date, etc)  │   │
│  │       │                                              │   │
│  │       ▼                                              │   │
│  │  Escaping: Sanitize for safe text output            │   │
│  │       │                                              │   │
│  │       ▼                                              │   │
│  │  Rendered: "Hi John, this is Sarah from Acme..."    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Design Decisions

- **Bracket-delimited tokens:** Using `[TokenName]` rather than `{{variable.path}}` is simpler for non-technical users and visually distinct from other template syntax. Trade-off: limited expressiveness vs. user accessibility.

- **Automatic token discovery:** The token registry scans contact fields, campaign config, and computed variables to auto-discover available tokens. Users can also register custom tokens. Trade-off: discovery overhead vs. always-available token list.

- **Fallback chain in token syntax:** `[FirstName|ValuedCustomer]` means use FirstName if available, otherwise use "ValuedCustomer." This provides natural fallbacks without conditional blocks. Trade-off: syntax complexity vs. inline fallback convenience.

- **Pre-preview with test data:** Token replacement offers a real-time preview with a test contact, showing exactly how the rendered script will sound. This catches missing data issues before the campaign launches. Trade-off: preview computation overhead vs. quality assurance.

## Implementation Approach

```
class TokenReplacementEngine {
  constructor(tokenRegistry, variableResolver) {
    this.registry = tokenRegistry;
    this.resolver = variableResolver;
    this.tokenPattern = /\[([\w]+(?:\|[\w\s]+)?(?::\w+)?)\]/g;
    this.escapePattern = /\[\[([\w]+)\]\]/g;
  }

  replaceTokens(text, context) {
    if (!text) return '';

    // Handle escaped tokens first [[Token]] → [Token]
    text = text.replace(this.escapePattern, '[$1]');

    // Replace actual tokens
    return text.replace(this.tokenPattern, (match, tokenExpression) => {
      return this.resolveToken(tokenExpression, context);
    });
  }

  resolveToken(tokenExpression, context) {
    // Parse token expression: [TokenName|Fallback:format]
    const parts = this.parseTokenExpression(tokenExpression);
    
    const tokenDef = this.registry.get(parts.tokenName);
    if (!tokenDef) {
      // Unknown token — return original
      return tokenExpression;
    }

    // Resolve value
    let value = this.resolver.resolve(tokenDef.source, tokenDef.field, context);
    
    // Apply fallback if value is empty
    if ((value === null || value === undefined || value === '') && parts.fallback) {
      value = parts.fallback;
    }

    // Apply formatting
    if (parts.format) {
      value = this.applyFormat(value, parts.format);
    }

    // Sanitize for text output
    return this.sanitize(value);
  }

  parseTokenExpression(expression) {
    const parts = {
      tokenName: expression,
      fallback: null,
      format: null
    };

    // Check for format: [Token:format]
    const formatMatch = expression.match(/^([^:]+):(\w+)$/);
    if (formatMatch) {
      parts.tokenName = formatMatch[1];
      parts.format = formatMatch[2];
    }

    // Check for fallback: [Token|Fallback]
    const fallbackMatch = parts.tokenName.match(/^([^|]+)\|(.+)$/);
    if (fallbackMatch) {
      parts.tokenName = fallbackMatch[1];
      parts.fallback = fallbackMatch[2];
    }

    return parts;
  }

  applyFormat(value, format) {
    if (value === null || value === undefined) return '';

    switch (format) {
      case 'uppercase':
        return String(value).toUpperCase();
      case 'lowercase':
        return String(value).toLowerCase();
      case 'capitalize':
        return String(value).replace(/\b\w/g, c => c.toUpperCase());
      case 'currency':
        return this.formatCurrency(value);
      case 'number':
        return this.formatNumber(value);
      case 'date':
        return this.formatDate(value);
      case 'relative_date':
        return this.formatRelativeDate(value);
      case 'phone':
        return this.formatPhone(value);
      case 'masked':
        // Show only last 4 digits: ****1234
        const s = String(value);
        return '*'.repeat(Math.max(0, s.length - 4)) + s.slice(-4);
      default:
        return String(value);
    }
  }

  sanitize(value) {
    // Prevent injection of template syntax in values
    return String(value)
      .replace(/\[/g, '\\[')
      .replace(/\]/g, '\\]')
      .replace(/\{\{/g, '\\{\\{')
      .replace(/\}\}/g, '\\}\\}');
  }
}

class TokenRegistry {
  constructor() {
    this.tokens = new Map();
    this.registerDefaultTokens();
  }

  register(tokenName, definition) {
    this.tokens.set(tokenName, definition);
  }

  get(tokenName) {
    return this.tokens.get(tokenName);
  }

  getAllTokens() {
    return Array.from(this.tokens.entries()).map(([name, def]) => ({
      name,
      description: def.description,
      example: def.example,
      category: def.category
    }));
  }

  registerDefaultTokens() {
    // Contact tokens
    this.register('FirstName', {
      source: 'contact', field: 'firstName',
      description: "Contact's first name",
      example: 'John', category: 'contact'
    });
    this.register('LastName', {
      source: 'contact', field: 'lastName',
      description: "Contact's last name",
      example: 'Doe', category: 'contact'
    });
    this.register('FullName', {
      source: 'computed', field: 'fullName',
      description: "Contact's full name",
      example: 'John Doe', category: 'contact'
    });
    this.register('PhoneNumber', {
      source: 'contact', field: 'phone',
      description: "Contact's phone number (formatted)",
      example: '(555) 123-4567', category: 'contact'
    });

    // Campaign tokens
    this.register('BusinessName', {
      source: 'campaign', field: 'businessName',
      description: 'Your business name',
      example: 'Acme Corp', category: 'campaign'
    });
    this.register('AgentName', {
      source: 'agent', field: 'name',
      description: 'AI agent name',
      example: 'Sarah', category: 'campaign'
    });
    this.register('CallPurpose', {
      source: 'campaign', field: 'callPurpose',
      description: 'Purpose of this call',
      example: 'follow up on your recent order', category: 'campaign'
    });

    // CRM tokens
    this.register('AccountBalance', {
      source: 'crm', field: 'accountBalance',
      description: 'Current account balance',
      example: '$123.45', category: 'crm'
    });
    this.register('LastOrderDate', {
      source: 'crm', field: 'lastOrderDate',
      description: 'Date of last order',
      example: 'March 15th', category: 'crm'
    });
    
    // Computed tokens
    this.register('DaysSinceContact', {
      source: 'computed', field: 'daysSinceLastContact',
      description: 'Days since last contact',
      example: '5', category: 'computed'
    });
    this.register('CurrentTime', {
      source: 'call', field: 'currentTime',
      description: 'Current time (formatted for speech)',
      example: '2:30 PM', category: 'computed'
    });
  }
}

// Token Preview System
class TokenPreviewService {
  constructor(tokenEngine, contactService) {
    this.tokenEngine = tokenEngine;
    this.contacts = contactService;
  }

  async previewTemplate(templateText, campaignId, testContactId) {
    const contact = await this.contacts.getById(testContactId);
    
    const context = {
      contact,
      campaign: { id: campaignId, /* ... campaign data */ },
      call: { currentTime: new Date() },
      agent: { name: 'Test Agent' }
    };

    const rendered = this.tokenEngine.replaceTokens(templateText, context);

    // Also generate token usage report
    const usedTokens = this.extractUsedTokens(templateText);
    const tokenStatuses = await this.getTokenStatuses(usedTokens, context);

    return {
      rendered,
      tokenStatuses,
      warnings: tokenStatuses
        .filter(t => t.status === 'missing')
        .map(t => `Token "${t.token}" has no value — using fallback or empty`)
    };
  }

  extractUsedTokens(text) {
    const tokens = [];
    const regex = /\[([\w]+(?:\|[\w\s]+)?(?::\w+)?)\]/g;
    let match;
    while ((match = regex.exec(text)) !== null) {
      tokens.push(match[1]);
    }
    return [...new Set(tokens)];
  }

  async getTokenStatuses(tokens, context) {
    return tokens.map(token => {
      const resolved = this.tokenEngine.resolveToken(token, context);
      return {
        token,
        resolved: resolved !== token,
        value: resolved,
        status: resolved === token ? 'missing' : 'resolved'
      };
    });
  }
}
```

## Integration Points

- **Script Editor UI:** Token picker and preview panel for non-technical users
- **Template Engine (sec-01):** Token replacement runs as a preprocessing step before template rendering
- **Variable Resolver (sec-02):** Resolves token values through the variable resolution system
- **CRM Injection (sec-04):** CRM tokens trigger real-time data fetching
- **Campaign Config:** Token definitions include campaign-scoped defaults
- **Preview System:** Shows rendered output with test contact data

## Open-Source Tools

- **React (Draft.js / TipTap):** Rich text editor with token autocomplete
- **lodash.get:** Safe nested value extraction for token resolution
- **date-fns / Luxon:** Date formatting for token date output
- **num-words:** Number-to-words conversion for natural speech
- **Fuse.js:** Token search and autocomplete in the editor

## Production Considerations

- Unknown tokens should be left as-is in the rendered output with a clear warning, not silently removed
- Token preview should use the same resolution pipeline as actual calls to ensure preview accuracy
- Token usage analytics show which tokens are used most/least — identifies unnecessary personalization
- Missing token values should be logged but should not fail the call — tokens are not critical
- Token injection attack prevention: sanitize token values to prevent template injection
- Long token values (e.g., long company names) should be truncated for natural conversation flow
- Token format options should be discoverable in the token picker UI
- Testing tokens with boundary values (empty, very long, special characters) prevents rendering surprises
- Cache token resolutions aggressively — the same tokens are resolved for all contacts in a campaign
- Provide a token compatibility check for campaigns running in multiple languages
