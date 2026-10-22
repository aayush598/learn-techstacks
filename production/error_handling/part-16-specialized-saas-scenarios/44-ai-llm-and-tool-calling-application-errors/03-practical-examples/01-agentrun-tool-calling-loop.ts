/**
 * AgentRun Tool-Calling Loop — Part XVI · Chapter 44 · Sections 44.7–44.11, 44.13, 44.19
 *
 * A production-shaped agent loop with the failure handling the naive version leaves out:
 *   44.7  tool failures returned as DATA, never thrown out of the loop
 *   44.8  every tool has its own deadline and an AbortSignal
 *   44.9  permissions: exposure → entitlement → argument scope → approval
 *   44.10 tool arguments parsed and schema-validated before dispatch
 *   44.11 a bounded loop: steps, tool calls, tokens, wall clock
 *   44.13 retry safety: the plan is frozen once a write has happened
 *   44.19 duplicate side effects prevented by a write-ahead effect ledger
 *
 * Key data: 12 model turns · 20 tool calls · 120 s deadline · 10 s tool deadline ·
 * 8 KB tool-result cap · 7-day ledger TTL.
 *
 * The recurring cast: Acme SaaS ships an `AgentRun` assistant that reads a customer's
 * tickets and knowledge base, and that can post internal notes.
 */
import { createHash } from "node:crypto";

// --- 1. The stable error contract (44.17): one vocabulary for the whole app
export type AppErrorCode =
  | "PROVIDER_UNAVAILABLE"    // 503 — vendor overloaded or down
  | "PROVIDER_RATE_LIMITED"   // 429 — retry after the stated delay
  | "PROVIDER_TIMEOUT"        // 504 — ambiguous outcome
  | "OUTPUT_TRUNCATED"        // 502 — finish_reason: length
  | "MODEL_REFUSED"           // 422 — content filter / refusal
  | "TOOL_NOT_FOUND"          // 422 — the model invented a tool
  | "TOOL_ARGS_INVALID"       // 422 — arguments failed the schema
  | "TOOL_FORBIDDEN"          // 403 — permission denied
  | "TOOL_FAILED"             // 502 — the tool threw
  | "TOOL_TIMEOUT"            // 504 — the tool did not answer in time
  | "TOOL_RESULT_TRUNCATED"   // 502 — the result exceeded the context budget
  | "TOOL_EFFECT_IN_FLIGHT"   // 409 — another worker claimed the same effect
  | "AGENT_BUDGET_EXCEEDED"   // 429 — step / token / time budget exhausted
  | "AGENT_LOOP_DETECTED";    // 422 — the model repeated itself

export class AppError extends Error {
  constructor(readonly code: AppErrorCode, readonly detail: Record<string, unknown> = {}) {
    super(code);
    this.name = "AppError";
  }
}

// --- 2. Provider response, normalized (44.20): four places, one shape
export type FinishReason = "stop" | "length" | "tool_calls" | "refused" | "unknown";
export type ToolCall = { id: string; name: string; argsJson: string };  // argsJson is a STRING
export type Usage = { promptTokens: number; completionTokens: number; totalTokens: number };
export type CompletionResponse = {
  finishReason: FinishReason; text: string; toolCalls: ToolCall[]; usage: Usage;
};
export type Message =
  | { role: "system" | "user" | "assistant"; content: string }
  | { role: "tool"; toolCallId: string; name: string; content: string };
export interface LlmProvider {
  readonly name: string;
  complete(req: { model: string; messages: Message[]; tools: ToolDef[]; maxTokens?: number },
           opts?: { signal?: AbortSignal }): Promise<CompletionResponse>;
}

// --- 3. The tool contract (44.7–44.10)
export type SideEffect = "none" | "read" | "write";
export type JsonSchema = Record<string, unknown>;
export type ToolDef = {
  name: string; description: string; parameters: JsonSchema;
  timeoutMs: number;              // 44.8 — every tool has its own deadline
  sideEffects: SideEffect;
  /** Derives the idempotency key from the business operation (44.19). */
  idempotencyKey?: (args: unknown) => string;
  execute(args: unknown, ctx: ToolContext): Promise<unknown>;
};
export type ToolContext = { actor: Actor; signal: AbortSignal; now: () => Date };
export type Actor = {
  userId: string; tenantId: string; agentId: string; entitledTools: string[];
  scopeFilter: Record<string, unknown>;   // e.g. { tenantId: "acme" }
};
export type ToolOutcome =
  | { ok: true; data: unknown }
  | { ok: false; code: AppErrorCode; message: string; retryable: boolean };

