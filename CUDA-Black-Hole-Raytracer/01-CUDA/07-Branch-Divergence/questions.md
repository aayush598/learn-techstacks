# Cuda — Branch Divergence Interview Questions and Answers

## Q1: What causes branch divergence?
**A:** A single if/else or loop whose condition differs across lanes of a warp; the hardware executes each branch path serially with masks, multiplying cost.

## Q2: What is the cost formula for divergence?
**A:** Time roughly proportional to the number of distinct paths taken: if half the warp takes each branch, the warp pays both branch bodies in sequence.

## Q3: How does divergence manifest in a geodesic tracer?
**A:** Rays terminate at different radii/step counts (disk hit, horizon capture, escape), producing divergence in every termination branch and loop count.

## Q4: What is the idiom to avoid per-ray early-out?
**A:** Instead of an early break per thread, set a 'dead ray' flag and let the warp continue; the loop increments for all lanes until the max budget, then exits once.

## Q5: How do you implement the dead-ray mask?
**A:** bool alive = true; in the loop: if (alive) { step }; alive &= (state != escaped); the warp still loops len(maxRay) times but only paying work for live lanes.

## Q6: What is the trade-off of the mask approach?
**A:** You pay the full loop length for the longest ray in the warp but only compute for live lanes; net win when path lengths are similar, loss when extreme.

## Q7: How do you sort rays to reduce divergence?
**A:** Bucket or sort rays by computed impact parameter or region before the kernel so warps contain similar-path rays - common in production tracers, costs a sort.

## Q8: Why is dynamic termination cheaper than a branch?
**A:** Some hardware supports 'convergent' or early-exit heuristics at the warp level; relying on them is compiler-dependent, so deterministic masks are the portable choice.

## Q9: How does divergence interact with the scheduling?
**A:** Divergence desynchronizes memory-access phases, potentially hurting coalescing; keeping warps homogeneous also keeps their memory stages aligned.

## Q10: What is the predication alternative to loops?
**A:** For short bodies, the compiler flattens branches to predicated selects; it removes divergence but always executes both sides - good for tiny geodesic steps.

## Q11: When measuring divergence, what profile metric do you watch?
**A:** Nsight's 'branch divergence' and SM 'warp stalls' counters; if divergence is small but stalls remain, memory latency rather than control flow is the issue.

## Q12: How do you test that divergence handling is correct?
**A:** Render scenes with mixed disk/bg rays and check images are identical to a CPU reference; divergence policy changes timing, never geometry results.

## Q13: What is the memory consequence of divergent control?
**A:** Divided warps issue divergent loads at different times, doubling the number of memory transactions for the same data - another hidden cost.

## Q14: What is the recommended lane count for testing?
**A:** Debug with warp-sized images (32 or 64 wide) so you can reason about every lane; scale up only after the killed-ray logic is proven.

## Q15: When does divergence become irrelevant?
**A:** When occupancy is high and scheduler slots idle anyway - divergence only matters once it starves issue or shows up as measured stalls.

## Q16: Explain the core idea behind branch divergence in the context of CUDA.
**A:** It is about expressing a parallel computation so the GPU scheduler can split it across many lightweight threads that execute the same instruction stream on different data.

## Q17: Why is branch divergence important for a raytracer kernel?
**A:** Because a raytracer runs the same integration work per pixel; understanding branch divergence tells you how to map pixels to threads and memory so the device stays saturated.

## Q18: What does the hardware do when a warp executes branch divergence?
**A:** All lanes in a warp execute the same instruction; branch divergence decides how that instruction interacts with memory banks, caches, and the per-SM execution resources.

## Q19: How does branch divergence affect occupancy?
**A:** Registry usage, shared memory, and work per thread set by branch divergence limit how many blocks fit per SM; higher occupancy hides latency but never guarantees speed.

## Q20: What are the common mistakes beginners make with branch divergence?
**A:** Launching too few threads, assuming serial ordering, ignoring memory layout, and treating device code as host code - all of which branch divergence must explicitly address.

## Q21: How would you validate your understanding of branch divergence?
**A:** Write a micro-benchmark that isolates the branch divergence behavior, measure with Nsight, and compare wall-clock time against a host reference implementation.

