# Content Style Guide — Production-Grade Error Handling

> This guide defines the exact structure, depth, and tone every chapter and file in this
> resource MUST follow. Consistency is what makes 60+ chapters feel like one book instead of
> 400 disconnected notes. Read this before writing or editing anything.

---

## 1. Audience and Learning Objective

The reader is a working software engineer (junior → senior) building SaaS products. They want
to *understand deeply and apply immediately*. Every file must be:

- **Self-contained** — a reader who opens only this file still learns something complete.
- **Practical** — every concept ends in code, a decision rule, or a checklist they can use today.
- **Opinionated but honest** — state the recommended default, then show the trade-off.
- **Dense but readable** — tables, short paragraphs, worked examples, no filler.

The goal is a **reusable error-handling standard**, not a giant framework. Always prefer the
simplest design that satisfies the requirement.

---

## 2. Directory Layout (fixed)

```
production/error_handling/
├── README.md                      # master index (parts → chapters → files)
├── _STYLE_GUIDE.md                # this file
├── GLOSSARY.md                    # shared vocabulary
├── part-NN-<part-slug>/
│   ├── README.md                  # part overview + chapter index
│   └── NN-<chapter-slug>/
│       ├── README.md              # chapter overview, objectives, file index, key takeaways
│       ├── 01-concepts/           # the "what" and "why" — mental models
│       ├── 02-deep-dive/          # the "how" — mechanics, internals, edge cases
│       ├── 03-practical-examples/ # runnable-ish code + real-world scenarios
│       ├── 04-dos-and-donts/      # rules, anti-patterns, checklists
│       └── 05-reference/          # cheat sheets, decision tables, glossary of the chapter
```

Every chapter folder MUST contain a `README.md`. Every populated subfolder SHOULD contain a
`README.md` that lists its files (one line each, with a short description). Number files so they
sort correctly: `01-...md`, `02-...md`, ...

---

## 3. File Anatomy

A typical concept/example file follows this skeleton. Not every heading is mandatory, but the
order must be preserved when used.

```markdown
# <Descriptive Title>

> Part X · Chapter Y · Section Z  ·  _Estimated reading time: N min_
> **Prerequisite:** <link to earlier file or "none">

## In one sentence
<The single most important takeaway. Bold the key phrase.>

## Why this matters in production
<Concrete consequence of getting it wrong: money, data loss, downtime, security, churn.>

## Core concept
<Explanation. Use tables and small diagrams (ASCII) freely.>

## How it works (mechanics)
<Step-by-step. Include the exact sequence of events.>

## Worked example
<A realistic scenario, then code, then the result. Label the language.>

```ts
// TypeScript example — keep snippets focused and runnable in spirit
```

## Key data / numbers
<Concrete metrics, limits, defaults, timeouts, header names, status codes, standard references.>

## Real-world use case
<A named-style scenario: "A multi-tenant billing SaaS…". Explain the failure, the fix, the
result. This section is mandatory in every concepts/example file.>

## Trade-offs
| Approach | Pros | Cons | When to use |
|----------|------|------|-------------|

## Do / Don't
| ✅ Do | ❌ Don't |
|-------|----------|
| ...   | ...      |

## Common mistakes
<Bullets. Each mistake = what happens + how to avoid.>

## Checklist
- [ ] ...

## Related
- <relative links to other files>
```

### Rules

- **Code fences** must always declare a language (`ts`, `python`, `go`, `sql`, `json`, `http`,
  `yaml`, `text`). Keep snippets short enough to read on one screen where possible; long examples
  may span but split into numbered "Step 1 / Step 2".
- **Tables** for anything enumerable: status codes, retry classes, do/don't, trade-offs.
- **Bold** the load-bearing phrase. Do not bold whole sentences.
- **No emojis** except the ✅/❌ markers in Do/Don't tables and ⚠️ for hazards, used sparingly.
- **No invented URLs.** Reference standards by name (RFC 9457, PostgreSQL SQLSTATE, gRPC status
  codes) not by fabricated link. Only link to other files inside this repo.
- **Numbers must be real** where a standard exists (e.g. `429`, `Retry-After`, `SQLSTATE 23505`,
  PostgreSQL `40001` serialization_failure, HTTP/2 `GOAWAY`). If unsure, say "commonly" or give a
  range and label it as a recommendation.
- Target **200–450 lines** per substantial file. Reference/cheat-sheet files may be shorter
  (80–200). Chapter READMEs are 60–140 lines.

---

## 4. Writing Voice

- Second person, direct: "You catch the error at the boundary, not in the domain."
- Short paragraphs (1–4 sentences). One idea per paragraph.
- Prefer concrete nouns: "the payment webhook", not "the component in question".
- Define a term the first time it appears, then use it consistently. Add it to `GLOSSARY.md`.
- When a rule has an exception, say so explicitly in a "Trade-offs" or "Exceptions" note.

---

## 5. The Recurring Cast (use the same running examples)

To make the whole book feel connected, reuse a small set of running examples:

1. **`Acme SaaS`** — a multi-tenant B2B project-management tool (REST API, Postgres, Redis,
   Stripe billing, S3 uploads, background jobs on a queue, an LLM "summarize" feature).
2. **`Checkout` flow** — a payment/subscription workflow (idempotency, partial failure, saga).
3. **`ExportJob`** — a long-running background export (retries, dead-letter, checkpointing).
4. **`WebhookIngest`** — inbound Stripe webhooks (signature verification, duplicates, replays).
5. **`AgentRun`** — an LLM tool-calling agent (provider errors, token limits, tool failures).

Use these consistently so cross-references make sense. Introduce a new example only when it
teaches something the cast cannot.

---

## 6. Cross-Linking Rules

- Every file ends with `## Related` linking 2–4 sibling or parent files using **relative paths**.
- Chapter README tables link every file in the chapter.
- Part READMEs link every chapter.
- The root `README.md` links every part.
- When you reference a concept owned by another part, link it instead of re-explaining it in depth.

---

## 7. Definition of Done for a File

- [ ] Follows the anatomy in §3.
- [ ] Has a "Real-world use case" using the recurring cast (concept/example files).
- [ ] Has do/don't and/or checklist content.
- [ ] Code snippets have language fences.
- [ ] `## Related` links resolve to real files.
- [ ] Provides at least one piece of real-world "key data" (status code, default, limit, header).
- [ ] No fabricated URLs, no secrets, no PII in examples.
