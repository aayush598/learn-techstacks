# DFDSOFT / DogFoodDev — Documentation, Communication & Startup Culture (100 Q&A)
> Role: AI Coding & Agent Development Specialist  > Candidate: Aayush Gid (open-source contributions/technical writing/startup internship background)

---

## Technical Documentation (Q1–Q15)

**Q1: What makes a good README?**
A: A good README answers: what the project does, why it exists, how to install and run it, and how to contribute — all within 30 seconds of reading. It starts with a one-line description and a minimal quickstart. For agent projects, include a "How the Agent Thinks" section explaining the system prompt logic and tool chain.

**Q2: How do you structure API documentation for an internal tool?**
A: Start with authentication, list every endpoint grouped by resource, include request/response examples with actual payloads, and document error codes. Use OpenAPI 3.1 so docs auto-generate. For internal tools, add a "When to Use This API" section with real caller examples from your codebase.

**Q3: What is an Architecture Decision Record (ADR)?**
A: An ADR captures a significant technical decision: the context, the options considered, the decision made, and consequences. Format: Title, Status, Context, Decision, Consequences. It is lightweight, version-controlled (usually in a `docs/adr/` folder), and prevents "why did we do it this way?" six months later.

**Q4: When would you write an ADR vs. just documenting in code comments?**
A: Use an ADR for irreversible or high-cost decisions (choosing a database, picking an agent framework, selecting a deployment model). Use code comments for local, explain-why-now decisions within a function. ADRs are for the team; comments are for the next reader of that file.

**Q5: How do you write a runbook for incident response?**
A: A runbook is step-by-step: trigger condition, severity classification, diagnostic steps, remediation actions, escalation contacts, and post-incident checklist. Keep each step as an imperative command ("Check the queue depth in Cloudflare dashboard"), not prose. Include direct links to dashboards and relevant CLI commands.

**Q6: What goes into a changelog?**
A: Every user-facing change: Added, Changed, Deprecated, Removed, Fixed, Security (Keep a Changelog format). Reference issue/PR numbers. Write for the person upgrading, not for the developer who wrote it. Never bundle "miscellaneous fixes" — each item stands alone. Example: `## [1.2.0] - 2026-08-20 — Added retry logic to agent tool calls (#142)`.

**Q7: How do you decide what level of code comments to add?**
A: Comment the "why," not the "what." A comment explaining a non-obvious business rule or workaround is valuable; a comment saying `// increment counter` is noise. For AI-generated code, add a brief note at the top of complex functions explaining the intent the model was given, so future humans understand the original goal.

**Q8: How do you document a system prompt for an AI agent?**
A: Document the prompt's purpose, the persona it establishes, the tools it exposes, expected input/output formats, known edge cases, and the version/date of the prompt. Include a "Behavioural contract" — what the agent should never do. Store prompts in version-controlled files, not buried in databases.

**Q9: What's your approach to writing playbooks for support teams?**
A: A playbook maps symptoms to actions. Structure: Symptom → Diagnosis → Resolution steps → Escalation path. Use conditional branching ("If error X, do Y. If error Z, do W."). Include screenshots or dashboard links. Review playbooks quarterly or after every incident that reveals a gap.

**Q10: How do you document tool descriptions for an agent that uses function calling?**
A: The tool name, a one-sentence description of what it does, every parameter with type, whether it is required, a concrete example value, and what the agent should expect in the response. Bad: `"get_weather" — "gets weather"`. Good: `"get_weather" — "Returns current weather for a city. Parameters: city (string, required, e.g. "San Francisco"), units (enum: "metric"|"imperial", default "imperial"). Returns: {temp, conditions, humidity}."`

**Q11: How do you keep documentation from becoming stale?**
A: Three tactics: (1) CI checks — fail the build if a README's example command doesn't run; (2) documentation review as part of every PR that changes behaviour; (3) owner attribution — every doc page has an `@owner` and a "last verified" date. Stale docs are worse than no docs because they build false confidence.

**Q12: What is a spec document for an agent workflow?**
A: A workflow spec defines: triggers, input schema, step-by-step logic (including which tools/agents are called), output schema, error handling paths, and performance budget (latency, token cost). Think of it as a flowchart plus a contract. It is the source of truth that both the implementer and the reviewer work from.

