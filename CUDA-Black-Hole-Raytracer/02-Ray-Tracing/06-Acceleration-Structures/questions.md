# Ray Tracing — Acceleration Structures Interview Questions and Answers

## Q1: What is an acceleration structure?
**A:** A spatial index (grid, BVH, octree) that prunes empty regions so ray-primitive tests skip space the ray never crosses - the difference between interactive and nightly renders.

## Q2: Why does the black-hole visualizer use them?
**A:** For the background starfield and disk primitives: without pruning, every ray tests every star; with a structure, rays only test tokens in crossed cells.

## Q3: What are the two families?
**A:** Grid-based (uniform/spatial hash, octree, AMR) and object-based (BVH, R-tree); grids excel at uniform scenes, BVH at varying densities.

## Q4: How do you classify a structure by ray-time efficiency?
**A:** Average intersections per ray: grid ~ build cells such that primitives per cell ~1; BVH ~ log(N) with good splitting; the metric is (traversal cost + test cost)/ray.

## Q5: What is the build-vs-trace trade-off?
**A:** Structures take build time amortized over many rays; a static sky builds once and pays off instantly, while a per-frame changing field can dominate rent.

## Q6: When is brute force acceptable?
**A:** Below ~20 primitives, direct testing wins because structure traversal (branching, memory hops) costs more than it saves.

## Q7: What does the 'N/population' rule for grids say?
**A:** Pick cell size so primitives/cell is ~1-3; too fine (many empty cells) wastes traversal, too coarse (many primitives) wastes tests.

## Q8: What is the traversal of a grid?
**A:** The 3D-DDA marches the ray cell by cell, testing primitives in each; the horizontal + vertical exit code from Amanatides & Woo handles accuracy.

## Q9: What is a BVH node?
**A:** An axis-aligned bounding box with either a primitive or two children; traversal descends both boxes the ray hits - the standard acceleration for triangle scenes.

## Q10: What is a surface-area heuristic (SAH)?
**A:** Chooses split planes minimizing estimated cost c = C(primitives) based on surface areas of child boxes - the near-optimal split for BVHs.

## Q11: What is the pyramid/octree variant?
**A:** An octree subdivides cubes adaptively into 8 children - best for adaptive plasma grids where cell density varies as it does near the horizon.

## Q12: What is the memory cost of structures?
**A:** Grids index cells (offset arrays); BVH nodes ~24-32B each; octrees bloom memory if unpruned - budget structures against the texture arrays they speed up.

## Q13: How do structures interact with cache?
**A:** Traversal chases pointers (BVH) or strides (grid); packing nodes in memory-contiguous arrays (SOA) and using 64-bit indices keeps cache lines hot.

## Q14: What is the standard way to move structures to device?
**A:** Build on host, then upload node/primitive arrays to constant/global memory; device builds are possible but host-build-then-copy is the simplest correct path.

## Q15: How do you verify a structure?
**A:** Render the same scene with and without the structure and assert pixel-identical output - accelerations must never change results, only speed.

## Q16: What is the purpose of acceleration structures in a raytracer?
**A:** It defines how geometric questions are answered for each pixel ray, converting abstract scene data into visible color contributions.

## Q17: Why does acceleration structures matter more in a GPU raytracer?
**A:** Because millions of rays run concurrently; acceleration structures determines whether each thread can proceed independently or stalls on divergent geometry work.

## Q18: Describe the main correctness concern in acceleration structures.
**A:** Precision: numerically unstable acceleration structures causes gaps, shadow acne, and flicker; consistently evaluate in double or carefully-ordered floats.

## Q19: How does acceleration structures affect perceptual quality?
**A:** Small errors in acceleration structures show up as aliasing, hard shadows, or wrong silhouettes long before an average viewer can name the cause.

## Q20: What is the standard way to structure acceleration structures code?
**A:** Separate pure functions (no state) so acceleration structures compiles to fast device code and can be unit-tested on the host with the same inputs.

## Q21: How do you benchmark acceleration structures?
**A:** Render a fixed scene at multiple resolutions, measure rays/second, and compare against an analytic ground truth for identical camera settings.

