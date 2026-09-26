# Gpu Performance — Bank Conflicts Interview Questions and Answers

## Q1: What is a bank conflict?
**A:** Shared-memory banks (32 banks, 4-byte words) serve one word per cycle; if multiple threads in a warp hit the SAME bank, the access serializes - a 2x-32x penalty.

## Q2: What causes conflicts in a raytracer?
**A:** Interleaved field slabs with a stride that maps columns to repeated banks, or per-thread lookup tables indexed by the same lane-dependent arithmetic.

## Q3: What is the classic conflict formula?
**A:** Address i maps to bank (address/4) mod 32; a stride of 32 floats collides every lane -> 32-way serialization - one of the worst silent degradations.

## Q4: How do you avoid them - padding?
**A:** Add +1 (unused) column to each row: address = row*(N+1)+col maps columns to distinct banks, eliminating the conflict for row-major access.

## Q5: How do you vectorize around conflicts?
**A:** float4 loads spread across alignment; shared banks are 4-byte, so a 16-byte float4 strides collide differently - mixing access widths is a tuning lever.

## Q6: What does the compiler do about conflicts?
**A:** The compiler often handles broadcast (all lanes same bank, same address) for free; patterns it can't prove stay serialized - write conflict-free layouts.

## Q7: How do you detect conflicts?
**A:** Nsight Compute's 'Memory Workload Analysis' reports shared bank conflict reuses/stalls; a large 'Bank Conflict' count on the hot kernel is a smoking gun.

## Q8: What is a compute-around strategy?
**A:** Pre-transpose or store the field in column-major, or duplicate with offsets - restructuring data beats removing conflicts arithmetic-wise.

## Q9: What about texture/surface conflicts?
**A:** Texture cache has no bank conflicts (HW handles); this is why texture-based field sampling sidesteps shared-memory bank drama entirely.

## Q10: What is the 64-bit twist?
**A:** Double-precision shared arrays use 8-byte words; a warp reads 2 banks per value - stride must be 4-float-aligned to avoid 2-way conflicts.

## Q11: What does an occupancy compromise look like?
**A:** Padding to avoid conflicts increases shared usage slightly; a 1-2% occupancy loss is usually worth a 16x serialization removal.

## Q12: What is the validation methodology?
**A:** Toggle the padded layout A/B; measure kernel time and bank-conflict count in the roadmap - never assume the fixed layout, measure it.

## Q13: What is the summary?
**A:** Bank conflicts are shared-memory's silent tax - pad layouts, prefer texture sampling, and verify with Nsight - it is a 32x swing hiding in a stride.

## Q14: What does bank conflicts mean for the raytracer's runtime?
**A:** It is the lever that turns a working kernel into a fast one; bank conflicts improvements typically change frame times by 2-10x with identical output.

## Q15: Why does bank conflicts matter more than FLOPs for raytracing?
**A:** Ray integration is memory- and latency-bound; bank conflicts targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins.

## Q16: How do you profile bank conflicts?
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; bank conflicts tuning starts from measured numbers, not guesses.

## Q17: What is the first thing to fix under bank conflicts?
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since bank conflicts memory stalls dominate.

## Q18: How does bank conflicts relate to warp occupancy?
**A:** More resident warps hide more latency, but registers/shared memory limit it; bank conflicts balances occupancy against per-thread state.

## Q19: What is a typical 90/10 bank conflicts rule?
**A:** 10% of the kernel is 90% of the runtime; bank conflicts spend begins by identifying and fixing that hot loop, then measuring again.

## Q20: How does bank conflicts handle determinism?
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep bank conflicts results reproducible while still fast.

## Q21: What does bank conflicts do about divergent geodesic paths?
**A:** Assign one ray per thread so long and short rays simply finish at different times; bank conflicts accepts this natural load imbalance.

## Q22: How is bank conflicts measured end-to-end?
**A:** Frames per second at fixed image size and step policy; bank conflicts reports both median kernel time and total wall time.

## Q23: How does bank conflicts choose block size?
**A:** A multiple of the warp size that fills the SM to target occupancy; bank conflicts sweeps 64-512 to find the plateau.

