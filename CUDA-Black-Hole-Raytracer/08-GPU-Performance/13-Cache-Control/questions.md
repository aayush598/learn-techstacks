# Gpu Performance — Cache Control Interview Questions and Answers

## Q1: What does cache control mean on a GPU?
**A:** Guiding L1/L2/texture behavior per access - which data stays cached, which streams - via const restrict, __ldg, inline PTX, or grid-control hints.

## Q2: What is the read-only cache (__ldg)?
**A:** Kernels read immutable field data through the read-only data cache: __ldg(&field[i]) bypasses the writable path - better hit rate for grid/texture-like arrays.

## Q3: What is 'const __restrict__'?
**A:** Marking pointer parameters const __restrict__ lets the compiler issue read-only loads and wide vector accesses - free wins on hot kernels.

## Q4: What is the texture-path for fields?
**A:** Global arrays bound as textures get dedicated caches + hardware filtering; trilinear sampling becomes fire-and-forget — the field natural home.

## Q5: What does 'cudaFuncSetAttribute' allow?
**A:** The preferred cache config (L1 vs shared split, or 'L1-only') tunes the silicon's on-chip budget to the kernel's fetches - e.g., more L1 for field reads.

## Q6: What is the L2 policy effort?
**A:** cudaStreamSetAttribute/property-based 'persisting' hints keep the hottest field slab (ring) resident in L2 across many tiles.