## Q22: When does acceleration structures produce artifacts?
**A:** When step sizes, tolerances, or intersection epsilons are tuned wrong - the classic acne/darkening trade-off of acceleration structures.

## Q23: How should acceleration structures handle edge cases like grazing angles?
**A:** Use robust predicates and minimum epsilon displacements so acceleration structures stays stable exactly where classic plane tests degenerate.

## Q24: What relationship does acceleration structures have with the rest of the pipeline?
**A:** acceleration structures produces the input for shading and post-processing; any error here is amplified by everything downstream.

## Q25: How do you make acceleration structures deterministic across runs?
**A:** Fix the accumulation order and sampling seed per pixel so acceleration structures reproduces bit-identical output for the same scene and parameters.

## Q26: Give a production example of acceleration structures in the black-hole visualizer.
**A:** Tracing a photon through the accretion flow uses acceleration structures at every step: intersect the disk plane, sample the field, and terminate at horizon or sky.

## Q27: What should you test about acceleration structures?
**A:** Golden images for a handful of scenes, analytic sizes for primitive shapes, and monotonic quality as samples increase for acceleration structures.

## Q28: How does acceleration structures interact with antialiasing?
**A:** Antialiasing launches many slightly different rays; acceleration structures must keep their per-ray state separate so samples blend correctly.

## Q29: What falls in the domain of acceleration structures vs rendering?
**A:** acceleration structures is geometric answer-finding; rendering decides color, lighting, and tone mapping from those answers - keep the boundary clean.

## Q30: What is the most common performance trap in acceleration structures?
**A:** Recomputing the same expensive data per ray instead of caching it in constant or shared memory before the acceleration structures loop starts.

## Q31: How do you explain acceleration structures trade-offs on a single slide?
**A:** A table: approach, cost per ray, memory, robustness, and GPU friendliness - summarize acceleration structures options in one comparison view.

## Q32: What happens if acceleration structures is not monotonic with samples?
**A:** The image converges to the wrong value, revealing a bug; acceleration structures results must approach a stable limit as sampling grows.

## Q33: How do you port acceleration structures from CPU to GPU?
**A:** Keep the math identical in device functions, inline the hot loops, and replace heap allocations with pre-allocated buffers for acceleration structures.

## Q34: What are the output guarantees of acceleration structures?
**A:** A per-pixel radiance estimate (and optionally depth/ray state) that downstream tone mapping can trust - the contract of acceleration structures.

## Q35: When is brute force acceptable for acceleration structures?
**A:** For a handful of primitives or when ray count dominates; then the cost of acceleration structures acceleration structures exceeds their savings.

## Q36: How does acceleration structures fit into a modular architecture?
**A:** As a component behind a stable interface - the renderer calls acceleration structures and never depends on its implementation details.

## Q37: What does a rigorous test suite assert about acceleration structures?
**A:** Correctness on constructed scenes, performance on a benchmark scene, and stability (no NaN/Inf) across resolution ranges.

## Q38: What tools measure acceleration structures quality?
**A:** A/B images, per-pixel error maps against reference, and error-vs-samples curves are the quantitative tools for acceleration structures.

## Q39: How do you teach acceleration structures fundamentals?
**A:** Start with a pinhole camera and a sphere; every later feature builds on the same try-a-ray, find-an-answer shape of acceleration structures.