**Q13: How do you write documentation that both engineers and non-technical stakeholders can use?**
A: Use layered documentation: a plain-English summary at the top (what it does, why it matters), a technical reference section below (API schemas, config options), and examples throughout. Avoid jargon in the top layer. Link between layers. When writing for a founder, lead with impact and timeline, not architecture.

**Q14: How do you approach versioning documentation alongside code?**
A: Tag documentation with the same version as the code it describes. For API docs, version the URL (e.g., `/v1/`, `/v2/`). For internal docs, use Git tags and a docs site that can render versioned content. Never modify old-version docs after release — create an update note pointing to the new version.

**Q15: Describe your process for writing a technical blog post or tutorial.**
A: (1) Define the audience and the single thing they will be able to do after reading; (2) build a working example first, capture exact steps; (3) write the intro and conclusion last; (4) include a "Prerequisites" section; (5) test every code block by running it in a clean environment; (6) get one peer review from someone outside the project.

---

## Agent Documentation (Q16–Q25)

**Q16: How do you document a multi-agent system?**
A: Create a system diagram showing agents, their roles, and communication flows. Then document each agent individually: its system prompt, available tools, input/output contract, and failure modes. Add a section on orchestration — how agents are selected, how results are merged, and how conflicts are resolved.

**Q17: What is a behaviour spec for an AI agent?**
A: A behaviour spec defines the agent's persona, capabilities, constraints, and guardrails in structured natural language. Example: "The agent is a helpful coding assistant. It must never execute destructive commands without confirmation. When uncertain, it asks a clarifying question rather than guessing." This lives alongside the system prompt as its reviewable, diffable counterpart.

**Q18: How do you document agent memory and state?**
A: Document what the agent remembers (conversation history, user preferences, learned context), how that memory is stored (context window, vector DB, key-value store), TTLs, and privacy implications. Include a state diagram for long-running agents. Be explicit about what happens when memory is cleared or exceeds limits.

**Q19: How do you write effective tool/function descriptions for an LLM agent?**
A: Be precise, include type signatures, state side effects, and failure modes. Bad: "Search the web." Good: "Search the web using the Brave Search API. Parameter: query (string, required). Returns up to 10 results with title, URL, and snippet. Rate limit: 1 req/sec. On rate limit, the agent should wait and retry once." Clarity here directly reduces hallucination.

**Q20: How do you document prompt engineering decisions?**
A: Use a prompt changelog. For each version: the diff from the previous version, the hypothesis ("adding chain-of-thought should reduce errors on multi-step reasoning"), the eval results, and whether the change shipped. This prevents "prompt roulette" — the situation where no one knows why the prompt is the way it is.

**Q21: How do you document error handling in an agent pipeline?**
A: For each tool call and agent step, document: the error types that can occur, the agent's retry strategy, the fallback behaviour (use cached data? ask the user? abort?), and the escalation path (log to Sentry? page someone?). Use a table format for quick reference during incidents.

**Q22: What does an onboarding doc for a new agent developer look like**
A: (1) Architecture overview with diagram; (2) local dev setup (env vars, API keys, which services to spin up); (3) how to modify a system prompt and test changes; (4) how tool calling works in this codebase; (5) where evals live and how to run them; (6) deployment process; (7) who to ask for help. Goal: new contributor ships a small change within their first day.

**Q23: How do you document agent eval results?**
A: Store evals in a versioned location (CSV or JSON in Git, or a dedicated eval dashboard). For each eval set: the dataset, the prompt version, the model used, pass/fail rates, and examples of failures. Track trends over time. Link eval results to the ADR or prompt changelog entry that caused a regression or improvement.

**Q24: How do you document workflow orchestration for a chain of agents?**
A: A visual flowchart (Mermaid or Excalidraw) plus a step-by-step description of each node, the data passed between nodes, timeout values, and retry policies. Include a "happy path" and an "error path" walkthrough. Annotate with latency and cost estimates so the team can reason about trade-offs.

**Q25: How do you write release notes for an agent update?**
A: Focus on user-visible changes: "The agent now supports multi-file editing," "Response latency reduced by 40%," "Fixed hallucination on financial queries." Include migration notes if system prompts changed (e.g., "Custom system prompts may need updating to include the new tool signature"). Avoid internal jargon.

---

## English Communication (Q26–Q40)

