# Projects & Resume Deep Dive - 200+ Interview Q&A
## For YC Startups & Top Tech Companies

## GuardrailZ: LLM Guardrails Suite (Q1-Q50)
### Q1: Explain GuardrailZ architecture and tech stack.
**Answer:** Full-stack NextJS + TypeScript application. Frontend: React components for managing guardrails, monitoring, configuration. Backend: NextJS API routes handle guardrail processing. Auth: Clerk for authentication and session management. Storage: PostgreSQL via Prisma. Each guardrail is modular (class-based). Middleware pipeline chains guardrails together. Deployment on Vercel.

### Q2: How do guardrails work internally? Explain the check() flow.
**Answer:** Each guardrail implements: `check(input: string, context: GuardrailContext): GuardrailResult`. The result contains: passed (boolean), score (0-1 confidence), redactedContent (sanitized version), details (what was found, positions). The pipeline: (1) Pre-input guardrails check user message (profanity, PII injection). (2) If passed, send to LLM. (3) Post-output guardrails check LLM response (unsafe content, data leakage). Configurable order and severity.

### Q3: How does PII/PHI detection work in GuardrailZ?
**Answer:** Multi-layer approach: (1) Regex patterns - email, phone, SSN, credit card, passport, etc. (2) NER (Named Entity Recognition) - identifies names, locations, orgs, dates. (3) PHI-specific: medical record numbers, diagnoses, lab tests, insurance IDs. (4) Contextual detection - phrases like "my email is" trigger enhanced checking. Redaction options: mask (a***@gmail.com), hash (consistent replacement), block entire response.

### Q4: What are the configurable security profiles?
**Answer:** Enterprise: strictest - blocks prompt injection, redacts PII/PHI, requires topic whitelist, fails closed on uncertainty. Child Safety: blocks profanity, personal info requests, violent content, self-harm mentions. Standard: balanced - warns on prompt injection, blocks PII, allows most topics. Custom: user selects specific guardrails and thresholds. Profiles defined as JSON config.

### Q5: How did you implement the 50+ guardrails?
**Answer:** Systematic categorization: (1) Input guardrails - prompt injection detection (pattern matching + LLM classifier), topic control, profanity filter, PII detection, SQL injection detection. (2) Output guardrails - toxicity check, bias detection, data leakage prevention, format validation, fact-check. (3) Security guardrails - SSRF prevention, URL validation, code injection detection. (4) Compliance guardrails - HIPAA PII detection, GDPR data minimization, SOC 2 logging.

### Q6: How do you handle false positives?
**Answer:** Configurable severity: block (always), warn (log but pass), flag (review). Score threshold tunable per guardrail. Context-aware detection reduces false positives (e.g., "email me at" vs technical discussion about email protocols). Profiling - users can mark incorrect blocks for review. Confidence scoring based on multiple detection signals.

## SaaS Launch Video Editor (Q51-Q90)
### Q7: How did you build the timeline component?
**Answer:** Custom React component with Zustand state management. Architecture: tracks container (clips arranged horizontally), playback head (position indicator synced with timer), zoom controls (time scale), ruler (time markers). Each clip has: start/end trim points, position in timeline, layer index. Drag to rearrange, handle resize for trim. Uses CSS transforms for smooth positioning, pointer events for drag interaction.

### Q8: How does video trimming work in the browser?
**Answer:** User sets in/out points on clip → record start and end timestamps. On export: use MediaRecorder API to capture segment between timestamps. Or use WebCodecs API for frame-level precision. Trim is non-destructive (original file preserved, only export affects output). Preview uses currentTime setting on HTML5 video element.

### Q9: How do overlays and animations work?
**Answer:** Overlays are absolutely positioned divs over the video preview area. Each overlay: position (x,y), size, timing (start, end in video), animation (CSS keyframes or Framer Motion). Animations: fade, slide, scale, rotate combined into sequences. Rendered on canvas during export. Framer Motion used for UI animations, not video export.

