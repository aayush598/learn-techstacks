# Cuda — Thread Hierarchy Interview Questions and Answers

## Q1: What is the CUDA thread hierarchy?
**A:** Grid -> Blocks -> Threads. A grid is up to 2^31-1 blocks (x) and 65535 (y/z); each block has up to 1024 threads arranged in a 3D index; threads within a block share shared memory and can synchronize.

## Q2: Why is the 3D indexing useful?
**A:** It maps naturally onto image grids and voxel grids: image (x,y) pixels, (x,y,z) data cubes; the API gives you blockIdx and threadIdx for each axis.

## Q3: What is the maximum number of threads in a block?
**A:** 1024 on all current NVIDIA architectures (this limit is per block, not per SM). Practical block sizes are 128-256 for raytracing to balance occupancy and register pressure.

## Q4: What is the grid-stride loop pattern?
**A:** Instead of launching one thread per element, launch a fixed number of threads and have each loop, striding by the grid size: for (i = tid; i < N; i += gridStride). This decouples launch config from problem size.

## Q5: Why is launching one thread per pixel bad for very large images?
**A:** Pixel counts (millions) exceed practical grid limits and tie kernel config to image size; the grid-stride loop lets one launch handle any resolution and reuses blocks for better scheduling.

## Q6: How do you flatten a 2D image index?
**A:** int idx = blockIdx.x * blockDim.x + threadIdx.x; using a 1D grid over w*h pixels, or use 2D blockIdx with (x,y) directly mapped to columns and rows.

## Q7: What is a block's role in the hierarchy?
**A:** A block is the unit of scheduling on a streaming multiprocessor (SM) and the unit of inter-thread cooperation: shared memory and __syncthreads() are block-scoped.

## Q8: What happens when you launch more blocks than SMs?
**A:** The scheduler runs blocks until the SMs fill, then queues the rest; blocks retire and new ones start, keeping the machine busy as long as there is queued work.

## Q9: Can separate blocks synchronize?
**A:** No - blocks are independent by design; cross-block coordination requires atomic flags, global memory spin-waits, or multiple kernel launches (separate synchronization 'phases').

## Q10: How do you choose block dimensions for a raytracer kernel?
**A:** Prefer a multiple of 32 (warp size). Common choices: (256,1,1) or (16,16) tiles; benchmark occupancy and tail effects because ragged image sizes waste lanes.

## Q11: What is the total thread limit per grid?
**A:** Blocks per grid (x) up to 2^31-1, so the practical total is huge; the grid-stride loop means you rarely approach it anyway.

## Q12: What does threadIdx.x do in a kernel?
**A:** It identifies the thread within its block; combined with blockIdx and blockDim it produces a global id used to pick which ray to trace.

## Q13: Why does thread and block indexing affect performance?
**A:** IDs determine which pixels neighboring lanes in a warp process; keeping IDs spatially adjacent helps coalesced writes and cache-friendly reads of the same image rows.

## Q14: What is the relationship between block size and register usage?
**A:** Registers per thread times threads per block must fit the SM's register file; a big block with heavy per-thread state reduces the number of resident blocks.

## Q15: When is one thread per pixel appropriate despite limits?
**A:** When rays are extremely long-lived and registers/temps dominate, a 1:1 mapping with grid-stride over pixels is still flexible; the point is never to hard-wire the launch to a fixed resolution.

## Q16: Explain the core idea behind thread hierarchy in the context of CUDA.
**A:** It is about expressing a parallel computation so the GPU scheduler can split it across many lightweight threads that execute the same instruction stream on different data.

## Q17: Why is thread hierarchy important for a raytracer kernel?
**A:** Because a raytracer runs the same integration work per pixel; understanding thread hierarchy tells you how to map pixels to threads and memory so the device stays saturated.

## Q18: What does the hardware do when a warp executes thread hierarchy?
**A:** All lanes in a warp execute the same instruction; thread hierarchy decides how that instruction interacts with memory banks, caches, and the per-SM execution resources.

## Q19: How does thread hierarchy affect occupancy?
**A:** Registry usage, shared memory, and work per thread set by thread hierarchy limit how many blocks fit per SM; higher occupancy hides latency but never guarantees speed.

## Q20: What are the common mistakes beginners make with thread hierarchy?
**A:** Launching too few threads, assuming serial ordering, ignoring memory layout, and treating device code as host code - all of which thread hierarchy must explicitly address.

