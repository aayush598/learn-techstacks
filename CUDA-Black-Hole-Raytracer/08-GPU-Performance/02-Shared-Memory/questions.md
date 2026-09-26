# Gpu Performance — Shared Memory Interview Questions and Answers

## Q1: What is shared memory?
**A:** On-chip SRAM per thread block, visible to all threads of the block - the fastest re-usable data beside registers, ~40-100x faster than global.

## Q2: What does shared memory buy a raytracer?
**A:** Caching a block's local grid slab (emissivity/frontier cells) so every thread's trilinear fetch reads once from global instead of 8 times.

## Q3: What is the classic tiled use?
**A:** A block processes a tile of rays over the same grid neighborhood; the neighborhood's field values load once into shared, then all rays interpolate locally.

## Q4: What is the tradeoff of shared vs texture fetch?
**A:** Shared gives explicit control and cheap reuse but uses an explicit copy; texture/L1 does implicit caching - for per-ray random-ish sampling, texture may win.

## Q5: How big is shared memory?
**A:** ~48-228 KB per SM (configurable); a 256-thread block with a 64^3 field slab (1 MB) obviously won't fit - size tiles to the field's true reuse footprint.

## Q6: What is a shared-memory pad (bank alignment)?
**A:** Padding the stride (e.g., [N][N+1]) shifts row starts so threads' column accesses hit distinct banks - the antidote to bank conflicts.

## Q7: What is the double-buffer pattern?
**A:** While a tile processes slab k, the next slab's data streams into shared - overlapping load and compute hides the memory latency completely.

## Q8: What is the 'atomics-in-shared' use?
**A:** Accumulating per-cell emissivity counters or votes inside a block in shared (via shared atomics) avoids global atomic contention on hot cells.

## Q9: When is shared memory NOT worth it?
**A:** When threads touch disjoint far-apart regions (e.g., scattered octree leaves) - the reuse is zero and the copy cost pure overhead; let L1 cache instead.

## Q10: How do you decide the tile size?
**A:** Measure the reuse factor (field fetches per cell load): tiles amortize load cost when reuse > 2-4; size to occupancy (registers + shared per block).

## Q11: What is the occupancy interplay?
**A:** Each block's shared allocation caps how many blocks fit per SM; a big slab that halves occupancy may lose more than it saves - test both directions.

## Q12: What are the debugging pitfalls?
**A:** Race conditions on initial shared fill (missing __syncthreads) corrupt the tile - use the patterns documented (fill-then-sync), never ad-hoc.

## Q13: What is the shared-memory-by-default variant?
**A:** Metrics: kernel's shared bytes per block; profiler's 'Shared Memory Bank Conflicts' and 'Occupancy' reports - the numbers tell the story.

## Q14: What is the summary?
**A:** Shared memory is for structured, reused neighborhood data within a block - tile the grid slab, pad for banks, double-buffer for latency - a measured tool.

## Q15: What does shared memory mean for the raytracer's runtime?
**A:** It is the lever that turns a working kernel into a fast one; shared memory improvements typically change frame times by 2-10x with identical output.

## Q16: Why does shared memory matter more than FLOPs for raytracing?
**A:** Ray integration is memory- and latency-bound; shared memory targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins.

## Q17: How do you profile shared memory?
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; shared memory tuning starts from measured numbers, not guesses.

## Q18: What is the first thing to fix under shared memory?
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since shared memory memory stalls dominate.

## Q19: How does shared memory relate to warp occupancy?
**A:** More resident warps hide more latency, but registers/shared memory limit it; shared memory balances occupancy against per-thread state.

## Q20: What is a typical 90/10 shared memory rule?
**A:** 10% of the kernel is 90% of the runtime; shared memory spend begins by identifying and fixing that hot loop, then measuring again.

## Q21: How does shared memory handle determinism?
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep shared memory results reproducible while still fast.

