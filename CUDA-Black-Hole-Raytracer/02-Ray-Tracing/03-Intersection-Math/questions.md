# Ray Tracing — Intersection Math Interview Questions and Answers

## Q1: What is ray-object intersection?
**A:** Finding where a ray (o + td, t>0) meets a surface; the 't' at the hit, the normal, and (for shading) whether the hit is front/back are computed.

## Q2: How do you solve ray-sphere intersection?
**A:** Intersect |o+td - c|^2 = R^2: a quadratic in t; discriminant < 0 -> miss, else t = (-b - sqrt(disc))/(2a) and the hit normal = (hit - c)/R.

## Q3: What is the reference-plane intersection used in disk renders?
**A:** For a flat disk, intersect the ray with the equatorial plane z=0: t = -oz/dz (if dz != 0) | r(radius from the hole) decides inside/outside of the flow.

## Q4: What is an ellipse/ellipsoid intersection?
**A:** Substitute the ray into ((x-cx)/a)^2+...=1 to get a quadratic in t with the same discriminant logic - used for tilted or warped emitter surfaces.

## Q5: What is the significance of 't>0'?
**A:** t must be positive (in front); a negative t is 'behind' the origin - or for a secondary scatter, past the previous event - so every hit test clamps t to the forward domain.

## Q6: What is the epsilon-trick in intersection?
**A:** Offsetting the origin or comparing t to a small epsilon avoids self-intersection and acne at grazing contacts - where rays start exactly on a surface.

## Q7: How do you compute simple normals for shading?
**A:** Sphere: normalize(hit - center); plane: its constant normal; triangle: normalized cross product of edges - tempered by interpolation for smooth meshes.

## Q8: What is the difference between geometric and shading intersection?
**A:** Geometric answers (where? which side? which t?) vs the shading's use of that answer (position, normal, material); keep them separate functions.

## Q9: Why is a disk emitter often approximated analytically?
**A:** The accretion flow is really volumetric, but a collapsed planar + radial emissivity only reaches closed-form integration that is a perfect validation target.

## Q10: What numerical care does intersection need in double?
**A:** Quadratics with large coefficients (radius vs distance scales) lose accuracy; dividing by R^2 and solving in double prevents false misses at distant disks.

## Q11: How do you test intersections?
**A:** Fire grids of rays at known shapes (sphere radius R at origin) and assert t equals the closed form within tolerance and misses at |b|>R.

## Q12: What are the degenerate cases for plane intersection?
**A:** dz == 0 (parallel ray) - return no hit; rays from the plane (t=0) - require t>eps to avoid self-intersection feedback.

## Q13: How does intersection feed the anisotropic disk?
**A:** Hit points give radius r, azimuth phi, and orbital motion where the boosted emissivity is evaluated - intersection is the geometry gate for texture sampling.

## Q14: What happens when the ray passes exactly through the hole center?
**A:** It can produce t with dz=0 or a degenerate on-plane condition - handle as a 'miss disk, continue to sky/horizon' fallback actively.

## Q15: What is the purpose of intersection math in a raytracer?
**A:** It defines how geometric questions are answered for each pixel ray, converting abstract scene data into visible color contributions.

## Q16: Why does intersection math matter more in a GPU raytracer?
**A:** Because millions of rays run concurrently; intersection math determines whether each thread can proceed independently or stalls on divergent geometry work.

## Q17: Describe the main correctness concern in intersection math.
**A:** Precision: numerically unstable intersection math causes gaps, shadow acne, and flicker; consistently evaluate in double or carefully-ordered floats.

## Q18: How does intersection math affect perceptual quality?
**A:** Small errors in intersection math show up as aliasing, hard shadows, or wrong silhouettes long before an average viewer can name the cause.

## Q19: What is the standard way to structure intersection math code?
**A:** Separate pure functions (no state) so intersection math compiles to fast device code and can be unit-tested on the host with the same inputs.

