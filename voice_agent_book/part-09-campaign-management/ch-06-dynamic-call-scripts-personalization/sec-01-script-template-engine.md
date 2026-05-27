# Section 01: Script Template Engine

## Overview

The script template engine is the core rendering system that converts campaign script templates into personalized, context-aware dialogue for AI agents. Templates contain static text combined with dynamic variables, conditional blocks, and control flow constructs. The engine processes these templates at call time, injecting contact data, CRM information, and campaign context to produce a natural, personalized script that the AI agent follows during the call.

The template engine must support complex variable interpolation with fallbacks, conditional sections (if/else based on contact attributes or call context), looping constructs for lists, and nested templates. It must also handle sanitization of injected data to prevent injection attacks and ensure proper grammar (e.g., gender agreement in languages with grammatical gender). The engine outputs structured script segments that the AI agent uses as conversation guides, not rigid word-for-word scripts.

## Architecture

```
+----------+    +----------+    +----------+    +----------+    +----------+
| Audio    |--->| WebSocket|--->| Jitter   |--->| PLC      |--->| Player   |
| Producer |    | (WSS)    |    | Buffer   |    | (Packet  |    | (smooth  |
| (100ms   |    | (binary) |    | (adaptive|    |  Loss    |    |  output) |
|  chunks) |    |          |    |  60-200) |    |  Conceal)|    +----------+
+----------+    +----------+    +----------+    +----------+
```


## Design Decisions

- **Provider Abstraction**: All STT providers implement a common interface. Enables seamless failover (Deepgram -> Whisper -> Web Speech API) without code changes.
- **VAD Gating**: Reduces STT costs by 40-60% by not billing silence. VAD miss rate must be <1%.
- **Audio Normalization**: 16kHz mono PCM via Kaiser-window resampling ensures consistent quality across diverse input codecs.
## Implementation Approach

