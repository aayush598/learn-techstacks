# Gpu Performance — Tiling Interview Questions and Answers

## Q1: What is tiling in the renderer?
**A:** Partitioning the image (or ray batch) into small tiles each handled by one thread block - the standard structure that makes coalescing, shared reuse, and occupancy coherent.

## Q2: How big should a tile be?
**A:** Common choices 8x8/16x16 pixels/block: enough for reuse and a full warp structure, small enough to keep blocks balanced and tails narrow.

## Q3: What does tiling do for field locality?
**A:** A tile's rays probe a compact area of the <real> scene (same geodesic neighborhood), so shared/tile caches hold the relevant field slab - reuse without waste.

## Q4: What is the 'ray tile' vs 'screen tile'?
**A:** Screen tile: pixels in a block (natural for output); ray tile: a batch of coherent rays (needed with supersampling/importance) - map pixels to rays once.

## Q5: How does tiling interact with adaptive steps?
**A:** A tile's rays realize similar integration difficulty; warp-uniform stepping stays coherent within the tile, minimizing divergence.

## Q6: What is the tile-order for the write-out?
**A:** Process tiles in a scanline that keeps the image write coalesced; a tiled frame is written tile-by-tile (each block its own region) - trivial with SoA.

## Q7: What does tiling do to L2?
**A:** Neighboring tiles' field fetches overlap L2 residually; an L2-friendly tile order amortizes the most-refetched ring slab across consecutive blocks.

## Q8: What is the halo/ghost requirement?
**A:** Interpolation needs neighbor cells beyond the tile's core volume; padded shared tiles carry a 1-cell halo so samples never touch global.

## Q9: What is the balance lever (tile granularity)?
**A:** Too-large tiles lose tail balance and halo efficiency; too-small tiles lose reuse and launch overhead - sweep and pick the plateau (e.g., 16x16).

## Q10: How do you handle the variable ray count per pixel?
**A:** Each tile carries its own supersample count (static per frame); accumulation per tile is shared-local then global - no atomics on the image plane.

## Q11: What is the validation for tiling?
**A:** The tile decomposition must produce bit-identical frames (deterministic reduction); A/B tile sizes must agree on the image to machine level.

## Q12: How does tiling serve the multi-pixel hybrid?
**A:** For pixels mixing capture/miss, the tile's write-out branches; branchless indices (mask vs pointer) keep the block's store pattern uniform.

## Q13: What is the summary?
**A:** Tiling is the structural backbone: fixed-size pixel tiles make coalescing, shared reuse, halo interpolation, quiet reduction, and balanced occupancy all fall out.

## Q14: What does tiling mean for the raytracer's runtime?
**A:** It is the lever that turns a working kernel into a fast one; tiling improvements typically change frame times by 2-10x with identical output.

## Q15: Why does tiling matter more than FLOPs for raytracing?
**A:** Ray integration is memory- and latency-bound; tiling targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins.

## Q16: How do you profile tiling?
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; tiling tuning starts from measured numbers, not guesses.

## Q17: What is the first thing to fix under tiling?
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since tiling memory stalls dominate.

## Q18: How does tiling relate to warp occupancy?
**A:** More resident warps hide more latency, but registers/shared memory limit it; tiling balances occupancy against per-thread state.

## Q19: What is a typical 90/10 tiling rule?
**A:** 10% of the kernel is 90% of the runtime; tiling spend begins by identifying and fixing that hot loop, then measuring again.

## Q20: How does tiling handle determinism?
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep tiling results reproducible while still fast.

## Q21: What does tiling do about divergent geodesic paths?
**A:** Assign one ray per thread so long and short rays simply finish at different times; tiling accepts this natural load imbalance.

## Q22: How is tiling measured end-to-end?
**A:** Frames per second at fixed image size and step policy; tiling reports both median kernel time and total wall time.

## Q23: How does tiling choose block size?
**A:** A multiple of the warp size that fills the SM to target occupancy; tiling sweeps 64-512 to find the plateau.

## Q24: What memory optimizations fall under tiling?
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the tiling toolbox.

## Q25: How does tiling scale to multi-GPU?
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; tiling keeps per-GPU work identical and overlap transfers.

## Q26: How does tiling use streams?
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; tiling overlaps host and device work.

## Q27: When is tiling over-engineering?
**A:** When the pipeline is still changing daily; tiling stabilization is reserved for mature kernels judged by their benchmark suite.

## Q28: What is the best first metric for tiling?
**A:** Achieved occupancy and DRAM throughput from Nsight; tiling optimization targets whichever is below the theoretical peak.

## Q29: How does tiling handle the image write-back?
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; tiling avoids read-modify-write penalties.

## Q30: What role does shared memory play in tiling?
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so tiling boosts cache hits dramatically.

## Q31: How does tiling cope with long-ish rays?
**A:** Spatially coherent groups finish similarly; tiling sorts/orders work briefly, or simply lets occupancy absorb the imbalance.

## Q32: What is a tiling regression test?
**A:** The golden image must not change when tiling is tuned; a side-channel checksum asserts identical pixels after each optimization.

## Q33: How does tiling treat constant and texture paths?
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; tiling chooses the path that reduces traffic.

## Q34: What should be avoided for tiling?
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle tiling.

## Q35: How do you explain tiling impact to a reviewer?
**A:** Show before/after Nsight categories and frame times; tiling communicates in measured evidence rather than opinion.

## Q36: What is the tiling budget for a movie frame?
**A:** If 1 second per frame is acceptable at 30 fps, tiling leaves ~33 ms; most pipelines budget a bit more and render offline with a farm.