## Q20: How do you benchmark intersection math?
**A:** Render a fixed scene at multiple resolutions, measure rays/second, and compare against an analytic ground truth for identical camera settings.

## Q21: When does intersection math produce artifacts?
**A:** When step sizes, tolerances, or intersection epsilons are tuned wrong - the classic acne/darkening trade-off of intersection math.

## Q22: How should intersection math handle edge cases like grazing angles?
**A:** Use robust predicates and minimum epsilon displacements so intersection math stays stable exactly where classic plane tests degenerate.

## Q23: What relationship does intersection math have with the rest of the pipeline?
**A:** intersection math produces the input for shading and post-processing; any error here is amplified by everything downstream.

## Q24: How do you make intersection math deterministic across runs?
**A:** Fix the accumulation order and sampling seed per pixel so intersection math reproduces bit-identical output for the same scene and parameters.

## Q25: Give a production example of intersection math in the black-hole visualizer.
**A:** Tracing a photon through the accretion flow uses intersection math at every step: intersect the disk plane, sample the field, and terminate at horizon or sky.

## Q26: What should you test about intersection math?
**A:** Golden images for a handful of scenes, analytic sizes for primitive shapes, and monotonic quality as samples increase for intersection math.

## Q27: How does intersection math interact with antialiasing?
**A:** Antialiasing launches many slightly different rays; intersection math must keep their per-ray state separate so samples blend correctly.

## Q28: What falls in the domain of intersection math vs rendering?
**A:** intersection math is geometric answer-finding; rendering decides color, lighting, and tone mapping from those answers - keep the boundary clean.

## Q29: What is the most common performance trap in intersection math?
**A:** Recomputing the same expensive data per ray instead of caching it in constant or shared memory before the intersection math loop starts.

## Q30: How do you explain intersection math trade-offs on a single slide?
**A:** A table: approach, cost per ray, memory, robustness, and GPU friendliness - summarize intersection math options in one comparison view.

## Q31: What happens if intersection math is not monotonic with samples?
**A:** The image converges to the wrong value, revealing a bug; intersection math results must approach a stable limit as sampling grows.

## Q32: How do you port intersection math from CPU to GPU?
**A:** Keep the math identical in device functions, inline the hot loops, and replace heap allocations with pre-allocated buffers for intersection math.

## Q33: What are the output guarantees of intersection math?
**A:** A per-pixel radiance estimate (and optionally depth/ray state) that downstream tone mapping can trust - the contract of intersection math.

## Q34: When is brute force acceptable for intersection math?
**A:** For a handful of primitives or when ray count dominates; then the cost of intersection math acceleration structures exceeds their savings.

## Q35: How does intersection math fit into a modular architecture?
**A:** As a component behind a stable interface - the renderer calls intersection math and never depends on its implementation details.

## Q36: What does a rigorous test suite assert about intersection math?
**A:** Correctness on constructed scenes, performance on a benchmark scene, and stability (no NaN/Inf) across resolution ranges.

## Q37: What tools measure intersection math quality?
**A:** A/B images, per-pixel error maps against reference, and error-vs-samples curves are the quantitative tools for intersection math.

## Q38: How do you teach intersection math fundamentals?
**A:** Start with a pinhole camera and a sphere; every later feature builds on the same try-a-ray, find-an-answer shape of intersection math.

