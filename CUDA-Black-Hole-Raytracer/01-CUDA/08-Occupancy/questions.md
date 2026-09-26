# Cuda — Occupancy Interview Questions and Answers

## Q1: What is occupancy?
**A:** The ratio of active warps to the maximum warps an SM can support; it is a proxy for how well latency can be hidden, not a direct measure of throughput.

## Q2: What limits occupancy?
**A:** Registers per thread, shared memory per block, block count per SM, and the fixed max warps/SM - the first two usually bind a raytracer.

## Q3: What is 'theoretical occupancy' formula?
**A:** occupancy = activeWarpsPerSM / maxWarpsPerSM; derived from launch config and resource limits via the occupancy API, always an upper bound.

## Q4: Why is high occupancy not always faster?
**A:** Too many resident warps can thrash cache and spill registers; sometimes fewer, better-scheduled warps with more registers per thread win.

## Q5: How does register usage per thread set occupancy?
**A:** The SM has a fixed register file (e.g., 65536 regs); if your kernel uses 40 regs/thread, only ~1600 threads fit - occupancy drops if you then launch 1024-thread blocks.

## Q6: How do you check spills?
**A:** Nsight Compute reports local memory (spill) traffic and registers used; ptxas '-v' or the compiler log also print counts at compile time.

## Q7: What is __launch_bounds__ and how does it control occupancy?
**A:** Declaring __launch_bounds__(256, 2) forces the compiler to cap registers so 2 blocks of 256 fit per SM, at the price of possible spills.

## Q8: How does shared memory per block reduce occupancy?
**A:** Blocks allocate smem at launch; the SM divides its shared pool by requested smem per block. Requesting 48KB/block leaves room for only ~3 blocks on a 227KB pool.

## Q9: What occupancy target is sensible for a raytracer?
**A:** 50-100% is the usual band; measure achieved occupancy and use it as a diagnostic - if achieved is far below theoretical, resources or scheduling are the cause.

## Q10: How do you use cudaOccupancyMaxActiveBlocksPerMultiprocessor?
**A:** int nb; cudaOccupancyMaxActiveBlocksPerMultiprocessor(&nb, kernel, blockSize, smem); then blocks = nb * deviceProps.multiProcessorCount.

## Q11: What is the difference between kernel-time occupancy and memory-time occupancy?
**A:** Nsight distinguishes occupancy during arithmetic vs during stalls; optimizing memory occupancy (overlap of loads) usually moves the needle more than raw active warps.

## Q12: How does the launch config density interplay with tail effects?
**A:** If the last partial block is small the SM may run one big unit late; launching many smaller blocks smooths the tail at slight scheduling cost.

## Q13: What effect does keeping per-ray state in registers have?
**A:** Geodesic state (x, p, redshift) is ~10-20 registers; that is cheap, so a tracer can afford high occupancy even with long per-ray loops.

## Q14: How do you pick the block size that maximizes occupancy?
**A:** For a known register count, an occupancy sweep (64..1024 threads) with cudaOccupancyMaxActiveBlocksPerMultiprocessor instantly reveals the plateau.

## Q15: What is the golden rule for occupancy tuning?
**A:** Decide rays, then measure achieved occupancy at three configs, then choose the fastest with identical output - never guess from theory alone.

## Q16: Explain the core idea behind occupancy in the context of CUDA.
**A:** It is about expressing a parallel computation so the GPU scheduler can split it across many lightweight threads that execute the same instruction stream on different data.

## Q17: Why is occupancy important for a raytracer kernel?
**A:** Because a raytracer runs the same integration work per pixel; understanding occupancy tells you how to map pixels to threads and memory so the device stays saturated.

## Q18: What does the hardware do when a warp executes occupancy?
**A:** All lanes in a warp execute the same instruction; occupancy decides how that instruction interacts with memory banks, caches, and the per-SM execution resources.

## Q19: How does occupancy affect occupancy?
**A:** Registry usage, shared memory, and work per thread set by occupancy limit how many blocks fit per SM; higher occupancy hides latency but never guarantees speed.

