# Meta — OS Topics Interview Guide

## Meta's Linux Usage
- **Custom Linux kernels** optimized for Meta's workloads
- **Kernel contributions:** BPF, cgroup v2, io_uring, slab allocator
- **HHVM (HipHop Virtual Machine):** JIT compiler for PHP/Hack

## Key OS Topics at Meta

### Memory Management at Scale
- **Page cache:** heavily used for web serving (file-backed mmap)
- **NUMA:** memory access latency varies by CPU socket
  - **NUMA-aware allocation:** `mbind()`, `numactl`, `libnuma`
  - **Remote vs local memory:** 2×–3× latency difference
- **THP (Transparent Huge Pages):** 2MB pages reduce TLB misses
  - But can cause higher memory usage (defragmentation)
- **OOM handling:** earlyoom / oomd — proactive OOM based on pressure

### Container Isolation (Twitter/Meta)
- **cgroup v2:** unified hierarchy for CPU, memory, I/O
  - **Memory limits:** `memory.max`, `memory.high` (soft limit)
  - **CPU:** `cpu.weight` (CFS shares), `cpu.max` (throttle)
- **Namespaces:** PID, NET, MNT, UTS, IPC, USER, CGROUP
- **Cgroup pressure:** PSI (Pressure Stall Information) — measure resource contention

### Kernel Bypass & Performance
- **io_uring:** async I/O with shared ring buffer (fewer syscalls)
  - Used for: storage I/O, network I/O (TCP)
- **BPF (eBPF):** programmable kernel
  - **XDP:** fast packet processing at driver level
  - **bpftrace:** dynamic tracing (strace for production)
  - **Kprobes/uprobes:** attach BPF to any kernel/user function

## HHVM & JIT
- **JIT compilation:** PHP bytecode → x86 machine code (hot paths)
- **Translation cache:** cache compiled code (large RSS)
- **TC JIT:** tracelet-based JIT (compiles hot traces)
- **Shared memory IPC:** HHVM uses shared memory for inter-process caching

## Meta's Open Source Contributions
| Project | OS Impact |
|---------|-----------|
| **BPF (eBPF)** | First major adopter + contributor |
| **cgroup v2** | Co-developed with Google (Facebook + Google) |
| **io_uring** | Meta contributed optimizations |
| **Malloc (jemalloc)** | Used by Meta, reduces fragmentation |
| **Rust in kernel** | Meta is a key Rust contributor |

## Interview Questions Pattern
- *"How does memory management change at scale with NUMA?"*
- *"How would you debug a production machine with high I/O latency?"*
  - Answer: check PSI, io_uring stats, disk iostat, BPF tracing
- *"How would you reduce tail latency in a web server?"*
  - Answer: CPU isolation, cache optimization, cgroup limits, RSS/working set tuning
- *"Explain eBPF and its use cases"*
  - Tracing, networking (XDP), security (seccomp-bpf), observability

## Interview Tips
- *"Meta runs at massive scale — every micro-optimization saves millions of dollars"*
- *"Know eBPF well — it powers observability, networking, and security at Meta"*
- *"Memory management toolkit: huge pages, NUMA binding, cgroup limits, jemalloc"*
- *"io_uring is the future of async I/O — fewer syscalls, better performance"*
