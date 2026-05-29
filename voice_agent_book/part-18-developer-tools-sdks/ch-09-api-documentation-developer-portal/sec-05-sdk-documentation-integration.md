# Section 05: SDK Documentation Integration

## Overview

SDK documentation is integrated into the developer portal alongside API reference docs. TypeScript and Python SDK docs are auto-generated from source code comments (TypeDoc, Sphinx) and linked from the portal. Versioning matches SDK versions to API versions, ensuring users see docs for the SDK version they're using.

## Architecture

```
SDK Documentation Integration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[SDK Source Code] → [Doc Generator] → [Static HTML] → [Developer Portal]
     │                     │
TypeScript SDK        TypeDoc          docs/sdks/typescript/
  → TSDoc comments       → HTML pages     → searchable, versioned
  → Decorators           → API reference  → linked from portal

Python SDK            Sphinx           docs/sdks/python/
  → Docstrings           → HTML pages     → searchable, versioned
  → Google-style         → API reference  → linked from portal

Portal Integration:
  docs.voiceagent.com/sdks/
  ├── typescript/
  │   ├── index.md          → Getting started with TS SDK
  │   ├── installation.md   → npm install @voiceagent/sdk
  │   ├── usage.md          → Basic usage examples
  │   └── api/
  │       └── index.html    → TypeDoc-generated API reference
  └── python/
      ├── index.md          → Getting started with Python SDK
      ├── installation.md   → pip install voice-agent-sdk
      ├── usage.md          → Basic usage examples
      └── api/
          └── index.html    → Sphinx-generated API reference

Cross-Referencing:
  API Reference → "See TypeScript SDK docs" ↗
  SDK Docs → "See API Reference for full endpoint details" ↗
```

## Design Decisions

- **TypeDoc for TypeScript**: Standard tool; outputs HTML pages; supports versioning
- **Sphinx for Python**: Standard tool; Read the Docs theme; supports versioning
- **Separate Build, Integrated Display**: SDK docs built separately, embedded via iframe or SSG import
- **Versioned SDK Docs**: Each SDK version has corresponding documentation subdirectory

## Implementation Approach

```typescript
// TypeDoc configuration
// tsconfig.json (SDK project)
{
  "typedocOptions": {
    "entryPoints": ["src/index.ts"],
    "out": "docs/api",
    "plugin": ["typedoc-plugin-markdown"],
    "theme": "docusaurus",
    "excludePrivate": true,
    "excludeProtected": true,
    "includeVersion": true
  }
}

// Build script for SDK docs
// package.json
{
  "scripts": {
    "docs:generate": "typedoc",
    "docs:build": "npm run docs:generate && docusaurus build"
  }
}

// Sphinx configuration (Python SDK)
// docs/conf.py
import os
import sys

sys.path.insert(0, os.path.abspath('../'))

project = 'Voice Agent Python SDK'
copyright = '2025, Voice Agent'
author = 'Voice Agent Team'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # Google-style docstrings
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx_autodoc_typehints',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

// Docusaurus integration — embed SDK docs
// docs/sdks/typescript.md
---
title: TypeScript SDK
sidebar_label: TypeScript
---

import TypeDocEmbed from '@site/src/components/TypeDocEmbed';

# TypeScript SDK

The TypeScript SDK provides a typed interface for the Voice Agent API.

## Installation

```bash npm2yarn
npm install @voiceagent/sdk
```

## Quick Start

```typescript
import { VoiceAgent } from '@voiceagent/sdk';

const client = new VoiceAgent({
  apiKey: process.env.VOICE_AGENT_API_KEY,
});

const agents = await client.agents.list();
console.log(agents);
```

## API Reference

<TypeDocEmbed src="/sdks/typescript/api/index.html" />

## Version Compatibility

| SDK Version | API Version | Status |
|------------|-------------|--------|
| 2.x        | v2          | Current |
| 1.x        | v1          | Legacy |
```

## Integration Points

- **Docusaurus Plugin**: Custom plugin to embed TypeDoc/Sphinx output
- **CI/CD Pipeline**: SDK docs built and deployed on SDK release
- **Search Indexing**: SDK documentation indexed by Algolia alongside API docs

## Production Considerations

- **Cross-Reference Links**: Maintain bidirectional links between API docs and SDK docs
- **Documentation Testing**: SDK code examples tested in CI for correctness
- **Version Switcher**: SDK version selector in documentation header
- **Deprecation Banners**: Show deprecation notice for outdated SDK versions

## Open-Source Tools

- **TypeDoc**: TypeScript documentation generator
- **Sphinx**: Python documentation generator
- **Read the Docs Sphinx Theme**: Clean documentation theme