## Q22: Describe how branch divergence interacts with the memory hierarchy.
**A:** The branch divergence access pattern decides whether reads hit the L2/L1 caches and coalesce into few transactions; global latency is the usual bottleneck.

## Q23: When should you avoid depending on branch divergence at all?
**A:** When the problem is tiny or serial, because launch overhead and fixed resource costs of branch divergence outperform any marginal GPU parallelism.

## Q24: What is the relationship between branch divergence and numerical correctness?
**A:** Floating point order and precision choices in branch divergence can change results; determinism requires fixed accumulation order or careful atomic handling.

## Q25: Give a concrete example where branch divergence matters on a modern GPU.
**A:** On a 4090-class card, branch divergence governs how many concurrent warps can backlog global-memory stalls, directly capping the achieved instructions per second.

## Q26: What should a production engineer benchmark about branch divergence?
**A:** Achieved occupancy, memory throughput, divergence rate, register spills, and kernel duration - all surfaced by profiling branch divergence choices.

## Q27: How does branch divergence change when scaling to multiple GPUs?
**A:** Per-device branch divergence stays local, but you add host-side distribution, transfer overlap, and result collection for the overall frame.

## Q28: What kernel design decisions flow from branch divergence?
**A:** Block size, grid dimensions, whether to preload to shared memory, loop structure, and halting strategy for early ray termination.

## Q29: Compare the cost of getting branch divergence right early vs late.
**A:** Fixing branch divergence after the pipeline is written means rewriting kernels and re-validating images; deciding it first saves most of that rework.

## Q30: What documentation should exist for branch divergence?
**A:** A short design note stating the assumptions, measured numbers, and the validation test so future changes to branch divergence are reviewable.

## Q31: How do you explain branch divergence to a non-GPU colleague?
**A:** Analogize to a factory: branch divergence is the layout of workbenches and machines so thousands of identical jobs finish in parallel without colliding.

## Q32: What role does branch divergence play in frame-to-frame consistency?
**A:** Deterministic branch divergence means the same inputs give identical pixels every export, which matters when you render an animation one frame at a time.

## Q33: How would you get a 2x speedup out of branch divergence?
**A:** Often by improving memory reuse through branch divergence: precompute, cache, and process in tiles instead of touching global memory repeatedly.

## Q34: What are the limits of branch divergence on current hardware?
**A:** The finite number of threads per SM, shared memory bytes, registers, and memory bandwidth all cap branch divergence; reaching these limits signals a rendering ceiling.

## Q35: How do warps schedule work that depends on branch divergence?
**A:** The scheduler picks eligible warps whose data dependencies are resolved; poor branch divergence creates long stalls that starve the execution units.

## Q36: What is the minimal viable test for branch divergence?
**A:** Render one known image, profile kernel time, and confirm the result matches a reference before adding more complexity on top of branch divergence.

## Q37: How does branch divergence interact with numerical integrators?
**A:** Integrators advance each ray with feedback; branch divergence decides whether per-ray state stays in registers and how divergent the compute becomes.

## Q38: What is the mental model for branch divergence at the thread level?
**A:** One thread owns one unit of work; branch divergence defines how that work reads inputs, keeps intermediate state, writes output, and finishes when done.

## Q39: How do libraries and your own kernels divide responsibility for branch divergence?
**A:** Libraries like cuBLAS/cuFFT handle their own branch divergence; your kernels must match their launch dimensions and memory layouts for zero-copy interop.

