# Cuda — Memory Hierarchy Interview Questions and Answers

## Q1: What is the CUDA memory hierarchy?
**A:** Registers (per-thread, fastest), shared memory (per-block, on-chip), global memory (device-wide, off-chip DRAM), plus constant, texture/read-only, and local memory (register spills).

## Q2: What is the trade-off between registers and shared memory?
**A:** Both are on-chip; registers are per-thread and fastest but limited (~64K per SM on modern GPUs while ~255 per thread); shared is per-block, indexed, and lets threads exchange data.

## Q3: Why is global memory latency so high?
**A:** DRAM access takes 400-800 cycles; kernels hide it with concurrency (many warps), so throughput depends on having enough parallelism in flight to keep memory busy.

## Q4: How does the L2 cache help a raytracer?
**A:** L2 (tens of MB on modern GPUs) caches global reads across SMs; nearby rays sampling nearby grid cells hit it, so interpolation-heavy stages benefit when data fits L2.

## Q5: What is the uniformity vs divergence of constant memory?
**A:** __constant__ is cached and optimized for every thread reading the SAME address (uniform); it is ideal for metric parameters (mass, spin) and camera matrices since they are read uniformly.

## Q6: When is texture/read-only memory useful?
**A:** For linear interpolation of fields (density, temperature) with cache benefits and clamping/wrap modes; the read-only __ldg() loads also hint the compiler.

## Q7: What is local memory?
**A:** Per-thread spill space that lives in global DRAM; it is a performance trap for large per-thread arrays - prefer keeping ray state in registers.

## Q8: What is the size of shared memory on current GPUs?
**A:** Up to 228KB per block on H100-class (opt-in) and ~100KB typical on consumer; dynamically beyond static amounts requires cudaFuncSetAttribute.

## Q9: How do printf and other host services interact with device memory?
**A:** printf in kernels is supported but serializes output and can perturb timing; use it in debug kernels only and gate it behind a compile flag.

## Q10: What is memory coalescing at the hardware level?
**A:** The memory system groups a warp's 32 accesses into as few 32-byte sectors/transactions as possible when addresses are consecutive - coalesced reads move data once per cache line.

## Q11: Why does padding matter for 2D/3D field arrays?
**A:** Row widths that are exact multiples of cache lines avoid wasted sectors; strided access across rows is where padding reduces effective bandwidth loss.

## Q12: How does zero-copy / managed memory fit the hierarchy?
**A:** cudaMallocManaged pages migrate between host and device on demand - convenient but with fine-grained faults it can serialize; pinned+explicit copies are often faster for streaming data.

## Q13: What is the correct order to optimize memory?
**A:** Measure first, then fix access patterns (coalescing/padding), then add shared-memory tiling, then manual data reuse - each step targets a measured bottleneck.

## Q14: How do atomics interact with the memory hierarchy?
**A:** Atomics operate in L2 on global addresses; they serialize for conflicting addresses (e.g., multiple rays scattering into one pixel) - avoid whenever one thread can own one output.

## Q15: What is the impact of FP32 vs FP64 throughput in the hierarchy sense?
**A:** FP64 runs at 1/2 to 1/64 of FP32 rate on consumer GPUs (1/2 on data-center A100/H100 without special config); the memory pipeline cares about bytes moved, not the FMUL class.

## Q16: Explain the core idea behind memory hierarchy in the context of CUDA.
**A:** It is about expressing a parallel computation so the GPU scheduler can split it across many lightweight threads that execute the same instruction stream on different data.

## Q17: Why is memory hierarchy important for a raytracer kernel?
**A:** Because a raytracer runs the same integration work per pixel; understanding memory hierarchy tells you how to map pixels to threads and memory so the device stays saturated.

## Q18: What does the hardware do when a warp executes memory hierarchy?
**A:** All lanes in a warp execute the same instruction; memory hierarchy decides how that instruction interacts with memory banks, caches, and the per-SM execution resources.

## Q19: How does memory hierarchy affect occupancy?
**A:** Registry usage, shared memory, and work per thread set by memory hierarchy limit how many blocks fit per SM; higher occupancy hides latency but never guarantees speed.

## Q20: What are the common mistakes beginners make with memory hierarchy?
**A:** Launching too few threads, assuming serial ordering, ignoring memory layout, and treating device code as host code - all of which memory hierarchy must explicitly address.