**Q26: How do you write a clear status update in Slack or Teams?**
A: Use the format: **Status** (one word: Done / In Progress / Blocked), **What changed since last update**, **Next step**, **Blocker if any**. Example: "Status: Blocked. Finished API integration, tests passing locally. Next: deploy to staging. Blocker: need staging env credentials from @founder." This respects everyone's time.

**Q27: How do you escalate an issue to a founder or manager asynchronously?**
A: Lead with the impact, not the problem. "User data sync is broken — affects ~200 daily active users. I've identified the root cause (API key rotation). Fix is ready, needs your approval to deploy. ETA: 30 minutes once approved." Attach a link to the PR or incident ticket. Propose a solution; don't just report the fire.

**Q28: How do you write meeting notes that people actually read?**
A: Use a consistent template: Date, Attendees, Decisions Made (top — bold), Action Items (who/what/when), Open Questions, Next Meeting. Send within 2 hours of the meeting. Keep it under one page. The goal is that someone who skipped the meeting can act on the notes without asking for a recap.

**Q29: How do you write a PR description that accelerates review?**
A: Template:

```
## What
One-sentence summary of the change.

## Why
Link to issue/context. What problem does this solve?

## How
Key design decisions. Alternatives considered.

## Testing
How to verify. Screenshots/logs if UI or agent output changed.

## Checklist
- [ ] Tests pass
- [ ] Docs updated
- [ ] No secrets committed
```

This reduces back-and-forth comments by 60%+.

**Q30: How do you handle disagreements about technical approaches in writing?**
A: Acknowledge the other person's reasoning first, then present your perspective with evidence (benchmarks, prior incidents, references). Avoid "you're wrong" — use "I see it differently because..." Propose a time-boxed experiment if debate stalls: "Let me build a small prototype of approach B and we compare by EOD."

**Q31: How do you write a bug report that engineers can act on immediately?**
A: Format: **Title** (specific, e.g., "Agent returns empty response for queries with 3+ tool calls"), **Steps to reproduce**, **Expected vs. actual behaviour**, **Environment** (model, OS, browser), **Screenshots/logs**, **Severity estimate**. The fewer questions the engineer has to ask, the faster the fix ships.

**Q32: How do you write a feature request that a founder can evaluate quickly?**
A: Structure: **Problem** (who has it, how often, what it costs), **Proposed solution** (one paragraph), **Scope** (MVP vs. full), **Effort estimate** (rough t-shirt size), **Alternatives considered**. This shows you've thought beyond "wouldn't it be cool if..."

**Q33: How do you communicate a technical delay to non-technical stakeholders?**
A: Be honest and early. "The database migration is taking longer than expected because we discovered a schema conflict with the legacy system. Original ETA was Thursday; new ETA is Monday. Risk: if we rush, we could lose data. Recommendation: ship on Monday." Always pair the delay with a recommendation.

**Q34: How do you write concise Slack messages in a fast-moving startup?**
A: One message, not ten. Number your points. Use bold for the key ask. "Hey @team — three things: (1) **Deployed v2.1** to staging — link. (2) **Agent latency** dropped from 8s to 3s after prompt refactor. (3) **Need review** on PR #287 before I can ship the memory feature. Tagging @reviewer." No preamble, no fluff.

**Q35: How do you write an incident post-mortem?**
A: Template: **Summary** (one paragraph), **Timeline** (timestamps), **Root Cause**, **Impact** (users, duration, revenue), **Resolution**, **Action Items** (preventative, with owners and deadlines), **What Went Well**, **What Went Wrong**, **Where We Got Lucky**. Blameless tone always — focus on systems, not individuals.

**Q36: How do you write documentation for an international team with varying English proficiency?**
A: Use simple sentence structures, avoid idioms ("let's table this" means opposite things in US vs. UK English), use numbered lists over prose, and include visual diagrams. Define acronyms on first use. The goal is clarity for a reader whose first language is not English.

**Q37: How do you write a clear commit message?**
A: Imperative mood, under 72 characters for the subject line, body explains what and why (not how — the diff shows how). Example: `fix(agent): handle empty tool response gracefully`. Add a `Co-authored-by:` line for AI-assisted commits. Reference the issue: `Closes #142`.

