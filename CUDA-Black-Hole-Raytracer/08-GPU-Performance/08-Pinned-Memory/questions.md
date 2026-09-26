# Gpu Performance — Pinned Memory Interview Questions and Answers

## Q1: What is pinned (page-locked) memory?
**A:** Host memory allocated with cudaHostAlloc so its pages never swap - the requirement for true async (overlapping) transfers with the GPU.

## Q2: Why can't regular host memory overlap?
**A:** The copy engine needs stable physical pages; unpinned memory forces staged copies through a temporary pinned staging buffer, killing overlap.

## Q3: What is the read-back pattern for frames?
**A:** The render's image floats are written into a pinned buffer and streamed to host while the next frame renders - the overlap thread of the movie pipeline.

## Q4: What is the pinned usage in the raytracer?
**A:** Grid field upload (GRMHD data) and per-frame state are the big pinned transfers; the image result streams back pinned.

## Q5: What is the caution (memory pressure)?
**A:** Pinned memory is a scarce OS resource; over-pinning starves the system for other apps - pin only the orchestrated hot buffers.

## Q6: What is host-side staging vs device-to-device?
**A:** If data stays on device across frames (reuse), D2D copies are far cheaper than host round-trips - pin only what truly crosses the PCIe bus.

## Q7: What are the IPC/peer features?
**A:** cudaMemcpyPeer/cudaMallocManaged replace pinned for multi-GPU in the 09 module; pinned remains the async-overlap staple on one GPU.

## Q8: What is zero-copy?
**A:** Reading pinned (mapped) memory directly from kernels without explicit copies - wins for small, read-once fields; loses for repeated reads (PCIe latency).

## Q9: What is the ordering caution?
**A:** Async writes must be ordered with events so the host-side consumer doesn't read a half-transferred frame - a classic bug when adding overlap.

## Q10: What is the Nsight Systems signature?
**A:** The transfer channels (H2D/D2H) busy while SM kernels idle (or vice versa) - the fix is pinning + streams + balance.

## Q11: What is the size-sweet-point?
**A:** Pin once, reuse many frames; amortized pinning cost across the render loop - a 100 MB GRMHD field pinned once is nothing over 1000 frames.

## Q12: What is the summary?
**A:** Pinned memory is the transport layer of async overlap - pin the hot buffers, stream via events, and keep the PCIe bus busy while SMs render.

## Q13: What does pinned memory mean for the raytracer's runtime?
**A:** It is the lever that turns a working kernel into a fast one; pinned memory improvements typically change frame times by 2-10x with identical output.

## Q14: Why does pinned memory matter more than FLOPs for raytracing?
**A:** Ray integration is memory- and latency-bound; pinned memory targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins.

## Q15: How do you profile pinned memory?
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; pinned memory tuning starts from measured numbers, not guesses.

## Q16: What is the first thing to fix under pinned memory?
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since pinned memory memory stalls dominate.

## Q17: How does pinned memory relate to warp occupancy?
**A:** More resident warps hide more latency, but registers/shared memory limit it; pinned memory balances occupancy against per-thread state.

## Q18: What is a typical 90/10 pinned memory rule?
**A:** 10% of the kernel is 90% of the runtime; pinned memory spend begins by identifying and fixing that hot loop, then measuring again.

## Q19: How does pinned memory handle determinism?
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep pinned memory results reproducible while still fast.

## Q20: What does pinned memory do about divergent geodesic paths?
**A:** Assign one ray per thread so long and short rays simply finish at different times; pinned memory accepts this natural load imbalance.

## Q21: How is pinned memory measured end-to-end?
**A:** Frames per second at fixed image size and step policy; pinned memory reports both median kernel time and total wall time.

## Q22: How does pinned memory choose block size?
**A:** A multiple of the warp size that fills the SM to target occupancy; pinned memory sweeps 64-512 to find the plateau.

## Q23: What memory optimizations fall under pinned memory?
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the pinned memory toolbox.

