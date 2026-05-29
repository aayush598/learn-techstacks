# Section 06: Browser vs Node.js Runtime

## Overview

The SDK supports both browser and Node.js runtimes, adapting to each environment's capabilities. Browser usage requires different transport mechanisms (fetch API, EventSource) while Node.js provides additional features (WebSocket, file system, environment variables). Runtime detection is automatic, and environment-specific code is isolated behind abstractions.

## Architecture

```
Runtime Detection & Adaptation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Feature                     Browser             Node.js
──────────────────────────────────────────────────────────
HTTP Transport              fetch API           fetch (native)
WebSocket                   WebSocket API       ws module
SSE                         EventSource         Custom impl
Environment Variables       N/A                 process.env
File System                 N/A                 fs module
Crypto                      crypto.subtle       node:crypto
Streaming                   ReadableStream      Node streams
Polyfills                   None needed         None needed

Runtime Detection:
  export function isBrowser(): boolean {
    return typeof window !== 'undefined' && typeof window.document !== 'undefined';
  }

  export function isNode(): boolean {
    return typeof process !== 'undefined'
      && process.versions != null
      && process.versions.node != null;
  }

Transport Selection:
  SDK detects runtime → selects appropriate transport
  → Browser: fetch + EventSource + WebSocket API
  → Node.js: fetch (Node 18+) + custom SSE + ws
```

## Design Decisions

- **Native fetch in Both Runtimes**: Node.js 18+ has native fetch; no isomorphic-fetch polyfill needed
- **Environment-Specific WebSocket**: Use global WebSocket in browser; import 'ws' in Node.js
- **No DOM Dependency**: SDK works in Web Workers and Service Workers where document is unavailable
- **Conditional Imports**: Node-specific modules imported via dynamic imports or exports package.json conditions

## Implementation Approach

```typescript
// Runtime detection
const Runtime = {
  isBrowser(): boolean {
    return typeof window !== 'undefined'
      && typeof window.document !== 'undefined';
  },

  isNode(): boolean {
    return typeof process !== 'undefined'
      && process.versions != null
      && process.versions.node != null;
  },

  isWebWorker(): boolean {
    return typeof self !== 'undefined'
      && typeof (self as unknown as { WorkerGlobalScope: unknown }).WorkerGlobalScope !== 'undefined';
  },

  getRuntime(): 'browser' | 'node' | 'web-worker' | 'unknown' {
    if (this.isBrowser()) return 'browser';
    if (this.isNode()) return 'node';
    if (this.isWebWorker()) return 'web-worker';
    return 'unknown';
  },
};

// Transport abstraction
interface TransportFactory {
  createFetch(): typeof fetch;
  createWebSocket(url: string, protocols?: string[]): WebSocket;
  createEventSource(url: string): EventSource;
  getCrypto(): Crypto;
}

// Browser transport
class BrowserTransport implements TransportFactory {
  createFetch(): typeof fetch {
    return globalThis.fetch.bind(globalThis);
  }

  createWebSocket(url: string): WebSocket {
    return new WebSocket(url);
  }

  createEventSource(url: string): EventSource {
    return new EventSource(url);
  }

  getCrypto(): Crypto {
    return globalThis.crypto;
  }
}

// Node.js transport
class NodeTransport implements TransportFactory {
  private fetchImpl: typeof fetch | null = null;

  createFetch(): typeof fetch {
    // Node 18+ has native fetch
    return globalThis.fetch.bind(globalThis);
  }

  createWebSocket(url: string): WebSocket {
    // Use 'ws' package in Node.js
    const { WebSocket: WsWebSocket } = require('ws') as typeof import('ws');
    return new WsWebSocket(url);
  }

  createEventSource(url: string): EventSource {
    // Use 'eventsource' package or custom implementation
    const { EventSource: NodeEventSource } = require('eventsource') as typeof import('eventsource');
    return new NodeEventSource(url);
  }

  getCrypto(): Crypto {
    const { webcrypto } = require('node:crypto') as typeof import('node:crypto');
    return webcrypto as unknown as Crypto;
  }
}

// Runtime-adaptive HTTP client
class AdaptiveHttpClient {
  private transport: TransportFactory;

  constructor() {
    if (Runtime.isBrowser() || Runtime.isWebWorker()) {
      this.transport = new BrowserTransport();
    } else {
      this.transport = new NodeTransport();
    }
  }

  async request<T>(method: string, url: string, options?: RequestOptions): Promise<T> {
    const fetch = this.transport.createFetch();
    const response = await fetch(url, {
      method,
      headers: options?.headers,
      body: options?.body ? JSON.stringify(options.body) : undefined,
      signal: options?.signal,
    });

    if (!response.ok) {
      throw await this.parseError(response);
    }

    return response.json();
  }

  async *stream<T>(url: string, options?: RequestOptions): AsyncGenerator<T> {
    const fetch = this.transport.createFetch();
    const response = await fetch(url, {
      method: 'GET',
      headers: options?.headers,
      signal: options?.signal,
    });

    if (!response.ok) {
      throw await this.parseError(response);
    }

    const reader = response.body?.getReader();
    if (!reader) return;

    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');

      for (let i = 0; i < lines.length - 1; i++) {
        if (lines[i].startsWith('data: ')) {
          try {
            yield JSON.parse(lines[i].slice(6));
          } catch {
            // Skip malformed SSE data
          }
        }
      }

      buffer = lines[lines.length - 1];
    }
  }
}

// package.json exports for conditional imports
{
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.mjs"
    },
    "./node": {
      "types": "./dist/node/index.d.ts",
      "import": "./dist/node/index.mjs",
      "require": "./dist/node/index.cjs"
    }
  }
}

// Node-specific features
export class NodeVoiceAgent extends VoiceAgent {
  constructor(config: VoiceAgentConfig) {
    super({ ...config, runtime: 'node' });
  }

  // Node-specific: load config from file
  static async fromConfigFile(path: string): Promise<NodeVoiceAgent> {
    const fs = await import('node:fs/promises');
    const config = JSON.parse(await fs.readFile(path, 'utf-8'));
    return new NodeVoiceAgent(config);
  }
}
```

## Integration Points

- **Bundler Configuration**: ESM-first exports; bundlers like webpack, Rollup, tsup handle tree-shaking
- **CDN Distribution**: UMD bundle for direct browser usage via CDN
- **Environment Detection**: Automatic runtime detection — no manual configuration needed

## Production Considerations

- **Bundle Size Check**: Verify browser bundle size (< 15KB gzipped) in CI
- **Node.js Version**: Require Node.js 18+ for native fetch support
- **Polyfill Documentation**: Document required polyfills for older environments (IE11)
- **SSR Compatibility**: Ensure SDK works in server-side rendering contexts (Next.js, Nuxt)

## Open-Source Tools

- **tsup**: Build ESM and CJS outputs for different runtimes
- **ws**: WebSocket library for Node.js
- **eventsource**: SSE implementation for Node.js
