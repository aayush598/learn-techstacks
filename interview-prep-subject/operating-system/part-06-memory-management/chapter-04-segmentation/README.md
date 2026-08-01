# Chapter: Segmentation

## What you'll learn
- Why **segmentation** was invented (protecting & growing each part of a program — code, data, stack — separately) and why it fits human intuition.
- The full segmentation model: segment tables, base+limit per segment, and how logical addresses become `(segment, offset)`.
- Why **pure segmentation failed** (external fragmentation, variable sizes) and how the modern world combines **segmentation with paging** — including why x86-64 dropped user-visible segments entirely.

## Prerequisites (linked)
- [Part 06 README](../README.md) and Chapters 01–03 — you need paging (Chapter 03) to understand what segmentation gets *combined with*, and Chapter 02 for fragmentation.

## Sections (linked table)
| # | Section | Core question it answers |
|---|---|---|
| 01 | [Segmentation In Depth](chapter-04-segmentation/section-01-segmentation-in-depth.md) | How does a `(segment, offset)` address give per-region protection and growth? |
| 02 | [Segmentation With Paging and Examples](chapter-04-segmentation/section-02-segmentation-with-paging-and-examples.md) | Why did the industry combine segments with pages — and then, on x86-64, drop segments? |

## One-paragraph narrative connecting all sections
Segmentation is the answer to paging's blindness to program *structure*: instead of uniform 4 KB pages, it lets each region (code, data, stack) be its own variable-size segment with its own base, limit, and permissions. Section 01 builds the model — a segment table with base+limit per entry, `(segment, offset)` addressing, and why that grants natural growth and sharing. Section 02 confronts the reality: pure segmentation suffers external fragmentation exactly like Chapter 02, so real systems fused the two ideas — first Intel's x86 32-bit segmentation-with-paging, then modern OSes (including x86-64 Linux) which keep the *segment registers* only as a compatibility shell and let paging do all the work. The takeaway for interviews: segmentation = good for the programmer's mental model, bad for the allocator; paging = good for the allocator, blind to structure; modern OSes chose paging and emulate "segments" in software (VMAs).

## Common interview trap in this chapter
**Trap:** Claiming "modern OSes use segmentation." They don't, for user memory — x86-64 Linux/Windows use flat 64-bit paging; the segment registers (CS/DS/SS/FS/GS) are either hardwired to a flat base 0 or repurposed (FS/GS for TLS/percpu). Pure segmentation was abandoned because of external fragmentation. Also: do **not** confuse "segmentation fault" (a generic name for a memory-protection error) with the segmentation *scheme* — a SIGSEGV is thrown by paging's protection checks too.

## Checklist before moving on
- [ ] I can translate a `(segment, offset)` address using a segment table.
- [ ] I can explain which fragmentation pure segmentation causes and why.
- [ ] I can explain how x86-32 combined segments + paging, and the two-step address translation.
- [ ] I can explain why x86-64 removed user-visible segmentation.
- [ ] I can explain how modern OSes emulate "segments" (VMAs, TLS via FS).
