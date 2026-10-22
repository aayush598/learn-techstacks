# Chapter 53 — Do's and Don'ts

> Part XXI · Chapter 53 · All sections

A condensed rule set for reducing error-handling complexity without building a framework.

## Finding and measuring repetition

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Count decision sites, not lines | Judge complexity by file length |
| Record whether the copies currently agree | Assume duplicated code is duplicated *and* correct |
| Delete accidental duplicates | Extract a helper for a single call site |
| Document deliberate divergence next to the copies | Let "we meant it to differ" live in a chat message |
| Add a test asserting the copies agree | Rely on review to catch drift |
| Re-measure every quarter | Measure once and assume it stays true |

## Extracting policies

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Give every policy a conservative default | Leave a category unresolved "for now" |
| Extract the decision, not the syntax | Extract a function that wraps one line |
| Make the table exhaustive | Add a `default` that guesses a category |
| Delete the old implementation | Keep the old path "as a fallback" |
| Re-run the cost analysis after re-scoping | Abandon the goal when the first design scores badly |
| Require observed drift as evidence | Count hypothetical drift as a benefit |

## Simplifying branches

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Write the decision as a table first | Nest `if`s and rely on the order |
| Make the default an explicit named constant | Let the fallthrough be the default |
| Normalize the vendor error, then map it | Write one branch per (provider, status) pair |
| Keep retry decisions pure and side-effect free | Read the clock inside the policy |
| Let the adapter own the fallback | Let each call site pick its own fallback |
| Mark degraded results as degraded | Return a fallback that looks like a normal success |

## Locating decisions and conventions

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Key status, retry, and recovery by category | Maintain a per-code status table |
| Put every provider behind one adapter | Let features call providers directly |
| Name tables after the question they answer | Scatter one question across several files |
| Measure the change cost of a new code | Assume "it's only a few files" |
| Enforce the conventions in CI | Rely on review to catch a stray status literal |
| Use `DOMAIN_CONDITION` codes | Derive codes from a class name or a message |

## Business logic and boilerplate

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Return named outcomes for expected failures | Throw an `Error` for every business rule |
| Map outcomes once, at the boundary | Map the same failure in three layers |
| Keep domain modules free of transport imports | Import `Response` into a domain file |
| Produce error codes through a typed factory | Build error objects field by field |
| Keep the happy path the shape of the code | Bury the domain rule between failure branches |
| Make the wrong thing fail to compile | Rely on discipline to keep codes consistent |

## Managing complexity

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Budget decision sites per feature | Budget only lines |
| Set budgets from the feature's shape | Apply one budget to every feature |
| Review the budget quarterly; run the check per PR | Re-negotiate the budget in every PR |
| Lower a budget only after a refactor | Lower a budget to make a check pass |
| Record adjustments in the budget file | Waive budgets in chat |
| Use a dated exception, not an inline waiver | Allow `// budget: ignore` comments |

## Anti-patterns in the wild

- **The Framework Proposal.** A 19-page design doc, 3,500 estimated lines, six weeks of work,
  to remove 210 duplicated lines. The duplication was a mapping problem; the framework was a
  solution to a different problem.
- **The Parameter Bag.** A shared helper that takes five arguments so it can serve two call
  sites that needed different answers. It acquires a sixth argument within a month.
- **The Unreachable Branch.** A correct decline handling branch that sits below a generic
  catch-all added in a later refactor. The copy that ran was the wrong one, and it paged the
  on-call team every Friday.
- **The Exception Interface.** A `FallbackProvider` with one method per failure mode, so
  every new mode became a five-file change — the exact opposite of the abstraction's purpose.
- **The Layered Table.** One table per layer (status here, retry there), so the same question
  has three answers.
- **The Budget Waiver.** A per-file `// budget: ignore` that becomes a style within a
  quarter.
- **The Line-Count Budget.** A budget that rewards compressed code and says nothing about
  duplicated decisions. Code gets denser, not simpler.

## Quick self-check

Before you call a refactor done, answer these five questions:

1. **How many decision sites does this decision have now?** If it is not 1, the refactor is
   not finished.
2. **What is the change cost of adding an error code?** More than 3 files means the
   convention is documentation, not structure.
3. **What did the extraction cost?** New concepts, new indirection, new maintenance — name
   them.
4. **Did anything get deleted?** If the old code is still there "just in case", the drift
   will return.
5. **Can a new engineer find the answer in one search?** If not, the decision is in the wrong
   place, not merely undocumented.

## Related

- [Chapter 53 — Reducing Error-Handling Complexity](../README.md)
- [Abstraction Cost Analysis](../02-deep-dive/01-abstraction-cost-analysis.md)
- [Reducing Repetition in the Checkout Flow](../03-practical-examples/01-reducing-repetition-in-checkout.md)
- [Chapter 54 — Reusable Error-Handling Infrastructure](../../54-reusable-error-handling-infrastructure/README.md)