## Q7: What is the directive vs reality caveat?
**A:** Cache POLICIES are hints; the real eviction is hardware-driven - the only truth is measured hit rates (Compute's 'L1 Hit Rate').

## Q8: What is the 'hot slab' reuse pattern?
**A:** The ring's field slice is touched by many tiles; keep it cached (L2-persist) while streaming the outer-disk slabs - a classic two-region memory diet.

## Q9: What is the translation of a CPU habit (preach locality)?
**A:** The GPU analog: warp-coherent accesses (same neighborhood) maximize a single cached line serving many lanes - same principle, translated.

## Q10: What are eviction-friendly patterns?
**A:** Huge, read-once arrays (e.g., per-frame emission cache) should stream and NOT pollute: load via __ldg with cache() spills or reuse small rings instead.

## Q11: What is the deterministic hazard?
**A:** Cache hints can change float ordering slightly (FMA/load scheduling) - if frames must be bit-reproducible, pin the hint set consistently.

## Q12: What is the summary?
**A:** Cache control steers the on-chip memory diet - const-restrict/read-only loads for fields, texture paths for filtering, and L2-persist hints for the hot ring slab.

## Q13: What does cache control mean for the raytracer's runtime?
**A:** It is the lever that turns a working kernel into a fast one; cache control improvements typically change frame times by 2-10x with identical output.

## Q14: Why does cache control matter more than FLOPs for raytracing?
**A:** Ray integration is memory- and latency-bound; cache control targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins.

## Q15: How do you profile cache control?
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; cache control tuning starts from measured numbers, not guesses.

## Q16: What is the first thing to fix under cache control?
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since cache control memory stalls dominate.

## Q17: How does cache control relate to warp occupancy?
**A:** More resident warps hide more latency, but registers/shared memory limit it; cache control balances occupancy against per-thread state.

## Q18: What is a typical 90/10 cache control rule?
**A:** 10% of the kernel is 90% of the runtime; cache control spend begins by identifying and fixing that hot loop, then measuring again.

## Q19: How does cache control handle determinism?
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep cache control results reproducible while still fast.

## Q20: What does cache control do about divergent geodesic paths?
**A:** Assign one ray per thread so long and short rays simply finish at different times; cache control accepts this natural load imbalance.

## Q21: How is cache control measured end-to-end?
**A:** Frames per second at fixed image size and step policy; cache control reports both median kernel time and total wall time.

## Q22: How does cache control choose block size?
**A:** A multiple of the warp size that fills the SM to target occupancy; cache control sweeps 64-512 to find the plateau.

## Q23: What memory optimizations fall under cache control?
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the cache control toolbox.

## Q24: How does cache control scale to multi-GPU?
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; cache control keeps per-GPU work identical and overlap transfers.

## Q25: How does cache control use streams?
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; cache control overlaps host and device work.

## Q26: When is cache control over-engineering?
**A:** When the pipeline is still changing daily; cache control stabilization is reserved for mature kernels judged by their benchmark suite.

## Q27: What is the best first metric for cache control?
**A:** Achieved occupancy and DRAM throughput from Nsight; cache control optimization targets whichever is below the theoretical peak.

## Q28: How does cache control handle the image write-back?
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; cache control avoids read-modify-write penalties.

## Q29: What role does shared memory play in cache control?
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so cache control boosts cache hits dramatically.

## Q30: How does cache control cope with long-ish rays?
**A:** Spatially coherent groups finish similarly; cache control sorts/orders work briefly, or simply lets occupancy absorb the imbalance.

## Q31: What is a cache control regression test?
**A:** The golden image must not change when cache control is tuned; a side-channel checksum asserts identical pixels after each optimization.

## Q32: How does cache control treat constant and texture paths?
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; cache control chooses the path that reduces traffic.

## Q33: What should be avoided for cache control?
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle cache control.

## Q34: How do you explain cache control impact to a reviewer?
**A:** Show before/after Nsight categories and frame times; cache control communicates in measured evidence rather than opinion.

## Q35: What is the cache control budget for a movie frame?
**A:** If 1 second per frame is acceptable at 30 fps, cache control leaves ~33 ms; most pipelines budget a bit more and render offline with a farm.

## Q36: Where should cache control stop?
**A:** Once no profile category dominates and further gains are under a few percent, cache control stops and the remaining money goes to more samples.

## Q37: Where should cache control stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, cache control stops and the remaining money goes to more samples. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q38: What is the cache control budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, cache control leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q39: How do you explain cache control impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; cache control communicates in measured evidence rather than opinion. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: What should be avoided for cache control - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle cache control. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: How does cache control treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; cache control chooses the path that reduces traffic. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What is a cache control regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when cache control is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How does cache control cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; cache control sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What role does shared memory play in cache control - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so cache control boosts cache hits dramatically. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: How does cache control handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; cache control avoids read-modify-write penalties. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What is the best first metric for cache control - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; cache control optimization targets whichever is below the theoretical peak. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: When is cache control over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; cache control stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How does cache control use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; cache control overlaps host and device work. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: How does cache control scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; cache control keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What memory optimizations fall under cache control - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the cache control toolbox. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How does cache control choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; cache control sweeps 64-512 to find the plateau. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How is cache control measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; cache control reports both median kernel time and total wall time. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What does cache control do about divergent geodesic paths - justify your answer with a concrete production example.
**A:** Assign one ray per thread so long and short rays simply finish at different times; cache control accepts this natural load imbalance. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does cache control handle determinism - justify your answer with a concrete production example.
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep cache control results reproducible while still fast. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is a typical 90/10 cache control rule - justify your answer with a concrete production example.
**A:** 10% of the kernel is 90% of the runtime; cache control spend begins by identifying and fixing that hot loop, then measuring again. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How does cache control relate to warp occupancy - justify your answer with a concrete production example.
**A:** More resident warps hide more latency, but registers/shared memory limit it; cache control balances occupancy against per-thread state. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What is the first thing to fix under cache control - justify your answer with a concrete production example.
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since cache control memory stalls dominate. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: How do you profile cache control - justify your answer with a concrete production example.
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; cache control tuning starts from measured numbers, not guesses. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: Why does cache control matter more than FLOPs for raytracing - justify your answer with a concrete production example.
**A:** Ray integration is memory- and latency-bound; cache control targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What does cache control mean for the raytracer's runtime - justify your answer with a concrete production example.
**A:** It is the lever that turns a working kernel into a fast one; cache control improvements typically change frame times by 2-10x with identical output. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What does cache control mean for the raytracer's runtime - justify your answer with a concrete production example.
**A:** It is the lever that turns a working kernel into a fast one; cache control improvements typically change frame times by 2-10x with identical output. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why does cache control matter more than FLOPs for raytracing - justify your answer with a concrete production example.
**A:** Ray integration is memory- and latency-bound; cache control targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: How do you profile cache control - justify your answer with a concrete production example.
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; cache control tuning starts from measured numbers, not guesses. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What is the first thing to fix under cache control - justify your answer with a concrete production example.
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since cache control memory stalls dominate. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: How does cache control relate to warp occupancy - justify your answer with a concrete production example.
**A:** More resident warps hide more latency, but registers/shared memory limit it; cache control balances occupancy against per-thread state. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is a typical 90/10 cache control rule - justify your answer with a concrete production example.
**A:** 10% of the kernel is 90% of the runtime; cache control spend begins by identifying and fixing that hot loop, then measuring again. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How does cache control handle determinism - justify your answer with a concrete production example.
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep cache control results reproducible while still fast. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What does cache control do about divergent geodesic paths - justify your answer with a concrete production example.
**A:** Assign one ray per thread so long and short rays simply finish at different times; cache control accepts this natural load imbalance. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How is cache control measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; cache control reports both median kernel time and total wall time. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How does cache control choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; cache control sweeps 64-512 to find the plateau. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What memory optimizations fall under cache control - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the cache control toolbox. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: How does cache control scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; cache control keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does cache control use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; cache control overlaps host and device work. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: When is cache control over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; cache control stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What is the best first metric for cache control - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; cache control optimization targets whichever is below the theoretical peak. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How does cache control handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; cache control avoids read-modify-write penalties. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What role does shared memory play in cache control - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so cache control boosts cache hits dramatically. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How does cache control cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; cache control sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What is a cache control regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when cache control is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does cache control treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; cache control chooses the path that reduces traffic. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: What should be avoided for cache control - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle cache control. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: How do you explain cache control impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; cache control communicates in measured evidence rather than opinion. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What is the cache control budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, cache control leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: Where should cache control stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, cache control stops and the remaining money goes to more samples. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: Where should cache control stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, cache control stops and the remaining money goes to more samples. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the cache control budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, cache control leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How do you explain cache control impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; cache control communicates in measured evidence rather than opinion. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What should be avoided for cache control - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle cache control. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: How does cache control treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; cache control chooses the path that reduces traffic. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What is a cache control regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when cache control is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How does cache control cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; cache control sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What role does shared memory play in cache control - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so cache control boosts cache hits dramatically. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: How does cache control handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; cache control avoids read-modify-write penalties. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What is the best first metric for cache control - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; cache control optimization targets whichever is below the theoretical peak. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: When is cache control over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; cache control stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How does cache control use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; cache control overlaps host and device work. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: How does cache control scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; cache control keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What memory optimizations fall under cache control - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the cache control toolbox. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How does cache control choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; cache control sweeps 64-512 to find the plateau. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How is cache control measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; cache control reports both median kernel time and total wall time. A concrete example: consistently applying cache control in code review and regression tests keeps the whole pipeline trustworthy.
