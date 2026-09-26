# Ray Tracing — Bounding Volume Hierarchy Interview Questions and Answers

## Q1: What is a BVH?
**A:** A binary tree of axis-aligned bounding boxes (AABBs) enclosing primitives; traversal descends only subtrees whose box the ray intersects, giving ~log(N) work.

## Q2: What is the node layout for a traversal-efficient BVH?
**A:** A contiguous array of 24/32-byte nodes, each storing childAABB, transformed bounds, and offset/count for leaf primitives; index 0 == root via traversal conventions.

## Q3: How do you build a BVH top-down?
**A:** Partition primitives along the largest AABB axis at the best split (SAH or median), recurse into children, emit nodes - O(N log N) typical, O(N^2) naive worst.

## Q4: What does SAH cost estimate?
**A:** c = C_traverse + (areaL/total)*cL*(countL) + (areaR/total)*cR*(countR); pick the split minimizing cost across candidate planes (binning to O(N log N)).

## Q5: What is a primitive-partition vs spatial-midpoint split?
**A:** Primitive partition: split by centroid order (balanced); midpoint: split by box mid (may imbalance). SAH bins the arbitrary of primitives best in practice.

## Q6: How does the greedy BVH traverse?
**A:** A stack: push children of a hit box; pop the nearest (distance) and test its primitives - recursion converted to an explicit stack for GPU/SIMT friendliness.

## Q7: What is the ray-box test?
**A:** slab: for each axis tmin = (min - o)/d, tmax = (max - o)/d, intersect ranges; ray hits the box iff max(tmin)>min(tmax) and within (0, tRayCap).

## Q8: How do you parallelize the build?
**A:** Morton-code ordering (sort by 3D bit interleave of centroid) lets you build a radix-tree BVH in O(N log N) fully parallel - the GPU community standard.

## Q9: What is the SAH cost of a static sky BVH?
**A:** Built once, ~hundreds of microseconds for 10^4 stars, amortized over millions of rays - effectively free while cutting per-ray intersection tests.

## Q10: How does the BVH fit the disk?
**A:** The disk can be represented as a BVH over emissive surface patches (or a single AABB over a grid) so rays cull most cells before deep sampling.

## Q11: What are the numerical traps in BVH traversal?
**A:** NaNs when a subdivided tiny direction divides by zero; clamp d==0 to +inf or split into per-axis degree; keep t values monotonic.

## Q12: What memory access pattern does traversal need?
**A:** Depth-first node visits are local but pointer jumps; using SIMD-4 nodes (BVH4) amortizes memory latency and enables branch-minimized stackless traversal.

## Q13: How do you test a BVH?
**A:** Same golden-image rule: enabling/disabling the BVH must not change a single pixel; plus count-assurance: average touched nodes << N.

## Q14: When is a BVH overkill for the black-hole scene?
**A:** For a pure sky + disk where a grid already reaches <5 tests/ray; reconsider when you add thousands of emissive particles and star primitives.

## Q15: What is the recommended production choice?
**A:** Start grid (simplest to implement both ways), keep the interface abstraction, and swap to BVH under the same traversal contract when scenes grow.

## Q16: What is the purpose of bounding volume hierarchy in a raytracer?
**A:** It defines how geometric questions are answered for each pixel ray, converting abstract scene data into visible color contributions.

## Q17: Why does bounding volume hierarchy matter more in a GPU raytracer?
**A:** Because millions of rays run concurrently; bounding volume hierarchy determines whether each thread can proceed independently or stalls on divergent geometry work.

## Q18: Describe the main correctness concern in bounding volume hierarchy.
**A:** Precision: numerically unstable bounding volume hierarchy causes gaps, shadow acne, and flicker; consistently evaluate in double or carefully-ordered floats.

## Q19: How does bounding volume hierarchy affect perceptual quality?
**A:** Small errors in bounding volume hierarchy show up as aliasing, hard shadows, or wrong silhouettes long before an average viewer can name the cause.

## Q20: What is the standard way to structure bounding volume hierarchy code?
**A:** Separate pure functions (no state) so bounding volume hierarchy compiles to fast device code and can be unit-tested on the host with the same inputs.

## Q21: How do you benchmark bounding volume hierarchy?
**A:** Render a fixed scene at multiple resolutions, measure rays/second, and compare against an analytic ground truth for identical camera settings.

