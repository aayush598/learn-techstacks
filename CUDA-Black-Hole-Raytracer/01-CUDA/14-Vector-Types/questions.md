# Cuda — Vector Types Interview Questions and Answers

## Q1: What are CUDA vector types?
**A:** Derived types like float2, float3, float4, dim3, and storage-backed structs that pack several scalars and enable aligned, vectorized memory access and SIMT-friendliness.

## Q2: Why use float4 for color/position?
**A:** A float4 is 16 bytes, aligning with 128-bit memory transactions and cache lines; writing pixels as float4 batches four writes into fewer transactions.

## Q3: How big is the throughput difference for aligned loads?
**A:** Loading float4 reduces the number of load instructions and transactions 4x versus scalar float, dramatically improving memory-bound kernels like ray-sample interpolation.

## Q4: What is the alignment requirement of float4?
**A:** 16-byte aligned; allocate with cudaMalloc (which aligns) and keep struct offsets on 16-byte boundaries or the compiler inserts slow fixups or errors.

## Q5: What are the swizzle/exponent operations on vector types?
**A:** Access fields as .x .y .z .w (or .r .g .b .a); pieces like float2 have no automatic packing - grouping is up to you so bundling state keeps memory local.

## Q6: When is a plain struct better than a vector type?
**A:** For heterogeneous state (position, momentum, redshift, flags), a custom struct gives one register-cache-friendly blob; vector types shine for homogeneous homogeneous packs (positions, colors).

## Q7: What is the difference between float3 and float4 storage?
**A:** float3 is 12 bytes (misaligned for some operations and padded to 16 in kernels); prefer float4 for output and align your arrays to 16.

## Q8: How do vector types interact with coalescing?
**A:** Averaging over lanes of a warp, a float4 stride consecutive addresses: each lane fetches 16B, total 512B per warp in one or two transactions - the ideal pattern.

## Q9: What are half-precision types?
**A:** half and half2 pack 16-bit FP (with half2 for 32-bit access); mainly for storage of values like sky textures where 11 mantissa bits suffice, not for geodesic integration.

## Q10: What is dim3 used for?
**A:** The 3D launch configuration: dim3 grid(64,64), dim3 block(16,16); it conveys blockIdx/threadIdx shapes for image or voxel kernels.

## Q11: How do you convert a vector type to colors in the image buffer?
**A:** A float4 pixel (r,g,b,a) writes directly; the import kernel then passes these to the tone-mapping kernel as float4 buffers end to end.

## Q12: What memory-buttons do vector types hide?
**A:** Intrinsics like __ldg (read-only cache) and the vector loads (v4) are compiler-generated; profile first, then consider __restrict and padding.

## Q13: How do you make a vector-poC struct for the geodesic state?
**A:** Store state as float4 (t, r, theta, phi) and float4 (pt, pr, ptH, pphi) - the whole state fits two 16-byte variables that stay in registers.

## Q14: What is the alignment rule of thumb?
**A:** Per-array stride must be a multiple of the natural alignment of the largest element; keep every stride at least 16 bytes and avoid odd padding in images.

## Q15: When is it wrong to use vector types?
**A:** When each lane stores a different quantity (a locate-equality where float4 wastes 3 lanes) - use scalar types then and rely on the compiler to assemble warps.

## Q16: Explain the core idea behind vector types in the context of CUDA.
**A:** It is about expressing a parallel computation so the GPU scheduler can split it across many lightweight threads that execute the same instruction stream on different data.

## Q17: Why is vector types important for a raytracer kernel?
**A:** Because a raytracer runs the same integration work per pixel; understanding vector types tells you how to map pixels to threads and memory so the device stays saturated.

## Q18: What does the hardware do when a warp executes vector types?
**A:** All lanes in a warp execute the same instruction; vector types decides how that instruction interacts with memory banks, caches, and the per-SM execution resources.

## Q19: How does vector types affect occupancy?
**A:** Registry usage, shared memory, and work per thread set by vector types limit how many blocks fit per SM; higher occupancy hides latency but never guarantees speed.

