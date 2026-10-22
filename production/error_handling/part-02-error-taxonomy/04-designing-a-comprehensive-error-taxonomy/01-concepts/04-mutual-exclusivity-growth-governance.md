# Mutual Exclusivity, Preventing Growth, and Governance

> Part II · Chapter 4 · Sections 4.16–4.18 · _Estimated reading time: 20 min_
> **Prerequisite:** [Classification Axes: HTTP → Compensation](./03-classification-axes-http-through-compensation.md)

## In one sentence

A usable taxonomy is **mutually exclusive where it must decide** and **explicitly overlapping
where it describes**; it grows only when a policy changes; and it survives only if every category
has an **owner**.

## Why this matters in production

A taxonomy fails in two opposite ways. If categories overlap everywhere, no handler knows which
one wins and you get inconsistent routing. If categories multiply without control, you get 300
codes nobody understands. Sections 4.16–4.18 are the governance controls that keep the taxonomy
*decision-grade*.

## 4.16 Mutually exclusive vs overlapping

**Mutually exclusive** dimensions force exactly one answer and are used for **routing**. **Overlapping**
dimensions can have multiple true values and are used for **description**.

| Kind | Example axis | Values | Use |
| ---- | ------------ | ------ | --- |
| Mutually exclusive | `category` | one of `validation` \| `conflict` \| `timeout` … | Routing, code prefix |
| Overlapping | `tags` | `["retryable","sensitive","partial"]` | Enrichment, filtering |

The rule: **one primary category per error**, plus zero or more descriptive tags.

```text
primary_category = "external_api"        (exactly one — drives routing)
tags             = ["transient", "dependency:stripe", "sensitive"]  (many — drive enrichment)
```

A single error legitimately belongs to several *axes* at once (transient + remote + partial), but
only **one primary category**. Choosing it is the subject of the deep-dive on the primary axis.

> ⚠️ **Hazard.** When two categories both seem "primary", the bug is usually that you are
> conflating an **axis** (a property) with a **category** (a bucket). `transient` is an axis
> value, not a category.

## 4.17 Preventing category growth

Categories should be added **only when the policy differs**. If two conditions share the same
retry verdict, status class, alert, and disclosure rule, they are one category, not two.

A decision test before adding a category:

```text
Does the new condition differ from an existing category in ANY of:
  - retry eligibility?
  - HTTP status class?
  - alert severity / routing?
  - compensation requirement?
  - disclosure/redaction rule?
If NO to all → it is a new CODE within an existing category, not a new category.
If YES to any → a new category may be justified.
```

Growth controls:

- **Bound the hierarchy.** Families ~7–12, categories per family single digits.
- **Favor codes over categories.** Specific conditions belong at level 3.
- **Reuse before you add.** Search the registry first (Chapter 8).
- **Deprecate.** Remove categories that no longer occur.

## 4.18 Ownership and governance

Every category needs an **owner** (a team), a **definition**, and a **change process**.

| Artifact | Owned by | Contains |
| -------- | -------- | -------- |
| Taxonomy doc | Platform/architecture | Families, axes, rules |
| Category definitions | Domain teams | Trigger, meaning, policy |
| Code registry | Platform + domain | Codes, HTTP map, retry, docs |
| Review gate | Architecture group | New/renamed categories |

A lightweight governance loop:

1. **Propose** a new category/code via an ADR or PR to the registry.
2. **Review** against the growth test in 4.17.
3. **Approve** and assign an owner and a documented policy.
4. **Publish** to the registry and the public error docs.
5. **Review** periodically; deprecate unused entries.

### Ownership anti-patterns

- **Unowned shared core** — everyone edits, nobody maintains.
- **Per-team vocabularies** — two teams call the same failure different names.
- **Governance by committee** — every addition takes weeks, so people bypass it.

Aim for a **fast path** (most codes added without ceremony) and a **slow path** (new families and
policy changes require review).

## Worked example — a rejected category

Acme proposes a new category `CONFLICT_EXPORT_RUNNING` because "two exports cannot run for the
same tenant." Applying 4.17:

```text
Retry?      no  (same as conflict)
HTTP?       409 (same as conflict)
Alert?      none (same as conflict)
Compensation? no (same as conflict)
Decision:   NOT a new category → it is code CONFLICT_OPERATION_IN_PROGRESS inside `conflict`.
```

The team avoids a sprawling category and gets a precise code.

## Key data / numbers

- A practical ceiling: **≤ 12 families**, **≤ ~100 categories** total, and codes grow in the
  hundreds but are grouped.
- Two categories with identical policy are a **merge candidate** — a common cleanup task.
- Registry reviews commonly run **monthly**; new families are rare (a few per year).

## Real-world use case — Acme SaaS

Acme's registry reached 40 categories, several overlapping (`not_found` vs `missing_resource`,
`timeout` vs `deadline`). A single owner (platform) merged them, mapped old codes to new ones via
aliases (Chapter 8 deprecation), and added a review gate. New features now add codes without new
categories, and the global handler's routing table shrank from 40 branches to 12. Fewer branches,
fewer bugs.

## Trade-offs

| Governance style | Pros | Cons | When |
| ---------------- | ---- | ---- | ---- |
| None | Fast | Sprawl, drift | Solo prototype |
| Lightweight (owners + ADR) | Balanced | Needs discipline | Most SaaS |
| Heavy (committee, SLAs) | Consistent | Slow, bypassed | Regulated enterprise |

## Do / Don't

| ✅ Do | ❌ Don't |
| ----- | -------- |
| One primary category + tags | Multiple simultaneous primary categories |
| Add a category only if policy differs | Add categories for every message |
| Assign a team owner per category | Leave categories unowned |
| Provide a fast path for codes | Require review for every code |

## Common mistakes

- **Treating an axis value as a category** (e.g. making `retryable` a category).
- **Goal-driven sprawl**: "we need a category per endpoint."
- **No deprecation**: dead categories accumulate and confuse.
- **Governance so heavy** that engineers route around it.

## Checklist

- [ ] Does each error have exactly one primary category?
- [ ] Are descriptive properties modeled as tags, not categories?
- [ ] Can you answer "why is this a separate category?" with a policy difference?
- [ ] Does every category have a named owner?
- [ ] Is there a process to propose, review, and deprecate categories?

## Related

- [The Multi-Axis Classification Model](../02-deep-dive/01-multi-axis-classification-model.md)
- [Taxonomy Governance and Evolution](../02-deep-dive/02-taxonomy-governance-and-evolution.md)
- [Error Codes and Error Registries](../../../part-03-error-models/08-error-codes-and-error-registries/README.md)
- [Error Translation and Normalization](../../../part-06-boundaries-and-translation/16-error-translation-and-normalization/README.md)