## Q22: What does shared memory do about divergent geodesic paths?
**A:** Assign one ray per thread so long and short rays simply finish at different times; shared memory accepts this natural load imbalance.

## Q23: How is shared memory measured end-to-end?
**A:** Frames per second at fixed image size and step policy; shared memory reports both median kernel time and total wall time.

## Q24: How does shared memory choose block size?
**A:** A multiple of the warp size that fills the SM to target occupancy; shared memory sweeps 64-512 to find the plateau.

## Q25: What memory optimizations fall under shared memory?
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the shared memory toolbox.

## Q26: How does shared memory scale to multi-GPU?
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; shared memory keeps per-GPU work identical and overlap transfers.

## Q27: How does shared memory use streams?
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; shared memory overlaps host and device work.

## Q28: When is shared memory over-engineering?
**A:** When the pipeline is still changing daily; shared memory stabilization is reserved for mature kernels judged by their benchmark suite.

## Q29: What is the best first metric for shared memory?
**A:** Achieved occupancy and DRAM throughput from Nsight; shared memory optimization targets whichever is below the theoretical peak.

## Q30: How does shared memory handle the image write-back?
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; shared memory avoids read-modify-write penalties.

## Q31: What role does shared memory play in shared memory?
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so shared memory boosts cache hits dramatically.

## Q32: How does shared memory cope with long-ish rays?
**A:** Spatially coherent groups finish similarly; shared memory sorts/orders work briefly, or simply lets occupancy absorb the imbalance.

## Q33: What is a shared memory regression test?
**A:** The golden image must not change when shared memory is tuned; a side-channel checksum asserts identical pixels after each optimization.

## Q34: How does shared memory treat constant and texture paths?
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; shared memory chooses the path that reduces traffic.

## Q35: What should be avoided for shared memory?
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle shared memory.

## Q36: How do you explain shared memory impact to a reviewer?
**A:** Show before/after Nsight categories and frame times; shared memory communicates in measured evidence rather than opinion.

## Q37: What is the shared memory budget for a movie frame?
**A:** If 1 second per frame is acceptable at 30 fps, shared memory leaves ~33 ms; most pipelines budget a bit more and render offline with a farm.

## Q38: Where should shared memory stop?
**A:** Once no profile category dominates and further gains are under a few percent, shared memory stops and the remaining money goes to more samples.

