# Infosys SP DSE — 100 MigratorGen Interview Q&A

> Based on the MigratorGen project by Aayush Gid — "AST-accurate, transaction-safe code migration with a REST API, MCP server, and parallel execution support." All answers are grounded in the actual implementation in the repo (`sdk/python/src/migrator_gen/`, `cli/`, `mcp/`, `backend/`).
> Candidate: Aayush Gid — B.Tech E&C | Agentic AI / AI Agent / Data Science Internships | MigratorGen, ScriptVector, OpenRTL.ai, Agno Open-Source PRs | IEEE Publication (2024)
> Scope: Deep-dive on MigratorGen only — architecture, LibCST transformers, transactional engine, version resolution, validation, symbol resolution, parallel execution, LLM integration, API/MCP/CLI surfaces, testing & engineering. DSA, SQL/tech-stack, and HR questions are covered in separate sheets.
> Interview pattern observed: panel picks the most technical project on your resume and grills it for 20–40 minutes — how it works, why you made each choice, what breaks, and how you'd scale it.

---

## 1. Project Overview & Architecture (Q1–Q15)

**Q1: What is MigratorGen and what problem does it solve?**
A: When a Python library ships a new major version, downstream developers must manually read the changelog and rewrite every affected import and call site. MigratorGen automates this. It consumes a JSON/Markdown changelog (`VersionChangelog` records), parses it into a typed `Rule` model, resolves a migration path from one version to another (upgrade or downgrade), then rewrites user code using LibCST transformers — all behind a transactional engine with checkpoint-based rollback, semantic symbol resolution, validation, and multiple interfaces (CLI, REST API, MCP server, parallel engine).

**Q2: Give me the high-level architecture of the project.**
A: Three layers. (1) Core SDK under `sdk/python/src/migrator_gen/core/` (~15 modules): `changelog_parser.py` turns changelog text into typed rules; `version_resolver.py` builds multi-step upgrade/downgrade paths; `migration_engine.py` is the transactional engine with `FileCheckpoint` rollback and confidence scoring; `transformers.py` + `transformers_advanced.py` hold the LibCST transformers; `validation.py` validates rules and tracks rule dependencies; `symbol_resolver.py` does semantic name analysis; `diff_analyzer.py` auto-generates rules from two code versions; `llm_engine.py` adds LLM suggestions; `parallel_engine.py` processes whole repos. (2) Surface layer: `cli/`, `mcp/` (MCP server), and a `backend/` with FastAPI (`/migrate/code`, `/rules/generate-from-diff`) + Celery/Redis worker + SQLAlchemy async + shared platform packages (auth, cache, metrics, logging). (3) `migrator_generator.py` bakes everything into a standalone, installable `.py` migrator package per library version range.

**Q3: Why did you split the code into core SDK + CLI + MCP + backend?**
A: Separation of concerns and reuse. The core SDK (`migrator_gen`) holds all migration logic as a pure, testable Python package — it has no I/O opinions about API vs CLI vs editor integration. That same SDK is imported by the CLI, used inside the MCP server for code-assistant integration, wrapped by FastAPI for remote/containerised use, and invoked by Celery tasks in the worker for async jobs. One engine, many surfaces.

**Q4: What is the core data flow from changelog to migrated code?**
A: Changelog → `VersionChangelog` (version, release_date, list of `Rule`) via `changelog_parser.py` → optional merge/validation → `VersionResolver` selects a `MigrationPath` with per-step `(from, to)` `MigrationStep`s → `TransactionalMigrationEngine.migrate_code()` runs each rule's LibCST transformer over the source → each application is recorded as a `ChangeRecord` (rule_id, line range, confidence, safety) and the file is checkpointed before write → on any failure the checkpoint restores the original → a `MigrateResponse` (transformed code, changes, rules_applied, average_confidence, was_modified) is returned.

**Q5: How many rule/change types does the system support, and what are they?**
A: The `ChangeType` enum in `constants.py` supports 40+ types. Renames: `rename_function`, `rename_class`, `rename_attribute`, `rename_import`, `rename_module`, `rename_parameter`, `rename_argument`. Signature changes: `add_argument`, `remove_argument`, `change_argument_default`, `change_type_annotation`, `reorder_arguments`. Deprecation/removal: `deprecate_function/class/module/parameter`, `remove_function`, `remove_class`. Moves: `move_to_module`, `move_to_submodule`, `move_class_to_module`. Decorators: `add/remove/change_decorator`. Async: `sync_to_async`, `async_to_sync`. Restructuring: `wrap_in_context_manager`, `wrap_in_sync_context_manager`, `class_split`, `module_split`, `merge_classes`, `merge_modules`, `change_return_type`. Enums & dataclasses: `enum_migration`, `change_enum_base`, `dataclass_field_add/remove/rename/change`, `replace_with_property`.

**Q6: What's the difference between the basic and advanced transformer libraries?**
A: `transformers.py` covers the classic codemod cases — renames (function, class, attribute, import, module), argument add/remove/default changes, move-to-module, replace-call-with-property, add/remove decorators. `transformers_advanced.py` handles structural/behavioral rewrites: `SyncToAsyncTransformer` (adds `asynchronous=` and optionally wraps calls in `Await`), `WrapInContextManagerTransformer`, `ClassSplitTransformer`, `ModuleSplitTransformer` (splits one import into two via `cst.FlattenSentinel`), `ChangeReturnTypeTransformer`, `EnumMigrationTransformer`, and dataclass field transformers. Basic ones override `leave_Name`/`leave_Attribute`; advanced ones usually override `leave_FunctionDef`, `leave_ClassDef`, or `leave_Call`.

**Q7: What tech stack did you choose and why?**
A: Python 3.8+, with `libcst>=1.0.0` as the lossless AST engine and `pydantic>=2.0.0` for all schema/rule models (`BaseModel`, `Field`, validators, `model_config = use_enum_values / populate_by_name`). Dev tooling: pytest (186 test cases — 131 core + 55 shared), ruff for lint, mypy for typing, pre-commit, rich for CLI UX. API extras: FastAPI, uvicorn, prometheus-client. Worker extras: Celery, redis, SQLAlchemy `[asyncio]`, asyncpg. MCP server uses the `mcp` SDK with httpx and tenacity. Everything is declared in `pyproject.toml` and driven by a root `Makefile` (`make test`, `make lint`).

**Q8: Why LibCST over Python's built-in `ast` module?**
A: The built-in `ast` module is lossy — it drops comments, whitespace, and exact formatting and cannot re-serialize faithfully. MigratorGen must be non-destructive: code the transform doesn't touch must stay byte-for-byte identical. LibCST builds a concrete syntax tree that preserves every token and every piece of whitespace/comment, so we can round-trip `code → parse → transform → .code` with zero collateral changes. Regex is out for the same reason — it can't parse nested/balanced constructs like function signatures or call expressions reliably.