## Q40: How do you teach acceleration structures fundamentals - justify your answer with a concrete production example.
**A:** Start with a pinhole camera and a sphere; every later feature builds on the same try-a-ray, find-an-answer shape of acceleration structures. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What tools measure acceleration structures quality - justify your answer with a concrete production example.
**A:** A/B images, per-pixel error maps against reference, and error-vs-samples curves are the quantitative tools for acceleration structures. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: What does a rigorous test suite assert about acceleration structures - justify your answer with a concrete production example.
**A:** Correctness on constructed scenes, performance on a benchmark scene, and stability (no NaN/Inf) across resolution ranges. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: How does acceleration structures fit into a modular architecture - justify your answer with a concrete production example.
**A:** As a component behind a stable interface - the renderer calls acceleration structures and never depends on its implementation details. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: When is brute force acceptable for acceleration structures - justify your answer with a concrete production example.
**A:** For a handful of primitives or when ray count dominates; then the cost of acceleration structures acceleration structures exceeds their savings. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: What are the output guarantees of acceleration structures - justify your answer with a concrete production example.
**A:** A per-pixel radiance estimate (and optionally depth/ray state) that downstream tone mapping can trust - the contract of acceleration structures. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: How do you port acceleration structures from CPU to GPU - justify your answer with a concrete production example.
**A:** Keep the math identical in device functions, inline the hot loops, and replace heap allocations with pre-allocated buffers for acceleration structures. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: What happens if acceleration structures is not monotonic with samples - justify your answer with a concrete production example.
**A:** The image converges to the wrong value, revealing a bug; acceleration structures results must approach a stable limit as sampling grows. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: How do you explain acceleration structures trade-offs on a single slide - justify your answer with a concrete production example.
**A:** A table: approach, cost per ray, memory, robustness, and GPU friendliness - summarize acceleration structures options in one comparison view. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What is the most common performance trap in acceleration structures - justify your answer with a concrete production example.
**A:** Recomputing the same expensive data per ray instead of caching it in constant or shared memory before the acceleration structures loop starts. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: What falls in the domain of acceleration structures vs rendering - justify your answer with a concrete production example.
**A:** acceleration structures is geometric answer-finding; rendering decides color, lighting, and tone mapping from those answers - keep the boundary clean. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: How does acceleration structures interact with antialiasing - justify your answer with a concrete production example.
**A:** Antialiasing launches many slightly different rays; acceleration structures must keep their per-ray state separate so samples blend correctly. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: What should you test about acceleration structures - justify your answer with a concrete production example.
**A:** Golden images for a handful of scenes, analytic sizes for primitive shapes, and monotonic quality as samples increase for acceleration structures. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: Give a production example of acceleration structures in the black-hole visualizer - justify your answer with a concrete production example.
**A:** Tracing a photon through the accretion flow uses acceleration structures at every step: intersect the disk plane, sample the field, and terminate at horizon or sky. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: How do you make acceleration structures deterministic across runs - justify your answer with a concrete production example.
**A:** Fix the accumulation order and sampling seed per pixel so acceleration structures reproduces bit-identical output for the same scene and parameters. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: What relationship does acceleration structures have with the rest of the pipeline - justify your answer with a concrete production example.
**A:** acceleration structures produces the input for shading and post-processing; any error here is amplified by everything downstream. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: How should acceleration structures handle edge cases like grazing angles - justify your answer with a concrete production example.
**A:** Use robust predicates and minimum epsilon displacements so acceleration structures stays stable exactly where classic plane tests degenerate. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: When does acceleration structures produce artifacts - justify your answer with a concrete production example.
**A:** When step sizes, tolerances, or intersection epsilons are tuned wrong - the classic acne/darkening trade-off of acceleration structures. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: How do you benchmark acceleration structures - justify your answer with a concrete production example.
**A:** Render a fixed scene at multiple resolutions, measure rays/second, and compare against an analytic ground truth for identical camera settings. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: What is the standard way to structure acceleration structures code - justify your answer with a concrete production example.
**A:** Separate pure functions (no state) so acceleration structures compiles to fast device code and can be unit-tested on the host with the same inputs. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: How does acceleration structures affect perceptual quality - justify your answer with a concrete production example.
**A:** Small errors in acceleration structures show up as aliasing, hard shadows, or wrong silhouettes long before an average viewer can name the cause. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: Describe the main correctness concern in acceleration structures - justify your answer with a concrete production example.
**A:** Precision: numerically unstable acceleration structures causes gaps, shadow acne, and flicker; consistently evaluate in double or carefully-ordered floats. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: Why does acceleration structures matter more in a GPU raytracer - justify your answer with a concrete production example.
**A:** Because millions of rays run concurrently; acceleration structures determines whether each thread can proceed independently or stalls on divergent geometry work. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What is the purpose of acceleration structures in a raytracer - justify your answer with a concrete production example.
**A:** It defines how geometric questions are answered for each pixel ray, converting abstract scene data into visible color contributions. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: What is the purpose of acceleration structures in a raytracer - justify your answer with a concrete production example.
**A:** It defines how geometric questions are answered for each pixel ray, converting abstract scene data into visible color contributions. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Why does acceleration structures matter more in a GPU raytracer - justify your answer with a concrete production example.
**A:** Because millions of rays run concurrently; acceleration structures determines whether each thread can proceed independently or stalls on divergent geometry work. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: Describe the main correctness concern in acceleration structures - justify your answer with a concrete production example.
**A:** Precision: numerically unstable acceleration structures causes gaps, shadow acne, and flicker; consistently evaluate in double or carefully-ordered floats. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: How does acceleration structures affect perceptual quality - justify your answer with a concrete production example.
**A:** Small errors in acceleration structures show up as aliasing, hard shadows, or wrong silhouettes long before an average viewer can name the cause. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: What is the standard way to structure acceleration structures code - justify your answer with a concrete production example.
**A:** Separate pure functions (no state) so acceleration structures compiles to fast device code and can be unit-tested on the host with the same inputs. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: How do you benchmark acceleration structures - justify your answer with a concrete production example.
**A:** Render a fixed scene at multiple resolutions, measure rays/second, and compare against an analytic ground truth for identical camera settings. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: When does acceleration structures produce artifacts - justify your answer with a concrete production example.
**A:** When step sizes, tolerances, or intersection epsilons are tuned wrong - the classic acne/darkening trade-off of acceleration structures. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: How should acceleration structures handle edge cases like grazing angles - justify your answer with a concrete production example.
**A:** Use robust predicates and minimum epsilon displacements so acceleration structures stays stable exactly where classic plane tests degenerate. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: What relationship does acceleration structures have with the rest of the pipeline - justify your answer with a concrete production example.
**A:** acceleration structures produces the input for shading and post-processing; any error here is amplified by everything downstream. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: How do you make acceleration structures deterministic across runs - justify your answer with a concrete production example.
**A:** Fix the accumulation order and sampling seed per pixel so acceleration structures reproduces bit-identical output for the same scene and parameters. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: Give a production example of acceleration structures in the black-hole visualizer - justify your answer with a concrete production example.
**A:** Tracing a photon through the accretion flow uses acceleration structures at every step: intersect the disk plane, sample the field, and terminate at horizon or sky. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: What should you test about acceleration structures - justify your answer with a concrete production example.
**A:** Golden images for a handful of scenes, analytic sizes for primitive shapes, and monotonic quality as samples increase for acceleration structures. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: How does acceleration structures interact with antialiasing - justify your answer with a concrete production example.
**A:** Antialiasing launches many slightly different rays; acceleration structures must keep their per-ray state separate so samples blend correctly. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What falls in the domain of acceleration structures vs rendering - justify your answer with a concrete production example.
**A:** acceleration structures is geometric answer-finding; rendering decides color, lighting, and tone mapping from those answers - keep the boundary clean. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: What is the most common performance trap in acceleration structures - justify your answer with a concrete production example.
**A:** Recomputing the same expensive data per ray instead of caching it in constant or shared memory before the acceleration structures loop starts. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: How do you explain acceleration structures trade-offs on a single slide - justify your answer with a concrete production example.
**A:** A table: approach, cost per ray, memory, robustness, and GPU friendliness - summarize acceleration structures options in one comparison view. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: What happens if acceleration structures is not monotonic with samples - justify your answer with a concrete production example.
**A:** The image converges to the wrong value, revealing a bug; acceleration structures results must approach a stable limit as sampling grows. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: How do you port acceleration structures from CPU to GPU - justify your answer with a concrete production example.
**A:** Keep the math identical in device functions, inline the hot loops, and replace heap allocations with pre-allocated buffers for acceleration structures. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: What are the output guarantees of acceleration structures - justify your answer with a concrete production example.
**A:** A per-pixel radiance estimate (and optionally depth/ray state) that downstream tone mapping can trust - the contract of acceleration structures. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: When is brute force acceptable for acceleration structures - justify your answer with a concrete production example.
**A:** For a handful of primitives or when ray count dominates; then the cost of acceleration structures acceleration structures exceeds their savings. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: How does acceleration structures fit into a modular architecture - justify your answer with a concrete production example.
**A:** As a component behind a stable interface - the renderer calls acceleration structures and never depends on its implementation details. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What does a rigorous test suite assert about acceleration structures - justify your answer with a concrete production example.
**A:** Correctness on constructed scenes, performance on a benchmark scene, and stability (no NaN/Inf) across resolution ranges. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: What tools measure acceleration structures quality - justify your answer with a concrete production example.
**A:** A/B images, per-pixel error maps against reference, and error-vs-samples curves are the quantitative tools for acceleration structures. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How do you teach acceleration structures fundamentals - justify your answer with a concrete production example.
**A:** Start with a pinhole camera and a sphere; every later feature builds on the same try-a-ray, find-an-answer shape of acceleration structures. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: How do you teach acceleration structures fundamentals - justify your answer with a concrete production example.
**A:** Start with a pinhole camera and a sphere; every later feature builds on the same try-a-ray, find-an-answer shape of acceleration structures. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What tools measure acceleration structures quality - justify your answer with a concrete production example.
**A:** A/B images, per-pixel error maps against reference, and error-vs-samples curves are the quantitative tools for acceleration structures. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: What does a rigorous test suite assert about acceleration structures - justify your answer with a concrete production example.
**A:** Correctness on constructed scenes, performance on a benchmark scene, and stability (no NaN/Inf) across resolution ranges. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: How does acceleration structures fit into a modular architecture - justify your answer with a concrete production example.
**A:** As a component behind a stable interface - the renderer calls acceleration structures and never depends on its implementation details. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: When is brute force acceptable for acceleration structures - justify your answer with a concrete production example.
**A:** For a handful of primitives or when ray count dominates; then the cost of acceleration structures acceleration structures exceeds their savings. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: What are the output guarantees of acceleration structures - justify your answer with a concrete production example.
**A:** A per-pixel radiance estimate (and optionally depth/ray state) that downstream tone mapping can trust - the contract of acceleration structures. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: How do you port acceleration structures from CPU to GPU - justify your answer with a concrete production example.
**A:** Keep the math identical in device functions, inline the hot loops, and replace heap allocations with pre-allocated buffers for acceleration structures. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: What happens if acceleration structures is not monotonic with samples - justify your answer with a concrete production example.
**A:** The image converges to the wrong value, revealing a bug; acceleration structures results must approach a stable limit as sampling grows. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: How do you explain acceleration structures trade-offs on a single slide - justify your answer with a concrete production example.
**A:** A table: approach, cost per ray, memory, robustness, and GPU friendliness - summarize acceleration structures options in one comparison view. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What is the most common performance trap in acceleration structures - justify your answer with a concrete production example.
**A:** Recomputing the same expensive data per ray instead of caching it in constant or shared memory before the acceleration structures loop starts. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: What falls in the domain of acceleration structures vs rendering - justify your answer with a concrete production example.
**A:** acceleration structures is geometric answer-finding; rendering decides color, lighting, and tone mapping from those answers - keep the boundary clean. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: How does acceleration structures interact with antialiasing - justify your answer with a concrete production example.
**A:** Antialiasing launches many slightly different rays; acceleration structures must keep their per-ray state separate so samples blend correctly. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: What should you test about acceleration structures - justify your answer with a concrete production example.
**A:** Golden images for a handful of scenes, analytic sizes for primitive shapes, and monotonic quality as samples increase for acceleration structures. A concrete example: consistently applying acceleration structures in code review and regression tests keeps the whole pipeline trustworthy.
