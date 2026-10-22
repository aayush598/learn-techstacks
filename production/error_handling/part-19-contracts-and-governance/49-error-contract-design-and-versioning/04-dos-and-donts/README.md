# Chapter 49 — Do's and Don'ts

> Part XIX · Chapter 49 · All sections

A condensed rule set for designing and evolving error contracts.

## Surfaces and tiers

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Assign a tier (T0–T3) and an owner per surface | Assume "internal" means "nobody depends on it" |
| Treat a first-party mobile app as a public consumer | Assume the frontend is always up to date |
| Version a service, not each error inside it | Carve per-error versions inside one service version |
| Export a vocabulary (code union) from shared modules | Export a class hierarchy as the contract |
| Choose the higher tier when unsure | Under-promise stability to avoid the work |

## Changing a contract

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify every change as additive or breaking | Change a public code's status in place |
| Introduce a new code for a new meaning | Repurpose a deprecated or retired code |
| Freeze the deprecated code's meaning | "Improve" the deprecated code mid-window |
| Add a new code for a status change | Change 4xx → 4xx and call it cosmetic |
| Gate removal on consumption telemetry | Remove because the date arrived |
| Keep the alias until the code is removed | Delete the alias with the registry row |
| Dual-emit one-to-one renames | Try to dual-emit a one-to-many split |

## Compatibility

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Have a default branch for every code lookup | Let an unknown code throw |
| Tolerate unknown fields and enum values | Reject unknown values |
| Canonicalise unknown inbound codes | Throw on an unrecognised inbound code |
| Use versionless `type` URIs, one per problem class | Version every `type` URI |
| Carry the contract version on every error response | Keep the version only in a document |
| Test published guarantees in CI | Assume the implementation matches the spec |

## Ownership and documentation

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Name one owning team per contract | Let a contract be "owned by the backend team" |
| Assign a steward per code family | Leave a family with no steward |
| Document guarantees, not observations | Promise the typical status for a condition |
| Version the contract document | Rewrite it without a bump |
| Generate the catalogue from the registry | Hand-edit the catalogue |
| Record decisions as ADRs | Adopt a contract without recording why |

## Messages

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Branch on `code`, then `type`, then `status` | Branch on `detail`, `title`, or `message` |
| Ship message keys; the client resolves the words | Ship English prose as the contract |
| Add a structured field when a value is needed | Parse a value out of a message with a regex |
| Reword freely | Treat wording as a promise |

## Anti-patterns in the wild

1. **The Status Mutator** — a public code's status changed "for accuracy"; clients now retry a
   permanent failure forever.
2. **The Repurposed Code** — `PAYMENT_CARD_DECLINED` now covers two conditions; half the clients
   take the wrong branch.
3. **The Wiki Contract** — a catalogue that lagged the registry by two months.
4. **The Ownerless Surface** — anyone can change any public code, because nobody is responsible.
5. **The Calendar Deprecation** — removed on schedule while three partners were still consuming it.
6. **The Prose Contract** — a client that regexes `detail` and breaks on a reword.
7. **The Contract Without a Version** — "which guarantees were live in March?" is unanswerable.
8. **The Accidental Major** — a MINOR release added a `clientAction` value and broke every
   exhaustive `switch`.

## Chapter checklist

- [ ] Every surface has a tier, an owner, and a written stability promise.
- [ ] Every change is classified additive or breaking before it ships.
- [ ] Breaking changes produce a new code; the old code keeps its meaning.
- [ ] Consumers have a default branch and tolerate unknown codes and fields.
- [ ] Deprecations run the full five-phase workflow with telemetry gates.
- [ ] The contract has its own version, changelog, and `type` URI convention.
- [ ] Ownership is encoded where the work happens (registry metadata, `CODEOWNERS`).
- [ ] No consumer branches on message text.
- [ ] Rules that cannot be checked are demoted to guidance.

## Related

- [Chapter 49 Reference](../05-reference/README.md)
- [The Deprecation Workflow: Introduce → Dual-Emit → Sunset](../03-practical-examples/01-deprecation-workflow-introduce-dual-emit-sunset.md)
- [The Error Contract Spec and the ADR That Adopted It](../03-practical-examples/02-error-contract-spec-and-adr.md)
- [Chapter 50 — Error Handling as an Engineering Standard](../50-error-handling-as-an-engineering-standard/README.md)