**Q38: How do you give constructive feedback on someone's code or documentation?**
A: Be specific, not general. Not "this is unclear" but "line 34 assumes the reader knows what a vector store is — a one-sentence definition would help." Frame as a suggestion: "Have you considered...?" Always acknowledge what works before pointing out what doesn't. Reference the goal, not the person.

**Q39: How do you write a handoff document when rotating off a project?**
A: Template: **Current State** (what's working, what's not), **Open Issues** (with links), **Key Decisions Made** (and why), **Gotchas** (things that will trip you up), **Next Steps** (prioritised), **Who to Ask** (for specific areas). Write it as if you're going on vacation for two weeks and the successor has never seen the codebase.

**Q40: How do you structure a Slack channel for a project?**
A: Use pinned messages for key links (repo, docs, deploy dashboard). Create threads for discussions. Use channel description as a mini-README: what the project is, who owns it, where to find things. Agree on norms: emoji reactions for quick ack (👀 = looking, ✅ = done), no DMs for project questions so knowledge stays in the channel.

---

## Working with Founders (Q41–Q50)

**Q41: A founder says "build me an AI agent that does X." How do you start?**
A: Ask clarifying questions: Who is the user? What does success look like? What is the input and expected output? Are there existing systems this integrates with? What is the timeline and what is the MVP vs. full vision? Write the answers down in a shared doc before writing any code. This 15-minute conversation saves days of rework.

**Q42: How do you translate a vague idea into a technical spec?**
A: Start from the user story: "As [user], I want [action] so that [outcome]." Then define the inputs, outputs, data sources, agent logic, tool calls, and success criteria. Include a "non-goals" section to scope what this version does NOT do. Share the spec and get written sign-off (even a Slack 👍 counts).

**Q43: How do you say "no" to a founder respectfully?**
A: Don't say no — say "yes, and here's the trade-off." Example: "We can build that, but it adds 2 weeks to the timeline and introduces auth complexity. An alternative that gets 80% of the value in 2 days is [simpler approach]. Which do you prefer?" This shows ownership, not obstruction.

**Q44: How do you manage scope creep in a startup environment?**
A: Maintain a written scope document. When new requests come in, add them to a "parking lot" section with priority and effort estimate. Refer back to it: "We can add this — it's a great idea — but it means pushing [existing feature] by a week. Want to reprioritise?" Written records prevent memory-based scope creep.

**Q45: How do you handle "let's ship this today" when the feature needs a week?**
A: Propose an MVP that ships today and a full version that ships this week. "I can ship a basic version today that handles the 80% case. The remaining 20% (error handling, edge cases, monitoring) ships Friday. Want me to go with the MVP approach?" Founders respect speed with honesty about trade-offs.

**Q46: How do you give a founder bad news about a technical blocker?**
A: Immediately, with context and a plan. "The third-party API we depend on has a rate limit we'll hit at scale. I've researched three alternatives: [A, B, C]. Recommendation: option B — it's cheapest and has the best uptime. Can we discuss in 10 minutes?" Never let a founder discover a blocker from a missed deadline.

**Q47: How do you prioritise when everything is "urgent"?**
A: Ask: "If we could only ship one thing this week, which one has the most user/business impact?" Use a simple 2x2 matrix: Impact (high/low) vs. Effort (high/low). Start with high-impact, low-effort. Document the prioritisation so when priorities shift (and they will), you have a record of what was deprioritised and why.

**Q48: How do you build trust with a technical founder?**
A: Ship small things quickly and reliably. Communicate proactively. Be honest about what you don't know. Show you understand the business, not just the tech. Over-communicate on progress. When you make a mistake, own it immediately and come with a fix. Trust is built in small, consistent deposits.

**Q49: How do you handle a founder who keeps changing the requirements?**
A: Acknowledge the iteration — it's natural in startups. But introduce lightweight checkpoints: "I've updated the spec three times this week. Let's schedule a 15-minute review tomorrow to lock in the v1 scope so I can build with confidence." Changes are fine; unrecorded changes are the enemy.

**Q50: How do you document a founder's口头 vision into something the team can execute?**
A: After every strategy conversation, write a summary and share it: "Here's my understanding of what we agreed on: [1, 2, 3]. Anything I missed?" This becomes the source of truth. Founders often think out loud — your job is to crystallise the signal from the noise without killing the creative energy.

---

## Startup Culture (Q51–Q65)

