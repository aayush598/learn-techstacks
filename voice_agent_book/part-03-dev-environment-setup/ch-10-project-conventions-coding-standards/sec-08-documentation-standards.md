# Section 08: Documentation Standards

## Overview

Documentation follows a tiered approach: JSDoc for public APIs, README files for package-level documentation, a changelog for release notes, and Architecture Decision Records (ADRs) for significant design choices. Each tier serves a different audience with a different level of detail. The goal is to document the "why" (decisions, trade-offs) and the "how" (usage, API) while letting the code itself document the "what".

## Documentation Tier Architecture

```text
┌──────────────────────────────────────────────────────────────┐
│                   Documentation Hierarchy                      │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  Tier 1: ADR (docs/adr/)                                      │
│  Audience: Current & future architects                        │
│  Content: Why we made significant decisions                   │
│  Format: Structured markdown (template below)                  │
│                                                               │
│  Tier 2: README (each package root)                            │
│  Audience: Developers using the package                       │
│  Content: What the package does, how to use it, API overview  │
│  Format: Markdown with code examples                          │
│                                                               │
│  Tier 3: JSDoc (in-source for public exports)                  │
│  Audience: Developers integrating with specific functions      │
│  Content: Parameter types, return values, exceptions, examples │
│  Format: TSDoc-compatible JSDoc annotations                   │
│                                                               │
│  Tier 4: README.md (project root)                              │
│  Audience: New developers joining the project                  │
│  Content: Getting started, architecture overview, links        │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

## JSDoc Standards

JSDoc is required for all **public** exports from packages. Internal functions and private methods do not require JSDoc (the code should be self-documenting).

```typescript
// packages/voice/src/streaming/voice-stream-manager.ts

/**
 * Manages a bidirectional voice stream between a participant
 * and the voice processing pipeline.
 *
 * @remarks
 * The VoiceStreamManager handles WebSocket connection lifecycle,
 * audio chunk buffering, stream health monitoring, and automatic
 * reconnection with exponential backoff.
 *
 * @example
 * ```typescript
 * const manager = new VoiceStreamManager({
 *   participantId: 'user_123',
 *   voiceProvider: 'twilio',
 * });
 * await manager.connect();
 * manager.on('transcript', (text) => console.log(text));
 * ```
 */
export class VoiceStreamManager {
  /**
   * Creates a new voice stream connection.
   *
   * @param options - Connection configuration including provider,
   *                  participant ID, initial metadata, and timeout.
   * @throws {ValidationError} If required options are missing
   *         or invalid.
   * @throws {ExternalServiceError} If the voice provider is
   *         unavailable.
   * @returns A promise that resolves when the stream is established.
   */
  async connect(options: ConnectOptions): Promise<void> {
    // ...
  }
}
```

**Required JSDoc tags:**
- `@param` with type and description for all parameters
- `@returns` with description
- `@throws` for documented exceptions
- `@example` for at least one usage example
- `@deprecated` with migration path (when applicable)

**Optional JSDoc tags:**
- `@remarks` for additional notes
- `@see` for related functions
- `@internal` for code not meant for public consumption

## Package README Template

Every package has a README.md following this structure:

```markdown
# @voice-agent/voice

> Voice streaming, WebSocket management, and speech-to-text processing.

## Installation

```bash
pnpm add @voice-agent/voice
```

## Usage

```typescript
import { VoiceStreamManager } from '@voice-agent/voice';

const manager = new VoiceStreamManager({ participantId: 'user_123' });
await manager.connect();
```

## API

### `VoiceStreamManager`

| Method | Description |
|--------|-------------|
| `connect(options)` | Establishes voice stream connection |
| `disconnect()` | Gracefully closes the connection |
| `sendAudio(chunk)` | Sends an audio buffer for processing |

### Events

| Event | Payload | Description |
|-------|---------|-------------|
| `transcript` | `string` | Speech-to-text result |
| `status` | `CallStatus` | Connection state change |
| `error` | `{ code, message }` | Error notification |

## Configuration

This package respects these environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `VOICE_PROVIDER_API_KEY` | — | API key for voice provider |
| `VOICE_WS_TIMEOUT_MS` | `30000` | WebSocket connection timeout |

## Dependencies

- `@voice-agent/shared` — Types, validation schemas, error classes
- `ws` — WebSocket client library

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Changelog