## Q24: What memory optimizations fall under bank conflicts?
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the bank conflicts toolbox.

## Q25: How does bank conflicts scale to multi-GPU?
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; bank conflicts keeps per-GPU work identical and overlap transfers.

## Q26: How does bank conflicts use streams?
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; bank conflicts overlaps host and device work.

## Q27: When is bank conflicts over-engineering?
**A:** When the pipeline is still changing daily; bank conflicts stabilization is reserved for mature kernels judged by their benchmark suite.

## Q28: What is the best first metric for bank conflicts?
**A:** Achieved occupancy and DRAM throughput from Nsight; bank conflicts optimization targets whichever is below the theoretical peak.

## Q29: How does bank conflicts handle the image write-back?
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; bank conflicts avoids read-modify-write penalties.

## Q30: What role does shared memory play in bank conflicts?
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so bank conflicts boosts cache hits dramatically.

## Q31: How does bank conflicts cope with long-ish rays?
**A:** Spatially coherent groups finish similarly; bank conflicts sorts/orders work briefly, or simply lets occupancy absorb the imbalance.

## Q32: What is a bank conflicts regression test?
**A:** The golden image must not change when bank conflicts is tuned; a side-channel checksum asserts identical pixels after each optimization.

## Q33: How does bank conflicts treat constant and texture paths?
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; bank conflicts chooses the path that reduces traffic.

## Q34: What should be avoided for bank conflicts?
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle bank conflicts.

## Q35: How do you explain bank conflicts impact to a reviewer?
**A:** Show before/after Nsight categories and frame times; bank conflicts communicates in measured evidence rather than opinion.

## Q36: What is the bank conflicts budget for a movie frame?
**A:** If 1 second per frame is acceptable at 30 fps, bank conflicts leaves ~33 ms; most pipelines budget a bit more and render offline with a farm.

## Q37: Where should bank conflicts stop?
**A:** Once no profile category dominates and further gains are under a few percent, bank conflicts stops and the remaining money goes to more samples.

