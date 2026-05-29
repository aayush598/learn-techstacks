# Section 01: Developer Portal Architecture

## Overview

The developer portal is a documentation-as-code site built with a static site generator (Docusaurus/MkDocs). It includes API reference docs, SDK docs, interactive playground, changelog, and support resources. The portal is versioned alongside the API and deployed as a static site via CDN.

## Architecture

```
Developer Portal Stack
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tech Stack:
  Framework:    Docusaurus (React-based static site)
  Styling:      Tailwind CSS + Radix UI
  Search:       Algolia DocSearch
  API Explorer: Scalar API Reference / Swagger UI
  Analytics:    Plausible / PostHog
  Hosting:      Vercel / Cloudflare Pages

Content Structure:
  docs.voiceagent.com/
  ├── getting-started/
  │   ├── quickstart.md           → 5-minute quickstart
  │   ├── authentication.md       → API key setup
  │   └── your-first-call.md      → Making first API call
  ├── api-reference/
  │   ├── agents.md               → OpenAPI-generated reference
  │   ├── calls.md
  │   ├── campaigns.md
  │   ├── webhooks.md
  │   └── analytics.md
  ├── sdks/
  │   ├── typescript.md           → TypeScript SDK docs
  │   ├── python.md               → Python SDK docs
  │   └── cli.md                  → CLI reference
  ├── guides/
  │   ├── voice-agent-basics.md
  │   ├── real-time-transcription.md
  │   ├── outbound-campaigns.md
  │   └── webhook-integration.md
  ├── changelog/
  │   └── index.md                → Auto-generated from commits
  └── support/
      ├── faq.md
      └── contact.md
```

## Design Decisions

- **Docusaurus Over GitBook**: Full control over UI, React components, versioning
- **Documentation-as-Code**: Content in markdown, versioned in git, built via CI
- **Versioned Documentation**: Each API version has corresponding doc version
- **SEO Optimization**: Static HTML generated at build time for search engines

## Implementation Approach

```typescript
// docusaurus.config.js
module.exports = {
  title: 'Voice Agent API Docs',
  tagline: 'Build intelligent voice agents',
  url: 'https://docs.voiceagent.com',
  baseUrl: '/',
  organizationName: 'voiceagent',
  projectName: 'docs',

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/voiceagent/docs/edit/main',
          lastVersion: 'current',
          versions: {
            current: { label: 'v2 (latest)', path: 'v2' },
            v1: { label: 'v1 (legacy)', path: 'v1' },
          },
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],

  themeConfig: {
    navbar: {
      title: 'Voice Agent',
      logo: { alt: 'Logo', src: 'img/logo.svg' },
      items: [
        { to: '/docs/getting-started', label: 'Docs', position: 'left' },
        { to: '/docs/api-reference', label: 'API Reference', position: 'left' },
        { to: '/docs/changelog', label: 'Changelog', position: 'left' },
        { type: 'docsVersionDropdown', position: 'right' },
        {
          href: 'https://dashboard.voiceagent.com',
          label: 'Dashboard',
          position: 'right',
        },
      ],
    },
    algolia: {
      appId: 'YOUR_APP_ID',
      apiKey: 'YOUR_SEARCH_API_KEY',
      indexName: 'voiceagent',
    },
  },

  plugins: [
    // OpenAPI integration
    [
      'docusaurus-plugin-openapi-docs',
      {
        id: 'api-reference',
        docsPluginId: 'classic',
        config: {
          voiceagent: {
            specPath: 'specs/openapi.yaml',
            outputDir: 'docs/api-reference',
            sidebarOptions: { groupPathsBy: 'tag' },
          },
        },
      },
    ],
  ],
};

// sidebars.js
module.exports = {
  docs: [
    'getting-started/index',
    'getting-started/authentication',
    'getting-started/your-first-call',
    {
      type: 'category',
      label: 'API Reference',
      link: { type: 'doc', id: 'api-reference/index' },
      items: require('./docs/api-reference/sidebar.js'),
    },
    {
      type: 'category',
      label: 'SDKs',
      items: [
        'sdks/typescript',
        'sdks/python',
        'sdks/cli',
      ],
    },
    {
      type: 'category',
      label: 'Guides',
      items: [
        'guides/voice-agent-basics',
        'guides/real-time-transcription',
        'guides/outbound-campaigns',
        'guides/webhook-integration',
      ],
    },
    'changelog/index',
  ],
};
```

## Integration Points

- **CI/CD**: Documentation built and deployed on merge to main
- **API Spec**: OpenAPI spec auto-generated from code; doc site consumes it
- **Search**: Algolia crawler indexes documentation daily
- **Analytics**: Page views, search queries, and API explorer usage tracked

## Production Considerations

- **SEO**: Static generation with meta tags, sitemap, structured data
- **Performance**: Lighthouse score > 90; CDN caching for static assets
- **Accessibility**: WCAG 2.1 AA compliance for all documentation pages
- **Search Ranking**: Structured content with proper heading hierarchy

## Open-Source Tools

- **Docusaurus**: React-based static site generator
- **Scalar API Reference**: Interactive API documentation
- **Algolia DocSearch**: Full-text search with typo tolerance
