# Section 08: Search & Discovery

## Overview

Full-text search across all documentation enables developers to quickly find relevant content. Algolia DocSearch provides typo-tolerant search with instant results, faceted by content type (API reference, guides, SDK docs, changelog). Search analytics track popular queries to identify documentation gaps.

## Architecture

```
Search Architecture
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Documentation Build]
       │
  [DocSearch Crawler] ──→ [Algolia Index]
       │                        │
  Crawls docs.voiceagent.com    │
  Extracts content + metadata   │
  Builds search index           │
       │                        │
  [Developer Portal]            │
       │                        │
  [Search UI] ←───────────────│
    ├── Search box
    ├── Instant results
    ├── Faceted filters
    └── Analytics tracking

Search Features:
  - Typo tolerance: "agennt" → "agent"
  - Synonym groups: { "api key", "authentication", "auth" }
  - Faceted by: content type, version, SDK language
  - Keyboard shortcuts: Ctrl+K to open search
  - Recent searches
  - Popular searches

Search Analytics:
  Top Queries        ↓     # Searches
  ─────────────────────────────────────
  create agent              1,234
  webhook setup             987
  api key                   876
  pagination                654
  rate limit                543
  Missing Results           23 (→ create new docs)
```

## Design Decisions

- **Algolia DocSearch**: Free for open-source; handles crawling, indexing, and serving
- **Instant Search**: Results appear as user types (debounced 300ms)
- **Content Prioritization**: API reference results weighted higher than guide results
- **Search Analytics**: Identify documentation gaps by tracking queries with zero results

## Implementation Approach

```typescript
// Algolia DocSearch configuration
// docusaurus.config.js
themeConfig: {
  algolia: {
    appId: 'YOUR_APP_ID',
    apiKey: 'YOUR_SEARCH_API_KEY',
    indexName: 'voiceagent',
    contextualSearch: true,
    searchParameters: {
      facetFilters: ['version:current'],
    },
  },
}

// Custom crawler config (DocSearch config file)
// docsearch.json
{
  "index_name": "voiceagent",
  "start_urls": [
    {
      "url": "https://docs.voiceagent.com/docs/",
      "selectors_key": "docs"
    }
  ],
  "sitemap_urls": ["https://docs.voiceagent.com/sitemap.xml"],
  "selectors": {
    "docs": {
      "lvl0": {
        "selector": ".menu__link--active",
        "global": true,
        "default_value": "Documentation"
      },
      "lvl1": "header h1",
      "lvl2": "article h2",
      "lvl3": "article h3",
      "lvl4": "article h4",
      "text": "article p, article li, article td"
    }
  },
  "custom_settings": {
    "attributesForFaceting": [
      "version",
      "type",
      "language"
    ],
    "separatorsToIndex": "_",
    "synonyms": [
      ["api key", "apikey", "api_key", "authentication", "auth"],
      ["webhook", "webhook endpoint", "webhook setup"],
      ["sdk", "client library", "client"],
      ["pagination", "cursor", "paginate"]
    ]
  }
}

// Custom search component
function SearchBox() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    if (query.length < 2) {
      setResults([]);
      return;
    }

    const timer = setTimeout(async () => {
      const response = await fetch(
        `https://YOUR_APP_ID-dsn.algolia.net/1/indexes/voiceagent/query`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Algolia-API-Key': 'YOUR_SEARCH_API_KEY',
            'X-Algolia-Application-Id': 'YOUR_APP_ID',
          },
          body: JSON.stringify({
            query,
            hitsPerPage: 10,
            facetFilters: ['version:current'],
          }),
        },
      );

      const data = await response.json();
      setResults(data.hits);
    }, 300);

    return () => clearTimeout(timer);
  }, [query]);

  return (
    <div className="search-container">
      <div className="search-input-wrapper">
        <kbd>Ctrl+K</kbd>
        <input
          type="search"
          placeholder="Search documentation..."
          value={query}
          onChange={e => setQuery(e.target.value)}
          onFocus={() => setIsOpen(true)}
          onKeyDown={e => {
            if (e.key === 'Escape') setIsOpen(false);
          }}
        />
      </div>

      {isOpen && results.length > 0 && (
        <div className="search-results">
          {results.map(result => (
            <a
              key={result.objectID}
              href={result.url}
              className="search-result-item"
            >
              <div className="result-type">
                {result.type || 'Documentation'}
              </div>
              <div className="result-title">
                <Highlight text={result.title} query={query} />
              </div>
              <div className="result-content">
                <Highlight text={result._snippetResult?.content?.value || ''} query={query} />
              </div>
              <div className="result-breadcrumbs">
                {result.ancestors?.join(' › ')}
              </div>
            </a>
          ))}
        </div>
      )}

      {isOpen && query.length >= 2 && results.length === 0 && (
        <div className="search-no-results">
          No results found. Try different keywords.
        </div>
      )}
    </div>
  );
}

// Search analytics tracking
class SearchAnalytics {
  async trackSearch(query: string, resultCount: number): Promise<void> {
    await fetch('/api/v1/analytics/search', {
      method: 'POST',
      body: JSON.stringify({
        query,
        resultCount,
        timestamp: new Date().toISOString(),
        source: 'developer-portal',
      }),
    });
  }

  async getPopularSearches(limit = 10): Promise<Array<{ query: string; count: number }>> {
    const response = await fetch(`/api/v1/analytics/search/popular?limit=${limit}`);
    return response.json();
  }

  async getMissingResults(): Promise<Array<{ query: string; count: number }>> {
    const response = await fetch('/api/v1/analytics/search/missing');
    return response.json();
  }
}
```

## Integration Points

- **Algolia Dashboard**: Search analytics, index management, synonym configuration
- **Content Management**: Missing search results trigger content creation tickets
- **Versioned Search**: Facet by version to surface relevant documentation

## Production Considerations

- **Crawl Frequency**: DocSearch crawls daily or on-demand via webhook
- **Search Rate Limits**: Algolia free tier handles 10,000 searches/month; scale to paid as needed
- **Result Quality**: Continuously tune ranking, synonyms, and faceting based on analytics
- **Offline Fallback**: Basic client-side search when Algolia is unavailable

## Open-Source Tools

- **Algolia DocSearch**: Free search for documentation sites
- **Meilisearch**: Self-hosted alternative to Algolia
- **Lunr.js**: Client-side search fallback