## Q21: How would you validate your understanding of memory hierarchy?
**A:** Write a micro-benchmark that isolates the memory hierarchy behavior, measure with Nsight, and compare wall-clock time against a host reference implementation.

## Q22: Describe how memory hierarchy interacts with the memory hierarchy.
**A:** The memory hierarchy access pattern decides whether reads hit the L2/L1 caches and coalesce into few transactions; global latency is the usual bottleneck.

## Q23: When should you avoid depending on memory hierarchy at all?
**A:** When the problem is tiny or serial, because launch overhead and fixed resource costs of memory hierarchy outperform any marginal GPU parallelism.

## Q24: What is the relationship between memory hierarchy and numerical correctness?
**A:** Floating point order and precision choices in memory hierarchy can change results; determinism requires fixed accumulation order or careful atomic handling.

## Q25: Give a concrete example where memory hierarchy matters on a modern GPU.
**A:** On a 4090-class card, memory hierarchy governs how many concurrent warps can backlog global-memory stalls, directly capping the achieved instructions per second.

## Q26: What should a production engineer benchmark about memory hierarchy?
**A:** Achieved occupancy, memory throughput, divergence rate, register spills, and kernel duration - all surfaced by profiling memory hierarchy choices.

## Q27: How does memory hierarchy change when scaling to multiple GPUs?
**A:** Per-device memory hierarchy stays local, but you add host-side distribution, transfer overlap, and result collection for the overall frame.

## Q28: What kernel design decisions flow from memory hierarchy?
**A:** Block size, grid dimensions, whether to preload to shared memory, loop structure, and halting strategy for early ray termination.

## Q29: Compare the cost of getting memory hierarchy right early vs late.
**A:** Fixing memory hierarchy after the pipeline is written means rewriting kernels and re-validating images; deciding it first saves most of that rework.

## Q30: What documentation should exist for memory hierarchy?
**A:** A short design note stating the assumptions, measured numbers, and the validation test so future changes to memory hierarchy are reviewable.

## Q31: How do you explain memory hierarchy to a non-GPU colleague?
**A:** Analogize to a factory: memory hierarchy is the layout of workbenches and machines so thousands of identical jobs finish in parallel without colliding.

## Q32: What role does memory hierarchy play in frame-to-frame consistency?
**A:** Deterministic memory hierarchy means the same inputs give identical pixels every export, which matters when you render an animation one frame at a time.

## Q33: How would you get a 2x speedup out of memory hierarchy?
**A:** Often by improving memory reuse through memory hierarchy: precompute, cache, and process in tiles instead of touching global memory repeatedly.

## Q34: What are the limits of memory hierarchy on current hardware?
**A:** The finite number of threads per SM, shared memory bytes, registers, and memory bandwidth all cap memory hierarchy; reaching these limits signals a rendering ceiling.

## Q35: How do warps schedule work that depends on memory hierarchy?
**A:** The scheduler picks eligible warps whose data dependencies are resolved; poor memory hierarchy creates long stalls that starve the execution units.

## Q36: What is the minimal viable test for memory hierarchy?
**A:** Render one known image, profile kernel time, and confirm the result matches a reference before adding more complexity on top of memory hierarchy.

## Q37: How does memory hierarchy interact with numerical integrators?
**A:** Integrators advance each ray with feedback; memory hierarchy decides whether per-ray state stays in registers and how divergent the compute becomes.

## Q38: What is the mental model for memory hierarchy at the thread level?
**A:** One thread owns one unit of work; memory hierarchy defines how that work reads inputs, keeps intermediate state, writes output, and finishes when done.

## Q39: How do libraries and your own kernels divide responsibility for memory hierarchy?
**A:** Libraries like cuBLAS/cuFFT handle their own memory hierarchy; your kernels must match their launch dimensions and memory layouts for zero-copy interop.