## Workflow-Canvas Library (Q91-Q130)
### Q10: Explain Workflow-Canvas architecture.
**Answer:** React + TypeScript library published as npm package. Uses ReactFlow (xyflow) for node/edge rendering and interaction. Zustand for state management (nodes, edges, selection, viewport). Custom node types (task, condition, loop, trigger, action). Custom edge types with animated paths. SVG rendering for crisp output. Drag-and-drop via ReactFlow's built-in handlers.

### Q11: What is Zustand and why did you choose it?
**Answer:** Minimal state management library. API: `const useStore = create((set) => ({ nodes: [], addNode: (node) => set((state) => ({ nodes: [...state.nodes, node] })) }))`. Chosen over Redux for: simpler API, no boilerplate, built-in TypeScript support, middleware (persist, devtools, immer), hooks-based, tiny bundle size (~1KB). Perfect for library development.

### Q12: How do you handle edge routing and connections?
**Answer:** ReactFlow provides built-in edge routing with bezier, step, smoothstep, and straight edge types. Custom: animated dashed edges for active connections, colored by type (success/error). Connection validation: check node type compatibility (e.g., output port → input port), prevent circular connections. Handle reconnection on drop.

### Q13: How do you export/import workflows?
**Answer:** Export: serialize Zustand store state (nodes, edges, viewport) to JSON. Import: parse JSON, validate schema, restore state. Supports versioning for backward compatibility (migrate old formats). Export formats: JSON (full flow), image (PNG - via html-to-image library), clipboard copy/paste.

## MigratorGen (Q131-Q160)
### Q14: How does MigratorGen work?
**Answer:** Python CLI tool + LibCST engine pipeline: (1) Parse changelogs (JSON or Markdown). (2) LLM extracts structured migration rules (old_pattern → new_pattern). (3) LibCST traverses source AST, applies transformations. (4) Generates migration package (code + tests). Supports library upgrades (e.g., when library v2 changes API) and downgrades.

### Q15: Why choose LibCST over regex or ast?
**Answer:** regex is fragile - breaks on code formatting changes, comments, complex expressions. ast module is read-only - can parse but not modify. LibCST: full concrete syntax tree (preserves whitespace, comments, formatting), read + write, pattern matching API. Result: clean transformations that maintain code style.

### Q16: How does the LLM integration work?
**Answer:** LLM receives changelog text + context (library name, version changes). Structured output: list of migration rules (old_code_pattern → new_code_pattern, description, conditions). LLM handles ambiguity in changelog, infers migration patterns from examples. Structured extraction via JSON mode or output parsing.

## ScriptVector (Q161-Q180)
### Q17: Explain ScriptVector - what does it do?
**Answer:** AI-powered Hindi Manhwa (comics) content generation system. Uses Gemini API + Agno agents to generate long-form content. Pipeline: generate plot outline → expand to chapters → generate dialogue → review consistency. SQLite stores content state, character profiles, plot continuity. Maintains contextual continuity across generations (character arcs, plot threads).

### Q18: How do you maintain content continuity?
**Answer:** Store comprehensive state: character profiles (name, traits, relationships), plot summaries (past events, foreshadowing), setting details, timeline of events. Each generation step receives relevant context (previous chapter summary, active plot threads, character states). SQLite queries retrieve most relevant context for current generation task.

## Marketing AI Agent (Q181-Q200)
### Q19: How does the Marketing AI Agent work?
**Answer:** Multi-model architecture supporting Gemini, HuggingFace, Groq APIs. Flask backend exposes REST endpoints for agent actions. Streamlit frontend for dashboard. Integration APIs: Gmail (send/read emails), Twitter (post tweets, read timeline), YouTube (upload videos, manage playlists). Agent can: create content using one model, post to social media, manage Google Drive files.

### Q20: How do you handle API keys and secure configuration?
**Answer:** Environment variables (.env file) for API keys. Never commit secrets to git. Each API provider configured via class: Provider(name, api_key, base_url, model). Secrets loaded at runtime. Streamlit secrets management for deployed version. Rate limiting per API (tokens-per-minute). Error handling: fallback between providers if one fails.