**Q51: How do you handle ambiguity in a startup role?**
A: Embrace it as the default. When facing ambiguity: (1) identify what you DO know; (2) list what you need to know; (3) find the fastest path to the missing information (ask, prototype, test); (4) make a decision with the best available info and iterate. In a startup, waiting for perfect information means shipping never.

**Q52: How do you handle a quick pivot mid-sprint?**
A: Anchor on the business goal, not the implementation. "We were building feature A to solve problem X. The pivot means problem X is deprioritised and problem Y is urgent. Here's what from sprint A still applies, here's what's discarded, and here's the new plan." Document the pivot and its reasoning — it prevents second-guessing later.

**Q53: What does "ownership mentality" mean to you in a startup?**
A: It means you don't wait to be told what to do. If you see a bug, you file it and fix it. If documentation is outdated, you update it. If a process is broken, you propose a fix. You treat the company's problems as your problems. Ownership is not about title — it's about acting as if the outcome depends on you, because it does.

**Q54: How do you "wear many hats" effectively?**
A: Prioritise ruthlessly. Spend 80% of your time on your core responsibility, and 20% flexing into adjacent needs. Be transparent: "I'm picking up support tickets this week because we're short-staffed, but that means the feature work will be 2 days later." Communicate trade-offs so no one is surprised.

**Q55: How do you maintain quality when moving fast?**
A: Automate what you can (CI, linting, tests), accept "good enough" where perfection would cost too long, and always ship with a way to roll back. The startup speed-quality trade-off is: speed > perfection, but broken > slow. A feature you can't revert is a feature that can kill you.

**Q56: How do you "fail fast" in practice?**
A: Build the smallest possible version, put it in front of users or in a real environment, and measure. If it doesn't work, you've lost hours not weeks. For agent development: test a prompt variation on 10 queries before deploying to 10,000. Define the metric that means "this worked" before you start.

**Q57: How do you handle wearing multiple hats during a crunch?**
A: Communicate openly about trade-offs. "I'm going to be the on-call support person this week while also shipping the agent update. Support will be my priority 9-5; agent work happens evenings. If agent work is higher priority, we need someone to cover support." Founders respect honesty about capacity.

**Q58: How do you stay productive with startup-style context switching?**
A: Time-boxing and capture systems. Block 2-hour deep work sessions for code. Between sessions, process the notification queue. Keep a "capture pad" (a running doc) for ideas and tasks so nothing gets lost during switches. At end of day, review and reprioritise tomorrow's list.

**Q59: How do you contribute to startup culture as a junior team member?**
A: Be the person who ships. Volunteer for ambiguous tasks. Ask "how can I help?" not "what should I do?" Challenge ideas respectfully with data. Celebrate small wins publicly. Document things so the team scales. Culture is not about hierarchy — it's about behaviour.

**Q60: How do you handle uncertainty about the company's direction?**
A: Ask for context: "I want to make sure my work aligns with where we're heading. Can you share the current top priorities and how my project fits?" Founders appreciate team members who think strategically. If the direction keeps changing, document it — patterns emerge that help you make better autonomous decisions.

**Q61: How do you approach "move fast and break things" responsibly?**
A: Move fast and break *non-critical* things. For anything touching user data, payments, or production systems, slow down and add guardrails. Break things in staging, in experiments, in A/B tests. The "break things" ethos means don't let perfectionism slow you down — it doesn't mean ship unsafe code.

**Q62: How do you stay motivated in a startup with shifting priorities?**
A: Connect to the mission. Even if the specific feature changes, the goal (helping entrepreneurs ship faster, building the best AI agent tools) stays constant. Celebrate what shipped, not what was planned. Keep a personal "wins" log. See every pivot as a learning opportunity, not a loss.

**Q63: How do you handle the "firefighting" culture common in startups?**
A: Fight every fire, then fix the fire alarm. After every incident or crisis, spend 30 minutes writing a quick post-mortem and adding a guardrail. Over time, the fires get smaller and less frequent. The goal is to make yourself progressively less needed for routine issues.

**Q64: How do you handle a situation where you're the only person who knows how something works?**
A: Document it immediately and aggressively. Write a runbook, pair with someone, record a walkthrough. "Bus factor of 1" is a risk the team should know about. If you're hit by a bus (or go on vacation), the system should still function. Being the only expert is not a power position — it's a vulnerability.