```
class ScriptTemplateEngine {
  constructor(sandbox, helpers) {
    this.sandbox = sandbox;
    this.helpers = { ...defaultHelpers, ...helpers };
    this.cache = new TemplateCache();
  }

  parse(templateSource) {
    // Check cache first
    const cached = this.cache.get(templateSource);
    if (cached) return cached;

    const tokens = this.lex(templateSource);
    const ast = this.parse(tokens);
    
    // Validate AST
    this.validate(ast);
    
    // Cache the parsed AST
    this.cache.set(templateSource, ast);
    
    return ast;
  }

  render(ast, context) {
    const parts = [];

    for (const node of ast) {
      switch (node.type) {
        case 'text':
          parts.push(node.value);
          break;

        case 'variable':
          const resolved = this.resolveVariable(node.path, context, node.default);
          const sanitized = this.sanitize(resolved, node.format);
          parts.push(sanitized);
          break;

        case 'if':
          const condition = this.evaluateExpression(node.expression, context);
          if (condition) {
            parts.push(this.render(node.children, context));
          } else if (node.elseChildren) {
            parts.push(this.render(node.elseChildren, context));
          }
          break;

        case 'each':
          const list = this.resolveVariable(node.listPath, context);
          if (Array.isArray(list)) {
            for (const item of list) {
              const itemContext = { ...context, 'this': item, ...this.createLoopVars(item, list) };
              parts.push(this.render(node.children, itemContext));
            }
          }
          break;

        case 'helper':
          const helper = this.helpers[node.helperName];
          if (helper) {
            const args = node.args.map(a => this.resolveVariable(a, context));
            parts.push(helper(...args, context));
          }
          break;
      }
    }

    return parts.join('');
  }

  resolveVariable(path, context, defaultValue) {
    const parts = path.split('.');
    let current = context;

    for (const part of parts) {
      if (current === null || current === undefined) {
        return this.safeDefault(defaultValue);
      }
      current = current[part];
    }

    return current !== undefined ? current : this.safeDefault(defaultValue);
  }

  evaluateExpression(expr, context) {
    // Safe expression evaluator — limited to boolean operations
    switch (expr.type) {
      case 'variable':
        return !!this.resolveVariable(expr.path, context);
      case 'comparison':
        const left = this.resolveVariable(expr.left, context);
        const right = this.resolveVariable(expr.right, context);
        return this.compare(left, expr.operator, right);
      case 'and':
        return this.evaluateExpression(expr.left, context) && 
               this.evaluateExpression(expr.right, context);
      case 'or':
        return this.evaluateExpression(expr.left, context) || 
               this.evaluateExpression(expr.right, context);
      case 'not':
        return !this.evaluateExpression(expr.expression, context);
    }
  }

  lex(source) {
    const tokens = [];
    let i = 0;

    while (i < source.length) {
      // Text between template tags
      if (source[i] === '{' && source[i + 1] === '{') {
        const end = source.indexOf('}}', i + 2);
        if (end === -1) throw new Error('Unclosed template tag');
        
        const content = source.slice(i + 2, end).trim();
        i = end + 2;

        // Determine tag type
        if (content.startsWith('#')) {
          tokens.push({ type: 'block_open', value: content.slice(1).trim(), raw: content });
        } else if (content.startsWith('/')) {
          tokens.push({ type: 'block_close', value: content.slice(1).trim(), raw: content });
        } else {
          tokens.push({ type: 'expression', value: content, raw: content });
        }
      } else {
        // Plain text
        const nextTag = source.indexOf('{{', i);
        const text = nextTag === -1 ? source.slice(i) : source.slice(i, nextTag);
        tokens.push({ type: 'text', value: text });
        i = nextTag === -1 ? source.length : nextTag;
      }
    }

    return tokens;
  }

  parse(tokens) {
    const ast = [];
    const stack = [];

    for (let i = 0; i < tokens.length; i++) {
      const token = tokens[i];

      switch (token.type) {
        case 'text':
          ast.push({ type: 'text', value: token.value });
          break;

        case 'expression':
          ast.push(this.parseExpression(token.value));
          break;

        case 'block_open':
          stack.push({ node: this.parseBlock(token.value), children: [] });
          break;

        case 'block_close':
          const completed = stack.pop();
          if (stack.length > 0) {
            stack[stack.length - 1].children.push(completed.node);
          } else {
            ast.push(completed.node);
          }
          break;
      }
    }

    return ast;
  }

  sanitize(value, format) {
    if (value === null || value === undefined) return '';

    switch (format) {
      case 'uppercase': return String(value).toUpperCase();
      case 'lowercase': return String(value).toLowerCase();
      case 'capitalize': return String(value).replace(/^\w/, c => c.toUpperCase());
      case 'currency': return this.formatCurrency(value);
      case 'phone': return this.formatPhone(value);
      default: return String(value);
    }
  }

  formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  }

  formatPhone(phone) {
    const cleaned = String(phone).replace(/\D/g, '');
    if (cleaned.length === 10) {
      return `(${cleaned.slice(0, 3)}) ${cleaned.slice(3, 6)}-${cleaned.slice(6)}`;
    }
    return phone;
  }
}
```

## Integration Points

- **Campaign Configuration (Ch 01):** Script templates are defined per campaign
- **Contact Data Service (Ch 02):** Contact attributes provide variable values
- **CRM Integration (Part 10, Ch 02):** Real-time CRM data injection during rendering
- **AI Agent Runtime (Part 06):** Rendered script guides agent conversation
- **A/B Testing (Ch 10):** Script variants are tested through the template engine
- **Analytics (Ch 09):** Script performance tracking per template variant

## Open-Source Tools

- **ws** (MIT): WebSocket
- **MediaRecorder API**: Recording
- **Opus** (BSD): Audio codec
## Production Considerations

- Template parsing is CPU-intensive — cache parsed ASTs aggressively, invalidate only when templates change
- Per-call rendering should complete in under 5ms — pre-resolve static variables and cache when possible
- Templates should be pre-compiled during deployment to eliminate parsing latency at call time
- Variable resolution with deep nesting can be slow — limit to 3 levels deep (e.g., `contact.address.city`)
- Sandbox execution adds overhead — benchmark to ensure it doesn't impact call setup latency
- Template validation should catch undefined variables during save, not during call rendering
- Log rendering errors gracefully — a failed variable should show fallback value, not crash the call
- Monitor rendering failure rate — unexpectedly high rates indicate template or data issues
- Provide a template preview tool in the script editor showing rendered output with sample data
- Internationalization: the template engine must support UTF-8 and RTL text natively
