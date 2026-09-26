# Gpu Performance — Reductions Interview Questions and Answers

## Q1: What is a GPU reduction?
**A:** Combining many values into one (sum, min, max of per-pixel intensities across tiles) - the classic parallel pattern a renderer uses to total a frame's flux.

## Q2: What is the tree reduction?
**A:** The standard: each thread reduces its chunk, shared-memory tree sums within a block (pairwise, synchronized), then atomics/tree across blocks - O(log n).

## Q3: Why are naive reductions slow?
**A:** The naive 'one thread sums all, shared serial loop' is O(n) serial — trees exploit all employees in parallel, crucial for per-frame flux totals.

## Q4: How does warp-shuffle reduce?
**A:** Threads exchange values directly via __shfl_down_sync in-register (no shared) - a full warp reduction in 5 shuffle steps, the modern fastest base.

## Q5: Where are reductions in the raytracer?
**A:** Total flux per band, image moments (center, rms), per-tile statistics, and the polarization averages - any scalar summary of the frame.

## Q6: What is the associative-precision trap?
**A:** Tree/reorder changes the summation order -> results differ between runs; a SPECIFIED tree order (or per-run float prec) pins the frame's reproducibility.

## Q7: What is the atomic slowdown hazard?
**A:** A global-add per thread serializes millions of atomics; reduce within the tile's shared memory first, then one atomic per block - the standard fix.

## Q8: What are the torn-write hazards?
**A:** Simultaneous per-pixel-accumulated writes to the image buffer from multiple tiles must be exact-add atomics or tile-dedicated regions - never racy reads.

## Q9: What does the profiler say?
**A:** Nsight's 'Atomics' throughput and memory reduce coverage shows whether the reduction path is starved; a saturated atomic path is the fix signal.

## Q10: What is hierarchical reduction for movies?
**A:** Reduce per frame, accumulate per movie; the two-level aggregation keeps singles-frame totals and a running total without re-reading history.

## Q11: What is the stochastic rejection benefit?
**A:** Reductions over supersampled rays (average, variance) yield the S/N statistics — a single reduction pass provides both value and error bars.

## Q12: What is the validation?
**A:** A known brute-force sum on an analytic field must agree with the tree reduction to rounding tolerance; enforce at the test-suite level.

## Q13: What is the summary?
**A:** Reductions are the frame's scalar-stats backbone: warp-shuffles + shared trees + one atomic/block, order-pinned for reproducibility — never naive serial.

## Q14: What does reductions mean for the raytracer's runtime?
**A:** It is the lever that turns a working kernel into a fast one; reductions improvements typically change frame times by 2-10x with identical output.

## Q15: Why does reductions matter more than FLOPs for raytracing?
**A:** Ray integration is memory- and latency-bound; reductions targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins.

## Q16: How do you profile reductions?
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; reductions tuning starts from measured numbers, not guesses.

## Q17: What is the first thing to fix under reductions?
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since reductions memory stalls dominate.

## Q18: How does reductions relate to warp occupancy?
**A:** More resident warps hide more latency, but registers/shared memory limit it; reductions balances occupancy against per-thread state.

## Q19: What is a typical 90/10 reductions rule?
**A:** 10% of the kernel is 90% of the runtime; reductions spend begins by identifying and fixing that hot loop, then measuring again.

## Q20: How does reductions handle determinism?
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep reductions results reproducible while still fast.

## Q21: What does reductions do about divergent geodesic paths?
**A:** Assign one ray per thread so long and short rays simply finish at different times; reductions accepts this natural load imbalance.

## Q22: How is reductions measured end-to-end?
**A:** Frames per second at fixed image size and step policy; reductions reports both median kernel time and total wall time.

## Q23: How does reductions choose block size?
**A:** A multiple of the warp size that fills the SM to target occupancy; reductions sweeps 64-512 to find the plateau.

## Q24: What memory optimizations fall under reductions?
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the reductions toolbox.

## Q25: How does reductions scale to multi-GPU?
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; reductions keeps per-GPU work identical and overlap transfers.

## Q26: How does reductions use streams?
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; reductions overlaps host and device work.

## Q27: When is reductions over-engineering?
**A:** When the pipeline is still changing daily; reductions stabilization is reserved for mature kernels judged by their benchmark suite.

## Q28: What is the best first metric for reductions?
**A:** Achieved occupancy and DRAM throughput from Nsight; reductions optimization targets whichever is below the theoretical peak.

## Q29: How does reductions handle the image write-back?
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; reductions avoids read-modify-write penalties.

## Q30: What role does shared memory play in reductions?
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so reductions boosts cache hits dramatically.

## Q31: How does reductions cope with long-ish rays?
**A:** Spatially coherent groups finish similarly; reductions sorts/orders work briefly, or simply lets occupancy absorb the imbalance.

## Q32: What is a reductions regression test?
**A:** The golden image must not change when reductions is tuned; a side-channel checksum asserts identical pixels after each optimization.

## Q33: How does reductions treat constant and texture paths?
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; reductions chooses the path that reduces traffic.

## Q34: What should be avoided for reductions?
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle reductions.

## Q35: How do you explain reductions impact to a reviewer?
**A:** Show before/after Nsight categories and frame times; reductions communicates in measured evidence rather than opinion.

## Q36: What is the reductions budget for a movie frame?
**A:** If 1 second per frame is acceptable at 30 fps, reductions leaves ~33 ms; most pipelines budget a bit more and render offline with a farm.

