# Gpu Performance — Nsight Compute Interview Questions and Answers

## Q1: What is Nsight Compute?
**A:** NVIDIA's per-kernel profiler giving register-level metrics (occupancy, memory throughput, stalls) for each kernel launch - the micro-analyzer of GPU code.

## Q2: How do you use it on a raytracer?
**A:** Profile one representative kernel (geodesic stepping) with a small but valid launch: read its occupancy, memory, and stall sections to guide tuning.

## Q3: What does 'Achieved Occupancy' mean here?
**A:** The actual average warps active across the kernel's execution vs the theoretical cap - divergence/tail effects drop it; it's the health metric of hiding.

## Q4: What are the memory sections?
**A:** Global/Local/Shared throughput percentages, latency tables, and cache-hit stats - tells you exactly which memory path your kernel leans on.

## Q5: What are the stall reasons?
**A:** 'Stall Barrier', 'Stall Long Scoreboard', 'Stall Wait' report what warps wait on - memory (scoreboard) vs sync vs dependencies - each suggests a fix.

## Q6: What is the single-kernel flow?
**A:** Profile -> identify top stall -> make one change (e.g., layout/occupancy) -> re-profile -> accept or revert - the honest, slow, reliable loop.

## Q7: What is 'IPC' (instructions per cycle)?
**A:** SM GPU throughput indicator; >3-4 is healthy for compute-heavy, raytracer loops more like 1.5-3 with memory latency - relative change, not absolute.

## Q8: What are the metric groups to save?
**A:** Save a named metric-group config (occupancy:registers, memory:workload) as a project file - every engineer reprofiles the same columns.

## Q9: How does Nsight Compute help with determinism?
**A:** It attributes per-kernel reads: the same kernel in different runs must report nearly identical metrics - a cheap determinism cross-check.

## Q10: What is the difference from Nsight Systems?
**A:** Systems = system-wide timeline (gaps, overlap); Compute = per-kernel internals (why a kernel is slow) - use Systems to spot, Compute to dig.

## Q11: How do you avoid profiling overhead?
**A:** Profile a reduced render (small resolution, few frames), never the full movie; write results to CSV for post-hoc comparisons.

## Q12: What is the summary?
**A:** Nsight Compute answers 'why is this kernel slow' at the register level - an analytical, measurement-driven companion to the design patterns.

## Q13: What does nsight compute mean for the raytracer's runtime?
**A:** It is the lever that turns a working kernel into a fast one; nsight compute improvements typically change frame times by 2-10x with identical output.

## Q14: Why does nsight compute matter more than FLOPs for raytracing?
**A:** Ray integration is memory- and latency-bound; nsight compute targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins.

## Q15: How do you profile nsight compute?
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; nsight compute tuning starts from measured numbers, not guesses.

## Q16: What is the first thing to fix under nsight compute?
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since nsight compute memory stalls dominate.

## Q17: How does nsight compute relate to warp occupancy?
**A:** More resident warps hide more latency, but registers/shared memory limit it; nsight compute balances occupancy against per-thread state.

## Q18: What is a typical 90/10 nsight compute rule?
**A:** 10% of the kernel is 90% of the runtime; nsight compute spend begins by identifying and fixing that hot loop, then measuring again.

## Q19: How does nsight compute handle determinism?
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep nsight compute results reproducible while still fast.

## Q20: What does nsight compute do about divergent geodesic paths?
**A:** Assign one ray per thread so long and short rays simply finish at different times; nsight compute accepts this natural load imbalance.

## Q21: How is nsight compute measured end-to-end?
**A:** Frames per second at fixed image size and step policy; nsight compute reports both median kernel time and total wall time.

## Q22: How does nsight compute choose block size?
**A:** A multiple of the warp size that fills the SM to target occupancy; nsight compute sweeps 64-512 to find the plateau.

## Q23: What memory optimizations fall under nsight compute?
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the nsight compute toolbox.

