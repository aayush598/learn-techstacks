# Gpu Performance — Latency Hiding Interview Questions and Answers

## Q1: What is latency hiding on a GPU?
**A:** While one warp waits on memory/integer stalls, the SM runs OTHER available warps - the GPU's way of turning memory latency into throughput.

## Q2: Why is occupancy the engine of latency hiding?
**A:** More resident warps = more independent work to interleave - the standard rule: high occupancy hides long-latency global/texture accesses.

## Q3: What is the arithmetic intensity?
**A:** The ratio of compute to memory per item; low-intensity raytracer loops (few flops per fetch) are bandwidth-bound and rely on hiding, not raw flops.

## Q4: How do you cap the raytracer's latency?
**A:** Enough resident rays (high per-block-rays, high blocks-per-SM) so memory fetches of one warp overlap ALU work of others - the parallelism is the hiding.

## Q5: What is the role of prefetching?
**A:** Issue the next segment's field fetches before computing the current one (double-buffer in shared/registers) - explicit code-level overlap.

## Q6: What does the profiler say about stalls?
**A:** Nsight's 'Memory Stall' vs 'Execute Stall' distribution: if memory stalls dominate, add occupancy or prefetch; if execute, it's ALU time.

## Q7: What is the target believe in occupancy?
**A:** Get enough warps to cover the worst memory-stall duration (~600-800 cycles): compute needed resident warps = stall_cycles/issue_cycles.

## Q8: How do adaptive ray paths hurt hiding?
**A:** Diverged rays fetch scattered memory and amortize fewer warps; sorting rays into bins (by region/branch) keeps warps coherent and the hiding uniform.

## Q9: What is the 'memory-to-compute overlap' benchmark?
**A:** With a known field, a pure-fetch kernel's throughput vs a pure-compute kernel - the gap is exactly the latency you are (or are not) hiding.

## Q10: What is the role of cache reuse in hiding?
**A:** L1/L2 hits flip 'long latency' into 'short hits' - good spatial locality among warp rays shrinks the stall, not just covers it.

## Q11: What are the long/life operations to hide?
**A:** Trilinear field fetches, HIT refinement bisections, and octree node loads: batch as many independent fetches per thread as registers allow (ILP).

## Q12: How does instruction-level parallelism (ILP) help?
**A:** Independent field samples (4-8 loads in flight per thread) hide each other's latency without needing more warps - a second lever beyond occupancy.

## Q13: What is the validation loop?
**A:** Vary occupancy (block/rays per block) and measure throughput; the knee of the curve is the practical hiding point - don't chase 100% occupancy blindly.

## Q14: What is the summary?
**A:** Latency hiding turns stalled time into throughput: crank occupancy, batch independent loads (ILP), prefetch, and verify that stalls are predominantly hidden in Nsight.

## Q15: What does latency hiding mean for the raytracer's runtime?
**A:** It is the lever that turns a working kernel into a fast one; latency hiding improvements typically change frame times by 2-10x with identical output.

## Q16: Why does latency hiding matter more than FLOPs for raytracing?
**A:** Ray integration is memory- and latency-bound; latency hiding targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins.

## Q17: How do you profile latency hiding?
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; latency hiding tuning starts from measured numbers, not guesses.

## Q18: What is the first thing to fix under latency hiding?
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since latency hiding memory stalls dominate.

## Q19: How does latency hiding relate to warp occupancy?
**A:** More resident warps hide more latency, but registers/shared memory limit it; latency hiding balances occupancy against per-thread state.

## Q20: What is a typical 90/10 latency hiding rule?
**A:** 10% of the kernel is 90% of the runtime; latency hiding spend begins by identifying and fixing that hot loop, then measuring again.

## Q21: How does latency hiding handle determinism?
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep latency hiding results reproducible while still fast.

## Q22: What does latency hiding do about divergent geodesic paths?
**A:** Assign one ray per thread so long and short rays simply finish at different times; latency hiding accepts this natural load imbalance.

## Q23: How is latency hiding measured end-to-end?
**A:** Frames per second at fixed image size and step policy; latency hiding reports both median kernel time and total wall time.