## Q24: How does pinned memory scale to multi-GPU?
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; pinned memory keeps per-GPU work identical and overlap transfers.

## Q25: How does pinned memory use streams?
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; pinned memory overlaps host and device work.

## Q26: When is pinned memory over-engineering?
**A:** When the pipeline is still changing daily; pinned memory stabilization is reserved for mature kernels judged by their benchmark suite.

## Q27: What is the best first metric for pinned memory?
**A:** Achieved occupancy and DRAM throughput from Nsight; pinned memory optimization targets whichever is below the theoretical peak.

## Q28: How does pinned memory handle the image write-back?
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; pinned memory avoids read-modify-write penalties.

## Q29: What role does shared memory play in pinned memory?
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so pinned memory boosts cache hits dramatically.

## Q30: How does pinned memory cope with long-ish rays?
**A:** Spatially coherent groups finish similarly; pinned memory sorts/orders work briefly, or simply lets occupancy absorb the imbalance.

## Q31: What is a pinned memory regression test?
**A:** The golden image must not change when pinned memory is tuned; a side-channel checksum asserts identical pixels after each optimization.

## Q32: How does pinned memory treat constant and texture paths?
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; pinned memory chooses the path that reduces traffic.

## Q33: What should be avoided for pinned memory?
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle pinned memory.

## Q34: How do you explain pinned memory impact to a reviewer?
**A:** Show before/after Nsight categories and frame times; pinned memory communicates in measured evidence rather than opinion.

## Q35: What is the pinned memory budget for a movie frame?
**A:** If 1 second per frame is acceptable at 30 fps, pinned memory leaves ~33 ms; most pipelines budget a bit more and render offline with a farm.

## Q36: Where should pinned memory stop?
**A:** Once no profile category dominates and further gains are under a few percent, pinned memory stops and the remaining money goes to more samples.

