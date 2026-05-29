# Section 07: CLI Testing & Distribution

## Overview

The CLI is tested with snapshot testing for output consistency, mocked API servers for integration tests, and end-to-end tests against the sandbox environment. Distribution uses npm for the TypeScript CLI and PyPI for the Python version, with executable packaging via pkg or PyInstaller.

## Architecture

```
Testing Strategy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Snapshot Testing (Output Consistency):
  Command: voiceagent agents list --output json
  Saved Snapshot: __snapshots__/agents-list.json
  Test: Run command → Compare output with saved snapshot
  Failure: Output format changed — update snapshot

Mock API Server Testing:
  [CLI] → [Mock HTTP Server (MSW)]
              │
         Returns fixture data
              │
  Test: Verify CLI behavior with controlled API responses
        - Error handling
        - Pagination
        - Rate limiting

E2E Testing:
  [CLI] → [Sandbox API (real)]
              │
  Test: Full workflow tests
    - Create agent, verify output
    - Deploy agent, verify status
    - List agents, verify pagination

Distribution Methods:
  npm package:  @voiceagent/cli    → npx voiceagent
  PyPI package: voiceagent-cli     → pipx install voiceagent-cli
  Docker image: voiceagent/cli     → docker run voiceagent/cli
  Standalone:   pkg binary         → Download from GitHub Releases

Installation Comparison:
  $ npx @voiceagent/cli agents list        # npm (requires Node)
  $ pipx run voiceagent-cli agents list    # Python (requires Python)
  $ docker run voiceagent/cli agents list  # Docker (requires Docker)
  $ ./voiceagent-linux agents list         # Binary (no deps needed)
```

## Design Decisions

- **Snapshot Testing**: Catch regressions in output formatting automatically
- **Mock API Server**: Fast, deterministic tests without network dependency
- **Multiple Distribution Channels**: npm, PyPI, Docker, and standalone binaries
- **Binary Packaging**: pkg bundles Node.js runtime for zero-dependency executable

## Implementation Approach

```typescript
// Snapshot test example (Vitest)
import { describe, it, expect } from 'vitest';
import { execSync } from 'node:child_process';
import path from 'node:path';

const CLI_PATH = path.resolve(__dirname, '../dist/cli.mjs');

function runCli(args: string[], env?: Record<string, string>): string {
  return execSync(`node ${CLI_PATH} ${args.join(' ')}`, {
    encoding: 'utf-8',
    env: { ...process.env, VOICE_AGENT_API_KEY: 'va_test_abc', ...env },
  });
}

describe('CLI Snapshot Tests', () => {
  it('should list agents in JSON format', () => {
    const output = runCli(['agents', 'list', '--output', 'json']);
    expect(JSON.parse(output)).toMatchSnapshot();
  });

  it('should get agent details in YAML format', () => {
    const output = runCli(['agents', 'get', 'ag_abc', '--output', 'yaml']);
    expect(output).toMatchSnapshot();
  });

  it('should output error for invalid agent ID', () => {
    expect(() => {
      runCli(['agents', 'get', 'nonexistent']);
    }).toThrow();
  });
});

// Integration test with mock API
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';

const mockServer = setupServer(
  http.get('https://api.sandbox.voiceagent.com/v1/agents', () => {
    return HttpResponse.json({
      data: [
        { id: 'ag_1', name: 'Test Agent', status: 'active', createdAt: '2025-01-01T00:00:00Z' },
      ],
      pagination: { cursor: null, hasMore: false },
    });
  }),
);

describe('CLI Integration Tests', () => {
  beforeAll(() => mockServer.listen({ onUnhandledRequest: 'bypass' }));
  afterEach(() => mockServer.resetHandlers());
  afterAll(() => mockServer.close());

  it('should list agents from mocked API', () => {
    const output = runCli(
      ['agents', 'list', '--output', 'json', '--environment', 'sandbox'],
      { VOICE_AGENT_API_KEY: 'va_test_abc' },
    );
    const result = JSON.parse(output);
    expect(result.data).toHaveLength(1);
  });
});

// Binary packaging with pkg
// package.json
{
  "bin": {
    "voiceagent": "./dist/cli.mjs"
  },
  "pkg": {
    "targets": [
      "node18-linux-x64",
      "node18-macos-x64",
      "node18-win-x64"
    ],
    "output": "bin/"
  },
  "scripts": {
    "build:binary": "pkg . --compress GZip",
    "build:docker": "docker build -t voiceagent/cli ."
  }
}

// Dockerfile
FROM node:18-alpine
RUN npm install -g @voiceagent/cli
ENTRYPOINT ["voiceagent"]

// GitHub release workflow
// .github/workflows/release.yml
name: Release CLI

on:
  push:
    tags: ['cli-v*']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run build
      - run: npm run build:binary
      - uses: softprops/action-gh-release@v1
        with:
          files: bin/*
          body_path: CHANGELOG.md
```

## Integration Points

- **CircleCI/GitHub Actions**: CI runs tests, builds binaries, and publishes releases
- **npm Registry**: `npm publish` for package distribution
- **Docker Hub**: `docker push` for container image
- **Homebrew**: Optional Homebrew formula for macOS users

## Production Considerations

- **Binary Size**: pkg binary is ~40MB (includes Node.js runtime); consider smaller alternatives
- **Platform Support**: Build binaries for linux-x64, macOS-x64/arm64, win-x64
- **Auto-Update**: Built-in `voiceagent update` command checks for new versions
- **Integrity Verification**: SHA-256 checksums published with releases

## Open-Source Tools

- **pkg**: Package Node.js applications into standalone executables
- **MSW (Mock Service Worker)**: HTTP request mocking for CLI tests
- **Vitest**: Fast test runner with snapshot support
- **Docker**: Container-based distribution