## Q24: How does latency hiding choose block size?
**A:** A multiple of the warp size that fills the SM to target occupancy; latency hiding sweeps 64-512 to find the plateau.

## Q25: What memory optimizations fall under latency hiding?
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the latency hiding toolbox.

## Q26: How does latency hiding scale to multi-GPU?
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; latency hiding keeps per-GPU work identical and overlap transfers.

## Q27: How does latency hiding use streams?
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; latency hiding overlaps host and device work.

## Q28: When is latency hiding over-engineering?
**A:** When the pipeline is still changing daily; latency hiding stabilization is reserved for mature kernels judged by their benchmark suite.

## Q29: What is the best first metric for latency hiding?
**A:** Achieved occupancy and DRAM throughput from Nsight; latency hiding optimization targets whichever is below the theoretical peak.

## Q30: How does latency hiding handle the image write-back?
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; latency hiding avoids read-modify-write penalties.

## Q31: What role does shared memory play in latency hiding?
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so latency hiding boosts cache hits dramatically.

## Q32: How does latency hiding cope with long-ish rays?
**A:** Spatially coherent groups finish similarly; latency hiding sorts/orders work briefly, or simply lets occupancy absorb the imbalance.

## Q33: What is a latency hiding regression test?
**A:** The golden image must not change when latency hiding is tuned; a side-channel checksum asserts identical pixels after each optimization.

## Q34: How does latency hiding treat constant and texture paths?
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; latency hiding chooses the path that reduces traffic.

## Q35: What should be avoided for latency hiding?
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle latency hiding.

## Q36: How do you explain latency hiding impact to a reviewer?
**A:** Show before/after Nsight categories and frame times; latency hiding communicates in measured evidence rather than opinion.

## Q37: What is the latency hiding budget for a movie frame?
**A:** If 1 second per frame is acceptable at 30 fps, latency hiding leaves ~33 ms; most pipelines budget a bit more and render offline with a farm.

## Q38: Where should latency hiding stop?
**A:** Once no profile category dominates and further gains are under a few percent, latency hiding stops and the remaining money goes to more samples.

