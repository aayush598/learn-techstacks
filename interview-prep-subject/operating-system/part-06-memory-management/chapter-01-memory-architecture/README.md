# Chapter: Memory Architecture

## What you'll learn
- Why programs use *virtual* addresses instead of raw RAM locations (the address-space abstraction).
- The three times an address can be bound to a physical location: compile time, load time, run time — and why run-time binding wins.
- The difference between logical (virtual), physical, and relative addresses, and the role of the **MMU** (Memory Management Unit).
- How the oldest, simplest protection scheme works: **base and limit registers**, and exactly why it is insufficient on modern hardware.

## Prerequisites (linked)
- [Part 06 README](../README.md) — memory management overview and study order.
- Part 01/02 concepts: a *process* is a program in execution with its own address space. Revisit if fuzzy.

## Sections (linked table)
| # | Section | Core question it answers |
|---|---|---|
| 01 | [Address Spaces and Address Binding](section-01-address-spaces-and-address-binding.md) | Why does every process get its own private "fake" address space, and *when* do fake addresses become real ones? |
| 02 | [Logical vs Physical Address and MMU](section-02-logical-vs-physical-address-and-mmu.md) | Who does the logical→physical translation on every memory access, and at what cost? |
| 03 | [Base and Limit Registers](section-03-base-and-limit-registers.md) | What was the first working protection scheme, and why did it die? |

## One-paragraph narrative connecting all sections
Every process believes it owns the entire machine's memory starting at address 0. Section 01 explains why that fiction exists (isolation, portability, relocation) and the three moments — compile, load, run — when the fiction can be reconciled with reality. Section 02 shows that on modern systems the reconciliation happens *per instruction* inside hardware: the CPU emits a logical address, and the MMU (aided by base/limit-style registers in its simplest form) translates and checks it before it ever reaches the memory bus. Section 03 zooms in on the simplest translator ever built — two registers per process — to make the translation/protection concept concrete, and reveals the flaw (physical memory is contiguous and fragmented) that motivates Part 06 Chapter 02-04.

## Common interview trap in this chapter
**Trap:** Saying "the MMU does the translation." The correct phrasing: the *CPU + MMU cooperate*; the MMU holds the base/limit (or page-table base) registers and performs the arithmetic/checking, but it's driven by the CPU's instruction fetch/execute path. Also: binding is **not** "either/or" — modern OSes use *load-time* for some things and *run-time* for nearly all user code. And a "logical address" is often *smaller* than the physical address space on 32-bit; on 64-bit systems a 64-bit virtual address maps onto a *larger* physical space only via PAE/address extension — know which one you're discussing.

## Checklist before moving on
- [ ] I can define logical vs physical address and say who translates.
- [ ] I can name all three binding times and when each runs.
- [ ] I can explain how base/limit gives protection but not relocation without software help.
- [ ] I can describe what the MMU does on a single `LOAD` instruction.
- [ ] I can explain why external fragmentation kills base/limit in practice.