**Q9: How does MigratorGen handle both upgrades and downgrades?**
A: `VersionResolver` computes forward and reverse paths. For an upgrade, it walks versions in increasing order, collecting the rules of every intermediate release between source and target. For a downgrade, it collects the same rules in reverse, and the engine reverses `RuleTransformer`s (using rule metadata like `reversible` and the transformer's own `reversible=True` / reverse application logic) so e.g. `rename_function(old→new)` becomes `new→old`. The generated `__main__.py` even implements `_resolve(src, tgt)` that composes version rulesets in the right direction. So a rule set defined once can drive both directions.

**Q10: What surfaces does a user interact with, and what can each do?**
A: Four. (1) CLI (`cli/`): list versions, migrate a file/directory, dry-run preview, diff preview, validate a file, backup `.py.bak` before writing. (2) REST API (`backend/api/src/main.py`): `GET /health`, `POST /migrate/code`, `POST /rules/generate-from-diff`, `POST /rules/generate-from-changelog`, `GET /libraries`. (3) Celery worker: async `migrate_code_task`, `migrate_directory_task`, and a scheduled `cleanup_old_jobs` that deletes stale job rows (done/failed/cancelled, older than 90 days). (4) MCP server (`mcp/`) so an AI assistant can trigger migrations as tools. All four call the same SDK.

**Q11: How is the API server structured?**
A: `backend/api/src/main.py` defines `app = FastAPI(title="MigratorGen API")` with CORS middleware, instantiates a single `MigrationClient(mode="local")` singleton, and exposes typed Pydantic request models (`MigrateCodeRequest` with `source_code`, `rules: list[dict]`, `source_version`, `target_version`, `dry_run`; `GenerateDiffRequest`; `GenerateChangelogRequest`). `server.py` is the full-featured variant; `main.py` is the minimal container-friendly entry point that runs under uvicorn with `workers=4`. Request handlers deserialize rules with `Rule.from_dict`, call the client, and raise `HTTPException(500)` on failure.

**Q12: How does the async worker fit in?**
A: `backend/worker/src/tasks/migration_tasks.py` defines Celery `@shared_task`s using `migrator_gen.MigrationClient` in local mode. `migrate_code_task` has `bind=True, max_retries=3, default_retry_delay=5`, times the run with `time.perf_counter()`, logs structured info (`job_id`, `tenant_id`, `was_modified`, `duration_ms`), and calls `self.retry(exc=exc)` on failure — exponential-ish backoff with capped retries. `migrate_directory_task` walks `rglob("*.py")`, migrates each, aggregates per-file results. `cleanup_old_jobs` runs a Celery beat task that executes an async SQLAlchemy `delete()` against `MigrationJob` after a 90-day cutoff.

**Q13: What does `MigrationClient` abstract away from all surfaces?**
A: It's the public façade (defined under the package root): it wraps `Rule`/`MigrationRule.from_dict`, `migrate_code`, `list_libraries`, `generate_rules_from_diff` (pipes into `diff_analyzer`), and `generate_rules_from_changelog`. Every interface — CLI, API, worker, MCP — calls `MigrationClient`, so consistent semantics (confidence, rules_applied, errors, was_modified) are guaranteed everywhere and adding a kind of migration is a one-place change.

**Q14: How is the whole thing packaged and released?**
A: The SDK is a standard `src/`-layout package (`migrator_gen`) with `pyproject.toml` declaring entry points, extras (`[api]`, `[worker]`, `[mcp]`), and `python_requires=">=3.8"`. The backend is containerised with Dockerfiles (separate ones for `api/` and `worker/`). Separately, `migrator_generator.py` *generates* a brand-new standalone distributable package — `setup.py` + `__main__.py` + `__init__.py` + `README.md` + `migration_rules.json` — whose only runtime dependency is `libcst`, so end users can `pip install -e .` and run `python -m mylib_migrator migrate --from 1.0.0 --to 2.0.0 ./proj/`.

**Q15: What makes this "AI" rather than just a codemod framework?**
A: Two AI pieces. (1) `diff_analyzer.py` auto-generates migration rules by diffing two versions of a codebase (`ASTExtractor` parses each side with LibCST and detects renamed APIs, removed args, moved imports). (2) `llm_engine.py` converts natural-language change descriptions or error messages into structured JSON rules (`suggest_from_error`, `generate_from_description`, `explain_breaking_changes`), with a deterministic regex fallback when no provider is configured. The core rewriting stays rule-driven and deterministic; the LLM only handles where understanding is needed.

---

## 2. Changelog Parsing & Rule Data Model (Q16–Q30)

**Q16: Walk me through how a changelog becomes typed rules.**
A: `changelog_parser.py` reads a `VersionChangelog` (version, optional release date, list of `Rule`) — typically from a JSON/changelog file — and exports `MigrationRule` objects. Each `MigrationRule` is Pydantic v2 validated with `extra="forbid"` so unknown fields are rejected and malformed rules surface as validation errors instead of failing mid-migration. `models.py` defines the full canonical schema: `Rule`, `VersionChangelog`, `MigrationFile` (library + schema_version + versions), response models (`MigrateResponse`, `DiffPreview`, `ValidationReport`, `MigrationReport`), and the async `MigrationJob`/`MigrationStatus` state machine.

**Q17: What fields does a `Rule` have? Describe the schema.**
A: Core identity: `id`, `change_type` (the `ChangeType` enum), `version_introduced` (regex `^[\w.]+$`), `description`. Type-specific fields, all optional: `old_name`/`new_name`, `function_name`, `argument_name`/`new_argument_name`, `default_value`/`new_argument_value`, `new_order`, `old_module`/`new_module`/`source_module`/`target_module`, `decorator_name`, `replacement`. Safety/metadata: `safety` (safe|review_required|risky), `confidence_hint` (high|medium|low), `when` (a `RuleWhenCondition`), `priority`, `depends_on`, `conflicts_with`, `reversible`, `idempotent_safe`. `model_config = {"use_enum_values": True, "populate_by_name": True}`; `to_dict()` dumps with `exclude_none=True`.

**Q18: What are `RuleWhenCondition` and how do they work?**
A: `RuleWhenCondition` is a nested model that makes rules context-gated: `import_context` (list of import paths present), `imported_from`, `inside_class`, `inside_function`, `has_decorator`, `has_annotation`, `module_pattern`. Before a rule is applied, the engine checks these against the file's imports and enclosing scope; if a condition isn't satisfied the rule is skipped for that file rather than blindly applied. This is what prevents a rename rule from touching a file that never imports the affected module — a correctness feature for big repos.

**Q19: How does the parser handle invalid or unknown rule fields?**
A: Pydantic's default strictness — `Rule`/`MigrationRule` use `extra="forbid"` (or equivalent) so an unknown key raises a `ValidationError` at load time; type coercion is governed by declared types (e.g. `priority: int = Field(ge=0)`, `safety` pattern `^(safe|review_required|risky)$`). The validation module wraps these into a `ValidationReport` with `errors`/`warnings`/`info` dicts and severity levels, so a broken rule is reported clearly up front instead of blowing up in the middle of a repo-wide migration.

**Q20: What is the `MigrationFile` wrapper?**
A: It's the schema for a complete rules file: `library` name, `schema_version` (default "1.0"), and a list of `VersionChangelog`. Each changelog holds one `version` plus its `rules`. This is the container that `migration-schema.json` describes and that `MigrationClient`/`validate_rules_from_file` reads, so a whole library's migration catalog lives in one document.

**Q21: Difference between `Rule` (models.py) and `MigrationRule` (changelog_parser.py)?**
A: They're the same concept at different dependency layers. `models.py` defines the canonical Pydantic `Rule` used across the package; `changelog_parser.py` exposes a `MigrationRule` (also Pydantic, with the `when` conditions and validators) that the parser and `get_transformer` factory consume. They serialize with `to_dict()`/`from_dict()` in both directions, and public surfaces like the API reconstruct rules via `Rule.from_dict(...)` before dispatch — so a JSON rule dict is interchangeable across layers.

**Q22: Why is type-safety so important in a migration rule model?**
A: Because a migration rule drives an irreversible-ish edit to user source. A typo like `safety="rireky"` or `version_introduced="2.0"` (invalid charset) must fail at parse time, not corrupt a codebase. Pydantic's `Pattern`-style constraints (`safety`/`confidence_hint` regexes, `version_introduced` regex, `priority >= 0`) plus enum coercion catch these cheaply and deterministically — the model *is* the contract between the changelog author and the transformer.

**Q23: How are version and safety metadata used at runtime?**
A: `version_introduced` tells the resolver which version a rule belongs to, so path computation only selects the right slice. `safety` feeds the engine's `SafetyLevel` (SAFE / REVIEW_REQUIRED / RISKY): risky rules can be gated behind `interactive_approval`, and every `ChangeRecord` carries the safety level back to the report so a user can tell exactly which edits are risky. `confidence_hint` seeds the engine's per-change confidence, which is aggregated into `average_confidence` and surfaced in `ChangeRecord`/`MigrateResponse`.

**Q24: What does the engine return per rule and overall?**
A: Per rule, `RuleResultSummary`: `rule_id`, `rule_description`, `success`, `confidence`, `safety`, `changes_made`, `errors`, and `skipped_reason` (nil when a `when` condition failed). Per run, `MigrateResponse`: `original_code`, `transformed_code`, `changes` (string log), `rules_applied`, `average_confidence`, `was_modified`, `errors`, `rule_results`, and `duration_ms`. `RuleApplicationResult`/`TransformResult` carry the intermediate per-rule outcomes from the engine to the report builder.

**Q25: How do you represent an intermediate version step?**
A: `models.py` has `MigrationStep(source, target, rules)` and `ResolvedPath(source_version, target_version, steps)` with convenience properties `rule_count` and `all_rules`. `version_resolver.py`'s `MigrationPath` mirrors this for the engine: `source_version`, `target_version`, `steps` (list of `(from, to, rules)`), and `is_upgrade`. This lets the engine apply rules release-by-release, which matters when a symbol was renamed in v2 and renamed again in v3 — you must not collapse the two hops into one.

**Q26: What pre-checks does the system run before migrating?**
A: Rule validation (`validate_rules_from_file`, JSON and YAML) checks schema correctness and cross-rule constraints; `RuleDependencyGraph` verifies `depends_on`/`conflicts_with` ordering; `IdempotencyChecker.compute_fingerprint(rules)` checks that applying a rule twice doesn't compound a change. The generated `__main__.py` also `_validate_rules()` at startup — it scans every version's rules for the mandatory keys `id`, `change_type`, `version_introduced`, `description` and `sys.exit(1)` if any are missing.

**Q27: How does `version_resolver` match or fuzzy-match versions?**
A: The resolver normalizes versions with `_version_key` (turning `"2.10.0"` into a comparable tuple like `(2,10,0)`) and handles `"latest"` as a target alias (resolved to the highest known version) and `"0.0.0"` as a base for "everything so far". Comparison is numeric, not lexicographic, so `2.9` < `2.10` correctly. If a requested version isn't known exactly, the resolver falls back to the nearest known version within the path.

**Q28: What is `MigrationStatus` and `MigrationJob` for?**
A: The async/backend path needs a durable job lifecycle. `MigrationStatus` enumerates `pending, running, completed, failed, cancelled, rolled_back`. `MigrationJob` (Pydantic) stores `job_id`, status, `source_version`, `target_version`, timestamps (`created_at`, `completed_at`), `error_message`, optional `result`, `rule_count`, `files_processed`. The worker persists/updates these (SQLAlchemy `MigrationJob` ORM model in `shared/database.py`) and Celery beat's `cleanup_old_jobs` prunes them after 90 days. `HealthStatus` feeds `/health`.

**Q29: How do you serialize rules for transport and for generated packages?**
A: `Rule.to_dict()` (`model_dump(exclude_none=True)`) produces plain JSON-safe dicts; `Rule.from_dict()` deserializes. The generated package's `_build_main_module` goes further: it double-encodes the migration data (`json.dumps(json.dumps(migration_data))`) and embeds it as `_MIGRATION_JSON` in the generated source, then `MIGRATION_DATA = json.loads(_MIGRATION_JSON)` at runtime — this avoids JSON `null/true/false` clashing with Python syntax and dodges `.format()` conflicts with f-strings in the generated code.

**Q30: Why `exclude_none=True` in `to_dict`?**
A: So each rule only carries the fields its `change_type` actually needs — a `rename_function` rule ships `old_name`/`new_name` but not `decorator_name`/`argument_name`. That keeps rules compact, transport lightweight, and matches expressed intent instead of a bloated 20-field object. Consumers (CLI, API, generated `__main__.py`) can safely read fields by `get` and treat missing = unused.

---

## 3. Version Resolution & Migration Paths (Q31–Q40)

**Q31: Explain the `VersionResolver` algorithm for upgrades.**
A: Given `source_version` and `target_version`, the resolver loads the ordered list of known versions, filters to versions strictly greater than source and less than or equal to target, and builds one `MigrationStep(from, to, rules)` per release boundary, chaining an intermediate release's rules exactly once. If a requested version isn't in the catalog, it snaps to the nearest known version (with "0.0.0" as the lowest sentinel). The whole thing is exposed as a `MigrationPath` with `is_upgrade=True` and, for downgrades, the roles invert.

**Q32: And for downgrades — how is the path computed?**
A: Downgrade is the mirror image: iterate the known versions in reverse, pick those strictly above the target and ≤ the source, and collect their rules in reverse order so the path applies the newest reverse-transforms first. Combined with per-rule `reversible` flags (a `main.py`-style `_resolve` loops `reversed(vs)` for downgrade), MigratorGen can `--to 1.0.0` from `3.0.0` and undo effects in the reverse release order.

**Q33: What is the point of stepping through intermediate versions instead of applying all rules at once?**
A: Sequential steps matter when later releases contradict earlier ones — a symbol renamed in v2.0 and renamed again in v2.1. Applying v2.0→2.1 rules directly to source that's still on v1 can produce the wrong intermediate name or a no-op. Stepping eats exactly one transition per version, so the source always reaches the destination the same way a user who upgraded incrementally would have. The demo (`examples/demo_all_features.py`) exercises a full `1.0 → latest` path this way.

**Q34: How is "latest" resolved, and why does it matter for correctness?**
A: `target_version="latest"` is a soft alias resolved at path-build time to the newest version in the catalog (`vs[-1]` after sorting by `_version_key`). It matters because a rules file may be edited later (new release appended), and materialising `latest` at run time means the CLI/API always migrates to the real newest release without hard-coding a version string in the request.

**Q35: What happens if source_version == target_version?**
A: The path is empty — zero steps, zero rules, so `migrate_code` returns `was_modified=False` with an empty change list. The engine short-circuits: no transformers run, no checkpoints are written, and the report shows 0 changes. This prevents an accidental no-op rewrite from reserializing (and thus touching) a file for no reason.

**Q36: How do you sort versions correctly?**
A: Numeric tuple comparison, not strings. `_version_key` splits on dots and casts numeric parts to int (`2.10.0 → (2,10,0)`), so ordering is `1.9 < 1.10 < 2.0`. The generated `__main__.py` `_vk()` does the same with `re.findall(r'\d+', ...)`. Lexicographic sorting would rank `2.10` below `2.9`, which would silently produce a wrong migration path.

**Q37: What role do `priority`, `depends_on`, and `conflicts_with` play in path execution?**
A: `priority` (int ≥ 0) orders rule execution within a step when the ruleset isn't already ordered, e.g. high-priority structural rules before low-priority cosmetic ones. `depends_on`/`conflicts_with` (rule IDs) feed `RuleDependencyGraph`: a rule that depends on another runs only after it (or reports a validation error if the dependency is missing); two conflicting rules can't both apply to the same code. This prevents rule interactions — like renaming `foo` and also adding argument `foo` — from producing garbage.

**Q38: How does per-file context influence path application?**
A: The engine is path-aware but file-gated: the full `MigrationPath` is resolved once, then each file independently runs the applicable rules. `RuleWhenCondition`s (`module_pattern`, `imported_from`, `import_context`) and `symbol_resolver` pre-checks decide per file whether a rule applies, so a file that doesn't import the library genuinely isn't touched even though the path technically includes every rule. `exclude_patterns` (e.g. `**/test_*.py`, `**/__pycache__/**`) further restrict scope at the directory level.

**Q39: What failures can the resolver produce, and how are they surfaced?**
A: Unknown source version, unsupported target (below zero / unknown), an empty catalog, or a path whose steps reference missing rule files. Failures propagate as clear errors into `MigrateResponse.errors` or the API's `HTTPException(500)`; rule *validation* errors go through `ValidationReport`. The design goal is a manifest of "why", not a bare traceback, because users run this on real repos.

**Q40: How did you test version resolution?**
A: Dedicated unit tests in the 131 core tests: build a fake catalog `{1.0:[r1], 1.1:[r2], 2.0:[r3]}` and assert upgrade `1.0→2.0` yields `[r1,r2,r3]` in that order, downgrade `2.0→1.0` yields the reverse, `latest` resolves to `2.0`, and `0.0.0` base includes everything. Plus property-style checks that upgrading then downgrading on reversible rules returns the original source.

---

## 4. LibCST Transformers (Q41–Q55)

**Q41: How does a LibCST transformer work under the hood?**
A: A `cst.CSTTransformer` is a visitor that walks the concrete syntax tree. You override `leave_<NodeType>` methods — called with `(original_node, updated_node)` — mutate the `updated_node` via `with_changes(...)` (LibCST nodes are immutable), and return the new node. For `RenameFunctionTransformer`, `leave_Name` checks `updated_node.value == old_name` and returns `updated_node.with_changes(value=new_name)`; `leave_Attribute` handles dotted access via `_get_call_name`. Because nodes are immutable and position/whitespace-aware, unchanged segments serialize byte-identically.

**Q42: What's the difference between `leave_Name` and `leave_Attribute` handling for renames?**
A: `leave_Name` catches *references* — a bare `Name` node whose `.value` equals `old_name` (local usage). `leave_Attribute` catches *attribute chains* like `obj.method()` where the attribute part (`attr.value`) matches. The two must be handled separately because in LibCST `obj.method` is `Attribute(value=Name('obj'), attr=Name('method'))` — a rename of `method` changes the `attr`, while `obj` itself is a `Name` deeper in the tree. The generated `__main__.py` also implements `_dn()` recursively to reconstruct a dotted name from a node.

**Q43: How do you rename imports without breaking `from` vs `import` forms?**
A: Two visit methods in the import renamer: `leave_ImportFrom` handles `from old.mod import name` — it compares the module's dotted name to `old_module`, rewrites the module via `cst.Attribute` construction (`_make_dotted_name`), and rewrites aliased names, being careful to leave `ImportStar` untouched. `leave_Import` handles `import old.mod as x` by matching `alias.name` and rebuilding names. In the generated package the `RI` transformer iterates `u.names` and rebuilds only when it actually changed a name, returning the node untouched otherwise.

**Q44: How does argument addition/removal keep the source valid?**
A: For adding: in `leave_Call`, if a `keyword` argument with that name already exists, return unchanged (idempotent); otherwise build `cst.Arg(keyword=Name(arg), value=cst.parse_expression(default), equal=AssignEqual(...))`, handle the trailing comma with `cst.MaybeSentinel.DEFAULT` on the previous arg, and append. For removing: filter args by keyword name and re-fix the trailing comma. `cst.MaybeSentinel.DEFAULT` is the key — it lets LibCST decide whether a comma is needed, so `f(a,)` and `f(a)` both stay valid.

**Q45: How do advanced transformers change function semantics, e.g. sync→async?**
A: `SyncToAsyncTransformer` overrides `leave_FunctionDef`: if the rule targets this function and `original_node.asynchronous is None`, it pushes `asynchronous=cst.Asynchronous()` to make `def` → `async def`. It also overrides `leave_Call` and, when `rule.extra.get('wrap_await')` is set and the callee matches, wraps the call in `cst.Await` — but only if it isn't already an `Await`. The reverse (`async_to_sync`) removes `asynchronous` and unwraps awaits. This is a *behavioral* change (the return is now a coroutine), so the rule carries `safety: review_required/risky`.

**Q46: How does `ModuleSplitTransformer` split one import line into two?**
A: `leave_ImportFrom` matches `source_module`, then partitions the alias list: symbols in `extract_symbols` get a new `ImportFrom` pointing at `target_module`; the rest stay in the original. If both remain, it returns `cst.FlattenSentinel([remaining_import, new_import])` — a LibCST mechanism that tells the parent to emit multiple statements in place of one. `ClassSplitTransformer` similarly *partitions `FunctionDef` children* of a `ClassDef`, removing extracted methods from the original body.

**Q47: Fit the `leave_Call` machinery: how do you tell `foo.bar()` from `bar()`?**
A: `_get_call_name(func_node)` (and `_cn` in the generated package) checks `isinstance(func, cst.Name)` → return `.value` (bare call), `isinstance(func, cst.Attribute)` → return the `.attr.value` (method call). This lets `replace_with_property` specifically target method-style calls with no args (renaming `get_x()` → `.x`) via `u.func.with_changes(attr=Name('x'))`, and lets argument rules match the right callee without false-positiving on attribute chains.

**Q48: How do decorator add/remove transformers work?**
A: `leave_FunctionDef` by function name; for add, it guards against duplicates by scanning existing `decorators` for the same `Name`, then appends `cst.Decorator(decorator=cst.Name(dn), leading_lines=[])`. For remove, it filters out decorators whose base name matches and, if any were removed, returns `with_changes(decorators=remaining)`. `WrapInContextManagerTransformer` is a generalization: it builds the decorator expression (handling dotted names like `contextlib.contextmanager`) and appends it, effectively turning a body into a context-managed generator-style function.

**Q49: How does `ChangeReturnTypeTransformer` update type annotations safely?**
A: `leave_FunctionDef` matches `rule.function_name`, reads `rule.extra['new_return_type']`, wraps it in `cst.Annotation(annotation=cst.parse_expression(new_return_type))`, and returns `with_changes(returns=annotation)`. The whole parse is wrapped in try/except so an unparseable annotation string (e.g. `"List["`) is left untouched rather than crashing. The rule is `review_required` because changing a return annotation can break static type checkers even when runtime behaves the same.

**Q50: What makes transformers idempotent, and why do you track it explicitly?**
A: Each transformer guards against re-applying its own edit: rename checks current value ≠ new value; add_argument checks the keyword isn't already present; add_decorator scans existing decorators; `leave_Attribute` for `replace_with_property` requires arguments to be empty. `Rule.idempotent_safe` records this assumption, and `IdempotencyChecker.compute_fingerprint(rules)` computes a hash the engine uses to detect "already migrated" files via the AST/disk cache — so re-running a migration on an already-migrated repo is a no-op instead of double-mutating code.

**Q51: How is a rule mapped to its transformer?**
A: `get_transformer(rule)` (in `transformers.py`) is a factory keyed by `rule.change_type` (the Changelog parser's enum) returning the right transformer class: basic types (rename*, add/remove argument, move_to_module, replace_with_property, decorators) from `transformers.py`; structural types (sync_to_async, class_split, module_split, change_return_type, enum/dataclass) from `transformers_advanced.py`. Unknown `change_type`s either raise a clear validation error or are skipped with a recorded warning — the engine never silently "does nothing" on a rule it doesn't understand.

**Q52: What problem does the `cst.parse_expression` usage solve?**
A: Defaults, annotations, and replacement values arrive as strings (`default_value="None"`, `new_return_type="dict[str, int]"`). `cst.parse_expression` turns those strings into real CST subtrees with correct whitespace/position, so they slot cleanly into `Arg(...)`/`Annotation(...)` nodes. This avoids hand-building nodes char by char and keeps the emitted code parseable — and it's what the generated `__main__.py` does (`cst.parse_expression(dv)` inside `leave_Call`) for `add_argument`.

**Q53: How does a transformer record its own changes?**
A: Every transformer keeps a `self.changes_made: list[str]` (advanced ones call `_record(msg)`; basic ones `self.ch.append(...)`). After `tree.visit(transformer)`, the engine reads `transformer.changes_made` into `ChangeRecord`s (rule_id, human-readable message, line_range where determinable, safety + confidence from the rule), and those strings end up in `MigrateResponse.changes` and the CLI's `    + Renamed foo -> bar` output. This gives an audit trail of exactly what each rule did to each file.

**Q54: Why are transformers kept pure/LibCST-only, with safety metadata separate?**
A: Separation of concerns: a transformer answers *how* to edit the tree; the engine and rule carry *whether it's safe* (`safety`), *how confident* we are (`confidence_hint`), and whether it's `reversible`/`idempotent_safe`. This lets the same transformer be used in auto mode (skip risky), interactive mode (pause for approval), and dry-run mode (compute the diff) without the transformer knowing about approval policies or reporting layers.

**Q55: What edge cases did you handle in transformer design?**
A: (1) `ImportStar` must not be rewritten name-by-name. (2) Trailing commas after arg removal — handled with `MaybeSentinel.DEFAULT`. (3) Calls that already have the target keyword argument. (4) Nested same-name attributes (`a.b.b` vs `a.b.c`) — checked via full dotted-name reconstruction, not `attr.value` alone. (5) Unparseable replacement strings — try/except around `parse_expression`. (6) Catching the return of `leave_ImportFrom` that must return a `FlattenSentinel` (a node *or* a special sentinel), which the LibCST visitor protocol allows only in specific methods.

---

## 5. Transactional Engine, Rollback & Safety (Q56–Q70)

**Q56: What does "transactional" mean in this engine?**
A: Each file migration is treated like a database transaction: snapshot the original source, apply the rules against a parsed CST, and only when the whole file's transforms succeed do we commit the change to disk. Any error during transformation or rule application causes a rollback to the saved original — so a partially-migrated file is never left on disk. `TransactionalMigrationEngine(transactional=False, ...)` (used per-file in parallel workers) runs non-transactionally per file, but each file's result is still atomic.

**Q57: What is a `FileCheckpoint`?**
A: `FileCheckpoint` (in `migration_engine.py`) captures `original_content`, `modified_content`, a `rule_fingerprint` (hash of the applied rules) and a `timestamp` for one file. The engine records a checkpoint before writing; if anything fails mid-file, the original content is restored from the checkpoint. It also doubles as a cache key — the `rule_fingerprint` + file content hash tells you whether a file was already migrated by exactly these rules.

**Q58: Describe the `ChangeRecord` structure.**
A: `ChangeRecord` is the per-edit log: `rule_id`, a human-readable `description`, optional `line_range` (start/end line numbers in the source — obtainable from CST position info), `confidence` (0.0–1.0, computed from the rule's `confidence_hint` and transformer outcome), and `safety` (from `SafetyLevel`). The engine aggregates all `ChangeRecord`s for a file/run into `RuleResultSummary` and eventually `MigrateResponse`, so the report is a structured, auditable list of every edit with its risk profile.

**Q59: What is interactive approval, and how does it interact with safety levels?**
A: With `interactive_approval=True`, the engine halts before applying rules whose `SafetyLevel` is `RISKY` (or `REVIEW_REQUIRED` when configured) and asks for explicit go/no-go. SAFE rules apply automatically. In headless/parallel modes approval is off, so risky rules are *skipped with a recorded reason* unless the caller explicitly disables gating — the engine never applies a risky transform silently in an automated run. This is the "don't shoot yourself in the foot" control valve.

**Q60: How is confidence computed and aggregated?**
A: Each rule carries `confidence_hint` (high/medium/low, mapped to e.g. 0.9/0.7/0.5); explicit user rules get high confidence, LLM-generated rules get the LLM's estimate (SuggestionConfidence HIGH/MEDIUM/LOW), and heuristic/diff-derived rules get moderate values. Per-file average feeds `MigrateResponse.average_confidence`; a repo report averages across all changed files. Low-confidence results are flagged in the report so a human reviews them — mirroring how you'd surface model uncertainty in any ML system.

**Q61: What happens if the transformed code fails to re-parse?**
A: The engine validates the transformed output by re-parsing with LibCST (and the generated package's `validate` command / API checks `cst.parse_module`). If re-parsing fails, the transformer is considered failed for that file, the change is rolled back from the checkpoint, and `errors` gets the parse failure — the original file remains untouched. Since a Codemod must never emit invalid Python, this is a hard gate, not a warning.

**Q62: How does the engine decide `was_modified`?**
A: `was_modified = transformed_code != original_code` — a structural comparison of the serialized trees, not "did a rule fire". This means a rule that was a no-op (e.g. a rename that found no occurrences, or a guard that skipped the call) does not mark the file as modified, and dry-runs use the same boolean so "files would have been modified" is honest.

**Q63: How do you handle a rule that errors on one file but the rest of the repo is fine?**
A: Per-file isolation. Transforms are applied inside try/except at the file/worker level: a failure produces an entry like `{"was_modified": False, "changes": ["Error: ..."]}` and is counted in `files_failed`, while other files proceed independently. In the parallel engine each file runs in its own process (`_migrate_file_worker` returns `(path, was_modified, changes, confidence)`), so a crash or a bad rule on one file can't take down a whole-repo run.

**Q64: What modes does the engine support, and how are they wired into CLI flags?**
A: `dry_run`: compute the transformed code and diff, write nothing. `preview`: show a unified diff per file (`difflib.unified_diff`) from the generated package's `preview_diff`. `backup`/`no_backup`: write `.py.bak` before modifying (default on, since migration is meant to be reversible). `interactive_approval`: pause on risky edits. `transactional`: per-file rollback on/off. Directory runs can pass `exclude_patterns`. These combine: `--dry-run --preview` gives a no-risk audit of an entire repo.

**Q65: How does the engine log/report rollbacks?**
A: `MigrationReport` carries a `transactions_rolled_back` counter, and its `summary()` prints `"Rollbacks: N"` when non-zero. `MigrationResponse.errors` collects the reasons. In the generated package (`__main__.py`), backups + only writing when `mod = nc != src` provide file-level undo even without the engine's transactional machinery — belt and suspenders for end users.

**Q66: What is `SafetyLevel` and how is it assigned to rules?**
A: `SafetyLevel` is SAFE / REVIEW_REQUIRED / RISKY. Assignments follow the *blast radius*: pure local renames of private-ish names are SAFE; renames that cross module boundaries or change signatures (`remove_argument`, `change_return_type`) are REVIEW_REQUIRED; behavioral transforms (`sync_to_async` — return type changes from object to coroutine — or `wrap_in_context_manager`) are RISKY. The rule author sets `safety` in the changelog; the LLM prompt also instructs generation with these exact three values.

**Q67: What's the difference between `safety` and `confidence`?**
A: `safety` is a categorical *risk* estimate (what breaks if this is wrong — compile? runtime? importing module absent?), set by the rule author; `confidence` is a numeric *certainty* that the rule should apply at this call site (how sure we are `foo` here is *the* `foo`). A high-confidence unsafe change should still be reviewed; a low-confidence safe change is auto-applied but flagged. The report exposes both per `ChangeRecord`, and approval policy keys off `safety`, while confidence ranking drives review triage.

**Q68: Can you give a concrete failure-and-recovery scenario?**
A: Repo has 40 files using `pkg.foo()`. Rule `remove_argument(bar)` targets a function that, in one file, is called with `bar=` positionally. The transformer removes it, outputs invalid call `f(x, y=)`. Re-parse fails → that file's checkpoint restores the original → file counted in `files_failed` with the parse error → the other 39 files commit fine → report shows `Rollbacks: 1` and the failing reason. The user fixes the rule, re-runs, and only the one file re-migrates because the rest are cache/checkpoint hits.

**Q69: How does checkpoint data avoid re-doing completed work?**
A: `FileCheckpoint.rule_fingerprint` (hash of the exact rules applied) is stored with the file's migrated content. On a new run, the engine hashes the rules and the current file content; if they match a checkpoint whose fingerprint equals the incoming rule set, the file is treated as already migrated and skipped (`IdempotencyChecker` + ASTCache/DiskCache short-circuit). This makes re-running migrations after a partial failure cheap and correct.

**Q70: Why is a "diff-preview gated" workflow important for production use?**
A: Because migrations edit a developer's source with irreversible consequences if wrong. The audit workflow — dry-run → unified diff review → real run with `.bak` backups → per-file rollback on failure → structured report of changes/confidence/safety → low-confidence and risky flagged — mirrors how infra teams deploy schema changes: preview, approve, apply, observe, roll back. That discipline is what makes a code-rewriting tool safe enough for CI.

---

## 6. Validation, Idempotency & Dependencies (Q71–Q80)

**Q71: What does `validate_rules_from_file` do, and what formats does it accept?**
A: It loads a rules document (JSON **and** YAML) and returns a `ValidationReport` with `valid`, `errors`, `warnings`, and `info` — each entry a dict with severity + message. It checks per-rule schema (required `id`/`change_type`/`version_introduced`/`description`, enum & regex constraints via Pydantic) and cross-rule invariants: unknown `change_type`, missing `depends_on` targets, conflicting `conflicts_with`, unsafe `safety` strings. Clean validation is a gate before any migration run; the API/CLI reject bad rule files up front.

**Q72: What is the `RuleValidator`?**
A: The class that performs the per-rule semantic checks beyond Pydantic's field constraints — e.g. that a `rename_function` rule declares both `old_name` and `new_name`, that `move_to_module` has `source_module`/`target_module`, and that a `deprecate_function` has a `replacement`. These are *type-specific* requirements that the generic schema can't express, so they live in dedicated validation logic and funnel failures into the report's `errors` with actionable messages.

**Q73: How does `RuleDependencyGraph` ensure correct rule ordering?**
A: It builds a DAG from `depends_on` edges (rule R of change_type X depends on rule S = the change that must happen first) and rejects cycles/missing nodes at validation time. During path execution, the engine topologically orders rules within a step so dependencies apply before dependents. `conflicts_with` edges mark incompatible pairs — validation rejects a catalog that would apply both to the same code. This is the "query planner" of the migration system.

**Q74: What is idempotency analysis, concretely?**
A: `IdempotencyChecker.compute_fingerprint(rules)` produces a stable hash identifying the *set* of transformations. The engine then answers: "given this exact rule set, has this file already been processed?" by comparing fingerprints. Idempotency *per rule* is checked via the transformer guards (no double-rename, no duplicate keyword arg, no duplicate decorator) — so even if caching is disabled, applying a rule twice yields the same output. Together: re-runs are safe and cheap.

**Q75: Why does a `FileCheckpoint` store `rule_fingerprint`?**
A: Because "has this file been migrated?" is meaningless without saying *by which rules*. The fingerprint ties a checkpoint to the exact rule set; a later run with a different (even superset) rule set must not be skipped just because the file content hash matches. It's the difference between a stale cache hit and a correct no-op. The DiskCache does the same with `(code_hash, rules_hash)` as its lookup key.

**Q76: How do you validate in the generated standalone package?**
A: Its `validate` CLI subcommand parses a single file with `cst.parse_module` and prints `OK:` or exits `1` with the failure. Before that, `_validate_rules()` scans every embedded version's rules for the mandatory keys and hard-exits on the first invalid rule. So even the mini version — with no Pydantic at runtime — enforces schema at boot.

**Q77: How do validation results surface to a user?**
A: `ValidationReport` exposes `error_count`/`warning_count`/`info_count` properties; the CLI prints human-readable failures; the API can return `ValidationReport` for `rules/generate-from-changelog` and migration validation; library consumers can short-circuit on `report.valid`. The goal: fail loudly, early, and with actionable messages.

**Q78: What cross-rule conflicts did you model, and why do they matter?**
A: `depends_on` (ordering constraints), `conflicts_with` (mutually exclusive rules — e.g. `rename_function` and `remove_function` on the same symbol). These matter because changelogs are hand-written and can *assert* contradictory changes for a release; a graph check surfaces "rules X and Y target the same old name and cannot both apply" at authoring time instead of producing broken code mid-run.

**Q79: How is YAML support implemented given the schema is Pydantic?**
A: The validation module detects the file suffix/format and parses YAML into the same dict structure the JSON path uses, then feeds identical Pydantic `Rule.from_dict`-style construction. Because the rule model is language-agnostic dicts, YAML gives changelog authors comments and readability while sharing the exact same validation as JSON `migration-schema.json`.

**Q80: What tests cover validation and idempotency?**
A: In the 131 core tests: valid/invalid rule fixtures asserting `ValidationReport` counts; dependency-graph cycle detection; `depends_on` ordering in resolved paths; double-application tests asserting output unchanged after a second pass; checkpoint fingerprint tests (same content + different rules = not a hit). Combined with the 55 shared-package tests (e.g. async DB failures, middleware), the suite gives ~100 per-feature assertions you can cite.

---

## 7. Semantic Symbol Resolution (Q81–Q88)

**Q81: What is `symbol_resolver.py` and why is it needed on top of transformers?**
A: A transformer is textual/CST-structural: it renames a `Name` if the *string* matches. It can't tell whether `foo` in `from x import foo` is the same `foo` as `self.foo()` or a local variable `foo`. `symbol_resolver` adds *semantics* — it resolves what each identifier actually refers to (which module/class/scope defines it) so rules fire only on references to the intended symbol, not coincidental name collisions. That's the difference between a grep-based codemod and a correct one.

**Q82: How do you resolve symbols with LibCST metadata?**
A: `parse_module` is wrapped in `MetadataWrapper` and calls `wrapper.resolve(node)` (or `MetadataWrapper(cst.parse_module(src))` + `WrapMetadataVisitor`) with providers: `ScopeProvider` (scope/assignment hierarchy), `QualifiedNameProvider`, and `FullyQualifiedNameProvider` (module-qualified names like `pkg.mod.Class.method`). LibCST builds these lazily from a full scope analysis, so a `Name` node's qualified name tells us the symbol's actual origin.

**Q83: What is `ImportGraph`, and what does it add?**
A: `ImportGraph` is a representation of the file's import structure (module → imported names, aliases) constructed during the analysis pass. The resolver uses it to answer questions like "is `np` imported from numpy?", "does this module import `pkg.old`?", and "is name `X` aliased?" — same data as a symbol table but import-centric. `RuleWhenCondition.import_context`/`imported_from` are evaluated against this graph, so rules can be scoped: *only if the file imports module M*.

**Q84: What is `ResolutionContext`?**
A: A data object passed through the analysis — the file's module name/path, the import graph, the current scope, and configuration (e.g. whether to consider the standard library). Transformers consult it (`SymbolResolver.resolve(name, context)`) to decide whether a `Name` node resolves to a rule's `old_name`. It keeps scope/inheritance context available to any component rather than re-deriving it per node.

**Q85: What is `SymbolKind`, and why do renames care about it?**
A: `SymbolKind` enumerates what a name denotes: function, class, method, attribute, module, parameter, variable. `rename_class` rules must only match class references — a function named `Foo` isn't the class `Foo`. The resolver annotates each resolved symbol with its kind so transformers (or a pre-filter pass) skip wrong-kind matches. This is the same reason compile-time renames in IDEs ask "did you mean the method or the variable?"

**Q86: How does symbol resolution interact with the transactional engine?**
A: The engine runs a resolution pass before transforms (feeding `when` conditions and per-file applicability) and pipes resolved references into transformers as context. If resolution *fails* for a rule's target (symbol not found in file's graph), the rule is recorded as skipped with a reason — same position as a failed `when` condition — instead of blindly applying a string-rename that could corrupt unrelated code.

**Q87: What's the trade-off vs. pure static analysis like pyright/mypy grammars?**
A: LibCST scope analysis is a correct, self-contained semantic layer without type inference: it resolves assignments, imports, and references but doesn't know variable *types*. That's precisely the right granularity for codemods — we need provenance of names, not type checking. Adding a full type checker would slow migrations massively and mixed-typed code would block half the rules; resolver skip-with-reason is a graceful degradation.

**Q88: Give an example where the resolver prevents a bug.**
A: A library renames class `Session` → `HTTPClient` in `client.py`. A user has `from myserver import Session` (their *own* token-session class) in `auth.py`. A string rename would corrupt `auth.py`'s import. The resolver sees `myserver.Session` resolves to a different fully-qualified name than `client.Session`, marks the rule as not applicable to this file (skipped, recorded), and `auth.py` stays untouched while real `client.Session` references are renamed in every file that resolves to it.

---

## 8. Parallel Engine & Performance (Q89–Q93)

**Q89: How does `ParallelMigrationEngine` scale a migration across a whole repo?**
A: `migrate_directory` globs `**/*.py` (minus `exclude_patterns`, defaulting to `**/test_*.py` and `**/__pycache__/**`), materialises a list of `(file, rules_json, dry_run)` tuples, and submits them to a `ProcessPoolExecutor` with `max_workers = cpu_count - 1`. Each file runs `_migrate_file_worker` in its own process (top-level for pickling); results stream back via `as_completed` and aggregate into a `ParallelMigrationReport` (files_processed/modified/failed, total_changes, per-file results). `max_workers=1` falls back to serial in-process execution.

**Q90: What caching does the parallel engine use, and how are caches keyed?**
A: Two-tier. `ASTCache` (in-memory, LRU `max_size=100`) keys parsed `cst.Module` by an md5 hash of the code — repeated migrations/retries skip re-parsing. `DiskCache` (under `tempfile.gettempdir()/migrator_gen_cache`) persists results keyed by `(code_hash, rules_hash)` and only returns a hit when `data['rules_hash'] == rules_hash` — so cache validity is tied to the exact rule set, not just file content. `invalidate(code_hash)` and `clear()` give control on rule set changes.

**Q91: Why multiprocessing instead of threads or asyncio for parallel files?**
A: The heavy work is CPU-bound LibCST parsing/visiting, which the GIL would make threads useless for; multiprocessing gives true parallelism across cores and isolates failures (a segfaulting C-extension edge case in one file can't take down the run). The worker signature is tuple-based and picklable — exactly what `ProcessPoolExecutor.submit` needs.

**Q92: How do you handle very large repos without OOM?**
A: `migrate_directory_chunked` processes files in chunks (`chunk_size=100` default), spinning up a fresh `ProcessPoolExecutor` per chunk and streaming results, so memory stays bounded by chunk size rather than total repo size. Individual workers hold only one file's tree at a time; the disk cache offloads repeats. There's also cancellation: `request_cancel()` sets a flag that stops new submissions and cancels pending futures — with a `timeout` on `future.result()` so a hung worker fails that file instead of stalling the run.

**Q93: How does the parallel report look and what does it enable?**
A: `ParallelMigrationReport.summary()` prints the version range header, files processed/modified/failed, total changes, workers used, and the first 10 failed files with their error messages. Programmatic access to `file_results` lets CI mark a migration step failed when `files_failed > 0`, and the per-file `was_modified`/`changes`/`confidence` map becomes the audit log for review.

---

## 9. LLM Integration & Auto-Generation (Q94–Q96)

**Q94: What does the `LLMSuggestionEngine` do, and how does it degrade gracefully?**
A: It (a) turns an error message + code context into candidate migration rules (`suggest_from_error`, e.g. `got an unexpected keyword argument 'x'` → `add_argument` with MEDIUM confidence), (b) generates structured rules from natural-language change descriptions (`generate_from_description`), and (c) explains a rule set as breaking changes for humans (`explain_breaking_changes`). Provider detection is opportunistic (Anthropic first, then OpenAI); if no SDK/key is available or the API call fails, it silently falls back to deterministic regex heuristics (`_fallback_suggest_from_error`) that parse the same error patterns. No provider → no hard failure; results degrade to rule-based suggestions.

**Q95: How do you keep LLM output in the rule schema, and how do you constrain hallucination?**
A: A strict `SYSTEM_PROMPT` enumerates allowable `change_types` with their required fields ("Always include: id, change_type, version_introduced, description, safety; safety ∈ safe|review_required|risky") and says *"be conservative — only suggest changes you're confident about"*. Output is requested as JSON, parsed via `_parse_suggestions`/`_parse_rules_json`, and cast into typed `MigrationSuggestion`/`SuggestionConfidence (HIGH/MEDIUM/LOW)`/rule dicts. Anything that doesn't parse is dropped, not passed through. LLM rules enter the same Pydantic + validation pipeline as hand-written rules, so schema drift is caught by the same machinery.

**Q96: How does `diff_analyzer` auto-generate rules from two versions of code?**
A: `ASTExtractor` parses both the old and new code with LibCST (`cst.parse_module`) and extracts the import lists (`_extract_imports`) and top-level definitions (`_extract_definitions` — functions, classes, module-level names). `APIDiff` diffs these symbol tables pair-wise and heuristically detects: renamed functions/classes (identical bodies, changed names), added/removed arguments (signature diffing), moved modules (import origin changed), and changed defaults. Each detection is emitted as a seeded `Rule` with a reasonable `safety` and moderate `confidence_hint`, then validated like any other rule. This gives library maintainers a draft changelog/ruleset they can review instead of writing rules by hand.

---

## 10. Interfaces, MCP, & Engineering Practices (Q97–Q100)

**Q97: What is the MCP server and why put one on a migration tool?**
A: MCP (Model Context Protocol) exposes MigratorGen's capabilities as tools an AI assistant can invoke — validate rules, run a dry-run migration, generate a diff, list libraries. The `mcp/` package is a thin MCP server over the same `MigrationClient`, so a coding agent in a capable IDE can suggest/apply migrations with the engine's safety guarantees instead of issuing raw text edits. It's the same SDK-on-the-wire pattern as the API, just over the MCP transport.

**Q98: How is the API integrated with the async worker and observability?**
A: FastAPI synchronously serves small migrations; heavy repo-wide jobs are delegated to Celery over Redis (tasks in `worker/src/tasks/migration_tasks.py`), with `MigrationJob` rows persisted via async SQLAlchemy (asyncpg driver) in `shared/database.py` for status polling. Observability: structured `logger.exception/info` calls on every task, a `shared/metrics` module with prometheus-client counters for API/worker, timed durations (`duration_ms`) on every response/task, and a `/health` endpoint. Cleanup of stale jobs is a scheduled Celery task. Everything is containerised (separate Dockerfiles for api and worker).

**Q99: What taste of the SDK do consumers get, and does the code follow any notable engineering practice?**
A: One-line `MigrationClient` façade with `Rule.from_dict` everywhere; typed Pydantic request/response models so API contracts don't drift; a root `Makefile` for `make test` / `make lint` (ruff); pre-commit hooks; 186 pytest cases across core + shared; a `demo_all_features.py` showing the full whistle-stop path; and `migration-schema.json` documenting the canonical rules format. The design is "pure core + thin I/O shells + codegen", which keeps the engine unit-testable in isolation from FastAPI/Celery.

**Q100: What would you do next to take MigratorGen toward production?**
A: (1) A `--review` mode emitting a machine-readable manifest of every risky/low-confidence change for a human approve flow. (2) Incremental/diff-only scanning so unchanged files aren't even parsed by hashing file content against the cache before running. (3) More `diff_analyzer` rule detectors (signature type changes, decorator migrations). (4) A type-aware pass on top of resolver (gradual typing hints) to sharpen name resolution on typed codebases. (5) Parallel engine: backpressure + per-chunk persistence so a kill doesn't lose progress. (6) Hardening: fuzzing transformers against a corpus of real code, property tests guaranteeing round-trip fidelity (`parse(transform(parse(x))) == transform(x)`), and a plugin registry so libraries ship their own rule packs in `migration-packs/`.

---

*Revision checklist: all answers verified against the MigratorGen repo layout (`sdk/python/src/migrator_gen/core/*`, `cli/`, `mcp/`, `backend/api`, `backend/worker`, `backend/packages/shared`) — engine semantics, enum names, field names, task/fastapi endpoints, Makefile test counts (186 = 131 core + 55 shared), and package extras all match the code.*