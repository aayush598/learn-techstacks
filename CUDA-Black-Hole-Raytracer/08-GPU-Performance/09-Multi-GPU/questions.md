# Gpu Performance — Multi Gpu Interview Questions and Answers

## Q1: What is the multi-GPU architecture for rendering?
**A:** Parallelism across GPUs: divide the image into contiguous slabs (image-parallel) or the field into spatial chunks (data-parallel) - the classic two models.

## Q2: What is image-parallel multi-GPU?
**A:** Each GPU traces its own horizontal strip of pixels with the SAME scene copy - trivial (no communication during the ray loop), perfect for tiles.

## Q3: What is data-parallel multi-GPU?
**A:** Split the GRMHD field across GPUs; rays migrate/requests cross PCIe/NVLink - harder (needed only when one GPU's memory can't hold the field).

## Q4: What is the P2P (peer-to-peer) path?
**A:** cudaMemcpyPeer across GPU memory directly (NVLink/PCIe P2P) instead of host staging - the fast lane for border exchange in data-parallel mode.

## Q5: What is the frame-buffer reduction issue?
**A:** Each GPU's strip pixels accumulate independently; the final image is a simple concatenation/shift (image-parallel) - no cross-GPU reduction at all.

## Q6: What is the load-balance concern?
**A:** The ring sits at the image center: a center-strip GPU gets harder rays (more steps) - assign strips with estimated workload weights, not equal sizes.

## Q7: What is the 'ray steal / dynamic tile' strategy?
**A:** Dispatch tiles to GPUs as they finish (work-queue) - the simplest robust load balancer; the counter-queue is a single atomic in pinned memory.

## Q8: How do you communicate the output?
**A:** Each GPU writes its strip to its own pinned buffer; the host (or a final gather kernel) concatenates - bit-deterministic if each strip is self-contained.

## Q9: What is NVSwitch/NVLink scaling reality?
**A:** NVLink gives ~600 GB/s between GPUs: data-parallel becomes viable; PCIe 16x (~30 GB/s) is fine for image-parallel only.

## Q10: What is the determinism contract?
**A:** Strip partitioning must not change pixel values (each pixel's rays don't cross strips) - frame reproducibility holds trivially in image-parallel.

## Q11: What does Nsight Systems show in multi-GPU?
**A:** Per-GPU timelines overlap fully when balanced; a straggler (idle GPU) shows as the timeline gap — the load-balancer's scoreboard.

## Q12: What is the scaling test?
**A:** N GPUs -> wall time ~ 1/N (image-parallel) up to the strip tail; verify via a strong-scaling sweep and report speedup vs 1 GPU honestly.

## Q13: What is the summary?
**A:** Multi-GPU = image-parallel strips with a work-queue for balance, P2P only when pushing the field around, and deterministic concatenation at the end.

## Q14: What does multi gpu mean for the raytracer's runtime?
**A:** It is the lever that turns a working kernel into a fast one; multi gpu improvements typically change frame times by 2-10x with identical output.

## Q15: Why does multi gpu matter more than FLOPs for raytracing?
**A:** Ray integration is memory- and latency-bound; multi gpu targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins.

## Q16: How do you profile multi gpu?
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; multi gpu tuning starts from measured numbers, not guesses.

## Q17: What is the first thing to fix under multi gpu?
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since multi gpu memory stalls dominate.

## Q18: How does multi gpu relate to warp occupancy?
**A:** More resident warps hide more latency, but registers/shared memory limit it; multi gpu balances occupancy against per-thread state.

## Q19: What is a typical 90/10 multi gpu rule?
**A:** 10% of the kernel is 90% of the runtime; multi gpu spend begins by identifying and fixing that hot loop, then measuring again.

## Q20: How does multi gpu handle determinism?
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep multi gpu results reproducible while still fast.

## Q21: What does multi gpu do about divergent geodesic paths?
**A:** Assign one ray per thread so long and short rays simply finish at different times; multi gpu accepts this natural load imbalance.

## Q22: How is multi gpu measured end-to-end?
**A:** Frames per second at fixed image size and step policy; multi gpu reports both median kernel time and total wall time.