## Q24: How does nsight compute scale to multi-GPU?
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; nsight compute keeps per-GPU work identical and overlap transfers.

## Q25: How does nsight compute use streams?
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; nsight compute overlaps host and device work.

## Q26: When is nsight compute over-engineering?
**A:** When the pipeline is still changing daily; nsight compute stabilization is reserved for mature kernels judged by their benchmark suite.

## Q27: What is the best first metric for nsight compute?
**A:** Achieved occupancy and DRAM throughput from Nsight; nsight compute optimization targets whichever is below the theoretical peak.

## Q28: How does nsight compute handle the image write-back?
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; nsight compute avoids read-modify-write penalties.

## Q29: What role does shared memory play in nsight compute?
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so nsight compute boosts cache hits dramatically.

## Q30: How does nsight compute cope with long-ish rays?
**A:** Spatially coherent groups finish similarly; nsight compute sorts/orders work briefly, or simply lets occupancy absorb the imbalance.

## Q31: What is a nsight compute regression test?
**A:** The golden image must not change when nsight compute is tuned; a side-channel checksum asserts identical pixels after each optimization.

## Q32: How does nsight compute treat constant and texture paths?
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; nsight compute chooses the path that reduces traffic.

## Q33: What should be avoided for nsight compute?
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle nsight compute.

## Q34: How do you explain nsight compute impact to a reviewer?
**A:** Show before/after Nsight categories and frame times; nsight compute communicates in measured evidence rather than opinion.

## Q35: What is the nsight compute budget for a movie frame?
**A:** If 1 second per frame is acceptable at 30 fps, nsight compute leaves ~33 ms; most pipelines budget a bit more and render offline with a farm.

## Q36: Where should nsight compute stop?
**A:** Once no profile category dominates and further gains are under a few percent, nsight compute stops and the remaining money goes to more samples.

