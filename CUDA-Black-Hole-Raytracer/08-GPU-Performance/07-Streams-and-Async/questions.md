# Gpu Performance — Streams And Async Interview Questions and Answers

## Q1: What are CUDA streams?
**A:** Ordered sequences of kernel launches that can OVERLAP - multiple streams execute concurrently on the same GPU when resources allow (e.g., different kernels, copies).

## Q2: What is the async copy path?
**A:** cudaMemcpyAsync row-compressed data into pinned/special buffers overlaps the transfer with compute - the classic 'compute on frame k, transfer k+1'.

## Q3: How do streams help a multi-frame renderer?
**A:** Frame pipeline: stream A traces frame k while stream B post-processes k-1 and transfers the result k-2 - the GPU never idles on I/O.

## Q4: What is the dependency problem?
**A:** Rays of frame k+1 are independent of frame k's output - ideal stream parallelism; only the accumulation of one frame is sequential internally.

## Q5: What is the event mechanism?
**A:** cudaEventRecord/StreamWaitEvent orders cross-stream dependencies (e.g., 'wait until geometry buffer ready') without busy-waiting.

## Q6: How does overlap interact with tiling?
**A:** Independent tiles of the SAME frame run well on one stream; overlapping DIFFERENT frames on multiple streams adds concurrency beyond occupancy - a second knob.

## Q7: What is the pinned-memory requirement?
**A:** Async copies to host require page-locked (pinned) buffers - without cudaHostAlloc the 'async' copy silently serializes.

## Q8: What does Nsight Systems show?
**A:** The timeline exposes idle gaps: if the GPU is <70% busy with streams+occupancy at max, the data flow is the bottleneck - fix with more/finer streams.

## Q9: What is the correctness hazard?
**A:** Streams race unless ordered by events; image accumulation must happen before downstream reads - any 'async' optimization is validated by determinism tests.

## Q10: When does multipl-stream hurt?
**A:** Too many streams with heavy resource contention thrash and serialize again; 2-4 streams with a clear per-frame role beats 16 ad-hoc ones.

## Q11: What is the copy-engine behavior?
**A:** DMA (copy engines) run independent of SMs; overlap H2D/D2H with compute requires separate streams + events - the standard 3-stage pipeline.

## Q12: What is the summary?
**A:** Streams and async copy pipeline independent frames and I/O - the last big lever beyond occupancy for keeping a big renderer's GPU always busy.

## Q13: What does streams and async mean for the raytracer's runtime?
**A:** It is the lever that turns a working kernel into a fast one; streams and async improvements typically change frame times by 2-10x with identical output.

## Q14: Why does streams and async matter more than FLOPs for raytracing?
**A:** Ray integration is memory- and latency-bound; streams and async targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins.

## Q15: How do you profile streams and async?
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; streams and async tuning starts from measured numbers, not guesses.

## Q16: What is the first thing to fix under streams and async?
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since streams and async memory stalls dominate.

## Q17: How does streams and async relate to warp occupancy?
**A:** More resident warps hide more latency, but registers/shared memory limit it; streams and async balances occupancy against per-thread state.

## Q18: What is a typical 90/10 streams and async rule?
**A:** 10% of the kernel is 90% of the runtime; streams and async spend begins by identifying and fixing that hot loop, then measuring again.

## Q19: How does streams and async handle determinism?
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep streams and async results reproducible while still fast.

## Q20: What does streams and async do about divergent geodesic paths?
**A:** Assign one ray per thread so long and short rays simply finish at different times; streams and async accepts this natural load imbalance.

## Q21: How is streams and async measured end-to-end?
**A:** Frames per second at fixed image size and step policy; streams and async reports both median kernel time and total wall time.

## Q22: How does streams and async choose block size?
**A:** A multiple of the warp size that fills the SM to target occupancy; streams and async sweeps 64-512 to find the plateau.

## Q23: What memory optimizations fall under streams and async?
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the streams and async toolbox.

## Q24: How does streams and async scale to multi-GPU?
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; streams and async keeps per-GPU work identical and overlap transfers.

## Q25: How does streams and async use streams?
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; streams and async overlaps host and device work.

## Q26: When is streams and async over-engineering?
**A:** When the pipeline is still changing daily; streams and async stabilization is reserved for mature kernels judged by their benchmark suite.

## Q27: What is the best first metric for streams and async?
**A:** Achieved occupancy and DRAM throughput from Nsight; streams and async optimization targets whichever is below the theoretical peak.

## Q28: How does streams and async handle the image write-back?
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; streams and async avoids read-modify-write penalties.

## Q29: What role does shared memory play in streams and async?
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so streams and async boosts cache hits dramatically.

## Q30: How does streams and async cope with long-ish rays?
**A:** Spatially coherent groups finish similarly; streams and async sorts/orders work briefly, or simply lets occupancy absorb the imbalance.

## Q31: What is a streams and async regression test?
**A:** The golden image must not change when streams and async is tuned; a side-channel checksum asserts identical pixels after each optimization.

## Q32: How does streams and async treat constant and texture paths?
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; streams and async chooses the path that reduces traffic.

## Q33: What should be avoided for streams and async?
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle streams and async.

## Q34: How do you explain streams and async impact to a reviewer?
**A:** Show before/after Nsight categories and frame times; streams and async communicates in measured evidence rather than opinion.

## Q35: What is the streams and async budget for a movie frame?
**A:** If 1 second per frame is acceptable at 30 fps, streams and async leaves ~33 ms; most pipelines budget a bit more and render offline with a farm.

## Q36: Where should streams and async stop?
**A:** Once no profile category dominates and further gains are under a few percent, streams and async stops and the remaining money goes to more samples.