## Q22: When does bounding volume hierarchy produce artifacts?
**A:** When step sizes, tolerances, or intersection epsilons are tuned wrong - the classic acne/darkening trade-off of bounding volume hierarchy.

## Q23: How should bounding volume hierarchy handle edge cases like grazing angles?
**A:** Use robust predicates and minimum epsilon displacements so bounding volume hierarchy stays stable exactly where classic plane tests degenerate.

## Q24: What relationship does bounding volume hierarchy have with the rest of the pipeline?
**A:** bounding volume hierarchy produces the input for shading and post-processing; any error here is amplified by everything downstream.

## Q25: How do you make bounding volume hierarchy deterministic across runs?
**A:** Fix the accumulation order and sampling seed per pixel so bounding volume hierarchy reproduces bit-identical output for the same scene and parameters.

## Q26: Give a production example of bounding volume hierarchy in the black-hole visualizer.
**A:** Tracing a photon through the accretion flow uses bounding volume hierarchy at every step: intersect the disk plane, sample the field, and terminate at horizon or sky.

## Q27: What should you test about bounding volume hierarchy?
**A:** Golden images for a handful of scenes, analytic sizes for primitive shapes, and monotonic quality as samples increase for bounding volume hierarchy.

## Q28: How does bounding volume hierarchy interact with antialiasing?
**A:** Antialiasing launches many slightly different rays; bounding volume hierarchy must keep their per-ray state separate so samples blend correctly.

## Q29: What falls in the domain of bounding volume hierarchy vs rendering?
**A:** bounding volume hierarchy is geometric answer-finding; rendering decides color, lighting, and tone mapping from those answers - keep the boundary clean.

## Q30: What is the most common performance trap in bounding volume hierarchy?
**A:** Recomputing the same expensive data per ray instead of caching it in constant or shared memory before the bounding volume hierarchy loop starts.

## Q31: How do you explain bounding volume hierarchy trade-offs on a single slide?
**A:** A table: approach, cost per ray, memory, robustness, and GPU friendliness - summarize bounding volume hierarchy options in one comparison view.

## Q32: What happens if bounding volume hierarchy is not monotonic with samples?
**A:** The image converges to the wrong value, revealing a bug; bounding volume hierarchy results must approach a stable limit as sampling grows.

## Q33: How do you port bounding volume hierarchy from CPU to GPU?
**A:** Keep the math identical in device functions, inline the hot loops, and replace heap allocations with pre-allocated buffers for bounding volume hierarchy.

## Q34: What are the output guarantees of bounding volume hierarchy?
**A:** A per-pixel radiance estimate (and optionally depth/ray state) that downstream tone mapping can trust - the contract of bounding volume hierarchy.

## Q35: When is brute force acceptable for bounding volume hierarchy?
**A:** For a handful of primitives or when ray count dominates; then the cost of bounding volume hierarchy acceleration structures exceeds their savings.

## Q36: How does bounding volume hierarchy fit into a modular architecture?
**A:** As a component behind a stable interface - the renderer calls bounding volume hierarchy and never depends on its implementation details.

## Q37: What does a rigorous test suite assert about bounding volume hierarchy?
**A:** Correctness on constructed scenes, performance on a benchmark scene, and stability (no NaN/Inf) across resolution ranges.

## Q38: What tools measure bounding volume hierarchy quality?
**A:** A/B images, per-pixel error maps against reference, and error-vs-samples curves are the quantitative tools for bounding volume hierarchy.

## Q39: How do you teach bounding volume hierarchy fundamentals?
**A:** Start with a pinhole camera and a sphere; every later feature builds on the same try-a-ray, find-an-answer shape of bounding volume hierarchy.