## Q21: How would you validate your understanding of thread hierarchy?
**A:** Write a micro-benchmark that isolates the thread hierarchy behavior, measure with Nsight, and compare wall-clock time against a host reference implementation.

## Q22: Describe how thread hierarchy interacts with the memory hierarchy.
**A:** The thread hierarchy access pattern decides whether reads hit the L2/L1 caches and coalesce into few transactions; global latency is the usual bottleneck.

## Q23: When should you avoid depending on thread hierarchy at all?
**A:** When the problem is tiny or serial, because launch overhead and fixed resource costs of thread hierarchy outperform any marginal GPU parallelism.

## Q24: What is the relationship between thread hierarchy and numerical correctness?
**A:** Floating point order and precision choices in thread hierarchy can change results; determinism requires fixed accumulation order or careful atomic handling.

## Q25: Give a concrete example where thread hierarchy matters on a modern GPU.
**A:** On a 4090-class card, thread hierarchy governs how many concurrent warps can backlog global-memory stalls, directly capping the achieved instructions per second.

## Q26: What should a production engineer benchmark about thread hierarchy?
**A:** Achieved occupancy, memory throughput, divergence rate, register spills, and kernel duration - all surfaced by profiling thread hierarchy choices.

## Q27: How does thread hierarchy change when scaling to multiple GPUs?
**A:** Per-device thread hierarchy stays local, but you add host-side distribution, transfer overlap, and result collection for the overall frame.

## Q28: What kernel design decisions flow from thread hierarchy?
**A:** Block size, grid dimensions, whether to preload to shared memory, loop structure, and halting strategy for early ray termination.

## Q29: Compare the cost of getting thread hierarchy right early vs late.
**A:** Fixing thread hierarchy after the pipeline is written means rewriting kernels and re-validating images; deciding it first saves most of that rework.

## Q30: What documentation should exist for thread hierarchy?
**A:** A short design note stating the assumptions, measured numbers, and the validation test so future changes to thread hierarchy are reviewable.

## Q31: How do you explain thread hierarchy to a non-GPU colleague?
**A:** Analogize to a factory: thread hierarchy is the layout of workbenches and machines so thousands of identical jobs finish in parallel without colliding.

## Q32: What role does thread hierarchy play in frame-to-frame consistency?
**A:** Deterministic thread hierarchy means the same inputs give identical pixels every export, which matters when you render an animation one frame at a time.

## Q33: How would you get a 2x speedup out of thread hierarchy?
**A:** Often by improving memory reuse through thread hierarchy: precompute, cache, and process in tiles instead of touching global memory repeatedly.

## Q34: What are the limits of thread hierarchy on current hardware?
**A:** The finite number of threads per SM, shared memory bytes, registers, and memory bandwidth all cap thread hierarchy; reaching these limits signals a rendering ceiling.

## Q35: How do warps schedule work that depends on thread hierarchy?
**A:** The scheduler picks eligible warps whose data dependencies are resolved; poor thread hierarchy creates long stalls that starve the execution units.

## Q36: What is the minimal viable test for thread hierarchy?
**A:** Render one known image, profile kernel time, and confirm the result matches a reference before adding more complexity on top of thread hierarchy.

## Q37: How does thread hierarchy interact with numerical integrators?
**A:** Integrators advance each ray with feedback; thread hierarchy decides whether per-ray state stays in registers and how divergent the compute becomes.

## Q38: What is the mental model for thread hierarchy at the thread level?
**A:** One thread owns one unit of work; thread hierarchy defines how that work reads inputs, keeps intermediate state, writes output, and finishes when done.

## Q39: How do libraries and your own kernels divide responsibility for thread hierarchy?
**A:** Libraries like cuBLAS/cuFFT handle their own thread hierarchy; your kernels must match their launch dimensions and memory layouts for zero-copy interop.

