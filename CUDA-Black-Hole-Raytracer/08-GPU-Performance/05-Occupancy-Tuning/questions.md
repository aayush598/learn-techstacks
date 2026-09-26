# Gpu Performance — Occupancy Tuning Interview Questions and Answers

## Q1: What is occupancy?
**A:** The ratio of active warps to the SM's maximum possible warps; high occupancy maximizes the chance the SM has work while any warp stalls.

## Q2: What limits occupancy in the raytracer?
**A:** Registers per thread (large phase-space state), shared-memory per block (field slabs), and the block/grid limits - measure which constrains first.

## Q3: What is the 50% vs 100% myth?
**A:** Full occupancy isn't always best: a kernel needing few warps to hide its short latency loses performance to cache thrash at 100% - find YOUR sweet spot.

## Q4: What is the field-cache vs occupancy tradeoff?
**A:** Big shared tiles raise occupancy pressure but cut memory traffic; a 70%-occupancy high-reuse config can beat 100%-occupancy sparse-cache configs.

## Q5: How do you measure achieved occupancy?
**A:** Nsight Compute's 'Achieved Occupancy' (actual average) vs 'Theoretical' - divergence and tail effects drag achieved below theoretical; fix those.

## Q6: What is the register-pressure lever?
**A:** Add __launch_bounds__(threads, blocks_per_sm) hint: it limits the compiler's register budget per thread, freeing blocks/SM at the cost of spills - test it.

## Q7: What is the tail effect?
**A:** The last partial wave of rays runs with a fraction of the occupancy - balance blocks to fill warps or adaptive grids to near-full tails.

## Q8: How do you size the ray batch per launch?
**A:** Choose rays_per_block so allocated registers+shared allow e.g. 4-8 blocks/SM; grid = ceil(pixels / block_rays) keeps every SM busy.

## Q9: What is occupancy's role in the RTE loop?
**A:** The transfer sampling touches many fields; without resident warps, each field fetch becomes a full stall serialization - occupancy is the transfer's shield.

## Q10: What is the multi-kernel story?
**A:** Geodesic-step and accumulation kernels each have different register/shared needs; tune occupancy PER KERNEL, not per program - the profiler per-kernel view.

## Q11: How does dynamic parallelism interact?
**A:** Child kernels from a parent (e.g., octree refinement) inherit the parent's occupancy budget - keep grid sizing explicit, avoid surprise nesting.

## Q12: What is the determinism effect?
**A:** Block-grid scheduling order can vary with occupancy; pin the launch config and the reduction order to keep frame-to-frame reproducibility.

## Q13: What is the validation loop for occupancy?
**A:** Sweep rays/block 32..1024 and measure rays/s; plot the knee ('range of optimal') and choose the robust plateau, not the single best sample.

## Q14: What is the summary?
**A:** Occupancy tuning is the balancing of warps-resident vs per-thread resource use - measured per kernel, plateau-picked, and never assumed at 100%.

## Q15: What does occupancy tuning mean for the raytracer's runtime?
**A:** It is the lever that turns a working kernel into a fast one; occupancy tuning improvements typically change frame times by 2-10x with identical output.

## Q16: Why does occupancy tuning matter more than FLOPs for raytracing?
**A:** Ray integration is memory- and latency-bound; occupancy tuning targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins.

## Q17: How do you profile occupancy tuning?
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; occupancy tuning tuning starts from measured numbers, not guesses.

## Q18: What is the first thing to fix under occupancy tuning?
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since occupancy tuning memory stalls dominate.

## Q19: How does occupancy tuning relate to warp occupancy?
**A:** More resident warps hide more latency, but registers/shared memory limit it; occupancy tuning balances occupancy against per-thread state.

## Q20: What is a typical 90/10 occupancy tuning rule?
**A:** 10% of the kernel is 90% of the runtime; occupancy tuning spend begins by identifying and fixing that hot loop, then measuring again.

## Q21: How does occupancy tuning handle determinism?
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep occupancy tuning results reproducible while still fast.

## Q22: What does occupancy tuning do about divergent geodesic paths?
**A:** Assign one ray per thread so long and short rays simply finish at different times; occupancy tuning accepts this natural load imbalance.

## Q23: How is occupancy tuning measured end-to-end?
**A:** Frames per second at fixed image size and step policy; occupancy tuning reports both median kernel time and total wall time.