## Q37: Where should nsight compute stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, nsight compute stops and the remaining money goes to more samples. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q38: What is the nsight compute budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, nsight compute leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q39: How do you explain nsight compute impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; nsight compute communicates in measured evidence rather than opinion. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: What should be avoided for nsight compute - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle nsight compute. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: How does nsight compute treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; nsight compute chooses the path that reduces traffic. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What is a nsight compute regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when nsight compute is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How does nsight compute cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; nsight compute sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What role does shared memory play in nsight compute - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so nsight compute boosts cache hits dramatically. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: How does nsight compute handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; nsight compute avoids read-modify-write penalties. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What is the best first metric for nsight compute - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; nsight compute optimization targets whichever is below the theoretical peak. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: When is nsight compute over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; nsight compute stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How does nsight compute use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; nsight compute overlaps host and device work. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: How does nsight compute scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; nsight compute keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What memory optimizations fall under nsight compute - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the nsight compute toolbox. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How does nsight compute choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; nsight compute sweeps 64-512 to find the plateau. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How is nsight compute measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; nsight compute reports both median kernel time and total wall time. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What does nsight compute do about divergent geodesic paths - justify your answer with a concrete production example.
**A:** Assign one ray per thread so long and short rays simply finish at different times; nsight compute accepts this natural load imbalance. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does nsight compute handle determinism - justify your answer with a concrete production example.
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep nsight compute results reproducible while still fast. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is a typical 90/10 nsight compute rule - justify your answer with a concrete production example.
**A:** 10% of the kernel is 90% of the runtime; nsight compute spend begins by identifying and fixing that hot loop, then measuring again. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How does nsight compute relate to warp occupancy - justify your answer with a concrete production example.
**A:** More resident warps hide more latency, but registers/shared memory limit it; nsight compute balances occupancy against per-thread state. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What is the first thing to fix under nsight compute - justify your answer with a concrete production example.
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since nsight compute memory stalls dominate. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: How do you profile nsight compute - justify your answer with a concrete production example.
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; nsight compute tuning starts from measured numbers, not guesses. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: Why does nsight compute matter more than FLOPs for raytracing - justify your answer with a concrete production example.
**A:** Ray integration is memory- and latency-bound; nsight compute targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What does nsight compute mean for the raytracer's runtime - justify your answer with a concrete production example.
**A:** It is the lever that turns a working kernel into a fast one; nsight compute improvements typically change frame times by 2-10x with identical output. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What does nsight compute mean for the raytracer's runtime - justify your answer with a concrete production example.
**A:** It is the lever that turns a working kernel into a fast one; nsight compute improvements typically change frame times by 2-10x with identical output. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why does nsight compute matter more than FLOPs for raytracing - justify your answer with a concrete production example.
**A:** Ray integration is memory- and latency-bound; nsight compute targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: How do you profile nsight compute - justify your answer with a concrete production example.
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; nsight compute tuning starts from measured numbers, not guesses. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What is the first thing to fix under nsight compute - justify your answer with a concrete production example.
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since nsight compute memory stalls dominate. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: How does nsight compute relate to warp occupancy - justify your answer with a concrete production example.
**A:** More resident warps hide more latency, but registers/shared memory limit it; nsight compute balances occupancy against per-thread state. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is a typical 90/10 nsight compute rule - justify your answer with a concrete production example.
**A:** 10% of the kernel is 90% of the runtime; nsight compute spend begins by identifying and fixing that hot loop, then measuring again. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How does nsight compute handle determinism - justify your answer with a concrete production example.
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep nsight compute results reproducible while still fast. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What does nsight compute do about divergent geodesic paths - justify your answer with a concrete production example.
**A:** Assign one ray per thread so long and short rays simply finish at different times; nsight compute accepts this natural load imbalance. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How is nsight compute measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; nsight compute reports both median kernel time and total wall time. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How does nsight compute choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; nsight compute sweeps 64-512 to find the plateau. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What memory optimizations fall under nsight compute - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the nsight compute toolbox. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: How does nsight compute scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; nsight compute keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does nsight compute use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; nsight compute overlaps host and device work. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: When is nsight compute over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; nsight compute stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What is the best first metric for nsight compute - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; nsight compute optimization targets whichever is below the theoretical peak. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How does nsight compute handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; nsight compute avoids read-modify-write penalties. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What role does shared memory play in nsight compute - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so nsight compute boosts cache hits dramatically. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How does nsight compute cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; nsight compute sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What is a nsight compute regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when nsight compute is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does nsight compute treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; nsight compute chooses the path that reduces traffic. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: What should be avoided for nsight compute - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle nsight compute. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: How do you explain nsight compute impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; nsight compute communicates in measured evidence rather than opinion. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What is the nsight compute budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, nsight compute leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: Where should nsight compute stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, nsight compute stops and the remaining money goes to more samples. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: Where should nsight compute stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, nsight compute stops and the remaining money goes to more samples. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the nsight compute budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, nsight compute leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How do you explain nsight compute impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; nsight compute communicates in measured evidence rather than opinion. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What should be avoided for nsight compute - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle nsight compute. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: How does nsight compute treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; nsight compute chooses the path that reduces traffic. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What is a nsight compute regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when nsight compute is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How does nsight compute cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; nsight compute sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What role does shared memory play in nsight compute - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so nsight compute boosts cache hits dramatically. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: How does nsight compute handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; nsight compute avoids read-modify-write penalties. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What is the best first metric for nsight compute - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; nsight compute optimization targets whichever is below the theoretical peak. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: When is nsight compute over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; nsight compute stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How does nsight compute use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; nsight compute overlaps host and device work. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: How does nsight compute scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; nsight compute keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What memory optimizations fall under nsight compute - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the nsight compute toolbox. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How does nsight compute choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; nsight compute sweeps 64-512 to find the plateau. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How is nsight compute measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; nsight compute reports both median kernel time and total wall time. A concrete example: consistently applying nsight compute in code review and regression tests keeps the whole pipeline trustworthy.
