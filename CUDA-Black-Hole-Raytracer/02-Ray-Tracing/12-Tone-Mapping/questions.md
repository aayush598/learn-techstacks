# Ray Tracing — Tone Mapping Interview Questions and Answers

## Q1: What is tone mapping?
**A:** Mapping unbounded linear radiance to a displayable [0,1] range while preserving perceptual contrast and highlights - the final stage before 8-bit encoding.

## Q2: What is the simplest (Reinhard) operator?
**A:** c_out = c/(1+c) preserving ratios (values <1 darken, >1 saturate toward 1); parameterizable by exposure and 'white point' version safe for cheap shots.

## Q3: What is the filmic/ACES tone mapping?
**A:** A response curve copied from film (ACES fit) that rolls off highlights gracefully - the standard look for cinematic renders.

## Q4: Why apply the exposure BEFORE tone mapping?
**A:** Exposure (a multiplicative gain) changes what the curve shows; the pipeline computes exposure from the histogram, multiplies, then curve-transforms.

## Q5: What is auto-exposure?
**A:** A percentile of the brightness histogram (e.g., p95) sets gain so the frame's key brightness lands mid-range; -consistency across frames needs the percentile from a tracked metric.

## Q6: What is the brightness histogram for?
**A:** auto-exposure: build log-intensity histogram, pick the high-percentile, set gain = target/percentile - robust across dynamic frames.

## Q7: What are the standard display gamma values?
**A:** sRGB EOTF (~2.2 curve, ~1/2.4 power), Rec.709 (same OETF), and D65 white point; encode to the target color space at the last step.

## Q8: How do you preserve highlights vs clipping?
**A:** A roll-off operator (film) compresses extremes without a hard clip; hard clipping at 1 loses detail in the ring's brightest fibers - visually annoying.

## Q9: What is color grading in tone mapping?
**A:** Perceptual LUTs (look, shadow/midtone/highlight) applied after the base curve - where 'style' lives, separate from the physics pipeline.

## Q10: How does tone mapping affect the photon ring visibility?
**A:** The faint outer wings gain contrast from a filmic roll-off while the bright inner ring holds - a well-identical curve changes which detail reads as 'ring'.

## Q11: What is the dark-surround (local) tone mapping?
**A:** Operators that adapt locally per-region (e.g., local Reinhard) - more contrast but halos at edges; avoid for science stills, keep for style.

## Q12: What is the correct sequence in the pipeline?
**A:** linear accumulate -> exposure -> (perceptual LUT) -> tone curve -> encode sRGB -> save PNG; never reverse the order of value transform.

## Q13: How do you verify tone mapping is neutral?
**A:** Render a mid-gray (0.18) scene: after exposure+curve it must map to ~0.18 in sRGB; a fixed gray patch test pins the operator's parameters.

## Q14: How do you keep tone mapping parameters reproducible?
**A:** Record exposure + curve name + LUT in the frame's metadata; a movie that varies exposure per frame needs the tracked percentile stored too.

## Q15: What is the purpose of tone mapping in a raytracer?
**A:** It defines how geometric questions are answered for each pixel ray, converting abstract scene data into visible color contributions.

## Q16: Why does tone mapping matter more in a GPU raytracer?
**A:** Because millions of rays run concurrently; tone mapping determines whether each thread can proceed independently or stalls on divergent geometry work.

## Q17: Describe the main correctness concern in tone mapping.
**A:** Precision: numerically unstable tone mapping causes gaps, shadow acne, and flicker; consistently evaluate in double or carefully-ordered floats.

## Q18: How does tone mapping affect perceptual quality?
**A:** Small errors in tone mapping show up as aliasing, hard shadows, or wrong silhouettes long before an average viewer can name the cause.

## Q19: What is the standard way to structure tone mapping code?
**A:** Separate pure functions (no state) so tone mapping compiles to fast device code and can be unit-tested on the host with the same inputs.

## Q20: How do you benchmark tone mapping?
**A:** Render a fixed scene at multiple resolutions, measure rays/second, and compare against an analytic ground truth for identical camera settings.

