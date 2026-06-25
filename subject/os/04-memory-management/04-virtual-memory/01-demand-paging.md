# Demand Paging & Virtual Memory

## Virtual Memory Concept

- Execute a process **not entirely in memory**
- Only parts of the program actively needed are resident
- Illusion of near-unlimited memory (up to address space size)
- Backed by **swap space** (disk) or memory-mapped files

## Demand Paging

- Load a page into memory **only when a reference is made** to it
- Lazy swapper: never bring a page in until needed
- **Valid-invalid bit** in page table entry:
  - **Valid:** page is in memory (frame# is correct)
  - **Invalid:** either not in memory or illegal access

## Page Fault

- Access to invalid page → hardware trap to OS (**page fault**)
- **6 steps of page fault handling:**
  1. Trap to OS (save registers, program counter)
  2. OS checks if reference was legal (valid/invalid bit + protection)
  3. Find free frame (or evict a page = page replacement)
  4. Schedule disk operation to read needed page into frame
  5. Disk I/O completes, update page table (valid=1, frame# set)
  6. Restart instruction that caused the fault

### Restart Consideration

- Some CPUs restart from beginning of instruction (simpler)
- Some require precise state recovery (complex)
- Must be careful: block move instructions may partially complete

## Effective Access Time

```
EAT = (1 - p) × memory_access + p × page_fault_time
```

- **p** = page fault rate (0 ≤ p ≤ 1), must be **extremely low**
- memory_access ≈ 100 ns
- page_fault_time ≈ 10 ms (seek + latency + transfer + overhead)

**Example:** p = 0.00001 (1 in 100,000)
```
EAT = 0.99999 × 100ns + 0.00001 × 10ms
    = 99.999 ns + 100 ns
    ≈ 200 ns  (doubled! still okay)
```

For p = 0.001 (1 in 1000):
```
EAT = 0.999 × 100ns + 0.001 × 10ms
    = 99.9 ns + 10,000 ns
    ≈ 10,100 ns  (100× slowdown!)
```

**Rule:** page fault rate must be ≤ 0.00001 for acceptable performance

## Copy-on-Write (COW)

- **fork()** optimization: parent and child share all pages initially
- Pages marked **copy-on-write** (read-only in hardware)
- When either process **writes** to a page → page fault → OS copies the page
- Saves time (no full process copy) and memory (shared until modified)
- **vfork():** stronger optimization, parent blocks until child execs (no COW needed)