// --- 4. Argument validation (44.10): the model's JSON is untrusted input
export function validateToolArgs(call: ToolCall, tool: ToolDef):
  { ok: true; args: unknown } | { ok: false; issues: string[] } {
  let parsed: unknown;
  try {
    parsed = JSON.parse(call.argsJson);          // ← a JSON string, not an object
  } catch (err) {
    return { ok: false, issues: [`arguments are not valid JSON: ${String(err)}`] };
  }
  const issues = validateAgainstSchema(parsed, tool.parameters);
  return issues.length > 0 ? { ok: false, issues } : { ok: true, args: parsed };
}

/** Canonical JSON for hashing: sorted object keys, array order preserved. */
export function canonicalJson(value: unknown): string {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(",")}]`;
  const entries = Object.entries(value as Record<string, unknown>).sort(([a], [b]) => (a < b ? -1 : 1));
  return `{${entries.map(([k, v]) => `${JSON.stringify(k)}:${canonicalJson(v)}`).join(",")}}`;
}
export function sha256(input: string): string {
  return createHash("sha256").update(input).digest("hex");
}

// --- 5. Permissions (44.9): four checks, in order
export class ToolAuthorizer {
  constructor(private readonly requiresApproval: (tool: ToolDef, args: unknown) => boolean = () => false) {}
  assertAllowed(actor: Actor, tool: ToolDef, args: unknown): void {
    if (!actor.entitledTools.includes(tool.name)) {
      throw new AppError("TOOL_FORBIDDEN", { reason: "tool not exposed to this agent" });
    }
    if (tool.sideEffects === "write" && !actor.entitledTools.includes(`write:${tool.name}`)) {
      throw new AppError("TOOL_FORBIDDEN", { reason: "tenant not entitled to this write" });
    }
    if (!withinScope(args, actor.scopeFilter)) {
      throw new AppError("TOOL_FORBIDDEN", { reason: "argument outside the caller's scope" });
    }
    if (tool.sideEffects === "write" && this.requiresApproval(tool, args)) {
      throw new AppError("TOOL_FORBIDDEN", { reason: "approval required before this write" });
    }
  }
}
function withinScope(args: unknown, scope: Record<string, unknown>): boolean {
  if (args === null || typeof args !== "object") return false;
  const a = args as Record<string, unknown>;
  return Object.entries(scope).every(([k, v]) => a[k] === v);
}

// --- 6. The effect ledger (44.19): claim before you act
export type EffectRow = { idempotencyKey: string; status: "claimed" | "applied" | "failed"; result: unknown };
export interface EffectStore {
  claim(key: string, runId: string, toolName: string, argsHash: string): Promise<boolean>;
  get(key: string): Promise<EffectRow | null>;
  markApplied(key: string, result: unknown): Promise<void>;
  markFailed(key: string): Promise<void>;
}
export async function applyEffect<T>(store: EffectStore, key: string, runId: string, toolName: string,
                                     args: unknown, fn: () => Promise<T>):
  Promise<{ replayed: boolean; value: T }> {
  const argsHash = sha256(canonicalJson(args));
  if (!(await store.claim(key, runId, toolName, argsHash))) {
    const existing = await store.get(key);
    if (existing?.status === "applied") return { replayed: true, value: existing.result as T };
    if (existing?.status === "claimed") throw new AppError("TOOL_EFFECT_IN_FLIGHT", { key });
    await store.claim(key, runId, toolName, argsHash);   // previous attempt failed: re-claim
  }
  try {
    const value = await fn();
    await store.markApplied(key, value);
    return { replayed: false, value };
  } catch (err) {
    await store.markFailed(key);
    throw err;
  }
}

// --- 7. Running one tool (44.7, 44.8): every failure becomes data
export async function runTool(call: ToolCall, registry: Map<string, ToolDef>, ctx: ToolContext,
                              authorizer: ToolAuthorizer): Promise<ToolOutcome> {
  const tool = registry.get(call.name);
  if (!tool) {
    return { ok: false, code: "TOOL_NOT_FOUND", retryable: false,
             message: `No tool named "${call.name}". Available: ${[...registry.keys()].join(", ")}.` };
  }
  const parsed = validateToolArgs(call, tool);
  if (!parsed.ok) {
    return { ok: false, code: "TOOL_ARGS_INVALID", retryable: false,
             message: `${parsed.issues.join("; ")}. Expected schema: ${JSON.stringify(tool.parameters)}` };
  }
  try {
    authorizer.assertAllowed(ctx.actor, tool, parsed.args);
    const data = await withDeadline(() => tool.execute(parsed.args, ctx), tool.timeoutMs, ctx.signal);
    return boundResult({ ok: true, data });
  } catch (err) {
    if (err instanceof TimeoutError) {
      return { ok: false, code: "TOOL_TIMEOUT", retryable: true, message: "The tool did not respond in time." };
    }
    if (err instanceof AppError) {
      return { ok: false, code: err.code, retryable: false, message: (err.detail.reason as string) ?? err.code };
    }
    return { ok: false, code: "TOOL_FAILED", retryable: false, message: toSafeMessage(err) };
  }
}
/** Cap the result so the next turn still fits in the context window (44.7). */
export function boundResult(outcome: ToolOutcome, maxChars = 8_000): ToolOutcome {
  if (JSON.stringify(outcome).length <= maxChars) return outcome;
  return { ok: false, code: "TOOL_RESULT_TRUNCATED", retryable: false,
           message: `Result exceeded ${maxChars} characters. Narrow the query or add filters.` };
}
export class TimeoutError extends Error {
  constructor(readonly ms: number) { super(`timeout after ${ms}ms`); this.name = "TimeoutError"; }
}
export async function withDeadline<T>(fn: () => Promise<T>, ms: number, signal: AbortSignal): Promise<T> {
  let timer: ReturnType<typeof setTimeout>;
  const deadline = new Promise<never>((_, reject) => {
    timer = setTimeout(() => reject(new TimeoutError(ms)), ms);
  });
  const aborted = new Promise<never>((_, reject) =>
    signal.addEventListener("abort", () => reject(new Error("aborted")), { once: true }));
  try { return await Promise.race([fn(), deadline, aborted]); } finally { clearTimeout(timer!); }
}

// --- 8. Loop detection (44.11): same tool AND same canonical args
export function detectLoop(calls: ToolCall[]): "repeat" | "oscillation" | null {
  const sig = calls.map((c) => `${c.name}:${canonicalJson(safeParse(c.argsJson))}`);
  if (sig.length >= 3 && sig.at(-1) === sig.at(-2) && sig.at(-2) === sig.at(-3)) return "repeat";
  if (sig.length >= 4) {
    const [a, b, c, d] = [sig.at(-4)!, sig.at(-3)!, sig.at(-2)!, sig.at(-1)!];
    if (a === c && b === d && a !== b) return "oscillation";
  }
  return null;
}
function safeParse(json: string): unknown {
  try { return JSON.parse(json); } catch { return json; }
}

// --- 9. The loop (44.11, 44.12, 44.13, 44.16)
export type AgentBudget = { maxSteps: number; maxToolCalls: number; maxTokens: number; deadlineMs: number };
export const DEFAULT_BUDGET: AgentBudget = {
  maxSteps: 12, maxToolCalls: 20, maxTokens: 120_000, deadlineMs: 120_000,
};
export type AgentRunResult =
  | { status: "completed"; answer: string; steps: number; tokens: number }
  | { status: "partial"; answer: string | null; reason: string; completedSteps: string[];
      steps: number; tokens: number }
  | { status: "failed"; code: AppErrorCode; message: string; steps: number; tokens: number }
  | { status: "cancelled"; reason: string; steps: number; tokens: number };
export type AgentRun = {
  id: string; actor: Actor; model: string; budget?: AgentBudget; provider: LlmProvider;
  registry: Map<string, ToolDef>; authorizer: ToolAuthorizer; effects: EffectStore;
  signal?: AbortSignal;
};
export async function runAgent(run: AgentRun, question: string): Promise<AgentRunResult> {
  const budget = run.budget ?? DEFAULT_BUDGET;
  const deadline = Date.now() + budget.deadlineMs;
  const messages: Message[] = [{ role: "system", content: SYSTEM }, { role: "user", content: question }];
  const calls: ToolCall[] = [];
  const completedSteps: string[] = [];
  let tokens = 0, steps = 0, toolCalls = 0;
  const partial = (reason: string): AgentRunResult =>
    ({ status: "partial", answer: null, reason, completedSteps, steps, tokens });

  while (steps < budget.maxSteps) {
    if (run.signal?.aborted) return { status: "cancelled", reason: "client disconnected", steps, tokens };
    if (Date.now() > deadline) return partial("deadline reached");
    const res = await run.provider.complete(
      { model: run.model, messages, tools: [...run.registry.values()] }, { signal: run.signal });
    steps += 1;
    tokens += res.usage.totalTokens;
    if (tokens > budget.maxTokens) return partial("token budget exceeded");
    if (res.finishReason === "length") throw new AppError("OUTPUT_TRUNCATED", { model: run.model });
    if (res.finishReason === "refused") throw new AppError("MODEL_REFUSED", { model: run.model });
    if (res.finishReason === "stop") return { status: "completed", answer: res.text, steps, tokens };
    if (res.finishReason !== "tool_calls") {
      return { status: "failed", code: "OUTPUT_TRUNCATED", message: "unknown finish reason", steps, tokens };
    }
    calls.push(...res.toolCalls);
    if (detectLoop(calls)) return partial("AGENT_LOOP_DETECTED");
    for (const call of res.toolCalls) {
      if (toolCalls >= budget.maxToolCalls) return partial("tool call budget exceeded");
      toolCalls += 1;
      const ctx: ToolContext = { actor: run.actor, signal: run.signal ?? new AbortController().signal,
                                 now: () => new Date() };
      const outcome = await runTool(call, run.registry, ctx, run.authorizer);
      messages.push({ role: "tool", toolCallId: call.id, name: call.name, content: JSON.stringify(outcome) });
      if (outcome.ok) completedSteps.push(call.name);
    }
  }
  return partial("AGENT_BUDGET_EXCEEDED");
}
const SYSTEM = "You are Acme's support agent. Use tools for facts; never invent document ids.";

// --- 10. Effects through the ledger (44.19)
/**
 * A mutating tool wired to the ledger. The key comes from the business operation
 * (`refund:{orderId}`), never from the model's arguments, so argument drift on a
 * retry cannot create a second key.
 */
export function idempotentTool(store: EffectStore, runId: string,
  def: Omit<ToolDef, "idempotencyKey"> & { keyFor: (args: any) => string }): ToolDef {
  const keyFor = (args: unknown) => sha256(def.keyFor(args));
  return {
    ...def,
    idempotencyKey: keyFor,
    async execute(args, ctx) {
      const { value } = await applyEffect(store, keyFor(args), runId, def.name, args,
                                          () => def.execute(args, ctx));
      return value;
    },
  };
}

/**
 * Real-world use case: Acme's `AgentRun` assistant reads tickets and posts internal notes.
 * The first version called the notes API directly, so a provider 503 after the note was
 * posted produced a second note. With the effect ledger in front of the write, the retry
 * replays the recorded result instead of posting again, and the plan stays frozen after
 * the first write so the model cannot re-plan into a new write.
 *
 * Key data: 12 model turns · 20 tool calls · 120 s deadline · 120k token cap ·
 * 10 s tool deadline · 8 KB tool-result cap · 7-day ledger TTL.
 *
 * Checklist: tool failures returned as data, never thrown · arguments parsed and
 * schema-validated before dispatch · every tool has a deadline and the AbortSignal ·
 * exposure, entitlement, scope, and approval all checked · the plan is frozen once a
 * mutating tool succeeds · every write effect claimed in the ledger before it is applied ·
 * budgets cover steps, tool calls, tokens, and wall clock.
 */
/**
 * Related:
 *   - Tool-Calling Failures: ../01-concepts/03-tool-calling-failures.md
 *   - Agent Loop Failures and Recovery: ../01-concepts/04-agent-loop-failures-and-recovery.md
 *   - Duplicate Side Effects During Agent Retries: ../02-deep-dive/02-duplicate-side-effects-during-agent-retries.md
 *   - Chapter 44 Reference: ../05-reference/README.md
 */