## Q39: Where should shared memory stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, shared memory stops and the remaining money goes to more samples. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: What is the shared memory budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, shared memory leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: How do you explain shared memory impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; shared memory communicates in measured evidence rather than opinion. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What should be avoided for shared memory - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle shared memory. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How does shared memory treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; shared memory chooses the path that reduces traffic. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What is a shared memory regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when shared memory is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: How does shared memory cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; shared memory sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What role does shared memory play in shared memory - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so shared memory boosts cache hits dramatically. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How does shared memory handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; shared memory avoids read-modify-write penalties. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What is the best first metric for shared memory - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; shared memory optimization targets whichever is below the theoretical peak. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: When is shared memory over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; shared memory stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How does shared memory use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; shared memory overlaps host and device work. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How does shared memory scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; shared memory keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What memory optimizations fall under shared memory - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the shared memory toolbox. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: How does shared memory choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; shared memory sweeps 64-512 to find the plateau. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How is shared memory measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; shared memory reports both median kernel time and total wall time. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What does shared memory do about divergent geodesic paths - justify your answer with a concrete production example.
**A:** Assign one ray per thread so long and short rays simply finish at different times; shared memory accepts this natural load imbalance. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How does shared memory handle determinism - justify your answer with a concrete production example.
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep shared memory results reproducible while still fast. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What is a typical 90/10 shared memory rule - justify your answer with a concrete production example.
**A:** 10% of the kernel is 90% of the runtime; shared memory spend begins by identifying and fixing that hot loop, then measuring again. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: How does shared memory relate to warp occupancy - justify your answer with a concrete production example.
**A:** More resident warps hide more latency, but registers/shared memory limit it; shared memory balances occupancy against per-thread state. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What is the first thing to fix under shared memory - justify your answer with a concrete production example.
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since shared memory memory stalls dominate. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: How do you profile shared memory - justify your answer with a concrete production example.
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; shared memory tuning starts from measured numbers, not guesses. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: Why does shared memory matter more than FLOPs for raytracing - justify your answer with a concrete production example.
**A:** Ray integration is memory- and latency-bound; shared memory targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: What does shared memory mean for the raytracer's runtime - justify your answer with a concrete production example.
**A:** It is the lever that turns a working kernel into a fast one; shared memory improvements typically change frame times by 2-10x with identical output. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does shared memory mean for the raytracer's runtime - justify your answer with a concrete production example.
**A:** It is the lever that turns a working kernel into a fast one; shared memory improvements typically change frame times by 2-10x with identical output. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: Why does shared memory matter more than FLOPs for raytracing - justify your answer with a concrete production example.
**A:** Ray integration is memory- and latency-bound; shared memory targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: How do you profile shared memory - justify your answer with a concrete production example.
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; shared memory tuning starts from measured numbers, not guesses. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is the first thing to fix under shared memory - justify your answer with a concrete production example.
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since shared memory memory stalls dominate. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How does shared memory relate to warp occupancy - justify your answer with a concrete production example.
**A:** More resident warps hide more latency, but registers/shared memory limit it; shared memory balances occupancy against per-thread state. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What is a typical 90/10 shared memory rule - justify your answer with a concrete production example.
**A:** 10% of the kernel is 90% of the runtime; shared memory spend begins by identifying and fixing that hot loop, then measuring again. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How does shared memory handle determinism - justify your answer with a concrete production example.
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep shared memory results reproducible while still fast. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What does shared memory do about divergent geodesic paths - justify your answer with a concrete production example.
**A:** Assign one ray per thread so long and short rays simply finish at different times; shared memory accepts this natural load imbalance. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How is shared memory measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; shared memory reports both median kernel time and total wall time. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: How does shared memory choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; shared memory sweeps 64-512 to find the plateau. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: What memory optimizations fall under shared memory - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the shared memory toolbox. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: How does shared memory scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; shared memory keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How does shared memory use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; shared memory overlaps host and device work. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: When is shared memory over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; shared memory stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What is the best first metric for shared memory - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; shared memory optimization targets whichever is below the theoretical peak. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How does shared memory handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; shared memory avoids read-modify-write penalties. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What role does shared memory play in shared memory - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so shared memory boosts cache hits dramatically. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does shared memory cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; shared memory sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: What is a shared memory regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when shared memory is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: How does shared memory treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; shared memory chooses the path that reduces traffic. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What should be avoided for shared memory - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle shared memory. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: How do you explain shared memory impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; shared memory communicates in measured evidence rather than opinion. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What is the shared memory budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, shared memory leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: Where should shared memory stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, shared memory stops and the remaining money goes to more samples. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: Where should shared memory stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, shared memory stops and the remaining money goes to more samples. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What is the shared memory budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, shared memory leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: How do you explain shared memory impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; shared memory communicates in measured evidence rather than opinion. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What should be avoided for shared memory - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle shared memory. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How does shared memory treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; shared memory chooses the path that reduces traffic. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What is a shared memory regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when shared memory is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: How does shared memory cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; shared memory sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What role does shared memory play in shared memory - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so shared memory boosts cache hits dramatically. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How does shared memory handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; shared memory avoids read-modify-write penalties. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What is the best first metric for shared memory - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; shared memory optimization targets whichever is below the theoretical peak. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: When is shared memory over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; shared memory stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How does shared memory use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; shared memory overlaps host and device work. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How does shared memory scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; shared memory keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What memory optimizations fall under shared memory - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the shared memory toolbox. A concrete example: consistently applying shared memory in code review and regression tests keeps the whole pipeline trustworthy.
