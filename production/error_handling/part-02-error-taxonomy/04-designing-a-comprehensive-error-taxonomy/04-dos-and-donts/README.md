# Chapter 4 — Do's and Don'ts

> Part II · Chapter 4 · All sections

A condensed rule set distilled from the chapter. Use it as a review checklist for any taxonomy
design.

## Why a taxonomy (4.1–4.2)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify once at creation and read everywhere | Re-derive category in each handler |
| Use a three-level hierarchy (family → category → code) | Keep one flat list of strings |
| Attach policy to categories | Hard-code policy per throw site |

## Classification axes (4.3–4.15)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| Classify origin by real cause | Infer origin from HTTP status |
| Treat severity as contextual per event | Log every `4xx` at `error` |
| Base retry on permanence **and** idempotency | Retry anything that failed once |
| Record user impact and blast radius | Alert a generic channel |
| Derive HTTP from category | Hand-pick status codes per endpoint |
| Prefix codes by domain/capability | Use global untyped codes |
| Flag security-sensitive errors | Leak SQLSTATE, SQL, or hostnames |
| Record transactional consequence | Assume every failure rolled back |
| Name the failing dependency | Treat all deps as equal |
| Mark compensation requirement | Retry blindly after partial success |

## Exclusivity and growth (4.16–4.18)

| ✅ Do | ❌ Don't |
| ----- | -------- |
| One primary category + tags | Multiple simultaneous primary categories |
| Add a category only if the policy differs | Add a category per feature or message |
| Fold extra detail into codes | Sprawl the category list |
| Assign an owner to every category | Leave categories unowned |
| Provide a fast path for new codes | Gate every code behind review |

## Anti-patterns in the wild

1. **The Message-Matching Taxonomy** — deciding policy from `err.message.includes("timeout")`.
2. **The Axis-As-Category** — making `retryable` or `transient` a category.
3. **The Flat Explosion** — 300 "categories" that are really 20 categories and 280 codes.
4. **The Status-Code Oracle** — trusting a vendor's `400` to mean client-caused.
5. **The Ownerless Family** — a shared category nobody maintains.
6. **The Rename Bomb** — renaming a public code in place, breaking clients.
7. **The Silent Category** — a new failure that never gets a home and defaults to `500`.

## Chapter checklist

- [ ] Families ≤ ~12; categories grouped and stable.
- [ ] Every error carries one primary category and a code.
- [ ] HTTP and retry are derived from the category table.
- [ ] Security-sensitive categories are flagged for redaction.
- [ ] Transactional consequence and compensation requirement are recorded for writes.
- [ ] Every category has a named owner.
- [ ] A documented process exists to add, alias, and deprecate categories and codes.

## Related

- [Chapter 4 Reference Cheat-Sheet](../05-reference/README.md)
- [Chapter 5 — Error Categories in Detail](../../05-error-categories-in-detail/README.md)
- [Error-Handling Patterns and Anti-Patterns](../../../part-17-organization/46-error-handling-patterns-and-anti-patterns/README.md)
