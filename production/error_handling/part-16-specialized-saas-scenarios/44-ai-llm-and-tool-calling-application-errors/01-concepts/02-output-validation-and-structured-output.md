# Output Validation and Structured Output

> Part XVI · Chapter 44 · Sections 44.5–44.6 · _Estimated reading time: 26 min_
> **Prerequisite:** [Provider and Quota Failures](./01-provider-and-quota-failures.md)

## In one sentence

A model response is **untrusted input that arrived over HTTP 200** — so you must
**validate it against a schema at the boundary** and treat a validation failure as a
*recoverable, bounded* condition, not as a 500.

## Why this matters in production

Everything downstream of the model assumes its output is well-formed: `JSON.parse` before
you read a field, a type checker before you call a function, a serializer before you write
to the database. When the model returns something slightly wrong, those assumptions fail
in the worst possible place — deep inside business logic, where the stack trace says
`Cannot read properties of undefined (reading 'id')` and the log contains the user's
entire document.

The failure is also **silent when it should be loud**. A model asked for a JSON object and
given prose instead sometimes returns perfectly valid JSON — `{}` — or a JSON object whose
fields are empty strings. It parses. It type-checks against a loose schema. And it is
useless. Schema validation with `required` fields catches it; `JSON.parse` never will.

## 44.5 — Invalid output: four distinct shapes

"Invalid output" is not one failure. Treating them the same is why teams end up with a
retry loop that never helps.

| Shape | HTTP | `finish_reason` | Symptom | Recoverable? |
| ----- | ---- | --------------- | ------- | ------------ |
| **Empty** | 200 | `stop` | Body is `""` or whitespace | ✅ Repair turn |
| **Truncated** | 200 | `length` | Output stops mid-sentence or mid-JSON | ✅ Raise `max_tokens`, then repair |
| **Refused** | 200 | `content_filter` / `refusal` | Empty or safety text | ❌ Do not retry the same prompt |
| **Wrong shape** | 200 | `stop` | Valid JSON, wrong fields | ✅ Repair turn with the schema errors |
| **Not JSON at all** | 200 | `stop` | Prose, Markdown fences, apology | ✅ Repair turn |

### The parse ladder

Validate in layers, cheapest first. Each layer has a different repair strategy:

```ts
export type ValidationStage =
  | "parse"        // is it JSON at all?
  | "schema"       // does it match the schema?
  | "semantic";    // are the values plausible?

export type OutputValidation =
  | { ok: true; value: unknown; stage: ValidationStage }
  | { ok: false; stage: ValidationStage; issues: string[]; raw: string };

export function validateOutput(raw: string, schema: JsonSchema): OutputValidation {
  const text = stripCodeFences(raw).trim();     // ```json ... ``` happens constantly
  if (text === "") return { ok: false, stage: "parse", issues: ["empty output"], raw };

  let parsed: unknown;
  try {
    parsed = JSON.parse(text);
  } catch (err) {
    return { ok: false, stage: "parse", issues: [String(err)], raw };
  }

  const issues = validateAgainstSchema(parsed, schema);   // Ajv, Zod, JSON Schema, …
  if (issues.length > 0) return { ok: false, stage: "schema", issues, raw };

  const semantic = validateSemantics(parsed);             // your business rules
  if (semantic.length > 0) return { ok: false, stage: "semantic", issues: semantic, raw };

  return { ok: true, value: parsed, stage: "semantic" };
}
```

**Key data:** stripping Markdown fences before parsing is not optional. Models wrap JSON
in ```` ```json ```` far more often than teams expect, especially when asked for "just the
JSON". Also strip a leading prose preamble ("Here is the JSON:") and a trailing comma.

### Semantic validation is the layer teams skip

Schema validation answers "is this the right shape?"; semantic validation answers "is this
the right *content*?" A `SupportTicket` with `severity: "high"` is schema-valid and
meaningless if `ticket_id` is empty or `assigned_to` is the literal string `"unknown"`.

```ts
export function validateSemantics(value: unknown): string[] {
  const t = value as SupportTicket;
  const issues: string[] = [];
  if (!t.ticket_id?.trim()) issues.push("ticket_id must not be empty");
  if (t.severity === "critical" && !t.assignee) issues.push("critical tickets need an assignee");
  if (t.customer_email && !t.customer_email.includes("@")) issues.push("customer_email is malformed");
  return issues;
}
```

## The repair turn

When validation fails, the cheapest correct recovery is to **ask the model again, with the
error**, exactly once:

```ts
export async function completeWithRepair(
  client: LlmClient, req: CompletionRequest, schema: JsonSchema,
): Promise<{ value: unknown; attempts: number }> {
  let messages = [...req.messages];
  let last: OutputValidation | null = null;

  for (let attempt = 0; attempt < 2; attempt++) {      // 1 initial + 1 repair
    const res = await client.complete({ ...req, messages });
    if (res.finishReason === "length") {
      throw new AppError("OUTPUT_TRUNCATED", { model: req.model });   // raise the cap instead
    }
    if (res.finishReason === "content_filter" || res.finishReason === "refusal") {
      throw new AppError("MODEL_REFUSED", { model: req.model });
    }
    const check = validateOutput(res.text, schema);
    if (check.ok) return { value: check.value, attempts: attempt + 1 };
    last = check;
    messages = [
      ...req.messages,
      { role: "assistant", content: res.text },
      { role: "user", content: repairPrompt(check) },
    ];
  }
  throw new AppError("OUTPUT_INVALID", {
    stage: last?.stage, issues: last?.issues?.slice(0, 5), attempts: 2,
  });
}