**Q65: What do you do when you realise you've made a mistake that affects the team?**
A: Own it immediately. "I made an error in the deployment config that broke staging. Here's what happened, here's the impact, and here's the fix — it's ready to deploy." Don't hide it, don't blame, don't over-apologise. Fix it fast, then do a brief post-mortem on how to prevent recurrence.

---

## Code Review (Q66–Q75)

**Q66: What's your checklist for reviewing AI-generated code?**
A: (1) Correctness — does it solve the stated problem? (2) Security — no secrets, no injection, proper auth checks; (3) Performance — no unnecessary loops, proper batching; (4) Readability — can a new team member understand this in 60 seconds? (5) Tests — are they meaningful or just happy-path? (6) Prompt provenance — is the logic traceable back to the prompt/intent?

**Q67: How do you write a PR review comment that helps without being condescending?**
A: Prefix with intent: "Question:" for clarification, "Suggestion:" for optional improvements, "Nit:" for style-only changes, "Blocker:" for must-fix issues. Example: "Suggestion: This could be simplified with `Promise.all` for parallel execution — the current sequential approach adds ~2s latency." Always explain the "why."

**Q68: How do you review a PR that changes an agent's system prompt?**
A: Review the diff alongside eval results. Check: (1) Does the new prompt still pass existing evals? (2) What specific behaviour changed? (3) Are tool descriptions still accurate? (4) Does the persona/intent match the product spec? (5) Are guardrails still in place? Never merge a prompt change without eval evidence.

**Q69: How do you handle a PR you disagree with?**
A: Comment with your concern and the reasoning. If it's a style preference, approve with a note. If it's a correctness or architecture issue, request changes with specific alternatives. If it's a deep disagreement, suggest a quick call or ADR. "I see it differently — here's why" is always better than a block without explanation.

**Q70: What makes a good test for AI agent behaviour?**
A: Tests that assert on observable behaviour, not internal implementation. "Given input X, the agent calls tool Y with parameter Z" is better than "the prompt contains the string 'always'". Include edge cases: empty inputs, malicious inputs, multi-turn conversations, tool failures.

**Q71: How do you review a PR that includes infrastructure changes?**
A: Extra scrutiny: check for hardcoded values that should be env vars, security groups that are too permissive, Terraform state locks, and drift from the documented architecture. Verify the change can be rolled back. Ask: "What happens if this fails mid-apply?" For cloud resources, check cost implications.

**Q72: How do you provide feedback on documentation PRs?**
A: Check for accuracy (does the doc match the code?), completeness (are all features covered?), and clarity (can a newcomer follow it?). Verify code examples actually run. Look for broken links. Suggest restructuring if the information hierarchy is wrong. Documentation PRs deserve the same rigor as code PRs.

**Q73: How do you balance thoroughness with speed in code review?**
A: For small PRs (< 200 lines): review within 4 hours. For large PRs: request the author to split it. For critical paths (auth, data, payments): be thorough, even if it means a longer review. Use automated tools (linters, type checkers, security scanners) to handle the mechanical parts so you can focus on logic and design.

**Q74: How do you review a PR that you don't fully understand?**
A: Ask for a walkthrough. "I'm not familiar with [library/protocol]. Can you add a brief explanation of how [component] works in the PR description?" This is not a weakness — it's how you learn and how the team shares knowledge. Never approve something you can't reason about.

**Q75: How do you write a PR description for a refactor that changes no behaviour?**
A: Explain: (1) What motivated the refactor (e.g., "this function was doing 3 unrelated things"); (2) what changed (move X to a new module, rename Y); (3) confirm no behaviour change (existing tests pass, no feature differences). A good refactor PR description is short but clear about intent.

---

## Remote Work (Q76–Q85)

**Q76: How do you manage working across IST and US timezones (8:30 PM–5:30 AM overlap)?**
A: Structure your day around the overlap: sync meetings and real-time collaboration during 8:30–11:30 PM IST. Reserve deep work (coding, writing) for morning IST when the US team is offline. Use async tools (Slack threads, Loom videos, written updates) for everything outside overlap. Log off knowing the async updates are posted.