## Q37: Where should pinned memory stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, pinned memory stops and the remaining money goes to more samples. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q38: What is the pinned memory budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, pinned memory leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q39: How do you explain pinned memory impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; pinned memory communicates in measured evidence rather than opinion. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: What should be avoided for pinned memory - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle pinned memory. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: How does pinned memory treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; pinned memory chooses the path that reduces traffic. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What is a pinned memory regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when pinned memory is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How does pinned memory cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; pinned memory sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What role does shared memory play in pinned memory - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so pinned memory boosts cache hits dramatically. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: How does pinned memory handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; pinned memory avoids read-modify-write penalties. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What is the best first metric for pinned memory - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; pinned memory optimization targets whichever is below the theoretical peak. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: When is pinned memory over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; pinned memory stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How does pinned memory use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; pinned memory overlaps host and device work. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: How does pinned memory scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; pinned memory keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What memory optimizations fall under pinned memory - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the pinned memory toolbox. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How does pinned memory choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; pinned memory sweeps 64-512 to find the plateau. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How is pinned memory measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; pinned memory reports both median kernel time and total wall time. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What does pinned memory do about divergent geodesic paths - justify your answer with a concrete production example.
**A:** Assign one ray per thread so long and short rays simply finish at different times; pinned memory accepts this natural load imbalance. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does pinned memory handle determinism - justify your answer with a concrete production example.
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep pinned memory results reproducible while still fast. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is a typical 90/10 pinned memory rule - justify your answer with a concrete production example.
**A:** 10% of the kernel is 90% of the runtime; pinned memory spend begins by identifying and fixing that hot loop, then measuring again. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How does pinned memory relate to warp occupancy - justify your answer with a concrete production example.
**A:** More resident warps hide more latency, but registers/shared memory limit it; pinned memory balances occupancy against per-thread state. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What is the first thing to fix under pinned memory - justify your answer with a concrete production example.
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since pinned memory memory stalls dominate. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: How do you profile pinned memory - justify your answer with a concrete production example.
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; pinned memory tuning starts from measured numbers, not guesses. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: Why does pinned memory matter more than FLOPs for raytracing - justify your answer with a concrete production example.
**A:** Ray integration is memory- and latency-bound; pinned memory targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What does pinned memory mean for the raytracer's runtime - justify your answer with a concrete production example.
**A:** It is the lever that turns a working kernel into a fast one; pinned memory improvements typically change frame times by 2-10x with identical output. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What does pinned memory mean for the raytracer's runtime - justify your answer with a concrete production example.
**A:** It is the lever that turns a working kernel into a fast one; pinned memory improvements typically change frame times by 2-10x with identical output. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why does pinned memory matter more than FLOPs for raytracing - justify your answer with a concrete production example.
**A:** Ray integration is memory- and latency-bound; pinned memory targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: How do you profile pinned memory - justify your answer with a concrete production example.
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; pinned memory tuning starts from measured numbers, not guesses. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What is the first thing to fix under pinned memory - justify your answer with a concrete production example.
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since pinned memory memory stalls dominate. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: How does pinned memory relate to warp occupancy - justify your answer with a concrete production example.
**A:** More resident warps hide more latency, but registers/shared memory limit it; pinned memory balances occupancy against per-thread state. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is a typical 90/10 pinned memory rule - justify your answer with a concrete production example.
**A:** 10% of the kernel is 90% of the runtime; pinned memory spend begins by identifying and fixing that hot loop, then measuring again. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How does pinned memory handle determinism - justify your answer with a concrete production example.
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep pinned memory results reproducible while still fast. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What does pinned memory do about divergent geodesic paths - justify your answer with a concrete production example.
**A:** Assign one ray per thread so long and short rays simply finish at different times; pinned memory accepts this natural load imbalance. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How is pinned memory measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; pinned memory reports both median kernel time and total wall time. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How does pinned memory choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; pinned memory sweeps 64-512 to find the plateau. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What memory optimizations fall under pinned memory - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the pinned memory toolbox. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: How does pinned memory scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; pinned memory keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does pinned memory use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; pinned memory overlaps host and device work. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: When is pinned memory over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; pinned memory stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What is the best first metric for pinned memory - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; pinned memory optimization targets whichever is below the theoretical peak. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How does pinned memory handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; pinned memory avoids read-modify-write penalties. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What role does shared memory play in pinned memory - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so pinned memory boosts cache hits dramatically. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How does pinned memory cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; pinned memory sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What is a pinned memory regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when pinned memory is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does pinned memory treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; pinned memory chooses the path that reduces traffic. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: What should be avoided for pinned memory - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle pinned memory. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: How do you explain pinned memory impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; pinned memory communicates in measured evidence rather than opinion. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What is the pinned memory budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, pinned memory leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: Where should pinned memory stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, pinned memory stops and the remaining money goes to more samples. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: Where should pinned memory stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, pinned memory stops and the remaining money goes to more samples. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the pinned memory budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, pinned memory leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How do you explain pinned memory impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; pinned memory communicates in measured evidence rather than opinion. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What should be avoided for pinned memory - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle pinned memory. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: How does pinned memory treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; pinned memory chooses the path that reduces traffic. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What is a pinned memory regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when pinned memory is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How does pinned memory cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; pinned memory sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What role does shared memory play in pinned memory - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so pinned memory boosts cache hits dramatically. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: How does pinned memory handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; pinned memory avoids read-modify-write penalties. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What is the best first metric for pinned memory - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; pinned memory optimization targets whichever is below the theoretical peak. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: When is pinned memory over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; pinned memory stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How does pinned memory use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; pinned memory overlaps host and device work. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: How does pinned memory scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; pinned memory keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What memory optimizations fall under pinned memory - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the pinned memory toolbox. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How does pinned memory choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; pinned memory sweeps 64-512 to find the plateau. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How is pinned memory measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; pinned memory reports both median kernel time and total wall time. A concrete example: consistently applying pinned memory in code review and regression tests keeps the whole pipeline trustworthy.