function repairPrompt(check: OutputValidation): string {
  return [
    "Your previous response did not pass validation.",
    `Stage: ${check.stage}.`, `Problems: ${check.issues.join("; ")}`,
    "Return ONLY the corrected JSON object. No prose, no code fences.",
  ].join(" ");
}
```

> ⚠️ **Hazard.** A repair turn is a **new inference**: it costs tokens and latency, and it
> can fail in a different way. Bound it at **one** repair attempt, then fail with a stable
> code. A loop that repairs up to five times is a latency incident waiting to happen and
> often hides a prompt-design bug.

**Key data:** one repair turn is the recommended default. Repair doubles cost and latency
for that call, so budget it explicitly rather than letting it happen implicitly.

## 44.6 — Structured output validation

Providers offer three increasing levels of output guarantee, and picking the right one
removes most validation work.

| Mechanism | Guarantee | Still must validate? |
| --------- | --------- | -------------------- |
| **Free-form text** | None | ✅ Yes, always |
| **JSON mode** | Valid JSON | ✅ Yes — schema only |
| **JSON-schema mode** (`strict`) | JSON matching the schema | ✅ Yes — semantics only |
| **Tool-based structured output** | Valid JSON in a tool-call argument | ✅ Yes — the schema is *your* tool's |

```ts
// Schema mode: the provider constrains generation to the schema.
const res = await client.complete({
  model: "acme-large-1",
  messages,
  responseFormat: {
    type: "json_schema",
    jsonSchema: {
      name: "support_ticket",
      strict: true,                                  // no extra keys, all required
      schema: {
        type: "object",
        additionalProperties: false,
        required: ["ticket_id", "severity", "summary"],
        properties: {
          ticket_id: { type: "string" },
          severity: { type: "string", enum: ["low", "medium", "high", "critical"] },
          summary: { type: "string", minLength: 1 },
        },
      },
    },
  },
});
```

Schema mode removes *shape* failures, not *content* failures. `ticket_id: ""` still
passes. `severity: "medium"` when the source text says "our production is down" is
schema-valid and operationally wrong. Always run the semantic layer on top.

### Where validation belongs

```text
provider bytes
   │
   ├─ parse (JSON.parse)          ← adapter layer
   ├─ schema validate             ← adapter layer
   ├─ semantic validate            ← domain layer
   ▼
domain value (typed, trusted)
```

The adapter owns the first two because they are about the *wire format*. The domain owns
the third because it is about *meaning*. Mixing them means the domain starts handling
`SyntaxError` from `JSON.parse`, and the adapter starts knowing what a `SupportTicket` is.

> ⚠️ **Hazard.** `strict: true` schema mode commonly requires **every** property to be in
> `required` and `additionalProperties: false`. Omitting them is rejected at request time
> with a 400 that reads like a model error but is a schema mistake.

### Validating the tool-call path

When the model answers through a tool call, the arguments are a **JSON string**, not an
object. Forgetting to parse it is the most common bug in tool-calling code:

```ts
const call = res.toolCalls[0];
const args = JSON.parse(call.function.arguments);     // ← a string, not an object
const parsed = validateAgainstSchema(args, tool.parameters);
if (!parsed.ok) throw new AppError("TOOL_ARGS_INVALID", { issues: parsed.issues });
```

**Key data:** `tool_calls[].function.arguments` is a **JSON-encoded string**. A schema
violation in tool arguments is a *model* error, but it is also a *your-tool-schema* error
— if the model repeatedly produces invalid arguments for the same tool, tighten the schema
and the description before you add retries.

## Worked example — ticket triage

Acme's support bot triages inbound tickets into a structured `SupportTicket`. The first
implementation did `JSON.parse(res.text)` and read `.severity`. In production:

- 4% of responses were wrapped in Markdown fences, so `JSON.parse` threw and surfaced as a
  500.
- 1.5% came back as prose ("I've analyzed the ticket and it appears to be a billing
  issue") and surfaced as `undefined` three layers down.
- 0.8% were truncated at `max_tokens: 512` because the model wrote a long summary first;
  `JSON.parse` threw on the cut-off object.
- 0.2% were valid JSON with `severity: "unknown"` — a value outside the enum — which the
  old code accepted and then used to route a P1 ticket to the queue for "other".

The rebuild: schema mode with `strict: true` and a closed enum, a parse ladder
(parse → schema → semantic), one repair turn that feeds the validation errors back, and a
`finish_reason` check before anything else. The user-visible error rate for this feature
went from ~6% to 0.1%, and the 0.1% that remained were genuine refusals and truncations,
now reported as distinct codes instead of a generic 500.

## Key data

| Fact | Value |
| ---- | ----- |
| JSON-mode guarantee | Valid JSON, no schema conformance |
| Schema-mode guarantee | Conforms to the submitted JSON Schema (`strict: true` ⇒ all fields required, no extra keys) |
| Tool-call arguments | A JSON **string** in `tool_calls[].function.arguments` |
| Validation layers | parse → schema → semantic |
| Repair turns | **1** recommended; hard-fail after that |
| Refusal signals | `finish_reason: content_filter`, `finish_reason: refusal` |
| Truncation signal | `finish_reason: length` |
| Markdown fences | Strip ```` ```json ```` and prose preambles before parsing |
| Cost of a repair turn | One extra inference: doubles that call's tokens and latency |