## Q37: Where should tiling stop?
**A:** Once no profile category dominates and further gains are under a few percent, tiling stops and the remaining money goes to more samples.

## Q38: Where should tiling stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, tiling stops and the remaining money goes to more samples. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q39: What is the tiling budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, tiling leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: How do you explain tiling impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; tiling communicates in measured evidence rather than opinion. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What should be avoided for tiling - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle tiling. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does tiling treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; tiling chooses the path that reduces traffic. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What is a tiling regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when tiling is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How does tiling cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; tiling sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What role does shared memory play in tiling - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so tiling boosts cache hits dramatically. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does tiling handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; tiling avoids read-modify-write penalties. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What is the best first metric for tiling - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; tiling optimization targets whichever is below the theoretical peak. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: When is tiling over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; tiling stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: How does tiling use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; tiling overlaps host and device work. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How does tiling scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; tiling keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What memory optimizations fall under tiling - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the tiling toolbox. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How does tiling choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; tiling sweeps 64-512 to find the plateau. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: How is tiling measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; tiling reports both median kernel time and total wall time. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: What does tiling do about divergent geodesic paths - justify your answer with a concrete production example.
**A:** Assign one ray per thread so long and short rays simply finish at different times; tiling accepts this natural load imbalance. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: How does tiling handle determinism - justify your answer with a concrete production example.
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep tiling results reproducible while still fast. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What is a typical 90/10 tiling rule - justify your answer with a concrete production example.
**A:** 10% of the kernel is 90% of the runtime; tiling spend begins by identifying and fixing that hot loop, then measuring again. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does tiling relate to warp occupancy - justify your answer with a concrete production example.
**A:** More resident warps hide more latency, but registers/shared memory limit it; tiling balances occupancy against per-thread state. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the first thing to fix under tiling - justify your answer with a concrete production example.
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since tiling memory stalls dominate. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How do you profile tiling - justify your answer with a concrete production example.
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; tiling tuning starts from measured numbers, not guesses. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: Why does tiling matter more than FLOPs for raytracing - justify your answer with a concrete production example.
**A:** Ray integration is memory- and latency-bound; tiling targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What does tiling mean for the raytracer's runtime - justify your answer with a concrete production example.
**A:** It is the lever that turns a working kernel into a fast one; tiling improvements typically change frame times by 2-10x with identical output. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: What does tiling mean for the raytracer's runtime - justify your answer with a concrete production example.
**A:** It is the lever that turns a working kernel into a fast one; tiling improvements typically change frame times by 2-10x with identical output. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: Why does tiling matter more than FLOPs for raytracing - justify your answer with a concrete production example.
**A:** Ray integration is memory- and latency-bound; tiling targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: How do you profile tiling - justify your answer with a concrete production example.
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; tiling tuning starts from measured numbers, not guesses. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: What is the first thing to fix under tiling - justify your answer with a concrete production example.
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since tiling memory stalls dominate. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How does tiling relate to warp occupancy - justify your answer with a concrete production example.
**A:** More resident warps hide more latency, but registers/shared memory limit it; tiling balances occupancy against per-thread state. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What is a typical 90/10 tiling rule - justify your answer with a concrete production example.
**A:** 10% of the kernel is 90% of the runtime; tiling spend begins by identifying and fixing that hot loop, then measuring again. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How does tiling handle determinism - justify your answer with a concrete production example.
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep tiling results reproducible while still fast. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What does tiling do about divergent geodesic paths - justify your answer with a concrete production example.
**A:** Assign one ray per thread so long and short rays simply finish at different times; tiling accepts this natural load imbalance. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How is tiling measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; tiling reports both median kernel time and total wall time. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How does tiling choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; tiling sweeps 64-512 to find the plateau. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What memory optimizations fall under tiling - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the tiling toolbox. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does tiling scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; tiling keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: How does tiling use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; tiling overlaps host and device work. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: When is tiling over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; tiling stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What is the best first metric for tiling - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; tiling optimization targets whichever is below the theoretical peak. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How does tiling handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; tiling avoids read-modify-write penalties. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What role does shared memory play in tiling - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so tiling boosts cache hits dramatically. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How does tiling cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; tiling sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What is a tiling regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when tiling is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does tiling treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; tiling chooses the path that reduces traffic. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What should be avoided for tiling - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle tiling. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How do you explain tiling impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; tiling communicates in measured evidence rather than opinion. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What is the tiling budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, tiling leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: Where should tiling stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, tiling stops and the remaining money goes to more samples. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: Where should tiling stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, tiling stops and the remaining money goes to more samples. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: What is the tiling budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, tiling leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How do you explain tiling impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; tiling communicates in measured evidence rather than opinion. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What should be avoided for tiling - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle tiling. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does tiling treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; tiling chooses the path that reduces traffic. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What is a tiling regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when tiling is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How does tiling cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; tiling sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What role does shared memory play in tiling - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so tiling boosts cache hits dramatically. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does tiling handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; tiling avoids read-modify-write penalties. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What is the best first metric for tiling - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; tiling optimization targets whichever is below the theoretical peak. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: When is tiling over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; tiling stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: How does tiling use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; tiling overlaps host and device work. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How does tiling scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; tiling keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What memory optimizations fall under tiling - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the tiling toolbox. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How does tiling choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; tiling sweeps 64-512 to find the plateau. A concrete example: consistently applying tiling in code review and regression tests keeps the whole pipeline trustworthy.
