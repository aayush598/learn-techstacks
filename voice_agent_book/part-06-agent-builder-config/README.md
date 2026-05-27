# Part 06: Agent Builder & Configuration System

> **Duration:** Builder Phase (Weeks 8-14)  
> **Goal:** Build a no-code visual agent builder with flow designer, prompt editor, template system, and versioning.

---

## Chapters Overview

| # | Chapter | Description |
|---|---------|-------------|
| 01 | [Visual Flow Builder Architecture](ch-01-visual-flow-builder-architecture/README.md) | React Flow integration, node types, edge routing, canvas state management, undo/redo |
| 02 | [Node Types & Conversation Components](ch-02-node-types-conversation-components/README.md) | Message nodes, question nodes, condition nodes, API call nodes, transfer nodes, webhook nodes |
| 03 | [Prompt Engineering Interface](ch-03-prompt-engineering-interface/README.md) | System prompt editor, variable injection, template syntax, prompt versioning, A/B testing |
| 04 | [Agent Templates & Presets](ch-04-agent-templates-presets/README.md) | Template schema, marketplace templates, industry-specific presets, customization layer |
| 05 | [Conditional Logic & Branching](ch-05-conditional-logic-branching/README.md) | Expression parser, variable comparison, intent-based routing, slot-based branching |
| 06 | [Workflow Chaining & Multi-Step Tasks](ch-06-workflow-chaining-multi-step-tasks/README.md) | Sequential tasks, parallel execution, timeout handling, retry logic, workflow composition |
| 07 | [Agent Versioning & Rollback](ch-07-agent-versioning-rollback/README.md) | Version snapshots, diff viewer, rollback mechanism, publishing workflow, draft/published states |
| 08 | [Tone & Personality Configuration](ch-08-tone-personality-configuration/README.md) | Tone presets, custom tone definitions, formality levels, empathy controls, brand voice rules |
| 09 | [Response Guardrails & Safety](ch-09-response-guardrails-safety/README.md) | Profanity filtering, content moderation, PII protection, topic restrictions, confidence thresholds |
| 10 | [Agent Testing & Preview Mode](ch-10-agent-testing-preview-mode/README.md) | In-browser conversation simulator, debug mode, utterance testing, flow validation |

---

## Key Open-Source Tools

- **React Flow** (MIT) — Node-based UI builder
- **Monaco Editor** (MIT) — Code/prompt editor
- **Zustand** (MIT) — State management
- **Immer** (MIT) — Immutable state updates
- **React DnD** (MIT) — Drag and drop
- **JSONata** (MIT) — Expression evaluation

---

## Learning Objectives

- Build a drag-and-drop visual flow builder using React Flow
- Design a comprehensive node type system for conversation flows
- Implement a prompt engineering interface with variable injection
- Create a template system with inheritance and customization
- Build complex conditional logic and branching workflows
- Implement agent versioning with rollback capabilities
- Configure tone, personality, and safety guardrails
- Create an in-browser testing environment for agent preview