**Q77: How do you run an effective daily standup asynchronously?**
A: Post by a fixed time (e.g., 9 AM IST): **Yesterday**: what shipped. **Today**: what you're working on. **Blockers**: anything preventing progress. Keep it under 5 lines. Use a dedicated Slack channel or Notion page. This replaces a 15-minute meeting with a 2-minute read that everyone can consume on their own schedule.

**Q78: How do you handle being the only team member in a timezone?**
A: Over-communicate async updates. Document decisions in writing so the next timezone can pick up. Leave clear handoff notes at end of day: "Here's where I left off, here's what needs review when you're online." Keep a shared task board visible across timezones. The goal is zero blockers when you log off.

**Q79: How do you prevent burnout in a remote startup with US hours?**
A: Hard boundaries: no Slack after a defined hour (except genuine emergencies). Use Do Not Disturb aggressively. Block your calendar for sleep and personal time. Communicate your availability hours to the team. A sustainable pace beats a heroic sprint every time — startups are marathons, not sprints.

**Q80: What tools do you use for async collaboration?**
A: Slack (structured threads, not random DMs), Notion or Confluence (docs and wikis), Loom (screen recordings for demos and walkthroughs), Linear or Jira (task tracking), GitHub (code review and discussions), Figma (design review). The tool doesn't matter — what matters is that everything is written and searchable.

**Q81: How do you build rapport with remote teammates you rarely see in person?**
A: Small consistent actions: acknowledge their work publicly in Slack, ask about their day briefly in standups, share wins and celebrations. Be reliable — do what you say you'll do. Trust is built remotely through consistency, not social events. Show genuine interest in their work and opinions.

**Q82: How do you handle a meeting that should have been a Slack message?**
A: Politely suggest it: "For next time, I think this could be an async update — I'll post a summary in the channel." Propose a decision framework for when to meet vs. when to write: "Meet if: decision needed in <1 hour, or disagreement needs real-time resolution. Write if: status update, FYI, or async-input-needed."

**Q83: How do you communicate effectively when you can't see the other person's face?**
A: Be extra explicit about tone and intent. Use emoji sparingly for tone ("I think we should go with A 😊 — happy to discuss"). Write "I'm not criticising, just brainstorming" if feedback could read harshly. Assume positive intent. When in doubt, a 30-second Loom video conveys tone better than 10 paragraphs of text.

**Q84: How do you manage your work environment for productivity at home?**
A: Dedicated workspace (even a specific corner), noise-cancelling headphones, consistent work hours, separate browser profiles for work and personal, and a ritual that signals "start of workday" (making coffee, opening tools in the same order). Treat remote work with the same discipline as office work.

**Q85: How do you handle being on-call or available outside hours for a remote startup?**
A: Agree on clear on-call expectations: what constitutes an emergency, response time SLA, and how you'll be alerted. Keep a runbook for common incidents so you don't have to debug from scratch at 2 AM. Rotate on-call duties if the team is large enough. Log every incident for future prevention.

---

## Support and Maintenance (Q86–Q90)

**Q86: How do you write a user-facing incident status page update?**
A: Template: "We are currently experiencing [issue]. Impact: [which users/features]. Investigating/identified/monitoring/resolved. ETA: [if known]. We'll update in [X minutes]." Tone: calm, factual, empathetic. Never blame the user. Never speculate about root cause publicly before confirming.

**Q87: How do you triage incoming bug reports?**
A: Classify by severity: **P0** (production down, data loss) → fix immediately. **P1** (major feature broken, workaround exists) → fix today. **P2** (minor feature broken, no workaround) → fix this sprint. **P3** (cosmetic, enhancement) → backlog. Use the user's language when describing the bug in tracking tools — don't translate it into engineering jargon.

**Q88: How do you write release notes for a non-technical audience?**
A: Focus on "what changed for you" not "what we did internally." Example: "New: You can now export your agent conversations as PDF. Improved: Search results are now 50% faster. Fixed: Login no longer fails on Safari." Use plain language, avoid version numbers as the headline, and link to full docs for technical details.

**Q89: How do you handle a support ticket that you can't resolve immediately?**
A: Acknowledge receipt within 1 hour. Reproduce the issue. If you can't fix it today, provide: "I've confirmed the issue. Here's what's happening: [brief explanation]. Workaround: [if any]. I'm working on a fix and expect it by [time]. I'll update you then." Set expectations and follow through.