## Q38: Where should bank conflicts stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, bank conflicts stops and the remaining money goes to more samples. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q39: What is the bank conflicts budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, bank conflicts leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: How do you explain bank conflicts impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; bank conflicts communicates in measured evidence rather than opinion. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What should be avoided for bank conflicts - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle bank conflicts. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does bank conflicts treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; bank conflicts chooses the path that reduces traffic. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What is a bank conflicts regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when bank conflicts is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How does bank conflicts cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; bank conflicts sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What role does shared memory play in bank conflicts - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so bank conflicts boosts cache hits dramatically. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does bank conflicts handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; bank conflicts avoids read-modify-write penalties. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What is the best first metric for bank conflicts - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; bank conflicts optimization targets whichever is below the theoretical peak. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: When is bank conflicts over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; bank conflicts stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: How does bank conflicts use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; bank conflicts overlaps host and device work. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How does bank conflicts scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; bank conflicts keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What memory optimizations fall under bank conflicts - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the bank conflicts toolbox. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How does bank conflicts choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; bank conflicts sweeps 64-512 to find the plateau. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: How is bank conflicts measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; bank conflicts reports both median kernel time and total wall time. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: What does bank conflicts do about divergent geodesic paths - justify your answer with a concrete production example.
**A:** Assign one ray per thread so long and short rays simply finish at different times; bank conflicts accepts this natural load imbalance. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: How does bank conflicts handle determinism - justify your answer with a concrete production example.
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep bank conflicts results reproducible while still fast. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What is a typical 90/10 bank conflicts rule - justify your answer with a concrete production example.
**A:** 10% of the kernel is 90% of the runtime; bank conflicts spend begins by identifying and fixing that hot loop, then measuring again. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does bank conflicts relate to warp occupancy - justify your answer with a concrete production example.
**A:** More resident warps hide more latency, but registers/shared memory limit it; bank conflicts balances occupancy against per-thread state. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the first thing to fix under bank conflicts - justify your answer with a concrete production example.
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since bank conflicts memory stalls dominate. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How do you profile bank conflicts - justify your answer with a concrete production example.
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; bank conflicts tuning starts from measured numbers, not guesses. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: Why does bank conflicts matter more than FLOPs for raytracing - justify your answer with a concrete production example.
**A:** Ray integration is memory- and latency-bound; bank conflicts targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What does bank conflicts mean for the raytracer's runtime - justify your answer with a concrete production example.
**A:** It is the lever that turns a working kernel into a fast one; bank conflicts improvements typically change frame times by 2-10x with identical output. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: What does bank conflicts mean for the raytracer's runtime - justify your answer with a concrete production example.
**A:** It is the lever that turns a working kernel into a fast one; bank conflicts improvements typically change frame times by 2-10x with identical output. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: Why does bank conflicts matter more than FLOPs for raytracing - justify your answer with a concrete production example.
**A:** Ray integration is memory- and latency-bound; bank conflicts targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: How do you profile bank conflicts - justify your answer with a concrete production example.
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; bank conflicts tuning starts from measured numbers, not guesses. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: What is the first thing to fix under bank conflicts - justify your answer with a concrete production example.
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since bank conflicts memory stalls dominate. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How does bank conflicts relate to warp occupancy - justify your answer with a concrete production example.
**A:** More resident warps hide more latency, but registers/shared memory limit it; bank conflicts balances occupancy against per-thread state. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What is a typical 90/10 bank conflicts rule - justify your answer with a concrete production example.
**A:** 10% of the kernel is 90% of the runtime; bank conflicts spend begins by identifying and fixing that hot loop, then measuring again. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How does bank conflicts handle determinism - justify your answer with a concrete production example.
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep bank conflicts results reproducible while still fast. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What does bank conflicts do about divergent geodesic paths - justify your answer with a concrete production example.
**A:** Assign one ray per thread so long and short rays simply finish at different times; bank conflicts accepts this natural load imbalance. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How is bank conflicts measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; bank conflicts reports both median kernel time and total wall time. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How does bank conflicts choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; bank conflicts sweeps 64-512 to find the plateau. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What memory optimizations fall under bank conflicts - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the bank conflicts toolbox. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does bank conflicts scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; bank conflicts keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: How does bank conflicts use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; bank conflicts overlaps host and device work. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: When is bank conflicts over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; bank conflicts stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What is the best first metric for bank conflicts - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; bank conflicts optimization targets whichever is below the theoretical peak. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How does bank conflicts handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; bank conflicts avoids read-modify-write penalties. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What role does shared memory play in bank conflicts - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so bank conflicts boosts cache hits dramatically. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How does bank conflicts cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; bank conflicts sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What is a bank conflicts regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when bank conflicts is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does bank conflicts treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; bank conflicts chooses the path that reduces traffic. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What should be avoided for bank conflicts - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle bank conflicts. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How do you explain bank conflicts impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; bank conflicts communicates in measured evidence rather than opinion. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What is the bank conflicts budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, bank conflicts leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: Where should bank conflicts stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, bank conflicts stops and the remaining money goes to more samples. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: Where should bank conflicts stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, bank conflicts stops and the remaining money goes to more samples. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: What is the bank conflicts budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, bank conflicts leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How do you explain bank conflicts impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; bank conflicts communicates in measured evidence rather than opinion. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What should be avoided for bank conflicts - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle bank conflicts. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does bank conflicts treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; bank conflicts chooses the path that reduces traffic. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What is a bank conflicts regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when bank conflicts is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How does bank conflicts cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; bank conflicts sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What role does shared memory play in bank conflicts - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so bank conflicts boosts cache hits dramatically. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does bank conflicts handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; bank conflicts avoids read-modify-write penalties. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What is the best first metric for bank conflicts - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; bank conflicts optimization targets whichever is below the theoretical peak. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: When is bank conflicts over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; bank conflicts stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: How does bank conflicts use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; bank conflicts overlaps host and device work. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How does bank conflicts scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; bank conflicts keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What memory optimizations fall under bank conflicts - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the bank conflicts toolbox. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How does bank conflicts choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; bank conflicts sweeps 64-512 to find the plateau. A concrete example: consistently applying bank conflicts in code review and regression tests keeps the whole pipeline trustworthy.