## Q20: What are the common mistakes beginners make with vector types?
**A:** Launching too few threads, assuming serial ordering, ignoring memory layout, and treating device code as host code - all of which vector types must explicitly address.

## Q21: How would you validate your understanding of vector types?
**A:** Write a micro-benchmark that isolates the vector types behavior, measure with Nsight, and compare wall-clock time against a host reference implementation.

## Q22: Describe how vector types interacts with the memory hierarchy.
**A:** The vector types access pattern decides whether reads hit the L2/L1 caches and coalesce into few transactions; global latency is the usual bottleneck.

## Q23: When should you avoid depending on vector types at all?
**A:** When the problem is tiny or serial, because launch overhead and fixed resource costs of vector types outperform any marginal GPU parallelism.

## Q24: What is the relationship between vector types and numerical correctness?
**A:** Floating point order and precision choices in vector types can change results; determinism requires fixed accumulation order or careful atomic handling.

## Q25: Give a concrete example where vector types matters on a modern GPU.
**A:** On a 4090-class card, vector types governs how many concurrent warps can backlog global-memory stalls, directly capping the achieved instructions per second.

## Q26: What should a production engineer benchmark about vector types?
**A:** Achieved occupancy, memory throughput, divergence rate, register spills, and kernel duration - all surfaced by profiling vector types choices.

## Q27: How does vector types change when scaling to multiple GPUs?
**A:** Per-device vector types stays local, but you add host-side distribution, transfer overlap, and result collection for the overall frame.

## Q28: What kernel design decisions flow from vector types?
**A:** Block size, grid dimensions, whether to preload to shared memory, loop structure, and halting strategy for early ray termination.

## Q29: Compare the cost of getting vector types right early vs late.
**A:** Fixing vector types after the pipeline is written means rewriting kernels and re-validating images; deciding it first saves most of that rework.

## Q30: What documentation should exist for vector types?
**A:** A short design note stating the assumptions, measured numbers, and the validation test so future changes to vector types are reviewable.

## Q31: How do you explain vector types to a non-GPU colleague?
**A:** Analogize to a factory: vector types is the layout of workbenches and machines so thousands of identical jobs finish in parallel without colliding.

## Q32: What role does vector types play in frame-to-frame consistency?
**A:** Deterministic vector types means the same inputs give identical pixels every export, which matters when you render an animation one frame at a time.

## Q33: How would you get a 2x speedup out of vector types?
**A:** Often by improving memory reuse through vector types: precompute, cache, and process in tiles instead of touching global memory repeatedly.

## Q34: What are the limits of vector types on current hardware?
**A:** The finite number of threads per SM, shared memory bytes, registers, and memory bandwidth all cap vector types; reaching these limits signals a rendering ceiling.

## Q35: How do warps schedule work that depends on vector types?
**A:** The scheduler picks eligible warps whose data dependencies are resolved; poor vector types creates long stalls that starve the execution units.

## Q36: What is the minimal viable test for vector types?
**A:** Render one known image, profile kernel time, and confirm the result matches a reference before adding more complexity on top of vector types.

## Q37: How does vector types interact with numerical integrators?
**A:** Integrators advance each ray with feedback; vector types decides whether per-ray state stays in registers and how divergent the compute becomes.

## Q38: What is the mental model for vector types at the thread level?
**A:** One thread owns one unit of work; vector types defines how that work reads inputs, keeps intermediate state, writes output, and finishes when done.

## Q39: How do libraries and your own kernels divide responsibility for vector types?
**A:** Libraries like cuBLAS/cuFFT handle their own vector types; your kernels must match their launch dimensions and memory layouts for zero-copy interop.