## Q24: How does occupancy tuning choose block size?
**A:** A multiple of the warp size that fills the SM to target occupancy; occupancy tuning sweeps 64-512 to find the plateau.

## Q25: What memory optimizations fall under occupancy tuning?
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the occupancy tuning toolbox.

## Q26: How does occupancy tuning scale to multi-GPU?
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; occupancy tuning keeps per-GPU work identical and overlap transfers.

## Q27: How does occupancy tuning use streams?
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; occupancy tuning overlaps host and device work.

## Q28: When is occupancy tuning over-engineering?
**A:** When the pipeline is still changing daily; occupancy tuning stabilization is reserved for mature kernels judged by their benchmark suite.

## Q29: What is the best first metric for occupancy tuning?
**A:** Achieved occupancy and DRAM throughput from Nsight; occupancy tuning optimization targets whichever is below the theoretical peak.

## Q30: How does occupancy tuning handle the image write-back?
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; occupancy tuning avoids read-modify-write penalties.

## Q31: What role does shared memory play in occupancy tuning?
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so occupancy tuning boosts cache hits dramatically.

## Q32: How does occupancy tuning cope with long-ish rays?
**A:** Spatially coherent groups finish similarly; occupancy tuning sorts/orders work briefly, or simply lets occupancy absorb the imbalance.

## Q33: What is a occupancy tuning regression test?
**A:** The golden image must not change when occupancy tuning is tuned; a side-channel checksum asserts identical pixels after each optimization.

## Q34: How does occupancy tuning treat constant and texture paths?
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; occupancy tuning chooses the path that reduces traffic.

## Q35: What should be avoided for occupancy tuning?
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle occupancy tuning.

## Q36: How do you explain occupancy tuning impact to a reviewer?
**A:** Show before/after Nsight categories and frame times; occupancy tuning communicates in measured evidence rather than opinion.

## Q37: What is the occupancy tuning budget for a movie frame?
**A:** If 1 second per frame is acceptable at 30 fps, occupancy tuning leaves ~33 ms; most pipelines budget a bit more and render offline with a farm.

## Q38: Where should occupancy tuning stop?
**A:** Once no profile category dominates and further gains are under a few percent, occupancy tuning stops and the remaining money goes to more samples.