## Q21: When does tone mapping produce artifacts?
**A:** When step sizes, tolerances, or intersection epsilons are tuned wrong - the classic acne/darkening trade-off of tone mapping.

## Q22: How should tone mapping handle edge cases like grazing angles?
**A:** Use robust predicates and minimum epsilon displacements so tone mapping stays stable exactly where classic plane tests degenerate.

## Q23: What relationship does tone mapping have with the rest of the pipeline?
**A:** tone mapping produces the input for shading and post-processing; any error here is amplified by everything downstream.

## Q24: How do you make tone mapping deterministic across runs?
**A:** Fix the accumulation order and sampling seed per pixel so tone mapping reproduces bit-identical output for the same scene and parameters.

## Q25: Give a production example of tone mapping in the black-hole visualizer.
**A:** Tracing a photon through the accretion flow uses tone mapping at every step: intersect the disk plane, sample the field, and terminate at horizon or sky.

## Q26: What should you test about tone mapping?
**A:** Golden images for a handful of scenes, analytic sizes for primitive shapes, and monotonic quality as samples increase for tone mapping.

## Q27: How does tone mapping interact with antialiasing?
**A:** Antialiasing launches many slightly different rays; tone mapping must keep their per-ray state separate so samples blend correctly.

## Q28: What falls in the domain of tone mapping vs rendering?
**A:** tone mapping is geometric answer-finding; rendering decides color, lighting, and tone mapping from those answers - keep the boundary clean.

## Q29: What is the most common performance trap in tone mapping?
**A:** Recomputing the same expensive data per ray instead of caching it in constant or shared memory before the tone mapping loop starts.

## Q30: How do you explain tone mapping trade-offs on a single slide?
**A:** A table: approach, cost per ray, memory, robustness, and GPU friendliness - summarize tone mapping options in one comparison view.

## Q31: What happens if tone mapping is not monotonic with samples?
**A:** The image converges to the wrong value, revealing a bug; tone mapping results must approach a stable limit as sampling grows.

## Q32: How do you port tone mapping from CPU to GPU?
**A:** Keep the math identical in device functions, inline the hot loops, and replace heap allocations with pre-allocated buffers for tone mapping.

## Q33: What are the output guarantees of tone mapping?
**A:** A per-pixel radiance estimate (and optionally depth/ray state) that downstream tone mapping can trust - the contract of tone mapping.

## Q34: When is brute force acceptable for tone mapping?
**A:** For a handful of primitives or when ray count dominates; then the cost of tone mapping acceleration structures exceeds their savings.

## Q35: How does tone mapping fit into a modular architecture?
**A:** As a component behind a stable interface - the renderer calls tone mapping and never depends on its implementation details.

## Q36: What does a rigorous test suite assert about tone mapping?
**A:** Correctness on constructed scenes, performance on a benchmark scene, and stability (no NaN/Inf) across resolution ranges.

## Q37: What tools measure tone mapping quality?
**A:** A/B images, per-pixel error maps against reference, and error-vs-samples curves are the quantitative tools for tone mapping.

## Q38: How do you teach tone mapping fundamentals?
**A:** Start with a pinhole camera and a sphere; every later feature builds on the same try-a-ray, find-an-answer shape of tone mapping.