## Q40: How do libraries and your own kernels divide responsibility for vector types - justify your answer with a concrete production example.
**A:** Libraries like cuBLAS/cuFFT handle their own vector types; your kernels must match their launch dimensions and memory layouts for zero-copy interop. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What is the mental model for vector types at the thread level - justify your answer with a concrete production example.
**A:** One thread owns one unit of work; vector types defines how that work reads inputs, keeps intermediate state, writes output, and finishes when done. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does vector types interact with numerical integrators - justify your answer with a concrete production example.
**A:** Integrators advance each ray with feedback; vector types decides whether per-ray state stays in registers and how divergent the compute becomes. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What is the minimal viable test for vector types - justify your answer with a concrete production example.
**A:** Render one known image, profile kernel time, and confirm the result matches a reference before adding more complexity on top of vector types. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How do warps schedule work that depends on vector types - justify your answer with a concrete production example.
**A:** The scheduler picks eligible warps whose data dependencies are resolved; poor vector types creates long stalls that starve the execution units. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What are the limits of vector types on current hardware - justify your answer with a concrete production example.
**A:** The finite number of threads per SM, shared memory bytes, registers, and memory bandwidth all cap vector types; reaching these limits signals a rendering ceiling. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How would you get a 2x speedup out of vector types - justify your answer with a concrete production example.
**A:** Often by improving memory reuse through vector types: precompute, cache, and process in tiles instead of touching global memory repeatedly. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What role does vector types play in frame-to-frame consistency - justify your answer with a concrete production example.
**A:** Deterministic vector types means the same inputs give identical pixels every export, which matters when you render an animation one frame at a time. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you explain vector types to a non-GPU colleague - justify your answer with a concrete production example.
**A:** Analogize to a factory: vector types is the layout of workbenches and machines so thousands of identical jobs finish in parallel without colliding. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What documentation should exist for vector types - justify your answer with a concrete production example.
**A:** A short design note stating the assumptions, measured numbers, and the validation test so future changes to vector types are reviewable. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: Compare the cost of getting vector types right early vs late - justify your answer with a concrete production example.
**A:** Fixing vector types after the pipeline is written means rewriting kernels and re-validating images; deciding it first saves most of that rework. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What kernel design decisions flow from vector types - justify your answer with a concrete production example.
**A:** Block size, grid dimensions, whether to preload to shared memory, loop structure, and halting strategy for early ray termination. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How does vector types change when scaling to multiple GPUs - justify your answer with a concrete production example.
**A:** Per-device vector types stays local, but you add host-side distribution, transfer overlap, and result collection for the overall frame. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What should a production engineer benchmark about vector types - justify your answer with a concrete production example.
**A:** Achieved occupancy, memory throughput, divergence rate, register spills, and kernel duration - all surfaced by profiling vector types choices. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: Give a concrete example where vector types matters on a modern GPU - justify your answer with a concrete production example.
**A:** On a 4090-class card, vector types governs how many concurrent warps can backlog global-memory stalls, directly capping the achieved instructions per second. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is the relationship between vector types and numerical correctness - justify your answer with a concrete production example.
**A:** Floating point order and precision choices in vector types can change results; determinism requires fixed accumulation order or careful atomic handling. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: When should you avoid depending on vector types at all - justify your answer with a concrete production example.
**A:** When the problem is tiny or serial, because launch overhead and fixed resource costs of vector types outperform any marginal GPU parallelism. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: Describe how vector types interacts with the memory hierarchy - justify your answer with a concrete production example.
**A:** The vector types access pattern decides whether reads hit the L2/L1 caches and coalesce into few transactions; global latency is the usual bottleneck. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: How would you validate your understanding of vector types - justify your answer with a concrete production example.
**A:** Write a micro-benchmark that isolates the vector types behavior, measure with Nsight, and compare wall-clock time against a host reference implementation. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What are the common mistakes beginners make with vector types - justify your answer with a concrete production example.
**A:** Launching too few threads, assuming serial ordering, ignoring memory layout, and treating device code as host code - all of which vector types must explicitly address. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: How does vector types affect occupancy - justify your answer with a concrete production example.
**A:** Registry usage, shared memory, and work per thread set by vector types limit how many blocks fit per SM; higher occupancy hides latency but never guarantees speed. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What does the hardware do when a warp executes vector types - justify your answer with a concrete production example.
**A:** All lanes in a warp execute the same instruction; vector types decides how that instruction interacts with memory banks, caches, and the per-SM execution resources. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why is vector types important for a raytracer kernel - justify your answer with a concrete production example.
**A:** Because a raytracer runs the same integration work per pixel; understanding vector types tells you how to map pixels to threads and memory so the device stays saturated. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: Explain the core idea behind vector types in the context of CUDA - justify your answer with a concrete production example.
**A:** It is about expressing a parallel computation so the GPU scheduler can split it across many lightweight threads that execute the same instruction stream on different data. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: Explain the core idea behind vector types in the context of CUDA - justify your answer with a concrete production example.
**A:** It is about expressing a parallel computation so the GPU scheduler can split it across many lightweight threads that execute the same instruction stream on different data. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why is vector types important for a raytracer kernel - justify your answer with a concrete production example.
**A:** Because a raytracer runs the same integration work per pixel; understanding vector types tells you how to map pixels to threads and memory so the device stays saturated. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What does the hardware do when a warp executes vector types - justify your answer with a concrete production example.
**A:** All lanes in a warp execute the same instruction; vector types decides how that instruction interacts with memory banks, caches, and the per-SM execution resources. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How does vector types affect occupancy - justify your answer with a concrete production example.
**A:** Registry usage, shared memory, and work per thread set by vector types limit how many blocks fit per SM; higher occupancy hides latency but never guarantees speed. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What are the common mistakes beginners make with vector types - justify your answer with a concrete production example.
**A:** Launching too few threads, assuming serial ordering, ignoring memory layout, and treating device code as host code - all of which vector types must explicitly address. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How would you validate your understanding of vector types - justify your answer with a concrete production example.
**A:** Write a micro-benchmark that isolates the vector types behavior, measure with Nsight, and compare wall-clock time against a host reference implementation. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: Describe how vector types interacts with the memory hierarchy - justify your answer with a concrete production example.
**A:** The vector types access pattern decides whether reads hit the L2/L1 caches and coalesce into few transactions; global latency is the usual bottleneck. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: When should you avoid depending on vector types at all - justify your answer with a concrete production example.
**A:** When the problem is tiny or serial, because launch overhead and fixed resource costs of vector types outperform any marginal GPU parallelism. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What is the relationship between vector types and numerical correctness - justify your answer with a concrete production example.
**A:** Floating point order and precision choices in vector types can change results; determinism requires fixed accumulation order or careful atomic handling. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: Give a concrete example where vector types matters on a modern GPU - justify your answer with a concrete production example.
**A:** On a 4090-class card, vector types governs how many concurrent warps can backlog global-memory stalls, directly capping the achieved instructions per second. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What should a production engineer benchmark about vector types - justify your answer with a concrete production example.
**A:** Achieved occupancy, memory throughput, divergence rate, register spills, and kernel duration - all surfaced by profiling vector types choices. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How does vector types change when scaling to multiple GPUs - justify your answer with a concrete production example.
**A:** Per-device vector types stays local, but you add host-side distribution, transfer overlap, and result collection for the overall frame. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What kernel design decisions flow from vector types - justify your answer with a concrete production example.
**A:** Block size, grid dimensions, whether to preload to shared memory, loop structure, and halting strategy for early ray termination. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: Compare the cost of getting vector types right early vs late - justify your answer with a concrete production example.
**A:** Fixing vector types after the pipeline is written means rewriting kernels and re-validating images; deciding it first saves most of that rework. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What documentation should exist for vector types - justify your answer with a concrete production example.
**A:** A short design note stating the assumptions, measured numbers, and the validation test so future changes to vector types are reviewable. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How do you explain vector types to a non-GPU colleague - justify your answer with a concrete production example.
**A:** Analogize to a factory: vector types is the layout of workbenches and machines so thousands of identical jobs finish in parallel without colliding. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What role does vector types play in frame-to-frame consistency - justify your answer with a concrete production example.
**A:** Deterministic vector types means the same inputs give identical pixels every export, which matters when you render an animation one frame at a time. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How would you get a 2x speedup out of vector types - justify your answer with a concrete production example.
**A:** Often by improving memory reuse through vector types: precompute, cache, and process in tiles instead of touching global memory repeatedly. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What are the limits of vector types on current hardware - justify your answer with a concrete production example.
**A:** The finite number of threads per SM, shared memory bytes, registers, and memory bandwidth all cap vector types; reaching these limits signals a rendering ceiling. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How do warps schedule work that depends on vector types - justify your answer with a concrete production example.
**A:** The scheduler picks eligible warps whose data dependencies are resolved; poor vector types creates long stalls that starve the execution units. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What is the minimal viable test for vector types - justify your answer with a concrete production example.
**A:** Render one known image, profile kernel time, and confirm the result matches a reference before adding more complexity on top of vector types. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: How does vector types interact with numerical integrators - justify your answer with a concrete production example.
**A:** Integrators advance each ray with feedback; vector types decides whether per-ray state stays in registers and how divergent the compute becomes. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the mental model for vector types at the thread level - justify your answer with a concrete production example.
**A:** One thread owns one unit of work; vector types defines how that work reads inputs, keeps intermediate state, writes output, and finishes when done. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How do libraries and your own kernels divide responsibility for vector types - justify your answer with a concrete production example.
**A:** Libraries like cuBLAS/cuFFT handle their own vector types; your kernels must match their launch dimensions and memory layouts for zero-copy interop. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How do libraries and your own kernels divide responsibility for vector types - justify your answer with a concrete production example.
**A:** Libraries like cuBLAS/cuFFT handle their own vector types; your kernels must match their launch dimensions and memory layouts for zero-copy interop. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What is the mental model for vector types at the thread level - justify your answer with a concrete production example.
**A:** One thread owns one unit of work; vector types defines how that work reads inputs, keeps intermediate state, writes output, and finishes when done. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does vector types interact with numerical integrators - justify your answer with a concrete production example.
**A:** Integrators advance each ray with feedback; vector types decides whether per-ray state stays in registers and how divergent the compute becomes. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What is the minimal viable test for vector types - justify your answer with a concrete production example.
**A:** Render one known image, profile kernel time, and confirm the result matches a reference before adding more complexity on top of vector types. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How do warps schedule work that depends on vector types - justify your answer with a concrete production example.
**A:** The scheduler picks eligible warps whose data dependencies are resolved; poor vector types creates long stalls that starve the execution units. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What are the limits of vector types on current hardware - justify your answer with a concrete production example.
**A:** The finite number of threads per SM, shared memory bytes, registers, and memory bandwidth all cap vector types; reaching these limits signals a rendering ceiling. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How would you get a 2x speedup out of vector types - justify your answer with a concrete production example.
**A:** Often by improving memory reuse through vector types: precompute, cache, and process in tiles instead of touching global memory repeatedly. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What role does vector types play in frame-to-frame consistency - justify your answer with a concrete production example.
**A:** Deterministic vector types means the same inputs give identical pixels every export, which matters when you render an animation one frame at a time. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you explain vector types to a non-GPU colleague - justify your answer with a concrete production example.
**A:** Analogize to a factory: vector types is the layout of workbenches and machines so thousands of identical jobs finish in parallel without colliding. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What documentation should exist for vector types - justify your answer with a concrete production example.
**A:** A short design note stating the assumptions, measured numbers, and the validation test so future changes to vector types are reviewable. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: Compare the cost of getting vector types right early vs late - justify your answer with a concrete production example.
**A:** Fixing vector types after the pipeline is written means rewriting kernels and re-validating images; deciding it first saves most of that rework. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What kernel design decisions flow from vector types - justify your answer with a concrete production example.
**A:** Block size, grid dimensions, whether to preload to shared memory, loop structure, and halting strategy for early ray termination. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How does vector types change when scaling to multiple GPUs - justify your answer with a concrete production example.
**A:** Per-device vector types stays local, but you add host-side distribution, transfer overlap, and result collection for the overall frame. A concrete example: consistently applying vector types in code review and regression tests keeps the whole pipeline trustworthy.
