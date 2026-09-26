# Gpu Performance — Cuda Graphs Interview Questions and Answers

## Q1: What are CUDA Graphs?
**A:** A complete launch DAG (kernels + copies + events) captured once and replayed with minimal CPU overhead - replacing the per-frame launch-call storm.

## Q2: How does a raytracer become a graph?
**A:** Frame pipeline: upload-state (if any), geodesic kernel, transfer/accumulate kernel, gather/boost kernel, image write - captured as a reusable graph.

## Q3: Why do CUDA Graphs matter here?
**A:** A 2k image with tile kernels launches ~10^4-10^5 calls per frame; graph replay cuts launch latency from ~5us/call to a single ~1us replay - multi-ms/frame saved.

## Q4: What is capture semantics?
**A:** cudaStreamBeginCapture, run the kernels normally, EndCapture -> graph; CPU-side gaps between launches collapse into one submitted plot.

## Q5: What is the mutable-node benefit?
**A:** Variable buffers (next frame's state) bind at launch; graph nodes refer to memory pools - update via the graph's resource handles, not re-capture.

## Q6: What is the interplay with streams?
**A:** A graph CAN embed stream semantics (dependent regions) for multi-frame overlap within one submission - stream capture + graph replay compose.

## Q7: What does the graph do to determinism?
**A:** Fixed DAG order = fixed execution order = reproducible results; one more reason graphs and fprintf-debuging work well together.

## Q8: What is the overhead of graph capture?
**A:** Capture costs ~ms (kernel launches are recorded); amortize: capture once per configuration, replay thousands of frames.

## Q9: What is the update-safe pattern for parameters?
**A:** The graph refers to device memory; parameters that change (camera, time) live in memory the graph's kernels already read - NO kernel-arg churn.

## Q10: How does the graph speed the movie path?
**A:** A 9000-frame movie with a captured frame-graph reduces the CPU-side launch overhead to nothing - purely a submission-efficiency win.

## Q11: What is the validation for graphs?
**A:** Replaying the graph must match the sequential-launch path bit-for-bit; enable a build flag to bypass graphs for debugging when it doesn't.

## Q12: What is the summary?
**A:** CUDA Graphs collapse per-frame launch chaos into one replayable DAG - the standard device-side executor of a production multi-frame pipeline.

## Q13: What does cuda graphs mean for the raytracer's runtime?
**A:** It is the lever that turns a working kernel into a fast one; cuda graphs improvements typically change frame times by 2-10x with identical output.

## Q14: Why does cuda graphs matter more than FLOPs for raytracing?
**A:** Ray integration is memory- and latency-bound; cuda graphs targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins.

## Q15: How do you profile cuda graphs?
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; cuda graphs tuning starts from measured numbers, not guesses.

## Q16: What is the first thing to fix under cuda graphs?
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since cuda graphs memory stalls dominate.

## Q17: How does cuda graphs relate to warp occupancy?
**A:** More resident warps hide more latency, but registers/shared memory limit it; cuda graphs balances occupancy against per-thread state.

## Q18: What is a typical 90/10 cuda graphs rule?
**A:** 10% of the kernel is 90% of the runtime; cuda graphs spend begins by identifying and fixing that hot loop, then measuring again.

## Q19: How does cuda graphs handle determinism?
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep cuda graphs results reproducible while still fast.

## Q20: What does cuda graphs do about divergent geodesic paths?
**A:** Assign one ray per thread so long and short rays simply finish at different times; cuda graphs accepts this natural load imbalance.

## Q21: How is cuda graphs measured end-to-end?
**A:** Frames per second at fixed image size and step policy; cuda graphs reports both median kernel time and total wall time.

## Q22: How does cuda graphs choose block size?
**A:** A multiple of the warp size that fills the SM to target occupancy; cuda graphs sweeps 64-512 to find the plateau.

## Q23: What memory optimizations fall under cuda graphs?
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the cuda graphs toolbox.

## Q24: How does cuda graphs scale to multi-GPU?
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; cuda graphs keeps per-GPU work identical and overlap transfers.

## Q25: How does cuda graphs use streams?
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; cuda graphs overlaps host and device work.

## Q26: When is cuda graphs over-engineering?
**A:** When the pipeline is still changing daily; cuda graphs stabilization is reserved for mature kernels judged by their benchmark suite.

## Q27: What is the best first metric for cuda graphs?
**A:** Achieved occupancy and DRAM throughput from Nsight; cuda graphs optimization targets whichever is below the theoretical peak.

## Q28: How does cuda graphs handle the image write-back?
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; cuda graphs avoids read-modify-write penalties.

## Q29: What role does shared memory play in cuda graphs?
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so cuda graphs boosts cache hits dramatically.

## Q30: How does cuda graphs cope with long-ish rays?
**A:** Spatially coherent groups finish similarly; cuda graphs sorts/orders work briefly, or simply lets occupancy absorb the imbalance.

## Q31: What is a cuda graphs regression test?
**A:** The golden image must not change when cuda graphs is tuned; a side-channel checksum asserts identical pixels after each optimization.

## Q32: How does cuda graphs treat constant and texture paths?
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; cuda graphs chooses the path that reduces traffic.

## Q33: What should be avoided for cuda graphs?
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle cuda graphs.

## Q34: How do you explain cuda graphs impact to a reviewer?
**A:** Show before/after Nsight categories and frame times; cuda graphs communicates in measured evidence rather than opinion.

## Q35: What is the cuda graphs budget for a movie frame?
**A:** If 1 second per frame is acceptable at 30 fps, cuda graphs leaves ~33 ms; most pipelines budget a bit more and render offline with a farm.

## Q36: Where should cuda graphs stop?
**A:** Once no profile category dominates and further gains are under a few percent, cuda graphs stops and the remaining money goes to more samples.

## Q37: Where should cuda graphs stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, cuda graphs stops and the remaining money goes to more samples. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q38: What is the cuda graphs budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, cuda graphs leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q39: How do you explain cuda graphs impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; cuda graphs communicates in measured evidence rather than opinion. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: What should be avoided for cuda graphs - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle cuda graphs. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: How does cuda graphs treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; cuda graphs chooses the path that reduces traffic. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What is a cuda graphs regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when cuda graphs is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How does cuda graphs cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; cuda graphs sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What role does shared memory play in cuda graphs - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so cuda graphs boosts cache hits dramatically. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: How does cuda graphs handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; cuda graphs avoids read-modify-write penalties. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What is the best first metric for cuda graphs - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; cuda graphs optimization targets whichever is below the theoretical peak. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: When is cuda graphs over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; cuda graphs stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How does cuda graphs use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; cuda graphs overlaps host and device work. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: How does cuda graphs scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; cuda graphs keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What memory optimizations fall under cuda graphs - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the cuda graphs toolbox. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How does cuda graphs choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; cuda graphs sweeps 64-512 to find the plateau. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: How is cuda graphs measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; cuda graphs reports both median kernel time and total wall time. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: What does cuda graphs do about divergent geodesic paths - justify your answer with a concrete production example.
**A:** Assign one ray per thread so long and short rays simply finish at different times; cuda graphs accepts this natural load imbalance. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How does cuda graphs handle determinism - justify your answer with a concrete production example.
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep cuda graphs results reproducible while still fast. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What is a typical 90/10 cuda graphs rule - justify your answer with a concrete production example.
**A:** 10% of the kernel is 90% of the runtime; cuda graphs spend begins by identifying and fixing that hot loop, then measuring again. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How does cuda graphs relate to warp occupancy - justify your answer with a concrete production example.
**A:** More resident warps hide more latency, but registers/shared memory limit it; cuda graphs balances occupancy against per-thread state. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: What is the first thing to fix under cuda graphs - justify your answer with a concrete production example.
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since cuda graphs memory stalls dominate. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: How do you profile cuda graphs - justify your answer with a concrete production example.
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; cuda graphs tuning starts from measured numbers, not guesses. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: Why does cuda graphs matter more than FLOPs for raytracing - justify your answer with a concrete production example.
**A:** Ray integration is memory- and latency-bound; cuda graphs targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: What does cuda graphs mean for the raytracer's runtime - justify your answer with a concrete production example.
**A:** It is the lever that turns a working kernel into a fast one; cuda graphs improvements typically change frame times by 2-10x with identical output. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: What does cuda graphs mean for the raytracer's runtime - justify your answer with a concrete production example.
**A:** It is the lever that turns a working kernel into a fast one; cuda graphs improvements typically change frame times by 2-10x with identical output. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why does cuda graphs matter more than FLOPs for raytracing - justify your answer with a concrete production example.
**A:** Ray integration is memory- and latency-bound; cuda graphs targets those bottlenecks, not raw arithmetic, so it dictates actual wall-clock wins. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: How do you profile cuda graphs - justify your answer with a concrete production example.
**A:** Nsight Compute gives detailed kernel metrics while Nsight Systems shows the timeline; cuda graphs tuning starts from measured numbers, not guesses. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What is the first thing to fix under cuda graphs - justify your answer with a concrete production example.
**A:** Memory access patterns - coalescing, cache friendliness, and streaming - before touching arithmetic, since cuda graphs memory stalls dominate. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: How does cuda graphs relate to warp occupancy - justify your answer with a concrete production example.
**A:** More resident warps hide more latency, but registers/shared memory limit it; cuda graphs balances occupancy against per-thread state. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: What is a typical 90/10 cuda graphs rule - justify your answer with a concrete production example.
**A:** 10% of the kernel is 90% of the runtime; cuda graphs spend begins by identifying and fixing that hot loop, then measuring again. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How does cuda graphs handle determinism - justify your answer with a concrete production example.
**A:** Deterministic algorithms (fixed order, no nondeterministic atomics for image pixels) keep cuda graphs results reproducible while still fast. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What does cuda graphs do about divergent geodesic paths - justify your answer with a concrete production example.
**A:** Assign one ray per thread so long and short rays simply finish at different times; cuda graphs accepts this natural load imbalance. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How is cuda graphs measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; cuda graphs reports both median kernel time and total wall time. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How does cuda graphs choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; cuda graphs sweeps 64-512 to find the plateau. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What memory optimizations fall under cuda graphs - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the cuda graphs toolbox. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: How does cuda graphs scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; cuda graphs keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How does cuda graphs use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; cuda graphs overlaps host and device work. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: When is cuda graphs over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; cuda graphs stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What is the best first metric for cuda graphs - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; cuda graphs optimization targets whichever is below the theoretical peak. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How does cuda graphs handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; cuda graphs avoids read-modify-write penalties. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What role does shared memory play in cuda graphs - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so cuda graphs boosts cache hits dramatically. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How does cuda graphs cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; cuda graphs sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What is a cuda graphs regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when cuda graphs is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How does cuda graphs treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; cuda graphs chooses the path that reduces traffic. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: What should be avoided for cuda graphs - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle cuda graphs. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: How do you explain cuda graphs impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; cuda graphs communicates in measured evidence rather than opinion. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: What is the cuda graphs budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, cuda graphs leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: Where should cuda graphs stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, cuda graphs stops and the remaining money goes to more samples. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: Where should cuda graphs stop - justify your answer with a concrete production example.
**A:** Once no profile category dominates and further gains are under a few percent, cuda graphs stops and the remaining money goes to more samples. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What is the cuda graphs budget for a movie frame - justify your answer with a concrete production example.
**A:** If 1 second per frame is acceptable at 30 fps, cuda graphs leaves ~33 ms; most pipelines budget a bit more and render offline with a farm. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How do you explain cuda graphs impact to a reviewer - justify your answer with a concrete production example.
**A:** Show before/after Nsight categories and frame times; cuda graphs communicates in measured evidence rather than opinion. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What should be avoided for cuda graphs - justify your answer with a concrete production example.
**A:** Dynamic allocation in kernels, per-ray locks, and excessive register-per-thread state all throttle cuda graphs. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: How does cuda graphs treat constant and texture paths - justify your answer with a concrete production example.
**A:** Read-only parameters go in __constant__; interpolatable fields can use texture/read-only caches; cuda graphs chooses the path that reduces traffic. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What is a cuda graphs regression test - justify your answer with a concrete production example.
**A:** The golden image must not change when cuda graphs is tuned; a side-channel checksum asserts identical pixels after each optimization. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How does cuda graphs cope with long-ish rays - justify your answer with a concrete production example.
**A:** Spatially coherent groups finish similarly; cuda graphs sorts/orders work briefly, or simply lets occupancy absorb the imbalance. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What role does shared memory play in cuda graphs - justify your answer with a concrete production example.
**A:** It tiles data reused across threads - exactly the pattern of nearby rays sampling nearby grid cells - so cuda graphs boosts cache hits dramatically. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: How does cuda graphs handle the image write-back - justify your answer with a concrete production example.
**A:** One thread writes one pixel (or a few) to an output buffer that is later copied to host; cuda graphs avoids read-modify-write penalties. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What is the best first metric for cuda graphs - justify your answer with a concrete production example.
**A:** Achieved occupancy and DRAM throughput from Nsight; cuda graphs optimization targets whichever is below the theoretical peak. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: When is cuda graphs over-engineering - justify your answer with a concrete production example.
**A:** When the pipeline is still changing daily; cuda graphs stabilization is reserved for mature kernels judged by their benchmark suite. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How does cuda graphs use streams - justify your answer with a concrete production example.
**A:** Concurrent kernels, async transfers on separate streams, and event-based chunking keep the device busy; cuda graphs overlaps host and device work. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: How does cuda graphs scale to multi-GPU - justify your answer with a concrete production example.
**A:** Each GPU renders a horizontal strip of the frame and transfers only its strip back; cuda graphs keeps per-GPU work identical and overlap transfers. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What memory optimizations fall under cuda graphs - justify your answer with a concrete production example.
**A:** Pinned transfers, constant memory for metric parameters, shared preloading of tiles, and avoiding repeated global reads - the cuda graphs toolbox. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How does cuda graphs choose block size - justify your answer with a concrete production example.
**A:** A multiple of the warp size that fills the SM to target occupancy; cuda graphs sweeps 64-512 to find the plateau. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: How is cuda graphs measured end-to-end - justify your answer with a concrete production example.
**A:** Frames per second at fixed image size and step policy; cuda graphs reports both median kernel time and total wall time. A concrete example: consistently applying cuda graphs in code review and regression tests keeps the whole pipeline trustworthy.