## Q20: What are the common mistakes beginners make with occupancy?
**A:** Launching too few threads, assuming serial ordering, ignoring memory layout, and treating device code as host code - all of which occupancy must explicitly address.

## Q21: How would you validate your understanding of occupancy?
**A:** Write a micro-benchmark that isolates the occupancy behavior, measure with Nsight, and compare wall-clock time against a host reference implementation.

## Q22: Describe how occupancy interacts with the memory hierarchy.
**A:** The occupancy access pattern decides whether reads hit the L2/L1 caches and coalesce into few transactions; global latency is the usual bottleneck.

## Q23: When should you avoid depending on occupancy at all?
**A:** When the problem is tiny or serial, because launch overhead and fixed resource costs of occupancy outperform any marginal GPU parallelism.

## Q24: What is the relationship between occupancy and numerical correctness?
**A:** Floating point order and precision choices in occupancy can change results; determinism requires fixed accumulation order or careful atomic handling.

## Q25: Give a concrete example where occupancy matters on a modern GPU.
**A:** On a 4090-class card, occupancy governs how many concurrent warps can backlog global-memory stalls, directly capping the achieved instructions per second.

## Q26: What should a production engineer benchmark about occupancy?
**A:** Achieved occupancy, memory throughput, divergence rate, register spills, and kernel duration - all surfaced by profiling occupancy choices.

## Q27: How does occupancy change when scaling to multiple GPUs?
**A:** Per-device occupancy stays local, but you add host-side distribution, transfer overlap, and result collection for the overall frame.

## Q28: What kernel design decisions flow from occupancy?
**A:** Block size, grid dimensions, whether to preload to shared memory, loop structure, and halting strategy for early ray termination.

## Q29: Compare the cost of getting occupancy right early vs late.
**A:** Fixing occupancy after the pipeline is written means rewriting kernels and re-validating images; deciding it first saves most of that rework.

## Q30: What documentation should exist for occupancy?
**A:** A short design note stating the assumptions, measured numbers, and the validation test so future changes to occupancy are reviewable.

## Q31: How do you explain occupancy to a non-GPU colleague?
**A:** Analogize to a factory: occupancy is the layout of workbenches and machines so thousands of identical jobs finish in parallel without colliding.

## Q32: What role does occupancy play in frame-to-frame consistency?
**A:** Deterministic occupancy means the same inputs give identical pixels every export, which matters when you render an animation one frame at a time.

## Q33: How would you get a 2x speedup out of occupancy?
**A:** Often by improving memory reuse through occupancy: precompute, cache, and process in tiles instead of touching global memory repeatedly.

## Q34: What are the limits of occupancy on current hardware?
**A:** The finite number of threads per SM, shared memory bytes, registers, and memory bandwidth all cap occupancy; reaching these limits signals a rendering ceiling.

## Q35: How do warps schedule work that depends on occupancy?
**A:** The scheduler picks eligible warps whose data dependencies are resolved; poor occupancy creates long stalls that starve the execution units.

## Q36: What is the minimal viable test for occupancy?
**A:** Render one known image, profile kernel time, and confirm the result matches a reference before adding more complexity on top of occupancy.

## Q37: How does occupancy interact with numerical integrators?
**A:** Integrators advance each ray with feedback; occupancy decides whether per-ray state stays in registers and how divergent the compute becomes.

## Q38: What is the mental model for occupancy at the thread level?
**A:** One thread owns one unit of work; occupancy defines how that work reads inputs, keeps intermediate state, writes output, and finishes when done.

## Q39: How do libraries and your own kernels divide responsibility for occupancy?
**A:** Libraries like cuBLAS/cuFFT handle their own occupancy; your kernels must match their launch dimensions and memory layouts for zero-copy interop.