## Q23: How does multi gpu choose block size?
**A:** A multiple of the warp size that fills the SM to target occupancy; multi gpu sweeps 64-512 to find the plateau.

## Q24: What memory optimizations fall under multi gpu?
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the multi gpu toolbox.

## Q25: How does multi gpu scale to multi-GPU?
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; multi gpu keeps per-GPU work identical and overlap transfers.

## Q26: How does multi gpu use streams?
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; multi gpu overlaps host and device work.

## Q27: When is multi gpu over-engineering?
**A:** When the pipeline is still changing daily; multi gpu stabilization is reserved for mature kernels judged by their benchmark suite.

## Q28: What is the best first metric for multi gpu?
**A:** Achieved occupancy and DRAM throughput from Nsight; multi gpu optimization targets whichever is below the theoretical peak.

## Q29: How does multi gpu handle the image write-back?
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; multi gpu avoids read-modify-write penalties.

## Q30: What role does shared memory play in multi gpu?
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so multi gpu boosts cache hits dramatically.

## Q31: How does multi gpu cope with long-ish rays?
**A:** Spatially coherent groups finish similarly; multi gpu sorts/orders work briefly, or simply lets occupancy absorb the imbalance.

## Q32: What is a multi gpu regression test?
**A:** The golden image must not change when multi gpu is tuned; a side-channel checksum asserts identical pixels after each optimization.

## Q33: How does multi gpu treat constant and texture paths?
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; multi gpu chooses the path that reduces traffic.

## Q34: What should be avoided for multi gpu?
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle multi gpu.

## Q35: How do you explain multi gpu impact to a reviewer?
**A:** Show before/after Nsight categories and frame times; multi gpu communicates in measured evidence rather than opinion.

## Q36: What is the multi gpu budget for a movie frame?
**A:** If 1 second per frame is acceptable at 30 fps, multi gpu leaves ~33 ms; most pipelines budget a bit more and render offline with a farm.

## Q37: Where should multi gpu stop?
**A:** Once no profile category dominates and further gains are under a few percent, multi gpu stops and the remaining money goes to more samples.