## Real-world use case

A multi-tenant SaaS adds an "extract action items from a meeting transcript" feature. The
output drives an automation that emails the customer and creates tasks, so a malformed
response does not just fail a request — it can create tasks with no owner.

The team validated at the boundary with a three-layer check: `JSON.parse` (after fence
stripping), JSON Schema (`required: ["action_items", "due_dates"]`, `additionalProperties:
false`), then a semantic pass that rejects an action item with no `owner` or a `due_date`
in the past. Invalid output triggered exactly one repair turn that included the concrete
validation errors; a second failure returned `OUTPUT_INVALID` with the stage and the
first five issues, and the transcript was attached to the run for review.

The measured result: invalid-output incidents fell from 7% of runs to 0.2%, and the
remaining failures were actionable — the team could read "stage: schema, missing
`due_dates`" and fix the prompt, instead of reading a stack trace.

## Trade-offs

| Approach | Pros | Cons | When to use |
| -------- | ---- | ---- | ----------- |
| Free-form + strict validation | Works with every provider | High invalid rate, needs repair turns | Portability across providers |
| JSON mode + schema validation | Simple, widely supported | Only guarantees valid JSON | Providers without schema mode |
| Schema mode (`strict`) | Shape errors nearly vanish | Provider-specific, stricter field rules | ✅ Default when available |
| Tool-based structured output | Reuses your tool layer and its validation | Tool-call plumbing, argument string parsing | When the output *is* a tool call |
| Repair turns | Recovers most invalid output | Doubles cost/latency for that call | ✅ Once, bounded |
| Silent fallback to prose | Never fails | The prose is unparseable downstream | Never |
| Schema validation only | Cheap | Misses `severity: "unknown"` | Never alone |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Validate at the boundary, before the domain sees the value | `JSON.parse` deep inside business logic |
| Check `finish_reason` before validating the body | Assume 200 means the content is usable |
| Use `strict: true` and `additionalProperties: false` | Leave optional fields out of `required` |
| Bound the repair turn at one attempt | Loop repairs until one passes |
| Feed the concrete validation errors into the repair prompt | Say "your output was invalid" |
| Strip code fences and prose preambles | Assume the body is bare JSON |
| Keep a semantic layer on top of schema validation | Trust schema conformance alone |
| Parse `tool_calls[].function.arguments` as JSON | Treat it as an object |

## Common mistakes

- **`JSON.parse` without a fence strip.** The most common single line of failure in LLM
  code.
- **Validating before checking truncation.** A truncated object often passes a loose schema.
- **Loose schemas.** `severity: { type: "string" }` accepts `"unknown"`; use an `enum`.
- **Unbounded repair loops.** Five repair turns is five inferences and a 30-second request.
- **Schema validation only.** Content-level nonsense passes every shape check.
- **Treating a refusal as an empty string.** `content_filter` and `refusal` are distinct
  outcomes and deserve distinct codes.
- **Validating in the domain.** Every layer now catches `SyntaxError`.

## Checklist

- [ ] The body is parsed, schema-validated, and semantically validated in that order.
- [ ] Code fences and prose preambles are stripped before parsing.
- [ ] `finish_reason` is checked before the body is used.
- [ ] Truncation, refusal, and invalid output have distinct internal codes.
- [ ] Schema mode is used with `strict: true` and `additionalProperties: false`.
- [ ] The repair turn is bounded at one and includes concrete validation errors.
- [ ] Tool-call arguments are parsed as JSON and validated against the tool schema.
- [ ] Validation lives at the boundary; the domain receives a typed value.

## Related

- [Provider and Quota Failures](./01-provider-and-quota-failures.md)
- [Tool-Calling Failures](./03-tool-calling-failures.md)
- [Agent Workflow and Provider Portability](./04-agent-loop-failures-and-recovery.md)
- [Chapter 44 Reference](../05-reference/README.md)