## Q40: How do libraries and your own kernels divide responsibility for branch divergence - justify your answer with a concrete production example.
**A:** Libraries like cuBLAS/cuFFT handle their own branch divergence; your kernels must match their launch dimensions and memory layouts for zero-copy interop. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the mental model for branch divergence at the thread level - justify your answer with a concrete production example.
**A:** One thread owns one unit of work; branch divergence defines how that work reads inputs, keeps intermediate state, writes output, and finishes when done. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does branch divergence interact with numerical integrators - justify your answer with a concrete production example.
**A:** Integrators advance each ray with feedback; branch divergence decides whether per-ray state stays in registers and how divergent the compute becomes. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What is the minimal viable test for branch divergence - justify your answer with a concrete production example.
**A:** Render one known image, profile kernel time, and confirm the result matches a reference before adding more complexity on top of branch divergence. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How do warps schedule work that depends on branch divergence - justify your answer with a concrete production example.
**A:** The scheduler picks eligible warps whose data dependencies are resolved; poor branch divergence creates long stalls that starve the execution units. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What are the limits of branch divergence on current hardware - justify your answer with a concrete production example.
**A:** The finite number of threads per SM, shared memory bytes, registers, and memory bandwidth all cap branch divergence; reaching these limits signals a rendering ceiling. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How would you get a 2x speedup out of branch divergence - justify your answer with a concrete production example.
**A:** Often by improving memory reuse through branch divergence: precompute, cache, and process in tiles instead of touching global memory repeatedly. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What role does branch divergence play in frame-to-frame consistency - justify your answer with a concrete production example.
**A:** Deterministic branch divergence means the same inputs give identical pixels every export, which matters when you render an animation one frame at a time. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you explain branch divergence to a non-GPU colleague - justify your answer with a concrete production example.
**A:** Analogize to a factory: branch divergence is the layout of workbenches and machines so thousands of identical jobs finish in parallel without colliding. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What documentation should exist for branch divergence - justify your answer with a concrete production example.
**A:** A short design note stating the assumptions, measured numbers, and the validation test so future changes to branch divergence are reviewable. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: Compare the cost of getting branch divergence right early vs late - justify your answer with a concrete production example.
**A:** Fixing branch divergence after the pipeline is written means rewriting kernels and re-validating images; deciding it first saves most of that rework. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What kernel design decisions flow from branch divergence - justify your answer with a concrete production example.
**A:** Block size, grid dimensions, whether to preload to shared memory, loop structure, and halting strategy for early ray termination. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How does branch divergence change when scaling to multiple GPUs - justify your answer with a concrete production example.
**A:** Per-device branch divergence stays local, but you add host-side distribution, transfer overlap, and result collection for the overall frame. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What should a production engineer benchmark about branch divergence - justify your answer with a concrete production example.
**A:** Achieved occupancy, memory throughput, divergence rate, register spills, and kernel duration - all surfaced by profiling branch divergence choices. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: Give a concrete example where branch divergence matters on a modern GPU - justify your answer with a concrete production example.
**A:** On a 4090-class card, branch divergence governs how many concurrent warps can backlog global-memory stalls, directly capping the achieved instructions per second. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is the relationship between branch divergence and numerical correctness - justify your answer with a concrete production example.
**A:** Floating point order and precision choices in branch divergence can change results; determinism requires fixed accumulation order or careful atomic handling. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: When should you avoid depending on branch divergence at all - justify your answer with a concrete production example.
**A:** When the problem is tiny or serial, because launch overhead and fixed resource costs of branch divergence outperform any marginal GPU parallelism. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: Describe how branch divergence interacts with the memory hierarchy - justify your answer with a concrete production example.
**A:** The branch divergence access pattern decides whether reads hit the L2/L1 caches and coalesce into few transactions; global latency is the usual bottleneck. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: How would you validate your understanding of branch divergence - justify your answer with a concrete production example.
**A:** Write a micro-benchmark that isolates the branch divergence behavior, measure with Nsight, and compare wall-clock time against a host reference implementation. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What are the common mistakes beginners make with branch divergence - justify your answer with a concrete production example.
**A:** Launching too few threads, assuming serial ordering, ignoring memory layout, and treating device code as host code - all of which branch divergence must explicitly address. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: How does branch divergence affect occupancy - justify your answer with a concrete production example.
**A:** Registry usage, shared memory, and work per thread set by branch divergence limit how many blocks fit per SM; higher occupancy hides latency but never guarantees speed. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What does the hardware do when a warp executes branch divergence - justify your answer with a concrete production example.
**A:** All lanes in a warp execute the same instruction; branch divergence decides how that instruction interacts with memory banks, caches, and the per-SM execution resources. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why is branch divergence important for a raytracer kernel - justify your answer with a concrete production example.
**A:** Because a raytracer runs the same integration work per pixel; understanding branch divergence tells you how to map pixels to threads and memory so the device stays saturated. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: Explain the core idea behind branch divergence in the context of CUDA - justify your answer with a concrete production example.
**A:** It is about expressing a parallel computation so the GPU scheduler can split it across many lightweight threads that execute the same instruction stream on different data. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: Explain the core idea behind branch divergence in the context of CUDA - justify your answer with a concrete production example.
**A:** It is about expressing a parallel computation so the GPU scheduler can split it across many lightweight threads that execute the same instruction stream on different data. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why is branch divergence important for a raytracer kernel - justify your answer with a concrete production example.
**A:** Because a raytracer runs the same integration work per pixel; understanding branch divergence tells you how to map pixels to threads and memory so the device stays saturated. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What does the hardware do when a warp executes branch divergence - justify your answer with a concrete production example.
**A:** All lanes in a warp execute the same instruction; branch divergence decides how that instruction interacts with memory banks, caches, and the per-SM execution resources. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How does branch divergence affect occupancy - justify your answer with a concrete production example.
**A:** Registry usage, shared memory, and work per thread set by branch divergence limit how many blocks fit per SM; higher occupancy hides latency but never guarantees speed. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What are the common mistakes beginners make with branch divergence - justify your answer with a concrete production example.
**A:** Launching too few threads, assuming serial ordering, ignoring memory layout, and treating device code as host code - all of which branch divergence must explicitly address. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How would you validate your understanding of branch divergence - justify your answer with a concrete production example.
**A:** Write a micro-benchmark that isolates the branch divergence behavior, measure with Nsight, and compare wall-clock time against a host reference implementation. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: Describe how branch divergence interacts with the memory hierarchy - justify your answer with a concrete production example.
**A:** The branch divergence access pattern decides whether reads hit the L2/L1 caches and coalesce into few transactions; global latency is the usual bottleneck. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: When should you avoid depending on branch divergence at all - justify your answer with a concrete production example.
**A:** When the problem is tiny or serial, because launch overhead and fixed resource costs of branch divergence outperform any marginal GPU parallelism. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What is the relationship between branch divergence and numerical correctness - justify your answer with a concrete production example.
**A:** Floating point order and precision choices in branch divergence can change results; determinism requires fixed accumulation order or careful atomic handling. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: Give a concrete example where branch divergence matters on a modern GPU - justify your answer with a concrete production example.
**A:** On a 4090-class card, branch divergence governs how many concurrent warps can backlog global-memory stalls, directly capping the achieved instructions per second. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What should a production engineer benchmark about branch divergence - justify your answer with a concrete production example.
**A:** Achieved occupancy, memory throughput, divergence rate, register spills, and kernel duration - all surfaced by profiling branch divergence choices. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How does branch divergence change when scaling to multiple GPUs - justify your answer with a concrete production example.
**A:** Per-device branch divergence stays local, but you add host-side distribution, transfer overlap, and result collection for the overall frame. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What kernel design decisions flow from branch divergence - justify your answer with a concrete production example.
**A:** Block size, grid dimensions, whether to preload to shared memory, loop structure, and halting strategy for early ray termination. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: Compare the cost of getting branch divergence right early vs late - justify your answer with a concrete production example.
**A:** Fixing branch divergence after the pipeline is written means rewriting kernels and re-validating images; deciding it first saves most of that rework. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What documentation should exist for branch divergence - justify your answer with a concrete production example.
**A:** A short design note stating the assumptions, measured numbers, and the validation test so future changes to branch divergence are reviewable. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How do you explain branch divergence to a non-GPU colleague - justify your answer with a concrete production example.
**A:** Analogize to a factory: branch divergence is the layout of workbenches and machines so thousands of identical jobs finish in parallel without colliding. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What role does branch divergence play in frame-to-frame consistency - justify your answer with a concrete production example.
**A:** Deterministic branch divergence means the same inputs give identical pixels every export, which matters when you render an animation one frame at a time. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How would you get a 2x speedup out of branch divergence - justify your answer with a concrete production example.
**A:** Often by improving memory reuse through branch divergence: precompute, cache, and process in tiles instead of touching global memory repeatedly. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What are the limits of branch divergence on current hardware - justify your answer with a concrete production example.
**A:** The finite number of threads per SM, shared memory bytes, registers, and memory bandwidth all cap branch divergence; reaching these limits signals a rendering ceiling. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How do warps schedule work that depends on branch divergence - justify your answer with a concrete production example.
**A:** The scheduler picks eligible warps whose data dependencies are resolved; poor branch divergence creates long stalls that starve the execution units. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What is the minimal viable test for branch divergence - justify your answer with a concrete production example.
**A:** Render one known image, profile kernel time, and confirm the result matches a reference before adding more complexity on top of branch divergence. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How does branch divergence interact with numerical integrators - justify your answer with a concrete production example.
**A:** Integrators advance each ray with feedback; branch divergence decides whether per-ray state stays in registers and how divergent the compute becomes. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the mental model for branch divergence at the thread level - justify your answer with a concrete production example.
**A:** One thread owns one unit of work; branch divergence defines how that work reads inputs, keeps intermediate state, writes output, and finishes when done. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How do libraries and your own kernels divide responsibility for branch divergence - justify your answer with a concrete production example.
**A:** Libraries like cuBLAS/cuFFT handle their own branch divergence; your kernels must match their launch dimensions and memory layouts for zero-copy interop. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How do libraries and your own kernels divide responsibility for branch divergence - justify your answer with a concrete production example.
**A:** Libraries like cuBLAS/cuFFT handle their own branch divergence; your kernels must match their launch dimensions and memory layouts for zero-copy interop. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the mental model for branch divergence at the thread level - justify your answer with a concrete production example.
**A:** One thread owns one unit of work; branch divergence defines how that work reads inputs, keeps intermediate state, writes output, and finishes when done. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does branch divergence interact with numerical integrators - justify your answer with a concrete production example.
**A:** Integrators advance each ray with feedback; branch divergence decides whether per-ray state stays in registers and how divergent the compute becomes. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What is the minimal viable test for branch divergence - justify your answer with a concrete production example.
**A:** Render one known image, profile kernel time, and confirm the result matches a reference before adding more complexity on top of branch divergence. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How do warps schedule work that depends on branch divergence - justify your answer with a concrete production example.
**A:** The scheduler picks eligible warps whose data dependencies are resolved; poor branch divergence creates long stalls that starve the execution units. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What are the limits of branch divergence on current hardware - justify your answer with a concrete production example.
**A:** The finite number of threads per SM, shared memory bytes, registers, and memory bandwidth all cap branch divergence; reaching these limits signals a rendering ceiling. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How would you get a 2x speedup out of branch divergence - justify your answer with a concrete production example.
**A:** Often by improving memory reuse through branch divergence: precompute, cache, and process in tiles instead of touching global memory repeatedly. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What role does branch divergence play in frame-to-frame consistency - justify your answer with a concrete production example.
**A:** Deterministic branch divergence means the same inputs give identical pixels every export, which matters when you render an animation one frame at a time. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you explain branch divergence to a non-GPU colleague - justify your answer with a concrete production example.
**A:** Analogize to a factory: branch divergence is the layout of workbenches and machines so thousands of identical jobs finish in parallel without colliding. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What documentation should exist for branch divergence - justify your answer with a concrete production example.
**A:** A short design note stating the assumptions, measured numbers, and the validation test so future changes to branch divergence are reviewable. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: Compare the cost of getting branch divergence right early vs late - justify your answer with a concrete production example.
**A:** Fixing branch divergence after the pipeline is written means rewriting kernels and re-validating images; deciding it first saves most of that rework. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What kernel design decisions flow from branch divergence - justify your answer with a concrete production example.
**A:** Block size, grid dimensions, whether to preload to shared memory, loop structure, and halting strategy for early ray termination. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How does branch divergence change when scaling to multiple GPUs - justify your answer with a concrete production example.
**A:** Per-device branch divergence stays local, but you add host-side distribution, transfer overlap, and result collection for the overall frame. A concrete example: consistently applying branch divergence in code review and regression tests keeps the whole pipeline trustworthy.