## Q40: How do libraries and your own kernels divide responsibility for occupancy - justify your answer with a concrete production example.
**A:** Libraries like cuBLAS/cuFFT handle their own occupancy; your kernels must match their launch dimensions and memory layouts for zero-copy interop. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the mental model for occupancy at the thread level - justify your answer with a concrete production example.
**A:** One thread owns one unit of work; occupancy defines how that work reads inputs, keeps intermediate state, writes output, and finishes when done. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does occupancy interact with numerical integrators - justify your answer with a concrete production example.
**A:** Integrators advance each ray with feedback; occupancy decides whether per-ray state stays in registers and how divergent the compute becomes. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What is the minimal viable test for occupancy - justify your answer with a concrete production example.
**A:** Render one known image, profile kernel time, and confirm the result matches a reference before adding more complexity on top of occupancy. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How do warps schedule work that depends on occupancy - justify your answer with a concrete production example.
**A:** The scheduler picks eligible warps whose data dependencies are resolved; poor occupancy creates long stalls that starve the execution units. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What are the limits of occupancy on current hardware - justify your answer with a concrete production example.
**A:** The finite number of threads per SM, shared memory bytes, registers, and memory bandwidth all cap occupancy; reaching these limits signals a rendering ceiling. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How would you get a 2x speedup out of occupancy - justify your answer with a concrete production example.
**A:** Often by improving memory reuse through occupancy: precompute, cache, and process in tiles instead of touching global memory repeatedly. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What role does occupancy play in frame-to-frame consistency - justify your answer with a concrete production example.
**A:** Deterministic occupancy means the same inputs give identical pixels every export, which matters when you render an animation one frame at a time. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you explain occupancy to a non-GPU colleague - justify your answer with a concrete production example.
**A:** Analogize to a factory: occupancy is the layout of workbenches and machines so thousands of identical jobs finish in parallel without colliding. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What documentation should exist for occupancy - justify your answer with a concrete production example.
**A:** A short design note stating the assumptions, measured numbers, and the validation test so future changes to occupancy are reviewable. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: Compare the cost of getting occupancy right early vs late - justify your answer with a concrete production example.
**A:** Fixing occupancy after the pipeline is written means rewriting kernels and re-validating images; deciding it first saves most of that rework. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What kernel design decisions flow from occupancy - justify your answer with a concrete production example.
**A:** Block size, grid dimensions, whether to preload to shared memory, loop structure, and halting strategy for early ray termination. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How does occupancy change when scaling to multiple GPUs - justify your answer with a concrete production example.
**A:** Per-device occupancy stays local, but you add host-side distribution, transfer overlap, and result collection for the overall frame. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What should a production engineer benchmark about occupancy - justify your answer with a concrete production example.
**A:** Achieved occupancy, memory throughput, divergence rate, register spills, and kernel duration - all surfaced by profiling occupancy choices. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: Give a concrete example where occupancy matters on a modern GPU - justify your answer with a concrete production example.
**A:** On a 4090-class card, occupancy governs how many concurrent warps can backlog global-memory stalls, directly capping the achieved instructions per second. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is the relationship between occupancy and numerical correctness - justify your answer with a concrete production example.
**A:** Floating point order and precision choices in occupancy can change results; determinism requires fixed accumulation order or careful atomic handling. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: When should you avoid depending on occupancy at all - justify your answer with a concrete production example.
**A:** When the problem is tiny or serial, because launch overhead and fixed resource costs of occupancy outperform any marginal GPU parallelism. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: Describe how occupancy interacts with the memory hierarchy - justify your answer with a concrete production example.
**A:** The occupancy access pattern decides whether reads hit the L2/L1 caches and coalesce into few transactions; global latency is the usual bottleneck. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: How would you validate your understanding of occupancy - justify your answer with a concrete production example.
**A:** Write a micro-benchmark that isolates the occupancy behavior, measure with Nsight, and compare wall-clock time against a host reference implementation. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What are the common mistakes beginners make with occupancy - justify your answer with a concrete production example.
**A:** Launching too few threads, assuming serial ordering, ignoring memory layout, and treating device code as host code - all of which occupancy must explicitly address. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: How does occupancy affect occupancy - justify your answer with a concrete production example.
**A:** Registry usage, shared memory, and work per thread set by occupancy limit how many blocks fit per SM; higher occupancy hides latency but never guarantees speed. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What does the hardware do when a warp executes occupancy - justify your answer with a concrete production example.
**A:** All lanes in a warp execute the same instruction; occupancy decides how that instruction interacts with memory banks, caches, and the per-SM execution resources. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why is occupancy important for a raytracer kernel - justify your answer with a concrete production example.
**A:** Because a raytracer runs the same integration work per pixel; understanding occupancy tells you how to map pixels to threads and memory so the device stays saturated. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: Explain the core idea behind occupancy in the context of CUDA - justify your answer with a concrete production example.
**A:** It is about expressing a parallel computation so the GPU scheduler can split it across many lightweight threads that execute the same instruction stream on different data. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: Explain the core idea behind occupancy in the context of CUDA - justify your answer with a concrete production example.
**A:** It is about expressing a parallel computation so the GPU scheduler can split it across many lightweight threads that execute the same instruction stream on different data. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why is occupancy important for a raytracer kernel - justify your answer with a concrete production example.
**A:** Because a raytracer runs the same integration work per pixel; understanding occupancy tells you how to map pixels to threads and memory so the device stays saturated. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What does the hardware do when a warp executes occupancy - justify your answer with a concrete production example.
**A:** All lanes in a warp execute the same instruction; occupancy decides how that instruction interacts with memory banks, caches, and the per-SM execution resources. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How does occupancy affect occupancy - justify your answer with a concrete production example.
**A:** Registry usage, shared memory, and work per thread set by occupancy limit how many blocks fit per SM; higher occupancy hides latency but never guarantees speed. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What are the common mistakes beginners make with occupancy - justify your answer with a concrete production example.
**A:** Launching too few threads, assuming serial ordering, ignoring memory layout, and treating device code as host code - all of which occupancy must explicitly address. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How would you validate your understanding of occupancy - justify your answer with a concrete production example.
**A:** Write a micro-benchmark that isolates the occupancy behavior, measure with Nsight, and compare wall-clock time against a host reference implementation. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: Describe how occupancy interacts with the memory hierarchy - justify your answer with a concrete production example.
**A:** The occupancy access pattern decides whether reads hit the L2/L1 caches and coalesce into few transactions; global latency is the usual bottleneck. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: When should you avoid depending on occupancy at all - justify your answer with a concrete production example.
**A:** When the problem is tiny or serial, because launch overhead and fixed resource costs of occupancy outperform any marginal GPU parallelism. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What is the relationship between occupancy and numerical correctness - justify your answer with a concrete production example.
**A:** Floating point order and precision choices in occupancy can change results; determinism requires fixed accumulation order or careful atomic handling. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: Give a concrete example where occupancy matters on a modern GPU - justify your answer with a concrete production example.
**A:** On a 4090-class card, occupancy governs how many concurrent warps can backlog global-memory stalls, directly capping the achieved instructions per second. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What should a production engineer benchmark about occupancy - justify your answer with a concrete production example.
**A:** Achieved occupancy, memory throughput, divergence rate, register spills, and kernel duration - all surfaced by profiling occupancy choices. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How does occupancy change when scaling to multiple GPUs - justify your answer with a concrete production example.
**A:** Per-device occupancy stays local, but you add host-side distribution, transfer overlap, and result collection for the overall frame. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What kernel design decisions flow from occupancy - justify your answer with a concrete production example.
**A:** Block size, grid dimensions, whether to preload to shared memory, loop structure, and halting strategy for early ray termination. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: Compare the cost of getting occupancy right early vs late - justify your answer with a concrete production example.
**A:** Fixing occupancy after the pipeline is written means rewriting kernels and re-validating images; deciding it first saves most of that rework. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What documentation should exist for occupancy - justify your answer with a concrete production example.
**A:** A short design note stating the assumptions, measured numbers, and the validation test so future changes to occupancy are reviewable. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How do you explain occupancy to a non-GPU colleague - justify your answer with a concrete production example.
**A:** Analogize to a factory: occupancy is the layout of workbenches and machines so thousands of identical jobs finish in parallel without colliding. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What role does occupancy play in frame-to-frame consistency - justify your answer with a concrete production example.
**A:** Deterministic occupancy means the same inputs give identical pixels every export, which matters when you render an animation one frame at a time. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How would you get a 2x speedup out of occupancy - justify your answer with a concrete production example.
**A:** Often by improving memory reuse through occupancy: precompute, cache, and process in tiles instead of touching global memory repeatedly. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What are the limits of occupancy on current hardware - justify your answer with a concrete production example.
**A:** The finite number of threads per SM, shared memory bytes, registers, and memory bandwidth all cap occupancy; reaching these limits signals a rendering ceiling. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How do warps schedule work that depends on occupancy - justify your answer with a concrete production example.
**A:** The scheduler picks eligible warps whose data dependencies are resolved; poor occupancy creates long stalls that starve the execution units. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What is the minimal viable test for occupancy - justify your answer with a concrete production example.
**A:** Render one known image, profile kernel time, and confirm the result matches a reference before adding more complexity on top of occupancy. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How does occupancy interact with numerical integrators - justify your answer with a concrete production example.
**A:** Integrators advance each ray with feedback; occupancy decides whether per-ray state stays in registers and how divergent the compute becomes. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the mental model for occupancy at the thread level - justify your answer with a concrete production example.
**A:** One thread owns one unit of work; occupancy defines how that work reads inputs, keeps intermediate state, writes output, and finishes when done. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How do libraries and your own kernels divide responsibility for occupancy - justify your answer with a concrete production example.
**A:** Libraries like cuBLAS/cuFFT handle their own occupancy; your kernels must match their launch dimensions and memory layouts for zero-copy interop. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How do libraries and your own kernels divide responsibility for occupancy - justify your answer with a concrete production example.
**A:** Libraries like cuBLAS/cuFFT handle their own occupancy; your kernels must match their launch dimensions and memory layouts for zero-copy interop. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the mental model for occupancy at the thread level - justify your answer with a concrete production example.
**A:** One thread owns one unit of work; occupancy defines how that work reads inputs, keeps intermediate state, writes output, and finishes when done. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does occupancy interact with numerical integrators - justify your answer with a concrete production example.
**A:** Integrators advance each ray with feedback; occupancy decides whether per-ray state stays in registers and how divergent the compute becomes. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What is the minimal viable test for occupancy - justify your answer with a concrete production example.
**A:** Render one known image, profile kernel time, and confirm the result matches a reference before adding more complexity on top of occupancy. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How do warps schedule work that depends on occupancy - justify your answer with a concrete production example.
**A:** The scheduler picks eligible warps whose data dependencies are resolved; poor occupancy creates long stalls that starve the execution units. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What are the limits of occupancy on current hardware - justify your answer with a concrete production example.
**A:** The finite number of threads per SM, shared memory bytes, registers, and memory bandwidth all cap occupancy; reaching these limits signals a rendering ceiling. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How would you get a 2x speedup out of occupancy - justify your answer with a concrete production example.
**A:** Often by improving memory reuse through occupancy: precompute, cache, and process in tiles instead of touching global memory repeatedly. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What role does occupancy play in frame-to-frame consistency - justify your answer with a concrete production example.
**A:** Deterministic occupancy means the same inputs give identical pixels every export, which matters when you render an animation one frame at a time. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you explain occupancy to a non-GPU colleague - justify your answer with a concrete production example.
**A:** Analogize to a factory: occupancy is the layout of workbenches and machines so thousands of identical jobs finish in parallel without colliding. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What documentation should exist for occupancy - justify your answer with a concrete production example.
**A:** A short design note stating the assumptions, measured numbers, and the validation test so future changes to occupancy are reviewable. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: Compare the cost of getting occupancy right early vs late - justify your answer with a concrete production example.
**A:** Fixing occupancy after the pipeline is written means rewriting kernels and re-validating images; deciding it first saves most of that rework. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What kernel design decisions flow from occupancy - justify your answer with a concrete production example.
**A:** Block size, grid dimensions, whether to preload to shared memory, loop structure, and halting strategy for early ray termination. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How does occupancy change when scaling to multiple GPUs - justify your answer with a concrete production example.
**A:** Per-device occupancy stays local, but you add host-side distribution, transfer overlap, and result collection for the overall frame. A concrete example: consistently applying occupancy in code review and regression tests keeps the whole pipeline trustworthy.