## Q39: How do you teach intersection math fundamentals - justify your answer with a concrete production example.
**A:** Start with a pinhole camera and a sphere; every later feature builds on the same try-a-ray, find-an-answer shape of intersection math. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: What tools measure intersection math quality - justify your answer with a concrete production example.
**A:** A/B images, per-pixel error maps against reference, and error-vs-samples curves are the quantitative tools for intersection math. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What does a rigorous test suite assert about intersection math - justify your answer with a concrete production example.
**A:** Correctness on constructed scenes, performance on a benchmark scene, and stability (no NaN/Inf) across resolution ranges. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does intersection math fit into a modular architecture - justify your answer with a concrete production example.
**A:** As a component behind a stable interface - the renderer calls intersection math and never depends on its implementation details. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: When is brute force acceptable for intersection math - justify your answer with a concrete production example.
**A:** For a handful of primitives or when ray count dominates; then the cost of intersection math acceleration structures exceeds their savings. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What are the output guarantees of intersection math - justify your answer with a concrete production example.
**A:** A per-pixel radiance estimate (and optionally depth/ray state) that downstream tone mapping can trust - the contract of intersection math. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: How do you port intersection math from CPU to GPU - justify your answer with a concrete production example.
**A:** Keep the math identical in device functions, inline the hot loops, and replace heap allocations with pre-allocated buffers for intersection math. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What happens if intersection math is not monotonic with samples - justify your answer with a concrete production example.
**A:** The image converges to the wrong value, revealing a bug; intersection math results must approach a stable limit as sampling grows. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How do you explain intersection math trade-offs on a single slide - justify your answer with a concrete production example.
**A:** A table: approach, cost per ray, memory, robustness, and GPU friendliness - summarize intersection math options in one comparison view. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What is the most common performance trap in intersection math - justify your answer with a concrete production example.
**A:** Recomputing the same expensive data per ray instead of caching it in constant or shared memory before the intersection math loop starts. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What falls in the domain of intersection math vs rendering - justify your answer with a concrete production example.
**A:** intersection math is geometric answer-finding; rendering decides color, lighting, and tone mapping from those answers - keep the boundary clean. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How does intersection math interact with antialiasing - justify your answer with a concrete production example.
**A:** Antialiasing launches many slightly different rays; intersection math must keep their per-ray state separate so samples blend correctly. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What should you test about intersection math - justify your answer with a concrete production example.
**A:** Golden images for a handful of scenes, analytic sizes for primitive shapes, and monotonic quality as samples increase for intersection math. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: Give a production example of intersection math in the black-hole visualizer - justify your answer with a concrete production example.
**A:** Tracing a photon through the accretion flow uses intersection math at every step: intersect the disk plane, sample the field, and terminate at horizon or sky. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: How do you make intersection math deterministic across runs - justify your answer with a concrete production example.
**A:** Fix the accumulation order and sampling seed per pixel so intersection math reproduces bit-identical output for the same scene and parameters. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: What relationship does intersection math have with the rest of the pipeline - justify your answer with a concrete production example.
**A:** intersection math produces the input for shading and post-processing; any error here is amplified by everything downstream. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: How should intersection math handle edge cases like grazing angles - justify your answer with a concrete production example.
**A:** Use robust predicates and minimum epsilon displacements so intersection math stays stable exactly where classic plane tests degenerate. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: When does intersection math produce artifacts - justify your answer with a concrete production example.
**A:** When step sizes, tolerances, or intersection epsilons are tuned wrong - the classic acne/darkening trade-off of intersection math. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How do you benchmark intersection math - justify your answer with a concrete production example.
**A:** Render a fixed scene at multiple resolutions, measure rays/second, and compare against an analytic ground truth for identical camera settings. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the standard way to structure intersection math code - justify your answer with a concrete production example.
**A:** Separate pure functions (no state) so intersection math compiles to fast device code and can be unit-tested on the host with the same inputs. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How does intersection math affect perceptual quality - justify your answer with a concrete production example.
**A:** Small errors in intersection math show up as aliasing, hard shadows, or wrong silhouettes long before an average viewer can name the cause. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: Describe the main correctness concern in intersection math - justify your answer with a concrete production example.
**A:** Precision: numerically unstable intersection math causes gaps, shadow acne, and flicker; consistently evaluate in double or carefully-ordered floats. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: Why does intersection math matter more in a GPU raytracer - justify your answer with a concrete production example.
**A:** Because millions of rays run concurrently; intersection math determines whether each thread can proceed independently or stalls on divergent geometry work. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: What is the purpose of intersection math in a raytracer - justify your answer with a concrete production example.
**A:** It defines how geometric questions are answered for each pixel ray, converting abstract scene data into visible color contributions. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What is the purpose of intersection math in a raytracer - justify your answer with a concrete production example.
**A:** It defines how geometric questions are answered for each pixel ray, converting abstract scene data into visible color contributions. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: Why does intersection math matter more in a GPU raytracer - justify your answer with a concrete production example.
**A:** Because millions of rays run concurrently; intersection math determines whether each thread can proceed independently or stalls on divergent geometry work. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Describe the main correctness concern in intersection math - justify your answer with a concrete production example.
**A:** Precision: numerically unstable intersection math causes gaps, shadow acne, and flicker; consistently evaluate in double or carefully-ordered floats. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How does intersection math affect perceptual quality - justify your answer with a concrete production example.
**A:** Small errors in intersection math show up as aliasing, hard shadows, or wrong silhouettes long before an average viewer can name the cause. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What is the standard way to structure intersection math code - justify your answer with a concrete production example.
**A:** Separate pure functions (no state) so intersection math compiles to fast device code and can be unit-tested on the host with the same inputs. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How do you benchmark intersection math - justify your answer with a concrete production example.
**A:** Render a fixed scene at multiple resolutions, measure rays/second, and compare against an analytic ground truth for identical camera settings. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: When does intersection math produce artifacts - justify your answer with a concrete production example.
**A:** When step sizes, tolerances, or intersection epsilons are tuned wrong - the classic acne/darkening trade-off of intersection math. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How should intersection math handle edge cases like grazing angles - justify your answer with a concrete production example.
**A:** Use robust predicates and minimum epsilon displacements so intersection math stays stable exactly where classic plane tests degenerate. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What relationship does intersection math have with the rest of the pipeline - justify your answer with a concrete production example.
**A:** intersection math produces the input for shading and post-processing; any error here is amplified by everything downstream. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: How do you make intersection math deterministic across runs - justify your answer with a concrete production example.
**A:** Fix the accumulation order and sampling seed per pixel so intersection math reproduces bit-identical output for the same scene and parameters. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: Give a production example of intersection math in the black-hole visualizer - justify your answer with a concrete production example.
**A:** Tracing a photon through the accretion flow uses intersection math at every step: intersect the disk plane, sample the field, and terminate at horizon or sky. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What should you test about intersection math - justify your answer with a concrete production example.
**A:** Golden images for a handful of scenes, analytic sizes for primitive shapes, and monotonic quality as samples increase for intersection math. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How does intersection math interact with antialiasing - justify your answer with a concrete production example.
**A:** Antialiasing launches many slightly different rays; intersection math must keep their per-ray state separate so samples blend correctly. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What falls in the domain of intersection math vs rendering - justify your answer with a concrete production example.
**A:** intersection math is geometric answer-finding; rendering decides color, lighting, and tone mapping from those answers - keep the boundary clean. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What is the most common performance trap in intersection math - justify your answer with a concrete production example.
**A:** Recomputing the same expensive data per ray instead of caching it in constant or shared memory before the intersection math loop starts. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How do you explain intersection math trade-offs on a single slide - justify your answer with a concrete production example.
**A:** A table: approach, cost per ray, memory, robustness, and GPU friendliness - summarize intersection math options in one comparison view. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What happens if intersection math is not monotonic with samples - justify your answer with a concrete production example.
**A:** The image converges to the wrong value, revealing a bug; intersection math results must approach a stable limit as sampling grows. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How do you port intersection math from CPU to GPU - justify your answer with a concrete production example.
**A:** Keep the math identical in device functions, inline the hot loops, and replace heap allocations with pre-allocated buffers for intersection math. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: What are the output guarantees of intersection math - justify your answer with a concrete production example.
**A:** A per-pixel radiance estimate (and optionally depth/ray state) that downstream tone mapping can trust - the contract of intersection math. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: When is brute force acceptable for intersection math - justify your answer with a concrete production example.
**A:** For a handful of primitives or when ray count dominates; then the cost of intersection math acceleration structures exceeds their savings. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How does intersection math fit into a modular architecture - justify your answer with a concrete production example.
**A:** As a component behind a stable interface - the renderer calls intersection math and never depends on its implementation details. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What does a rigorous test suite assert about intersection math - justify your answer with a concrete production example.
**A:** Correctness on constructed scenes, performance on a benchmark scene, and stability (no NaN/Inf) across resolution ranges. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What tools measure intersection math quality - justify your answer with a concrete production example.
**A:** A/B images, per-pixel error maps against reference, and error-vs-samples curves are the quantitative tools for intersection math. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: How do you teach intersection math fundamentals - justify your answer with a concrete production example.
**A:** Start with a pinhole camera and a sphere; every later feature builds on the same try-a-ray, find-an-answer shape of intersection math. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How do you teach intersection math fundamentals - justify your answer with a concrete production example.
**A:** Start with a pinhole camera and a sphere; every later feature builds on the same try-a-ray, find-an-answer shape of intersection math. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What tools measure intersection math quality - justify your answer with a concrete production example.
**A:** A/B images, per-pixel error maps against reference, and error-vs-samples curves are the quantitative tools for intersection math. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What does a rigorous test suite assert about intersection math - justify your answer with a concrete production example.
**A:** Correctness on constructed scenes, performance on a benchmark scene, and stability (no NaN/Inf) across resolution ranges. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does intersection math fit into a modular architecture - justify your answer with a concrete production example.
**A:** As a component behind a stable interface - the renderer calls intersection math and never depends on its implementation details. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: When is brute force acceptable for intersection math - justify your answer with a concrete production example.
**A:** For a handful of primitives or when ray count dominates; then the cost of intersection math acceleration structures exceeds their savings. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What are the output guarantees of intersection math - justify your answer with a concrete production example.
**A:** A per-pixel radiance estimate (and optionally depth/ray state) that downstream tone mapping can trust - the contract of intersection math. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: How do you port intersection math from CPU to GPU - justify your answer with a concrete production example.
**A:** Keep the math identical in device functions, inline the hot loops, and replace heap allocations with pre-allocated buffers for intersection math. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What happens if intersection math is not monotonic with samples - justify your answer with a concrete production example.
**A:** The image converges to the wrong value, revealing a bug; intersection math results must approach a stable limit as sampling grows. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How do you explain intersection math trade-offs on a single slide - justify your answer with a concrete production example.
**A:** A table: approach, cost per ray, memory, robustness, and GPU friendliness - summarize intersection math options in one comparison view. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What is the most common performance trap in intersection math - justify your answer with a concrete production example.
**A:** Recomputing the same expensive data per ray instead of caching it in constant or shared memory before the intersection math loop starts. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What falls in the domain of intersection math vs rendering - justify your answer with a concrete production example.
**A:** intersection math is geometric answer-finding; rendering decides color, lighting, and tone mapping from those answers - keep the boundary clean. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How does intersection math interact with antialiasing - justify your answer with a concrete production example.
**A:** Antialiasing launches many slightly different rays; intersection math must keep their per-ray state separate so samples blend correctly. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What should you test about intersection math - justify your answer with a concrete production example.
**A:** Golden images for a handful of scenes, analytic sizes for primitive shapes, and monotonic quality as samples increase for intersection math. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: Give a production example of intersection math in the black-hole visualizer - justify your answer with a concrete production example.
**A:** Tracing a photon through the accretion flow uses intersection math at every step: intersect the disk plane, sample the field, and terminate at horizon or sky. A concrete example: consistently applying intersection math in code review and regression tests keeps the whole pipeline trustworthy.