## Q37: Where should streams and async stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, streams and async stops and the remaining money goes to more samples. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q38: What is the streams and async budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, streams and async leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q39: How do you explain streams and async impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; streams and async communicates in measured evidence rather than opinion. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: What should be avoided for streams and async - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle streams and async. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: How does streams and async treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; streams and async chooses the path that reduces traffic. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What is a streams and async regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when streams and async is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How does streams and async cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; streams and async sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What role does shared memory play in streams and async - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so streams and async boosts cache hits dramatically. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: How does streams and async handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; streams and async avoids read-modify-write penalties. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What is the best first metric for streams and async - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; streams and async optimization targets whichever is below the theoretical peak. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: When is streams and async over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; streams and async stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How does streams and async use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; streams and async overlaps host and device work. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: How does streams and async scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; streams and async keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What memory optimizations fall under streams and async - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the streams and async toolbox. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How does streams and async choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; streams and async sweeps 64-512 to find the plateau. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How is streams and async measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; streams and async reports both median kernel time and total wall time. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What does streams and async do about divergent geodesic paths - justify your answer with a concrete production example.
**A:** Assign one ray per thread so long and short rays simply finish at different times; streams and async accepts this natural load imbalance. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does streams and async handle determinism - justify your answer with a concrete production example.
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep streams and async results reproducible while still fast. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is a typical 90/10 streams and async rule - justify your answer with a concrete production example.
**A:** 10% of the kernel is 90% of the runtime; streams and async spend begins by identifying and fixing that hot loop, then measuring again. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How does streams and async relate to warp occupancy - justify your answer with a concrete production example.
**A:** More resident warps hide more latency, but registers/shared memory limit it; streams and async balances occupancy against per-thread state. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What is the first thing to fix under streams and async - justify your answer with a concrete production example.
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since streams and async memory stalls dominate. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: How do you profile streams and async - justify your answer with a concrete production example.
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; streams and async tuning starts from measured numbers, not guesses. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: Why does streams and async matter more than FLOPs for raytracing - justify your answer with a concrete production example.
**A:** Ray integration is memory- and latency-bound; streams and async targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What does streams and async mean for the raytracer's runtime - justify your answer with a concrete production example.
**A:** It is the lever that turns a working kernel into a fast one; streams and async improvements typically change frame times by 2-10x with identical output. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What does streams and async mean for the raytracer's runtime - justify your answer with a concrete production example.
**A:** It is the lever that turns a working kernel into a fast one; streams and async improvements typically change frame times by 2-10x with identical output. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why does streams and async matter more than FLOPs for raytracing - justify your answer with a concrete production example.
**A:** Ray integration is memory- and latency-bound; streams and async targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: How do you profile streams and async - justify your answer with a concrete production example.
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; streams and async tuning starts from measured numbers, not guesses. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What is the first thing to fix under streams and async - justify your answer with a concrete production example.
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since streams and async memory stalls dominate. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: How does streams and async relate to warp occupancy - justify your answer with a concrete production example.
**A:** More resident warps hide more latency, but registers/shared memory limit it; streams and async balances occupancy against per-thread state. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is a typical 90/10 streams and async rule - justify your answer with a concrete production example.
**A:** 10% of the kernel is 90% of the runtime; streams and async spend begins by identifying and fixing that hot loop, then measuring again. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How does streams and async handle determinism - justify your answer with a concrete production example.
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep streams and async results reproducible while still fast. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What does streams and async do about divergent geodesic paths - justify your answer with a concrete production example.
**A:** Assign one ray per thread so long and short rays simply finish at different times; streams and async accepts this natural load imbalance. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How is streams and async measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; streams and async reports both median kernel time and total wall time. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How does streams and async choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; streams and async sweeps 64-512 to find the plateau. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What memory optimizations fall under streams and async - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the streams and async toolbox. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: How does streams and async scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; streams and async keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does streams and async use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; streams and async overlaps host and device work. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: When is streams and async over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; streams and async stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What is the best first metric for streams and async - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; streams and async optimization targets whichever is below the theoretical peak. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How does streams and async handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; streams and async avoids read-modify-write penalties. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What role does shared memory play in streams and async - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so streams and async boosts cache hits dramatically. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How does streams and async cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; streams and async sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What is a streams and async regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when streams and async is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does streams and async treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; streams and async chooses the path that reduces traffic. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: What should be avoided for streams and async - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle streams and async. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: How do you explain streams and async impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; streams and async communicates in measured evidence rather than opinion. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What is the streams and async budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, streams and async leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: Where should streams and async stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, streams and async stops and the remaining money goes to more samples. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: Where should streams and async stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, streams and async stops and the remaining money goes to more samples. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the streams and async budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, streams and async leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How do you explain streams and async impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; streams and async communicates in measured evidence rather than opinion. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What should be avoided for streams and async - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle streams and async. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: How does streams and async treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; streams and async chooses the path that reduces traffic. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What is a streams and async regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when streams and async is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How does streams and async cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; streams and async sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What role does shared memory play in streams and async - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so streams and async boosts cache hits dramatically. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: How does streams and async handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; streams and async avoids read-modify-write penalties. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What is the best first metric for streams and async - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; streams and async optimization targets whichever is below the theoretical peak. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: When is streams and async over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; streams and async stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How does streams and async use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; streams and async overlaps host and device work. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: How does streams and async scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; streams and async keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What memory optimizations fall under streams and async - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the streams and async toolbox. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How does streams and async choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; streams and async sweeps 64-512 to find the plateau. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How is streams and async measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; streams and async reports both median kernel time and total wall time. A concrete example: consistently applying streams and async in code review and regression tests keeps the whole pipeline trustworthy.