**Q90: How do you prioritise between new feature development and bug fixes?**
A: Bugs that affect multiple users or core functionality come first. Features that are on the critical path to launch come second. Everything else is backlog. Communicate the trade-off: "I'm spending today fixing the auth bug affecting 40 users. The search feature ships tomorrow instead of today." Data-driven prioritisation, not gut feel.

---

## Knowledge Management (Q91–Q95)

**Q91: How do you structure a team wiki or knowledge base?**
A: Top-level categories: (1) Getting Started (onboarding, setup); (2) Architecture (diagrams, ADRs); (3) How-To Guides (task-oriented); (4) Runbooks (incident response, maintenance); (5) Reference (API docs, config). Use consistent templates for each page. Every page has an owner and a "last verified" date.

**Q92: How do you make documentation searchable and discoverable?**
A: Use a tool with full-text search (Notion, Confluence, or a static site with Algolia). Name files and headings with the words people would actually search for ("How to deploy a Worker" not "Deployment Procedures v2"). Add tags. Include a docs FAQ that links to detailed pages. Maintain a "Start Here" page for new team members.

**Q93: How do you preserve institutional knowledge when a team member leaves?**
A: (1) Require handoff documents for every role (see Q39); (2) pair programming and knowledge-sharing sessions before departure; (3) all knowledge in writing, not in DMs or private notes; (4) cross-train on critical systems. The goal is that no single person is the only source of truth for anything.

**Q94: How do you maintain a living document vs. a one-time write-up?**
A: Assign an owner and a review cadence. Use "evergreen" headers instead of date-based articles. Include "Last verified: [date]" on every page. Add documentation tasks to the sprint. When code changes, check if docs need updating in the same PR. Stale docs are liabilities.

**Q95: How do you onboard a new team member using your knowledge base?**
A: Create a 30-60-90 day onboarding plan. Day 1: read the README, set up the dev environment, deploy something to staging. Week 1: read architecture docs, make a small code change, join one customer interaction. Month 1: own a small feature end-to-end. Track onboarding progress and ask for feedback on doc gaps.

---

## Behavioral Interview (Q96–Q100)

**Q96: Tell me about yourself.**
A: "I'm Aayush, a developer focused on AI agent systems and technical documentation. I've contributed to open-source projects where I wrote documentation and reviewed community PRs. During a startup internship, I worked across the stack — from fixing bugs to writing runbooks — and learned how to thrive in fast-moving, ambiguous environments. I'm drawn to DFDSOFT because building AI agents for entrepreneurs matches exactly the kind of work where I do my best thinking and shipping."

**Q97: Why this role at DFDSOFT specifically?**
A: "Three reasons. First, the intersection of AI agents and documentation is where I want to spend my career — agents are only as good as the instructions that guide them, and I love making those instructions precise and effective. Second, DFDSOFT's startup culture means I'll wear many hats and learn fast, which is how I grow best. Third, working with entrepreneurs building real products means my work has immediate impact — not theoretical, not six months away."

**Q98: Describe a time you dealt with ambiguity.**
A: "During a hackathon, our team had 12 hours to build an AI-powered tool and no clear product spec. I took the lead on defining the scope: I identified the core user problem, wrote a one-page spec, and divided the work. We shipped a working prototype in 10 hours. The lesson: when no one knows exactly what to build, the person who clarifies the goal — even imperfectly — enables everyone else to move fast. I'd apply the same approach at DFDSOFT when a founder gives a vague brief."

**Q99: How do you handle quick pivots?**
A: "At my startup internship, we pivoted our agent framework mid-sprint when the underlying API changed. I documented the old approach, identified what was reusable, and wrote a migration plan in an afternoon. The team was back on track within a day. I've learned that pivots are not failures — they're the startup version of optimising. The key is documenting why the pivot happened so you don't accidentally pivot back."

**Q100: Describe your most challenging project and what you learned.**
A: "During a student project, I built an AI agent that needed to integrate with three different APIs, each with different auth, rate limits, and data formats. The hardest part was not the code — it was documenting the integration clearly enough that my teammates could maintain it. I created architecture diagrams, API reference sheets, and a troubleshooting guide. The agent worked, but the real win was that two new contributors could make changes within a day of joining. The lesson: code ships features, but documentation ships teams. At DFDSOFT, I'd bring that same discipline to every agent and workflow I build."