## Q39: Where should latency hiding stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, latency hiding stops and the remaining money goes to more samples. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: What is the latency hiding budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, latency hiding leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: How do you explain latency hiding impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; latency hiding communicates in measured evidence rather than opinion. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What should be avoided for latency hiding - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle latency hiding. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How does latency hiding treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; latency hiding chooses the path that reduces traffic. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What is a latency hiding regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when latency hiding is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: How does latency hiding cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; latency hiding sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What role does shared memory play in latency hiding - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so latency hiding boosts cache hits dramatically. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How does latency hiding handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; latency hiding avoids read-modify-write penalties. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What is the best first metric for latency hiding - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; latency hiding optimization targets whichever is below the theoretical peak. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: When is latency hiding over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; latency hiding stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How does latency hiding use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; latency hiding overlaps host and device work. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How does latency hiding scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; latency hiding keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What memory optimizations fall under latency hiding - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the latency hiding toolbox. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: How does latency hiding choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; latency hiding sweeps 64-512 to find the plateau. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How is latency hiding measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; latency hiding reports both median kernel time and total wall time. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What does latency hiding do about divergent geodesic paths - justify your answer with a concrete production example.
**A:** Assign one ray per thread so long and short rays simply finish at different times; latency hiding accepts this natural load imbalance. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How does latency hiding handle determinism - justify your answer with a concrete production example.
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep latency hiding results reproducible while still fast. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What is a typical 90/10 latency hiding rule - justify your answer with a concrete production example.
**A:** 10% of the kernel is 90% of the runtime; latency hiding spend begins by identifying and fixing that hot loop, then measuring again. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: How does latency hiding relate to warp occupancy - justify your answer with a concrete production example.
**A:** More resident warps hide more latency, but registers/shared memory limit it; latency hiding balances occupancy against per-thread state. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What is the first thing to fix under latency hiding - justify your answer with a concrete production example.
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since latency hiding memory stalls dominate. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: How do you profile latency hiding - justify your answer with a concrete production example.
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; latency hiding tuning starts from measured numbers, not guesses. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: Why does latency hiding matter more than FLOPs for raytracing - justify your answer with a concrete production example.
**A:** Ray integration is memory- and latency-bound; latency hiding targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: What does latency hiding mean for the raytracer's runtime - justify your answer with a concrete production example.
**A:** It is the lever that turns a working kernel into a fast one; latency hiding improvements typically change frame times by 2-10x with identical output. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does latency hiding mean for the raytracer's runtime - justify your answer with a concrete production example.
**A:** It is the lever that turns a working kernel into a fast one; latency hiding improvements typically change frame times by 2-10x with identical output. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: Why does latency hiding matter more than FLOPs for raytracing - justify your answer with a concrete production example.
**A:** Ray integration is memory- and latency-bound; latency hiding targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: How do you profile latency hiding - justify your answer with a concrete production example.
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; latency hiding tuning starts from measured numbers, not guesses. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is the first thing to fix under latency hiding - justify your answer with a concrete production example.
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since latency hiding memory stalls dominate. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How does latency hiding relate to warp occupancy - justify your answer with a concrete production example.
**A:** More resident warps hide more latency, but registers/shared memory limit it; latency hiding balances occupancy against per-thread state. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What is a typical 90/10 latency hiding rule - justify your answer with a concrete production example.
**A:** 10% of the kernel is 90% of the runtime; latency hiding spend begins by identifying and fixing that hot loop, then measuring again. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How does latency hiding handle determinism - justify your answer with a concrete production example.
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep latency hiding results reproducible while still fast. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What does latency hiding do about divergent geodesic paths - justify your answer with a concrete production example.
**A:** Assign one ray per thread so long and short rays simply finish at different times; latency hiding accepts this natural load imbalance. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How is latency hiding measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; latency hiding reports both median kernel time and total wall time. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: How does latency hiding choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; latency hiding sweeps 64-512 to find the plateau. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: What memory optimizations fall under latency hiding - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the latency hiding toolbox. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: How does latency hiding scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; latency hiding keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How does latency hiding use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; latency hiding overlaps host and device work. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: When is latency hiding over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; latency hiding stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What is the best first metric for latency hiding - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; latency hiding optimization targets whichever is below the theoretical peak. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How does latency hiding handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; latency hiding avoids read-modify-write penalties. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What role does shared memory play in latency hiding - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so latency hiding boosts cache hits dramatically. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does latency hiding cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; latency hiding sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: What is a latency hiding regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when latency hiding is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: How does latency hiding treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; latency hiding chooses the path that reduces traffic. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What should be avoided for latency hiding - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle latency hiding. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: How do you explain latency hiding impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; latency hiding communicates in measured evidence rather than opinion. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What is the latency hiding budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, latency hiding leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: Where should latency hiding stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, latency hiding stops and the remaining money goes to more samples. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: Where should latency hiding stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, latency hiding stops and the remaining money goes to more samples. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What is the latency hiding budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, latency hiding leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: How do you explain latency hiding impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; latency hiding communicates in measured evidence rather than opinion. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What should be avoided for latency hiding - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle latency hiding. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How does latency hiding treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; latency hiding chooses the path that reduces traffic. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What is a latency hiding regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when latency hiding is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: How does latency hiding cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; latency hiding sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What role does shared memory play in latency hiding - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so latency hiding boosts cache hits dramatically. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How does latency hiding handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; latency hiding avoids read-modify-write penalties. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What is the best first metric for latency hiding - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; latency hiding optimization targets whichever is below the theoretical peak. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: When is latency hiding over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; latency hiding stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How does latency hiding use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; latency hiding overlaps host and device work. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How does latency hiding scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; latency hiding keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What memory optimizations fall under latency hiding - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the latency hiding toolbox. A concrete example: consistently applying latency hiding in code review and regression tests keeps the whole pipeline trustworthy.