## Q38: Where should multi gpu stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, multi gpu stops and the remaining money goes to more samples. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q39: What is the multi gpu budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, multi gpu leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: How do you explain multi gpu impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; multi gpu communicates in measured evidence rather than opinion. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What should be avoided for multi gpu - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle multi gpu. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does multi gpu treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; multi gpu chooses the path that reduces traffic. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: What is a multi gpu regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when multi gpu is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: How does multi gpu cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; multi gpu sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What role does shared memory play in multi gpu - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so multi gpu boosts cache hits dramatically. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How does multi gpu handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; multi gpu avoids read-modify-write penalties. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What is the best first metric for multi gpu - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; multi gpu optimization targets whichever is below the theoretical peak. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: When is multi gpu over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; multi gpu stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: How does multi gpu use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; multi gpu overlaps host and device work. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How does multi gpu scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; multi gpu keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What memory optimizations fall under multi gpu - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the multi gpu toolbox. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How does multi gpu choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; multi gpu sweeps 64-512 to find the plateau. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: How is multi gpu measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; multi gpu reports both median kernel time and total wall time. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: What does multi gpu do about divergent geodesic paths - justify your answer with a concrete production example.
**A:** Assign one ray per thread so long and short rays simply finish at different times; multi gpu accepts this natural load imbalance. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: How does multi gpu handle determinism - justify your answer with a concrete production example.
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep multi gpu results reproducible while still fast. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: What is a typical 90/10 multi gpu rule - justify your answer with a concrete production example.
**A:** 10% of the kernel is 90% of the runtime; multi gpu spend begins by identifying and fixing that hot loop, then measuring again. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How does multi gpu relate to warp occupancy - justify your answer with a concrete production example.
**A:** More resident warps hide more latency, but registers/shared memory limit it; multi gpu balances occupancy against per-thread state. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the first thing to fix under multi gpu - justify your answer with a concrete production example.
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since multi gpu memory stalls dominate. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How do you profile multi gpu - justify your answer with a concrete production example.
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; multi gpu tuning starts from measured numbers, not guesses. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: Why does multi gpu matter more than FLOPs for raytracing - justify your answer with a concrete production example.
**A:** Ray integration is memory- and latency-bound; multi gpu targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What does multi gpu mean for the raytracer's runtime - justify your answer with a concrete production example.
**A:** It is the lever that turns a working kernel into a fast one; multi gpu improvements typically change frame times by 2-10x with identical output. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: What does multi gpu mean for the raytracer's runtime - justify your answer with a concrete production example.
**A:** It is the lever that turns a working kernel into a fast one; multi gpu improvements typically change frame times by 2-10x with identical output. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: Why does multi gpu matter more than FLOPs for raytracing - justify your answer with a concrete production example.
**A:** Ray integration is memory- and latency-bound; multi gpu targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: How do you profile multi gpu - justify your answer with a concrete production example.
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; multi gpu tuning starts from measured numbers, not guesses. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: What is the first thing to fix under multi gpu - justify your answer with a concrete production example.
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since multi gpu memory stalls dominate. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How does multi gpu relate to warp occupancy - justify your answer with a concrete production example.
**A:** More resident warps hide more latency, but registers/shared memory limit it; multi gpu balances occupancy against per-thread state. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What is a typical 90/10 multi gpu rule - justify your answer with a concrete production example.
**A:** 10% of the kernel is 90% of the runtime; multi gpu spend begins by identifying and fixing that hot loop, then measuring again. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How does multi gpu handle determinism - justify your answer with a concrete production example.
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep multi gpu results reproducible while still fast. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: What does multi gpu do about divergent geodesic paths - justify your answer with a concrete production example.
**A:** Assign one ray per thread so long and short rays simply finish at different times; multi gpu accepts this natural load imbalance. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How is multi gpu measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; multi gpu reports both median kernel time and total wall time. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How does multi gpu choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; multi gpu sweeps 64-512 to find the plateau. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What memory optimizations fall under multi gpu - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the multi gpu toolbox. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does multi gpu scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; multi gpu keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: How does multi gpu use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; multi gpu overlaps host and device work. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: When is multi gpu over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; multi gpu stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What is the best first metric for multi gpu - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; multi gpu optimization targets whichever is below the theoretical peak. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: How does multi gpu handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; multi gpu avoids read-modify-write penalties. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What role does shared memory play in multi gpu - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so multi gpu boosts cache hits dramatically. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How does multi gpu cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; multi gpu sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What is a multi gpu regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when multi gpu is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How does multi gpu treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; multi gpu chooses the path that reduces traffic. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What should be avoided for multi gpu - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle multi gpu. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How do you explain multi gpu impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; multi gpu communicates in measured evidence rather than opinion. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What is the multi gpu budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, multi gpu leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: Where should multi gpu stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, multi gpu stops and the remaining money goes to more samples. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: Where should multi gpu stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, multi gpu stops and the remaining money goes to more samples. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: What is the multi gpu budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, multi gpu leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How do you explain multi gpu impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; multi gpu communicates in measured evidence rather than opinion. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What should be avoided for multi gpu - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle multi gpu. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does multi gpu treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; multi gpu chooses the path that reduces traffic. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: What is a multi gpu regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when multi gpu is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: How does multi gpu cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; multi gpu sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What role does shared memory play in multi gpu - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so multi gpu boosts cache hits dramatically. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How does multi gpu handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; multi gpu avoids read-modify-write penalties. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What is the best first metric for multi gpu - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; multi gpu optimization targets whichever is below the theoretical peak. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: When is multi gpu over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; multi gpu stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: How does multi gpu use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; multi gpu overlaps host and device work. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How does multi gpu scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; multi gpu keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What memory optimizations fall under multi gpu - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the multi gpu toolbox. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How does multi gpu choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; multi gpu sweeps 64-512 to find the plateau. A concrete example: consistently applying multi gpu in code review and regression tests keeps the whole pipeline trustworthy.