## Q40: How do you teach bounding volume hierarchy fundamentals - justify your answer with a concrete production example.
**A:** Start with a pinhole camera and a sphere; every later feature builds on the same try-a-ray, find-an-answer shape of bounding volume hierarchy. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What tools measure bounding volume hierarchy quality - justify your answer with a concrete production example.
**A:** A/B images, per-pixel error maps against reference, and error-vs-samples curves are the quantitative tools for bounding volume hierarchy. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What does a rigorous test suite assert about bounding volume hierarchy - justify your answer with a concrete production example.
**A:** Correctness on constructed scenes, performance on a benchmark scene, and stability (no NaN/Inf) across resolution ranges. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How does bounding volume hierarchy fit into a modular architecture - justify your answer with a concrete production example.
**A:** As a component behind a stable interface - the renderer calls bounding volume hierarchy and never depends on its implementation details. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: When is brute force acceptable for bounding volume hierarchy - justify your answer with a concrete production example.
**A:** For a handful of primitives or when ray count dominates; then the cost of bounding volume hierarchy acceleration structures exceeds their savings. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What are the output guarantees of bounding volume hierarchy - justify your answer with a concrete production example.
**A:** A per-pixel radiance estimate (and optionally depth/ray state) that downstream tone mapping can trust - the contract of bounding volume hierarchy. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How do you port bounding volume hierarchy from CPU to GPU - justify your answer with a concrete production example.
**A:** Keep the math identical in device functions, inline the hot loops, and replace heap allocations with pre-allocated buffers for bounding volume hierarchy. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What happens if bounding volume hierarchy is not monotonic with samples - justify your answer with a concrete production example.
**A:** The image converges to the wrong value, revealing a bug; bounding volume hierarchy results must approach a stable limit as sampling grows. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you explain bounding volume hierarchy trade-offs on a single slide - justify your answer with a concrete production example.
**A:** A table: approach, cost per ray, memory, robustness, and GPU friendliness - summarize bounding volume hierarchy options in one comparison view. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What is the most common performance trap in bounding volume hierarchy - justify your answer with a concrete production example.
**A:** Recomputing the same expensive data per ray instead of caching it in constant or shared memory before the bounding volume hierarchy loop starts. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What falls in the domain of bounding volume hierarchy vs rendering - justify your answer with a concrete production example.
**A:** bounding volume hierarchy is geometric answer-finding; rendering decides color, lighting, and tone mapping from those answers - keep the boundary clean. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How does bounding volume hierarchy interact with antialiasing - justify your answer with a concrete production example.
**A:** Antialiasing launches many slightly different rays; bounding volume hierarchy must keep their per-ray state separate so samples blend correctly. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What should you test about bounding volume hierarchy - justify your answer with a concrete production example.
**A:** Golden images for a handful of scenes, analytic sizes for primitive shapes, and monotonic quality as samples increase for bounding volume hierarchy. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: Give a production example of bounding volume hierarchy in the black-hole visualizer - justify your answer with a concrete production example.
**A:** Tracing a photon through the accretion flow uses bounding volume hierarchy at every step: intersect the disk plane, sample the field, and terminate at horizon or sky. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How do you make bounding volume hierarchy deterministic across runs - justify your answer with a concrete production example.
**A:** Fix the accumulation order and sampling seed per pixel so bounding volume hierarchy reproduces bit-identical output for the same scene and parameters. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What relationship does bounding volume hierarchy have with the rest of the pipeline - justify your answer with a concrete production example.
**A:** bounding volume hierarchy produces the input for shading and post-processing; any error here is amplified by everything downstream. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How should bounding volume hierarchy handle edge cases like grazing angles - justify your answer with a concrete production example.
**A:** Use robust predicates and minimum epsilon displacements so bounding volume hierarchy stays stable exactly where classic plane tests degenerate. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: When does bounding volume hierarchy produce artifacts - justify your answer with a concrete production example.
**A:** When step sizes, tolerances, or intersection epsilons are tuned wrong - the classic acne/darkening trade-off of bounding volume hierarchy. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: How do you benchmark bounding volume hierarchy - justify your answer with a concrete production example.
**A:** Render a fixed scene at multiple resolutions, measure rays/second, and compare against an analytic ground truth for identical camera settings. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What is the standard way to structure bounding volume hierarchy code - justify your answer with a concrete production example.
**A:** Separate pure functions (no state) so bounding volume hierarchy compiles to fast device code and can be unit-tested on the host with the same inputs. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: How does bounding volume hierarchy affect perceptual quality - justify your answer with a concrete production example.
**A:** Small errors in bounding volume hierarchy show up as aliasing, hard shadows, or wrong silhouettes long before an average viewer can name the cause. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: Describe the main correctness concern in bounding volume hierarchy - justify your answer with a concrete production example.
**A:** Precision: numerically unstable bounding volume hierarchy causes gaps, shadow acne, and flicker; consistently evaluate in double or carefully-ordered floats. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why does bounding volume hierarchy matter more in a GPU raytracer - justify your answer with a concrete production example.
**A:** Because millions of rays run concurrently; bounding volume hierarchy determines whether each thread can proceed independently or stalls on divergent geometry work. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What is the purpose of bounding volume hierarchy in a raytracer - justify your answer with a concrete production example.
**A:** It defines how geometric questions are answered for each pixel ray, converting abstract scene data into visible color contributions. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What is the purpose of bounding volume hierarchy in a raytracer - justify your answer with a concrete production example.
**A:** It defines how geometric questions are answered for each pixel ray, converting abstract scene data into visible color contributions. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why does bounding volume hierarchy matter more in a GPU raytracer - justify your answer with a concrete production example.
**A:** Because millions of rays run concurrently; bounding volume hierarchy determines whether each thread can proceed independently or stalls on divergent geometry work. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: Describe the main correctness concern in bounding volume hierarchy - justify your answer with a concrete production example.
**A:** Precision: numerically unstable bounding volume hierarchy causes gaps, shadow acne, and flicker; consistently evaluate in double or carefully-ordered floats. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How does bounding volume hierarchy affect perceptual quality - justify your answer with a concrete production example.
**A:** Small errors in bounding volume hierarchy show up as aliasing, hard shadows, or wrong silhouettes long before an average viewer can name the cause. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What is the standard way to structure bounding volume hierarchy code - justify your answer with a concrete production example.
**A:** Separate pure functions (no state) so bounding volume hierarchy compiles to fast device code and can be unit-tested on the host with the same inputs. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How do you benchmark bounding volume hierarchy - justify your answer with a concrete production example.
**A:** Render a fixed scene at multiple resolutions, measure rays/second, and compare against an analytic ground truth for identical camera settings. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: When does bounding volume hierarchy produce artifacts - justify your answer with a concrete production example.
**A:** When step sizes, tolerances, or intersection epsilons are tuned wrong - the classic acne/darkening trade-off of bounding volume hierarchy. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How should bounding volume hierarchy handle edge cases like grazing angles - justify your answer with a concrete production example.
**A:** Use robust predicates and minimum epsilon displacements so bounding volume hierarchy stays stable exactly where classic plane tests degenerate. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What relationship does bounding volume hierarchy have with the rest of the pipeline - justify your answer with a concrete production example.
**A:** bounding volume hierarchy produces the input for shading and post-processing; any error here is amplified by everything downstream. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How do you make bounding volume hierarchy deterministic across runs - justify your answer with a concrete production example.
**A:** Fix the accumulation order and sampling seed per pixel so bounding volume hierarchy reproduces bit-identical output for the same scene and parameters. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: Give a production example of bounding volume hierarchy in the black-hole visualizer - justify your answer with a concrete production example.
**A:** Tracing a photon through the accretion flow uses bounding volume hierarchy at every step: intersect the disk plane, sample the field, and terminate at horizon or sky. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What should you test about bounding volume hierarchy - justify your answer with a concrete production example.
**A:** Golden images for a handful of scenes, analytic sizes for primitive shapes, and monotonic quality as samples increase for bounding volume hierarchy. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How does bounding volume hierarchy interact with antialiasing - justify your answer with a concrete production example.
**A:** Antialiasing launches many slightly different rays; bounding volume hierarchy must keep their per-ray state separate so samples blend correctly. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What falls in the domain of bounding volume hierarchy vs rendering - justify your answer with a concrete production example.
**A:** bounding volume hierarchy is geometric answer-finding; rendering decides color, lighting, and tone mapping from those answers - keep the boundary clean. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What is the most common performance trap in bounding volume hierarchy - justify your answer with a concrete production example.
**A:** Recomputing the same expensive data per ray instead of caching it in constant or shared memory before the bounding volume hierarchy loop starts. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How do you explain bounding volume hierarchy trade-offs on a single slide - justify your answer with a concrete production example.
**A:** A table: approach, cost per ray, memory, robustness, and GPU friendliness - summarize bounding volume hierarchy options in one comparison view. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What happens if bounding volume hierarchy is not monotonic with samples - justify your answer with a concrete production example.
**A:** The image converges to the wrong value, revealing a bug; bounding volume hierarchy results must approach a stable limit as sampling grows. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How do you port bounding volume hierarchy from CPU to GPU - justify your answer with a concrete production example.
**A:** Keep the math identical in device functions, inline the hot loops, and replace heap allocations with pre-allocated buffers for bounding volume hierarchy. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What are the output guarantees of bounding volume hierarchy - justify your answer with a concrete production example.
**A:** A per-pixel radiance estimate (and optionally depth/ray state) that downstream tone mapping can trust - the contract of bounding volume hierarchy. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: When is brute force acceptable for bounding volume hierarchy - justify your answer with a concrete production example.
**A:** For a handful of primitives or when ray count dominates; then the cost of bounding volume hierarchy acceleration structures exceeds their savings. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: How does bounding volume hierarchy fit into a modular architecture - justify your answer with a concrete production example.
**A:** As a component behind a stable interface - the renderer calls bounding volume hierarchy and never depends on its implementation details. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What does a rigorous test suite assert about bounding volume hierarchy - justify your answer with a concrete production example.
**A:** Correctness on constructed scenes, performance on a benchmark scene, and stability (no NaN/Inf) across resolution ranges. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What tools measure bounding volume hierarchy quality - justify your answer with a concrete production example.
**A:** A/B images, per-pixel error maps against reference, and error-vs-samples curves are the quantitative tools for bounding volume hierarchy. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How do you teach bounding volume hierarchy fundamentals - justify your answer with a concrete production example.
**A:** Start with a pinhole camera and a sphere; every later feature builds on the same try-a-ray, find-an-answer shape of bounding volume hierarchy. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How do you teach bounding volume hierarchy fundamentals - justify your answer with a concrete production example.
**A:** Start with a pinhole camera and a sphere; every later feature builds on the same try-a-ray, find-an-answer shape of bounding volume hierarchy. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What tools measure bounding volume hierarchy quality - justify your answer with a concrete production example.
**A:** A/B images, per-pixel error maps against reference, and error-vs-samples curves are the quantitative tools for bounding volume hierarchy. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What does a rigorous test suite assert about bounding volume hierarchy - justify your answer with a concrete production example.
**A:** Correctness on constructed scenes, performance on a benchmark scene, and stability (no NaN/Inf) across resolution ranges. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How does bounding volume hierarchy fit into a modular architecture - justify your answer with a concrete production example.
**A:** As a component behind a stable interface - the renderer calls bounding volume hierarchy and never depends on its implementation details. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: When is brute force acceptable for bounding volume hierarchy - justify your answer with a concrete production example.
**A:** For a handful of primitives or when ray count dominates; then the cost of bounding volume hierarchy acceleration structures exceeds their savings. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What are the output guarantees of bounding volume hierarchy - justify your answer with a concrete production example.
**A:** A per-pixel radiance estimate (and optionally depth/ray state) that downstream tone mapping can trust - the contract of bounding volume hierarchy. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How do you port bounding volume hierarchy from CPU to GPU - justify your answer with a concrete production example.
**A:** Keep the math identical in device functions, inline the hot loops, and replace heap allocations with pre-allocated buffers for bounding volume hierarchy. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What happens if bounding volume hierarchy is not monotonic with samples - justify your answer with a concrete production example.
**A:** The image converges to the wrong value, revealing a bug; bounding volume hierarchy results must approach a stable limit as sampling grows. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you explain bounding volume hierarchy trade-offs on a single slide - justify your answer with a concrete production example.
**A:** A table: approach, cost per ray, memory, robustness, and GPU friendliness - summarize bounding volume hierarchy options in one comparison view. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What is the most common performance trap in bounding volume hierarchy - justify your answer with a concrete production example.
**A:** Recomputing the same expensive data per ray instead of caching it in constant or shared memory before the bounding volume hierarchy loop starts. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What falls in the domain of bounding volume hierarchy vs rendering - justify your answer with a concrete production example.
**A:** bounding volume hierarchy is geometric answer-finding; rendering decides color, lighting, and tone mapping from those answers - keep the boundary clean. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How does bounding volume hierarchy interact with antialiasing - justify your answer with a concrete production example.
**A:** Antialiasing launches many slightly different rays; bounding volume hierarchy must keep their per-ray state separate so samples blend correctly. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What should you test about bounding volume hierarchy - justify your answer with a concrete production example.
**A:** Golden images for a handful of scenes, analytic sizes for primitive shapes, and monotonic quality as samples increase for bounding volume hierarchy. A concrete example: consistently applying bounding volume hierarchy in code review and regression tests keeps the whole pipeline trustworthy.