## Q37: Where should reductions stop?
**A:** Once no profile category dominates and further gains are under a few percent, reductions stops and the remaining money goes to more samples.

## Q38: Where should reductions stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, reductions stops and the remaining money goes to more samples. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q39: What is the reductions budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, reductions leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: How do you explain reductions impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; reductions communicates in measured evidence rather than opinion. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What should be avoided for reductions - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle reductions. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does reductions treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; reductions chooses the path that reduces traffic. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What is a reductions regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when reductions is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How does reductions cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; reductions sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What role does shared memory play in reductions - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so reductions boosts cache hits dramatically. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does reductions handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; reductions avoids read-modify-write penalties. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What is the best first metric for reductions - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; reductions optimization targets whichever is below the theoretical peak. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: When is reductions over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; reductions stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: How does reductions use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; reductions overlaps host and device work. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How does reductions scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; reductions keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What memory optimizations fall under reductions - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the reductions toolbox. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How does reductions choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; reductions sweeps 64-512 to find the plateau. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: How is reductions measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; reductions reports both median kernel time and total wall time. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: What does reductions do about divergent geodesic paths - justify your answer with a concrete production example.
**A:** Assign one ray per thread so long and short rays simply finish at different times; reductions accepts this natural load imbalance. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: How does reductions handle determinism - justify your answer with a concrete production example.
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep reductions results reproducible while still fast. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What is a typical 90/10 reductions rule - justify your answer with a concrete production example.
**A:** 10% of the kernel is 90% of the runtime; reductions spend begins by identifying and fixing that hot loop, then measuring again. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does reductions relate to warp occupancy - justify your answer with a concrete production example.
**A:** More resident warps hide more latency, but registers/shared memory limit it; reductions balances occupancy against per-thread state. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the first thing to fix under reductions - justify your answer with a concrete production example.
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since reductions memory stalls dominate. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How do you profile reductions - justify your answer with a concrete production example.
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; reductions tuning starts from measured numbers, not guesses. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: Why does reductions matter more than FLOPs for raytracing - justify your answer with a concrete production example.
**A:** Ray integration is memory- and latency-bound; reductions targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What does reductions mean for the raytracer's runtime - justify your answer with a concrete production example.
**A:** It is the lever that turns a working kernel into a fast one; reductions improvements typically change frame times by 2-10x with identical output. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: What does reductions mean for the raytracer's runtime - justify your answer with a concrete production example.
**A:** It is the lever that turns a working kernel into a fast one; reductions improvements typically change frame times by 2-10x with identical output. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: Why does reductions matter more than FLOPs for raytracing - justify your answer with a concrete production example.
**A:** Ray integration is memory- and latency-bound; reductions targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: How do you profile reductions - justify your answer with a concrete production example.
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; reductions tuning starts from measured numbers, not guesses. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: What is the first thing to fix under reductions - justify your answer with a concrete production example.
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since reductions memory stalls dominate. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How does reductions relate to warp occupancy - justify your answer with a concrete production example.
**A:** More resident warps hide more latency, but registers/shared memory limit it; reductions balances occupancy against per-thread state. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What is a typical 90/10 reductions rule - justify your answer with a concrete production example.
**A:** 10% of the kernel is 90% of the runtime; reductions spend begins by identifying and fixing that hot loop, then measuring again. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How does reductions handle determinism - justify your answer with a concrete production example.
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep reductions results reproducible while still fast. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What does reductions do about divergent geodesic paths - justify your answer with a concrete production example.
**A:** Assign one ray per thread so long and short rays simply finish at different times; reductions accepts this natural load imbalance. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How is reductions measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; reductions reports both median kernel time and total wall time. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How does reductions choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; reductions sweeps 64-512 to find the plateau. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What memory optimizations fall under reductions - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the reductions toolbox. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does reductions scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; reductions keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: How does reductions use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; reductions overlaps host and device work. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: When is reductions over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; reductions stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What is the best first metric for reductions - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; reductions optimization targets whichever is below the theoretical peak. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How does reductions handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; reductions avoids read-modify-write penalties. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What role does shared memory play in reductions - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so reductions boosts cache hits dramatically. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How does reductions cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; reductions sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What is a reductions regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when reductions is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does reductions treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; reductions chooses the path that reduces traffic. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What should be avoided for reductions - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle reductions. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How do you explain reductions impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; reductions communicates in measured evidence rather than opinion. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What is the reductions budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, reductions leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: Where should reductions stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, reductions stops and the remaining money goes to more samples. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: Where should reductions stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, reductions stops and the remaining money goes to more samples. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: What is the reductions budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, reductions leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How do you explain reductions impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; reductions communicates in measured evidence rather than opinion. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What should be avoided for reductions - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle reductions. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does reductions treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; reductions chooses the path that reduces traffic. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What is a reductions regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when reductions is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How does reductions cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; reductions sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What role does shared memory play in reductions - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so reductions boosts cache hits dramatically. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does reductions handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; reductions avoids read-modify-write penalties. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What is the best first metric for reductions - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; reductions optimization targets whichever is below the theoretical peak. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: When is reductions over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; reductions stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: How does reductions use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; reductions overlaps host and device work. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How does reductions scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; reductions keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What memory optimizations fall under reductions - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the reductions toolbox. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How does reductions choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; reductions sweeps 64-512 to find the plateau. A concrete example: consistently applying reductions in code review and regression tests keeps the whole pipeline trustworthy.