## Q39: How do you teach tone mapping fundamentals - justify your answer with a concrete production example.
**A:** Start with a pinhole camera and a sphere; every later feature builds on the same try-a-ray, find-an-answer shape of tone mapping. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q40: What tools measure tone mapping quality - justify your answer with a concrete production example.
**A:** A/B images, per-pixel error maps against reference, and error-vs-samples curves are the quantitative tools for tone mapping. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q41: What does a rigorous test suite assert about tone mapping - justify your answer with a concrete production example.
**A:** Correctness on constructed scenes, performance on a benchmark scene, and stability (no NaN/Inf) across resolution ranges. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q42: How does tone mapping fit into a modular architecture - justify your answer with a concrete production example.
**A:** As a component behind a stable interface - the renderer calls tone mapping and never depends on its implementation details. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q43: When is brute force acceptable for tone mapping - justify your answer with a concrete production example.
**A:** For a handful of primitives or when ray count dominates; then the cost of tone mapping acceleration structures exceeds their savings. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q44: What are the output guarantees of tone mapping - justify your answer with a concrete production example.
**A:** A per-pixel radiance estimate (and optionally depth/ray state) that downstream tone mapping can trust - the contract of tone mapping. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q45: How do you port tone mapping from CPU to GPU - justify your answer with a concrete production example.
**A:** Keep the math identical in device functions, inline the hot loops, and replace heap allocations with pre-allocated buffers for tone mapping. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q46: What happens if tone mapping is not monotonic with samples - justify your answer with a concrete production example.
**A:** The image converges to the wrong value, revealing a bug; tone mapping results must approach a stable limit as sampling grows. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q47: How do you explain tone mapping trade-offs on a single slide - justify your answer with a concrete production example.
**A:** A table: approach, cost per ray, memory, robustness, and GPU friendliness - summarize tone mapping options in one comparison view. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q48: What is the most common performance trap in tone mapping - justify your answer with a concrete production example.
**A:** Recomputing the same expensive data per ray instead of caching it in constant or shared memory before the tone mapping loop starts. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q49: What falls in the domain of tone mapping vs rendering - justify your answer with a concrete production example.
**A:** tone mapping is geometric answer-finding; rendering decides color, lighting, and tone mapping from those answers - keep the boundary clean. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q50: How does tone mapping interact with antialiasing - justify your answer with a concrete production example.
**A:** Antialiasing launches many slightly different rays; tone mapping must keep their per-ray state separate so samples blend correctly. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q51: What should you test about tone mapping - justify your answer with a concrete production example.
**A:** Golden images for a handful of scenes, analytic sizes for primitive shapes, and monotonic quality as samples increase for tone mapping. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q52: Give a production example of tone mapping in the black-hole visualizer - justify your answer with a concrete production example.
**A:** Tracing a photon through the accretion flow uses tone mapping at every step: intersect the disk plane, sample the field, and terminate at horizon or sky. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q53: How do you make tone mapping deterministic across runs - justify your answer with a concrete production example.
**A:** Fix the accumulation order and sampling seed per pixel so tone mapping reproduces bit-identical output for the same scene and parameters. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q54: What relationship does tone mapping have with the rest of the pipeline - justify your answer with a concrete production example.
**A:** tone mapping produces the input for shading and post-processing; any error here is amplified by everything downstream. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q55: How should tone mapping handle edge cases like grazing angles - justify your answer with a concrete production example.
**A:** Use robust predicates and minimum epsilon displacements so tone mapping stays stable exactly where classic plane tests degenerate. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q56: When does tone mapping produce artifacts - justify your answer with a concrete production example.
**A:** When step sizes, tolerances, or intersection epsilons are tuned wrong - the classic acne/darkening trade-off of tone mapping. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q57: How do you benchmark tone mapping - justify your answer with a concrete production example.
**A:** Render a fixed scene at multiple resolutions, measure rays/second, and compare against an analytic ground truth for identical camera settings. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q58: What is the standard way to structure tone mapping code - justify your answer with a concrete production example.
**A:** Separate pure functions (no state) so tone mapping compiles to fast device code and can be unit-tested on the host with the same inputs. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q59: How does tone mapping affect perceptual quality - justify your answer with a concrete production example.
**A:** Small errors in tone mapping show up as aliasing, hard shadows, or wrong silhouettes long before an average viewer can name the cause. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q60: Describe the main correctness concern in tone mapping - justify your answer with a concrete production example.
**A:** Precision: numerically unstable tone mapping causes gaps, shadow acne, and flicker; consistently evaluate in double or carefully-ordered floats. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q61: Why does tone mapping matter more in a GPU raytracer - justify your answer with a concrete production example.
**A:** Because millions of rays run concurrently; tone mapping determines whether each thread can proceed independently or stalls on divergent geometry work. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q62: What is the purpose of tone mapping in a raytracer - justify your answer with a concrete production example.
**A:** It defines how geometric questions are answered for each pixel ray, converting abstract scene data into visible color contributions. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q63: What is the purpose of tone mapping in a raytracer - justify your answer with a concrete production example.
**A:** It defines how geometric questions are answered for each pixel ray, converting abstract scene data into visible color contributions. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q64: Why does tone mapping matter more in a GPU raytracer - justify your answer with a concrete production example.
**A:** Because millions of rays run concurrently; tone mapping determines whether each thread can proceed independently or stalls on divergent geometry work. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q65: Describe the main correctness concern in tone mapping - justify your answer with a concrete production example.
**A:** Precision: numerically unstable tone mapping causes gaps, shadow acne, and flicker; consistently evaluate in double or carefully-ordered floats. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q66: How does tone mapping affect perceptual quality - justify your answer with a concrete production example.
**A:** Small errors in tone mapping show up as aliasing, hard shadows, or wrong silhouettes long before an average viewer can name the cause. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q67: What is the standard way to structure tone mapping code - justify your answer with a concrete production example.
**A:** Separate pure functions (no state) so tone mapping compiles to fast device code and can be unit-tested on the host with the same inputs. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q68: How do you benchmark tone mapping - justify your answer with a concrete production example.
**A:** Render a fixed scene at multiple resolutions, measure rays/second, and compare against an analytic ground truth for identical camera settings. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q69: When does tone mapping produce artifacts - justify your answer with a concrete production example.
**A:** When step sizes, tolerances, or intersection epsilons are tuned wrong - the classic acne/darkening trade-off of tone mapping. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q70: How should tone mapping handle edge cases like grazing angles - justify your answer with a concrete production example.
**A:** Use robust predicates and minimum epsilon displacements so tone mapping stays stable exactly where classic plane tests degenerate. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q71: What relationship does tone mapping have with the rest of the pipeline - justify your answer with a concrete production example.
**A:** tone mapping produces the input for shading and post-processing; any error here is amplified by everything downstream. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q72: How do you make tone mapping deterministic across runs - justify your answer with a concrete production example.
**A:** Fix the accumulation order and sampling seed per pixel so tone mapping reproduces bit-identical output for the same scene and parameters. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q73: Give a production example of tone mapping in the black-hole visualizer - justify your answer with a concrete production example.
**A:** Tracing a photon through the accretion flow uses tone mapping at every step: intersect the disk plane, sample the field, and terminate at horizon or sky. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q74: What should you test about tone mapping - justify your answer with a concrete production example.
**A:** Golden images for a handful of scenes, analytic sizes for primitive shapes, and monotonic quality as samples increase for tone mapping. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q75: How does tone mapping interact with antialiasing - justify your answer with a concrete production example.
**A:** Antialiasing launches many slightly different rays; tone mapping must keep their per-ray state separate so samples blend correctly. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q76: What falls in the domain of tone mapping vs rendering - justify your answer with a concrete production example.
**A:** tone mapping is geometric answer-finding; rendering decides color, lighting, and tone mapping from those answers - keep the boundary clean. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q77: What is the most common performance trap in tone mapping - justify your answer with a concrete production example.
**A:** Recomputing the same expensive data per ray instead of caching it in constant or shared memory before the tone mapping loop starts. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q78: How do you explain tone mapping trade-offs on a single slide - justify your answer with a concrete production example.
**A:** A table: approach, cost per ray, memory, robustness, and GPU friendliness - summarize tone mapping options in one comparison view. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q79: What happens if tone mapping is not monotonic with samples - justify your answer with a concrete production example.
**A:** The image converges to the wrong value, revealing a bug; tone mapping results must approach a stable limit as sampling grows. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q80: How do you port tone mapping from CPU to GPU - justify your answer with a concrete production example.
**A:** Keep the math identical in device functions, inline the hot loops, and replace heap allocations with pre-allocated buffers for tone mapping. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q81: What are the output guarantees of tone mapping - justify your answer with a concrete production example.
**A:** A per-pixel radiance estimate (and optionally depth/ray state) that downstream tone mapping can trust - the contract of tone mapping. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q82: When is brute force acceptable for tone mapping - justify your answer with a concrete production example.
**A:** For a handful of primitives or when ray count dominates; then the cost of tone mapping acceleration structures exceeds their savings. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q83: How does tone mapping fit into a modular architecture - justify your answer with a concrete production example.
**A:** As a component behind a stable interface - the renderer calls tone mapping and never depends on its implementation details. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q84: What does a rigorous test suite assert about tone mapping - justify your answer with a concrete production example.
**A:** Correctness on constructed scenes, performance on a benchmark scene, and stability (no NaN/Inf) across resolution ranges. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q85: What tools measure tone mapping quality - justify your answer with a concrete production example.
**A:** A/B images, per-pixel error maps against reference, and error-vs-samples curves are the quantitative tools for tone mapping. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q86: How do you teach tone mapping fundamentals - justify your answer with a concrete production example.
**A:** Start with a pinhole camera and a sphere; every later feature builds on the same try-a-ray, find-an-answer shape of tone mapping. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q87: How do you teach tone mapping fundamentals - justify your answer with a concrete production example.
**A:** Start with a pinhole camera and a sphere; every later feature builds on the same try-a-ray, find-an-answer shape of tone mapping. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q88: What tools measure tone mapping quality - justify your answer with a concrete production example.
**A:** A/B images, per-pixel error maps against reference, and error-vs-samples curves are the quantitative tools for tone mapping. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q89: What does a rigorous test suite assert about tone mapping - justify your answer with a concrete production example.
**A:** Correctness on constructed scenes, performance on a benchmark scene, and stability (no NaN/Inf) across resolution ranges. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q90: How does tone mapping fit into a modular architecture - justify your answer with a concrete production example.
**A:** As a component behind a stable interface - the renderer calls tone mapping and never depends on its implementation details. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q91: When is brute force acceptable for tone mapping - justify your answer with a concrete production example.
**A:** For a handful of primitives or when ray count dominates; then the cost of tone mapping acceleration structures exceeds their savings. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q92: What are the output guarantees of tone mapping - justify your answer with a concrete production example.
**A:** A per-pixel radiance estimate (and optionally depth/ray state) that downstream tone mapping can trust - the contract of tone mapping. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q93: How do you port tone mapping from CPU to GPU - justify your answer with a concrete production example.
**A:** Keep the math identical in device functions, inline the hot loops, and replace heap allocations with pre-allocated buffers for tone mapping. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q94: What happens if tone mapping is not monotonic with samples - justify your answer with a concrete production example.
**A:** The image converges to the wrong value, revealing a bug; tone mapping results must approach a stable limit as sampling grows. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q95: How do you explain tone mapping trade-offs on a single slide - justify your answer with a concrete production example.
**A:** A table: approach, cost per ray, memory, robustness, and GPU friendliness - summarize tone mapping options in one comparison view. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q96: What is the most common performance trap in tone mapping - justify your answer with a concrete production example.
**A:** Recomputing the same expensive data per ray instead of caching it in constant or shared memory before the tone mapping loop starts. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q97: What falls in the domain of tone mapping vs rendering - justify your answer with a concrete production example.
**A:** tone mapping is geometric answer-finding; rendering decides color, lighting, and tone mapping from those answers - keep the boundary clean. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q98: How does tone mapping interact with antialiasing - justify your answer with a concrete production example.
**A:** Antialiasing launches many slightly different rays; tone mapping must keep their per-ray state separate so samples blend correctly. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q99: What should you test about tone mapping - justify your answer with a concrete production example.
**A:** Golden images for a handful of scenes, analytic sizes for primitive shapes, and monotonic quality as samples increase for tone mapping. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.

## Q100: Give a production example of tone mapping in the black-hole visualizer - justify your answer with a concrete production example.
**A:** Tracing a photon through the accretion flow uses tone mapping at every step: intersect the disk plane, sample the field, and terminate at horizon or sky. A concrete example: consistently applying tone mapping in code review and regression tests keeps the whole pipeline trustworthy.