See [CHANGELOG.md](../../CHANGELOG.md) for release history.
```

## Architecture Decision Records

ADRs capture significant design decisions with context, options considered, and rationale:

```markdown
# ADR-001: Use WebSocket for Real-Time Voice Streaming

## Status
Accepted (2024-06-15)

## Context
The voice agent platform needs to stream audio between
participants and the voice processing pipeline. Options include
WebSocket, Server-Sent Events (SSE), HTTP long-polling, and
WebRTC.

## Decision
We will use WebSocket for bidirectional voice streaming.

## Options Considered

### WebSocket
- Full-duplex communication, low latency
- Standard protocol with broad library support
- Automatic reconnection via custom logic
- Upside: 50-100ms latency for audio chunks

### Server-Sent Events (SSE)
- Unidirectional only (server → client)
- Would require separate upload channel
- Native browser support without libraries
- Upside: Simpler for server-to-client only

### WebRTC
- Peer-to-peer with NAT traversal
- Built-in audio codec support
- High complexity for server-side processing
- Upside: Best latency (10-30ms)
- Downside: Requires media server infrastructure

## Consequences
1. Positive: Bidirectional communication with ~50ms latency
2. Positive: Mature library ecosystem (ws, socket.io)
3. Negative: Must implement reconnection logic (not built-in)
4. Negative: WebSocket doesn't automatically recover from
   network interruptions
5. Trade-off: Choosing ws raw over socket.io for lower
   overhead but more manual implementation

## Related Decisions
- ADR-002: Voice Provider Abstraction Layer
- ADR-005: Audio Codec Selection (Opus)
```

ADR files are stored in `docs/adr/` and numbered sequentially. Each ADR is immutable once accepted — updates create a new ADR that supersedes the old one.

## Changelog Maintenance

The changelog follows Keep a Changelog format and is updated with every PR:

```markdown
# Changelog

## [1.2.0] - 2024-06-15

### Added
- Voice stream reconnection with exponential backoff
- Support for Opus audio codec input
- Rate limiting per API key

### Changed
- Upgraded Prisma to v5.14
- Reduced WebSocket timeout from 60s to 30s

### Fixed
- Memory leak in audio buffer cleanup
- N+1 query in voice call listing endpoint

### Security
- Updated dependencies with critical CVEs
```

Changelog entries reference PR numbers and link to GitHub:

```
- Voice stream reconnection with exponential backoff ([#142](https://github.com/voice-agent/platform/pull/142))
```

## Documentation Generation

```bash
# Generate API docs from JSDoc
pnpm exec typedoc --out docs/api packages/*/src

# Generate changelog from conventional commits
pnpm exec conventional-changelog --config conventional-changelog-conventionalcommits

# Validate documentation coverage
pnpm exec tsdoc-coverage packages/*/src
```

The documentation pipeline runs as a CI step but does not block merges (docs are always improvable). The typedoc output is deployed to the team's internal documentation site.

## Integration Points

- **TypeDoc**: Generates HTML documentation from JSDoc annotations
- **Conventional Commits**: Commit messages drive automated changelog generation
- **GitHub Releases**: Tagged releases publish changelog entries to the GitHub Releases page
- **Storybook**: Component documentation (interactive examples) complements JSDoc
- **OpenAPI/Swagger**: API endpoint documentation generated from Zod schemas via `zod-to-openapi`

## Production Considerations

1. **Documentation drift**: Automated validation in CI ensures that public API changes require JSDoc updates. A custom ESLint rule (`require-jsdoc-exports`) warns when exported functions lack JSDoc.
2. **Diagrams as code**: Architecture diagrams in ADRs use Mermaid.js syntax, not embedded images. Mermaid renders natively in GitHub markdown and stays in sync with the text diff.
3. **README freshness check**: A weekly CI job checks the last-modified date of each README against the package's git log. If the package has changed but the README hasn't been updated in 30 days, an issue is auto-created.
4. **Searchability**: All documentation is indexed by an internal search tool (Algolia DocSearch or similar). ADRs are tagged by domain (voice, ai, infrastructure) for cross-referencing.
5. **Ownership**: Each ADR and README has an explicit owner listed in the CODEOWNERS file. Documentation without a clear owner becomes stale.