## Q39: Where should occupancy tuning stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, occupancy tuning stops and the remaining money goes to more samples. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: What is the occupancy tuning budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, occupancy tuning leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: How do you explain occupancy tuning impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; occupancy tuning communicates in measured evidence rather than opinion. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What should be avoided for occupancy tuning - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle occupancy tuning. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How does occupancy tuning treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; occupancy tuning chooses the path that reduces traffic. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What is a occupancy tuning regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when occupancy tuning is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: How does occupancy tuning cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; occupancy tuning sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What role does shared memory play in occupancy tuning - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so occupancy tuning boosts cache hits dramatically. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How does occupancy tuning handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; occupancy tuning avoids read-modify-write penalties. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What is the best first metric for occupancy tuning - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; occupancy tuning optimization targets whichever is below the theoretical peak. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: When is occupancy tuning over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; occupancy tuning stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How does occupancy tuning use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; occupancy tuning overlaps host and device work. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How does occupancy tuning scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; occupancy tuning keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What memory optimizations fall under occupancy tuning - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the occupancy tuning toolbox. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: How does occupancy tuning choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; occupancy tuning sweeps 64-512 to find the plateau. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How is occupancy tuning measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; occupancy tuning reports both median kernel time and total wall time. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What does occupancy tuning do about divergent geodesic paths - justify your answer with a concrete production example.
**A:** Assign one ray per thread so long and short rays simply finish at different times; occupancy tuning accepts this natural load imbalance. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How does occupancy tuning handle determinism - justify your answer with a concrete production example.
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep occupancy tuning results reproducible while still fast. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What is a typical 90/10 occupancy tuning rule - justify your answer with a concrete production example.
**A:** 10% of the kernel is 90% of the runtime; occupancy tuning spend begins by identifying and fixing that hot loop, then measuring again. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: How does occupancy tuning relate to warp occupancy - justify your answer with a concrete production example.
**A:** More resident warps hide more latency, but registers/shared memory limit it; occupancy tuning balances occupancy against per-thread state. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What is the first thing to fix under occupancy tuning - justify your answer with a concrete production example.
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since occupancy tuning memory stalls dominate. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: How do you profile occupancy tuning - justify your answer with a concrete production example.
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; occupancy tuning tuning starts from measured numbers, not guesses. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: Why does occupancy tuning matter more than FLOPs for raytracing - justify your answer with a concrete production example.
**A:** Ray integration is memory- and latency-bound; occupancy tuning targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: What does occupancy tuning mean for the raytracer's runtime - justify your answer with a concrete production example.
**A:** It is the lever that turns a working kernel into a fast one; occupancy tuning improvements typically change frame times by 2-10x with identical output. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What does occupancy tuning mean for the raytracer's runtime - justify your answer with a concrete production example.
**A:** It is the lever that turns a working kernel into a fast one; occupancy tuning improvements typically change frame times by 2-10x with identical output. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: Why does occupancy tuning matter more than FLOPs for raytracing - justify your answer with a concrete production example.
**A:** Ray integration is memory- and latency-bound; occupancy tuning targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: How do you profile occupancy tuning - justify your answer with a concrete production example.
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; occupancy tuning tuning starts from measured numbers, not guesses. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is the first thing to fix under occupancy tuning - justify your answer with a concrete production example.
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since occupancy tuning memory stalls dominate. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How does occupancy tuning relate to warp occupancy - justify your answer with a concrete production example.
**A:** More resident warps hide more latency, but registers/shared memory limit it; occupancy tuning balances occupancy against per-thread state. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What is a typical 90/10 occupancy tuning rule - justify your answer with a concrete production example.
**A:** 10% of the kernel is 90% of the runtime; occupancy tuning spend begins by identifying and fixing that hot loop, then measuring again. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How does occupancy tuning handle determinism - justify your answer with a concrete production example.
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep occupancy tuning results reproducible while still fast. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: What does occupancy tuning do about divergent geodesic paths - justify your answer with a concrete production example.
**A:** Assign one ray per thread so long and short rays simply finish at different times; occupancy tuning accepts this natural load imbalance. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How is occupancy tuning measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; occupancy tuning reports both median kernel time and total wall time. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: How does occupancy tuning choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; occupancy tuning sweeps 64-512 to find the plateau. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: What memory optimizations fall under occupancy tuning - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the occupancy tuning toolbox. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: How does occupancy tuning scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; occupancy tuning keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How does occupancy tuning use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; occupancy tuning overlaps host and device work. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: When is occupancy tuning over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; occupancy tuning stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What is the best first metric for occupancy tuning - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; occupancy tuning optimization targets whichever is below the theoretical peak. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How does occupancy tuning handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; occupancy tuning avoids read-modify-write penalties. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What role does shared memory play in occupancy tuning - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so occupancy tuning boosts cache hits dramatically. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does occupancy tuning cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; occupancy tuning sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: What is a occupancy tuning regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when occupancy tuning is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: How does occupancy tuning treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; occupancy tuning chooses the path that reduces traffic. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What should be avoided for occupancy tuning - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle occupancy tuning. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: How do you explain occupancy tuning impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; occupancy tuning communicates in measured evidence rather than opinion. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What is the occupancy tuning budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, occupancy tuning leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: Where should occupancy tuning stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, occupancy tuning stops and the remaining money goes to more samples. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: Where should occupancy tuning stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, occupancy tuning stops and the remaining money goes to more samples. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What is the occupancy tuning budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, occupancy tuning leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: How do you explain occupancy tuning impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; occupancy tuning communicates in measured evidence rather than opinion. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What should be avoided for occupancy tuning - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle occupancy tuning. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How does occupancy tuning treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; occupancy tuning chooses the path that reduces traffic. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What is a occupancy tuning regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when occupancy tuning is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: How does occupancy tuning cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; occupancy tuning sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What role does shared memory play in occupancy tuning - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so occupancy tuning boosts cache hits dramatically. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How does occupancy tuning handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; occupancy tuning avoids read-modify-write penalties. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What is the best first metric for occupancy tuning - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; occupancy tuning optimization targets whichever is below the theoretical peak. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: When is occupancy tuning over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; occupancy tuning stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How does occupancy tuning use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; occupancy tuning overlaps host and device work. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How does occupancy tuning scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; occupancy tuning keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What memory optimizations fall under occupancy tuning - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the occupancy tuning toolbox. A concrete example: consistently applying occupancy tuning in code review and regression tests keeps the whole pipeline trustworthy.