## Q40: How do libraries and your own kernels divide responsibility for thread hierarchy - justify your answer with a concrete production example.
**A:** Libraries like cuBLAS/cuFFT handle their own thread hierarchy; your kernels must match their launch dimensions and memory layouts for zero-copy interop. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the mental model for thread hierarchy at the thread level - justify your answer with a concrete production example.
**A:** One thread owns one unit of work; thread hierarchy defines how that work reads inputs, keeps intermediate state, writes output, and finishes when done. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does thread hierarchy interact with numerical integrators - justify your answer with a concrete production example.
**A:** Integrators advance each ray with feedback; thread hierarchy decides whether per-ray state stays in registers and how divergent the compute becomes. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What is the minimal viable test for thread hierarchy - justify your answer with a concrete production example.
**A:** Render one known image, profile kernel time, and confirm the result matches a reference before adding more complexity on top of thread hierarchy. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How do warps schedule work that depends on thread hierarchy - justify your answer with a concrete production example.
**A:** The scheduler picks eligible warps whose data dependencies are resolved; poor thread hierarchy creates long stalls that starve the execution units. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What are the limits of thread hierarchy on current hardware - justify your answer with a concrete production example.
**A:** The finite number of threads per SM, shared memory bytes, registers, and memory bandwidth all cap thread hierarchy; reaching these limits signals a rendering ceiling. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How would you get a 2x speedup out of thread hierarchy - justify your answer with a concrete production example.
**A:** Often by improving memory reuse through thread hierarchy: precompute, cache, and process in tiles instead of touching global memory repeatedly. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What role does thread hierarchy play in frame-to-frame consistency - justify your answer with a concrete production example.
**A:** Deterministic thread hierarchy means the same inputs give identical pixels every export, which matters when you render an animation one frame at a time. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you explain thread hierarchy to a non-GPU colleague - justify your answer with a concrete production example.
**A:** Analogize to a factory: thread hierarchy is the layout of workbenches and machines so thousands of identical jobs finish in parallel without colliding. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What documentation should exist for thread hierarchy - justify your answer with a concrete production example.
**A:** A short design note stating the assumptions, measured numbers, and the validation test so future changes to thread hierarchy are reviewable. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: Compare the cost of getting thread hierarchy right early vs late - justify your answer with a concrete production example.
**A:** Fixing thread hierarchy after the pipeline is written means rewriting kernels and re-validating images; deciding it first saves most of that rework. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What kernel design decisions flow from thread hierarchy - justify your answer with a concrete production example.
**A:** Block size, grid dimensions, whether to preload to shared memory, loop structure, and halting strategy for early ray termination. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How does thread hierarchy change when scaling to multiple GPUs - justify your answer with a concrete production example.
**A:** Per-device thread hierarchy stays local, but you add host-side distribution, transfer overlap, and result collection for the overall frame. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What should a production engineer benchmark about thread hierarchy - justify your answer with a concrete production example.
**A:** Achieved occupancy, memory throughput, divergence rate, register spills, and kernel duration - all surfaced by profiling thread hierarchy choices. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: Give a concrete example where thread hierarchy matters on a modern GPU - justify your answer with a concrete production example.
**A:** On a 4090-class card, thread hierarchy governs how many concurrent warps can backlog global-memory stalls, directly capping the achieved instructions per second. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is the relationship between thread hierarchy and numerical correctness - justify your answer with a concrete production example.
**A:** Floating point order and precision choices in thread hierarchy can change results; determinism requires fixed accumulation order or careful atomic handling. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: When should you avoid depending on thread hierarchy at all - justify your answer with a concrete production example.
**A:** When the problem is tiny or serial, because launch overhead and fixed resource costs of thread hierarchy outperform any marginal GPU parallelism. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: Describe how thread hierarchy interacts with the memory hierarchy - justify your answer with a concrete production example.
**A:** The thread hierarchy access pattern decides whether reads hit the L2/L1 caches and coalesce into few transactions; global latency is the usual bottleneck. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: How would you validate your understanding of thread hierarchy - justify your answer with a concrete production example.
**A:** Write a micro-benchmark that isolates the thread hierarchy behavior, measure with Nsight, and compare wall-clock time against a host reference implementation. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What are the common mistakes beginners make with thread hierarchy - justify your answer with a concrete production example.
**A:** Launching too few threads, assuming serial ordering, ignoring memory layout, and treating device code as host code - all of which thread hierarchy must explicitly address. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: How does thread hierarchy affect occupancy - justify your answer with a concrete production example.
**A:** Registry usage, shared memory, and work per thread set by thread hierarchy limit how many blocks fit per SM; higher occupancy hides latency but never guarantees speed. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What does the hardware do when a warp executes thread hierarchy - justify your answer with a concrete production example.
**A:** All lanes in a warp execute the same instruction; thread hierarchy decides how that instruction interacts with memory banks, caches, and the per-SM execution resources. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why is thread hierarchy important for a raytracer kernel - justify your answer with a concrete production example.
**A:** Because a raytracer runs the same integration work per pixel; understanding thread hierarchy tells you how to map pixels to threads and memory so the device stays saturated. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: Explain the core idea behind thread hierarchy in the context of CUDA - justify your answer with a concrete production example.
**A:** It is about expressing a parallel computation so the GPU scheduler can split it across many lightweight threads that execute the same instruction stream on different data. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: Explain the core idea behind thread hierarchy in the context of CUDA - justify your answer with a concrete production example.
**A:** It is about expressing a parallel computation so the GPU scheduler can split it across many lightweight threads that execute the same instruction stream on different data. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why is thread hierarchy important for a raytracer kernel - justify your answer with a concrete production example.
**A:** Because a raytracer runs the same integration work per pixel; understanding thread hierarchy tells you how to map pixels to threads and memory so the device stays saturated. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What does the hardware do when a warp executes thread hierarchy - justify your answer with a concrete production example.
**A:** All lanes in a warp execute the same instruction; thread hierarchy decides how that instruction interacts with memory banks, caches, and the per-SM execution resources. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How does thread hierarchy affect occupancy - justify your answer with a concrete production example.
**A:** Registry usage, shared memory, and work per thread set by thread hierarchy limit how many blocks fit per SM; higher occupancy hides latency but never guarantees speed. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What are the common mistakes beginners make with thread hierarchy - justify your answer with a concrete production example.
**A:** Launching too few threads, assuming serial ordering, ignoring memory layout, and treating device code as host code - all of which thread hierarchy must explicitly address. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How would you validate your understanding of thread hierarchy - justify your answer with a concrete production example.
**A:** Write a micro-benchmark that isolates the thread hierarchy behavior, measure with Nsight, and compare wall-clock time against a host reference implementation. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: Describe how thread hierarchy interacts with the memory hierarchy - justify your answer with a concrete production example.
**A:** The thread hierarchy access pattern decides whether reads hit the L2/L1 caches and coalesce into few transactions; global latency is the usual bottleneck. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: When should you avoid depending on thread hierarchy at all - justify your answer with a concrete production example.
**A:** When the problem is tiny or serial, because launch overhead and fixed resource costs of thread hierarchy outperform any marginal GPU parallelism. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What is the relationship between thread hierarchy and numerical correctness - justify your answer with a concrete production example.
**A:** Floating point order and precision choices in thread hierarchy can change results; determinism requires fixed accumulation order or careful atomic handling. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: Give a concrete example where thread hierarchy matters on a modern GPU - justify your answer with a concrete production example.
**A:** On a 4090-class card, thread hierarchy governs how many concurrent warps can backlog global-memory stalls, directly capping the achieved instructions per second. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What should a production engineer benchmark about thread hierarchy - justify your answer with a concrete production example.
**A:** Achieved occupancy, memory throughput, divergence rate, register spills, and kernel duration - all surfaced by profiling thread hierarchy choices. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How does thread hierarchy change when scaling to multiple GPUs - justify your answer with a concrete production example.
**A:** Per-device thread hierarchy stays local, but you add host-side distribution, transfer overlap, and result collection for the overall frame. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What kernel design decisions flow from thread hierarchy - justify your answer with a concrete production example.
**A:** Block size, grid dimensions, whether to preload to shared memory, loop structure, and halting strategy for early ray termination. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: Compare the cost of getting thread hierarchy right early vs late - justify your answer with a concrete production example.
**A:** Fixing thread hierarchy after the pipeline is written means rewriting kernels and re-validating images; deciding it first saves most of that rework. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What documentation should exist for thread hierarchy - justify your answer with a concrete production example.
**A:** A short design note stating the assumptions, measured numbers, and the validation test so future changes to thread hierarchy are reviewable. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How do you explain thread hierarchy to a non-GPU colleague - justify your answer with a concrete production example.
**A:** Analogize to a factory: thread hierarchy is the layout of workbenches and machines so thousands of identical jobs finish in parallel without colliding. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What role does thread hierarchy play in frame-to-frame consistency - justify your answer with a concrete production example.
**A:** Deterministic thread hierarchy means the same inputs give identical pixels every export, which matters when you render an animation one frame at a time. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How would you get a 2x speedup out of thread hierarchy - justify your answer with a concrete production example.
**A:** Often by improving memory reuse through thread hierarchy: precompute, cache, and process in tiles instead of touching global memory repeatedly. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What are the limits of thread hierarchy on current hardware - justify your answer with a concrete production example.
**A:** The finite number of threads per SM, shared memory bytes, registers, and memory bandwidth all cap thread hierarchy; reaching these limits signals a rendering ceiling. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How do warps schedule work that depends on thread hierarchy - justify your answer with a concrete production example.
**A:** The scheduler picks eligible warps whose data dependencies are resolved; poor thread hierarchy creates long stalls that starve the execution units. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What is the minimal viable test for thread hierarchy - justify your answer with a concrete production example.
**A:** Render one known image, profile kernel time, and confirm the result matches a reference before adding more complexity on top of thread hierarchy. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How does thread hierarchy interact with numerical integrators - justify your answer with a concrete production example.
**A:** Integrators advance each ray with feedback; thread hierarchy decides whether per-ray state stays in registers and how divergent the compute becomes. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the mental model for thread hierarchy at the thread level - justify your answer with a concrete production example.
**A:** One thread owns one unit of work; thread hierarchy defines how that work reads inputs, keeps intermediate state, writes output, and finishes when done. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How do libraries and your own kernels divide responsibility for thread hierarchy - justify your answer with a concrete production example.
**A:** Libraries like cuBLAS/cuFFT handle their own thread hierarchy; your kernels must match their launch dimensions and memory layouts for zero-copy interop. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How do libraries and your own kernels divide responsibility for thread hierarchy - justify your answer with a concrete production example.
**A:** Libraries like cuBLAS/cuFFT handle their own thread hierarchy; your kernels must match their launch dimensions and memory layouts for zero-copy interop. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the mental model for thread hierarchy at the thread level - justify your answer with a concrete production example.
**A:** One thread owns one unit of work; thread hierarchy defines how that work reads inputs, keeps intermediate state, writes output, and finishes when done. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does thread hierarchy interact with numerical integrators - justify your answer with a concrete production example.
**A:** Integrators advance each ray with feedback; thread hierarchy decides whether per-ray state stays in registers and how divergent the compute becomes. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What is the minimal viable test for thread hierarchy - justify your answer with a concrete production example.
**A:** Render one known image, profile kernel time, and confirm the result matches a reference before adding more complexity on top of thread hierarchy. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How do warps schedule work that depends on thread hierarchy - justify your answer with a concrete production example.
**A:** The scheduler picks eligible warps whose data dependencies are resolved; poor thread hierarchy creates long stalls that starve the execution units. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What are the limits of thread hierarchy on current hardware - justify your answer with a concrete production example.
**A:** The finite number of threads per SM, shared memory bytes, registers, and memory bandwidth all cap thread hierarchy; reaching these limits signals a rendering ceiling. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How would you get a 2x speedup out of thread hierarchy - justify your answer with a concrete production example.
**A:** Often by improving memory reuse through thread hierarchy: precompute, cache, and process in tiles instead of touching global memory repeatedly. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What role does thread hierarchy play in frame-to-frame consistency - justify your answer with a concrete production example.
**A:** Deterministic thread hierarchy means the same inputs give identical pixels every export, which matters when you render an animation one frame at a time. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you explain thread hierarchy to a non-GPU colleague - justify your answer with a concrete production example.
**A:** Analogize to a factory: thread hierarchy is the layout of workbenches and machines so thousands of identical jobs finish in parallel without colliding. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What documentation should exist for thread hierarchy - justify your answer with a concrete production example.
**A:** A short design note stating the assumptions, measured numbers, and the validation test so future changes to thread hierarchy are reviewable. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: Compare the cost of getting thread hierarchy right early vs late - justify your answer with a concrete production example.
**A:** Fixing thread hierarchy after the pipeline is written means rewriting kernels and re-validating images; deciding it first saves most of that rework. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What kernel design decisions flow from thread hierarchy - justify your answer with a concrete production example.
**A:** Block size, grid dimensions, whether to preload to shared memory, loop structure, and halting strategy for early ray termination. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How does thread hierarchy change when scaling to multiple GPUs - justify your answer with a concrete production example.
**A:** Per-device thread hierarchy stays local, but you add host-side distribution, transfer overlap, and result collection for the overall frame. A concrete example: consistently applying thread hierarchy in code review and regression tests keeps the whole pipeline trustworthy.