## Q40: How do libraries and your own kernels divide responsibility for memory hierarchy - justify your answer with a concrete production example.
**A:** Libraries like cuBLAS/cuFFT handle their own memory hierarchy; your kernels must match their launch dimensions and memory layouts for zero-copy interop. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the mental model for memory hierarchy at the thread level - justify your answer with a concrete production example.
**A:** One thread owns one unit of work; memory hierarchy defines how that work reads inputs, keeps intermediate state, writes output, and finishes when done. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does memory hierarchy interact with numerical integrators - justify your answer with a concrete production example.
**A:** Integrators advance each ray with feedback; memory hierarchy decides whether per-ray state stays in registers and how divergent the compute becomes. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What is the minimal viable test for memory hierarchy - justify your answer with a concrete production example.
**A:** Render one known image, profile kernel time, and confirm the result matches a reference before adding more complexity on top of memory hierarchy. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How do warps schedule work that depends on memory hierarchy - justify your answer with a concrete production example.
**A:** The scheduler picks eligible warps whose data dependencies are resolved; poor memory hierarchy creates long stalls that starve the execution units. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What are the limits of memory hierarchy on current hardware - justify your answer with a concrete production example.
**A:** The finite number of threads per SM, shared memory bytes, registers, and memory bandwidth all cap memory hierarchy; reaching these limits signals a rendering ceiling. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How would you get a 2x speedup out of memory hierarchy - justify your answer with a concrete production example.
**A:** Often by improving memory reuse through memory hierarchy: precompute, cache, and process in tiles instead of touching global memory repeatedly. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What role does memory hierarchy play in frame-to-frame consistency - justify your answer with a concrete production example.
**A:** Deterministic memory hierarchy means the same inputs give identical pixels every export, which matters when you render an animation one frame at a time. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you explain memory hierarchy to a non-GPU colleague - justify your answer with a concrete production example.
**A:** Analogize to a factory: memory hierarchy is the layout of workbenches and machines so thousands of identical jobs finish in parallel without colliding. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What documentation should exist for memory hierarchy - justify your answer with a concrete production example.
**A:** A short design note stating the assumptions, measured numbers, and the validation test so future changes to memory hierarchy are reviewable. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: Compare the cost of getting memory hierarchy right early vs late - justify your answer with a concrete production example.
**A:** Fixing memory hierarchy after the pipeline is written means rewriting kernels and re-validating images; deciding it first saves most of that rework. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What kernel design decisions flow from memory hierarchy - justify your answer with a concrete production example.
**A:** Block size, grid dimensions, whether to preload to shared memory, loop structure, and halting strategy for early ray termination. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How does memory hierarchy change when scaling to multiple GPUs - justify your answer with a concrete production example.
**A:** Per-device memory hierarchy stays local, but you add host-side distribution, transfer overlap, and result collection for the overall frame. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What should a production engineer benchmark about memory hierarchy - justify your answer with a concrete production example.
**A:** Achieved occupancy, memory throughput, divergence rate, register spills, and kernel duration - all surfaced by profiling memory hierarchy choices. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: Give a concrete example where memory hierarchy matters on a modern GPU - justify your answer with a concrete production example.
**A:** On a 4090-class card, memory hierarchy governs how many concurrent warps can backlog global-memory stalls, directly capping the achieved instructions per second. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is the relationship between memory hierarchy and numerical correctness - justify your answer with a concrete production example.
**A:** Floating point order and precision choices in memory hierarchy can change results; determinism requires fixed accumulation order or careful atomic handling. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: When should you avoid depending on memory hierarchy at all - justify your answer with a concrete production example.
**A:** When the problem is tiny or serial, because launch overhead and fixed resource costs of memory hierarchy outperform any marginal GPU parallelism. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: Describe how memory hierarchy interacts with the memory hierarchy - justify your answer with a concrete production example.
**A:** The memory hierarchy access pattern decides whether reads hit the L2/L1 caches and coalesce into few transactions; global latency is the usual bottleneck. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: How would you validate your understanding of memory hierarchy - justify your answer with a concrete production example.
**A:** Write a micro-benchmark that isolates the memory hierarchy behavior, measure with Nsight, and compare wall-clock time against a host reference implementation. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What are the common mistakes beginners make with memory hierarchy - justify your answer with a concrete production example.
**A:** Launching too few threads, assuming serial ordering, ignoring memory layout, and treating device code as host code - all of which memory hierarchy must explicitly address. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: How does memory hierarchy affect occupancy - justify your answer with a concrete production example.
**A:** Registry usage, shared memory, and work per thread set by memory hierarchy limit how many blocks fit per SM; higher occupancy hides latency but never guarantees speed. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What does the hardware do when a warp executes memory hierarchy - justify your answer with a concrete production example.
**A:** All lanes in a warp execute the same instruction; memory hierarchy decides how that instruction interacts with memory banks, caches, and the per-SM execution resources. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why is memory hierarchy important for a raytracer kernel - justify your answer with a concrete production example.
**A:** Because a raytracer runs the same integration work per pixel; understanding memory hierarchy tells you how to map pixels to threads and memory so the device stays saturated. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: Explain the core idea behind memory hierarchy in the context of CUDA - justify your answer with a concrete production example.
**A:** It is about expressing a parallel computation so the GPU scheduler can split it across many lightweight threads that execute the same instruction stream on different data. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: Explain the core idea behind memory hierarchy in the context of CUDA - justify your answer with a concrete production example.
**A:** It is about expressing a parallel computation so the GPU scheduler can split it across many lightweight threads that execute the same instruction stream on different data. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why is memory hierarchy important for a raytracer kernel - justify your answer with a concrete production example.
**A:** Because a raytracer runs the same integration work per pixel; understanding memory hierarchy tells you how to map pixels to threads and memory so the device stays saturated. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What does the hardware do when a warp executes memory hierarchy - justify your answer with a concrete production example.
**A:** All lanes in a warp execute the same instruction; memory hierarchy decides how that instruction interacts with memory banks, caches, and the per-SM execution resources. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How does memory hierarchy affect occupancy - justify your answer with a concrete production example.
**A:** Registry usage, shared memory, and work per thread set by memory hierarchy limit how many blocks fit per SM; higher occupancy hides latency but never guarantees speed. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What are the common mistakes beginners make with memory hierarchy - justify your answer with a concrete production example.
**A:** Launching too few threads, assuming serial ordering, ignoring memory layout, and treating device code as host code - all of which memory hierarchy must explicitly address. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How would you validate your understanding of memory hierarchy - justify your answer with a concrete production example.
**A:** Write a micro-benchmark that isolates the memory hierarchy behavior, measure with Nsight, and compare wall-clock time against a host reference implementation. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: Describe how memory hierarchy interacts with the memory hierarchy - justify your answer with a concrete production example.
**A:** The memory hierarchy access pattern decides whether reads hit the L2/L1 caches and coalesce into few transactions; global latency is the usual bottleneck. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: When should you avoid depending on memory hierarchy at all - justify your answer with a concrete production example.
**A:** When the problem is tiny or serial, because launch overhead and fixed resource costs of memory hierarchy outperform any marginal GPU parallelism. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What is the relationship between memory hierarchy and numerical correctness - justify your answer with a concrete production example.
**A:** Floating point order and precision choices in memory hierarchy can change results; determinism requires fixed accumulation order or careful atomic handling. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: Give a concrete example where memory hierarchy matters on a modern GPU - justify your answer with a concrete production example.
**A:** On a 4090-class card, memory hierarchy governs how many concurrent warps can backlog global-memory stalls, directly capping the achieved instructions per second. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What should a production engineer benchmark about memory hierarchy - justify your answer with a concrete production example.
**A:** Achieved occupancy, memory throughput, divergence rate, register spills, and kernel duration - all surfaced by profiling memory hierarchy choices. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How does memory hierarchy change when scaling to multiple GPUs - justify your answer with a concrete production example.
**A:** Per-device memory hierarchy stays local, but you add host-side distribution, transfer overlap, and result collection for the overall frame. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What kernel design decisions flow from memory hierarchy - justify your answer with a concrete production example.
**A:** Block size, grid dimensions, whether to preload to shared memory, loop structure, and halting strategy for early ray termination. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: Compare the cost of getting memory hierarchy right early vs late - justify your answer with a concrete production example.
**A:** Fixing memory hierarchy after the pipeline is written means rewriting kernels and re-validating images; deciding it first saves most of that rework. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What documentation should exist for memory hierarchy - justify your answer with a concrete production example.
**A:** A short design note stating the assumptions, measured numbers, and the validation test so future changes to memory hierarchy are reviewable. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How do you explain memory hierarchy to a non-GPU colleague - justify your answer with a concrete production example.
**A:** Analogize to a factory: memory hierarchy is the layout of workbenches and machines so thousands of identical jobs finish in parallel without colliding. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What role does memory hierarchy play in frame-to-frame consistency - justify your answer with a concrete production example.
**A:** Deterministic memory hierarchy means the same inputs give identical pixels every export, which matters when you render an animation one frame at a time. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How would you get a 2x speedup out of memory hierarchy - justify your answer with a concrete production example.
**A:** Often by improving memory reuse through memory hierarchy: precompute, cache, and process in tiles instead of touching global memory repeatedly. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What are the limits of memory hierarchy on current hardware - justify your answer with a concrete production example.
**A:** The finite number of threads per SM, shared memory bytes, registers, and memory bandwidth all cap memory hierarchy; reaching these limits signals a rendering ceiling. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How do warps schedule work that depends on memory hierarchy - justify your answer with a concrete production example.
**A:** The scheduler picks eligible warps whose data dependencies are resolved; poor memory hierarchy creates long stalls that starve the execution units. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What is the minimal viable test for memory hierarchy - justify your answer with a concrete production example.
**A:** Render one known image, profile kernel time, and confirm the result matches a reference before adding more complexity on top of memory hierarchy. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How does memory hierarchy interact with numerical integrators - justify your answer with a concrete production example.
**A:** Integrators advance each ray with feedback; memory hierarchy decides whether per-ray state stays in registers and how divergent the compute becomes. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the mental model for memory hierarchy at the thread level - justify your answer with a concrete production example.
**A:** One thread owns one unit of work; memory hierarchy defines how that work reads inputs, keeps intermediate state, writes output, and finishes when done. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How do libraries and your own kernels divide responsibility for memory hierarchy - justify your answer with a concrete production example.
**A:** Libraries like cuBLAS/cuFFT handle their own memory hierarchy; your kernels must match their launch dimensions and memory layouts for zero-copy interop. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How do libraries and your own kernels divide responsibility for memory hierarchy - justify your answer with a concrete production example.
**A:** Libraries like cuBLAS/cuFFT handle their own memory hierarchy; your kernels must match their launch dimensions and memory layouts for zero-copy interop. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the mental model for memory hierarchy at the thread level - justify your answer with a concrete production example.
**A:** One thread owns one unit of work; memory hierarchy defines how that work reads inputs, keeps intermediate state, writes output, and finishes when done. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does memory hierarchy interact with numerical integrators - justify your answer with a concrete production example.
**A:** Integrators advance each ray with feedback; memory hierarchy decides whether per-ray state stays in registers and how divergent the compute becomes. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What is the minimal viable test for memory hierarchy - justify your answer with a concrete production example.
**A:** Render one known image, profile kernel time, and confirm the result matches a reference before adding more complexity on top of memory hierarchy. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How do warps schedule work that depends on memory hierarchy - justify your answer with a concrete production example.
**A:** The scheduler picks eligible warps whose data dependencies are resolved; poor memory hierarchy creates long stalls that starve the execution units. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What are the limits of memory hierarchy on current hardware - justify your answer with a concrete production example.
**A:** The finite number of threads per SM, shared memory bytes, registers, and memory bandwidth all cap memory hierarchy; reaching these limits signals a rendering ceiling. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How would you get a 2x speedup out of memory hierarchy - justify your answer with a concrete production example.
**A:** Often by improving memory reuse through memory hierarchy: precompute, cache, and process in tiles instead of touching global memory repeatedly. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What role does memory hierarchy play in frame-to-frame consistency - justify your answer with a concrete production example.
**A:** Deterministic memory hierarchy means the same inputs give identical pixels every export, which matters when you render an animation one frame at a time. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you explain memory hierarchy to a non-GPU colleague - justify your answer with a concrete production example.
**A:** Analogize to a factory: memory hierarchy is the layout of workbenches and machines so thousands of identical jobs finish in parallel without colliding. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What documentation should exist for memory hierarchy - justify your answer with a concrete production example.
**A:** A short design note stating the assumptions, measured numbers, and the validation test so future changes to memory hierarchy are reviewable. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: Compare the cost of getting memory hierarchy right early vs late - justify your answer with a concrete production example.
**A:** Fixing memory hierarchy after the pipeline is written means rewriting kernels and re-validating images; deciding it first saves most of that rework. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What kernel design decisions flow from memory hierarchy - justify your answer with a concrete production example.
**A:** Block size, grid dimensions, whether to preload to shared memory, loop structure, and halting strategy for early ray termination. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How does memory hierarchy change when scaling to multiple GPUs - justify your answer with a concrete production example.
**A:** Per-device memory hierarchy stays local, but you add host-side distribution, transfer overlap, and result collection for the overall frame. A concrete example: consistently applying memory hierarchy in code review and regression tests keeps the whole pipeline trustworthy.
